"""
Data management for structured content (tables, metadata, etc.)
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class DataManager:
    """Manage YAML/JSON data files for tables and structured content"""
    
    def __init__(self, data_dir: Path):
        """
        Initialize data manager
        
        Args:
            data_dir: Directory containing YAML/JSON data files
        """
        self.data_dir = Path(data_dir)
        self.cache: Dict[str, Any] = {}
    
    def load_data(self, filename: str) -> Dict[str, Any]:
        """Load data from YAML or JSON file"""
        if filename in self.cache:
            return self.cache[filename]
        
        file_path = self.data_dir / filename
        
        if file_path.suffix in ['.yml', '.yaml']:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        self.cache[filename] = data
        return data
    
    def render_table(self, data: Dict[str, Any], format: str = 'html') -> str:
        """
        Render table data to specified format
        
        Args:
            data: Table data dictionary
            format: Output format ('html', 'markdown', 'latex')
        
        Returns:
            Rendered table string
        """
        if format == 'html':
            return self._render_html_table(data)
        elif format == 'markdown':
            return self._render_markdown_table(data)
        elif format == 'latex':
            return self._render_latex_table(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _render_html_table(self, data: Dict[str, Any]) -> str:
        """Render table as HTML"""
        headers = data.get('headers', [])
        rows = data.get('rows', [])
        caption = data.get('caption', '')
        
        html = []
        html.append('<table class="data-table">')
        
        if caption:
            html.append(f'<caption>{caption}</caption>')
        
        # Headers
        if headers:
            html.append('<thead>')
            html.append('<tr>')
            for header in headers:
                html.append(f'<th>{header}</th>')
            html.append('</tr>')
            html.append('</thead>')
        
        # Body
        html.append('<tbody>')
        for row in rows:
            html.append('<tr>')
            for cell in row:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')
        
        html.append('</table>')
        return '\n'.join(html)
    
    def _render_markdown_table(self, data: Dict[str, Any]) -> str:
        """Render table as Markdown"""
        headers = data.get('headers', [])
        rows = data.get('rows', [])
        caption = data.get('caption', '')
        
        lines = []
        
        if caption:
            lines.append(f"*{caption}*")
            lines.append("")
        
        # Headers
        if headers:
            lines.append('| ' + ' | '.join(str(h) for h in headers) + ' |')
            lines.append('|' + '|'.join(['---'] * len(headers)) + '|')
        
        # Rows
        for row in rows:
            lines.append('| ' + ' | '.join(str(cell) for cell in row) + ' |')
        
        return '\n'.join(lines)
    
    def _render_latex_table(self, data: Dict[str, Any]) -> str:
        """Render table as LaTeX"""
        headers = data.get('headers', [])
        rows = data.get('rows', [])
        caption = data.get('caption', '')
        
        lines = []
        
        # Calculate column spec
        num_cols = len(headers) if headers else len(rows[0]) if rows else 0
        col_spec = 'l' * num_cols
        
        lines.append('\\begin{table}[h]')
        lines.append('\\centering')
        lines.append(f'\\begin{{tabular}}{{{col_spec}}}')
        lines.append('\\toprule')
        
        # Headers
        if headers:
            lines.append(' & '.join(str(h) for h in headers) + ' \\\\')
            lines.append('\\midrule')
        
        # Rows
        for row in rows:
            lines.append(' & '.join(str(cell) for cell in row) + ' \\\\')
        
        lines.append('\\bottomrule')
        lines.append('\\end{tabular}')
        
        if caption:
            lines.append(f'\\caption{{{caption}}}')
        
        lines.append('\\end{table}')
        
        return '\n'.join(lines)