from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3
from typing import Any


@dataclass
class GuidMatch:
    guid: str
    name: str
    object_type: str
    owner: str = ""
    package: str = ""
    stereotype: str = ""
    confidence: str = "low"


@dataclass
class GuidValidationResult:
    guid: str
    exists: bool
    object_type: str = ""
    name: str = ""
    owner: str = ""
    package: str = ""


class SQLiteAdapter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.conn: sqlite3.Connection | None = None

    def connect(self) -> None:
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def fetchall(self, query: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
        if self.conn is None:
            raise RuntimeError("SQLite adapter is not connected")
        cur = self.conn.execute(query, params)
        return [dict(row) for row in cur.fetchall()]


class AccessAdapter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.conn = None

    def connect(self) -> None:
        try:
            import pyodbc  # type: ignore
        except Exception as exc:
            raise RuntimeError("pyodbc is required for .eap/.eapx Access lookup") from exc

        conn_str = (
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            + f"DBQ={self.path};"
        )
        self.conn = pyodbc.connect(conn_str)

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def fetchall(self, query: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
        if self.conn is None:
            raise RuntimeError("Access adapter is not connected")
        cur = self.conn.cursor()
        cur.execute(query, params)
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        return [{cols[i]: row[i] for i in range(len(cols))} for row in rows]


class ComAdapter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.repository = None

    def connect(self) -> None:
        try:
            import win32com.client  # type: ignore
        except Exception as exc:
            raise RuntimeError("pywin32 is required for Enterprise Architect COM lookup") from exc

        repo = win32com.client.Dispatch("EA.Repository")
        if not repo.OpenFile(str(self.path)):
            raise RuntimeError(f"Unable to open EA repository via COM: {self.path}")
        self.repository = repo

    def close(self) -> None:
        if self.repository is not None:
            try:
                self.repository.CloseFile()
                self.repository.Exit()
            finally:
                self.repository = None

    def fetchall(self, query: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
        if self.repository is None:
            raise RuntimeError("COM adapter is not connected")
        if params:
            for value in params:
                safe = str(value).replace("'", "''")
                query = query.replace("?", f"'{safe}'", 1)
        xml = self.repository.SQLQuery(query)
        import xml.etree.ElementTree as ET

        rows: list[dict[str, Any]] = []
        root = ET.fromstring(xml)
        dataset = root.find("Data")
        if dataset is None:
            return rows
        for row in dataset:
            rows.append({child.tag: child.text for child in row})
        return rows


class EapxGuidExtractor:
    def __init__(self, path: str | Path, backend: str = "auto"):
        self.path = Path(path)
        self.backend = backend
        self.adapter: SQLiteAdapter | AccessAdapter | ComAdapter | None = None

    def __enter__(self) -> EapxGuidExtractor:
        self._connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.adapter is not None:
            self.adapter.close()

    def _pick_backend(self) -> str:
        if self.backend != "auto":
            return self.backend
        suffix = self.path.suffix.lower()
        if suffix in {".qea", ".qeax"}:
            return "sqlite"
        if suffix in {".eap", ".eapx"}:
            return "access"
        return "sqlite"

    def _connect(self) -> None:
        selected = self._pick_backend()
        if selected == "sqlite":
            self.adapter = SQLiteAdapter(self.path)
        elif selected == "access":
            self.adapter = AccessAdapter(self.path)
        elif selected == "com":
            self.adapter = ComAdapter(self.path)
        else:
            raise ValueError(f"Unsupported backend: {selected}")

        self.adapter.connect()

    def _extract_operation_matches(self, operation_name: str) -> list[GuidMatch]:
        if self.adapter is None:
            return []
        query = (
            "SELECT op.ea_guid, op.Name "
            "FROM t_operation AS op "
            "WHERE op.Name = ?"
        )
        rows = self.adapter.fetchall(query, (operation_name,))
        return [
            GuidMatch(
                guid=str(r.get("ea_guid", "")),
                name=str(r.get("Name", "")),
                object_type="operation",
                confidence="high",
            )
            for r in rows
            if r.get("ea_guid")
        ]

    def _extract_object_matches(self, object_name: str) -> list[GuidMatch]:
        if self.adapter is None:
            return []
        query = (
            "SELECT obj.ea_guid, obj.Name "
            "FROM t_object AS obj "
            "WHERE obj.Name = ?"
        )
        rows = self.adapter.fetchall(query, (object_name,))
        return [
            GuidMatch(
                guid=str(r.get("ea_guid", "")),
                name=str(r.get("Name", "")),
                object_type="object",
                confidence="medium",
            )
            for r in rows
            if r.get("ea_guid")
        ]

    def extract_guid_matches(
        self,
        name: str,
        *,
        owner: str | None = None,
        package: str | None = None,
        stereotype: str | None = None,
    ) -> list[GuidMatch]:
        matches = self._extract_operation_matches(name)
        if not matches:
            matches = self._extract_object_matches(name)

        if owner:
            owner_lower = owner.lower()
            scoped = [m for m in matches if m.owner.lower() == owner_lower]
            if scoped:
                matches = scoped
        if package:
            package_lower = package.lower()
            scoped = [m for m in matches if m.package.lower() == package_lower]
            if scoped:
                matches = scoped
        if stereotype:
            stereotype_lower = stereotype.lower()
            scoped = [m for m in matches if m.stereotype.lower() == stereotype_lower]
            if scoped:
                matches = scoped

        return matches

    def extract_guid(
        self,
        name: str,
        *,
        owner: str | None = None,
        package: str | None = None,
        stereotype: str | None = None,
    ) -> str | None:
        matches = self.extract_guid_matches(name, owner=owner, package=package, stereotype=stereotype)
        if len(matches) == 1:
            return matches[0].guid
        return None

    def validate_guid(self, guid: str) -> GuidValidationResult:
        if self.adapter is None:
            return GuidValidationResult(guid=guid, exists=False)

        query_operation = (
            "SELECT op.ea_guid, op.Name "
            "FROM t_operation AS op "
            "WHERE op.ea_guid = ?"
        )
        rows = self.adapter.fetchall(query_operation, (guid,))
        if rows:
            row = rows[0]
            return GuidValidationResult(
                guid=guid,
                exists=True,
                object_type="operation",
                name=str(row.get("Name", "")),
            )

        query_object = (
            "SELECT obj.ea_guid, obj.Name "
            "FROM t_object AS obj "
            "WHERE obj.ea_guid = ?"
        )
        rows = self.adapter.fetchall(query_object, (guid,))
        if rows:
            row = rows[0]
            return GuidValidationResult(
                guid=guid,
                exists=True,
                object_type="object",
                name=str(row.get("Name", "")),
            )

        return GuidValidationResult(guid=guid, exists=False)


class EAGuidExtractor(EapxGuidExtractor):
    pass
