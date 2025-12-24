#!/usr/bin/env python3
"""Enhanced HTML generator with better code and table handling"""

import re
from pathlib import Path
import sys

def get_heading_text(line):
    """Extract clean heading text without chapter numbers"""
    # Remove markdown heading markers
    text = re.sub(r'^#+\s*', '', line).strip()
    
    # Remove leading chapter numbers (e.g., "第1章　" or "第1章 ")
    text = re.sub(r'^第\d+章[\s　]+', '', text)
    
    return text

def extract_chapter_info(content):
    """Extract chapter information from markdown content"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = get_heading_text(line)
            # Extract chapter number if present
            match = re.match(r'第(\d+)章', line)
            if match:
                return int(match.group(1)), title
            return None, title
    return None, None

def escape_html(text):
    """Escape HTML entities"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def process_code_blocks(text):
    """Process code blocks first to protect them from other conversions"""
    # Replace code blocks with placeholders
    code_blocks = []
    placeholder_template = "___CODEBLOCK_{}___"
    
    # Process fenced code blocks (```...```)
    def save_fenced_code_block(match):
        language = match.group(1) or ''
        code = match.group(2)
        
        # Check if this code block contains a table-like structure
        if '|' in code and any('-' in line and '|' in line for line in code.split('\n')):
            # This looks like a table in code - format it nicely
            formatted_code = format_code_table(code)
        else:
            # Regular code block
            formatted_code = f'<pre><code>{escape_html(code)}</code></pre>'
        
        code_blocks.append(formatted_code)
        return placeholder_template.format(len(code_blocks) - 1)
    
    # Match fenced code blocks with optional language specifier
    text = re.sub(r'```(\w*)\n(.*?)\n```', save_fenced_code_block, text, flags=re.DOTALL)
    
    # Process indented code blocks
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        # Check if this line is indented (4 spaces or 1 tab)
        if lines[i].startswith('    ') or lines[i].startswith('\t'):
            # Start collecting code block
            code_lines = []
            
            # Collect all consecutive indented lines
            while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t') or lines[i].strip() == ''):
                if lines[i].strip() == '':
                    code_lines.append('')
                else:
                    # Remove indentation
                    if lines[i].startswith('    '):
                        code_lines.append(lines[i][4:])
                    else:
                        code_lines.append(lines[i][1:])
                i += 1
            
            # Only treat as code block if it looks like code
            if code_lines and len(code_lines) > 1:
                # Remove trailing empty lines
                while code_lines and code_lines[-1] == '':
                    code_lines.pop()
                
                code = '\n'.join(code_lines)
                formatted_code = f'<pre><code>{escape_html(code)}</code></pre>'
                code_blocks.append(formatted_code)
                result.append(placeholder_template.format(len(code_blocks) - 1))
            else:
                # Not a code block, keep as is
                result.extend(['    ' + line for line in code_lines if line])
                if code_lines and not code_lines[-1]:
                    result.append('')
        else:
            result.append(lines[i])
            i += 1
    
    text = '\n'.join(result)
    
    return text, code_blocks

def format_code_table(code):
    """Format a table that appears inside a code block"""
    lines = code.strip().split('\n')
    
    # Parse the table to find column widths
    rows = []
    for line in lines:
        if '|' in line:
            cells = [cell.strip() for cell in line.split('|')]
            # Remove empty cells at start and end
            if cells and cells[0] == '':
                cells = cells[1:]
            if cells and cells[-1] == '':
                cells = cells[:-1]
            rows.append(cells)
    
    if not rows:
        return f'<pre><code>{escape_html(code)}</code></pre>'
    
    # Calculate column widths
    col_widths = []
    for i in range(max(len(row) for row in rows)):
        width = max(len(row[i]) if i < len(row) else 0 for row in rows)
        col_widths.append(width)
    
    # Format the table with proper alignment
    formatted_lines = []
    for row in rows:
        formatted_cells = []
        for i, cell in enumerate(row):
            if i < len(col_widths):
                formatted_cells.append(cell.ljust(col_widths[i]))
        formatted_lines.append(' | '.join(formatted_cells))
    
    formatted_code = '\n'.join(formatted_lines)
    return f'<pre><code>{escape_html(formatted_code)}</code></pre>'

