from __future__ import annotations

import abc
import logging
from pathlib import Path

from vcast_automation.parser_engine.code_model import ParsedFile

logger = logging.getLogger(__name__)


class ParserError(RuntimeError):
    """Raised when a parser cannot process a file."""


class ParserBase(abc.ABC):
    """Abstract C/C++ parser."""

    name = "base"

    @abc.abstractmethod
    def available(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def parse_text(self, path: str, text: str, is_header: bool) -> ParsedFile:
        raise NotImplementedError

    def parse_file(self, path: str | Path) -> ParsedFile:
        p = Path(path)
        text = p.read_text(encoding="utf-8", errors="replace")
        is_header = p.suffix.lower() in {".h", ".hpp", ".hh", ".hxx"}
        return self.parse_text(str(p), text, is_header)


class ParserSelector:
    """
    Selects the best available parser.

    The intended order is:
    1. tree_sitter
    2. lightweight fallback
    """

    def __init__(self, parsers: list[ParserBase]):
        self.parsers = parsers

    def parse_file(self, path: str | Path) -> ParsedFile:
        last_result: ParsedFile | None = None

        for parser in self.parsers:
            if not parser.available():
                continue

            result = parser.parse_file(path)
            last_result = result

            if result.parse_ok and result.functions:
                return result

            # Accept header files even if they only contain declarations/types.
            if result.parse_ok and Path(path).suffix.lower() in {".h", ".hpp", ".hh", ".hxx"}:
                return result

        if last_result is not None:
            return last_result

        p = Path(path)
        return ParsedFile(
            path=str(p),
            parser_used="none",
            parse_ok=False,
            warnings=["No parser backend was available."],
        )