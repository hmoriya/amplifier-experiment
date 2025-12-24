#!/usr/bin/env python3
"""
Test markdown conversion capabilities
"""

import re
from pathlib import Path
from generate_book_simple import SimpleBookGenerator


def test_markdown_features():
    """Test various markdown features"""
    print("Markdown Conversion Test")
    print("=" * 50)
    
    # Read test document
    test_file = Path("test-markdown-features.md")
    if not test_file.exists():
        print("❌ Test file not found!")
        return
    
    content = test_file.read_text(encoding='utf-8')
    
    # Initialize converter
    generator = SimpleBookGenerator(
        book_dir=Path("."),  # Not used in this test
        output_dir=Path("output")
    )
    
    # Test conversion
    html_content = generator.convert_markdown_to_html(content)
    
    # Save test output
    output_file = Path("output/test-markdown-conversion.html")
    
    # Create complete HTML document for testing
    html_doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown変換テスト</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        h1, h2, h3, h4 {{
            margin-top: 24px;
            margin-bottom: 16px;
        }}
        
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-bottom: 1px solid #ecf0f1; padding-bottom: 5px; }}
        h3 {{ color: #7f8c8d; }}
        h4 {{ color: #95a5a6; }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: white;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
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
            margin: 16px 0;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #abb2bf;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 16px 0;
            padding: 10px 20px;
            background-color: #f1f8ff;
            color: #555;
        }}
        
        ul, ol {{
            margin: 16px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 32px 0;
        }}
        
        /* Test result indicators */
        .test-success {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        
        .test-fail {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        
        .test-info {{
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="test-info">
        <strong>📋 Markdown変換テスト結果</strong><br>
        このページは、Markdown処理機能のテスト結果を表示しています。
    </div>
    
    {html_content}
    
    <hr>
    
    <div class="test-info">
        <strong>🔍 変換機能の確認ポイント：</strong>
        <ul>
            <li>基本的なテキスト装飾（太字、イタリック、インラインコード）</li>
            <li>見出しレベル（H1〜H4）</li>
            <li>リスト（順序あり/なし、ネスト、チェックボックス）</li>
            <li>テーブル（標準Markdownテーブル）</li>
            <li>コードブロック（言語指定あり/なし）</li>
            <li>引用ブロック</li>
            <li>リンク</li>
            <li>水平線</li>
        </ul>
    </div>
</body>
</html>"""
    
    output_file.write_text(html_doc, encoding='utf-8')
    
    # Analyze conversion results
    print("\n📊 Conversion Analysis:")
    print("-" * 50)
    
    # Check what was converted successfully
    features = {
        "Headers (H1-H4)": bool(re.search(r'<h[1-4]>', html_content)),
        "Bold text": bool(re.search(r'<strong>', html_content)),
        "Italic text": bool(re.search(r'<em>', html_content)),
        "Inline code": bool(re.search(r'<code>', html_content)),
        "Code blocks": bool(re.search(r'<pre>', html_content)),
        "Tables": bool(re.search(r'<table>', html_content)),
        "Lists": bool(re.search(r'<ul>|<ol>', html_content)),
        "Links": bool(re.search(r'<a href=', html_content)),
        "Blockquotes": bool(re.search(r'<blockquote>', html_content)),
        "Checkboxes": bool(re.search(r'☐|☑', html_content)),
    }
    
    for feature, supported in features.items():
        status = "✅" if supported else "❌"
        print(f"{status} {feature}")
    
    print(f"\n📄 Test output saved to: {output_file}")
    print("\n🌐 Open the HTML file in a browser to see the visual result.")
    
    # Additional detailed checks
    print("\n📋 Detailed Checks:")
    print("-" * 50)
    
    # Check table conversion
    table_count = html_content.count('<table>')
    print(f"Tables found: {table_count}")
    
    # Check code block conversion
    code_block_count = html_content.count('<pre>')
    print(f"Code blocks found: {code_block_count}")
    
    # Check list conversion
    ul_count = html_content.count('<ul>')
    ol_count = html_content.count('<ol>')
    print(f"Unordered lists: {ul_count}, Ordered lists: {ol_count}")
    
    # Generate a simple report
    report_file = Path("output/markdown-test-report.txt")
    report = f"""Markdown Conversion Test Report
{'=' * 50}

Test Date: {Path(test_file).stat().st_mtime}
Input File: {test_file}
Output File: {output_file}

Conversion Results:
{'-' * 30}
"""
    
    for feature, supported in features.items():
        report += f"{feature}: {'Supported' if supported else 'Not Supported'}\n"
    
    report += f"""
Detailed Statistics:
{'-' * 30}
Tables converted: {table_count}
Code blocks converted: {code_block_count}
Unordered lists: {ul_count}
Ordered lists: {ol_count}

Notes:
- Mermaid diagrams: Not yet supported (requires external renderer)
- LaTeX math: Not yet supported
- Complex nested structures: Partially supported
"""
    
    report_file.write_text(report, encoding='utf-8')
    print(f"\n📊 Detailed report saved to: {report_file}")


if __name__ == "__main__":
    test_markdown_features()