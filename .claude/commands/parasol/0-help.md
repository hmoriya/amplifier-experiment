---
description: Parasol V5 workflow guide and help (project:parasol)
---

# Parasol V5 - ヘルプシステム

Parasol V5 フレームワークの包括的なガイドとヘルプを提供します。

## 使用方法

```bash
/parasol:0-help              # メインヘルプメニュー
/parasol:0-help overview     # フレームワーク概要
/parasol:0-help workflow     # 実行ワークフロー
/parasol:0-help commands     # コマンドリファレンス
/parasol:0-help concepts     # 主要概念の説明
/parasol:0-help mapping      # DDD/マイクロサービスマッピング
/parasol:0-help templates    # テンプレート一覧
/parasol:0-help subagents    # Amplifierサブエージェント連携
```

## 実行

ユーザーからのトピックパラメータを確認し、以下のように応答します：

### パラメータなしの場合

トピック一覧とメインメニューを表示：

```
📚 Parasol V5 - ヘルプシステム

利用可能なヘルプトピック：

1. **overview** - フレームワーク概要
   `/parasol:0-help overview`

2. **workflow** - 実行ワークフロー
   `/parasol:0-help workflow`

3. **commands** - コマンドリファレンス
   `/parasol:0-help commands`

4. **concepts** - 主要概念（VS、Capability Hierarchy、ZIGZAG）
   `/parasol:0-help concepts`

5. **mapping** - DDD/マイクロサービスマッピング
   `/parasol:0-help mapping`

6. **templates** - テンプレート一覧
   `/parasol:0-help templates`

7. **subagents** - Amplifierサブエージェント連携
   `/parasol:0-help subagents`

---

🚀 クイックスタート:
1. `/parasol:1-context` でプロジェクト文脈を確立
2. `/parasol:2-value` で価値ストリームを定義
3. `/parasol:3-capabilities cl1` でドメイン分類
4. `/parasol:status` で進捗確認

📖 詳細ガイド: parasol-v5/FRAMEWORK-DESIGN.md
```

### トピック: overview

Parasol V5 フレームワークの全体像を説明：

- 目的：ビジネス価値からソフトウェア設計への体系的な変換
- 主要特徴：価値駆動、段階的分解、DDD統合、実装指向
- 7つのフェーズ概要
- ZIGZAG パターンの説明
- 参照: `/parasol:0-help workflow` で詳細ワークフロー

### 🎯 V5特有機能: 設計ストーリー出力

Parasol V5の特徴的な機能として、**設計ストーリー（なぜそう設計したか）**の自動出力があります。

#### 目的

- **理解促進**: チーム全員が設計判断の背景を理解
- **意思決定記録**: 後から見直す際に「なぜこうなっているか」がわかる
- **学習資産**: プロジェクト固有の知見をナレッジとして蓄積

#### 出力されるフェーズ

| フェーズ | 設計ストーリー内容 |
|----------|-------------------|
| **Phase 2: 価値定義** | 価値分解・MSバックキャスティング・MS→VS変換の理由 |
| **Phase 3: ケーパビリティ** | ドメイン分類・サブドメイン粒度・BC境界の理由、継承関係、重複回避の工夫 |
| **Phase 4: アーキテクチャ** | サービス境界・Context Map・統合パターン選択の理由 |

#### 設計ストーリーの参照

- 業種別の設計ストーリー例: `parasol/patterns/value/industry-value-stream-patterns.md`
- 価値方法論の設計背景: `.claude/commands/parasol/_value-methodology.md`

### トピック: workflow

完全な実行ワークフローを表示：

**Phase 1: Context（1回のみ）**
- コマンド: `/parasol:1-context`
- 成果物: organization-analysis.md, market-assessment.md, constraints.md, stakeholder-map.md

**Phase 2: Value Definition（VSごと、反復可能）**
- コマンド: `/parasol:2-value [VS番号]`
- 成果物: value-definition.md, value-streams-mapping.md, vs{N}-detail.md

