#!/usr/bin/env python3
"""
Generate Parasol V5 book using the comprehensive book generation module
"""

import logging
from pathlib import Path
import sys

# Add the parent directory to path to import our module
sys.path.insert(0, str(Path(__file__).parent))

from parasol_book_generator import ParasolBookGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to generate the book"""
    # Paths
    book_dir = Path(".claude/commands/parasol/docs/book")
    output_dir = Path("output")
    data_dir = Path("parasol_book_data")  # For YAML/JSON data files
    
    # Create data directory if it doesn't exist
    data_dir.mkdir(exist_ok=True)
    
    # Create some sample data files
    create_sample_data_files(data_dir)
    
    # Initialize generator
    generator = ParasolBookGenerator(
        book_dir=book_dir,
        output_dir=output_dir,
        data_dir=data_dir
    )
    
    # Generate book in both formats
    logger.info("Starting Parasol V5 book generation...")
    
    try:
        generator.generate(formats=['html', 'pdf'])
        logger.info("✅ Book generation completed successfully!")
        
        # List generated files
        logger.info("\n📚 Generated files:")
        for file in output_dir.glob('*'):
            if file.is_file():
                logger.info(f"  • {file.name}")
        
    except Exception as e:
        logger.error(f"❌ Book generation failed: {e}")
        sys.exit(1)


def create_sample_data_files(data_dir: Path):
    """Create sample YAML data files for tables"""
    import yaml
    
    # Industry DNA table
    industry_dna_data = {
        'caption': '産業DNA一覧',
        'headers': ['産業', 'コア価値観', '制約条件', '成功要因'],
        'rows': [
            [
                '製造業',
                '品質第一、無駄の排除、継続的改善',
                '設備投資が巨大、リードタイムが長い、在庫リスク',
                '歩留まり向上、稼働率最大化、不良品ゼロ'
            ],
            [
                '金融業',
                '信用と信頼、リスク管理、コンプライアンス',
                '厳格な規制、24時間365日、ゼロ欠陥要求',
                '処理速度、正確性、セキュリティ'
            ],
            [
                '医療',
                '患者の安全、エビデンス重視、倫理的配慮',
                '人命に関わる、規制が複雑、情報の機密性',
                '医療過誤防止、迅速な診断、患者満足度'
            ]
        ]
    }
    
    with open(data_dir / 'industry-dna.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(industry_dna_data, f, allow_unicode=True, default_flow_style=False)
    
    # Phase comparison table
    phase_comparison_data = {
        'caption': 'フェーズ別の重点事項',
        'headers': ['フェーズ', '重点事項'],
        'rows': [
            ['Phase 0-1', '既存設備・システムの詳細調査'],
            ['Phase 2', '品質向上と効率化の価値定義'],
            ['Phase 3', '生産管理・品質管理能力'],
            ['Phase 4-7', 'MES/ERPとの統合']
        ]
    }
    
    with open(data_dir / 'phase-comparison.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(phase_comparison_data, f, allow_unicode=True, default_flow_style=False)
    
    logger.info(f"Created sample data files in {data_dir}")


if __name__ == "__main__":
    main()