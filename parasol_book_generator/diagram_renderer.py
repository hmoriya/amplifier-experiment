"""
Diagram rendering for Mermaid and other diagram formats
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DiagramRenderer:
    """Render Mermaid and other diagrams to various formats"""
    
    def __init__(self, output_dir: Path):
        """
        Initialize diagram renderer
        
        Args:
            output_dir: Directory for generated diagram files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Check for required tools
        self.mermaid_cli = self._check_mermaid_cli()
        self.plantuml = self._check_plantuml()
    
    def _check_mermaid_cli(self) -> Optional[str]:
        """Check if mermaid-cli (mmdc) is available"""
        if shutil.which('mmdc'):
            return 'mmdc'
        elif shutil.which('npx'):
            # Try using npx to run mermaid-cli
            try:
                subprocess.run(['npx', '-y', '@mermaid-js/mermaid-cli', '--version'], 
                             capture_output=True, check=True)
                return 'npx -y @mermaid-js/mermaid-cli'
            except:
                pass
        logger.warning("Mermaid CLI not found. Diagram rendering will be limited.")
        return None
    
    def _check_plantuml(self) -> Optional[str]:
        """Check if PlantUML is available"""
        if shutil.which('plantuml'):
            return 'plantuml'
        logger.warning("PlantUML not found. UML diagram rendering will be limited.")
        return None
    
    def render_mermaid(self, mermaid_code: str, name: str, 
                      format: str = 'svg', theme: str = 'default') -> Optional[Path]:
        """
        Render Mermaid diagram to file
        
        Args:
            mermaid_code: Mermaid diagram code
            name: Output filename (without extension)
            format: Output format (svg, png, pdf)
            theme: Mermaid theme
        
        Returns:
            Path to generated file or None if failed
        """
        if not self.mermaid_cli:
            logger.error("Mermaid CLI not available")
            return None
        
        output_file = self.output_dir / f"{name}.{format}"
        
        # Write mermaid code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as tmp:
            tmp.write(mermaid_code)
            tmp_path = tmp.name
        
        try:
            # Run mermaid CLI
            cmd = self.mermaid_cli.split() + [
                '-i', tmp_path,
                '-o', str(output_file),
                '-t', theme,
                '-f', format
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Mermaid rendering failed: {result.stderr}")
                return None
            
            return output_file
            
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)
    
    def render_mermaid_inline(self, mermaid_code: str, format: str = 'svg') -> Optional[str]:
        """
        Render Mermaid diagram and return as inline content
        
        Args:
            mermaid_code: Mermaid diagram code
            format: Output format (svg only for inline)
        
        Returns:
            Inline SVG string or None if failed
        """
        if format != 'svg':
            logger.error("Only SVG format supported for inline rendering")
            return None
        
        # Generate temporary name
        import uuid
        temp_name = f"temp_{uuid.uuid4().hex}"
        
        # Render to file
        output_file = self.render_mermaid(mermaid_code, temp_name, format)
        
        if not output_file:
            return None
        
        try:
            # Read SVG content
            svg_content = output_file.read_text(encoding='utf-8')
            
            # Clean up for inline use
            # Remove XML declaration
            svg_content = svg_content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            
            # Add class for styling
            svg_content = svg_content.replace('<svg', '<svg class="mermaid-diagram"', 1)
            
            return svg_content.strip()
            
        finally:
            # Clean up temp file
            output_file.unlink(missing_ok=True)
    
    def process_markdown_diagrams(self, content: str) -> str:
        """
        Find and render all Mermaid diagrams in markdown content
        
        Args:
            content: Markdown content with ```mermaid blocks
        
        Returns:
            Content with rendered diagrams
        """
        import re
        
        def replace_mermaid_block(match):
            mermaid_code = match.group(1).strip()
            svg_content = self.render_mermaid_inline(mermaid_code)
            
            if svg_content:
                return f'<div class="diagram-container">\n{svg_content}\n</div>'
            else:
                # Fall back to code block if rendering failed
                return f'```mermaid\n{mermaid_code}\n```'
        
        # Find all mermaid code blocks
        pattern = r'```mermaid\n(.*?)\n```'
        return re.sub(pattern, replace_mermaid_block, content, flags=re.DOTALL)