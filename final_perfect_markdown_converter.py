#!/usr/bin/env python3
"""
Final perfect markdown to HTML converter with complete blockquote table support
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict


class FinalPerfectMarkdownConverter:
    """Final perfect markdown to HTML converter"""
    
    def __init__(self):
        self.code_blocks = []
        self.inline_codes = []
    
    def convert(self, markdown: str) -> str:
        """Convert markdown to HTML with complete support"""
        html = markdown
        
        # 1. Protect code blocks and inline code first
        html = self._protect_code_blocks(html)
        html = self._protect_inline_code(html)
        
        # 2. Process blockquotes with ALL nested content
        html = self._convert_blockquotes_complete(html)
        
        # 3. Convert block elements (outside blockquotes)
        html = self._convert_headers(html)
        html = self._convert_tables(html)
        html = self._convert_lists(html)
        html = self._convert_horizontal_rules(html)
        
        # 4. Convert inline elements
        html = self._convert_emphasis_safe(html)
        html = self._convert_links(html)
        html = self._convert_checkboxes(html)
        
        # 5. Convert paragraphs
        html = self._convert_paragraphs(html)
        
        # 6. Restore protected content
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
        
        # Fenced code blocks
        def save_fenced(match):
            lang = match.group(1) or ''
            code = match.group(2).rstrip()
            lang_class = f' class="language-{lang}"' if lang else ''
            self.code_blocks.append(f'<pre><code{lang_class}>{self._escape_html(code)}</code></pre>')
            return f'___CODEBLOCK_{len(self.code_blocks) - 1}___'
        
        text = re.sub(r'```(\w*)\n(.*?)```', save_fenced, text, flags=re.DOTALL)
        
        # Indented code blocks
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Skip if in blockquote
            if lines[i].startswith('>'):
                result.append(lines[i])
                i += 1
                continue
                
            # Check for indented code block
            if lines[i].startswith(('    ', '\t')):
                # Make sure previous line is empty
                if i > 0 and not lines[i-1].strip() and not lines[i-1].startswith('>'):
                    code_lines = []
                    while i < len(lines) and (lines[i].startswith(('    ', '\t')) or not lines[i].strip()):
                        if lines[i].startswith('    '):
                            code_lines.append(lines[i][4:])
                        elif lines[i].startswith('\t'):
                            code_lines.append(lines[i][1:])
                        else:
                            code_lines.append(lines[i])
                        i += 1
                    
                    while code_lines and not code_lines[-1].strip():
                        code_lines.pop()
                    
                    if code_lines:
                        code = '\n'.join(code_lines)
                        self.code_blocks.append(f'<pre><code>{self._escape_html(code)}</code></pre>')
                        result.append(f'___CODEBLOCK_{len(self.code_blocks) - 1}___')
                        continue
            
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
    
    def _convert_blockquotes_complete(self, text: str) -> str:
        """Convert blockquotes with complete nested content support"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            if lines[i].startswith('>'):
                # Start collecting blockquote
                quote_lines = []
                
                # Collect all lines that are part of this blockquote
                while i < len(lines) and (lines[i].startswith('>') or 
                                         (i > 0 and lines[i-1].startswith('>') and lines[i].strip() == '')):
                    # Remove the '> ' or '>' prefix
                    if lines[i].startswith('> '):
                        quote_lines.append(lines[i][2:])
                    elif lines[i].startswith('>'):
                        quote_lines.append(lines[i][1:])
                    else:
                        quote_lines.append('')
                    i += 1
                
                if quote_lines:
                    # Process ALL content inside the blockquote
                    quote_content = '\n'.join(quote_lines)
                    
                    # Apply ALL conversions to blockquote content
                    # Headers
                    for level in range(6, 0, -1):
                        pattern = f'^{"#" * level} (.+)$'
                        quote_content = re.sub(pattern, f'<h{level}>\\1</h{level}>', quote_content, flags=re.MULTILINE)
                    
                    # Tables (special handling for blockquote tables)
                    quote_content = self._convert_blockquote_tables(quote_content)
                    
                    # Lists
                    quote_content = self._convert_blockquote_lists(quote_content)
                    
                    # Links and emphasis
                    quote_content = self._convert_links(quote_content)
                    quote_content = self._apply_emphasis(quote_content)
                    
                    # Convert paragraphs in blockquote
                    quote_lines = quote_content.split('\n')
                    formatted_lines = []
                    para_lines = []
                    
                    for line in quote_lines:
                        if line.strip().startswith('<') or not line.strip():
                            if para_lines:
                                formatted_lines.append(f'<p>{" ".join(para_lines)}</p>')
                                para_lines = []
                            if line.strip():
                                formatted_lines.append(line)
                        else:
                            para_lines.append(line)
                    
                    if para_lines:
                        formatted_lines.append(f'<p>{" ".join(para_lines)}</p>')
                    
                    quote_content = '\n'.join(formatted_lines)
                    
                    # Wrap in blockquote
                    result.append(f'<blockquote>\n{quote_content}\n</blockquote>')
            else:
                result.append(lines[i])
                i += 1
        
        return '\n'.join(result)
    
    def _convert_blockquote_tables(self, text: str) -> str:
        """Convert tables inside blockquotes"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Check if this looks like a table row
            if '|' in lines[i] and not lines[i].strip().startswith('___'):
                # Look ahead to see if this is a table
                is_table = False
                if i + 1 < len(lines) and '|' in lines[i + 1]:
                    # Check if second line is separator
                    cells = [cell.strip() for cell in lines[i + 1].split('|')]
                    cells = [c for c in cells if c]
                    if cells:
                        is_separator = all(
                            all(ch in '-: ' for ch in cell) and '-' in cell
                            for cell in cells
                        )
                        if is_separator:
                            is_table = True
                
                if is_table:
                    table_lines = []
                    # Collect table lines
                    while i < len(lines) and '|' in lines[i]:
                        table_lines.append(lines[i])
                        i += 1
                    
                    if len(table_lines) >= 2:
                        result.append(self._build_html_table(table_lines))
                        continue
            
            result.append(lines[i])
            i += 1
        
        return '\n'.join(result)
    
    def _convert_blockquote_lists(self, text: str) -> str:
        """Convert lists inside blockquotes"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Check for unordered list
            if re.match(r'^(\s*)[-*+] ', lines[i]):
                list_lines = []
                list_type = 'ul'
                
                while i < len(lines) and re.match(r'^(\s*)[-*+] ', lines[i]):
                    content = re.sub(r'^(\s*)[-*+] ', '', lines[i])
                    list_lines.append((0, content))
                    i += 1
                
                if list_lines:
                    result.append(self._build_simple_list(list_lines, list_type))
                    continue
                    
            # Check for ordered list
            elif re.match(r'^(\s*)\d+\. ', lines[i]):
                list_lines = []
                list_type = 'ol'
                
                while i < len(lines) and re.match(r'^(\s*)\d+\. ', lines[i]):
                    content = re.sub(r'^(\s*)\d+\. ', '', lines[i])
                    list_lines.append((0, content))
                    i += 1
                
                if list_lines:
                    result.append(self._build_simple_list(list_lines, list_type))
                    continue
            
            result.append(lines[i])
            i += 1
        
        return '\n'.join(result)
    
    def _build_simple_list(self, items: List[Tuple[int, str]], list_type: str) -> str:
        """Build simple HTML list"""
        if not items:
            return ''
        
        html = [f'<{list_type}>']
        for _, content in items:
            html.append(f'<li>{content}</li>')
        html.append(f'</{list_type}>')
        
        return '\n'.join(html)
    
    def _convert_headers(self, text: str) -> str:
        """Convert markdown headers to HTML"""
        for level in range(6, 0, -1):
            pattern = f'^{"#" * level} (.+)$'
            text = re.sub(pattern, f'<h{level}>\\1</h{level}>', text, flags=re.MULTILINE)
        return text
    
    def _convert_tables(self, text: str) -> str:
        """Convert markdown tables to HTML (outside blockquotes)"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Skip protected content and blockquotes
            if '___CODEBLOCK_' in lines[i] or '___INLINECODE_' in lines[i] or lines[i].startswith('<blockquote'):
                result.append(lines[i])
                i += 1
                continue
                
            # Check if this looks like a table row
            if '|' in lines[i]:
                # Look ahead to see if this is a table
                is_table = False
                if i + 1 < len(lines) and '|' in lines[i + 1]:
                    # Check if second line is separator
                    cells = [cell.strip() for cell in lines[i + 1].split('|')]
                    cells = [c for c in cells if c]
                    if cells:
                        is_separator = all(
                            all(ch in '-: ' for ch in cell) and '-' in cell
                            for cell in cells
                        )
                        if is_separator:
                            is_table = True
                
                if is_table:
                    table_lines = []
                    # Collect table lines
                    while i < len(lines) and '|' in lines[i] and '___CODEBLOCK_' not in lines[i]:
                        table_lines.append(lines[i])
                        i += 1
                    
                    if len(table_lines) >= 2:
                        result.append(self._build_html_table(table_lines))
                        continue
            
            result.append(lines[i])
            i += 1
        
        return '\n'.join(result)
    
    def _build_html_table(self, lines: List[str]) -> str:
        """Build HTML table from markdown table lines"""
        if len(lines) < 2:
            return '\n'.join(lines)
        
        # Parse alignment from separator line
        separator_cells = [cell.strip() for cell in lines[1].split('|')]
        separator_cells = [c for c in separator_cells if c]
        
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
        header_cells = [c for c in header_cells if c]
        
        html.append('<thead>')
        html.append('<tr>')
        for i, cell in enumerate(header_cells):
            align = f' style="text-align: {alignments[i]}"' if i < len(alignments) and alignments[i] else ''
            # Process inline elements in cells
            cell = self._process_cell_content(cell)
            html.append(f'<th{align}>{cell}</th>')
        html.append('</tr>')
        html.append('</thead>')
        
        # Parse body rows
        if len(lines) > 2:
            html.append('<tbody>')
            for line in lines[2:]:
                cells = [cell.strip() for cell in line.split('|')]
                cells = [c for c in cells if c]
                
                html.append('<tr>')
                for i, cell in enumerate(cells):
                    align = f' style="text-align: {alignments[i]}"' if i < len(alignments) and alignments[i] else ''
                    # Process inline elements in cells
                    cell = self._process_cell_content(cell)
                    html.append(f'<td{align}>{cell}</td>')
                html.append('</tr>')
            html.append('</tbody>')
        
        html.append('</table>')
        return '\n'.join(html)
    
    def _process_cell_content(self, cell: str) -> str:
        """Process inline markdown in table cells"""
        # Links
        cell = self._convert_links(cell)
        # Emphasis
        cell = self._apply_emphasis(cell)
        return cell
    
    def _convert_lists(self, text: str) -> str:
        """Convert markdown lists to HTML (outside blockquotes)"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Skip if in blockquote
            if lines[i].startswith('>') or lines[i].startswith('<blockquote'):
                result.append(lines[i])
                i += 1
                continue
                
            # Check for unordered list
            if re.match(r'^(\s*)[-*+] ', lines[i]):
                list_lines = []
                list_type = 'ul'
                base_indent = len(re.match(r'^(\s*)', lines[i]).group(1))
                
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
        
        for indent, content in items:
            html.append(f'<li>{content}</li>')
        
        html.append(f'</{list_type}>')
        return '\n'.join(html)
    
    def _convert_emphasis_safe(self, text: str) -> str:
        """Convert bold and italic, protecting placeholders"""
        # Split by placeholder patterns
        parts = []
        current_pos = 0
        
        # Find all placeholders
        placeholder_pattern = r'(___(?:CODEBLOCK|INLINECODE)_\d+___)'
        
        for match in re.finditer(placeholder_pattern, text):
            # Process text before placeholder
            before_text = text[current_pos:match.start()]
            if before_text:
                # Apply emphasis to this part
                before_text = self._apply_emphasis(before_text)
                parts.append(before_text)
            
            # Add placeholder as-is
            parts.append(match.group(0))
            current_pos = match.end()
        
        # Process remaining text
        if current_pos < len(text):
            remaining = text[current_pos:]
            remaining = self._apply_emphasis(remaining)
            parts.append(remaining)
        
        return ''.join(parts)
    
    def _apply_emphasis(self, text: str) -> str:
        """Apply emphasis conversions to text"""
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
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
        return text
    
    def _convert_horizontal_rules(self, text: str) -> str:
        """Convert horizontal rules"""
        text = re.sub(r'^([-*_])\1{2,}\s*$', '<hr>', text, flags=re.MULTILINE)
        return text
    
    def _convert_checkboxes(self, text: str) -> str:
        """Convert checkboxes"""
        text = re.sub(r'\[\s*\]', '☐', text)
        text = re.sub(r'\[[xX]\]', '☑', text)
        return text
    
    def _convert_paragraphs(self, text: str) -> str:
        """Convert paragraphs"""
        blocks = text.split('\n\n')
        result = []
        
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            
            # Skip if already HTML, special content, or contains placeholders
            if (block.startswith(('<', '|')) or 
                re.match(r'^[-*#]', block) or
                '___CODEBLOCK_' in block or '___INLINECODE_' in block or
                block.startswith('☐') or block.startswith('☑')):
                result.append(block)
            else:
                # Plain text paragraph
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