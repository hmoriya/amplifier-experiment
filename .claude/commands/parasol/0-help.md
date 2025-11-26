---
description: Parasol V4 Lite workflow guide and help (project:parasol)
---

# Parasol V4 Lite - ヘルプシステム

Parasol V4 Lite フレームワークの包括的なガイドとヘルプを提供します。

## 使用方法

```bash
/parasol:0-help              # メインヘルプメニュー
/parasol:0-help overview     # フレームワーク概要
/parasol:0-help workflow     # 実行ワークフロー
/parasol:0-help commands     # コマンドリファレンス
/parasol:0-help concepts     # 主要概念の説明
/parasol:0-help mapping      # DDD/マイクロサービスマッピング
/parasol:0-help templates    # テンプレート一覧
```

## 実行

ユーザーからのトピックパラメータを確認し、以下のように応答します：

### パラメータなしの場合

トピック一覧とメインメニューを表示：

```
📚 Parasol V4 Lite - ヘルプシステム

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

---

🚀 クイックスタート:
1. `/parasol:1-context` でプロジェクト文脈を確立
2. `/parasol:2-value` で価値ストリームを定義
3. `/parasol:3-capabilities cl1` でドメイン分類
4. `/parasol:status` で進捗確認

📖 詳細ガイド: parasol-v4-lite/FRAMEWORK-DESIGN.md
```

### トピック: overview

Parasol V4 Lite フレームワークの全体像を説明：

- 目的：ビジネス価値からソフトウェア設計への体系的な変換
- 主要特徴：価値駆動、段階的分解、DDD統合、実装指向
- 7つのフェーズ概要
- ZIGZAG パターンの説明
- 参照: `/parasol:0-help workflow` で詳細ワークフロー

### トピック: workflow

完全な実行ワークフローを表示：

**Phase 1: Context（1回のみ）**
- コマンド: `/parasol:1-context`
- 成果物: organization-analysis.md, market-assessment.md, constraints.md, stakeholder-map.md

**Phase 2: Value Definition（VSごと、反復可能）**
- コマンド: `/parasol:2-value [VS番号]`
- 成果物: value-definition.md, value-streams-mapping.md, vs{N}-detail.md

**Phase 3: Capabilities（段階的、VS単位）**
- 3a. CL1: `/parasol:3-capabilities cl1` - 全VSのドメイン分類
- 3b. CL2: `/parasol:3-capabilities cl2 [VS番号]` - VS単位でサブドメイン設計
  - 例: `/parasol:3-capabilities cl2 VS2` (製品開発)
- 3c. CL3: `/parasol:3-capabilities cl3 [subdomain]` - サブドメインのBC定義
  - 例: `/parasol:3-capabilities cl3 vs2-fermentation-tech`

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
- `/parasol:3-capabilities cl1` - 全VSのドメイン分類
- `/parasol:3-capabilities cl2 [VS番号]` - 例: `/parasol:3-capabilities cl2 VS2`
- `/parasol:3-capabilities cl3 [subdomain]` - 例: `/parasol:3-capabilities cl3 vs2-fermentation-tech`
- `/parasol:4-architecture`
- `/parasol:5-software [service] [bc]`
- `/parasol:6-implementation [service] [bc]`
- `/parasol:7-platform`

パラメータ規則：`[]` = オプション、`<>` = 必須、`|` = 選択肢
VS番号形式：`VS0`, `VS1`, `VS2`, ... `VS7`

### トピック: concepts

主要概念の詳細説明：

**Value Stream (VS)**: 企業の価値創造の流れ（VS0-VS7）

**Capability Hierarchy**:
- CL1: 戦略的（ドメイン分類：Core/Supporting/Generic）
- CL2: 戦術的（サブドメイン≈マイクロサービス候補）
- CL3: 運用的（Bounded Context）
- L4: システム/コンポーネント

**ZIGZAG パターン**: WHAT→HOW→WHAT の分解アプローチ

### トピック: mapping

DDD/マイクロサービスへの完全なマッピング：

```
Value Stream (VS0-VS7)
    ↓
Phase 2: VS詳細化 (vs{N}-detail.md)
    ↓
CL1: Domain Type Classification (Core/Supporting/Generic)
    ↓
CL2: VS単位でSubdomain設計 ≈ Microservice Candidates
    ↓
CL3: Bounded Context = Team Boundaries
    ↓
Business Operations = Use Cases + UI
    ↓
L4: Aggregates, Entities, Value Objects
```

**VS単位のサブドメイン分解**:
- VS2 → vs2-subdomains.md → vs2-fermentation-tech-bc, vs2-product-dev-bc, ...
- VS3 → vs3-subdomains.md → vs3-brand-mgmt-bc, vs3-campaign-bc, ...

重要な対応関係とコンテキストマップパターンを説明。

### トピック: templates

利用可能なテンプレート一覧：

**Phase 2**: vs{N}-detail.md（各VSの詳細定義）
**Phase 3**:
  - CL1: strategic-classification.md（ドメイン分類）
  - CL2: vs{N}-subdomains.md（VS単位のサブドメイン設計）
  - CL3: {subdomain-name}-bc.md（Bounded Context定義）
**Phase 4**: service-boundary-template.md, context-map-template.md, adr-template.md
**Phase 5**: domain-language-template.md, api-specification-template.md, database-design-template.md, use-case-template.md, page-definition-template.md

各フェーズのコマンドが自動的に適切なテンプレートを使用します。

---

📖 **詳細ガイド**: `parasol-v4-lite/FRAMEWORK-DESIGN.md`を参照
