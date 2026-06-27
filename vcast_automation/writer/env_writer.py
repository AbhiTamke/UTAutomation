"""
env_writer.py — VectorCAST .env file generation from templates.

Generates environment configuration files for test execution.
"""

from __future__ import annotations

from pathlib import Path


def render_env(
    source_model,
    plans: list,
    context: dict,
) -> str:
    """
    Generate .env file content from test plans and context.
    
    Args:
        source_model: Source file being tested.
        plans: List of test plans.
        context: Execution context (compiler, platform, etc).
    
    Returns:
        .env file content as string.
    """
    lines = []
    
    # Header
    lines.append("// Environment file for VectorCAST")
    lines.append(f"// Source: {source_model.source_path}")
    lines.append(f"// Generated environment")
    lines.append("")
    
    # Compiler info
    lines.append("[Compiler]")
    compiler = context.get("compiler", "generic")
    lines.append(f"Name={compiler}")
    lines.append(f"Version={context.get('compiler_version', 'unknown')}")
    lines.append("")
    
    # Platform info
    lines.append("[Platform]")
    lines.append(f"Name={context.get('platform', 'generic')}")
    lines.append(f"Architecture={context.get('arch', 'x86_64')}")
    lines.append(f"Bits={context.get('bits', 64)}")
    lines.append("")
    
    # Execution settings
    lines.append("[Execution]")
    lines.append("Timeout=30000")
    lines.append("MaxTests=100")
    lines.append("CoverageMode=statement")
    lines.append("")
    
    # Include paths
    if hasattr(source_model, 'includes') and source_model.includes:
        lines.append("[IncludePaths]")
        for inc in source_model.includes[:5]:  # First 5 includes
            lines.append(f"Path={inc}")
        lines.append("")
    
    # Defines/Macros
    if hasattr(source_model, 'macros') and source_model.macros:
        lines.append("[Defines]")
        for macro in source_model.macros[:10]:  # First 10 macros
            lines.append(f"Define={macro}")
        lines.append("")
    
    # Stubs
    lines.append("[Stubs]")
    if source_model.functions:
        fn = source_model.functions[0]
        for stub in fn.external_calls[:5]:
            lines.append(f"Stub={stub}")
    lines.append("")
    
    return "\n".join(lines)


def write_env(output_path: str, content: str) -> str:
    """
    Write .env file to disk.
    
    Args:
        output_path: Path to write .env file.
        content: .env file content.
    
    Returns:
        Path that was written.
    """
    output_path = str(output_path).replace(".tst", ".env")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return str(path)
