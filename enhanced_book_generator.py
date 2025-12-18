#!/usr/bin/env python3
"""
Enhanced Parasol V5 book generator with improved markdown support
"""

import re
import json
from pathlib import Path
from improved_markdown_converter import ImprovedMarkdownConverter


class EnhancedBookGenerator:
    """Enhanced book generator with better markdown support"""
    
    def __init__(self, book_dir: Path, output_dir: Path):
        self.book_dir = Path(book_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.converter = ImprovedMarkdownConverter()
        
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
        """Extract chapter number and title"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                match = re.match(r'第(\d+)章[\s　]+(.+)', title)
                if match:
                    return int(match.group(1)), match.group(2)
                return None, title
        return None, None
    
    def process_special_tables(self, content):
        """Process special table formats like ASCII box tables"""
        # Convert ASCII box tables to markdown tables
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Detect ASCII box table
            if any(char in lines[i] for char in '┌├└┼┬┴┤┐┘─━│'):
                table_lines = []
                # Collect table lines
                while i < len(lines) and (any(char in lines[i] for char in '┌├└┼┬┴┤┐┘─━│') or 
                                        (table_lines and lines[i].strip() == '')):
                    if lines[i].strip():
                        table_lines.append(lines[i])
                    i += 1
                
                if table_lines:
                    # Convert to markdown table
                    markdown_table = self.convert_ascii_to_markdown_table(table_lines)
                    result.extend(markdown_table.split('\n'))
                    continue
            
            result.append(lines[i])
            i += 1
        
        return '\n'.join(result)
    
    def convert_ascii_to_markdown_table(self, lines):
        """Convert ASCII box table to markdown table"""
        content_rows = []
        
        for line in lines:
            if '│' in line and not all(c in '─━┌├└┼┬┴┤┐┘│ ' for c in line):
                # This is a content row
                cells = []
                parts = line.split('│')
                for part in parts:
                    cell = part.strip()
                    if cell:
                        cells.append(cell)
                if cells:
                    content_rows.append(cells)
        
        if not content_rows:
            return '\n'.join(lines)
        
        # Build markdown table
        markdown_lines = []
        
        # Header row
        markdown_lines.append('| ' + ' | '.join(content_rows[0]) + ' |')
        
        # Separator
        markdown_lines.append('|' + '|'.join(['-' * (len(cell) + 2) for cell in content_rows[0]]) + '|')
        
        # Data rows
        for row in content_rows[1:]:
            # Ensure same number of cells
            while len(row) < len(content_rows[0]):
                row.append('')
            markdown_lines.append('| ' + ' | '.join(row) + ' |')
        
        return '\n'.join(markdown_lines)
    
    def enhance_content(self, content):
        """Enhance content with special processing"""
        # Process special tables
        content = self.process_special_tables(content)
        
        # Add any other enhancements here
        # For example, process diagrams, special notations, etc.
        
        return content
    
    def generate_html(self):
        """Generate HTML book with enhanced formatting"""
        print("📚 Parasol V5 Enhanced Book Generator")
        print("=" * 50)
        
        chapters = []
        toc_entries = []
        chapter_num = 1
        
        print("\n📖 Processing chapters...")
        
        for part_name, chapter_files in self.chapter_structure:
            part_dir = self.book_dir / part_name
            
            for chapter_file in chapter_files:
                file_path = part_dir / chapter_file
                
                if not file_path.exists():
                    print(f"  ⚠️  {chapter_file} not found")
                    continue
                
                content = file_path.read_text(encoding='utf-8')
                
                # Extract chapter info
                _, title = self.extract_chapter_info(content)
                
                if title:
                    print(f"  ✓ 第{chapter_num}章: {title}")
                    toc_entries.append((f"chapter{chapter_num}", f"第{chapter_num}章　{title}"))
                    
                    # Enhance content
                    enhanced_content = self.enhance_content(content)
                    
                    # Convert to HTML
                    html_content = self.converter.convert(enhanced_content)
                    
                    chapters.append({
                        'number': chapter_num,
                        'title': title,
                        'content': html_content
                    })
                    
                    chapter_num += 1
        
        # Generate HTML document
        html = self.generate_html_document(chapters, toc_entries)
        
        # Save file
        output_file = self.output_dir / 'parasol-v5-enhanced.html'
        output_file.write_text(html, encoding='utf-8')
        
        print(f"\n✅ HTML book generated: {output_file}")
        
        # Generate metadata
        self.generate_metadata(len(chapters))
        
        return output_file
    
    def generate_html_document(self, chapters, toc_entries):
        """Generate complete HTML document with enhanced styles"""
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parasol V5 完全ガイドブック</title>
    <style>
        /* Base styles */
        body {{
            font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif JP', serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fafafa;
        }}
        
        /* Cover page */
        .cover {{
            text-align: center;
            padding: 100px 20px;
            page-break-after: always;
            margin-bottom: 50px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 10px;
        }}
        
        .cover h1 {{
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #2c3e50;
        }}
        
        .cover h2 {{
            font-size: 1.5em;
            color: #7f8c8d;
            font-weight: normal;
        }}
        
        .cover .version {{
            margin-top: 50px;
            color: #95a5a6;
        }}
        
        /* Table of contents */
        .toc {{
            background: white;
            padding: 40px;
            margin: 40px 0;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            page-break-after: always;
            border-radius: 10px;
        }}
        
        .toc h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin: 15px 0;
            padding-left: 25px;
            position: relative;
        }}
        
        .toc li:before {{
            content: "▸";
            position: absolute;
            left: 0;
            color: #3498db;
            font-size: 1.2em;
        }}
        
        .toc a {{
            text-decoration: none;
            color: #333;
            transition: color 0.3s;
        }}
        
        .toc a:hover {{
            color: #3498db;
            text-decoration: underline;
        }}
        
        /* Headers */
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
            margin-bottom: 30px;
            font-size: 2em;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 35px;
            margin-bottom: 20px;
            font-size: 1.6em;
        }}
        
        h3 {{
            color: #7f8c8d;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        h4 {{
            color: #95a5a6;
            margin-top: 25px;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        
        /* Tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 5px;
            overflow: hidden;
        }}
        
        th, td {{
            border: 1px solid #e0e0e0;
            padding: 12px 16px;
            text-align: left;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
            letter-spacing: 0.5px;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s;
        }}
        
        /* Code */
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 0.9em;
            color: #e83e8c;
        }}
        
        pre {{
            background-color: #282c34;
            color: #abb2bf;
            padding: 16px;
            border-radius: 5px;
            overflow-x: auto;
            line-height: 1.4;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #abb2bf;
        }}
        
        /* Language-specific syntax highlighting */
        .language-javascript code {{
            color: #e06c75;
        }}
        
        .language-python code {{
            color: #98c379;
        }}
        
        /* Blockquotes */
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 15px 20px;
            background-color: #f1f8ff;
            color: #555;
            font-style: italic;
            border-radius: 0 5px 5px 0;
        }}
        
        /* Lists */
        ul, ol {{
            margin: 16px 0;
            padding-left: 35px;
        }}
        
        li {{
            margin: 8px 0;
            line-height: 1.7;
        }}
        
        /* Links */
        a {{
            color: #3498db;
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        a:hover {{
            color: #2980b9;
            text-decoration: underline;
        }}
        
        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 40px 0;
        }}
        
        /* Chapter styling */
        .chapter {{
            page-break-before: always;
            margin-top: 60px;
            background: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
            border-radius: 10px;
        }}
        
        /* Checkboxes */
        li {{
            list-style: none;
        }}
        
        li:has(☐), li:has(☑) {{
            margin-left: -20px;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background-color: white;
                max-width: none;
            }}
            .cover, .toc, .chapter {{
                box-shadow: none;
                border-radius: 0;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
        }}
    </style>
</head>
<body>
    <!-- Cover page -->
    <div class="cover">
        <h1>Parasol V5 完全ガイドブック</h1>
        <h2>価値駆動による実践的システム設計</h2>
        <p class="version">Version 1.0.0<br>2025年12月18日</p>
    </div>
    
    <!-- Table of contents -->
    <div class="toc">
        <h1>目次</h1>
        <ul>
            {"".join(f'<li><a href="#{anchor}">{title}</a></li>' for anchor, title in toc_entries)}
        </ul>
    </div>
    
    <!-- Chapters -->
    {"".join(f'''<div id="chapter{ch['number']}" class="chapter">{ch['content']}</div>''' for ch in chapters)}
</body>
</html>"""
    
    def generate_metadata(self, chapter_count):
        """Generate book metadata"""
        metadata = {
            "title": "Parasol V5 完全ガイドブック",
            "subtitle": "価値駆動による実践的システム設計",
            "version": "1.0.0",
            "date": "2025年12月18日",
            "chapters": chapter_count,
            "format": "HTML",
            "generator": "EnhancedBookGenerator v1.0"
        }
        
        metadata_file = self.output_dir / 'book-metadata.json'
        metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"📋 Metadata saved: {metadata_file}")


def main():
    """Main function"""
    generator = EnhancedBookGenerator(
        book_dir=Path(".claude/commands/parasol/docs/book"),
        output_dir=Path("output")
    )
    
    generator.generate_html()
    
    print("\n📊 Generation complete!")
    print("Open the HTML file in your browser to view the enhanced book.")


if __name__ == "__main__":
    main()