"""
Internal parser engine package for vcast_automation.

This package ports the reference parser architecture into vcast_automation
without relying on ea_sdd_generator.* imports.
"""

from vcast_automation.parser_engine.parser_base import ParserSelector
from vcast_automation.parser_engine.lightweight_c_parser import LightweightCParser
from vcast_automation.parser_engine.tree_sitter_engine import TreeSitterEngine

__all__ = [
    "ParserSelector",
    "LightweightCParser",
    "TreeSitterEngine",
]
