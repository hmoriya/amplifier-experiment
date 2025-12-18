"""
Converters for different stages of book generation
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import subprocess
import shutil
import logging

logger = logging.getLogger(__name__)


class MarkdownConverter:
    """Convert and process Markdown content"""
    
    def __init__(self):
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.code_block_pattern = re.compile(r'```(\w*)\n(.*?)\n```', re.DOTALL)
        
    def extract_chapter_info(self, content: str) -> Tuple[Optional[int], Optional[str]]:
        """Extract chapter number and title from content"""
        for match in self.heading_pattern.finditer(content):
            if match.group(1) == '#':  # H1 heading
                title_text = match.group(2).strip()
                # Extract chapter number
                chapter_match = re.match(r'第(\d+)章[\\s　]+(.+)', title_text)
                if chapter_match:
                    return int(chapter_match.group(1)), chapter_match.group(2)
                return None, title_text
        return None, None
    
    def clean_heading_text(self, text: str) -> str:
        """Clean heading text for TOC"""
        # Remove chapter prefix
        text = re.sub(r'^第\d+章[\\s　]+', '', text)
        return text.strip()
    
    def process_code_blocks(self, content: str, escape_html: bool = True) -> Tuple[str, List[str]]:
        """Process code blocks and return content with placeholders"""
        code_blocks = []
        
        def save_code_block(match):
            language = match.group(1) or ''
            code = match.group(2)
            
            if escape_html:
                code = self._escape_html(code)
            
            code_blocks.append({
                'language': language,
                'code': code,
                'original': match.group(0)
            })
            return f'___CODEBLOCK_{len(code_blocks) - 1}___'
        
        processed = self.code_block_pattern.sub(save_code_block, content)
        return processed, code_blocks
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML entities"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text
    
    def process_tables(self, content: str) -> str:
        """Process Markdown tables"""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Check for markdown table
            if '|' in lines[i] and i + 1 < len(lines) and re.match(r'^[\s\-:|]+$', lines[i + 1].replace('|', '')):
                table_lines = []
                # Collect table lines
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                
                # Process table
                result.append(self._convert_markdown_table(table_lines))
            else:
                result.append(lines[i])
                i += 1
        
        return '\n'.join(result)
    
    def _convert_markdown_table(self, lines: List[str]) -> str:
        """Convert markdown table to structured format"""
        # This returns a placeholder that can be processed differently for HTML/PDF
        return f"___TABLE_START___\n" + '\n'.join(lines) + "\n___TABLE_END___"


class HTMLBuilder:
    """Build HTML output"""
    
    def __init__(self, template_path: Optional[Path] = None):
        self.template_path = template_path
        self.default_styles = self._load_default_styles()
    
    def _load_default_styles(self) -> str:
        """Load default CSS styles"""
        return """
        body {
            font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif JP', serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fafafa;
        }
        
        .cover {
            text-align: center;
            padding: 100px 20px;
            page-break-after: always;
            margin-bottom: 50px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        .toc {
            background: white;
            padding: 40px;
            margin: 40px 0;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            page-break-after: always;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: white;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        
        code {
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
        }
        
        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            line-height: 1.4;
        }
        
        .diagram-container {
            margin: 20px 0;
            text-align: center;
        }
        
        .mermaid-diagram {
            max-width: 100%;
            height: auto;
        }
        
        @media print {
            body {
                background-color: white;
                max-width: none;
            }
            .cover, .toc {
                box-shadow: none;
            }
            pre {
                white-space: pre-wrap;
                word-wrap: break-word;
            }
        }
        """
    
    def build_html(self, chapters: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
        """Build complete HTML document"""
        html_parts = []
        
        # Header
        html_parts.append(self._build_header(metadata))
        
        # Cover page
        html_parts.append(self._build_cover(metadata))
        
        # Table of contents
        html_parts.append(self._build_toc(chapters))
        
        # Chapters
        for chapter in chapters:
            html_parts.append(self._build_chapter(chapter))
        
        # Footer
        html_parts.append(self._build_footer())
        
        return '\n'.join(html_parts)
    
    def _build_header(self, metadata: Dict[str, Any]) -> str:
        """Build HTML header"""
        title = metadata.get('title', 'Book')
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {self.default_styles}
    </style>
</head>
<body>"""
    
    def _build_cover(self, metadata: Dict[str, Any]) -> str:
        """Build cover page"""
        title = metadata.get('title', 'Book')
        subtitle = metadata.get('subtitle', '')
        version = metadata.get('version', '1.0.0')
        date = metadata.get('date', '')
        
        return f"""
    <div class="cover">
        <h1>{title}</h1>
        <h2>{subtitle}</h2>
        <p class="version">Version {version}<br>{date}</p>
    </div>"""
    
    def _build_toc(self, chapters: List[Dict[str, Any]]) -> str:
        """Build table of contents"""
        toc_items = []
        for chapter in chapters:
            chapter_num = chapter['number']
            title = chapter['title']
            toc_items.append(f'<li><a href="#chapter{chapter_num}">第{chapter_num}章　{title}</a></li>')
        
        return f"""
    <div class="toc">
        <h1>目次</h1>
        <ul>
            {chr(10).join(toc_items)}
        </ul>
    </div>"""
    
    def _build_chapter(self, chapter: Dict[str, Any]) -> str:
        """Build chapter HTML"""
        chapter_num = chapter['number']
        content = chapter['content_html']
        
        return f"""
    <div id="chapter{chapter_num}" class="chapter">
        {content}
    </div>"""
    
    def _build_footer(self) -> str:
        """Build HTML footer"""
        return """
</body>
</html>"""


class PDFBuilder:
    """Build PDF output using various backends"""
    
    def __init__(self, backend: str = 'weasyprint'):
        """
        Initialize PDF builder
        
        Args:
            backend: PDF generation backend ('weasyprint', 'pandoc', 'wkhtmltopdf')
        """
        self.backend = backend
        self._check_backend()
    
    def _check_backend(self):
        """Check if the selected backend is available"""
        if self.backend == 'weasyprint':
            try:
                import weasyprint
                self.weasyprint_available = True
            except ImportError:
                logger.warning("WeasyPrint not installed. Install with: pip install weasyprint")
                self.weasyprint_available = False
        
        elif self.backend == 'pandoc':
            self.pandoc_available = shutil.which('pandoc') is not None
            if not self.pandoc_available:
                logger.warning("Pandoc not found. Install from: https://pandoc.org/")
        
        elif self.backend == 'wkhtmltopdf':
            self.wkhtmltopdf_available = shutil.which('wkhtmltopdf') is not None
            if not self.wkhtmltopdf_available:
                logger.warning("wkhtmltopdf not found. Install from: https://wkhtmltopdf.org/")
    
    def html_to_pdf(self, html_file: Path, output_file: Path) -> bool:
        """Convert HTML to PDF"""
        if self.backend == 'weasyprint':
            return self._weasyprint_convert(html_file, output_file)
        elif self.backend == 'pandoc':
            return self._pandoc_convert(html_file, output_file)
        elif self.backend == 'wkhtmltopdf':
            return self._wkhtmltopdf_convert(html_file, output_file)
        else:
            logger.error(f"Unknown backend: {self.backend}")
            return False
    
    def _weasyprint_convert(self, html_file: Path, output_file: Path) -> bool:
        """Convert using WeasyPrint"""
        if not self.weasyprint_available:
            return False
        
        try:
            import weasyprint
            html = weasyprint.HTML(filename=str(html_file))
            html.write_pdf(str(output_file))
            return True
        except Exception as e:
            logger.error(f"WeasyPrint conversion failed: {e}")
            return False
    
    def _pandoc_convert(self, html_file: Path, output_file: Path) -> bool:
        """Convert using Pandoc"""
        if not self.pandoc_available:
            return False
        
        try:
            cmd = [
                'pandoc',
                str(html_file),
                '-o', str(output_file),
                '--pdf-engine=xelatex',
                '-V', 'documentclass=ltjsarticle',
                '-V', 'classoption=a4paper',
                '-V', 'geometry:margin=1in'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Pandoc conversion failed: {result.stderr}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Pandoc conversion failed: {e}")
            return False
    
    def _wkhtmltopdf_convert(self, html_file: Path, output_file: Path) -> bool:
        """Convert using wkhtmltopdf"""
        if not self.wkhtmltopdf_available:
            return False
        
        try:
            cmd = [
                'wkhtmltopdf',
                '--enable-local-file-access',
                '--encoding', 'utf-8',
                '--margin-top', '20mm',
                '--margin-bottom', '20mm',
                '--margin-left', '20mm',
                '--margin-right', '20mm',
                str(html_file),
                str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"wkhtmltopdf conversion failed: {result.stderr}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"wkhtmltopdf conversion failed: {e}")
            return False