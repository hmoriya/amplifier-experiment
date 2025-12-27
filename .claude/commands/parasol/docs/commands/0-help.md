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
2. `/parasol:2-value` で価値ステージ（顧客状態遷移）を定義
3. `/parasol:3-capabilities cl1` で活動領域識別（傾向的分類）
4. `/parasol:status` で進捗確認

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
| **Phase 3: ケーパビリティ** | CL1活動領域識別（傾向的分類）・CL2ケイパビリティ（正式分類）・CL3業務オペレーション、継承関係、重複回避の工夫 |
| **Phase 4: アーキテクチャ** | BC境界確定・サービス境界・Context Map・統合パターン選択の理由 |

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
- 3a. CL1: `/parasol:3-capabilities cl1` - 活動領域識別（Core/Supporting/Generic**傾向**・参考情報）
- 3b. CL2: `/parasol:3-capabilities cl2 [VS番号]` - ケイパビリティ設計（**正式分類**・投資判断根拠）
  - 例: `/parasol:3-capabilities cl2 VS2` (製品開発)
- 3c. CL3: `/parasol:3-capabilities cl3 [capability]` - 業務オペレーション定義（分類なし・網羅性重視）
  - 例: `/parasol:3-capabilities cl3 fermentation-research`

**Phase 4: Application Design（BC境界確定）**
- `/parasol:4-application-design` - サービス境界確定、Context Map定義
- BC境界確定: Phase 3のCL3定義を入力としてBC境界を決定

**Phase 5-7**: Software Design, Implementation, Platform

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
- `/parasol:3-capabilities cl1` - 活動領域識別（CL1・傾向的分類）
- `/parasol:3-capabilities cl2 [VS番号]` - ケイパビリティ設計（CL2・正式分類）
- `/parasol:3-capabilities cl3 [capability]` - 業務オペレーション定義（CL3・分類なし）
- `/parasol:4-application-design` - BC境界確定・Context Map定義
- `/parasol:5-software-design [service] [bc]` - BC実装設計（Parasolドメイン言語）
- `/parasol:6-implementation [service] [bc]`
- `/parasol:7-platform`

パラメータ規則：`[]` = オプション、`<>` = 必須、`|` = 選択肢
VS番号形式：`VS0`, `VS1`, `VS2`, ... `VS7`

### トピック: concepts

主要概念の詳細説明：

**価値駆動ZIGZAGプロセス（2段階モデル）**:

価値からソフトウェア実装まで、2段階のZIGZAGパターンで体系的に分解：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第1段階】価値のZIGZAG（Phase 2）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VL1 ────→ VL2 ────→ VL3 ────→ VMS ────→ VS
 (抽象)   (中間)    (具体)   (マイル)  (成果)
 最上位価値   構造化    詳細価値    定義     状態変化

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第2段階】ビジネスと設計のZIGZAG（Phase 3-6）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────┐
│ Problem Space（問題領域）= WHAT（何を）                      │
│  CL1(抽象) ──→ CL2(中間) ──→ CL3(具体)                     │
│  活動領域      ドメイン分類    業務オペレーション             │
└─────────────────────────────────────────────────────────────┘
                    ↓ 問題→解決 変換（DDDマッピング）
