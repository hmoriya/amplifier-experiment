# Parasol 共有コンテキスト

このファイルは、Parasolプロジェクト実行エージェントと書籍執筆エージェント間の知識共有を実現します。

## 概要

### Parasolエージェント体系
```
┌─────────────────────────┐     ┌─────────────────────────┐
│   プロジェクト実行      │     │     書籍執筆           │
├─────────────────────────┤     ├─────────────────────────┤
│ • parasol-phase1-7      │ ←→ │ • parasol-book-architect│
│ • axiomatic-design      │     │ • 章別設計書           │
│ • 実行成果物           │     │ • BOOK_DESIGN.md       │
└─────────────────────────┘     └─────────────────────────┘
                    ↑
                    │
            PARASOL_SHARED_CONTEXT.md
                （このファイル）
```

## ZIGZAGプロセスと書籍構成のマッピング

### Phase to Chapter Mapping

| 実行フェーズ | 対応する書籍パート | 章番号 | 成果物の文書化先 |
|------------|-------------------|--------|-----------------|
| Phase 0: 準備 | Part 1: Foundation | Ch1-5 | 理論的基盤として |
| Phase 1: Context | Part 2: Organization | Ch6-7 | 組織分析結果 |
| Phase 2: Value | Part 3: Value Space | Ch9-12 | 価値定義と測定 |
| Phase 3: Capabilities | Part 4: Problem Space | Ch13-16 | ZIGZAG実行記録 |
| Phase 4: Architecture | Part 5: Solution/Arch | Ch17-19 | 設計決定理由 |
| Phase 5: Software | Part 5: Solution/SW | Ch20-22 | 実装パターン |
| Phase 6: Implementation | Part 5: Solution/Quality | Ch23-28 | 品質保証手法 |
| Phase 7: Platform | Part 6: Integration | Ch29-31 | 統合事例 |

### ZIGZAG層と書籍構造の対応

```
ZIGZAGの3層構造              書籍の8パート構造
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level 1: ビジネス層    →    Part 2-3 (Organization/Value)
  WHAT ↔ HOW

Level 2: サービス層    →    Part 4-5 (Problem/Solution)
  WHAT ↔ HOW

Level 3: 実装層        →    Part 5-6 (Implementation/Integration)
  WHAT ↔ HOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                      ↓
              Part 7-8 (Practice/Future)
              実践と将来展望
```

## 実行成果の文書化ガイドライン

### 1. フェーズ実行時の記録項目

各phaseエージェントは以下を記録：

```markdown
## Phase [X] 実行記録

### 実行概要
- **日時**: 
- **組織**: 
- **目的**: 
- **主要成果**: 

### 発見事項
- **新しい洞察**: 
- **直面した課題**: 
- **解決アプローチ**: 

### 書籍化のポイント
- **どの章に反映すべきか**: Chapter [X]
- **ストーリー候補**: 
- **学習ポイント**: 
- **コード例の有無**: 
```

### 2. 成果物から章への変換プロセス

```
実行成果物                  →  章のセクション
────────────────────────────────────────────
分析レポート               →  Section 1: フック（実例）
課題定義                   →  Section 2: 問題の本質
解決フレームワーク         →  Section 3: 核心概念
実装コード                 →  Section 4: 実世界例（最小化）
適用手順                   →  Section 5: 実践ガイダンス
統合パターン               →  Section 6: 技術統合
```

### 3. コード比率管理

**実行時のコード**: 通常50-70%（実装詳細含む）
**書籍化後のコード**: 必ず30%以下に圧縮

変換ルール：
1. 完全実装 → 概念説明 + 最小例
2. 設定ファイル → 重要部分の抜粋
3. ツールコマンド → 手順の要約
4. エラー処理 → パターンの説明

## 用語集と表記統一

### 統一用語（全エージェント共通）

| 日本語 | 英語 | 表記ルール |
|--------|------|------------|
| ジグザグ | ZIGZAG | 全て大文字、ハイフンなし |
| ケイパビリティ | Capability | カタカナ統一 |
| コンテキスト | Context | カタカナ統一 |
| 価値ストリーム | Value Stream | 英語は頭文字大文字 |
| 設計行列 | Design Matrix | 英語は頭文字大文字 |
| 機能要求 | Functional Requirement (FR) | 略語は初出で説明 |
| 設計パラメータ | Design Parameter (DP) | 略語は初出で説明 |

### フェーズ表記

- **実行時**: Phase 0, Phase 1, ... Phase 7
- **書籍内**: Part 1, Part 2, ... Part 8
- **章番号**: Chapter 1, Chapter 2, ... Chapter 38

### 読者層の呼称

1. **エグゼクティブ**: 経営層、意思決定者
2. **アーキテクト**: 設計者、技術リーダー
3. **開発者**: 実装者、エンジニア

## エージェント間の連携プロトコル

### 1. Phase実行 → 書籍化フロー

```
parasol-phase[X]
    ↓ 実行成果
PARASOL_SHARED_CONTEXT.md（マッピング確認）
    ↓ 
parasol-book-architect
    ↓ 章設計
chapter[X]_design.md
    ↓ 執筆
chapter[X].md + appendix[X].md
```

### 2. 品質チェックポイント

- [ ] 実行成果が該当章にマッピングされているか
- [ ] 用語統一が守られているか
- [ ] コード比率30%以下か
- [ ] 3読者層への価値が明確か
- [ ] ストーリー性があるか

### 3. 相互参照

各エージェントは以下を参照：
- **本ファイル**: マッピングと用語統一
- **BOOK_DESIGN.md**: 全体構造と品質基準
- **STYLE_GUIDE.md**: 執筆スタイル
- **CHAPTER_CONTEXT_TEMPLATE.md**: 章構成

## バージョン管理と更新

### 更新タイミング
- 新しいフェーズ実行完了時
- 章構成の変更時
- 用語の追加・変更時

### 更新手順
1. 該当エージェントが提案
2. parasol-book-architectがレビュー
3. 合意後に本ファイル更新
4. 全エージェントに通知

---

最終更新: 2025-12-28
管理責任: parasol-book-architect + 全parasol-phaseエージェント