def convert_tables(content):
    """Convert markdown tables to HTML with better handling"""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for standard Markdown table
        if i + 1 < len(lines) and '|' in line and '|' in lines[i + 1] and re.match(r'^[\s\-:|]+$', lines[i + 1].replace('|', '')):
            # Start of a markdown table
            table_lines = []
            
            # Collect all table lines
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            
            # Convert to HTML table
            result.append(convert_markdown_table(table_lines))
            continue
        
        # Check for ASCII box-drawing table
        elif any(char in line for char in '┌├└┼┬┴┤┐┘─━│'):
            # Collect all lines that are part of the ASCII table
            table_lines = []
            start_i = i
            
            while i < len(lines) and (any(char in lines[i] for char in '┌├└┼┬┴┤┐┘─━│') or (i > start_i and lines[i].strip() == '')):
                if lines[i].strip():  # Only add non-empty lines
                    table_lines.append(lines[i])
                i += 1
            
            if table_lines:
                result.append(convert_ascii_table(table_lines))
                continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def convert_markdown_table(lines):
    """Convert standard Markdown table to HTML"""
    if len(lines) < 2:
        return '\n'.join(lines)
    
    html = ['<table class="table">']
    
    # Process header
    header_cells = [cell.strip() for cell in lines[0].split('|')[1:-1]]
    html.append('<thead>')
    html.append('<tr>')
    for cell in header_cells:
        html.append(f'<th>{cell}</th>')
    html.append('</tr>')
    html.append('</thead>')
    
    # Process body (skip separator line)
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

def convert_ascii_table(lines):
    """Convert ASCII box-drawing table to HTML"""
    # Extract content rows (lines with │ that aren't just borders)
    content_rows = []
    
    for line in lines:
        # Check if this line has content (not just a border)
        if '│' in line:
            # Check if this is just a border line
            is_border = all(c in '─━┌├└┼┬┴┤┐┘│' or c.isspace() for c in line)
            
            if not is_border:
                # Split by the vertical bar
                parts = line.split('│')
                
                # Clean up each cell
                cells = []
                for part in parts:
                    cell = part.strip()
                    if cell:  # Only include non-empty cells
                        cells.append(cell)
                
                if cells:
                    content_rows.append(cells)
    
    # Convert to HTML table
    if not content_rows:
        return '\n'.join(lines)
    
    html = ['<table class="table">']
    
    # Check if this is the 6軸システム table by looking for specific content
    is_six_axis_table = any('軸' in str(row) and '分析の焦点' in str(row) for row in content_rows)
    
    if is_six_axis_table and len(content_rows) > 0:
        # Special handling for 6軸システム table
        # First row might be a title, check if it has only one cell
        start_idx = 0
        if len(content_rows[0]) == 1 and '6軸システム' in content_rows[0][0]:
            # Skip the title row
            start_idx = 1
        
        # Next row should be headers
        if start_idx < len(content_rows):
            html.append('<thead>')
            html.append('<tr>')
            for cell in content_rows[start_idx]:
                html.append(f'<th>{cell}</th>')
            html.append('</tr>')
            html.append('</thead>')
            
            # Rest are body rows
            if len(content_rows) > start_idx + 1:
                html.append('<tbody>')
                for row in content_rows[start_idx + 1:]:
                    html.append('<tr>')
                    for cell in row:
                        html.append(f'<td>{cell}</td>')
                    html.append('</tr>')
                html.append('</tbody>')
    else:
        # Standard table handling
        # First row is header
        html.append('<thead>')
        html.append('<tr>')
        for cell in content_rows[0]:
            html.append(f'<th>{cell}</th>')
        html.append('</tr>')
        html.append('</thead>')
        
        # Rest are body rows
        if len(content_rows) > 1:
            html.append('<tbody>')
            for row in content_rows[1:]:
                html.append('<tr>')
                for cell in row:
                    html.append(f'<td>{cell}</td>')
                html.append('</tr>')
            html.append('</tbody>')
    
    html.append('</table>')
    return '\n'.join(html)