┌─────────────────────────────────────────────────────────────┐
│ Solution Space（解決領域）= HOW（どう）                      │
│  BC ─────→ UseCase(←CL3) ──→ Service ──→ 実装            │
│  境界Ctx     ユースケース       サービス設計   コード         │
└─────────────────────────────────────────────────────────────┘
```

**各段階の役割**:

| 段階 | Level | 役割 | 成果物 |
|------|-------|------|--------|
| **第1段階** | VL1→VL2→VL3→VMS→VS | 価値のZIGZAG | 価値分解→マイル定義 |
| **第2段階** | CL1→CL2→CL3 | Problem Space | 活動領域→業務オペ |
| **第2段階** | BC→Service→実装 | Solution Space | 境界Ctx→コード |

**Value Stage（VS）とValue Stream（VStr）**:

| 用語 | 略称 | 定義 | 例 |
|------|------|------|-----|
| **Value Stage** | VS | 顧客の「状態」（個々のステージ） | VS0, VS1, VS2...VS7 |
| **Value Stream** | VStr | 価値の「流れ」（VS0→VS7の遷移プロセス全体） | 全体のフロー |

**重要**: Value Stageは「組織の活動」ではなく「顧客の状態」を定義します。

| VS | 顧客状態 | 顧客視点の定義 |
|----|----------|----------------|
| VS0 | 潜在ニーズ状態 | 「まだ気づいていないが、この価値を必要としている」 |
| VS1 | 認知到達状態 | 「この価値の存在を知る」 |
| VS2 | 選好形成状態 | 「この価値を選びたいと思う」 |
| VS3 | 意思決定状態 | 「この価値を獲得することを決める」 |
| VS4 | 価値獲得状態 | 「この価値を手に入れる」 |
| VS5 | 価値実感状態 | 「この価値を実感している」 |
| VS6 | 価値継続状態 | 「この価値を継続的に享受している」 |
| VS7 | 価値共創状態 | 「この価値を他者と共有・推奨している」 |

**VS-Swimlane モデル**:

VSを「時間文脈を持つオペレーションフェーズ」として解釈し、Capability/Operationを配置：

```
                     時間軸（Time）→
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│   VS2    │   VS3    │   VS4    │   VS5    │   VS6    │
│ 選好形成 │ 意思決定 │ 価値獲得 │ 価値実感 │ 価値継続 │
├──────────┼──────────┼──────────┼──────────┼──────────┤
│  Core:   │  Core:   │  Core:   │          │          │
│ 製品開発 │ セールス │ 出荷管理 │          │          │
│    │     │    ↑     │    ↑     │          │          │
│    └─────┼────┘     │    │     │          │          │  ← 参照関係
│       参照（依存）   │  参照    │          │          │
├──────────┼──────────┼──────────┼──────────┼──────────┤
│Supporting│Supporting│Supporting│Supporting│Supporting│
│データ基盤│データ基盤│データ基盤│データ基盤│データ基盤│  ← 進化
│   v1    │   v1    │   v2    │   v2    │   v3    │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

**VS-Swimlane の3つの特性**:

| 特性 | 説明 |
|------|------|
| **時間性** | VSは時間文脈を提供、オペレーションは時間順に配置 |
| **文脈最適化** | 同じCapabilityでもVS文脈で具体Operationが異なる |
| **参照可能性** | 先行VSで確立したCapabilityを後続VSが参照・再利用 |

**Capability分類と顧客接点**（CL2正式分類）:

| 分類 | 顧客接点 | VS紐付け | 例 |
|------|---------|---------|-----|
| **Core** | 直接 | 特定VSに紐付く | 製品開発、販売、顧客サービス |
| **Supporting** | 間接 | VStr全体を支援 | データ基盤、物流、分析 |
| **Generic** | なし | 組織全体の基盤 | HR、経理、IT運用、セキュリティ |

**設計原則**:
- **主語は顧客**: 各VSは顧客の状態を記述
- **Cap→Op導出**: 組織活動（Operation）はCapabilityを分解して導出
- **内部活動の捕捉**: Supporting/Generic CDで顧客に見えない内部活動を捕捉

**重要原則**: Phase 4でサービス枠を確定（以降の変更は高コスト）

詳細: `.claude/commands/parasol/_zigzag-process.md` を参照

### トピック: mapping

DDD/マイクロサービスへの完全なマッピング：

