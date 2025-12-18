#!/usr/bin/env python3
"""
Simple PDF generator for Parasol V5 book using markdown.

This is a simplified version that generates HTML first,
which can then be converted to PDF using browser print function.
"""

import re
from pathlib import Path
from datetime import datetime


def read_chapter(file_path: Path) -> str:
    """Read a chapter file and return its content"""
    return file_path.read_text(encoding='utf-8')


def convert_markdown_to_html(content: str) -> str:
    """Simple markdown to HTML conversion"""
    
    # First, convert tables (must be done before other conversions)
    content = convert_tables(content)
    
    # Convert headers
    content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Convert bold and italic
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', content)
    
    # Convert code blocks
    content = re.sub(r'```(\w*)\n(.*?)```', 
                    lambda m: f'<pre><code class="language-{m.group(1) or "text"}">{m.group(2)}</code></pre>', 
                    content, flags=re.DOTALL)
    
    # Convert inline code
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
    
    # Convert blockquotes
    content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)
    
    # Convert lists
    content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'^\* (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    
    # Wrap consecutive list items
    lines = content.split('\n')
    result = []
    in_ul = False
    
    for line in lines:
        if line.startswith('<li>'):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            result.append(line)
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            result.append(line)
    
    if in_ul:
        result.append('</ul>')
    
    content = '\n'.join(result)
    
    # Convert paragraphs
    content = re.sub(r'\n\n([^<\n][^\n]*)\n', r'\n\n<p>\1</p>\n', content)
    
    return content


def convert_tables(content: str) -> str:
    """Convert Markdown tables and ASCII tables to HTML"""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for ASCII box-drawing tables
        if any(char in line for char in ['┌', '├', '└', '─', '│', '┼', '┬', '┴', '┤']):
            # Start collecting ASCII table
            ascii_table_lines = []
            table_start = i
            
            # Collect all lines that look like part of the ASCII table
            while i < len(lines) and any(char in lines[i] for char in ['┌', '├', '└', '─', '│', '┼', '┬', '┴', '┤', '|']):
                ascii_table_lines.append(lines[i])
                i += 1
            
            # Convert ASCII table to HTML
            if ascii_table_lines:
                html_table = convert_ascii_table(ascii_table_lines)
                result.append(html_table)
                continue
        
        # Check if this looks like a Markdown table row
        if line.startswith('|') and line.endswith('|') and '---' not in line:
            # Start of a table
            table_lines = []
            
            # Collect all table lines
            while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            
            # Process table
            if len(table_lines) >= 2:  # At least header and separator
                html_table = ['<table class="table">']
                
                # Check if second line is separator
                is_markdown_table = False
                if len(table_lines) > 1 and all(c in '-|: ' for c in table_lines[1]):
                    is_markdown_table = True
                
                if is_markdown_table:
                    # Process header
                    header_cells = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]
                    html_table.append('<thead><tr>')
                    for cell in header_cells:
                        html_table.append(f'<th>{cell}</th>')
                    html_table.append('</tr></thead>')
                    
                    # Process body (skip separator line)
                    if len(table_lines) > 2:
                        html_table.append('<tbody>')
                        for row in table_lines[2:]:
                            cells = [cell.strip() for cell in row.split('|')[1:-1]]
                            html_table.append('<tr>')
                            for cell in cells:
                                html_table.append(f'<td>{cell}</td>')
                            html_table.append('</tr>')
                        html_table.append('</tbody>')
                    
                    html_table.append('</table>')
                    result.extend(html_table)
                else:
                    # Not a valid Markdown table, add lines as-is
                    result.extend(table_lines)
            else:
                # Not a valid table, add lines as-is
                result.extend(table_lines)
        else:
            result.append(lines[i])
            i += 1
    
    return '\n'.join(result)


def convert_ascii_table(lines):
    """Convert ASCII box-drawing table to HTML"""
    # Extract content rows
    content_rows = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
            
        # Skip pure border lines (only box-drawing characters)
        if all(c in '─━┌├└┼┬┴┤┐┘│' or c.isspace() for c in line):
            continue
            
        # Extract content from lines with vertical bars
        if '│' in line:
            # Split by box-drawing vertical bar
            parts = line.split('│')
            # Clean up each cell
            cells = []
            for part in parts:
                cell = part.strip()
                if cell:  # Only include non-empty cells
                    cells.append(cell)
            
            if cells:
                content_rows.append(cells)
    
    if not content_rows:
        return '<pre>' + '\n'.join(lines) + '</pre>'
    
    # Build HTML table
    html = ['<table class="table">']
    
    # First content row might be title (single cell spanning table)
    if len(content_rows) > 0 and len(content_rows[0]) == 1:
        # Single cell row - likely a title
        html.append('<caption>' + content_rows[0][0] + '</caption>')
        content_rows = content_rows[1:]
    
    # Find header row (usually after title or first row)
    header_idx = 0
    if content_rows:
        html.append('<thead><tr>')
        for cell in content_rows[header_idx]:
            html.append(f'<th>{cell}</th>')
        html.append('</tr></thead>')
        
        # Process body rows
        if len(content_rows) > header_idx + 1:
            html.append('<tbody>')
            for row in content_rows[header_idx + 1:]:
                html.append('<tr>')
                # Ensure same number of cells as header
                for i, cell in enumerate(row):
                    html.append(f'<td>{cell}</td>')
                html.append('</tr>')
            html.append('</tbody>')
    
    html.append('</table>')
    return '\n'.join(html)


