#!/usr/bin/env python3
"""
Generate Parasol V5 book with diagram references using the new diagram generation system
"""

import logging
import sys
from pathlib import Path
import re

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
    metadata = {
        'title': 'Parasol V5 完全ガイドブック',
        'subtitle': '価値駆動による実践的システム設計',
        'version': '2.0.0',
        'date': '2025年12月18日',
        'author': 'Parasol Team',
        'language': 'ja',
        'diagram_version': '5.0',
        'diagram_type': 'Modular Configuration-Driven Engine',
        'build_time': '2025-12-18 11:20 JST'
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
    
    # Headers
    content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Bold and italic
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', content)
    
    # Links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # Tables
    content = convert_tables(content)
    
    # Lists
    content = convert_lists(content)
    
    # Blockquotes
    content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)
    
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
            if len(code_content_lines) > 1 and '│' in block and '─' in block and '┌' in block:
                # This looks like an ASCII table, convert it to HTML
                replacement = convert_ascii_table_to_html(block)
            else:
                # Regular code block
                language_match = re.match(r'```(\w+)', block)
                language = language_match.group(1) if language_match else ''
                code_content = block[3+len(language):-3].strip()
                replacement = f'<pre><code class="language-{language}">{code_content}</code></pre>'
        content = content.replace(f'___CODEBLOCK_{i}___', replacement)
    
    return content

def convert_ascii_table_to_html(block: str) -> str:
    """Convert ASCII art table to HTML table"""
    lines = block.strip('```').strip().split('\n')
    
    # Check for two types of ASCII tables
    if '│' in block:
        # Box-drawing style table
        content_lines = []
        for line in lines:
            if '│' in line and not line.strip().startswith('┌') and not line.strip().startswith('└') and not line.strip().startswith('├'):
                content_lines.append(line)
        
        if not content_lines:
            return f'<pre><code>{block}</code></pre>'
        
        # Extract cells from each content line
        rows = []
        for line in content_lines:
            # Split by │ and clean up
            cells = [cell.strip() for cell in line.split('│') if cell.strip()]
            if cells:
                rows.append(cells)
    
    elif '|' in block and '-' in block:
        # Markdown-style table with | and ---
        rows = []
        separator_found = False
        
        for line in lines:
            if '|' in line:
                # Check if this is a separator line
                if set(line.replace('|', '').replace(' ', '').replace('-', '')) == set():
                    separator_found = True
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
    
    else:
        return f'<pre><code>{block}</code></pre>'
    
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

def convert_tables(content: str) -> str:
    """Convert markdown tables to HTML"""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        # Check if this line looks like a table header
        if i + 1 < len(lines) and '|' in lines[i] and '|' in lines[i + 1] and re.match(r'^[\s\-:|]+$', lines[i + 1].replace('|', '')):
            # Found a table
            table_html = ['<table>']
            
            # Process header row
            header_cells = [cell.strip() for cell in lines[i].split('|') if cell.strip()]
            table_html.append('<thead>')
            table_html.append('<tr>')
            for cell in header_cells:
                table_html.append(f'<th>{cell}</th>')
            table_html.append('</tr>')
            table_html.append('</thead>')
            
            # Skip separator row
            i += 2
            
            # Process body rows
            table_html.append('<tbody>')
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                cells = [cell.strip() for cell in lines[i].split('|') if cell.strip()]
                if cells:  # Only add row if it has content
                    table_html.append('<tr>')
                    for cell in cells:
                        table_html.append(f'<td>{cell}</td>')
                    table_html.append('</tr>')
                i += 1
            table_html.append('</tbody>')
            table_html.append('</table>')
            
            result.append('\n'.join(table_html))
        else:
            result.append(lines[i])
            i += 1
    
    return '\n'.join(result)

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
                item_content = re.sub(r'^\d+\.\s+', '', lines[i].strip())
                list_html.append(f'<li>{item_content}</li>')
                i += 1
            list_html.append('</ol>')
            result.append('\n'.join(list_html))
        else:
            result.append(lines[i])
            i += 1
    
    return '\n'.join(result)

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