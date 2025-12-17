# Parasol V5 - CL階層定義（Capability Level Hierarchy）

## 概要

本ドキュメントは、Parasol V5におけるCL（Capability Level）階層の正式定義です。DDDの標準的解釈との整合性を確保しつつ、Parasol独自の価値駆動アプローチを明確化しています。

### DDDとの対応（Problem Space → Solution Space）

```
┌─────────────────────────────────────────────────────────────────┐
│                      DDD概念との対応                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CL1 ≈ Problem Space（問題領域）                               │
│         └─ 「何を解決すべきか」の全体像                         │
│         └─ 傾向的分類は"どの領域が重要そうか"の初期仮説         │
│                                                                  │
│   CL2 ≈ Subdomain（サブドメイン）                               │
│         └─ 「どう分割して取り組むか」                           │
│         └─ 正式分類＝投資配分の意思決定                         │
│                                                                  │
│   CL3 ≈ Domain Model詳細（Business Operation）                  │
│         └─ 「具体的に何をするか」（複数アクター協調）           │
│                                                                  │
│   Actor UseCase ≈ UseCase（アプリケーション層）                 │
│         └─ 「誰が何をするか」（★シングルアクター）             │
│         └─ Agile User Storyに対応（INVEST原則）                 │
│                                                                  │
│   BC  = Solution Space（解決領域）の境界                        │
│         └─ 「どう実装するか」の技術的境界                       │
│         └─ 内容: Domain Model(SSOT) + DB + API                  │
│                                                                  │
│   View ≈ Presentation（プレゼンテーション層）                   │
│         └─ 「どの画面で実現するか」                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 階層サマリー

```
                           【Phase 2-3: ビジネス設計】
CL1 (Value Stream Level) ──┬── Core/Supporting/Generic: 傾向的分類（参考情報）
        │                  └── 経営判断：どのVSに投資するか     【Initiative】
        ↓ 1:N
CL2 (Capability Level) ────┬── Core/Supporting/Generic: 正式分類（投資判断）
        │                  └── 事業判断：どの能力を内製/外注か   【Theme】
        ↓ 1:N
CL3 (Business Operation) ──┬── 分類なし（網羅性が目的）
                           └── 運用判断：業務をどう実行するか   【Epic/Feature】

                           【Phase 4: アプリケーション設計】
Service Boundary ──────────┬── サービス境界分析（CL2→Service対応）
        │                  └── Context Map（BC間関係、統合パターン）
        ↓ N:M

                           【Phase 5: ソフトウェア設計】
BC (Bounded Context) ──────┬── 分類継承（親CL2から）
        │                  └── 内容：Domain Model(SSOT) + DB + API
        ↓ 1:N
Actor UseCase ─────────────┬── 分類なし（BC内の実装単位）
        │                  └── ★シングルアクター原則            【User Story】
        ↓ 1:N
View ──────────────────────┬── 分類なし
                           └── 画面実装                          【Task】
```

## DDD対応表

| Parasol | DDD概念 | Phase | Agile対応 | Core/Supporting/Generic | 責任者 |
|---------|---------|-------|-----------|------------------------|--------|
| CL1 (Value Stream) | ≈ Problem Space全体 | 2-3 | Initiative | 傾向的（参考） | 経営層 |
| CL2 (Capability) | ≈ **Subdomain** | 3 | Theme | **正式分類** | 事業部長 |
| CL3 (Business Operation) | ≈ Domain Model詳細 | 3 | **Epic/Feature** | なし | 業務担当者 |
| Service Boundary | ≈ Service分割 | **4** | - | - | アーキテクト |
| Context Map | = Context Map | **4** | - | - | アーキテクト |
| BC | = Bounded Context | 5 | - | 継承 | 開発チーム |
| Actor UseCase | ≈ UseCase | 5 | **User Story** | なし | 開発チーム |
| View | ≈ Presentation | 5-6 | **Task** | なし | 開発者 |

---

## CL1: Value Stream Level（価値ストリーム層）

### 定義

```yaml
CL1:
  name: "Value Stream Level"
  japanese: "価値ストリーム層"
  purpose: "企業の主要な価値創出の流れを識別・分類する"
  granularity: "企業全体を3-7個のValue Streamに分解"
  owner: "経営層 / 事業戦略責任者"
  ddd_mapping: "Problem Space全体（Domainより広い概念）"
