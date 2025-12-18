#!/usr/bin/env python3
"""Test table conversion"""

import re

test_content = """
6. multi-tier-vstr-axis（多層価値ストリーム軸）

問い：価値はどのように階層的に流れ、積み上がるか？

例：「現場→部門→全社」「店舗→地域→本部」「個人→チーム→組織」

┌────────────────────────────────────────────────────────────────────┐
│                    6軸システム                    │
├────────────────────┬───────────────────────────────────────────┤
│ 軸                 │ 問い（分析の焦点）                        │
├────────────────────┼───────────────────────────────────────────┤
│ capability-axis    │ 何ができるか？（能力）                    │
│ business-unit-axis │ 誰が担うか？（組織）                      │
│ value-axis         │ どんな価値か？（成果）                    │
│ platform-axis      │ 何が支えるか？（基盤）                    │
│ fusion-axis        │ 組み合わせ効果は？（融合）                │
│ multi-tier-vstr-axis │ どう積み上がるか？（階層）              │
└────────────────────┴───────────────────────────────────────────┘
"""

def convert_ascii_table_v2(lines):
    """Improved ASCII table conversion"""
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
    
    # First content row might be title
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

# Test the conversion
lines = test_content.strip().split('\n')
table_lines = []
in_table = False

for line in lines:
    if '┌' in line or '├' in line or '└' in line or '│' in line:
        in_table = True
        table_lines.append(line)
    elif in_table and line.strip() == '':
        # End of table
        if table_lines:
            html = convert_ascii_table_v2(table_lines)
            print("Converted HTML:")
            print(html)
            print("\n---\n")
        table_lines = []
        in_table = False

# Handle last table if any
if table_lines:
    html = convert_ascii_table_v2(table_lines)
    print("Converted HTML:")
    print(html)