**Phase 3: Capabilities（段階的、VS単位）**
- 3a. CL1: `/parasol:3-capabilities cl1` - 活動領域分類（Core/Supporting/Generic）
- 3b. CL2: `/parasol:3-capabilities cl2 [VS番号]` - ケイパビリティ設計（サービス境界）
  - 例: `/parasol:3-capabilities cl2 VS2` (製品開発)
- 3c. CL3: `/parasol:3-capabilities cl3 [capability]` - 業務オペレーション定義
  - 例: `/parasol:3-capabilities cl3 fermentation-research`
- 3d. BC: `/parasol:3-capabilities bc [capability]` - 実装設計（技術者向け）
  - 例: `/parasol:3-capabilities bc fermentation-research`

**Phase 4-7**: Architecture, Software, Implementation, Platform

### トピック: commands

全コマンドのリファレンス：

**プロジェクト管理**:
- `/parasol:project init {name}` - 新規プロジェクト作成
- `/parasol:project list` - プロジェクト一覧
- `/parasol:project info` - 現在のプロジェクト情報
- `/parasol:project status` - 進捗確認

**コンテキスト管理**:
- `/parasol:0-help [topic]` - ヘルプ
- `/parasol:status [phase]` - 進捗確認
- `/parasol:validate [scope]` - 検証

**フェーズコマンド**:
- `/parasol:1-context`
- `/parasol:2-value [VS番号]` - 例: `/parasol:2-value VS2`
- `/parasol:3-capabilities cl1` - 活動領域分類（CL1）
- `/parasol:3-capabilities cl2 [VS番号]` - ケイパビリティ設計（CL2）
- `/parasol:3-capabilities cl3 [capability]` - 業務オペレーション定義（CL3）
- `/parasol:3-capabilities bc [capability]` - 実装設計（BC）
- `/parasol:4-architecture`
- `/parasol:5-software [service] [bc]`
- `/parasol:6-implementation [service] [bc]`
- `/parasol:7-platform`

パラメータ規則：`[]` = オプション、`<>` = 必須、`|` = 選択肢
VS番号形式：`VS0`, `VS1`, `VS2`, ... `VS7`

### トピック: concepts

主要概念の詳細説明：

**Value Stream (VS)**: 企業の価値創造の流れ（VS0-VS7）

**Capability Hierarchy（ビジネスフレンドリーな4階層）**:

```
WHAT       →      HOW        →      WHAT       →      HOW
何の領域?        どう組織?         何をする?         どう実装?
    │               │                │                │
   CL1            CL2              CL3              BC
 活動領域     ケイパビリティ     業務OP          実装設計
 ─────────   ────────────     ─────────       ─────────
  経営層        事業部長        業務担当         開発者
```

- **CL1 活動領域 (Activity Area)**: 【WHAT領域】経営層向け、投資判断単位（Core/Supporting/Generic）
- **CL2 ケイパビリティ (Capability)**: 【HOW構造】事業部長向け、チーム境界・サービス境界（≈マイクロサービス候補）
- **CL3 業務オペレーション (Business Operation)**: 【WHAT詳細】業務担当者向け、トリガー→活動→成果物
- **BC 実装設計 (Bounded Context)**: 【HOW実装】開発者向け、集約/イベント/API契約

**ZIGZAG パターン**: WHAT → HOW → WHAT → HOW の交互分解アプローチ

### トピック: mapping

DDD/マイクロサービスへの完全なマッピング：

```
Value Stream (VS0-VS7)
    ↓
Phase 2: VS詳細化 (vs{N}-detail.md)
    ↓
CL1: 活動領域 (Activity Area) ≈ Domain Classification
    ↓ 【WHAT領域】経営層の投資判断単位
CL2: ケイパビリティ (Capability) ≈ Subdomain / Microservice Candidates
    ↓ 【HOW構造】チーム境界・サービス境界の定義
CL3: 業務オペレーション (Business Operation) ≈ Use Case
    ↓ 【WHAT詳細】具体的な業務活動（トリガー→活動→成果物）
BC: 実装設計 (Bounded Context)
    ↓ 【HOW実装】技術設計（集約/イベント/API契約）
L4: Aggregates, Entities, Value Objects
```