```

### Core/Supporting/Generic分類

**CL1での分類は「傾向的分類」（参考情報）**

```yaml
classification:
  purpose: "投資方向性の初期判断"
  binding: false  # 拘束力なし
  inheritance: false  # CL2に継承されない

  criteria:
    Core:
      definition: "競争優位の源泉となるValue Stream"
      investment: "重点投資"
    Supporting:
      definition: "Coreを支える必要不可欠なValue Stream"
      investment: "適正投資"
    Generic:
      definition: "業界共通の標準的なValue Stream"
      investment: "効率化重視"
```

### 重要な設計判断

> **CL1の分類はCL2に継承されない**
>
> Generic VS内にもCore Capabilityが存在しうる。
> 例：人事VS（Generic）の「タレント分析」が差別化要因の企業

### 成果物

- Value Stream一覧（VS0-VS7）
- 各VSの傾向的分類
- 投資優先度の方向性

---

## CL2: Capability Level（ケイパビリティ層）

### 定義

```yaml
CL2:
  name: "Capability Level"
  japanese: "ケイパビリティ層"
  purpose: "各Value Stream内の主要なビジネス能力を識別・分類する"
  granularity: "1つのVSを3-7個のCapabilityに分解"
  owner: "事業部門長 / ドメインエキスパート"
  ddd_mapping: "Subdomain（DDDの標準的概念）"
```

### Core/Supporting/Generic分類

**CL2での分類が「正式分類」（投資判断の根拠）**

```yaml
classification:
  purpose: "投資判断・内製/外注の決定"
  binding: true  # 拘束力あり
  inheritance: false  # CL1から継承しない（独立評価）

  criteria:
    Core:
      definition: "当該VS内で差別化の核となるCapability"
      characteristics:
        - "VS目標達成に最も重要"
        - "独自のノウハウ・ロジックを含む"
        - "専用マイクロサービス候補"
      decision: "内製・高投資"

    Supporting:
      definition: "Coreを支援する必須Capability"
      characteristics:
        - "Coreの品質・効率に影響"
        - "標準的だが調整が必要"
        - "共有サービスまたは専用"
      decision: "内製または戦略的外注"

    Generic:
      definition: "VS内で標準化されたCapability"
      characteristics:
        - "業界標準の処理"
        - "差別化に寄与しない"
        - "既存サービス活用推奨"
      decision: "外注・SaaS活用"
```

### CL1との独立性

```yaml
independence:
  rule: "CL2の分類はCL1から継承されない"
  reason: "各Capabilityは個別に評価すべき"

  example:
    vs: "人事VS（CL1でGeneric）"
    capabilities:
      - name: "給与計算"
        classification: "Generic"  # 標準処理
      - name: "勤怠管理"
        classification: "Generic"  # 標準処理
      - name: "タレント分析"
        classification: "Core"     # 差別化要因！
```

### 成果物

- Capability一覧（VS毎に3-7個）
- 各Capabilityの正式分類
- サービス境界の候補
- 投資配分計画

---

## CL3: Operation Level（オペレーション層）

### 定義

```yaml
CL3:
  name: "Operation Level"
  japanese: "オペレーション層"
  purpose: "各Capabilityの具体的な業務オペレーションを詳細化する"
  granularity: "1つのCapabilityを3-10個のOperationに分解"
  owner: "業務担当者 / プロセスオーナー"
  ddd_mapping: "Domain Model詳細（UseCase/Scenario相当）"
```

### 分類

**CL3では分類を行わない**

```yaml
classification:
  enabled: false
  reason: "CL3は詳細化のための層であり、分類ではなく網羅性が重要"
