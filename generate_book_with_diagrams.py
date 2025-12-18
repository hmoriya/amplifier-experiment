#!/usr/bin/env python3
"""
Generate Parasol V5 book with diagram references using the new diagram generation system
"""

import logging
import sys
from pathlib import Path
import re
from typing import List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_book_with_diagrams():
    """Generate the book with diagram references processed"""
    
    # Book paths (use absolute paths)
    script_dir = Path(__file__).parent
    book_dir = script_dir / '.claude/commands/parasol/docs/book'
    output_dir = script_dir / 'generated_books'
    output_dir.mkdir(exist_ok=True)
    
    logger.info(f"📚 Starting Parasol V5 book generation...")
    logger.info(f"Source: {book_dir}")
    logger.info(f"Output: {output_dir}")
    
    # Import diagram generator
    script_dir = Path(__file__).parent
    generator_path = script_dir / 'parasol_book_generator'
    logger.info(f"Script directory: {script_dir}")
    logger.info(f"Adding to path: {generator_path}")
    sys.path.insert(0, str(generator_path))
    
    try:
        import diagram_generator
        logger.info("✅ Diagram generator loaded successfully")
    except ImportError as e:
        logger.error(f"Failed to import diagram generator: {e}")
        logger.info(f"Current directory: {Path.cwd()}")
        logger.info(f"Generator path exists: {generator_path.exists()}")
        logger.info(f"Python path: {sys.path[:3]}")
        sys.exit(1)
    
    # Book metadata
    from datetime import datetime
    now = datetime.now()
    
    metadata = {
        'title': 'Parasol V5 完全ガイドブック',
        'subtitle': '価値駆動による実践的システム設計',
        'version': '2.0.0',
        'date': now.strftime('%Y年%m月%d日'),
        'author': 'Parasol Team',
        'language': 'ja',
        'diagram_version': '5.0',
        'diagram_type': 'Modular Configuration-Driven Engine',
        'build_time': now.strftime('%Y-%m-%d %H:%M JST')
    }
    
    # Chapter structure
    chapter_structure = [
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
    
    # Process chapters
    chapters = []
    chapter_num = 1
    
    logger.info("📖 Processing chapters...")
    
    for part_name, chapter_files in chapter_structure:
        part_dir = book_dir / part_name
        
        for chapter_file in chapter_files:
            file_path = part_dir / chapter_file
            
            if not file_path.exists():
                logger.warning(f"Chapter file not found: {file_path}")
                continue
            
            # Read content
            content = file_path.read_text(encoding='utf-8')
            
            # Remove frontmatter before extracting title
            content_without_frontmatter = content
            if content.startswith('---\n'):
                parts = content.split('---\n', 2)
                if len(parts) >= 3:
                    content_without_frontmatter = parts[2]
            
            # Extract title (first h1)
            title_match = re.search(r'^#\s+(.+)$', content_without_frontmatter, re.MULTILINE)
            title = title_match.group(1) if title_match else f"Chapter {chapter_num}"
            
            # Process diagram references
            processed_content = process_diagram_references(content)
            
            chapters.append({
                'number': chapter_num,
                'title': title,
                'file': chapter_file,
                'part': part_name,
                'content': processed_content
            })
            
            chapter_num += 1
            logger.info(f"Processed: {title}")
    
    logger.info(f"✅ Processed {len(chapters)} chapters")
    
    # Generate HTML
    generate_html(chapters, metadata, output_dir)
    
    # Try to generate PDF
    try:
        generate_pdf(output_dir)
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        logger.info("HTML generation completed successfully")

def process_diagram_references(content: str) -> str:
    """Replace diagram references with generated diagrams (respecting metadata settings)"""
    
    import diagram_generator
    generator = diagram_generator.DiagramGenerator()
    
    # Parse frontmatter metadata
    frontmatter = {}
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            metadata_text = parts[1]
            content = parts[2]  # Remove frontmatter from content
            
            # Parse YAML-like metadata (simple parsing)
            for line in metadata_text.split('\n'):
                if ':' in line and not line.strip().startswith('#'):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                    frontmatter[key] = value
    
    # Check diagram rendering preferences
    force_html_css = frontmatter.get('force_html_css', False)
    diagram_rendering = frontmatter.get('diagram_rendering', 'html_css')
    disable_mermaid = frontmatter.get('disable_mermaid', False)
    
    def replace_diagram_ref(match):
        full_match = match.group(0)
        ref_type = match.group(1)
        
        # Parse extended syntax {{diagram:name|param=value|param2=value2}}
        if '|' in full_match:
            parts = full_match.split('|')
            ref_base = parts[0]  # {{diagram:name
            ref_name = ref_base.split(':')[1].replace('}', '')
            
            # Parse parameters
            params = {}
            for part in parts[1:]:
                part = part.strip().replace('}', '')
                if '=' in part:
                    key, value = part.split('=', 1)
                    params[key.strip()] = value.strip()
        else:
            ref_name = match.group(2)
            params = {}
        
        # Override with inline parameters
        rendering_mode = params.get('rendering', diagram_rendering)
        
        if ref_type == 'diagram':
            try:
                # Force HTML/CSS if specified in metadata or inline
                if force_html_css or disable_mermaid or rendering_mode == 'html_css':
                    if ref_name == 'parasol_8_phases':
                        return diagram_generator.generate_parasol_phase_diagram()
                    
                    elif ref_name == 'six_axis_system':
                        return diagram_generator.generate_six_axis_system()
                
                    elif ref_name == 'value_traceability':
                        data = {
                            'components': [
                                {'name': 'Value Stream', 'layer': 'business', 'id': 'vs'},
                                {'name': 'Capability', 'layer': 'business', 'id': 'cap'},
                                {'name': 'Bounded Context', 'layer': 'domain', 'id': 'bc'},
                                {'name': 'Service', 'layer': 'application', 'id': 'service'},
                                {'name': 'API', 'layer': 'infrastructure', 'id': 'api'}
                            ],
                            'connections': [
                                {'from': 'vs', 'to': 'cap', 'label': 'traces to'},
                                {'from': 'cap', 'to': 'bc', 'label': 'implements'},
                                {'from': 'bc', 'to': 'service', 'label': 'realizes'},
                                {'from': 'service', 'to': 'api', 'label': 'exposes'}
                            ]
                        }
                        return generator.generate_diagram('architecture_overview', data)
                    
                    elif ref_name == 'capability_levels':
                        data = {
                            'capabilities': [
                                {'name': 'Business Value', 'level': 'CL1', 'id': 'bv', 'parent': None},
                                {'name': 'Core Capability', 'level': 'CL2', 'id': 'cc', 'parent': 'bv'},
                                {'name': 'Business Operation', 'level': 'CL3', 'id': 'bo', 'parent': 'cc'}
                            ]
                        }
                        return generator.generate_diagram('capability_map', data)
                    
                    else:
                        logger.warning(f"Unknown diagram reference: {ref_name}")
                        return f"<!-- Diagram placeholder: {ref_name} -->"
                
                # Fallback to Mermaid if HTML/CSS not forced (legacy behavior)
                else:
                    if ref_name == 'parasol_8_phases':
                        return diagram_generator.generate_parasol_phase_diagram()
                    
                    elif ref_name == 'six_axis_system':
                        return diagram_generator.generate_six_axis_system()
                    
                    elif ref_name == 'value_traceability':
                        data = {
                            'components': [
                                {'name': 'Value Stream', 'layer': 'business', 'id': 'vs'},
                                {'name': 'Capability', 'layer': 'business', 'id': 'cap'},
                                {'name': 'Bounded Context', 'layer': 'domain', 'id': 'bc'},
                                {'name': 'Service', 'layer': 'application', 'id': 'service'}
                            ],
                            'connections': [
                                {'from': 'vs', 'to': 'cap', 'label': 'traces to'},
                                {'from': 'cap', 'to': 'bc', 'label': 'implements'},
                                {'from': 'bc', 'to': 'service', 'label': 'realizes'}
                            ]
                        }
                        return generator.generate_diagram('architecture_overview', data)
                    
                    elif ref_name == 'capability_levels':
                        data = {
                            'capabilities': [
                                {'name': 'Business Value', 'level': 'CL1', 'id': 'bv', 'parent': None},
                                {'name': 'Core Capability', 'level': 'CL2', 'id': 'cc', 'parent': 'bv'},
                                {'name': 'Business Operation', 'level': 'CL3', 'id': 'bo', 'parent': 'cc'}
                            ]
                        }
                        return generator.generate_diagram('capability_map', data)
                    
                    else:
                        logger.warning(f"Unknown diagram reference: {ref_name}")
                        return f"<!-- Diagram placeholder: {ref_name} -->"
                    
            except Exception as e:
                logger.error(f"Failed to generate diagram {ref_name}: {e}")
                return f"<!-- Failed to generate diagram: {ref_name} -->"
        
        return match.group(0)
    
    # Find patterns like {{diagram:name}} or {{diagram:name|param=value}}
    pattern = r'\{\{(diagram):([a-zA-Z0-9_-]+)(?:\|[^}]+)?\}\}'
    result = re.sub(pattern, replace_diagram_ref, content)
    
    # Count diagrams generated
    original_diagrams = len(re.findall(pattern, content))
    generated_diagrams = result.count('parasol-flow-diagram')  # Count HTML/CSS diagrams instead
    
    if original_diagrams > 0:
        render_mode = "HTML/CSS" if (force_html_css or disable_mermaid or diagram_rendering == 'html_css') else "Mermaid"
        logger.info(f"  → Generated {generated_diagrams} {render_mode} diagrams from {original_diagrams} references")
    
    return result

def generate_html(chapters, metadata, output_dir):
    """Generate HTML book"""
    
    logger.info("🌐 Generating HTML...")
    
    # Generate table of contents
    toc_html = "<nav class='toc'><h2>目次</h2><ol>"
    for chapter in chapters:
        toc_html += f"<li><a href='#chapter-{chapter['number']}'>{chapter['title']}</a></li>"
    toc_html += "</ol></nav>"
    
    # Generate chapters HTML
    chapters_html = ""
    for chapter in chapters:
        chapter_html = f"""
<section id="chapter-{chapter['number']}" class="chapter">
    <div class="chapter-header">
        <h1>第{chapter['number']}章</h1>
    </div>
    {convert_markdown_to_html(chapter['content'])}
</section>
"""
        chapters_html += chapter_html
    
    # Complete HTML document
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']}</title>
    
    <!-- Mermaid.js for diagram rendering -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'cardinal'
            }},
            themeVariables: {{
                primaryColor: '#e1f5fe',
                primaryTextColor: '#000',
                primaryBorderColor: '#01579b',
                lineColor: '#666',
                sectionBkgColor: '#f5f5f5'
            }}
        }});
    </script>
    
    <style>
        body {{
            font-family: 'Hiragino Sans', 'Yu Gothic', 'Meiryo', sans-serif;
            line-height: 1.8;
            margin: 0;
            padding: 0;
            background: #fafafa;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .title-page {{
            text-align: center;
            padding: 60px 20px;
            border-bottom: 3px solid #01579b;
            margin-bottom: 40px;
        }}
        .title-page h1 {{
            font-size: 2.5em;
            color: #01579b;
            margin-bottom: 10px;
        }}
        .title-page .subtitle {{
            font-size: 1.3em;
            color: #666;
            margin-bottom: 30px;
        }}
        .toc {{
            margin: 40px 0;
            padding: 20px;
            background: #f8f9fa;
            border-left: 4px solid #01579b;
        }}
        .toc h2 {{
            color: #01579b;
            margin-top: 0;
        }}
        .toc ol {{
            padding-left: 20px;
        }}
        .toc a {{
            color: #333;
            text-decoration: none;
            padding: 5px 0;
            display: inline-block;
        }}
        .toc a:hover {{
            color: #01579b;
            text-decoration: underline;
        }}
        .chapter {{
            margin: 60px 0;
            page-break-before: always;
        }}
        .chapter-header {{
            border-bottom: 2px solid #01579b;
            margin-bottom: 30px;
            padding-bottom: 10px;
        }}
        .chapter-header h1 {{
            color: #01579b;
            margin: 0;
            font-size: 1.8em;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #333;
            margin-top: 2em;
            margin-bottom: 1em;
        }}
        h1 {{ font-size: 1.8em; border-bottom: 2px solid #01579b; padding-bottom: 0.5em; }}
        h2 {{ font-size: 1.5em; color: #01579b; }}
        h3 {{ font-size: 1.3em; }}
        h4 {{ font-size: 1.1em; }}
        
        p {{
            margin: 1em 0;
            text-align: justify;
        }}
        
        .diagram-container {{
            margin: 30px 0;
            text-align: center;
            background: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        
        .mermaid-diagram {{
            max-width: 100%;
            height: auto;
        }}
        
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }}
        
        pre {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #01579b;
            white-space: pre;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
            font-size: 0.9em;
            line-height: 1.4;
        }}
        
        pre code {{
            white-space: pre;
            font-family: inherit;
            font-size: inherit;
            line-height: inherit;
        }}
        
        blockquote {{
            border-left: 4px solid #01579b;
            margin: 20px 0;
            padding: 10px 20px;
            background: #f8f9fa;
            font-style: italic;
        }}
        
        ul, ol {{
            margin: 1em 0;
            padding-left: 2em;
        }}
        
        li {{
            margin: 0.5em 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        
        th {{
            background: #f8f9fa;
            font-weight: bold;
        }}
        
        strong {{
            color: #01579b;
            font-weight: bold;
        }}
        
        .footer {{
            margin-top: 60px;
            padding: 20px 0;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .hierarchy-diagram {{
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            overflow-x: auto;
        }}
        
        .hierarchy-diagram pre {{
            margin: 0;
            padding: 0;
            background: transparent;
            border: none;
            color: #333;
        }}
        
        .hierarchy-box {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
        }}
        
        .hierarchy-box .vms-title {{
            font-weight: bold;
            color: #01579b;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .hierarchy-box .objective {{
            margin-left: 20px;
            margin-top: 10px;
            padding: 10px;
            background: #e3f2fd;
            border-left: 3px solid #1976d2;
            border-radius: 4px;
        }}
        
        .hierarchy-box .key-result {{
            margin-left: 40px;
            margin-top: 5px;
            padding: 8px;
            background: #fff;
            border-left: 2px solid #64b5f6;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title-page">
            <h1>{metadata['title']}</h1>
            <div class="subtitle">{metadata['subtitle']}</div>
            <div class="meta">
                <p>Book Version {metadata['version']} | Diagrams v{metadata['diagram_version']}</p>
                <p>Generated: {metadata['build_time']}</p>
                <p>著者: {metadata['author']}</p>
            </div>
        </div>
        
        {toc_html}
        
        <main>
            {chapters_html}
        </main>
        
        <footer class="footer">
            <p>Generated with Parasol V5 Book Generator | {metadata['date']}</p>
        </footer>
    </div>
</body>
</html>"""
    
    # Write HTML file
    html_file = output_dir / 'parasol-v5-book.html'
    html_file.write_text(html_content, encoding='utf-8')
    
    logger.info(f"✅ HTML generated: {html_file}")
    logger.info(f"   File size: {html_file.stat().st_size:,} bytes")

def convert_markdown_to_html(content: str) -> str:
    """Simple markdown to HTML conversion"""
    
    # Convert code blocks first (preserve them)
    code_blocks = []
    def preserve_code_block(match):
        code_blocks.append(match.group(0))
        return f"___CODEBLOCK_{len(code_blocks)-1}___"
    
    content = re.sub(r'```.*?```', preserve_code_block, content, flags=re.DOTALL)
    
    # Detect and convert ASCII tables that are not in code blocks
    content = convert_ascii_tables_in_text(content)
    
    # Headers
    content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Inline code - preserve content and mark with placeholders
    code_segments = []
    def preserve_inline_code(match):
        code_segments.append(f'<code>{match.group(1)}</code>')
        return f'___INLINECODE_{len(code_segments)-1}___'
    
    content = re.sub(r'`([^`]+)`', preserve_inline_code, content)
    
    # Bold and italic (won't affect preserved code segments)
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', content)
    
    # Restore inline code segments
    for i, segment in enumerate(code_segments):
        content = content.replace(f'___INLINECODE_{i}___', segment)
    
    # Links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # Tables
    content = convert_tables(content)
    
    # Lists
    content = convert_lists(content)
    
    # Blockquotes - handle multi-line blockquotes
    content = convert_blockquotes(content)
    
    # Paragraphs
    content = add_paragraphs(content)
    
    # Restore code blocks
    for i, block in enumerate(code_blocks):
        if block.startswith('```mermaid'):
            # Mermaid diagram
            diagram_content = block[10:-3].strip()  # Remove ```mermaid and ```
            replacement = f'<div class="diagram-container"><div class="mermaid">{diagram_content}</div></div>'
        else:
            # Check if it's a table in a code block
            code_content_lines = block.strip('```').strip().split('\n')
            # Check for ASCII table patterns
            has_table_pattern = False
            for line in code_content_lines:
                # Look for separator lines with pipes and dashes
                if re.match(r'^[\s\-|]+$', line) and '|' in line and '-' in line:
                    has_table_pattern = True
                    break
                # Also check for box-drawing characters
                if any(char in line for char in ['│', '─', '┌', '└', '├', '┤', '┬', '┴', '┼']):
                    has_table_pattern = True
                    break
            
            if has_table_pattern:
                # This looks like an ASCII table, convert it to HTML
                replacement = convert_ascii_table_to_html(block)
            else:
                # Check if it's a tree/hierarchy structure
                if is_hierarchy_structure(block):
                    # Keep as preformatted text with proper styling
                    content_lines = block.strip('```').strip().split('\n')
                    if content_lines and content_lines[0] and not any(char in content_lines[0] for char in ['│', '├', '└', '─']):
                        content_lines = content_lines[1:]
                    content = '\n'.join(content_lines)
                    # Escape HTML entities
                    content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    replacement = f'<div class="hierarchy-diagram"><pre style="font-family: monospace; line-height: 1.4;">{content}</pre></div>'
                # Check if it's a graph/chart in ASCII art
                elif is_ascii_graph(block):
                    # Convert ASCII graph to SVG
                    replacement = convert_ascii_graph_to_svg(block)
                else:
                    # Regular code block
                    language_match = re.match(r'```(\w*)', block)
                    if language_match:
                        language = language_match.group(1) if language_match.group(1) else ''
                        # Remove the backticks and language identifier
                        lines = block.split('\n')
                        if lines[0].startswith('```'):
                            lines = lines[1:]
                        if lines and lines[-1].strip() == '```':
                            lines = lines[:-1]
                        code_content = '\n'.join(lines)
                    else:
                        language = ''
                        code_content = block
                    
                    # Preserve whitespace and formatting in code blocks
                    # First escape HTML entities
                    code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    
                    # For tree structures, ensure spacing is preserved
                    if '├──' in code_content or '└──' in code_content or '│' in code_content:
                        # Wrap in pre to strictly preserve formatting
                        replacement = f'<pre style="white-space: pre; font-family: monospace;"><code class="language-{language}">{code_content}</code></pre>'
                    else:
                        replacement = f'<pre><code class="language-{language}">{code_content}</code></pre>'
        content = content.replace(f'___CODEBLOCK_{i}___', replacement)
    
    return content

def is_hierarchy_structure(block: str) -> bool:
    """Detect if a code block is a hierarchy/tree structure"""
    content = block.strip()
    if content.startswith('```'):
        lines = content.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        content = '\n'.join(lines)
    
    # Look for tree/hierarchy patterns
    tree_patterns = [
        '│',  # Vertical line
        '├─', # Branch
        '└─', # Last branch
        '├──', # Extended branch
        '└──', # Extended last branch
        '    ├─', # Indented branch
        '    └─', # Indented last branch
        'VMS', # Specific content patterns
        'OKR',
        'Objective',
        'Key Results'
    ]
    
    # Check if multiple tree patterns exist
    pattern_count = sum(1 for pattern in tree_patterns if pattern in content)
    return pattern_count >= 3

def is_ascii_graph(block: str) -> bool:
    """Detect if a code block is an ASCII graph/chart"""
    content = block.strip()
    if content.startswith('```'):
        lines = content.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        content = '\n'.join(lines)
    
    # Look for graph patterns
    graph_patterns = [
        '↑',  # Y-axis arrow
        '→',  # X-axis arrow
        '╱',  # Diagonal lines
        '╲',  # Diagonal lines
        '═',  # Horizontal lines
        '│',  # Vertical axis
        '└─', # Axis corner
        'リリース時の価値',  # Specific graph labels
        '継続的改善'
    ]
    
    # Check if multiple graph patterns exist
    pattern_count = sum(1 for pattern in graph_patterns if pattern in content)
    return pattern_count >= 3

def convert_ascii_graph_to_svg(block: str) -> str:
    """Convert ASCII graph to SVG visualization"""
    # Extract content from code block
    content = block.strip()
    if content.startswith('```'):
        lines = content.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        content = '\n'.join(lines)
    
    # Check if it's the value decay curve
    if 'リリース時の価値' in content:
        # Value decay curve
        svg = '''
<div class="diagram-container" style="margin: 30px 0; text-align: center;">
    <svg width="500" height="300" viewBox="0 0 500 300" style="border: 1px solid #ddd; background: #fff;">
        <!-- Title -->
        <text x="250" y="20" text-anchor="middle" font-size="16" font-weight="bold">価値の減衰曲線</text>
        
        <!-- Axes -->
        <line x1="50" y1="250" x2="450" y2="250" stroke="#333" stroke-width="2" />
        <line x1="50" y1="250" x2="50" y2="50" stroke="#333" stroke-width="2" />
        
        <!-- Arrow heads -->
        <polygon points="450,250 440,245 440,255" fill="#333" />
        <polygon points="50,50 45,60 55,60" fill="#333" />
        
        <!-- Axis labels -->
        <text x="250" y="280" text-anchor="middle" font-size="14">時間</text>
        <text x="20" y="150" text-anchor="middle" font-size="14" transform="rotate(-90, 20, 150)">価値</text>
        
        <!-- Decay curve (no maintenance) -->
        <path d="M 50,100 Q 150,100 200,150 T 350,230" 
              stroke="#dc3545" stroke-width="2" fill="none" stroke-dasharray="5,5" />
        
        <!-- Maintained value line -->
        <line x1="50" y1="100" x2="350" y2="100" stroke="#28a745" stroke-width="3" />
        
        <!-- Labels -->
        <text x="100" y="90" font-size="12" fill="#333">リリース時の価値</text>
        <text x="300" y="90" font-size="12" fill="#28a745">継続的改善 →</text>
        <text x="280" y="210" font-size="12" fill="#dc3545">保守されないシステム</text>
        
        <!-- Legend -->
        <line x1="320" y1="140" x2="350" y2="140" stroke="#28a745" stroke-width="3" />
        <text x="355" y="145" font-size="11">価値を保つ</text>
        
        <line x1="320" y1="160" x2="350" y2="160" stroke="#dc3545" stroke-width="2" stroke-dasharray="5,5" />
        <text x="355" y="165" font-size="11">価値が減衰</text>
    </svg>
</div>
        '''
        return svg
    
    # For other ASCII graphs, show as code
    return f'<pre><code>{content}</code></pre>'

def convert_ascii_table_to_html(block: str) -> str:
    """Convert ASCII art table to HTML table"""
    # Remove code block markers if present
    content = block
    if content.startswith('```'):
        lines = content.split('\n')
        # Remove first line (``` or ```language)
        if lines[0].startswith('```'):
            lines = lines[1:]
        # Remove last line if it's ```
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        content = '\n'.join(lines)
    
    lines = content.strip().split('\n')
    
    # Detect if this is an ASCII table
    is_ascii_table = False
    
    # Check for various table patterns
    for i, line in enumerate(lines):
        # Look for lines like ---|---|--- or similar
        if re.match(r'^[\s\-|]+$', line) and '|' in line and '-' in line:
            is_ascii_table = True
            break
        # Check for box-drawing characters
        if any(char in line for char in ['│', '─', '┌', '└', '├', '┤', '┬', '┴', '┼']):
            is_ascii_table = True
            break
    
    if not is_ascii_table:
        # Not a table, return as code block
        return f'<pre><code>{block}</code></pre>'
    
    # Extract table rows
    rows = []
    for i, line in enumerate(lines):
        # Skip separator lines
        if re.match(r'^[\s\-|]+$', line) and '-' in line:
            continue
        # Skip box-drawing lines
        if line.strip().startswith(('┌', '└', '├', '┤')) or re.match(r'^[─│┬┴┼\s]+$', line):
            continue
            
        # Process data lines with pipes or box-drawing vertical bars
        if '|' in line or '│' in line:
            # Split by pipe or box-drawing vertical bar
            if '│' in line:
                cells = [cell.strip() for cell in line.split('│')]
            else:
                cells = [cell.strip() for cell in line.split('|')]
            # Remove empty first/last cells
            if cells and cells[0] == '':
                cells = cells[1:]
            if cells and cells[-1] == '':
                cells = cells[:-1]
            
            if cells:
                rows.append(cells)
    
    if not rows:
        return f'<pre><code>{block}</code></pre>'
    
    # Build HTML table
    html = ['<table>']
    
    # First row is header
    html.append('<thead>')
    html.append('<tr>')
    for cell in rows[0]:
        html.append(f'<th>{cell}</th>')
    html.append('</tr>')
    html.append('</thead>')
    
    # Rest are body rows
    if len(rows) > 1:
        html.append('<tbody>')
        for row in rows[1:]:
            html.append('<tr>')
            for cell in row:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')
    
    html.append('</table>')
    
    return '\n'.join(html)

def convert_ascii_tables_in_text(content: str) -> str:
    """Convert ASCII tables that appear in regular text (not in code blocks)"""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        # Check for ASCII table with separator line (e.g., ---|---|---)
        if (i + 1 < len(lines) and 
            '|' in lines[i] and 
            '|' in lines[i + 1] and 
            re.match(r'^[\s\-|]+$', lines[i + 1])):
            
            # Found a potential ASCII table
            table_lines = [lines[i]]
            i += 1
            
            # Collect separator line
            table_lines.append(lines[i])
            i += 1
            
            # Collect data rows
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            
            # Convert to HTML table
            html_table = convert_ascii_table_lines_to_html(table_lines)
            result.append(html_table)
        else:
            result.append(lines[i])
            i += 1
    
    return '\n'.join(result)

def convert_ascii_table_lines_to_html(lines: List[str]) -> str:
    """Convert ASCII table lines to HTML table"""
    if len(lines) < 2:
        return '\n'.join(lines)
    
    # Extract cells from each line
    rows = []
    for idx, line in enumerate(lines):
        if idx == 1 and re.match(r'^[\s\-|]+$', line):
            # Skip separator line
            continue
        
        # Extract cells
        cells = [cell.strip() for cell in line.split('|')]
        # Remove empty first/last cells from | at line start/end
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
        
        if cells:
            rows.append(cells)
    
    if not rows:
        return '\n'.join(lines)
    
    # Build HTML table
    html = ['<table>']
    
    # First row is header
    html.append('<thead>')
    html.append('<tr>')
    for cell in rows[0]:
        html.append(f'<th>{cell}</th>')
    html.append('</tr>')
    html.append('</thead>')
    
    # Rest are body rows
    if len(rows) > 1:
        html.append('<tbody>')
        for row in rows[1:]:
            html.append('<tr>')
            for cell in row:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')
    
    html.append('</table>')
    
    return '\n'.join(html)

def convert_tables(content: str) -> str:
    """Convert markdown tables to HTML"""
    # This function is now primarily for standard Markdown tables
    # ASCII tables are handled by convert_ascii_tables_in_text
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        # Standard Markdown table detection (already handled by convert_ascii_tables_in_text)
        # Skip if already converted
        if '<table>' in lines[i]:
            result.append(lines[i])
            i += 1
        else:
            result.append(lines[i])
            i += 1
    
    return '\n'.join(result)

def convert_blockquotes(content: str) -> str:
    """Convert markdown blockquotes to HTML, handling multi-line quotes"""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        if lines[i].strip().startswith('>'):
            # Start of blockquote
            quote_lines = []
            
            # Process continuous blockquote lines
            while i < len(lines) and (lines[i].strip().startswith('>') or 
                                     (lines[i].strip() == '' and i + 1 < len(lines) and 
                                      lines[i + 1].strip().startswith('>'))):
                if lines[i].strip().startswith('>'):
                    # Remove the '>' and any following space
                    line = lines[i]
                    # Find the position of '>' and preserve indentation before it
                    quote_pos = line.find('>')
                    if quote_pos >= 0:
                        line_content = line[quote_pos + 1:].lstrip()
                        quote_lines.append(line_content)
                else:
                    # Empty line within blockquote
                    quote_lines.append('')
                i += 1
            
            # Process the blockquote content to handle nested structures
            quote_html = process_blockquote_content(quote_lines)
            result.append(f'<blockquote>{quote_html}</blockquote>')
        else:
            result.append(lines[i])
            i += 1
    
    return '\n'.join(result)

def process_blockquote_content(lines):
    """Process blockquote content to handle lists and other structures"""
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for hierarchy structure (VMS-OKR format)
        if is_hierarchy_blockquote(lines, i):
            # Process hierarchy structure
            hierarchy_html = process_hierarchy_blockquote(lines, i)
            result.append(hierarchy_html['html'])
            i = hierarchy_html['next_index']
        
        # Check for Markdown table
        elif i + 1 < len(lines) and '|' in line and '|' in lines[i + 1] and re.match(r'^[\s\-|]+$', lines[i + 1]):
            # Found a table, collect all table lines
            table_lines = [line]
            i += 1
            # Add separator line
            table_lines.append(lines[i])
            i += 1
            # Collect data rows
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            # Convert table to HTML
            table_html = convert_markdown_table_to_html(table_lines)
            result.append(table_html)
        
        # Check for list items with dash
        elif line.strip().startswith('- '):
            # Start of list
            list_items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                item = lines[i].strip()[2:].strip()
                list_items.append(f'<li>{item}</li>')
                i += 1
            if list_items:
                result.append('<ul>' + ''.join(list_items) + '</ul>')
        
        # Check for indented content (code or special formatting)
        elif line.startswith('  ') and line.strip():
            # Collect indented lines
            code_lines = []
            while i < len(lines) and (lines[i].startswith('  ') or not lines[i].strip()):
                if lines[i].strip():
                    code_lines.append(lines[i][2:])  # Remove 2 spaces of indentation
                else:
                    code_lines.append('')
                i += 1
            if code_lines:
                # Check if it's a table-like structure
                if any('|' in line for line in code_lines):
                    # Try to process as a table
                    table_html = try_convert_indented_table(code_lines)
                    if table_html:
                        result.append(table_html)
                    else:
                        result.append('<pre>' + '\n'.join(code_lines) + '</pre>')
                else:
                    result.append('<pre>' + '\n'.join(code_lines) + '</pre>')
        else:
            # Regular line
            if line.strip():
                result.append(line)
            else:
                result.append('<br>')
            i += 1
    
    return ''.join(result)

def convert_markdown_table_to_html(lines):
    """Convert markdown table lines to HTML"""
    if len(lines) < 2:
        return '\n'.join(lines)
    
    # Extract cells from each line
    rows = []
    for idx, line in enumerate(lines):
        if idx == 1 and re.match(r'^[\s\-|]+$', line):
            # Skip separator line
            continue
        
        # Extract cells
        cells = [cell.strip() for cell in line.split('|')]
        # Remove empty first/last cells from | at line start/end
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
        
        if cells:
            rows.append(cells)
    
    if not rows:
        return '\n'.join(lines)
    
    # Build HTML table
    html = ['<table>']
    
    # First row is header
    html.append('<thead>')
    html.append('<tr>')
    for cell in rows[0]:
        html.append(f'<th>{cell}</th>')
    html.append('</tr>')
    html.append('</thead>')
    
    # Rest are body rows
    if len(rows) > 1:
        html.append('<tbody>')
        for row in rows[1:]:
            html.append('<tr>')
            for cell in row:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')
    
    html.append('</table>')
    
    return '\n'.join(html)

def try_convert_indented_table(lines):
    """Try to convert indented lines to a table if they look like a table"""
    # Check if lines contain table-like structure
    has_separator = any(re.match(r'^[\s\-|]+$', line) and '|' in line for line in lines)
    
    if not has_separator:
        return None
    
    # Find separator line
    separator_idx = -1
    for idx, line in enumerate(lines):
        if re.match(r'^[\s\-|]+$', line) and '|' in line:
            separator_idx = idx
            break
    
    if separator_idx <= 0:
        return None
    
    # Process as table
    return convert_markdown_table_to_html(lines)

def convert_lists(content: str) -> str:
    """Convert markdown lists to HTML"""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        if lines[i].strip().startswith(('- ', '* ', '+ ')):
            # Start of unordered list
            list_html = ['<ul>']
            while i < len(lines) and lines[i].strip().startswith(('- ', '* ', '+ ')):
                item_content = re.sub(r'^[\-\*\+]\s+', '', lines[i].strip())
                list_html.append(f'<li>{item_content}</li>')
                i += 1
            list_html.append('</ul>')
            result.append('\n'.join(list_html))
        elif re.match(r'^\d+\.\s', lines[i].strip()):
            # Start of ordered list
            list_html = ['<ol>']
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                # Extract the actual number from the source
                match = re.match(r'^(\d+)\.\s', lines[i].strip())
                number = int(match.group(1))
                item_content = re.sub(r'^\d+\.\s+', '', lines[i].strip())
                list_html.append(f'<li value="{number}">{item_content}</li>')
                i += 1
            list_html.append('</ol>')
            result.append('\n'.join(list_html))
        else:
            result.append(lines[i])
            i += 1
    
    return '\n'.join(result)

def is_hierarchy_blockquote(lines, start_index):
    """Check if the blockquote contains a hierarchy structure"""
    if start_index >= len(lines):
        return False
    
    # Look for VMS-OKR patterns
    hierarchy_keywords = ['VMS', 'Objective', 'KR', '├─', '└─', '│']
    
    # Check the next few lines for hierarchy patterns
    for i in range(start_index, min(start_index + 5, len(lines))):
        if any(keyword in lines[i] for keyword in hierarchy_keywords):
            return True
    
    return False

def process_hierarchy_blockquote(lines, start_index):
    """Process hierarchy structure in blockquote with box-style display"""
    hierarchy_lines = []
    i = start_index
    
    # Collect all hierarchy lines
    while i < len(lines):
        line = lines[i]
        # Check if line is part of hierarchy (contains tree symbols or is indented continuation)
        if any(symbol in line for symbol in ['VMS', '├─', '└─', '│', 'Objective', 'KR']) or (line.strip() and hierarchy_lines):
            hierarchy_lines.append(line)
            i += 1
        elif not line.strip() and hierarchy_lines:
            # Empty line might be part of hierarchy, check next line
            if i + 1 < len(lines) and any(symbol in lines[i + 1] for symbol in ['├─', '└─', '│', 'KR']):
                hierarchy_lines.append(line)
                i += 1
            else:
                break
        else:
            break
    
    # Build hierarchy HTML
    html = ['<div class="hierarchy-box" style="']
    html.append('background: #f8f9fa;')
    html.append('border: 1px solid #dee2e6;')
    html.append('border-radius: 8px;')
    html.append('padding: 20px;')
    html.append('margin: 20px 0;')
    html.append('font-family: monospace;')
    html.append('">')
    
    # Process each line
    for line in hierarchy_lines:
        if 'VMS' in line and ':' in line:
            # Main VMS line
            parts = line.split(':', 1)
            vms_id = parts[0].strip()
            vms_desc = parts[1].strip() if len(parts) > 1 else ''
            html.append(f'<div style="font-weight: bold; color: #01579b; font-size: 1.1em; margin-bottom: 10px;">{vms_id}: {vms_desc}</div>')
        elif 'Objective:' in line:
            # Objective line
            obj_text = line.replace('└─', '').replace('├─', '').strip()
            html.append(f'<div style="margin-left: 20px; margin-top: 10px; padding: 10px; background: #e3f2fd; border-left: 3px solid #1976d2; border-radius: 4px;">{obj_text}</div>')
        elif 'KR' in line and ':' in line:
            # Key Result line
            kr_text = line.replace('├─', '').replace('└─', '').replace('│', '').strip()
            html.append(f'<div style="margin-left: 40px; margin-top: 5px; padding: 8px; background: #fff; border-left: 2px solid #64b5f6; border-radius: 4px;">{kr_text}</div>')
        elif line.strip():
            # Other content
            clean_line = line.replace('│', '').strip()
            if clean_line:
                indent_level = (len(line) - len(line.lstrip())) * 10
                html.append(f'<div style="margin-left: {indent_level}px; margin-top: 5px;">{clean_line}</div>')
    
    html.append('</div>')
    
    return {
        'html': ''.join(html),
        'next_index': i
    }

def add_paragraphs(content: str) -> str:
    """Add paragraph tags to plain text blocks"""
    paragraphs = content.split('\n\n')
    result = []
    
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<') and not re.match(r'^___\w+___', para):
            result.append(f'<p>{para}</p>')
        else:
            result.append(para)
    
    return '\n\n'.join(result)

def generate_pdf(output_dir):
    """Try to generate PDF from HTML"""
    
    logger.info("📄 Attempting PDF generation...")
    
    html_file = output_dir / 'parasol-v5-book.html'
    pdf_file = output_dir / 'parasol-v5-book.pdf'
    
    # Try different PDF generation methods
    methods = [
        ('weasyprint', f'weasyprint {html_file} {pdf_file}'),
        ('wkhtmltopdf', f'wkhtmltopdf {html_file} {pdf_file}'),
        ('pandoc', f'pandoc {html_file} -o {pdf_file} --pdf-engine=wkhtmltopdf')
    ]
    
    import subprocess
    import shutil
    
    for method_name, command in methods:
        if shutil.which(method_name.split()[0]):
            try:
                logger.info(f"Trying PDF generation with {method_name}...")
                result = subprocess.run(command.split(), capture_output=True, text=True)
                
                if result.returncode == 0 and pdf_file.exists():
                    logger.info(f"✅ PDF generated successfully with {method_name}: {pdf_file}")
                    logger.info(f"   File size: {pdf_file.stat().st_size:,} bytes")
                    return
                else:
                    logger.warning(f"PDF generation with {method_name} failed")
                    
            except Exception as e:
                logger.warning(f"PDF generation with {method_name} error: {e}")
    
    logger.warning("PDF generation failed - no suitable PDF generator found")
    logger.info("Install weasyprint, wkhtmltopdf, or pandoc for PDF generation")

if __name__ == '__main__':
    try:
        generate_book_with_diagrams()
        print("\n🎉 Book generation completed successfully!")
    except Exception as e:
        logger.error(f"Book generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)