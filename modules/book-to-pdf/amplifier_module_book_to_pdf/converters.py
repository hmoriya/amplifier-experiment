"""
Markdown to HTML converters for book-to-pdf.

Handles conversion of Markdown content to HTML with support for:
- Syntax highlighting
- Mermaid diagrams
- Japanese text
- Custom extensions
"""

import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from rich.console import Console

console = Console()


class MermaidPreprocessor(Preprocessor):
    """Convert Mermaid diagrams to images"""
    
    def run(self, lines):
        new_lines = []
        in_mermaid = False
        mermaid_content = []
        
        for line in lines:
            if line.strip() == '```mermaid':
                in_mermaid = True
                mermaid_content = []
            elif in_mermaid and line.strip() == '```':
                # Process mermaid content
                in_mermaid = False
                diagram = '\n'.join(mermaid_content)
                img_tag = self.convert_mermaid(diagram)
                new_lines.append(img_tag)
            elif in_mermaid:
                mermaid_content.append(line)
            else:
                new_lines.append(line)
        
        return new_lines
    
    def convert_mermaid(self, diagram: str) -> str:
        """Convert Mermaid diagram to image tag"""
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(diagram)
                mmd_file = f.name
            
            png_file = mmd_file.replace('.mmd', '.png')
            
            # Try to use mmdc (Mermaid CLI)
            result = subprocess.run(
                ['mmdc', '-i', mmd_file, '-o', png_file, '-b', 'white'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and Path(png_file).exists():
                # Read and embed as base64
                import base64
                with open(png_file, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode()
                
                # Clean up
                Path(mmd_file).unlink()
                Path(png_file).unlink()
                
                return f'<img src="data:image/png;base64,{img_data}" class="mermaid-diagram" />'
            else:
                # Fallback: render as code block
                console.print("[yellow]Warning: Mermaid CLI not available, rendering as code block[/yellow]")
                return f'<pre class="mermaid-fallback"><code>{diagram}</code></pre>'
                
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to convert Mermaid diagram: {e}[/yellow]")
            return f'<pre class="mermaid-fallback"><code>{diagram}</code></pre>'


class MermaidExtension(Extension):
    """Markdown extension for Mermaid support"""
    
    def extendMarkdown(self, md):
        md.preprocessors.register(MermaidPreprocessor(md), 'mermaid', 175)


class MarkdownConverter:
    """Convert Markdown to HTML with enhanced features"""
    
    def __init__(self):
        self.md = markdown.Markdown(
            extensions=[
                'fenced_code',
                'tables',
                'toc',
                'attr_list',
                'def_list',
                'footnotes',
                'meta',
                'codehilite',
                'nl2br',
                MermaidExtension(),
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'linenums': False,
                    'guess_lang': True,
                },
                'toc': {
                    'permalink': True,
                    'permalink_class': 'toc-anchor',
                    'permalink_title': 'リンク',
                },
            }
        )
        
        # Custom code block handler
        self.code_pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
        
    def convert(self, content: str) -> str:
        """Convert Markdown content to HTML"""
        # Pre-process code blocks for better syntax highlighting
        content = self.process_code_blocks(content)
        
        # Convert to HTML
        html = self.md.convert(content)
        
        # Post-process for Japanese typography
        html = self.improve_japanese_typography(html)
        
        # Reset the Markdown instance for next conversion
        self.md.reset()
        
        return html
    
    def process_code_blocks(self, content: str) -> str:
        """Process code blocks with syntax highlighting"""
        def replace_code_block(match):
            lang = match.group(1) or 'text'
            code = match.group(2)
            
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except:
                lexer = TextLexer()
            
            formatter = HtmlFormatter(cssclass='highlight', style='monokai')
            highlighted = highlight(code, lexer, formatter)
            
            return f'<div class="code-block code-{lang}">{highlighted}</div>'
        
        # Only process non-mermaid code blocks
        lines = content.split('\n')
        result = []
        in_code = False
        code_lang = None
        code_lines = []
        
        for line in lines:
            if line.strip().startswith('```'):
                if not in_code:
                    in_code = True
                    code_lang = line.strip()[3:].strip()
                    code_lines = []
                else:
                    in_code = False
                    if code_lang != 'mermaid':
                        # Process non-mermaid code block
                        code_content = '\n'.join(code_lines)
                        try:
                            lexer = get_lexer_by_name(code_lang or 'text', stripall=True)
                        except:
                            lexer = TextLexer()
                        
                        formatter = HtmlFormatter(cssclass='highlight', style='monokai')
                        highlighted = highlight(code_content, lexer, formatter)
                        result.append(f'<div class="code-block code-{code_lang or "text"}">{highlighted}</div>')
                    else:
                        # Keep mermaid blocks as-is for MermaidPreprocessor
                        result.append(f'```{code_lang}')
                        result.extend(code_lines)
                        result.append('```')
            elif in_code:
                code_lines.append(line)
            else:
                result.append(line)
        
        return '\n'.join(result)
    
    def improve_japanese_typography(self, html: str) -> str:
        """Improve Japanese typography in HTML"""
        # Add word-break for long Japanese text
        html = html.replace('<p>', '<p class="jp-text">')
        html = html.replace('<li>', '<li class="jp-text">')
        
        # Ensure proper spacing around inline code
        html = re.sub(r'([ぁ-んァ-ヶー一-龠]+)<code>', r'\1 <code>', html)
        html = re.sub(r'</code>([ぁ-んァ-ヶー一-龠]+)', r'</code> \1', html)
        
        return html


class PDFGenerator:
    """Generate PDF from HTML content"""
    
    def __init__(self):
        self.formatter = HtmlFormatter(style='monokai')
        
    def get_syntax_css(self) -> str:
        """Get CSS for syntax highlighting"""
        return self.formatter.get_style_defs('.highlight')
    
    def process_for_print(self, html: str) -> str:
        """Process HTML for better print output"""
        # Add print-specific classes
        html = html.replace('<table>', '<table class="print-table">')
        
        # Ensure images fit on page
        html = re.sub(r'<img ([^>]+)>', r'<img \1 class="print-image">', html)
        
        # Add page breaks before major sections
        html = re.sub(r'<h1', r'<div class="page-break"></div><h1', html)
        
        return html
    
    def add_headers_footers(self, html: str, title: str, page_num: int = 1) -> str:
        """Add headers and footers for PDF"""
        header = f'<div class="pdf-header">{title}</div>'
        footer = f'<div class="pdf-footer">Page <span class="page-num">{page_num}</span></div>'
        
        return f'{header}{html}{footer}'