```

### 構造

```yaml
operation:
  attributes:
    - name: "操作名（動詞+目的語）"
    - trigger: "開始条件"
    - inputs: "必要な入力データ"
    - outputs: "生成される出力"
    - business_rules: "適用されるビジネスルール"
    - actors: "実行者（人/システム）"
    - frequency: "実行頻度"
    - exceptions: "例外・エラーケース"
```

### 成果物

- Business Operation一覧（Capability毎）
- 業務フロー図
- ビジネスルール一覧
- データ要件

---

## Actor UseCase: アクターユースケース層

### 定義

```yaml
Actor UseCase:
  name: "Actor UseCase"
  japanese: "アクターユースケース"
  purpose: "単一アクターの完結した操作を定義する"
  granularity: "1つのBusiness Operationを1-5個のActor UseCaseに分解"
  owner: "開発チーム / プロダクトオーナー"
  ddd_mapping: "UseCase（アプリケーション層の単位）"
  agile_mapping: "User Story（INVEST原則に準拠）"
```

### シングルアクター原則

**Actor UseCaseは必ず単一のアクターが実行する**

```yaml
single_actor_principle:
  rule: "1つのActor UseCase = 1人のアクターの完結操作"
  reason: "Agile User Storyとの整合性（As a [single role], I want...）"

  characteristics:
    - "単一のアクターが開始から終了まで責任を持つ"
    - "他のアクターの介入なしに完結する"
    - "明確な開始条件と終了条件を持つ"
    - "独立してテスト可能"

  example:
    good:
      - "研究員が酵母株を登録する"
      - "品質管理者が発酵条件を承認する"
      - "管理者がレポートを出力する"
    bad:
      - "研究員が登録し、管理者が承認する"  # 2アクター → Business Operation
```

### Agile User Storyとの対応

```yaml
agile_correspondence:
  format: "As a [Actor], I want [Goal] so that [Benefit]"

  invest_principle:
    I: "Independent - 他のストーリーから独立"
    N: "Negotiable - 詳細は交渉可能"
    V: "Valuable - ユーザーに価値を提供"
    E: "Estimable - 見積もり可能"
    S: "Small - 1スプリントで完了可能"
    T: "Testable - テスト可能"

  example:
    actor_usecase: "研究員が新しい酵母株を登録する"
    user_story: |
      As a 研究員,
      I want to 新しい酵母株を登録する
      so that 発酵実験で使用できるようになる

    acceptance_criteria:
      - "株コードが自動生成される"
      - "必須項目が入力されている"
      - "登録完了メッセージが表示される"
```

### Business OperationとActor UseCaseの関係

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CL3: Business Operation（複数アクター協調）≈ Epic/Feature                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                              │
│  例: 「酵母株スクリーニング」Business Operation                              │
│      └─ 研究員、品質管理者、管理者が協調して実行                             │
│                                                                              │
│         ┌──────────────────────────────────────────────────────────┐        │
│         │                    分解                                   │        │
│         └──────────────────────────────────────────────────────────┘        │
│                                    │                                         │
│                                    ▼                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Actor UseCase（シングルアクター）≈ User Story                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │ 研究員が        │  │ 品質管理者が    │  │ 管理者が        │              │
│  │ 酵母株を登録する │  │ 株を評価する    │  │ レポートを出力  │              │
│  │ (User Story 1)  │  │ (User Story 2)  │  │ (User Story 3)  │              │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              │
│           │                    │                    │                        │
│           ▼                    ▼                    ▼                        │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │  View（画面・タスク）                                            │        │
│  │  ・株登録フォーム  ・評価入力画面  ・レポート出力画面            │        │
│  └─────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 成果物

- Actor UseCase一覧（Business Operation毎）
- User Story形式の要件定義
- 受け入れ基準（Acceptance Criteria）
- 画面遷移図

---

## BC: Bounded Context（境界づけられたコンテキスト）

### 定義

```yaml
BC:
  name: "Bounded Context"
  japanese: "境界づけられたコンテキスト"
  purpose: "DDDに基づく実装境界とユビキタス言語の範囲を定義する"
  granularity: "1-3 Capabilityをまとめた実装単位"
  owner: "アーキテクト / テックリード"
  ddd_mapping: "Bounded Context（DDDの標準的概念）"
