#!/usr/bin/env python3
"""Debug table conversion to see what's happening"""

test_content = """
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

def debug_ascii_table(lines):
    """Debug ASCII table parsing"""
    print("=== DEBUG ASCII TABLE ===")
    print(f"Total lines: {len(lines)}")
    print()
    
    content_rows = []
    
    for i, line in enumerate(lines):
        print(f"Line {i}: {repr(line)}")
        
        # Skip empty lines
        if not line.strip():
            print("  -> Empty line, skipping")
            continue
            
        # Check if border line
        is_border = all(c in '─━┌├└┼┬┴┤┐┘│' or c.isspace() for c in line)
        print(f"  -> Is border: {is_border}")
        
        # Extract content from lines with vertical bars
        if '│' in line and not is_border:
            # Split by box-drawing vertical bar
            parts = line.split('│')
            print(f"  -> Split into {len(parts)} parts")
            
            # Clean up each cell
            cells = []
            for j, part in enumerate(parts):
                cell = part.strip()
                if cell:  # Only include non-empty cells
                    cells.append(cell)
                    print(f"     Cell {j}: '{cell}'")
            
            if cells:
                content_rows.append(cells)
                print(f"  -> Added row with {len(cells)} cells")
        print()
    
    print(f"\nTotal content rows: {len(content_rows)}")
    for i, row in enumerate(content_rows):
        print(f"Row {i}: {row}")

# Test
lines = test_content.strip().split('\n')
debug_ascii_table(lines)