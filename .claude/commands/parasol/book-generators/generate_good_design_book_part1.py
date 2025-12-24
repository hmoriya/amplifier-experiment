#!/usr/bin/env python3
"""
Generate Good Design Book Part 1 with diagram generation
"""

import logging
import sys
from pathlib import Path
import re
from typing import List
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the diagram generation functions from the existing module
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Import only the main conversion function
from generate_book_with_diagrams import convert_markdown_to_html

def generate_good_design_book_part1():
    """Generate Part 1 of the Good Design book"""
    
    # Book paths
    book_dir = script_dir / '.claude/commands/parasol/docs/good-design-book/part1-redefining'
    output_dir = script_dir / 'generated_books'
    output_dir.mkdir(exist_ok=True)
    
    logger.info(f"📚 Starting Good Design Book Part 1 generation...")
    logger.info(f"Source: {book_dir}")
    logger.info(f"Output: {output_dir}")
    
    # Book metadata
    now = datetime.now()
    metadata = {
        'title': '価値駆動設計 ― Parasol V5で実現する良い設計の本質',
        'subtitle': '第I部：良い設計の再定義',
        'author': 'Parasol V5 Team',
        'date': now.strftime('%Y年%m月%d日'),
        'version': '1.0',
    }
    
    # Collect chapters
    chapters = []
    
    # Add chapters in order
    chapter_files = [
        'chapter1-why-correct-design-fails.md',
        'chapter2-parasol-v5-good-design.md',
        'chapter3-multidimensional-quality.md'  # Will be created
    ]
    
    for chapter_file in chapter_files[:2]:  # Only process existing chapters
        chapter_path = book_dir / chapter_file
        if chapter_path.exists():
            logger.info(f"Processing: {chapter_file}")
            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()
            chapters.append({
                'title': extract_chapter_title(content),
                'content': content
            })
        else:
            logger.warning(f"Chapter file not found: {chapter_file}")
    
    # Generate HTML
    html_content = generate_html(metadata, chapters)
    
    # Save HTML
    output_path = output_dir / 'good-design-book-part1.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"✅ HTML generated: {output_path}")
    logger.info(f"   File size: {output_path.stat().st_size:,} bytes")
    
    # Try to open in browser
    import webbrowser
    import os
    file_url = f"file://{os.path.abspath(output_path)}"
    logger.info(f"🌐 Opening in browser: {file_url}")
    webbrowser.open(file_url)
    
    return str(output_path)

def extract_chapter_title(content):
    """Extract chapter title from markdown content"""
    lines = content.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return "無題"

def generate_html(metadata, chapters):
    """Generate complete HTML document"""
    
    # Process chapters
    processed_chapters = []
    for chapter in chapters:
        processed_content = convert_markdown_to_html(chapter['content'])
        processed_chapters.append({
            'title': chapter['title'],
            'content': processed_content
        })
    
    # Create TOC
    toc_items = []
    for i, chapter in enumerate(processed_chapters, 1):
        toc_items.append(f'<li><a href="#chapter{i}">{chapter["title"]}</a></li>')
    toc_html = '<ul class="toc">\n' + '\n'.join(toc_items) + '\n</ul>'
    
    # Create chapter HTML
    chapters_html = []
    for i, chapter in enumerate(processed_chapters, 1):
        chapter_html = f'''
<section id="chapter{i}" class="chapter">
{chapter["content"]}
</section>
'''
        chapters_html.append(chapter_html)
    
    # Complete HTML
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata["title"]} - {metadata["subtitle"]}</title>
    <style>
        body {{
            font-family: "游ゴシック", "Yu Gothic", "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 0.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
        }}
        h2 {{
            font-size: 2em;
            color: #34495e;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 0.3em;
        }}
        h3 {{
            font-size: 1.5em;
            color: #34495e;
            margin-top: 1.2em;
            margin-bottom: 0.5em;
        }}
        h4 {{
            font-size: 1.2em;
            color: #34495e;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }}
        p {{
            margin: 1em 0;
            text-align: justify;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: Consolas, Monaco, 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            line-height: 1.4;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 1.5em 0;
            padding: 0.5em 1em;
            background-color: #ecf8ff;
            font-style: italic;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .toc {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 20px;
            margin: 2em 0;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 20px;
        }}
        .toc > ul {{
            padding-left: 0;
        }}
        .toc a {{
            color: #007bff;
            text-decoration: none;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        .chapter {{
            margin-top: 3em;
            page-break-before: always;
        }}
        .title-page {{
            text-align: center;
            padding: 100px 0;
            page-break-after: always;
        }}
        .title-page h1 {{
            font-size: 3em;
            border: none;
            margin-bottom: 0.5em;
        }}
        .title-page h2 {{
            font-size: 2em;
            color: #7f8c8d;
            font-weight: normal;
            border: none;
        }}
        .metadata {{
            margin-top: 3em;
            color: #7f8c8d;
        }}
        .architecture-diagram {{
            margin: 20px 0;
            background: #f8f8f8;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        .architecture-diagram pre {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.2;
            white-space: pre;
            margin: 0;
            border: none;
            padding: 0;
            background: transparent;
        }}
        .practice-example {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        ul, ol {{
            margin: 1em 0;
            padding-left: 2em;
        }}
        li {{
            margin: 0.5em 0;
        }}
        strong {{
            color: #2c3e50;
            font-weight: bold;
        }}
        @media print {{
            body {{
                background-color: white;
            }}
            .container {{
                max-width: 100%;
                box-shadow: none;
                padding: 20px;
            }}
            .chapter {{
                page-break-before: always;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title-page">
            <h1>{metadata["title"]}</h1>
            <h2>{metadata["subtitle"]}</h2>
            <div class="metadata">
                <p>{metadata["author"]}</p>
                <p>{metadata["date"]}</p>
                <p>Version {metadata["version"]}</p>
            </div>
        </div>
        
        <section class="toc-section">
            <h2>目次</h2>
            {toc_html}
        </section>
        
        {''.join(chapters_html)}
        
        <footer style="margin-top: 4em; padding-top: 2em; border-top: 1px solid #ddd; color: #666; text-align: center;">
            <p>Generated with Parasol V5 Book Generator</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html

if __name__ == '__main__':
    generate_good_design_book_part1()
    print("🎉 Good Design Book Part 1 generation completed successfully!")