```

### 分類

**BCは親CL2の分類を継承**

```yaml
classification:
  enabled: false  # 新規分類は行わない
  inheritance: true  # 親CL2から継承

  rule: "BCが属するCapabilityの分類を参照"
  usage: "投資判断・技術選定の参考"
```

### Capabilityとの対応関係

```yaml
relationship:
  type: "N:1（複数Capabilityが1つのBCを形成可能）"
  criteria:
    cohesion: "内部の凝集度が高い"
    coupling: "外部との結合度が低い"
    autonomy: "独立してデプロイ可能"
    language: "統一された用語体系"
```

### BC内容物（設計単位としてのBC）

**BCはParasolドメインモデルを管理する単位**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BC: fermentation-research-bc                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                              │
│  fermentation-research-bc/                                                   │
│  ├── domain-language.md      ← ドメインモデル（SSOT: Single Source of Truth）│
│  │   └── エンティティ、値オブジェクト、ドメインイベント、用語定義            │
│  │                                                                           │
│  ├── api-specification.md    ← API仕様                                       │
│  │   └── エンドポイント、リクエスト/レスポンス、認証・認可                   │
│  │                                                                           │
│  ├── database-design.md      ← データベース設計                              │
│  │   └── テーブル定義、リレーション、インデックス                            │
│  │                                                                           │
│  └── operations/             ← Actor UseCase実装                             │
│      ├── register-yeast-strain.md                                            │
│      ├── evaluate-strain.md                                                  │
│      └── export-report.md                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### BC内容物の詳細

```yaml
bc_contents:
  domain_language:
    file: "domain-language.md"
    purpose: "ドメインモデルの単一真実源（SSOT）"
    includes:
      - "エンティティ定義（属性、ライフサイクル）"
      - "値オブジェクト（不変、等価性）"
      - "ドメインイベント（状態遷移トリガー）"
      - "ユビキタス言語辞書"
      - "ビジネスルール"
    inheritance: "operations/内のファイルはdomain-languageを参照"

  api_specification:
    file: "api-specification.md"
    purpose: "外部とのインターフェース定義"
    includes:
      - "RESTエンドポイント"
      - "リクエスト/レスポンススキーマ"
      - "認証・認可要件"
      - "エラーハンドリング"

  database_design:
    file: "database-design.md"
    purpose: "永続化層の設計"
    includes:
      - "テーブル定義"
      - "リレーション（FK、インデックス）"
      - "データ型マッピング"
      - "マイグレーション戦略"

  operations:
    directory: "operations/"
    purpose: "Actor UseCaseの実装詳細"
    includes:
      - "各Actor UseCaseのAPI実装"
      - "バリデーションルール"
      - "ワークフロー定義"
