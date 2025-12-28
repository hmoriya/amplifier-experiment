"""Content generation for Parasol V5.4 book chapters."""

import logging
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
import re

from .models import ChapterMetadata, DiagramMetadata
from .constants import WORDS_PER_PAGE
from .utils import calculate_word_count, calculate_page_count, format_chapter_number

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates chapter content using templates and domain knowledge."""
    
    def __init__(self, template_dir: str = "templates"):
        """Initialize content generator."""
        self.template_dir = Path(__file__).parent / template_dir
        self.glossary = self._load_glossary()
        self.chapter_templates = self._load_chapter_templates()
    
    def _load_glossary(self) -> Dict[str, str]:
        """Load technical glossary."""
        glossary_path = Path(__file__).parent / "content" / "glossary.json"
        if glossary_path.exists():
            with open(glossary_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_chapter_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load chapter content templates."""
        # In a real implementation, these would be loaded from files
        # For now, we'll define them inline
        return self._get_chapter_content_templates()
    
    def generate_chapter_content(self, chapter: ChapterMetadata, 
                               diagrams: List[DiagramMetadata] = None) -> str:
        """Generate complete chapter content."""
        # Get template data for this chapter
        template_data = self._get_chapter_template_data(chapter)
        
        # Generate main content
        main_content = self._generate_main_content(chapter, template_data)
        
        # Add diagrams if provided
        if diagrams:
            main_content = self._integrate_diagrams(main_content, diagrams)
        
        # Process glossary terms
        main_content = self._process_glossary_terms(main_content)
        
        # Ensure content meets page target
        main_content = self._adjust_content_length(main_content, chapter.target_pages)
        
        # Generate complete chapter using template
        full_content = self._apply_chapter_template(chapter, template_data, main_content)
        
        return full_content
    
    def _get_chapter_template_data(self, chapter: ChapterMetadata) -> Dict[str, Any]:
        """Get template data for a specific chapter."""
        # Check if we have specific template for this chapter
        if chapter.chapter_id in self.chapter_templates:
            return self.chapter_templates[chapter.chapter_id]
        
        # Generate default template data
        return self._generate_default_template_data(chapter)
    
    def _generate_default_template_data(self, chapter: ChapterMetadata) -> Dict[str, Any]:
        """Generate default template data for a chapter."""
        return {
            'overview': f"{chapter.title}に関する詳細な解説",
            'learning_objectives': [
                f"{chapter.title}の基本概念を理解する",
                f"{chapter.title}の実践的な適用方法を学ぶ",
                f"{chapter.title}に関するベストプラクティスを習得する"
            ],
            'key_points': [
                {'title': '重要ポイント1', 'description': '説明'},
                {'title': '重要ポイント2', 'description': '説明'},
            ],
            'summary': f"{chapter.title}について学びました",
            'next_steps': "次章ではさらに詳細な内容を学習します"
        }
    
    def _generate_main_content(self, chapter: ChapterMetadata, 
                              template_data: Dict[str, Any]) -> str:
        """Generate the main content for a chapter."""
        # Get content generator based on chapter type
        if "phase" in chapter.chapter_id.lower():
            return self._generate_phase_content(chapter)
        elif "value" in chapter.chapter_id.lower():
            return self._generate_value_content(chapter)
        elif "capability" in chapter.chapter_id.lower():
            return self._generate_capability_content(chapter)
        elif "architecture" in chapter.chapter_id.lower():
            return self._generate_architecture_content(chapter)
        elif "claude-code" in chapter.chapter_id:
            return self._generate_claude_code_content(chapter)
        else:
            return self._generate_generic_content(chapter)
    
    def _generate_phase_content(self, chapter: ChapterMetadata) -> str:
        """Generate content for phase-related chapters."""
        phase_match = re.search(r'phase(\d)', chapter.chapter_id.lower())
        phase_num = int(phase_match.group(1)) if phase_match else 0
        
        content = f"""## Phase {phase_num}の概要

Phase {phase_num}は、Parasol V5フレームワークにおける重要なステップです。

### 目的と背景

このフェーズでは、以下のことを実現します：

"""
        
        # Add phase-specific content based on phase number
        phase_content = self._get_phase_specific_content(phase_num)
        content += phase_content
        
        return content
    
    def _get_phase_specific_content(self, phase_num: int) -> str:
        """Get phase-specific content."""
        phase_contents = {
            0: """
### 組織とドメインの理解

Phase 0では、プロジェクトを開始する前に、組織とビジネスドメインを深く理解します。

#### ステップ1：組織文化の把握

組織の文化、価値観、意思決定プロセスを理解します。

#### ステップ2：ドメイン知識の収集

ビジネスドメインの専門知識を収集し、整理します。

#### ステップ3：ステークホルダー分析

関係者を識別し、それぞれのニーズと期待を明確にします。
""",
            1: """
### プロジェクト基盤の構築

Phase 1では、プロジェクトを成功に導くための基盤を構築します。

#### チーム編成

適切なスキルセットを持ったチームを編成します。

#### 開発環境の整備

効率的な開発を可能にするツールと環境を整備します。

#### 産業パターンの選択

業界に適したパターンを選択し、適用します。
""",
            2: """
### 価値の発見と設計

Phase 2は、Parasol V5の中核となる価値中心アプローチを実現するフェーズです。

#### 価値探索

6軸探索システムを使用して、ビジネス価値を網羅的に探索します。

#### 価値ストリームマッピング

発見された価値をストリームとして整理し、可視化します。

#### VS/VL設計

価値ステージと価値レベルを定義し、階層化します。
"""
        }
        
        return phase_contents.get(phase_num, self._generate_generic_phase_content(phase_num))
    
    def _generate_generic_phase_content(self, phase_num: int) -> str:
        """Generate generic phase content."""
        return f"""
### Phase {phase_num}の実施内容

このフェーズでは、以下の活動を実施します：

1. 現状分析と課題の特定
2. 目標設定と計画策定
3. 実施と検証
4. 次フェーズへの準備

### 成果物

- 文書化された分析結果
- 実行計画
- 検証結果
"""
    
    def _generate_value_content(self, chapter: ChapterMetadata) -> str:
        """Generate content for value-related chapters."""
        return f"""
## 価値中心アプローチ

Parasol V5の最大の特徴は、価値を中心に据えたアプローチです。

### 価値とは何か

ビジネスにおける価値とは、顧客やステークホルダーが得る利益やベネフィットを指します。

### 価値の種類

1. **経済的価値**：コスト削減、売上増加
2. **時間的価値**：時間短縮、効率化
3. **品質的価値**：品質向上、エラー減少
4. **体験的価値**：顧客満足度、ユーザビリティ

### 価値の識別方法

6軸探索システムを使用して、全方位的に価値を探索します：

1. **WHO軸**：誰のための価値か
2. **WHAT軸**：何を提供するのか
3. **WHEN軸**：いつ価値が実現されるのか
4. **WHERE軸**：どこで価値が生まれるのか
5. **WHY軸**：なぜそれが価値なのか
6. **HOW軸**：どのように価値を実現するのか
"""
    
    def _generate_capability_content(self, chapter: ChapterMetadata) -> str:
        """Generate content for capability-related chapters."""
        return f"""
## ケイパビリティの理解

ケイパビリティ（能力）は、価値を実現するために組織が持つべき機能を表します。

### ケイパビリティレベル（CL）

Parasol V5では、ケイパビリティを4つのレベルに分類します：

#### CL0：コアケイパビリティ

ビジネスの中核となる差別化要素である能力です。

- 競争優位の源泉
- 簡単に模倣できない
- ビジネスのアイデンティティ

#### CL1：サポートケイパビリティ

コアケイパビリティを支える重要な能力です。

- コアを効果的に機能させる
- 業界標準の実装
- 最適化が重要

#### CL2：基盤ケイパビリティ

システム全体を支える基礎的な能力です。

- セキュリティ、認証
- 監査、コンプライアンス
- システム運用

#### CL3：汎用ケイパビリティ

どのビジネスでも必要な一般的な能力です。

- メール送信
- ファイル管理
- 基本的なデータ処理

### ケイパビリティの分解方法

価値からケイパビリティを導出する際は、「この価値を実現するために何が必要か？」と問いかけます。
"""
    
    def _generate_architecture_content(self, chapter: ChapterMetadata) -> str:
        """Generate content for architecture-related chapters."""
        return f"""
## アーキテクチャ設計

ソフトウェアアーキテクチャは、システムの基本的な構造と振る舞いを定義します。

### アーキテクチャパターン

Parasol V5では、以下のアーキテクチャパターンを推奨します：

#### 1. レイヤードアーキテクチャ

関心事を層ごとに分離し、保守性を高めます。

- プレゼンテーション層
- アプリケーション層
- ドメイン層
- インフラストラクチャ層

#### 2. マイクロサービスアーキテクチャ

ケイパビリティごとに独立したサービスとして実装します。

- 高いスケーラビリティ
- 独立したデプロイ
- 技術スタックの自由度

#### 3. イベント駆動アーキテクチャ

ビジネスイベントを中心にシステムを構築します。

- 結合度の低減
- 監査性の向上
- 柔軟な統合

### BCへのマッピング

ケイパビリティをBounded Contextにマッピングする際のポイント：

1. **ビジネス時間的凝集**：同じタイミングで変更される機能をまとめる
2. **ドメイン言語の統一**：同じ用語を使う範囲をBCとする
3. **チームの境界**：一つのチームが責任を持つ範囲
"""
    
    def _generate_claude_code_content(self, chapter: ChapterMetadata) -> str:
        """Generate content for Claude Code integration chapter."""
        return f"""
## Claude Code統合

Claude Codeは、AIを活用したコード生成・支援ツールで、Parasol V5の実装を加速します。

### Claude Codeの活用シーン

#### 1. コード生成

ケイパビリティの仕様から、基本的な実装コードを自動生成します。

```python
# Claude Codeへの指示例
"受注管理ケイパビリティの基本的なCRUD操作を実装してください。
DDDのパターンに従って、Repositoryパターンを使用してください。"
```

#### 2. テストコード生成

実装されたコードに対して、網羅的なテストコードを生成します。

#### 3. ドキュメント生成

コードからドキュメントを自動生成し、保守性を向上させます。

### ベストプラクティス

1. **明確な指示**：曖昧さを避け、具体的な要求を伝える
2. **段階的な利用**：小さなタスクから始めて徐々に拡大
3. **レビューの重要性**：AI生成コードも必ずレビューする
4. **コンテキストの提供**：既存コードやアーキテクチャを共有

### 導入効果

- **開発速度の向上**：定型的なコードの自動生成
- **品質の均一化**：ベストプラクティスの自動適用
- **学習効率の向上**：AIからのフィードバック
"""
    
    def _generate_generic_content(self, chapter: ChapterMetadata) -> str:
        """Generate generic chapter content."""
        return f"""
## {chapter.title}

{chapter.title}は、Parasol V5フレームワークにおいて重要な役割を果たします。

### 概要

この章では、{chapter.title}について詳しく解説します。

### 基本概念

{chapter.title}を理解するためには、以下の概念を把握する必要があります：

1. 基本的な定義と用語
2. 関連する概念との関係性
3. 実践的な適用方法

### 実践アプローチ

実際のプロジェクトで{chapter.title}を活用するためのアプローチを紹介します。

### 具体例

以下に、{chapter.title}の具体的な適用例を示します：

#### 例1：基本的なケース

シンプルな状況での適用例です。

#### 例2：応用的なケース  

より複雑な状況での適用例です。

### 注意点

{chapter.title}を実践する際に注意すべきポイント：

- 誤った適用を避ける
- パフォーマンスへの影響を考慮する
- チーム内での共通理解を促進する
"""
    
    def _integrate_diagrams(self, content: str, diagrams: List[DiagramMetadata]) -> str:
        """Integrate diagrams into chapter content."""
        for diagram in diagrams:
            # Find appropriate location to insert diagram
            # For now, we'll append at the end of relevant sections
            diagram_markdown = f"""
### {diagram.title}

```mermaid
{diagram.mermaid_code}
```

*{diagram.description}*
"""
            
            # Simple heuristic: insert after related heading
            if diagram.type == "flow":
                content = self._insert_after_heading(content, "フロー", diagram_markdown)
            elif diagram.type == "architecture":
                content = self._insert_after_heading(content, "アーキテクチャ", diagram_markdown)
            else:
                # Append at end if no specific location found
                content += "\n" + diagram_markdown
        
        return content
    
    def _insert_after_heading(self, content: str, heading_keyword: str, 
                            insert_content: str) -> str:
        """Insert content after a heading containing keyword."""
        lines = content.split('\n')
        inserted = False
        
        for i, line in enumerate(lines):
            if line.startswith('#') and heading_keyword in line:
                # Find the end of this section
                section_end = i + 1
                while section_end < len(lines) and not lines[section_end].startswith('#'):
                    section_end += 1
                
                # Insert before next heading or at end
                lines.insert(section_end, insert_content)
                inserted = True
                break
        
        if not inserted:
            lines.append(insert_content)
        
        return '\n'.join(lines)
    
    def _process_glossary_terms(self, content: str) -> str:
        """Process glossary terms in content."""
        # Replace glossary terms with tooltips
        for term, definition in self.glossary.items():
            # Only replace whole words
            pattern = r'\b' + re.escape(term) + r'\b'
            replacement = f'<abbr title="{definition}">{term}</abbr>'
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _adjust_content_length(self, content: str, target_pages: int) -> str:
        """Adjust content length to meet page target."""
        current_pages = calculate_page_count(content)
        
        if current_pages < target_pages * 0.9:  # Too short
            # Add more content
            additional_content = self._generate_additional_content(target_pages - current_pages)
            content += "\n\n" + additional_content
        elif current_pages > target_pages * 1.1:  # Too long
            # Trim content (simplified - in reality would be more sophisticated)
            target_words = target_pages * WORDS_PER_PAGE
            current_words = calculate_word_count(content)
            if current_words > target_words:
                # Keep proportion of content
                ratio = target_words / current_words
                lines = content.split('\n')
                keep_lines = int(len(lines) * ratio)
                content = '\n'.join(lines[:keep_lines])
        
        return content
    
    def _generate_additional_content(self, pages_needed: int) -> str:
        """Generate additional content to meet page requirements."""
        words_needed = pages_needed * WORDS_PER_PAGE
        
        additional_sections = [
            """
### 詳細な解説

このセクションでは、さらに詳細な情報を提供します。
""",
            """
### ケーススタディ

実際のプロジェクトでの適用事例を紹介します。
""",
            """
### ベストプラクティス

推奨される実践方法とパターンを説明します。
""",
            """
### よくある課題と解決策

実践上よく遇到する問題とその対処法を説明します。
"""
        ]
        
        # Add sections until we meet the word count
        added_content = ""
        current_word_count = 0
        
        for section in additional_sections:
            added_content += section
            current_word_count = calculate_word_count(added_content)
            if current_word_count >= words_needed:
                break
        
        return added_content
    
    def _apply_chapter_template(self, chapter: ChapterMetadata, 
                               template_data: Dict[str, Any], 
                               main_content: str) -> str:
        """Apply chapter template to generate final content."""
        # For now, we'll use a simple template substitution
        # In a real implementation, this would use Jinja2
        
        template = self._get_base_chapter_template()
        
        # Prepare template variables
        variables = {
            'title': chapter.title,
            'number': chapter.number,
            'part_title': self._get_part_title(chapter.part_id),
            'keywords': chapter.keywords,
            'breadcrumb': self._generate_breadcrumb(chapter),
            'overview': template_data.get('overview', ''),
            'learning_objectives': template_data.get('learning_objectives', []),
            'prerequisites': chapter.prerequisites,
            'content': main_content,
            'summary': template_data.get('summary', ''),
            'key_points': template_data.get('key_points', []),
            'exercises': template_data.get('exercises', []),
            'next_steps': template_data.get('next_steps', ''),
            'references': template_data.get('references', []),
            'prev_chapter': self._get_prev_chapter_link(chapter),
            'next_chapter': self._get_next_chapter_link(chapter)
        }
        
        # Simple template replacement
        result = template
        for key, value in variables.items():
            if isinstance(value, list):
                value = '\n'.join(f"- {item}" for item in value)
            elif isinstance(value, dict):
                continue  # Skip complex objects for now
            result = result.replace(f"{{{{{key}}}}}", str(value))
        
        return result
    
    def _get_base_chapter_template(self) -> str:
        """Get base chapter template."""
        # Simplified version of the template
        return """
---
title: {{title}}
chapter: {{number}}
keywords: {{keywords}}
---

# 第{{number}}章：{{title}}

{{breadcrumb}}

## 概要

{{overview}}

## 学習目標

{{learning_objectives}}

---

{{content}}

---

## まとめ

{{summary}}

## 次のステップ

{{next_steps}}

---

[← 前の章]({{prev_chapter}}) | [目次](../index.md) | [次の章 →]({{next_chapter}})
"""
    
    def _get_part_title(self, part_id: str) -> str:
        """Get part title from ID."""
        part_titles = {
            "part1": "基礎編",
            "part2": "組織理解編",
            "part3": "価値領域編",
            "part4": "問題領域編",
            "part5": "解決領域編",
            "part6": "統合編",
            "part7": "実践編",
            "part8": "発展編"
        }
        return part_titles.get(part_id, "")
    
    def _generate_breadcrumb(self, chapter: ChapterMetadata) -> str:
        """Generate breadcrumb navigation."""
        part_title = self._get_part_title(chapter.part_id)
        return f"[Parasol V5.4 完全ガイド](../../index.md) > [{part_title}](../index.md) > {format_chapter_number(chapter.number)}"
    
    def _get_prev_chapter_link(self, chapter: ChapterMetadata) -> str:
        """Get link to previous chapter."""
        if chapter.number > 1:
            return f"chapter{chapter.number - 1}.md"
        return "../index.md"
    
    def _get_next_chapter_link(self, chapter: ChapterMetadata) -> str:
        """Get link to next chapter."""
        if chapter.number < 38:
            return f"chapter{chapter.number + 1}.md"
        return "../../appendices/index.md"
    
    def _get_chapter_content_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get content templates for specific chapters."""
        # This would normally be loaded from files
        # For now, return a sample structure
        return {
            "chapter1-why-parasol": {
                'overview': "Parasol V5がなぜ必要なのか、その背景と動機を解説します",
                'learning_objectives': [
                    "現代のソフトウェア開発の課題を理解する",
                    "Parasol V5が解決する問題を把握する",
                    "V5の基本的な価値提案を説明できるようになる"
                ],
                'summary': "Parasol V5は、ビジネス価値と技術実装を統合的に管理するフレームワークです",
                'next_steps': "次章では、V5の核心となる3つのスペースについて学びます"
            }
        }