def process_lists(text):
    """Process markdown lists to HTML with better handling"""
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a list
        if re.match(r'^(\s*)[•\-\*]\s+', line):
            # Determine the indent level
            list_items = []
            current_indent = len(re.match(r'^(\s*)', line).group(1))
            
            # Collect all list items at this level or deeper
            while i < len(lines) and re.match(r'^(\s*)[•\-\*]\s+', lines[i]):
                indent = len(re.match(r'^(\s*)', lines[i]).group(1))
                content = re.sub(r'^(\s*)[•\-\*]\s+', '', lines[i])
                list_items.append((indent, content))
                i += 1
            
            # Convert to HTML
            result.append(convert_list_items_to_html(list_items, current_indent))
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def convert_list_items_to_html(items, base_indent=0):
    """Convert list items to HTML with proper nesting"""
    if not items:
        return ''
    
    html = ['<ul>']
    i = 0
    
    while i < len(items):
        indent, content = items[i]
        
        # Check if next items are more indented (nested)
        nested_items = []
        j = i + 1
        while j < len(items) and items[j][0] > indent:
            nested_items.append(items[j])
            j += 1
        
        # Add the list item
        if nested_items:
            # Has nested items
            html.append(f'<li>{content}')
            # Add nested list
            html.append(convert_list_items_to_html(nested_items, indent))
            html.append('</li>')
            i = j  # Skip the nested items
        else:
            # Simple item
            html.append(f'<li>{content}</li>')
            i += 1
    
    html.append('</ul>')
    return '\n'.join(html)

def simple_markdown_to_html(text):
    """Simple markdown to HTML conversion"""
    # First process code blocks to protect them
    text, code_blocks = process_code_blocks(text)
    
    # Convert tables
    text = convert_tables(text)
    
    # Convert headings - be more specific to avoid converting lines that just start with #
    text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Convert bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert italic (but be careful not to match bold)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Convert inline code - protect from further processing
    inline_codes = []
    def save_inline_code(match):
        code = match.group(1)
        formatted = f'<code>{escape_html(code)}</code>'
        inline_codes.append(formatted)
        return f'___INLINECODE_{len(inline_codes) - 1}___'
    
    text = re.sub(r'`([^`]+)`', save_inline_code, text)
    
    # Convert blockquotes
    lines = text.split('\n')
    result = []
    in_blockquote = False
    blockquote_lines = []
    
    for line in lines:
        if line.startswith('> '):
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            blockquote_lines.append(line[2:])
        else:
            if in_blockquote:
                result.append('<blockquote>' + '<br>'.join(blockquote_lines) + '</blockquote>')
                in_blockquote = False
                blockquote_lines = []
            result.append(line)
    
    if in_blockquote:
        result.append('<blockquote>' + '<br>'.join(blockquote_lines) + '</blockquote>')
    
    text = '\n'.join(result)
    
    # Process lists
    text = process_lists(text)
    
    # Convert [ ] checkboxes
    text = re.sub(r'\[\s*\]', '☐', text)
    text = re.sub(r'\[x\]', '☑', text, flags=re.IGNORECASE)
    
    # Convert paragraphs - but be smarter about it
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<') and not para.startswith('|') and not para.startswith('#') and not para.startswith('___'):
            # Check if it's not already wrapped in HTML tags
            if not re.match(r'^<[^>]+>', para):
                # Don't wrap if it's a plain list of items or contains block elements
                if not re.match(r'^(☐|☑)', para) and '___CODEBLOCK_' not in para and '___INLINECODE_' not in para:
                    # Also don't wrap lines that look like markdown formatting
                    if not re.match(r'^[-\*]{3,}$', para) and not re.match(r'^[=\-]{3,}$', para):
                        result.append(f'<p>{para}</p>')
                    else:
                        result.append(para)
                else:
                    result.append(para)
            else:
                result.append(para)
        else:
            result.append(para)
    
    text = '\n'.join(result)
    
    # Restore code blocks
    for i, code_block in enumerate(code_blocks):
        text = text.replace(f'___CODEBLOCK_{i}___', code_block)
    
    # Restore inline codes
    for i, inline_code in enumerate(inline_codes):
        text = text.replace(f'___INLINECODE_{i}___', inline_code)
    
    return text