```

### 成果物

- Bounded Context一覧
- Context Map
- ユビキタス言語辞書（domain-language.md）
- API仕様書（api-specification.md）
- データベース設計書（database-design.md）
- Actor UseCase実装（operations/）

---

## 階層間の関係性

### 分解フロー図（Agile対応付き）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Phase 2: Value Streams                                │
│                                                                              │
│    VS0 ─── VS1 ─── VS2 ─── VS3 ─── VS4 ─── VS5 ─── VS6 ─── VS7             │
│    経営    研究    商品    原材料   製造    物流    マーケ   販売            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CL1: 活動領域識別 ≈ Problem Space（問題領域）        【Agile: Initiative】  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  目的: 「何を解決すべきか」の全体像把握・経営層向け                           │
│  分類: 傾向的（参考情報）※ CL2に継承されない                                 │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                        │
│  │ Core傾向     │  │ Supporting   │  │ Generic傾向  │                        │
│  │ VS2 商品開発 │  │ 傾向         │  │ VS0 経営     │                        │
│  │ VS4 製造     │  │ VS3, VS5, VS6│  │              │                        │
│  └──────────────┘  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CL2: ケイパビリティ設計 ≈ Subdomain（サブドメイン）     【Agile: Theme】    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  目的: 「どう分割して取り組むか」の決定・事業部長向け                         │
│  分類: ★正式分類（投資判断の根拠）                                          │
│  ※ CL1がGenericでもCL2でCoreになりうる（個別評価）                           │
│                                                                              │
│  VS2（商品開発）の分解例:                                                    │
│  ┌────────────────────┬────────────────────┬────────────────────┐           │
│  │ Core（70%投資）    │ Supporting（25%）  │ Generic（5%）      │           │
│  │ ・発酵研究         │ ・官能評価         │ ・開発プロジェクト │           │
│  │ ・素材研究         │ ・試作生産         │   管理             │           │
│  │ ・プレミアム開発   │                    │                    │           │
│  └────────────────────┴────────────────────┴────────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CL3: Business Operation ≈ Domain Model詳細          【Agile: Epic/Feature】│
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  目的: 「具体的に何をするか」の詳細化・業務担当者向け     【Phase 3】        │
│  分類: なし（網羅性が目的）                                                  │
│  特徴: 複数アクターが協調して実行                                            │
│                                                                              │
│  「発酵研究」ケイパビリティの分解例:                                         │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │ ・酵母株スクリーニング    ・発酵条件最適化                       │        │
│  │ ・菌株保存管理            ・発酵実験実施                         │        │
│  │ ・育種・選抜              ・技術知見体系化                       │        │
│  └─────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Service Boundary Analysis + Context Map                     【Phase 4】    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  目的: アプリケーションアーキテクチャの設計・アーキテクト向け                 │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │  1. サービス境界分析                                            │        │
│  │     └─ CL2 Capability → Service への対応決定                    │        │
│  │     └─ 複数CL2を1サービスにまとめる/分離する判断               │        │
│  │                                                                 │        │
│  │  2. Context Map作成                                             │        │
│  │     └─ BC間の関係定義（Customer-Supplier, Partnership等）       │        │
│  │     └─ 統合パターン選択（ACL, Open Host等）                     │        │
│  │                                                                 │        │
│  │  3. 統合方式決定                                                │        │
│  │     └─ 同期/非同期、REST/gRPC/イベント等                       │        │
│  └─────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│  成果物:                                                                     │
│  ├── service-boundaries.md     ← サービス境界定義                           │
│  ├── context-map.md            ← BC間関係図                                 │
│  └── integration-patterns.md   ← 統合パターン                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  BC: Bounded Context = Solution Space（解決領域）の境界      【Phase 5】    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  目的: 「どう実装するか」の技術的境界定義・開発者向け                         │
│  分類: CL2から継承                                                           │
│  内容: Domain Model（SSOT）+ DB設計 + API仕様 + Actor UseCase                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │  fermentation-research-bc/                                      │        │
│  │  ├── domain-language.md   ← ドメインモデル（SSOT）              │        │
│  │  ├── api-specification.md ← API仕様                             │        │
│  │  ├── database-design.md   ← DB設計                              │        │
│  │  └── operations/          ← Actor UseCase実装                   │        │
│  │      ├── register-yeast-strain/                                 │        │
│  │      │   ├── actor-usecase.md   ← シングルアクター定義          │        │
│  │      │   └── views/             ← 画面定義                      │        │
│  │      └── evaluate-strain/                                       │        │
│  └─────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Actor UseCase ≈ UseCase（BC内部の実装単位）             【Agile: User Story】│
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  目的: シングルアクターの完結操作を定義                       【Phase 5】    │
│  特徴: ★単一アクター原則（INVEST準拠）                                      │
│  形式: "As a [Actor], I want [Goal] so that [Benefit]"                       │
│                                                                              │
│  「酵母株スクリーニング」Business Operationの分解例:                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │ 研究員が        │  │ 品質管理者が    │  │ 管理者が        │              │
│  │ 酵母株を登録する │  │ 株を評価する    │  │ レポートを出力  │              │
│  │ (User Story 1)  │  │ (User Story 2)  │  │ (User Story 3)  │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  View ≈ Presentation                                    【Agile: Task】     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  目的: 画面・UIの実装                                        【Phase 5/6】  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │ ・株登録フォーム  ・評価入力画面  ・レポート出力画面            │        │
│  └─────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 分類継承ルール

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          分類の継承関係                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   CL1（傾向的）──╳──▶ CL2（正式）   ※継承しない！個別評価                   │
│                                                                              │
│   CL2（正式）  ──────▶ BC           ※継承する（投資判断に直結）             │
│                                                                              │
│   CL3          ──────▶ なし         ※分類なし（網羅性が目的）               │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  例: Generic傾向のVS0（経営管理）                                            │
│                                                                              │
│  CL1: VS0 = Generic傾向（参考）                                              │
│         │                                                                    │
│         ▼                                                                    │
│  CL2: ├─ 戦略策定 = Core（差別化要因なら）★個別評価                         │
│       ├─ 予算管理 = Supporting                                               │
│       └─ 総務     = Generic                                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 関係性の詳細

| 関係 | 対応 | Phase | 分類継承 | Agile対応 | 目的 |
|------|------|-------|---------|-----------|------|
| CL1→CL2 | 1:N（1 VS = 3-7 Capabilities） | 3 | **継承しない** | Initiative→Theme | 投資判断の精緻化 |
| CL2→CL3 | 1:N（1 Capability = 3-10 Operations） | 3 | なし | Theme→Epic/Feature | 業務詳細の網羅 |
| CL2→Service Boundary | N:M（複数CL2を1サービスに） | **4** | - | - | サービス境界決定 |
| Service→Context Map | 1:N（各サービス間の関係定義） | **4** | - | - | 統合パターン決定 |
| CL3→BC | N:M（複数Operationが複数BCに） | 4→5 | CL2から継承 | - | 実装境界の決定 |
| BC→Actor UseCase | 1:N（1 BC = N Actor UseCases） | 5 | なし | →**User Story** | シングルアクター分解 |
| Actor UseCase→View | 1:N（1 UseCase = 1-3 Views） | 5-6 | なし | User Story→**Task** | 画面実装 |

### 各層の決定ポイント

| 層 | 問い | Phase | Agile対応 | 判断者 |
|----|------|-------|-----------|--------|
| CL1 | どのValue Streamに投資するか？ | 2-3 | Initiative | 経営層 |
| CL2 | どのCapabilityを内製/外注するか？ | 3 | Theme | 事業部長 |
| CL3 | 業務をどう実行するか？ | 3 | Epic/Feature | 業務担当者 |
| Service Boundary | どのCL2をどのサービスにまとめるか？ | **4** | - | アーキテクト |
| Context Map | サービス間をどう連携するか？ | **4** | - | アーキテクト |
| BC | システムをどう分割するか？ | 5 | - | 開発チーム |
| Actor UseCase | 誰が何をするか？（シングルアクター） | 5 | **User Story** | 開発チーム |
| View | どの画面で実現するか？ | 5-6 | Task | 開発者 |

---

## 解消された矛盾

### 矛盾1: CL1での分類がCL2に継承されていた

**問題**: VS全体をCoreと分類すると、全Capabilityが自動的にCoreになる

**解決**: CL1の分類は「傾向」、CL2で独立評価

### 矛盾2: CL3に分類を適用すべきか曖昧

**問題**: 一部の文書でCL3にもCore/Supporting/Generic分類を示唆

**解決**: CL3は分類なし（網羅性が目的）

### 矛盾3: BCの分類方法が不明確

**問題**: BCに独自の分類を設けるか、継承するか

**解決**: 親CL2の分類を継承（二重分類は混乱の原因）

### 矛盾4: CapabilityとBCの対応関係

**問題**: 1:1なのかN:1なのか

**解決**: N:1（複数Capabilityが1つのBCを形成可能）

---

## VS→Capability→Service→BCマッピング

### マッピング概念図

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VS → Capability → Service → BC マッピング                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  【Phase 2-3】              【Phase 4】              【Phase 5】             │
│   ビジネス設計               アプリケーション設計      ソフトウェア設計       │
│                                                                              │
│   VS0 ──┬── Cap-A ─────┐                                                    │
│         │              ├──→ Service-1 ──┬──→ BC-1                          │
│         └── Cap-B ─────┘                │                                   │
│                                         └──→ BC-2                          │
│   VS1 ──┬── Cap-C ─────────→ Service-2 ────→ BC-3                          │
│         │                                                                    │
│         └── Cap-D ─────┐                                                    │
│                        ├──→ Service-3 ────→ BC-4                           │
│   VS2 ──┬── Cap-E ─────┘                                                    │
│         │                                                                    │
│         └── Cap-F ─────────→ Service-4 ──┬──→ BC-5                          │
│                                          └──→ BC-6                          │
│                                                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                              │
│  対応パターン:                                                               │
│  ・VS : Capability = 1 : N （1つのVSに複数のCapability）                    │
│  ・Capability : Service = N : M （複数Capabilityが1サービス、または分離）   │
│  ・Service : BC = 1 : N （1サービスに複数BC、または1:1）                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### マッピングテーブル（成果物テンプレート）

以下のテンプレートを使用して、VS→Capability→Service→BCの対応を管理します。

```markdown
# VS-Capability-Service-BC マッピング表

