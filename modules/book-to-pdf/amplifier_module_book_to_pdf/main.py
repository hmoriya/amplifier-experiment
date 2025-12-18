#!/usr/bin/env python3
"""
Book to PDF - Main CLI entry point.

Converts Parasol V5 Markdown documentation to PDF format.
"""

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

import click
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from rich import print as rprint
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from .converters import MarkdownConverter, PDFGenerator
from .styles import get_default_css

console = Console()


class BookToPDFConverter:
    """Main converter class for book to PDF conversion"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path.cwd()
        self.book_path = self.base_path / ".claude" / "commands" / "parasol" / "docs" / "book"
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup template environment
        template_dir = Path(__file__).parent / "templates"
        if not template_dir.exists():
            template_dir.mkdir(parents=True)
            self._create_default_templates(template_dir)
        
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        self.md_converter = MarkdownConverter()
        self.pdf_generator = PDFGenerator()
        
    def _create_default_templates(self, template_dir: Path):
        """Create default templates if they don't exist"""
        # Base template
        base_template = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <style>
        {{ css }}
    </style>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>'''
        
        (template_dir / "base.html").write_text(base_template)
        
        # Cover template
        cover_template = '''{% extends "base.html" %}
{% block content %}
<div class="cover">
    <h1 class="cover-title">{{ title }}</h1>
    {% if subtitle %}
    <h2 class="cover-subtitle">{{ subtitle }}</h2>
    {% endif %}
    <div class="cover-meta">
        <p class="version">Version {{ version }}</p>
        <p class="date">{{ date }}</p>
    </div>
</div>
{% endblock %}'''
        
        (template_dir / "cover.html").write_text(cover_template)
        
        # TOC template
        toc_template = '''<div class="toc">
    <h1>目次</h1>
    <ul class="toc-list">
    {% for item in toc_items %}
        <li class="toc-item toc-level-{{ item.level }}">
            <a href="#{{ item.id }}">{{ item.title }}</a>
        </li>
    {% endfor %}
    </ul>
