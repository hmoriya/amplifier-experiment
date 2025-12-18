#!/usr/bin/env python3
"""
Ultimate Parasol V5 book generator with complete markdown support
"""

import re
import json
from pathlib import Path
from ultimate_markdown_converter import UltimateMarkdownConverter


class UltimateBookGenerator:
    """Ultimate book generator with perfect markdown support"""
    
    def __init__(self, book_dir: Path, output_dir: Path):
        self.book_dir = Path(book_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.converter = UltimateMarkdownConverter()
        
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
    
    def process_special_content(self, content):
        """Process special content like ASCII tables"""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Check if line is in a blockquote
            if lines[i].startswith('>'):
                result.append(lines[i])
                i += 1
                continue
            
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
                    markdown_table = self.convert_ascii_to_markdown(table_lines)
                    result.extend(markdown_table.split('\n'))
                    continue
            
            result.append(lines[i])
            i += 1
        
        return '\n'.join(result)
    
    def convert_ascii_to_markdown(self, lines):
        """Convert ASCII box table to markdown"""
        content_rows = []
        
        for line in lines:
            if '│' in line and not all(c in '─━┌├└┼┬┴┤┐┘│ ' for c in line):
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
        markdown = []
        
        # Header
        markdown.append('| ' + ' | '.join(content_rows[0]) + ' |')
        
        # Separator
        markdown.append('|' + '|'.join(['-' * (len(cell) + 2) for cell in content_rows[0]]) + '|')
        
        # Rows
        for row in content_rows[1:]:
            while len(row) < len(content_rows[0]):
                row.append('')
            markdown.append('| ' + ' | '.join(row) + ' |')
        
        return '\n'.join(markdown)
    
    def generate_html(self):
        """Generate HTML book"""
        print("📚 Ultimate Parasol V5 Book Generator")
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
                
                # Extract info
                _, title = self.extract_chapter_info(content)
                
                if title:
                    print(f"  ✓ 第{chapter_num}章: {title}")
                    toc_entries.append((f"chapter{chapter_num}", f"第{chapter_num}章　{title}"))
                    
                    # Process special content
                    processed_content = self.process_special_content(content)
                    
                    # Convert to HTML
                    html_content = self.converter.convert(processed_content)
                    
                    # Final emphasis processing for any remaining text
                    html_content = self._finalize_emphasis(html_content)
                    
                    chapters.append({
                        'number': chapter_num,
                        'title': title,
                        'content': html_content
                    })
                    
                    chapter_num += 1
        
        # Generate HTML
        html = self.generate_html_document(chapters, toc_entries)
        
        # Save
        output_file = self.output_dir / 'parasol-v5-ultimate.html'
        output_file.write_text(html, encoding='utf-8')
        
        print(f"\n✅ Ultimate HTML book: {output_file}")
        print(f"📊 Total chapters: {len(chapters)}")
        
        # Metadata
        self.save_metadata(chapters)
        
        return output_file
    
    def _finalize_emphasis(self, html: str) -> str:
        """Apply emphasis to any remaining text after all conversions"""
        lines = html.split('\n')
        result = []
        
        for line in lines:
            # Only process lines that don't contain HTML tags or code
            if not line.strip().startswith('<') and '<pre>' not in line and '<code>' not in line:
                # Apply emphasis
                line = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', line)
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                line = re.sub(r'__(.+?)__', r'<strong>\1</strong>', line)
                line = re.sub(r'(?<!\*)\*([^\*]+?)\*(?!\*)', r'<em>\1</em>', line)
                line = re.sub(r'(?<!_)_([^_]+?)_(?!_)', r'<em>\1</em>', line)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def generate_html_document(self, chapters, toc_entries):
        """Generate HTML document"""
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parasol V5 完全ガイドブック</title>
    <style>
        /* Base */
        body {{
            font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif JP', serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        /* Cover */
        .cover {{
            text-align: center;
            padding: 120px 40px;
            page-break-after: always;
            margin-bottom: 50px;
            background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-radius: 10px;
        }}
        
        .cover h1 {{
            font-size: 3em;
            margin-bottom: 30px;
            color: #2c3e50;
            font-weight: 300;
            letter-spacing: 2px;
        }}
        
        .cover h2 {{
            font-size: 1.8em;
            color: #7f8c8d;
            font-weight: 300;
            margin-bottom: 50px;
        }}
        
        .cover .version {{
            margin-top: 80px;
            color: #95a5a6;
            font-size: 1.1em;
        }}
        
        /* TOC */
        .toc {{
            background: white;
            padding: 50px;
            margin: 50px 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            page-break-after: always;
            border-radius: 10px;
        }}
        
        .toc h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 40px;
            font-size: 2.2em;
        }}
        
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin: 20px 0;
            padding-left: 30px;
            position: relative;
            font-size: 1.1em;
        }}
        
        .toc li:before {{
            content: "▸";
            position: absolute;
            left: 0;
            color: #3498db;
            font-size: 1.3em;
        }}
        
        .toc a {{
            text-decoration: none;
            color: #333;
            transition: all 0.3s;
            display: inline-block;
        }}
        
        .toc a:hover {{
            color: #3498db;
            transform: translateX(5px);
        }}
        
        /* Headers */
        h1, h2, h3, h4 {{
            font-weight: 400;
            line-height: 1.3;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin: 50px 0 30px;
            font-size: 2.2em;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 10px;
            margin: 40px 0 20px;
            font-size: 1.7em;
        }}
        
        h3 {{
            color: #7f8c8d;
            margin: 35px 0 15px;
            font-size: 1.4em;
        }}
        
        h4 {{
            color: #95a5a6;
            margin: 30px 0 10px;
            font-size: 1.2em;
        }}
        
        /* Blockquotes */
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding: 20px 25px;
            background-color: #f8f9fa;
            border-radius: 0 8px 8px 0;
        }}
        
        blockquote p {{
            margin: 10px 0;
        }}
        
        blockquote table {{
            margin: 15px 0;
            background: white;
        }}
        
        /* Tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th, td {{
            border: 1px solid #e0e0e0;
            padding: 14px 18px;
            text-align: left;
        }}
        
        th {{
            background: linear-gradient(to bottom, #3498db, #2980b9);
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
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
            background-color: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.85em;
            color: #e83e8c;
            border: 1px solid #e0e0e0;
        }}
        
        pre {{
            background-color: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            line-height: 1.5;
            margin: 25px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-size: 0.9em;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #abb2bf;
            border: none;
        }}
        
        /* Lists */
        ul, ol {{
            margin: 20px 0;
            padding-left: 35px;
        }}
        
        li {{
            margin: 10px 0;
            line-height: 1.7;
        }}
        
        /* Links */
        a {{
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: all 0.3s;
        }}
        
        a:hover {{
            color: #2980b9;
            border-bottom-color: #2980b9;
        }}
        
        /* HR */
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 50px 0;
        }}
        
        /* Chapter */
        .chapter {{
            page-break-before: always;
            margin-top: 80px;
            background: white;
            padding: 50px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            border-radius: 10px;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .cover {{
                padding: 80px 20px;
            }}
            
            .cover h1 {{
                font-size: 2em;
            }}
            
            .toc, .chapter {{
                padding: 30px;
            }}
            
            table {{
                font-size: 0.9em;
            }}
            
            th, td {{
                padding: 10px;
            }}
        }}
        
        /* Print */
        @media print {{
            body {{
                background-color: white;
                max-width: none;
            }}
            
            .cover, .toc, .chapter {{
                box-shadow: none;
                border-radius: 0;
                background: white;
            }}
            
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            
            .chapter {{
                page-break-before: always;
            }}
        }}
    </style>