## Phase 2-3: VS → Capability対応

| VS ID | VS名 | CL2分類 | Capability ID | Capability名 | 正式分類 |
|-------|------|---------|---------------|--------------|----------|
| VS0 | 経営管理 | Generic傾向 | CAP-0-1 | 戦略策定 | Core |
| VS0 | 経営管理 | Generic傾向 | CAP-0-2 | 予算管理 | Supporting |
| VS2 | 商品開発 | Core傾向 | CAP-2-1 | 発酵研究 | Core |
| VS2 | 商品開発 | Core傾向 | CAP-2-2 | 官能評価 | Supporting |
| VS2 | 商品開発 | Core傾向 | CAP-2-3 | 試作生産 | Supporting |

## Phase 4: Capability → Service対応

| Service ID | Service名 | 含まれるCapability | サービス境界の理由 |
|------------|-----------|-------------------|-------------------|
| SVC-1 | fermentation-service | CAP-2-1, CAP-2-3 | 発酵プロセスの凝集性 |
| SVC-2 | quality-service | CAP-2-2 | 品質管理の独立性 |
| SVC-3 | strategy-service | CAP-0-1, CAP-0-2 | 経営情報の統合管理 |

## Phase 4: Service間関係（Context Map）

| 上流Service | 下流Service | 統合パターン | 通信方式 | 理由 |
|-------------|-------------|-------------|----------|------|
| fermentation-service | quality-service | Customer-Supplier | REST | 品質評価に発酵データが必要 |
| strategy-service | fermentation-service | Conformist | Event | 戦略変更時の通知 |