</div>'''
        
        (template_dir / "toc.html").write_text(toc_template)
    
    def get_book_structure(self) -> Dict[str, Any]:
        """Get the book structure from README"""
        readme_path = self.book_path / "README.md"
        if not readme_path.exists():
            raise FileNotFoundError(f"Book README not found at {readme_path}")
        
        # Parse README to get structure
        structure = {
            "title": "Parasol V5 完全ガイドブック",
            "subtitle": "価値駆動による実践的システム設計",
            "version": "1.0.0",
            "parts": []
        }
        
        # Read actual structure from directory
        for part_dir in sorted(self.book_path.glob("part*")):
            if part_dir.is_dir():
                part_info = {
                    "name": part_dir.name,
                    "chapters": []
                }
                
                for chapter_file in sorted(part_dir.glob("chapter*.md")):
                    part_info["chapters"].append(chapter_file)
                
                if part_info["chapters"]:
                    structure["parts"].append(part_info)
        
        # Add appendices
        appendix_dir = self.book_path / "appendices"
        if appendix_dir.exists():
            appendix_info = {
                "name": "appendices",
                "chapters": sorted(appendix_dir.glob("appendix-*.md"))
            }
            if appendix_info["chapters"]:
                structure["parts"].append(appendix_info)
        
        return structure
    
    def convert_markdown_to_html(self, md_file: Path) -> str:
        """Convert markdown file to HTML"""
        content = md_file.read_text(encoding='utf-8')
        
        # Convert markdown to HTML
        html_content = self.md_converter.convert(content)
        
        return html_content
    
    def generate_toc(self, parts: List[Dict]) -> str:
        """Generate table of contents"""
        toc_items = []
        
        for part in parts:
            for chapter_file in part["chapters"]:
                content = chapter_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for line in lines:
                    if line.startswith('#'):
                        level = len(line.split()[0])
                        title = line.strip('#').strip()
                        item_id = title.lower().replace(' ', '-')
                        
                        toc_items.append({
                            'level': level,
                            'title': title,
                            'id': item_id
                        })
        
        template = self.env.get_template('toc.html')
        return template.render(toc_items=toc_items)
    
    def combine_chapters(self, parts: List[Dict]) -> str:
        """Combine all chapters into single HTML"""
        combined_html = []
        
        for part in parts:
            # Add part separator
            part_name = part["name"]
            if part_name.startswith("part"):
                part_num = part_name.replace("part", "第") + "部"
                combined_html.append(f'<div class="part-separator"><h1>{part_num}</h1></div>')
            
            for chapter_file in part["chapters"]:
                console.print(f"  Processing: {chapter_file.name}")
                html_content = self.convert_markdown_to_html(chapter_file)
                combined_html.append(f'<div class="chapter">{html_content}</div>')
        
        return '\n'.join(combined_html)
    
    def generate_pdf(self, output_file: Path, structure: Dict, parts: Optional[List[int]] = None):
        """Generate PDF from book structure"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating PDF...", total=None)
            
            # Filter parts if specified
            if parts:
                filtered_parts = [p for i, p in enumerate(structure["parts"]) if i + 1 in parts]
            else:
                filtered_parts = structure["parts"]
            
            if not filtered_parts:
                console.print("[red]No parts found to process[/red]")
                return
            
            # Generate cover
            cover_template = self.env.get_template('cover.html')
            cover_html = cover_template.render(
                title=structure["title"],
                subtitle=structure["subtitle"],
                version=structure["version"],
                date=datetime.now().strftime("%Y年%m月%d日"),
                css=get_default_css()
            )
            
            # Generate TOC
            toc_html = self.generate_toc(filtered_parts)
            
            # Combine all chapters
            content_html = self.combine_chapters(filtered_parts)
            
            # Generate final HTML
            base_template = self.env.get_template('base.html')
            final_html = base_template.render(
                title=structure["title"],
                css=get_default_css(),
                content=cover_html + toc_html + content_html
            )
            
            # Convert to PDF
            progress.update(task, description="Converting to PDF...")
            
            font_config = FontConfiguration()
            html_doc = HTML(string=final_html, base_url=str(self.book_path))
            css = CSS(string=get_default_css(), font_config=font_config)
            
            html_doc.write_pdf(
                str(output_file),
                stylesheets=[css],
                font_config=font_config
            )
            
            progress.update(task, description="Done!", completed=True)
    
    def check_dependencies(self) -> bool:
        """Check if all dependencies are installed"""
        checks = []
        
        # Check for required fonts
        console.print("\n[bold]Checking dependencies...[/bold]")
        
        # Check WeasyPrint
        try:
            import weasyprint
            console.print("✅ WeasyPrint installed")
            checks.append(True)
        except ImportError:
            console.print("❌ WeasyPrint not found")
            checks.append(False)
        
        # Check for Japanese fonts (simplified check)
        font_paths = [
            "/System/Library/Fonts",  # macOS
            "/usr/share/fonts",       # Linux
            "C:\\Windows\\Fonts"      # Windows
        ]
        
        font_found = False
        for path in font_paths:
            if Path(path).exists():
                font_found = True
                break
        
        if font_found:
            console.print("✅ System fonts directory found")
        else:
            console.print("⚠️  System fonts directory not found - Japanese text may not render correctly")
        
        return all(checks)


@click.group()
def cli():
    """Book to PDF converter for Parasol V5 documentation"""
    pass


@cli.command()
@click.option('--part', '-p', type=int, multiple=True, help='Specific part number(s) to convert')
@click.option('--output', '-o', type=click.Path(), help='Output PDF file path')
@click.option('--page-size', default='A4', type=click.Choice(['A4', 'letter']), help='Page size')
@click.option('--font-size', type=int, default=10, help='Base font size in points')
def convert(part: tuple, output: Optional[str], page_size: str, font_size: int):
    """Convert book to PDF format"""
    converter = BookToPDFConverter()
    
    # Check dependencies
    if not converter.check_dependencies():
        console.print("\n[red]Missing dependencies. Please install required packages.[/red]")
        sys.exit(1)
    
    try:
        structure = converter.get_book_structure()
        
        # Determine output filename
        if output:
            output_file = Path(output)
        else:
            if part:
                part_str = '-'.join(str(p) for p in part)
                output_file = converter.output_dir / f"parasol-v5-part{part_str}.pdf"
            else:
                output_file = converter.output_dir / "parasol-v5-complete-guide.pdf"
        
        console.print(f"\n[bold]Converting Parasol V5 book to PDF[/bold]")
        console.print(f"Output: {output_file}")
        
        # Generate PDF
        converter.generate_pdf(output_file, structure, list(part) if part else None)
        
        console.print(f"\n[green]✅ PDF generated successfully![/green]")
        console.print(f"📄 {output_file} ({output_file.stat().st_size // 1024} KB)")
        
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def check_fonts():
    """Check available fonts for Japanese text"""
    console.print("\n[bold]Checking font availability...[/bold]\n")
    
    # Common Japanese font names
    japanese_fonts = [
        "Noto Sans CJK JP",
        "Noto Sans JP",
        "Hiragino Sans",
        "Yu Gothic",
        "Meiryo",
        "MS Gothic",
        "IPAGothic"
    ]
    
    console.print("Common Japanese fonts to check:")
    for font in japanese_fonts:
        console.print(f"  - {font}")
    
    console.print("\n[yellow]Note: WeasyPrint will use the first available font it finds.[/yellow]")
    console.print("Install Noto Sans CJK JP for best results.")


@cli.command()
def check_dependencies():
    """Check all dependencies for PDF generation"""
    converter = BookToPDFConverter()
    
    if converter.check_dependencies():
        console.print("\n[green]✅ All dependencies are installed![/green]")
    else:
        console.print("\n[red]❌ Some dependencies are missing.[/red]")
        console.print("\nInstall missing dependencies with:")
        console.print("  pip install weasyprint")


@cli.command()
@click.option('--port', '-p', type=int, default=8000, help='Port for preview server')
def preview(port: int):
    """Preview book in HTML format (development)"""
    console.print(f"\n[bold]Starting preview server on port {port}...[/bold]")
    console.print("[yellow]Note: This is for development preview only.[/yellow]")
    console.print("\nPress Ctrl+C to stop.\n")
    
    # Simple HTTP server for preview
    import http.server
    import socketserver
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(Path.cwd()), **kwargs)
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        console.print(f"Preview available at: http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            console.print("\n\nShutting down preview server...")


if __name__ == '__main__':
    cli()