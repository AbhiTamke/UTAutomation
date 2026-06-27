"""
cfg_writer.py — VectorCAST .cfg file generation from environment profiles.

Generates configuration files based on environment and compiler settings.
"""

from __future__ import annotations

from pathlib import Path


def render_cfg(
    source_model,
    context: dict,
) -> str:
    """
    Generate .cfg file content from environment/compiler profile.
    
    Args:
        source_model: Source file being tested.
        context: Compiler and environment context.
    
    Returns:
        .cfg file content as string.
    """
    lines = []
    
    # Header
    lines.append("/* Configuration file for VectorCAST */")
    lines.append(f"/* Source: {source_model.source_path} */")
    lines.append("")
    
    # Compiler configuration
    compiler = context.get("compiler", "generic")
    lines.append("/* Compiler Configuration */")
    lines.append(f"COMPILER = {compiler}")
    lines.append(f"COMPILER_VERSION = {context.get('compiler_version', '')}")
    lines.append("")
    
    # Optimization
    lines.append("/* Optimization */")
    lines.append(f"OPTIMIZATION_LEVEL = {context.get('optimization', 'O0')}")
    lines.append("")
    
    # Include paths
    lines.append("/* Include Paths */")
    if hasattr(source_model, 'includes'):
        for inc in source_model.includes[:3]:
            lines.append(f"ADD_INCLUDE = {inc}")
    lines.append("")
    
    # Defines
    lines.append("/* Preprocessor Defines */")
    if hasattr(source_model, 'macros'):
        for macro in source_model.macros[:5]:
            lines.append(f"ADD_DEFINE = {macro}")
    lines.append("ADD_DEFINE = VCAST_ENV_GENERATED=1")
    lines.append("")
    
    # Type sizes (platform-specific)
    lines.append("/* Type Sizes */")
    lines.append(f"SIZEOF_INT = {context.get('int_size', 4)}")
    lines.append(f"SIZEOF_LONG = {context.get('long_size', 8)}")
    lines.append(f"SIZEOF_POINTER = {context.get('pointer_size', 8)}")
    lines.append("")
    
    # Coverage
    lines.append("/* Coverage Configuration */")
    lines.append("COVERAGE_MODE = STATEMENT")
    lines.append("TRACK_COVERAGE = TRUE")
    lines.append("")
    
    # Stubs
    lines.append("/* External Stubs */")
    if source_model.functions:
        fn = source_model.functions[0]
        for call in fn.external_calls[:3]:
            lines.append(f"STUB = {call}")
    lines.append("")
    
    return "\n".join(lines)


def write_cfg(output_path: str, content: str) -> str:
    """
    Write .cfg file to disk.
    
    Args:
        output_path: Path to write .cfg file.
        content: .cfg file content.
    
    Returns:
        Path that was written.
    """
    output_path = str(output_path).replace(".tst", ".cfg")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return str(path)
