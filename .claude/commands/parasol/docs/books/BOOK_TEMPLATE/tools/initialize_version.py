#!/usr/bin/env python3
"""
Parasol書籍の新バージョン初期化スクリプト
"""

import os
import yaml
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class VersionInitializer:
    """新バージョンの初期化を管理するクラス"""
    
    def __init__(self, template_dir: Path, target_dir: Path, config: Dict[str, Any]):
        self.template_dir = template_dir
        self.target_dir = target_dir
        self.config = config
        
    def initialize(self) -> None:
        """新バージョンを初期化"""
        print(f"Initializing Parasol {self.config['version']}-{self.config['variant']}...")
        
        # 基本構造の作成
        self._create_directory_structure()
        
        # 設定ファイルの配置
        self._setup_config_files()
        
        # テンプレートの展開
        self._expand_templates()
        
        # ベースバージョンからの継承（該当する場合）
        if self.config.get('base_version'):
            self._inherit_from_base()
            
        # 初期ドキュメントの生成
        self._generate_initial_docs()
        
        print("✅ Initialization complete!")
        
    def _create_directory_structure(self) -> None:
        """ディレクトリ構造を作成"""
        directories = [
            'design',
            'diagrams', 
            'appendices',
            'archive',
            'tools',
            'config'
        ]
        
        # パート構造の作成
        for i in range(1, 9):  # Part 1-8
            if i == 5:
                # Part 5は3つのセクション
                directories.extend([
                    f'part5-architecture',
                    f'part5-software-design',
                    f'part5-implementation-quality'
                ])
            else:
                part_names = {
                    1: 'foundation',
                    2: 'organization', 
                    3: 'value-space',
                    4: 'problem-space',
                    6: 'integration',
                    7: 'practice',
                    8: 'future-outlook'
                }
                directories.append(f'part{i}-{part_names.get(i, "unknown")}')
                
        for dir_name in directories:
            (self.target_dir / dir_name).mkdir(parents=True, exist_ok=True)
            
    def _setup_config_files(self) -> None:
        """設定ファイルを配置"""
        # VERSION_CONFIG.ymlのカスタマイズ
        version_config = self.config.copy()
        version_config['metadata']['release_date'] = datetime.now().strftime('%Y-%m-%d')
        
        with open(self.target_dir / 'VERSION_CONFIG.yml', 'w', encoding='utf-8') as f:
            yaml.dump(version_config, f, allow_unicode=True, default_flow_style=False)
            
    def _expand_templates(self) -> None:
        """テンプレートファイルを展開"""
        # 変数置換用の辞書
        replacements = {
            '[VERSION]': self.config['version'],
            '[VARIANT]': self.config['variant'],
            '[STATUS]': self.config['status'],
            '[YYYY-MM-DD]': datetime.now().strftime('%Y-%m-%d'),
            'X.Y': self.config['version']
        }
        
        # テンプレートファイルのコピーと置換
        template_files = [
            'README.md',
            'BOOK_DESIGN.md', 
            'STYLE_GUIDE.md',
            'CHAPTER_TEMPLATE.md'
        ]
        
        for file_name in template_files:
            src = self.template_dir / file_name
            dst = self.target_dir / file_name
            
            if src.exists():
                with open(src, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 変数置換
                for key, value in replacements.items():
                    content = content.replace(key, str(value))
                    
                with open(dst, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
    def _inherit_from_base(self) -> None:
        """ベースバージョンから継承"""
        base_version = self.config['base_version']
        base_dir = self.template_dir.parent / f"parasol-v{base_version}-modular"
        
        if not base_dir.exists():
            print(f"⚠️  Base version {base_version} not found, skipping inheritance")
            return
            
        # 継承する要素
        inheritable = [
            'GLOSSARY.md',
            'appendices/*',
            'diagrams/*.puml'
        ]
        
        print(f"Inheriting from base version {base_version}...")
        
        for pattern in inheritable:
            if '*' in pattern:
                # ワイルドカードパターン
                base_path = base_dir / pattern.replace('*', '')
                if base_path.parent.exists():
                    for item in base_path.parent.glob(base_path.name):
                        if item.is_file():
                            dst = self.target_dir / item.relative_to(base_dir)
                            dst.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(item, dst)
            else:
                # 単一ファイル
                src = base_dir / pattern
                if src.exists():
                    dst = self.target_dir / pattern
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    
    def _generate_initial_docs(self) -> None:
        """初期ドキュメントを生成"""
        # CHANGELOG.md
        changelog_content = f"""# Changelog - Parasol {self.config['version']}-{self.config['variant']}

## [{self.config['version']}] - {datetime.now().strftime('%Y-%m-%d')}

### Added
- Initial version based on Parasol methodology

### Changed
- [List changes from base version if applicable]

### Removed
- [List removed features if applicable]
"""
        
        with open(self.target_dir / 'CHANGELOG.md', 'w', encoding='utf-8') as f:
            f.write(changelog_content)
            
        # STATUS.md
        status_content = f"""# Parasol {self.config['version']}-{self.config['variant']} Status

**Current Status**: {self.config['status']}  
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}

## Progress

- [ ] Part 1: Foundation (0/5 chapters)
- [ ] Part 2: Organization (0/3 chapters)  
- [ ] Part 3: Value Space (0/4 chapters)
- [ ] Part 4: Problem Space (0/4 chapters)
- [ ] Part 5: Solution Space (0/12 chapters)
- [ ] Part 6: Integration (0/3 chapters)
- [ ] Part 7: Practice (0/4 chapters)
- [ ] Part 8: Future Outlook (0/3 chapters)

## Next Steps

1. Review and customize BOOK_DESIGN.md
2. Begin chapter planning in design/ directory
3. Set up quality review process
"""
        
        with open(self.target_dir / 'STATUS.md', 'w', encoding='utf-8') as f:
            f.write(status_content)


def main():
    parser = argparse.ArgumentParser(description='Initialize a new Parasol book version')
    parser.add_argument('--config', required=True, help='Path to VERSION_CONFIG.yml')
    parser.add_argument('--target', required=True, help='Target directory for new version')
    parser.add_argument('--template', default='.', help='Template directory (default: current)')
    
    args = parser.parse_args()
    
    # 設定の読み込み
    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    # パスの設定
    template_dir = Path(args.template).resolve()
    target_dir = Path(args.target).resolve()
    
    # 初期化の実行
    initializer = VersionInitializer(template_dir, target_dir, config)
    initializer.initialize()


if __name__ == '__main__':
    main()