def generate_html_book():
    """Generate HTML version of the book"""
    base_path = Path.cwd()
    book_path = base_path / ".claude" / "commands" / "parasol" / "docs" / "book"
    
    # HTML template
    html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>Parasol V5 完全ガイドブック</title>
    <style>
        body {
            font-family: 'Noto Sans JP', 'Hiragino Sans', sans-serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        
        h1, h2, h3, h4 {
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 1em;
        }
        
        h1 {
            font-size: 2em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.3em;
        }
        
        h2 {
            font-size: 1.6em;
        }
        
        h3 {
            font-size: 1.3em;
        }
        
        h4 {
            font-size: 1.1em;
        }
        
        code {
            background-color: #f5f5f5;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Source Code Pro', monospace;
        }
        
        pre {
            background-color: #2c3e50;
            color: #f8f8f2;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
            color: #f8f8f2;
        }
        
        ul, ol {
            margin: 1em 0;
            padding-left: 2em;
        }
        
        li {
            margin: 0.5em 0;
        }
        
        p {
            margin: 1em 0;
        }
        
        .chapter {
            page-break-before: always;
            margin-top: 3em;
        }
        
        .part-header {
            page-break-before: always;
            text-align: center;
            margin: 4em 0;
        }
        
        .part-header h1 {
            font-size: 2.5em;
            border: none;
            color: #3498db;
        }
        
        .toc {
            page-break-after: always;
            margin: 2em 0;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 0.5em 0;
        }
        
        .toc a {
            text-decoration: none;
            color: #2c3e50;
        }
        
        .toc a:hover {
            color: #3498db;
        }
        
        .cover {
            text-align: center;
            margin: 8em 0;
            page-break-after: always;
        }
        
        .cover h1 {
            font-size: 3em;
            border: none;
            margin-bottom: 0.5em;
        }
        
        .cover h2 {
            font-size: 1.5em;
            color: #7f8c8d;
            margin-bottom: 2em;
        }
        
        .cover .version {
            color: #95a5a6;
            margin-top: 4em;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            font-size: 0.95em;
            page-break-inside: avoid;
        }
        
        table caption {
            padding: 0.5em;
            font-weight: bold;
            background-color: #2c3e50;
            color: white;
            text-align: center;
        }
        
        th, td {
            padding: 0.5em 0.8em;
            text-align: left;
            border: 1px solid #ddd;
        }
        
        th {
            background-color: #f5f5f5;
            font-weight: bold;
            color: #2c3e50;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        blockquote {
            margin: 1em 0;
            padding-left: 1em;
            border-left: 4px solid #3498db;
            color: #666;
            font-style: italic;
        }
        
        @media print {
            body {
                margin: 0;
                padding: 0;
            }
            
            .chapter, .part-header {
                page-break-before: always;
            }
        }
    </style>
</head>
<body>
"""
    
    html_content = []
    
    # Cover
    html_content.append("""
    <div class="cover">
        <h1>Parasol V5 完全ガイドブック</h1>
        <h2>価値駆動による実践的システム設計</h2>
        <p class="version">Version 1.0.0<br>""" + datetime.now().strftime("%Y年%m月%d日") + """</p>
    </div>
    """)
    
    # Table of contents
    toc_content = ['<div class="toc"><h1>目次</h1><ul>']
    chapter_num = 1
    
    # Process all parts
    parts = [
        ("第I部 基礎編", "part1-foundation"),
        ("第II部 理解編", "part2-understanding"),
        ("第III部 実践編", "part3-practice"),
        ("第IV部 発展編", "part4-advanced"),
    ]
    
    for part_title, part_dir in parts:
        # Part header
        html_content.append(f'<div class="part-header"><h1>{part_title}</h1></div>')
        
        # Process chapters in part
        part_path = book_path / part_dir
        if part_path.exists():
            for chapter_file in sorted(part_path.glob("chapter*.md")):
                # Read chapter
                chapter_content = read_chapter(chapter_file)
                
                # Extract title
                title_match = re.search(r'^# (.+)$', chapter_content, re.MULTILINE)
                if title_match:
                    chapter_title = title_match.group(1)
                    toc_content.append(f'<li><a href="#chapter{chapter_num}">第{chapter_num}章 {chapter_title}</a></li>')
                
                # Convert to HTML
                chapter_html = convert_markdown_to_html(chapter_content)
                html_content.append(f'<div class="chapter" id="chapter{chapter_num}">')
                html_content.append(chapter_html)
                html_content.append('</div>')
                
                chapter_num += 1
    
    # Add appendices
    html_content.append('<div class="part-header"><h1>付録</h1></div>')
    
    appendix_path = book_path / "appendices"
    if appendix_path.exists():
        for appendix_file in sorted(appendix_path.glob("appendix-*.md")):
            appendix_content = read_chapter(appendix_file)
            appendix_html = convert_markdown_to_html(appendix_content)
            html_content.append(f'<div class="chapter">')
            html_content.append(appendix_html)
            html_content.append('</div>')
    
    toc_content.append('</ul></div>')
    
    # Combine all
    final_html = html_template
    final_html += ''.join(toc_content)
    final_html += ''.join(html_content)
    final_html += '</body></html>'
    
    # Save HTML
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "parasol-v5-book.html"
    output_file.write_text(final_html, encoding='utf-8')
    
    print(f"✅ HTMLファイルを生成しました: {output_file}")
    print("\n📄 PDFに変換するには:")
    print("1. ブラウザでHTMLファイルを開く")
    print("2. ファイル → 印刷 (または Cmd+P)")
    print("3. プリンターで「PDFとして保存」を選択")
    print("4. 保存")
    
    return output_file


if __name__ == "__main__":
    generate_html_book()