## Phase 5: Service → BC対応

| Service ID | BC ID | BC名 | 含まれるCL3 | ドメインモデル |
|------------|-------|------|------------|---------------|
| SVC-1 | BC-1-1 | fermentation-research-bc | 酵母株スクリーニング, 発酵条件最適化 | YeastStrain, FermentationCondition |
| SVC-1 | BC-1-2 | production-trial-bc | 試作生産管理 | TrialBatch, ProductionOrder |
| SVC-2 | BC-2-1 | sensory-evaluation-bc | 官能評価実施, 評価基準管理 | EvaluationSession, SensoryProfile |
```

### マッピング作成ガイド

#### Phase 3終了時（CL3完了後）

```yaml
作成物:
  - VS → Capability対応表
  - 各Capabilityの正式分類（Core/Supporting/Generic）
  - CL3 Business Operation一覧

チェックポイント:
  - 全VSがCapabilityに分解されているか
  - 正式分類が投資方針と整合しているか
  - CL3が業務を網羅しているか
```

#### Phase 4終了時（Service Boundary決定後）

```yaml
作成物:
  - Capability → Service対応表
  - Context Map（Service間関係）
  - 統合パターン決定表

チェックポイント:
  - サービス境界の理由が明確か
  - Core Capabilityが適切に保護されているか
  - 統合パターンが保守性を考慮しているか
