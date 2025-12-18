"""
Main generator class that orchestrates the book generation process
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from .converters import MarkdownConverter, HTMLBuilder, PDFBuilder
from .data_manager import DataManager
from .diagram_renderer import DiagramRenderer
from .diagram_generator import DiagramGenerator

logger = logging.getLogger(__name__)


class ParasolBookGenerator:
    """Main book generator for Parasol V5 documentation"""
    
    def __init__(self, book_dir: Path, output_dir: Path, data_dir: Optional[Path] = None):
        """
        Initialize the book generator
        
        Args:
            book_dir: Directory containing markdown chapter files
            output_dir: Directory for generated output
            data_dir: Directory containing YAML/JSON data files
        """
        self.book_dir = Path(book_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.markdown_converter = MarkdownConverter()
        self.html_builder = HTMLBuilder()
        self.data_manager = DataManager(data_dir) if data_dir else None
        self.diagram_renderer = DiagramRenderer(self.output_dir / 'diagrams')
        self.diagram_generator = DiagramGenerator()
        
        # Chapter structure
        self.chapter_structure = [
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
        
        # Metadata
        self.metadata = {
            'title': 'Parasol V5 完全ガイドブック',
            'subtitle': '価値駆動による実践的システム設計',
            'version': '1.0.0',
            'date': '2025年12月18日',
            'author': 'Parasol Team',
            'language': 'ja'
        }
    
    def generate(self, formats: List[str] = ['html', 'pdf']):
        """
        Generate the book in specified formats
        
        Args:
            formats: List of output formats to generate
        """
        logger.info(f"Starting book generation for formats: {formats}")
        
        # Process chapters
        chapters = self._process_chapters()
        
        if 'html' in formats:
            self._generate_html(chapters)
        
        if 'pdf' in formats:
            self._generate_pdf(chapters)
        
        # Generate metadata file
        self._generate_metadata()
        
        logger.info("Book generation completed")
    
    def _process_chapters(self) -> List[Dict[str, Any]]:
        """Process all chapters and return structured data"""
        chapters = []
        chapter_num = 1
        
        for part_name, chapter_files in self.chapter_structure:
            part_dir = self.book_dir / part_name
            
            for chapter_file in chapter_files:
                file_path = part_dir / chapter_file
                
                if not file_path.exists():
                    logger.warning(f"Chapter file not found: {file_path}")
                    continue
                
                # Read content
                content = file_path.read_text(encoding='utf-8')
                
                # Extract chapter info
                _, title = self.markdown_converter.extract_chapter_info(content)
                
                if not title:
                    logger.warning(f"No title found in {chapter_file}")
                    continue
                
                # Process content
                processed_content = self._process_chapter_content(content)
                
                chapters.append({
                    'number': chapter_num,
                    'title': title,
                    'file': chapter_file,
                    'part': part_name,
                    'content': content,
                    'content_processed': processed_content,
                    'content_html': self._convert_to_html(processed_content)
                })
                
                chapter_num += 1
                logger.info(f"Processed chapter {chapter_num - 1}: {title}")
        
        return chapters
    
    def _process_chapter_content(self, content: str) -> str:
        """Process chapter content with all enhancements"""
        # Process diagrams
        if self.diagram_renderer:
            content = self.diagram_renderer.process_markdown_diagrams(content)
        
        # Process data references (e.g., {{table:industry-dna}})
        if self.data_manager:
            content = self._process_data_references(content)
        
        return content
    
    def _process_data_references(self, content: str) -> str:
        """Replace data references with rendered content"""
        import re
        
        def replace_data_ref(match):
            ref_type = match.group(1)
            ref_name = match.group(2)
            
            if ref_type == 'table':
                try:
                    data = self.data_manager.load_data(f"{ref_name}.yaml")
                    return self.data_manager.render_table(data, format='markdown')
                except Exception as e:
                    logger.error(f"Failed to load table {ref_name}: {e}")
                    return match.group(0)
            
            elif ref_type == 'diagram':
                # Generate diagram on-demand
                return self._generate_diagram_reference(ref_name)
            
            return match.group(0)
        
        # Find patterns like {{table:name}}, {{data:name}}, or {{diagram:name}}
        pattern = r'\{\{(table|data|diagram):([a-zA-Z0-9_-]+)\}\}'
        return re.sub(pattern, replace_data_ref, content)
    
    def _generate_diagram_reference(self, diagram_name: str) -> str:
        """Generate diagram content from name reference"""
        
        # Standard Parasol diagrams
        if diagram_name == 'parasol_8_phases':
            from .diagram_generator import generate_parasol_phase_diagram
            return generate_parasol_phase_diagram()
        
        elif diagram_name == 'value_traceability':
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
            return self.diagram_generator.generate_diagram('architecture_overview', data)
        
        elif diagram_name == 'capability_levels':
            data = {
                'capabilities': [
                    {'name': 'Business Value', 'level': 'CL1', 'id': 'bv', 'parent': None},
                    {'name': 'Core Capability', 'level': 'CL2', 'id': 'cc', 'parent': 'bv'},
                    {'name': 'Business Operation', 'level': 'CL3', 'id': 'bo', 'parent': 'cc'}
                ]
            }
            return self.diagram_generator.generate_diagram('capability_map', data)
        
        else:
            # Try to load diagram specification from file
            try:
                if self.data_manager:
                    diagram_spec = self.data_manager.load_data(f"diagrams/{diagram_name}.yaml")
                    diagram_type = diagram_spec.get('type', 'process_flow')
                    return self.diagram_generator.generate_diagram(diagram_type, diagram_spec)
            except Exception as e:
                logger.warning(f"Failed to load diagram spec {diagram_name}: {e}")
            
            # Return placeholder
            return f"<!-- Diagram placeholder: {diagram_name} -->"
    
    def _convert_to_html(self, content: str) -> str:
        """Convert processed markdown to HTML"""
        # Process code blocks
        content, code_blocks = self.markdown_converter.process_code_blocks(content)
        
        # Convert basic markdown elements
        import re
        
        # Headings
        content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        
        # Bold and italic
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', content)
        
        # Links
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
        
        # Lists
        content = self._convert_lists(content)
        
        # Tables
        content = self._convert_tables_placeholder(content)
        
        # Paragraphs
        content = self._add_paragraphs(content)
        
        # Restore code blocks
        for i, block in enumerate(code_blocks):
            language_class = f' class="language-{block["language"]}"' if block['language'] else ''
            replacement = f'<pre><code{language_class}>{block["code"]}</code></pre>'
            content = content.replace(f'___CODEBLOCK_{i}___', replacement)
        
        return content
    
    def _convert_lists(self, content: str) -> str:
        """Convert markdown lists to HTML"""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            if lines[i].strip().startswith(('- ', '* ', '+ ')):
                # Start of a list
                list_html = ['<ul>']
                while i < len(lines) and lines[i].strip().startswith(('- ', '* ', '+ ')):
                    item_content = re.sub(r'^[\-\*\+]\s+', '', lines[i].strip())
                    list_html.append(f'<li>{item_content}</li>')
                    i += 1
                list_html.append('</ul>')
                result.append('\n'.join(list_html))
            else:
                result.append(lines[i])
                i += 1
        
        return '\n'.join(result)
    
    def _convert_tables_placeholder(self, content: str) -> str:
        """Convert table placeholders to HTML"""
        import re
        
        def convert_table_block(match):
            table_content = match.group(1)
            lines = table_content.strip().split('\n')
            
            if not lines:
                return ''
            
            # Parse markdown table
            rows = []
            for line in lines:
                if not re.match(r'^[\s\-:|]+$', line.replace('|', '')):
                    cells = [cell.strip() for cell in line.split('|')]
                    # Remove empty cells at start/end
                    if cells and cells[0] == '':
                        cells = cells[1:]
                    if cells and cells[-1] == '':
                        cells = cells[:-1]
                    if cells:
                        rows.append(cells)
            
            if not rows:
                return match.group(0)
            
            # Build HTML table
            html = ['<table>']
            
            # First row as header
            html.append('<thead><tr>')
            for cell in rows[0]:
                html.append(f'<th>{cell}</th>')
            html.append('</tr></thead>')
            
            # Rest as body
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
        
        # Convert table placeholders
        pattern = r'___TABLE_START___\n(.*?)\n___TABLE_END___'
        return re.sub(pattern, convert_table_block, content, flags=re.DOTALL)
    
    def _add_paragraphs(self, content: str) -> str:
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
    
    def _generate_html(self, chapters: List[Dict[str, Any]]):
        """Generate HTML output"""
        logger.info("Generating HTML output")
        
        html_content = self.html_builder.build_html(chapters, self.metadata)
        
        output_file = self.output_dir / 'parasol-v5-book.html'
        output_file.write_text(html_content, encoding='utf-8')
        
        logger.info(f"HTML output saved to: {output_file}")
    
    def _generate_pdf(self, chapters: List[Dict[str, Any]]):
        """Generate PDF output"""
        logger.info("Generating PDF output")
        
        # First generate HTML if not exists
        html_file = self.output_dir / 'parasol-v5-book.html'
        if not html_file.exists():
            self._generate_html(chapters)
        
        # Try different PDF backends
        pdf_file = self.output_dir / 'parasol-v5-book.pdf'
        
        for backend in ['weasyprint', 'pandoc', 'wkhtmltopdf']:
            logger.info(f"Trying PDF generation with {backend}")
            pdf_builder = PDFBuilder(backend=backend)
            
            if pdf_builder.html_to_pdf(html_file, pdf_file):
                logger.info(f"PDF generated successfully with {backend}: {pdf_file}")
                return
        
        logger.error("Failed to generate PDF with all available backends")
    
    def _generate_metadata(self):
        """Generate metadata file"""
        metadata_file = self.output_dir / 'book-metadata.json'
        
        metadata = {
            **self.metadata,
            'chapters': len([ch for part, chapters in self.chapter_structure for ch in chapters]),
            'parts': len(self.chapter_structure),
            'generated_formats': list(self.output_dir.glob('parasol-v5-book.*'))
        }
        
        # Convert Path objects to strings
        metadata['generated_formats'] = [str(p.name) for p in metadata['generated_formats']]
        
        metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
        logger.info(f"Metadata saved to: {metadata_file}")