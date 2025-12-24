#!/usr/bin/env python3
"""
Generate Parasol V5 book - simplified version without external dependencies
"""

import re
import json
from pathlib import Path
import subprocess
import shutil


class SimpleBookGenerator:
    """Simplified book generator without external dependencies"""
    
    def __init__(self, book_dir: Path, output_dir: Path):
        self.book_dir = Path(book_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Chapter structure
        self.chapter_structure = [
            ("part1-foundation", [
                "chapter1-why-parasol.md",
                "chapter2-overview.md",
                "chapter3-philosophy.md",
                "chapter4-v5-and-ddd.md"
            ]),
            ("part2-understanding", [
                "chapter5-phase0-1.md",
                "chapter6-phase2-value.md",
                "chapter7-phase3-capability.md",
                "chapter8-phase4-7.md",
                "chapter9-value-traceability.md"
            ]),
            ("part3-practice", [
                "chapter10-industry-patterns.md",
                "chapter11-claude-code.md",
                "chapter12-team-scaling.md",
                "chapter13-troubleshooting.md"
            ]),
            ("part4-advanced", [
                "chapter14-custom-patterns.md",
                "chapter15-v5-future.md"
            ])
        ]
    
    def extract_chapter_info(self, content):
        """Extract chapter number and title from content"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                # Extract chapter number
                match = re.match(r'第(\d+)章[\s　]+(.+)', title)
                if match:
                    return int(match.group(1)), match.group(2)
                return None, title
        return None, None
    
    def escape_html(self, text):
        """Escape HTML entities"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text
    
    def convert_markdown_to_html(self, content):
        """Simple markdown to HTML conversion"""
        # Process code blocks first
        code_blocks = []
        
        def save_code_block(match):
            language = match.group(1) or ''
            code = match.group(2)
            code_blocks.append(f'<pre><code>{self.escape_html(code)}</code></pre>')
            return f'___CODEBLOCK_{len(code_blocks) - 1}___'
        
        content = re.sub(r'```(\w*)\n(.*?)\n```', save_code_block, content, flags=re.DOTALL)
        
        # Convert headings
        content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        
        # Convert bold and italic
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', content)
        
        # Convert links
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
        
        # Convert lists
        lines = content.split('\n')
        result = []
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith(('- ', '* ')):
                result.append('<ul>')
                while i < len(lines) and lines[i].strip().startswith(('- ', '* ')):
                    item = re.sub(r'^[\-\*]\s+', '', lines[i].strip())
                    result.append(f'<li>{item}</li>')
                    i += 1
                result.append('</ul>')
            else:
                result.append(lines[i])
                i += 1
        content = '\n'.join(result)
        
        # Convert tables
        content = self.convert_tables(content)
        
        # Convert checkboxes
        content = re.sub(r'\[\s*\]', '☐', content)
        content = re.sub(r'\[x\]', '☑', content, flags=re.IGNORECASE)
        
        # Convert paragraphs
        paragraphs = content.split('\n\n')
        result = []
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('<') and not para.startswith('___'):
                if not re.match(r'^<[^>]+>', para):
                    result.append(f'<p>{para}</p>')
                else:
                    result.append(para)
            else:
                result.append(para)
        content = '\n\n'.join(result)
        
        # Restore code blocks
        for i, code_block in enumerate(code_blocks):
            content = content.replace(f'___CODEBLOCK_{i}___', code_block)
        
        return content
    
    def convert_tables(self, content):
        """Convert markdown tables to HTML"""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Check for markdown table
            if '|' in lines[i] and i + 1 < len(lines) and '|' in lines[i + 1]:
                # Check if next line is separator
                if re.match(r'^[\s\-:|]+$', lines[i + 1].replace('|', '')):
                    # This is a table
                    table_lines = []
                    while i < len(lines) and '|' in lines[i]:
                        table_lines.append(lines[i])
                        i += 1
                    result.append(self.render_markdown_table(table_lines))
                    continue
            
            result.append(lines[i])
            i += 1
        
        return '\n'.join(result)
    
    def render_markdown_table(self, lines):
        """Render markdown table as HTML"""
        if len(lines) < 2:
            return '\n'.join(lines)
        
        # Parse header
        headers = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        html = ['<table class="data-table">']
        html.append('<thead><tr>')
        for header in headers:
            html.append(f'<th>{header}</th>')
        html.append('</tr></thead>')
        
        # Parse body (skip separator line)
        if len(lines) > 2:
            html.append('<tbody>')
            for line in lines[2:]:
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                html.append('<tr>')
                for cell in cells:
                    html.append(f'<td>{cell}</td>')
                html.append('</tr>')
            html.append('</tbody>')
        
        html.append('</table>')
        return '\n'.join(html)
    
    def generate_html(self):
        """Generate HTML book"""
        print("Generating HTML book...")
        
        # Collect chapters
        chapters = []
        toc_entries = []
        chapter_num = 1
        
        for part_name, chapter_files in self.chapter_structure:
            part_dir = self.book_dir / part_name
            
            for chapter_file in chapter_files:
                file_path = part_dir / chapter_file
                
                if not file_path.exists():
                    print(f"Warning: {file_path} not found")
                    continue
                
                content = file_path.read_text(encoding='utf-8')
                _, title = self.extract_chapter_info(content)
                
                if title:
                    toc_entries.append((f"chapter{chapter_num}", f"第{chapter_num}章　{title}"))
                    
                    # Convert to HTML
                    html_content = self.convert_markdown_to_html(content)
                    
                    chapters.append({
                        'number': chapter_num,
                        'title': title,
                        'content': html_content
                    })
                    
                    chapter_num += 1
                    print(f"  Processed: 第{chapter_num - 1}章　{title}")
        
        # Generate complete HTML
        html = self.generate_html_document(chapters, toc_entries)
        
        # Save file
        output_file = self.output_dir / 'parasol-v5-book.html'
        output_file.write_text(html, encoding='utf-8')
        print(f"✅ HTML saved to: {output_file}")
        
        return output_file
    
    def generate_html_document(self, chapters, toc_entries):
        """Generate complete HTML document"""
        html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parasol V5 完全ガイドブック</title>
    <style>
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
        
        .cover h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #2c3e50;
        }
        
        .cover h2 {
            font-size: 1.5em;
            color: #7f8c8d;
            font-weight: normal;
        }
        
        .toc {
            background: white;
            padding: 40px;
            margin: 40px 0;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            page-break-after: always;
        }
        
        .toc h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 15px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .toc li:before {
            content: "▸";
            position: absolute;
            left: 0;
            color: #3498db;
        }
        
        .toc a {
            text-decoration: none;
            color: #333;
        }
        
        .toc a:hover {
            color: #3498db;
        }
        
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 40px; }
        h2 { color: #34495e; border-bottom: 1px solid #ecf0f1; padding-bottom: 5px; margin-top: 30px; }
        h3 { color: #7f8c8d; margin-top: 25px; }
        h4 { color: #95a5a6; margin-top: 20px; }
        
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
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
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
            font-size: 0.9em;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin-left: 0;
            padding-left: 20px;
            color: #555;
            font-style: italic;
            background-color: #f8f9fa;
            padding: 15px 20px;
        }
        
        .chapter {
            page-break-before: always;
            margin-top: 60px;
        }
        
        @media print {
            body {
                background-color: white;
                max-width: none;
            }
            .cover, .toc {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>"""
        
        # Cover page
        html += """
    <div class="cover">
        <h1>Parasol V5 完全ガイドブック</h1>
        <h2>価値駆動による実践的システム設計</h2>
        <p class="version">Version 1.0.0<br>2025年12月18日</p>
    </div>"""
        
        # Table of contents
        html += '\n    <div class="toc">\n        <h1>目次</h1>\n        <ul>'
        for anchor, title in toc_entries:
            html += f'\n            <li><a href="#{anchor}">{title}</a></li>'
        html += '\n        </ul>\n    </div>\n'
        
        # Chapters
        for chapter in chapters:
            html += f"""
    <div id="chapter{chapter['number']}" class="chapter">
        {chapter['content']}
    </div>"""
        
        html += """
</body>
</html>"""
        
        return html
    
    def generate_pdf(self, html_file):
        """Try to generate PDF from HTML"""
        print("\nAttempting PDF generation...")
        
        pdf_file = self.output_dir / 'parasol-v5-book.pdf'
        
        # Try wkhtmltopdf
        if shutil.which('wkhtmltopdf'):
            print("Using wkhtmltopdf...")
            cmd = [
                'wkhtmltopdf',
                '--enable-local-file-access',
                '--encoding', 'utf-8',
                str(html_file),
                str(pdf_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ PDF saved to: {pdf_file}")
                return True
            else:
                print(f"❌ wkhtmltopdf failed: {result.stderr}")
        
        # Try pandoc
        if shutil.which('pandoc'):
            print("Using pandoc...")
            cmd = [
                'pandoc',
                str(html_file),
                '-o', str(pdf_file),
                '--pdf-engine=xelatex'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ PDF saved to: {pdf_file}")
                return True
            else:
                print(f"❌ pandoc failed: {result.stderr}")
        
        print("⚠️  No PDF generator available (install wkhtmltopdf or pandoc)")
        return False


def main():
    """Main function"""
    print("Parasol V5 Book Generator (Simplified Version)")
    print("=" * 50)
    
    # Initialize generator
    generator = SimpleBookGenerator(
        book_dir=Path(".claude/commands/parasol/docs/book"),
        output_dir=Path("output")
    )
    
    # Generate HTML
    html_file = generator.generate_html()
    
    # Try to generate PDF
    generator.generate_pdf(html_file)
    
    # Show summary
    print("\n📚 Generation Summary:")
    print("=" * 50)
    for file in generator.output_dir.glob('parasol-v5-book.*'):
        print(f"  • {file.name} ({file.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()