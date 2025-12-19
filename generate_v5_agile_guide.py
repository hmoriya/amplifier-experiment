#!/usr/bin/env python3
"""
Generate V5 Agile Guide HTML book with diagram support
"""

import logging
import sys
from pathlib import Path
import re
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_chapters_from_single_file(input_file: Path) -> List[Dict[str, Any]]:
    """Process chapters from a single markdown file"""
    chapters = []
    content = input_file.read_text(encoding='utf-8')
    
    # Split by # 第X章 pattern
    chapter_pattern = r'^# 第(\d+)章[　\s]+(.+?)$'
    lines = content.split('\n')
    
    current_chapter = None
    current_content = []
    
    for line in lines:
        match = re.match(chapter_pattern, line)
        if match:
            # Save previous chapter if exists
            if current_chapter:
                chapters.append({
                    'number': current_chapter['number'],
                    'title': current_chapter['title'],
                    'content': '\n'.join(current_content)
                })
            
            # Start new chapter
            chapter_num = match.group(1)
            chapter_title = match.group(2).strip()
            current_chapter = {
                'number': f"第{chapter_num}章",
                'title': chapter_title
            }
            current_content = [line]
        elif current_chapter:
            current_content.append(line)
    
    # Don't forget the last chapter
    if current_chapter:
        chapters.append({
            'number': current_chapter['number'],
            'title': current_chapter['title'],
            'content': '\n'.join(current_content)
        })
    
    return chapters

def escape_html_in_text(text: str) -> str:
    """Escape HTML entities in regular text"""
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;'))

def process_markdown_to_html(content: str) -> str:
    """Convert markdown to HTML with proper formatting"""
    html_parts = []
    lines = content.split('\n')
    in_code_block = False
    in_practice_example = False
    code_lang = ''
    current_block = []
    
    for i, line in enumerate(lines):
        # Check for practice example start
        if line.strip().startswith('```') and i + 1 < len(lines) and lines[i + 1].startswith('実践例：'):
            in_practice_example = True
            in_code_block = True
            code_lang = line[3:].strip() or 'text'
            current_block = []
            continue
            
        # Check for regular code block start/end
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block
                if current_block:
                    content = '\n'.join(current_block)
                    if in_practice_example:
                        # Don't escape HTML in practice examples
                        html_parts.append(f'<pre><code class="language-{code_lang}">{content}</code></pre>')
                    else:
                        # Escape HTML in regular code blocks
                        html_parts.append(f'<pre><code class="language-{code_lang}">{escape_html_in_text(content)}</code></pre>')
                in_code_block = False
                in_practice_example = False
                code_lang = ''
                current_block = []
            else:
                # Start of code block
                in_code_block = True
                code_lang = line[3:].strip() or 'text'
                current_block = []
            continue
        
        if in_code_block:
            current_block.append(line)
            continue
        
        # Process regular markdown
        # Headers
        if line.startswith('### '):
            html_parts.append(f'<h3>{escape_html_in_text(line[4:])}</h3>')
        elif line.startswith('## '):
            html_parts.append(f'<h2>{escape_html_in_text(line[3:])}</h2>')
        elif line.startswith('# '):
            html_parts.append(f'<h1>{escape_html_in_text(line[2:])}</h1>')
        # Lists
        elif line.strip().startswith('- '):
            html_parts.append(f'<li>{escape_html_in_text(line.strip()[2:])}</li>')
        # Blockquotes
        elif line.strip().startswith('> '):
            html_parts.append(f'<blockquote>{escape_html_in_text(line.strip()[2:])}</blockquote>')
        # Paragraphs
        elif line.strip():
            # Handle bold text
            text = line
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            # Don't escape the HTML we just added for formatting
            text = text.replace('<strong>', '__STRONG_START__').replace('</strong>', '__STRONG_END__')
            text = escape_html_in_text(text)
            text = text.replace('__STRONG_START__', '<strong>').replace('__STRONG_END__', '</strong>')
            html_parts.append(f'<p>{text}</p>')
        else:
            html_parts.append('')
    
    return '\n'.join(html_parts)

def generate_html(chapters: List[Dict[str, Any]], title: str, subtitle: str) -> str:
    """Generate complete HTML document"""
    
    now = datetime.now()
    
    html_template = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #fafafa;
        }}
        .book-header {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 40px;
        }}
        .book-title {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .book-subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
        }}
        .chapter {{
            background: white;
            padding: 40px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            font-size: 2em;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            font-size: 1.5em;
            color: #555;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-left: 10px;
            border-left: 4px solid #667eea;
        }}
        h3 {{
            font-size: 1.2em;
            color: #666;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        p {{
            margin-bottom: 20px;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
        }}
        pre {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        code {{
            font-family: "Consolas", "Monaco", "Courier New", monospace;
            font-size: 0.9em;
        }}
        li {{
            margin-bottom: 10px;
        }}
        strong {{
            color: #667eea;
            font-weight: bold;
        }}
        .toc {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .toc h2 {{
            margin-top: 0;
        }}
        .toc-item {{
            margin-bottom: 10px;
            padding-left: 20px;
        }}
        .toc-link {{
            color: #667eea;
            text-decoration: none;
        }}
        .toc-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            padding: 40px;
            color: #888;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="book-header">
        <div class="book-title">{title}</div>
        <div class="book-subtitle">{subtitle}</div>
    </div>
    
    <div class="toc">
        <h2>目次</h2>
'''
    
    # Add table of contents
    for i, chapter in enumerate(chapters):
        html_template += f'        <div class="toc-item"><a href="#chapter{i+1}" class="toc-link">{chapter["number"]} {chapter["title"]}</a></div>\n'
    
    html_template += '''    </div>
    
'''
    
    # Add chapters
    for i, chapter in enumerate(chapters):
        logger.info(f"Processing: {chapter['number']} {chapter['title']}")
        html_content = process_markdown_to_html(chapter['content'])
        
        html_template += f'''    <div class="chapter" id="chapter{i+1}">
{html_content}
    </div>
    
'''
    
    html_template += f'''    <div class="footer">
        <p>Generated on {now.strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>{title} - {subtitle}</p>
    </div>
</body>
</html>'''
    
    return html_template

def main():
    # Configuration
    input_file = Path('.claude/commands/parasol/docs/v5-agile-guide-revised/part1-complete.md')
    output_file = Path('.claude/commands/parasol/docs/v5-agile-guide-revised/part1-agile-value-guide.html')
    title = "アジャイル原点回帰ガイド with Parasol V5"
    subtitle = "第1部：アジャイルの理想と現実"
    
    logger.info(f"📚 Starting V5 Agile Guide generation...")
    logger.info(f"Input: {input_file}")
    logger.info(f"Output: {output_file}")
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Process chapters
    chapters = process_chapters_from_single_file(input_file)
    logger.info(f"✅ Processed {len(chapters)} chapters")
    
    # Generate HTML
    logger.info("🌐 Generating HTML...")
    html_content = generate_html(chapters, title, subtitle)
    
    # Write output
    output_file.write_text(html_content, encoding='utf-8')
    logger.info(f"✅ HTML generated: {output_file}")
    logger.info(f"   File size: {output_file.stat().st_size:,} bytes")
    
    print("🎉 Book generation completed successfully!")

if __name__ == "__main__":
    main()