```
2段階ZIGZAGプロセス → DDD/マイクロサービス

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第1段階】価値のZIGZAG → ビジネスドメイン発見
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VL1→VL2→VL3 → VMS→VS  ≈ Domain（ドメイン）発見
  価値分解         マイル定義   ビジネス目標の明確化

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第2段階】ビジネスと設計のZIGZAG → サービス境界確定
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────┐
│ Problem Space → DDDの問題空間                               │
│   CL1 活動領域     ≈ Domain（ドメイン分類）                 │
│   CL2 ドメイン分類 ≈ Subdomain（マイクロサービス候補）      │
│   CL3 業務オペ     ≈ Domain Knowledge（ビジネスルール）     │
└─────────────────────────────────────────────────────────────┘
                    ↓ DDDマッピング
┌─────────────────────────────────────────────────────────────┐
│ Solution Space → DDDの解決空間                              │
│   BC 境界Ctx       ≈ Bounded Context（サービス境界確定）    │
│   Service設計      ≈ Context Map（サービス間関係）          │
│   実装             ≈ Domain Model / Aggregates / Code       │
└─────────────────────────────────────────────────────────────┘
```

**DDD対応表（技術者参照用）**:

| Parasol概念 | Phase | DDD用語 | 備考 |
|-------------|-------|---------|------|
| Value Stage (VS) | 2 | Domain | **顧客状態として定義**（組織活動ではない） |
| Value Stream (VStr) | 2 | - | VS0→VS7の価値の流れ全体 |
| Activity Area (AA) | 3 CL1 | Problem Space | Core/Supporting/Generic**傾向**（参考情報） |
| Capability (Cap) | 3 CL2 | Subdomain | **正式分類**・投資判断・サービス境界 |
| Operation (Op) | 3 CL3 | Domain Model詳細 | 分類なし・業務オペレーション詳細 |
| Service境界 | 4 | Bounded Context | ここで確定 |
| ハイレベルUC | 3-4 | Use Case | Capability内の業務 |
| Domain Model | 5 | Aggregates, Entities | 実装設計 |

**注**: Enterprise Activity（EA）は独立概念ではなく、Capability→Operation分解で導出されます。

**Context Mapパターン**:
- Partnership（対等連携）
- Customer-Supplier（上流下流）
- Conformist（準拠）
- Anti-Corruption Layer（腐敗防止層）
- Open Host Service（公開サービス）
- Published Language（公開言語）

### トピック: templates

利用可能なテンプレート一覧：

**Phase 2**: vs{N}-detail.md（各VSの詳細定義）
**Phase 3**:
  - CL1: cl1-activity-area.md（活動領域識別・傾向的分類）
  - CL2: cl2-capability-design.md（ケイパビリティ設計・正式分類）
  - CL3: cl3-operations/{capability}-operations.md（業務オペレーション・分類なし）
**Phase 4**: service-boundary-template.md, context-map-template.md, capability-bc-mapping.md, adr-template.md
**Phase 5**: domain-language-template.md, api-specification-template.md, database-design-template.md, use-case-template.md, page-definition-template.md

**V5解析エンジン対応テンプレート** (Mermaid非依存):
  - `_software-design-reference/_templates/structured-md-format.md` - 構造化MD形式（パラソルドメイン言語）
  - `_software-design-reference/_templates/test-definition-format.md` - テスト定義形式（5層テストピラミッド）

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
| **Phase 4** | zen-architect (ARCHITECT) | BC境界確定・システム設計 |
| | api-contract-designer | Context Map定義 |
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

📖 **詳細ガイド**:
- `_parasol-overview.md` - **全体構成図・Value Stream例示・UC階層**
- `_zigzag-process.md` - ZIGZAGプロセス詳細
- `_value-methodology.md` - 価値方法論
- `_parasol-architecture-overview.md` - 3層アーキテクチャ

📐 **V5.1 階層構造ガイド**:
- `_software-design-reference/capability-bc-test-structure.md` - **Capability・BC・テスト構造の整合性定義**
- `_software-design-reference/business-operations.md` - ビジネスオペレーション・ユースケース階層
