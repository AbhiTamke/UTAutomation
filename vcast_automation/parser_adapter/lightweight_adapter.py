from __future__ import annotations

from pathlib import Path

from vcast_automation.models.core import SourceFileModel
from vcast_automation.parser_adapter.model_mapper import map_parsed_file_to_source_model
from vcast_automation.parser_engine.lightweight_c_parser import LightweightCParser
from vcast_automation.parser_engine.parser_base import ParserSelector
from vcast_automation.parser_engine.tree_sitter_engine import TreeSitterEngine


class LightweightParserAdapter:
    """
    Backward-compatible adapter name.

    Internally, this now uses:
    1. TreeSitterEngine when available
    2. LightweightCParser fallback
    """

    def __init__(self) -> None:
        self.selector = ParserSelector(
            parsers=[
                TreeSitterEngine(),
                LightweightCParser(),
            ]
        )

    def parse_file(self, source_path: str | Path) -> SourceFileModel:
        parsed = self.selector.parse_file(source_path)
        return map_parsed_file_to_source_model(parsed)