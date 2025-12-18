#!/usr/bin/env python3
"""
Improved markdown to HTML converter with better table and formatting support
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict


class ImprovedMarkdownConverter:
    """Enhanced markdown to HTML converter"""
    
    def __init__(self):
        self.code_blocks = []
        self.inline_codes = []
    
    def convert(self, markdown: str) -> str:
        """Convert markdown to HTML with improved handling"""
        # Process in specific order to avoid conflicts
        html = markdown
        
        # 1. Protect code blocks and inline code first
        html = self._protect_code_blocks(html)
        html = self._protect_inline_code(html)
        
        # 2. Convert block elements
        html = self._convert_headers(html)
        html = self._convert_blockquotes(html)
        html = self._convert_tables(html)
        html = self._convert_lists(html)
        html = self._convert_horizontal_rules(html)
        
        # 3. Convert inline elements
        html = self._convert_emphasis(html)
        html = self._convert_links(html)
        html = self._convert_checkboxes(html)
        
        # 4. Convert paragraphs
        html = self._convert_paragraphs(html)
        
        # 5. Restore protected content
        html = self._restore_code_blocks(html)
        html = self._restore_inline_code(html)
        
        return html
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text
    
    def _protect_code_blocks(self, text: str) -> str:
        """Protect code blocks from processing"""
        self.code_blocks = []
        
        # Fenced code blocks with language
        def save_fenced(match):
            lang = match.group(1) or ''
            code = match.group(2)
            lang_class = f' class="language-{lang}"' if lang else ''
            self.code_blocks.append(f'<pre><code{lang_class}>{self._escape_html(code)}</code></pre>')
            return f'___CODEBLOCK_{len(self.code_blocks) - 1}___'
        
        text = re.sub(r'```(\w*)\n(.*?)\n```', save_fenced, text, flags=re.DOTALL)
        
        # Indented code blocks (4 spaces or tab)
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Detect indented code block
            if lines[i].startswith(('    ', '\t')):
                code_lines = []
                # Collect consecutive indented lines
                while i < len(lines) and (lines[i].startswith(('    ', '\t')) or not lines[i].strip()):
                    if lines[i].startswith('    '):
                        code_lines.append(lines[i][4:])
                    elif lines[i].startswith('\t'):
                        code_lines.append(lines[i][1:])
                    else:
                        code_lines.append(lines[i])
                    i += 1
                
                # Remove trailing empty lines
                while code_lines and not code_lines[-1].strip():
                    code_lines.pop()
                
                if code_lines:
                    code = '\n'.join(code_lines)
                    self.code_blocks.append(f'<pre><code>{self._escape_html(code)}</code></pre>')
                    result.append(f'___CODEBLOCK_{len(self.code_blocks) - 1}___')
            else:
                result.append(lines[i])
                i += 1
        
        return '\n'.join(result)
    
    def _protect_inline_code(self, text: str) -> str:
        """Protect inline code from processing"""
        self.inline_codes = []
        
        def save_inline(match):
            code = match.group(1)
            self.inline_codes.append(f'<code>{self._escape_html(code)}</code>')
            return f'___INLINECODE_{len(self.inline_codes) - 1}___'
        
        return re.sub(r'`([^`]+)`', save_inline, text)
    
    def _convert_headers(self, text: str) -> str:
        """Convert markdown headers to HTML"""
        # Convert headers from H6 to H1 (reverse order to avoid conflicts)
        for level in range(6, 0, -1):
            pattern = f'^{"#" * level} (.+)$'
            text = re.sub(pattern, f'<h{level}>\\1</h{level}>', text, flags=re.MULTILINE)
        return text
    
    def _convert_blockquotes(self, text: str) -> str:
        """Convert blockquotes to HTML"""
        lines = text.split('\n')
        result = []
        in_quote = False
        quote_lines = []
        
        for line in lines:
            if line.startswith('> '):
                if not in_quote:
                    in_quote = True
                    quote_lines = []
                quote_lines.append(line[2:])
            elif line.startswith('>') and not line[1:].strip():
                # Empty quote line
                if in_quote:
                    quote_lines.append('')
            else:
                if in_quote:
                    # End of blockquote
                    result.append('<blockquote>' + '<br>'.join(quote_lines) + '</blockquote>')
                    in_quote = False
                    quote_lines = []
                result.append(line)
        
        # Handle blockquote at end of text
        if in_quote:
            result.append('<blockquote>' + '<br>'.join(quote_lines) + '</blockquote>')
        
        return '\n'.join(result)
    
    def _convert_tables(self, text: str) -> str:
        """Convert markdown tables to HTML"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Check if this looks like a table row
            if '|' in lines[i] and not lines[i].strip().startswith('___'):
                table_lines = []
                
                # Collect consecutive lines with pipes
                while i < len(lines) and '|' in lines[i] and not lines[i].strip().startswith('___'):
                    table_lines.append(lines[i])
                    i += 1
                
                # Check if we have at least 2 lines and second line is separator
                if len(table_lines) >= 2:
                    # Check if second line is separator
                    cells = [cell.strip() for cell in table_lines[1].split('|')]
                    cells = [c for c in cells if c]  # Remove empty strings
                    
                    is_separator = all(
                        all(ch in '-: ' for ch in cell) and '-' in cell
                        for cell in cells
                    )
                    
                    if is_separator:
                        # This is a proper markdown table
                        result.append(self._build_html_table(table_lines))
                        continue
                
                # Not a table, add lines back
                result.extend(table_lines)
            else:
                result.append(lines[i])
                i += 1
        
        return '\n'.join(result)
    
    def _build_html_table(self, lines: List[str]) -> str:
        """Build HTML table from markdown table lines"""
        if len(lines) < 2:
            return '\n'.join(lines)
        
        # Parse alignment from separator line
        separator_cells = [cell.strip() for cell in lines[1].split('|')]
        alignments = []
        for cell in separator_cells:
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.endswith(':'):
                alignments.append('right')
            elif cell.startswith(':'):
                alignments.append('left')
            else:
                alignments.append('')
        
        html = ['<table>']
        
        # Parse header row
        header_cells = [cell.strip() for cell in lines[0].split('|')]
        header_cells = [c for c in header_cells if c]  # Remove empty
        
        html.append('<thead>')
        html.append('<tr>')
        for i, cell in enumerate(header_cells):
            align = f' style="text-align: {alignments[i]}"' if i < len(alignments) and alignments[i] else ''
            html.append(f'<th{align}>{cell}</th>')
        html.append('</tr>')
        html.append('</thead>')
        
        # Parse body rows (skip separator)
        if len(lines) > 2:
            html.append('<tbody>')
            for line in lines[2:]:
                cells = [cell.strip() for cell in line.split('|')]
                cells = [c for c in cells if c or cells.index(c) != 0 and cells.index(c) != len(cells)-1]
                
                html.append('<tr>')
                for i, cell in enumerate(cells):
                    align = f' style="text-align: {alignments[i]}"' if i < len(alignments) and alignments[i] else ''
                    html.append(f'<td{align}>{cell}</td>')
                html.append('</tr>')
            html.append('</tbody>')
        
        html.append('</table>')
        return '\n'.join(html)
    
    def _convert_lists(self, text: str) -> str:
        """Convert markdown lists to HTML"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Check for unordered list
            if re.match(r'^(\s*)[-*+] ', lines[i]):
                list_lines = []
                list_type = 'ul'
                base_indent = len(re.match(r'^(\s*)', lines[i]).group(1))
                
                # Collect list items
                while i < len(lines) and re.match(r'^(\s*)[-*+] ', lines[i]):
                    indent = len(re.match(r'^(\s*)', lines[i]).group(1))
                    content = re.sub(r'^(\s*)[-*+] ', '', lines[i])
                    list_lines.append((indent - base_indent, content))
                    i += 1
                
                result.append(self._build_nested_list(list_lines, list_type))
                
            # Check for ordered list
            elif re.match(r'^(\s*)\d+\. ', lines[i]):
                list_lines = []
                list_type = 'ol'
                base_indent = len(re.match(r'^(\s*)', lines[i]).group(1))
                
                # Collect list items
                while i < len(lines) and re.match(r'^(\s*)\d+\. ', lines[i]):
                    indent = len(re.match(r'^(\s*)', lines[i]).group(1))
                    content = re.sub(r'^(\s*)\d+\. ', '', lines[i])
                    list_lines.append((indent - base_indent, content))
                    i += 1
                
                result.append(self._build_nested_list(list_lines, list_type))
                
            else:
                result.append(lines[i])
                i += 1
        
        return '\n'.join(result)
    
    def _build_nested_list(self, items: List[Tuple[int, str]], list_type: str) -> str:
        """Build nested HTML list"""
        if not items:
            return ''
        
        html = [f'<{list_type}>']
        
        i = 0
        while i < len(items):
            indent, content = items[i]
            
            # Check if next items are more indented (nested)
            nested_items = []
            j = i + 1
            while j < len(items) and items[j][0] > indent:
                nested_items.append((items[j][0] - indent - 2, items[j][1]))
                j += 1
            
            if nested_items:
                html.append(f'<li>{content}')
                html.append(self._build_nested_list(nested_items, list_type))
                html.append('</li>')
                i = j
            else:
                html.append(f'<li>{content}</li>')
                i += 1
        
        html.append(f'</{list_type}>')
        return '\n'.join(html)
    
    def _convert_emphasis(self, text: str) -> str:
        """Convert bold and italic"""
        # Bold (must come before italic to handle ***)
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        
        # Italic
        text = re.sub(r'(?<!\*)\*([^\*]+?)\*(?!\*)', r'<em>\1</em>', text)
        text = re.sub(r'(?<!_)_([^_]+?)_(?!_)', r'<em>\1</em>', text)
        
        return text
    
    def _convert_links(self, text: str) -> str:
        """Convert markdown links"""
        # Links [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Images ![alt](url)
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
        
        return text
    
    def _convert_horizontal_rules(self, text: str) -> str:
        """Convert horizontal rules"""
        # Three or more -, *, or _
        text = re.sub(r'^([-*_])\1{2,}\s*$', '<hr>', text, flags=re.MULTILINE)
        return text
    
    def _convert_checkboxes(self, text: str) -> str:
        """Convert checkboxes"""
        text = re.sub(r'\[\s*\]', '☐', text)
        text = re.sub(r'\[[xX]\]', '☑', text)
        return text
    
    def _convert_paragraphs(self, text: str) -> str:
        """Convert paragraphs"""
        # Split by double newlines
        blocks = text.split('\n\n')
        result = []
        
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            
            # Skip if already has HTML tags or is special content
            if (block.startswith('<') or 
                block.startswith('___') or 
                block.startswith('|') or
                re.match(r'^[-*#]', block)):
                result.append(block)
            else:
                # Check if it's a plain text paragraph
                if not re.match(r'^<[^>]+>', block):
                    result.append(f'<p>{block}</p>')
                else:
                    result.append(block)
        
        return '\n\n'.join(result)
    
    def _restore_code_blocks(self, text: str) -> str:
        """Restore code blocks"""
        for i, code_block in enumerate(self.code_blocks):
            text = text.replace(f'___CODEBLOCK_{i}___', code_block)
        return text
    
    def _restore_inline_code(self, text: str) -> str:
        """Restore inline code"""
        for i, inline_code in enumerate(self.inline_codes):
            text = text.replace(f'___INLINECODE_{i}___', inline_code)
        return text


def test_improved_converter():
    """Test the improved converter"""
    print("Testing Improved Markdown Converter")
    print("=" * 50)
    
    # Read test file
    test_file = Path("test-markdown-features.md")
    content = test_file.read_text(encoding='utf-8')
    
    # Convert
    converter = ImprovedMarkdownConverter()
    html = converter.convert(content)
    
    # Save output
    output_file = Path("output/improved-markdown-test.html")
    
    # Create HTML document
    html_doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Improved Markdown Test</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown-light.min.css">
    <style>
        body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }}
        .markdown-body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        table td, table th {{
            border: 1px solid #ddd;
            padding: 8px 12px;
        }}
        table th {{
            background-color: #f6f8fa;
            font-weight: 600;
        }}
        table tr:nth-child(even) {{
            background-color: #f6f8fa;
        }}
    </style>
</head>
<body>
    <article class="markdown-body">
        {html}
    </article>
</body>
</html>"""
    
    output_file.write_text(html_doc, encoding='utf-8')
    
    # Check features
    print("\n✅ Conversion completed!")
    print(f"📄 Output: {output_file}")
    
    # Feature check
    features = {
        "Tables": html.count('<table>'),
        "Code blocks": html.count('<pre>'),
        "Blockquotes": html.count('<blockquote>'),
        "Lists": html.count('<ul>') + html.count('<ol>'),
        "Headers": sum(html.count(f'<h{i}>') for i in range(1, 7)),
        "Inline code": html.count('<code>') - html.count('<pre><code'),
    }
    
    print("\n📊 Conversion statistics:")
    for feature, count in features.items():
        print(f"  {feature}: {count}")


if __name__ == "__main__":
    test_improved_converter()