**DDD対応表（技術者参照用）**:
| Parasol用語 | DDD用語 | 備考 |
|-------------|---------|------|
| 活動領域 (CL1) | Domain + Strategic Classification | 投資判断を含む拡張 |
| ケイパビリティ (CL2) | Subdomain | チーム境界の明示を追加 |
| 業務オペレーション (CL3) | Use Case / Business Process | トリガー/成果物を構造化 |
| 実装設計 (BC) | Bounded Context | 同一概念 |

重要な対応関係とコンテキストマップパターンを説明。

### トピック: templates

利用可能なテンプレート一覧：

**Phase 2**: vs{N}-detail.md（各VSの詳細定義）
**Phase 3**:
  - CL1: cl1-domain-classification.md（ドメイン分類）
  - CL2: cl2-subdomain-design.md（ビジネスオペレーション群）
  - CL3: cl3-business-operations/{subdomain}-operations.md（ビジネスオペレーション）
  - BC: bounded-contexts/{subdomain}-bc.md（実装設計）
**Phase 4**: service-boundary-template.md, context-map-template.md, adr-template.md
**Phase 5**: domain-language-template.md, api-specification-template.md, database-design-template.md, use-case-template.md, page-definition-template.md

各フェーズのコマンドが自動的に適切なテンプレートを使用します。

### トピック: subagents

Parasol V5 は Amplifier のサブエージェントと連携して、各フェーズの品質を向上させます。

#### フェーズ別サブエージェント一覧

| フェーズ | サブエージェント | 用途 |
|----------|-----------------|------|
| **Phase 1** | concept-extractor | 業界知識・概念の抽出 |
| | content-researcher | 既存資料からの知見収集 |
| | zen-architect (ANALYZE) | 戦略的コンテキスト分析 |
| **Phase 2** | insight-synthesizer | 異なる概念間の革新的接続を発見 |
| | knowledge-archaeologist | 業界の価値創造の進化を追跡 |
| | zen-architect (ANALYZE) | 戦略的価値分析 |
| **Phase 3** | zen-architect (ANALYZE) | CL1活動領域分類 |
| | zen-architect (ARCHITECT) | CL2ケイパビリティ設計 |
| | zen-architect (ARCHITECT) | CL3業務オペレーション定義 |
| | zen-architect (ARCHITECT) + api-contract-designer | BC実装設計 |
| **Phase 4** | zen-architect (ARCHITECT) | システム設計 |
| | database-architect | データベース設計 |
| | integration-specialist | 外部システム連携 |
| | security-guardian | セキュリティレビュー |
| **Phase 5** | api-contract-designer | API仕様設計 |
| | contract-spec-author | ドメイン言語仕様化 |
| | database-architect | DBスキーマ最適化 |
| **Phase 6** | modular-builder | モジュール単位コード生成 |
| | test-coverage | テストカバレッジ分析 |
| | bug-hunter | バグ検出・修正 |
| | zen-architect (REVIEW) | コード品質レビュー |

#### DDDワークフロー連携

Parasol は Amplifier DDD ワークフロー（`/ddd:*`）と連携できます：

```
📋 Phase 5-6 での DDD ワークフロー活用

1. /ddd:prime     - DDDコンテキストをロード
2. /ddd:1-plan    - ドメイン設計の計画
3. /ddd:2-docs    - ドキュメント生成
4. /ddd:3-code-plan - 実装計画
5. /ddd:4-code    - コード実装
6. /ddd:5-finish  - クリーンアップ
```

#### ナレッジ蓄積

各フェーズで抽出した概念やパターンをナレッジベースに蓄積：

- `outputs/1-context/extracted-concepts.json` - 抽出された概念
- `outputs/2-value/value-insights.json` - 価値洞察
- `outputs/5-software/design-patterns.json` - 設計パターン
- `outputs/6-implementation/implementation-learnings.json` - 実装学習

#### サブエージェント起動方法

各フェーズのコマンドファイルに詳細なプロンプト例があります：

```
Task tool を使用して {subagent-name} を起動：

プロンプト:
「{具体的な指示}」
```

詳細は各フェーズのコマンドファイル内「🤖 Amplifierサブエージェント連携」セクションを参照。

---

📖 **詳細ガイド**: `parasol-v5/FRAMEWORK-DESIGN.md`を参照