```

#### Phase 5終了時（BC設計完了後）

```yaml
作成物:
  - Service → BC対応表
  - 各BCの成果物（domain-language, api, database）
  - Actor UseCase一覧

チェックポイント:
  - BCがCL3を適切にカバーしているか
  - ドメインモデルがSSoTになっているか
  - Actor UseCaseがシングルアクター原則に従っているか
```

### トレーサビリティの検証

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        トレーサビリティ検証                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  検証1: 価値からの追跡（Top-Down）                                          │
│  ───────────────────────────────────────                                    │
│  VL1 → VL2 → VL3 → VS → Capability → Service → BC → Actor UseCase          │
│                                                                              │
│  質問: 「この機能はどの価値に貢献しているか？」                              │
│  → Actor UseCaseからVL1まで遡れること                                       │
│                                                                              │
│  検証2: 実装からの追跡（Bottom-Up）                                         │
│  ───────────────────────────────────────                                    │
│  Actor UseCase → BC → Service → Capability → VS → VL3 → VL2 → VL1          │
│                                                                              │
│  質問: 「このAPIは何のために存在するか？」                                  │
│  → APIからVL1まで遡れること                                                 │
│                                                                              │
│  検証3: 投資判断との整合                                                    │
│  ───────────────────────────────────────                                    │
│  CL2正式分類 → Service投資配分 → BC実装優先度                               │
│                                                                              │
│  質問: 「Core Capabilityに十分な投資がされているか？」                      │
│  → Core分類のCapabilityを含むServiceに70%の投資                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agile対応サマリー

### Parasol階層とAgile階層の対応

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Parasol ←→ Agile 対応表                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Parasol階層              Agile階層           特徴                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│  CL1 (Value Stream)   →   Initiative         戦略的方向性                    │
│  CL2 (Capability)     →   Theme              投資判断の単位                  │
│  CL3 (Business Op.)   →   Epic/Feature       複数アクター協調                │
│  Actor UseCase        →   User Story ★      シングルアクター（INVEST）       │
│  View                 →   Task               実装タスク                       │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  ★ シングルアクター原則                                                      │
│                                                                              │
│  User Story形式: "As a [単一のActor], I want [Goal] so that [Benefit]"       │
│                                                                              │
│  INVEST原則:                                                                 │
│  ・Independent  - 他のストーリーから独立                                     │
│  ・Negotiable   - 詳細は交渉可能                                             │
│  ・Valuable     - ユーザーに価値を提供                                       │
│  ・Estimable    - 見積もり可能                                               │
│  ・Small        - 1スプリントで完了可能                                      │
│  ・Testable     - テスト可能                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### なぜシングルアクターが重要か

```yaml
single_actor_importance:
  agile_alignment:
    - "User Storyは単一ロールの視点で書く"
    - "複数アクターが混在すると見積もりが困難"
    - "受け入れ基準が曖昧になる"

  design_benefit:
    - "責任の所在が明確"
    - "テストが書きやすい"
    - "UIの設計単位と一致"

  implementation_benefit:
    - "1つのActor UseCaseが1つのAPIエンドポイントに対応"
    - "認可設計がシンプル"
    - "進捗管理が容易"
```

---

## 関連ドキュメント

- [ZIGZAG Process](./zigzag-process.md) - WHATとHOWの交互展開
- [Business Operations](./../_software-design-reference/business-operations.md) - Business OperationとActor UseCaseの詳細
- [3-capabilities](../commands/3-capabilities.md) - Phase 3コマンド
- [4-application-design](../commands/4-application-design.md) - Phase 4コマンド
- [5-software-design](../commands/5-software-design.md) - Phase 5コマンド（BC設計）
