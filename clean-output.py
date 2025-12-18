#!/usr/bin/env python3
"""Clean up any remaining formatting issues in the HTML"""

from pathlib import Path
import re

# Read the HTML file
html_file = Path("output/parasol-v5-book.html")
content = html_file.read_text(encoding='utf-8')

# Fix any remaining Markdown table syntax that wasn't converted
# This pattern matches lines with | separators that aren't in <pre> blocks
def fix_remaining_tables(content):
    lines = content.split('\n')
    result = []
    in_pre = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Track pre blocks
        if '<pre>' in line:
            in_pre = True
        if '</pre>' in line:
            in_pre = False
        
        # If we find a line with pipes and we're not in a pre block or table
        if not in_pre and '|' in line and not any(tag in line for tag in ['<table', '<tr>', '<td>', '<th>', '</table>']):
            # Check if this looks like a Markdown table
            if line.strip().startswith('|') and line.strip().endswith('|'):
                # Start collecting table lines
                table_lines = []
                while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                    table_lines.append(lines[i].strip())
                    i += 1
                
                # Convert to HTML table
                if len(table_lines) >= 2:
                    html_table = ['<table class="table">']
                    
                    # Check if second line is separator
                    is_markdown_table = len(table_lines) > 1 and all(c in '-|: ' for c in table_lines[1])
                    
                    if is_markdown_table:
                        # Process header
                        header_cells = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]
                        html_table.append('<thead><tr>')
                        for cell in header_cells:
                            html_table.append(f'<th>{cell}</th>')
                        html_table.append('</tr></thead>')
                        
                        # Process body
                        if len(table_lines) > 2:
                            html_table.append('<tbody>')
                            for row in table_lines[2:]:
                                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                                html_table.append('<tr>')
                                for cell in cells:
                                    html_table.append(f'<td>{cell}</td>')
                                html_table.append('</tr>')
                            html_table.append('</tbody>')
                    else:
                        # Not a valid Markdown table, just add as-is
                        for tl in table_lines:
                            result.append(tl)
                        continue
                    
                    html_table.append('</table>')
                    result.extend(html_table)
                    continue
                else:
                    # Just add the lines
                    result.extend(table_lines)
                    continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

# Apply fixes
content = fix_remaining_tables(content)

# Write back
html_file.write_text(content, encoding='utf-8')

print("✅ HTMLファイルをクリーンアップしました: output/parasol-v5-book.html")