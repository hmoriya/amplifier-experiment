#!/usr/bin/env python3
"""
Test script for the integrated diagram generation system
Tests the ParasolBookGenerator with diagram references
"""

import logging
from pathlib import Path
import tempfile
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_diagram_generation():
    """Test the diagram generation system"""
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        book_dir = tmp_path / "book"
        output_dir = tmp_path / "output"
        
        # Create book structure
        part_dir = book_dir / "part1-foundation"
        part_dir.mkdir(parents=True)
        
        # Create test chapter with diagram reference
        test_content = """# テスト章：Parasol 8フェーズ概要

## Parasol V5の全体フロー

以下は、Parasol V5の8つのフェーズを示すフローチャートです：

{{diagram:parasol_8_phases}}

このフローチャートは、理想的なシステムを建築するための段階的なプロセスを示しています。

## 価値トレーサビリティ

価値の流れを追跡する仕組み：

{{diagram:value_traceability}}

## ケイパビリティレベル

階層的なケイパビリティマップ：

{{diagram:capability_levels}}

## まとめ

これらの図表により、Parasol V5の構造が明確になりました。
"""
        
        chapter_file = part_dir / "chapter-test.md"
        chapter_file.write_text(test_content, encoding='utf-8')
        
        # Test diagram generation
        logger.info("Testing diagram generation...")
        
        # Import and initialize generator
        import sys
        sys.path.append(str(Path(__file__).parent))
        
        from parasol_book_generator.generator import ParasolBookGenerator
        
        # Create generator with custom chapter structure for testing
        generator = ParasolBookGenerator(book_dir, output_dir)
        generator.chapter_structure = [
            ("part1-foundation", ["chapter-test.md"])
        ]
        
        # Generate book
        logger.info("Generating test book...")
        generator.generate(['html'])
        
        # Check output
        html_file = output_dir / 'parasol-v5-book.html'
        if html_file.exists():
            content = html_file.read_text(encoding='utf-8')
            
            # Check for diagram presence
            if '```mermaid' in content:
                logger.info("✅ Mermaid diagrams found in output")
                
                # Count diagrams
                diagram_count = content.count('```mermaid')
                logger.info(f"✅ Found {diagram_count} diagrams in output")
                
                # Check specific diagrams
                if 'flowchart TD' in content:
                    logger.info("✅ Parasol 8-phase diagram generated successfully")
                if 'architecture_overview' in content or 'graph TB' in content:
                    logger.info("✅ Value traceability diagram generated successfully")
                if 'capability_map' in content or 'CL1' in content:
                    logger.info("✅ Capability levels diagram generated successfully")
                
            else:
                logger.warning("⚠️  No Mermaid diagrams found in output")
            
            # Show first part of content
            logger.info("First 1000 characters of generated HTML:")
            print("=" * 60)
            print(content[:1000])
            print("=" * 60)
            
        else:
            logger.error("❌ HTML output file not found")
        
        # Check for any generated diagram files
        diagrams_dir = output_dir / 'diagrams'
        if diagrams_dir.exists():
            diagram_files = list(diagrams_dir.glob('*'))
            logger.info(f"Generated diagram files: {[f.name for f in diagram_files]}")
        
        logger.info("Test completed")


if __name__ == '__main__':
    test_diagram_generation()