def main():
    # Book root directory
    book_dir = Path(".claude/commands/parasol/docs/book")
    
    # Output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Collect all markdown files
    print("収集中のMarkdownファイル...")
    
    # Predefined chapter order
    chapters = [
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
    
    # Collect chapter information and content
    toc_entries = []
    all_content = []
    
    chapter_num = 1
    for part_name, chapter_files in chapters:
        part_dir = book_dir / part_name
        
        for chapter_file in chapter_files:
            file_path = part_dir / chapter_file
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                
                # Extract chapter info
                _, title = extract_chapter_info(content)
                
                if title:
                    # Create TOC entry with proper chapter number and title (no duplication)
                    toc_entries.append((f"chapter{chapter_num}", f"第{chapter_num}章　{title}"))
                    
                    # Add anchor for the chapter
                    all_content.append(f'<div id="chapter{chapter_num}" class="chapter">')
                    
                    # Process the content (which already has the full chapter heading)
                    all_content.append(content)
                    all_content.append('</div>')
                    
                    chapter_num += 1
    
    # Generate HTML
    html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parasol V5 完全ガイドブック</title>
    <style>
        body {
            font-family: 'Hiragino Mincho ProN', 'Yu Mincho', serif;
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
        
        .cover .version {
            margin-top: 50px;
            color: #95a5a6;
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
            margin-bottom: 30px;
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
            transition: color 0.3s;
        }
        
        .toc a:hover {
            color: #3498db;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
            margin-bottom: 30px;
            font-size: 2em;
        }
        
        h2 {
            color: #34495e;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        
        h3 {
            color: #7f8c8d;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        
        h4 {
            color: #95a5a6;
            margin-top: 20px;
            margin-bottom: 10px;
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
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tr:hover {
            background-color: #e3f2fd;
        }
        
        code {
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
        }
        
        pre {
            background-color: #282c34;
            color: #abb2bf;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            line-height: 1.4;
            white-space: pre;
            word-wrap: normal;
            margin: 15px 0;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
            color: inherit;
            font-size: 1em;
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
        
        ul, ol {
            margin-left: 20px;
            margin-bottom: 15px;
        }
        
        ul ul, ol ol, ul ol, ol ul {
            margin-left: 20px;
            margin-bottom: 0;
        }
        
        li {
            margin-bottom: 5px;
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
            pre {
                white-space: pre-wrap;
                word-wrap: break-word;
            }
        }
    </style>
</head>
<body>"""
    
    # Create cover page
    html_content = html_template + """
    <div class="cover">
        <h1>Parasol V5 完全ガイドブック</h1>
        <h2>価値駆動による実践的システム設計</h2>
        <p class="version">Version 1.0.0<br>2025年12月18日</p>
    </div>
"""
    
    # Add table of contents with fixed chapter titles
    html_content += '<div class="toc"><h1>目次</h1><ul>'
    for anchor, title in toc_entries:
        html_content += f'<li><a href="#{anchor}">{title}</a></li>'
    html_content += '</ul></div>\n'
    
    # Add processed content
    for content in all_content:
        # Convert markdown to HTML
        html = simple_markdown_to_html(content)
        html_content += html + '\n'
    
    html_content += """
</body>
</html>"""
    
    # Write HTML file
    output_file = output_dir / "parasol-v5-book.html"
    output_file.write_text(html_content, encoding='utf-8')
    
    print(f"✅ HTMLファイルを生成しました: {output_file}")
    print(f"📚 合計 {len(toc_entries)} 章を処理しました")
    
    # Show TOC for verification
    print("\n目次:")
    for _, title in toc_entries:
        print(f"  • {title}")

if __name__ == "__main__":
    main()