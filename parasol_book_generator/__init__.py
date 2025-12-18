"""
Parasol V5 Book Generator Module

A comprehensive book generation system that supports:
- Multiple output formats (HTML, PDF)
- Mermaid diagram rendering
- YAML-based data management
- Consistent formatting across formats
"""

from .generator import ParasolBookGenerator
from .converters import MarkdownConverter, HTMLBuilder, PDFBuilder
from .data_manager import DataManager
from .diagram_renderer import DiagramRenderer

__version__ = "1.0.0"
__all__ = [
    "ParasolBookGenerator",
    "MarkdownConverter",
    "HTMLBuilder",
    "PDFBuilder",
    "DataManager",
    "DiagramRenderer",
]