</head>
<body>
    <!-- Cover -->
    <div class="cover">
        <h1>Parasol V5<br>完全ガイドブック</h1>
        <h2>価値駆動による実践的システム設計</h2>
        <div class="version">
            Version 1.0.0<br>
            2025年12月18日
        </div>
    </div>
    
    <!-- TOC -->
    <div class="toc">
        <h1>目次</h1>
        <ul>
            {"".join(f'<li><a href="#{anchor}">{title}</a></li>' for anchor, title in toc_entries)}
        </ul>
    </div>
    
    <!-- Chapters -->
    {"".join(f'<div id="chapter{ch["number"]}" class="chapter">{ch["content"]}</div>' for ch in chapters)}
</body>
</html>"""
    
    def save_metadata(self, chapters):
        """Save book metadata"""
        metadata = {
            "title": "Parasol V5 完全ガイドブック",
            "subtitle": "価値駆動による実践的システム設計",
            "version": "1.0.0",
            "date": "2025年12月18日",
            "chapters": len(chapters),
            "format": "HTML",
            "features": [
                "Complete markdown support",
                "Blockquote tables",
                "ASCII table conversion",
                "Syntax highlighting",
                "Responsive design",
                "Print optimization",
                "Perfect code block and inline code handling",
                "Nested content in blockquotes"
            ]
        }
        
        metadata_file = self.output_dir / 'book-metadata.json'
        metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    """Main function"""
    generator = UltimateBookGenerator(
        book_dir=Path(".claude/commands/parasol/docs/book"),
        output_dir=Path("output")
    )
    
    generator.generate_html()


if __name__ == "__main__":
    main()