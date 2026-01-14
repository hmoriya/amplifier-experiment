# Parasol V5.6 仕様書

> **バージョン**: 5.6.0
> **ステータス**: Draft
> **作成日**: 2026-01-14
> **コードネーム**: 5W1H-Driven Value Architecture

---

## 1. エグゼクティブサマリー

### 1.1 V5.6のビジョン

Parasol V5.6は、BIZBOKのビジネスアーキテクチャ概念とParasolの価値駆動設計を統合する**5W1Hフレームワーク**を導入します。

```
【V5.6 コアコンセプト】

  5W1H要素        V5.6での表現
  ─────────────────────────────────────────────
  WHY (なぜ)   → Vision/Mission/Core Values
                 VL (Value Level) 階層

  WHAT (何を)  → 二面性の明示化
                 ├── 外向きWHAT: Value Component (VC)
                 └── 内向きWHAT: Capability

  HOW (どう)   → Business Operation (BO)
                 Bounded Context (BC)

  WHEN (いつ)  → Value Stage (VS0-VS7) 顧客状態
                 Operational Stage (OS) 運用段階

  WHO (誰が)   → Actor (実行者)
                 ステークホルダー分析

  WHERE (どこ) → Channel/Touchpoint
                 価値提供接点
```

### 1.2 主要イノベーション

| # | イノベーション | 概要 |
|---|---------------|------|
| 1 | **WHATの二面性** | 外向きWHAT（Value Component）と内向きWHAT（Capability）の明示的区別 |
| 2 | **Value Component (VC)** | 5つの価値構成要素カテゴリによる顧客視点の価値分析 |
| 3 | **Operational Stage (OS)** | バリューストリーム内の運用段階の正式導入 |
| 4 | **3軸価値分解** | ステークホルダー/時間/性質軸による多角的価値分析 |
| 5 | **ステージ依存TVDC** | Value Stageに応じた動的TVDC分類 |

### 1.3 V5.5からの変更点

| 変更種別 | V5.5 | V5.6 |
|---------|------|------|
| WHAT定義 | Capability中心 | **二面性（VC + Cap）を明示** |
| 価値分析 | VL階層のみ | VL + **VC構成分析** |
| ステージ概念 | VS（顧客状態）のみ | VS + **OS（運用段階）** |
| TVDC分類 | 静的分類 | **ステージ依存動的分類** |
| VC-Cap対応 | 暗黙的 | **明示的マッピング** |

---

## 2. 新概念定義

### 2.1 Value Component（価値構成要素）

#### 2.1.1 定義

**Value Component（価値構成要素）**: 顧客に提供する価値を構成する要素。顧客視点で「何を受け取るか」を記述する外向きWHAT。

#### 2.1.2 5つの基本要素

| ID | 要素 | 英語 | 定義 | 顧客の問い |
|----|------|------|------|-----------|
| **VC1** | 製品価値 | Product Value | 製品そのものが提供する価値 | 「何を買うのか」 |
| **VC2** | サービス価値 | Service Value | 利便性・アクセス性の価値 | 「どう手に入るか」 |
| **VC3** | 体験価値 | Experience Value | 購入・使用時の体験価値 | 「どう感じるか」 |
| **VC4** | 関係価値 | Relationship Value | ブランドとの関係性価値 | 「なぜ選び続けるか」 |
| **VC5** | 情報価値 | Information Value | 提供される情報の価値 | 「何を知れるか」 |

#### 2.1.3 VC構造（詳細）

```yaml
Value_Component:
  VC1_Product:
    VC1-1: 機能的価値（性能、品質、機能）
    VC1-2: 品質価値（安全、信頼性、耐久性）
    VC1-3: 多様性価値（選択肢、カスタマイズ）

  VC2_Service:
    VC2-1: アクセス価値（入手しやすさ、チャネル）
    VC2-2: 価格価値（価格妥当性、コスパ）
    VC2-3: 安定価値（安定供給、可用性）

  VC3_Experience:
    VC3-1: 購入体験（購買プロセス、接客）
    VC3-2: 使用体験（使い心地、感動）
    VC3-3: 所有体験（デザイン、満足感）

  VC4_Relationship:
    VC4-1: 信頼価値（ブランド信頼、安心感）
    VC4-2: 帰属価値（コミュニティ、所属感）
    VC4-3: 継続価値（ロイヤリティ、習慣）

  VC5_Information:
    VC5-1: 知識価値（製品知識、使い方）
    VC5-2: 発見価値（新商品、トレンド）
    VC5-3: 共有価値（口コミ、推奨）
```

### 2.2 Operational Stage（運用段階）

#### 2.2.1 定義

**Operational Stage（OS）**: バリューストリーム内の価値蓄積区切り。組織視点で「いつ価値が蓄積されるか」を記述するWHEN要素。

#### 2.2.2 VSとOSの区別

| 概念 | 定義 | 主語 | 視点 |
|------|------|------|------|
| **Value Stage (VS)** | 顧客の状態遷移（VS0-VS7） | 顧客 | Outside-In |
| **Operational Stage (OS)** | 組織の活動段階 | 組織 | Inside-Out |

#### 2.2.3 階層関係

```
VS (Value Stage)
│  顧客状態の遷移
│  VS0→VS1→VS2→VS3→VS4→VS5→VS6→VS7
│
└── VStr (Value Stream)
    │  価値提供の流れ（顧客セグメント別に1本）
    │
    └── OS (Operational Stage)
        │  各VSを支援する運用段階
        │
        └── Capability
            1ケイパビリティ = 1OS（ステージを跨がない）
```

#### 2.2.4 OS設計原則

```yaml
OS設計原則:
  価値蓄積単位: 各段階で価値が蓄積される
  ケイパビリティ境界: 1ケイパビリティが複数OSを跨がない
  判断ポイント: 意思決定や承認を明確にする
  測定ポイント: 進捗や品質を測定できる

  良いOS:
    - 価値が蓄積される区切り
    - 判断・意思決定ポイント
    - ステークホルダーとの接点

  悪いOS:
    - 単なるタスク（「システム入力」「書類作成」）
    - 担当者の切り替え（組織都合）
```

### 2.3 3軸価値分解

#### 2.3.1 概要

WHY（価値）からWHAT（何を）への分解に3つの軸を適用：

```
         WHY（企業理念・価値）
              │
   ┌──────────┼──────────┐
   │          │          │
   ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐
│ステーク│  │時間軸 │  │価値の│
│ホルダー│  │      │  │性質軸│
│  軸   │  │      │  │      │
└──────┘  └──────┘  └──────┘
   │          │          │
   ▼          ▼          ▼
 誰への     いつの     どんな
 価値か     価値か     価値か
```

#### 2.3.2 軸1：ステークホルダー軸

| ステークホルダー | 提供価値の例 |
|----------------|-------------|
| **顧客** | 製品、サービス、体験、関係、情報 |
| **株主** | 収益、成長、配当、企業価値 |
| **従業員** | 報酬、成長機会、働きがい、安全 |
| **パートナー** | 取引機会、成長支援、関係性 |
| **社会** | 環境、地域、雇用、文化 |

#### 2.3.3 軸2：時間軸

| 時間区分 | 定義 | VS対応 |
|---------|------|--------|
| **現在価値** | 今、提供している価値 | VS0-VS7全体 |
| **将来価値** | これから提供する価値 | 主にVS0-VS2 |
| **持続価値** | 長期的に維持すべき価値 | 主にVS6-VS7 |

#### 2.3.4 軸3：価値性質軸

| 性質 | 定義 | 顧客の問い |
|------|------|-----------|
| **機能的価値** | 実用性、品質、性能 | 「何ができるか」 |
| **情緒的価値** | 体験、感動、安心 | 「どう感じるか」 |
| **社会的価値** | 所属、ステータス、貢献 | 「社会にどう見られるか」 |

### 2.4 ステージ依存TVDC

#### 2.4.1 概念

同一ケイパビリティでも、Value Stageによって競争優位への貢献度が変化する。

#### 2.4.2 仕様

```yaml
capability:
  id: "CL2-X-Y"
  name: "ケイパビリティ名"

  # デフォルトTVDC分類
  tvdc_default: "VCI"

  # ステージ依存オーバーライド
  stage_overrides:
    VS1_VS2:  # 認知→選好段階
      tvdc: "Core"
      rationale: "選好形成において競争優位を生む"

    VS4_VS7:  # 継続→推奨段階
      tvdc: "Supporting"
      rationale: "定着段階では差別化要因ではない"
```

#### 2.4.3 ステージ依存TVDCの例

| ケイパビリティ | デフォルト | VS1-VS2 | VS2-VS3 | VS4-VS7 |
|--------------|----------|---------|---------|---------|
| **ブランド管理** | Core | Core | Core | VCI |
| **店頭陳列設計** | VCI | Core | Core | VCI |
| **在庫管理** | Supporting | Supporting | VCI | Supporting |
| **製造管理** | VCI | Supporting | VCI | VCI |

---

## 3. WHATの二面性

### 3.1 概念図

```
┌─────────────────────────────────────────────────────────────┐
│                       WHAT = 問題領域                        │
├─────────────────────────────┬───────────────────────────────┤
│     外向きWHAT              │     内向きWHAT                │
│   (External WHAT)           │   (Internal WHAT)             │
├─────────────────────────────┼───────────────────────────────┤
│                             │                               │
│   Value Component (VC)      │   Capability                  │
│   「顧客に何を提供するか」   │   「自社に何ができるか」        │
│                             │                               │
│   ┌─────────────────────┐   │   ┌───────────────────────┐   │
│   │ VC1: 製品価値       │←──│──→│ 製品系: 開発、製造     │   │
│   │ VC2: サービス価値   │←──│──→│ 供給系: チャネル、在庫  │   │
│   │ VC3: 体験価値       │←──│──→│ 体験系: 店頭、UX設計    │   │
│   │ VC4: 関係価値       │←──│──→│ 関係系: ブランド、CRM   │   │
│   │ VC5: 情報価値       │←──│──→│ 情報系: マーケ、コンテンツ│  │
│   └─────────────────────┘   │   └───────────────────────┘   │
│                             │                               │
│   顧客視点・価値提案        │   組織視点・能力定義          │
└─────────────────────────────┴───────────────────────────────┘
```

### 3.2 VC-Capability対応マトリクス

各VL3（詳細価値）に対して、VC構成とそれを実現するCapabilityの対応を明示：

```yaml
vl3_vc_cap_mapping:
  vl3_id: "VL3-1-1"
  vl3_name: "発酵技術による味の革新"

  vc_composition:
    VC1_product:
      importance: "★★★"
      capabilities:
        - "CL2-1-1: レシピ開発"
        - "CL2-1-2: 発酵制御"

    VC2_service:
      importance: "★"
      capabilities:
        - "CL2-2-1: チャネル管理"

    VC3_experience:
      importance: "★★"
      capabilities:
        - "CL2-3-1: 店頭体験設計"

    VC4_relationship:
      importance: "★"
      capabilities:
        - "CL2-4-1: ブランド管理"

    VC5_information:
      importance: "★"
      capabilities:
        - "CL2-5-1: 製品情報管理"

  gap_analysis:
    VC3:
      gap: "体験設計能力が不足"
      action: "店頭体験設計ケイパビリティの強化"
```

---

## 4. VS-VC優先度マトリクス

### 4.1 概念

各Value Stage（顧客状態）で重要なValue Componentは異なる。

### 4.2 標準マトリクス

```
           │  VC1    │  VC2    │  VC3    │  VC4    │  VC5   │
           │ 製品    │サービス │  体験   │  関係   │  情報  │
───────────┼─────────┼─────────┼─────────┼─────────┼────────┤
VS0→VS1   │    ★    │    ★    │   ★★   │    ★    │  ★★★  │
(認知)     │         │         │         │         │        │
───────────┼─────────┼─────────┼─────────┼─────────┼────────┤
VS1→VS2   │  ★★★   │   ★★   │  ★★★   │   ★★   │  ★★★  │
(選好形成) │         │         │         │         │        │
───────────┼─────────┼─────────┼─────────┼─────────┼────────┤
VS2→VS3   │  ★★★   │  ★★★   │  ★★★   │    ★    │   ★★  │
(初回体験) │         │         │         │         │        │
───────────┼─────────┼─────────┼─────────┼─────────┼────────┤
VS3→VS4   │  ★★★   │  ★★★   │   ★★   │   ★★   │    ★   │
(継続利用) │         │         │         │         │        │
───────────┼─────────┼─────────┼─────────┼─────────┼────────┤
VS4→VS5   │   ★★   │   ★★   │   ★★   │  ★★★   │    ★   │
(定着)     │         │         │         │         │        │
───────────┼─────────┼─────────┼─────────┼─────────┼────────┤
VS5→VS6   │   ★★   │    ★    │   ★★   │  ★★★   │   ★★  │
(発展)     │         │         │         │         │        │
───────────┼─────────┼─────────┼─────────┼─────────┼────────┤
VS6→VS7   │    ★    │    ★    │  ★★★   │  ★★★   │  ★★★  │
(推奨)     │         │         │         │         │        │
───────────┴─────────┴─────────┴─────────┴─────────┴────────┘
```

### 4.3 活用指針

| VS段階 | 重点VC | 投資方針 |
|--------|--------|---------|
| VS0-VS2（認知〜選好） | VC5情報、VC3体験 | マーケティング投資 |
| VS2-VS4（初回〜継続） | VC1製品、VC2サービス | 製品・供給投資 |
| VS4-VS7（定着〜推奨） | VC4関係、VC3体験 | CRM・ブランド投資 |

---

## 5. Phase構成への影響

### 5.1 Phase別変更サマリー

| Phase | 変更規模 | 主な変更内容 |
|-------|---------|-------------|
| Phase 1 | 小 | ステークホルダー識別の追加 |
| Phase 2 | **大** | VC分析、3軸価値分解、Value Portfolio |
| Phase 3 | **大** | OS定義、ステージ依存TVDC、VC-Cap対応 |
| Phase 4 | 中 | OS-BC整合ガイダンス |
| Phase 5-7 | 小 | 上流メタデータの継承 |

### 5.2 Phase 2: 価値定義（V5.6拡張）

```yaml
Phase_2_V56:
  Step_2.1: VL定義（既存）
    - VL1 → VL2 → VL3の階層分解

  Step_2.2: VC分析（V5.6追加）
    - 各VL3のVC構成を分析
    - VC別重要度（★〜★★★）を設定
    - VC構成パターンの識別

  Step_2.3: 3軸価値分解（V5.6追加）
    - ステークホルダー別価値定義
    - 時間軸別価値定義（現在/将来/持続）
    - 性質別価値定義（機能/情緒/社会）

  Step_2.4: VS設計（既存）
    - VS0-VS7の顧客状態定義

  Step_2.5: VS-VC対応（V5.6追加）
    - 各VSで重要なVCを特定
    - VS-VCマトリクスの作成

  Step_2.6: Value Portfolio（V5.6追加）
    - 価値軸別投資配分比率の決定
    - 優先ステークホルダーの明確化

出力:
  - value-declaration.md（拡張版）
  - vl3-with-vc.yaml（各VL3のVC構成）
  - vs-vc-matrix.yaml（VS-VC優先度マトリクス）
  - value-portfolio.yaml（投資配分）
```

### 5.3 Phase 3: ケイパビリティ分解（V5.6拡張）

```yaml
Phase_3_V56:
  Step_3.1: CL1 Activity Area識別（既存）

  Step_3.2: CL2 Capability定義（拡張）
    - 既存定義に加えて:
    - value_component: 対応するVC
    - stage_overrides: ステージ依存TVDC

  Step_3.3: OS (Operational Stage) 定義（V5.6追加）
    - 各VStr内の運用段階を定義
    - OS-Capability対応を設定
    - 「1ケイパビリティ = 1OS」原則の検証

  Step_3.4: ステージ依存TVDC設定（V5.6追加）
    - デフォルトTVDC分類
    - VS別オーバーライド設定
    - 分類理由の記録

  Step_3.5: CL3 Sub-capability定義（既存）

  Step_3.6: VC-Cap対応マッピング（V5.6追加）
    - 各VCに対応するCapabilityの明示
    - ギャップ分析の実施
    - 強化すべきCapabilityの特定

出力:
  - capability-hierarchy.yaml（拡張版）
  - operational-stage.yaml（OS定義）
  - vc-cap-matrix.yaml（VC-Cap対応）
  - gap-analysis.md（ギャップ分析レポート）
```

### 5.4 Phase 4: アプリケーション設計（V5.6拡張）

```yaml
Phase_4_V56:
  OS-BC整合:
    - OSがBC境界の参考情報となる
    - 同一OS内のCapabilityは同一BCを検討
    - OS跨ぎのデータフローを識別

  TVDC基づく設計判断:
    - Core: 内製、カスタム開発優先
    - VCI: 品質投資、段階的改善
    - Supporting: 効率化、SaaS検討
    - Generic: SaaS/共通基盤活用
```

---

## 6. テンプレート仕様

### 6.1 VL3 with VC (vl3-with-vc.yaml)

```yaml
# VL3 価値要素定義（V5.6版）

value_element:
  id: "VL3-X-Y"
  name: "{価値要素名}"
  parent: "VL2-X"
  description: "{詳細説明}"

  # Value Component構成（V5.6追加）
  value_components:
    VC1_product:
      importance: "{★ | ★★ | ★★★}"
      description: "{製品価値の説明}"
      sub_components:
        - VC1-1: "{機能的価値の詳細}"
        - VC1-2: "{品質価値の詳細}"

    VC2_service:
      importance: "{★ | ★★ | ★★★}"
      description: "{サービス価値の説明}"

    VC3_experience:
      importance: "{★ | ★★ | ★★★}"
      description: "{体験価値の説明}"

    VC4_relationship:
      importance: "{★ | ★★ | ★★★}"
      description: "{関係価値の説明}"

    VC5_information:
      importance: "{★ | ★★ | ★★★}"
      description: "{情報価値の説明}"

  # VS別VC重要度
  vs_vc_priority:
    VS0_VS1: ["VC5", "VC3"]
    VS1_VS2: ["VC1", "VC3", "VC5"]
    VS2_VS3: ["VC1", "VC2", "VC3"]
    VS3_VS4: ["VC1", "VC2"]
    VS4_VS7: ["VC4", "VC3"]

  # Phase 3への引継ぎ
  capability_mapping:
    VC1: ["{対応Cap1}", "{対応Cap2}"]
    VC2: ["{対応Cap3}"]
    VC3: ["{対応Cap4}"]
    VC4: ["{対応Cap5}"]
    VC5: ["{対応Cap6}"]
```

### 6.2 Operational Stage (operational-stage.yaml)

```yaml
# Operational Stage定義（V5.6版）

operational_stage:
  value_stream: "{VStr ID}"
  value_stage: "{VS ID (例: VS2_VS3)}"

  stages:
    - id: "OS-1"
      name: "{運用段階名}"
      description: "{価値蓄積の説明}"

      # 設計原則適合
      value_accumulation: "{蓄積される価値}"
      decision_point: "{判断ポイント}"
      stakeholder_contact: "{ステークホルダー接点}"

      # Capability対応
      capability: "CL2-X-Y"

      # 入出力
      input: "{入力}"
      output: "{出力}"

    - id: "OS-2"
      name: "{次の運用段階名}"
      # ...

  # 検証
  validation:
    cap_stage_crossing: false  # ケイパビリティがステージを跨いでいないか
    value_accumulation_each: true  # 各ステージで価値蓄積があるか
```

### 6.3 CL2 Extended (cl2-extended.yaml)

```yaml
# CL2 Capability定義（V5.6拡張版）

capability:
  id: "CL2-X-Y"
  name: "{ケイパビリティ名}"
  parent: "CL1-X"
  description: "{説明}"

  # V5.6追加: Value Component対応
  value_component: "VC{1-5}"
  vc_contribution: "{VCへの貢献説明}"

  # V5.6追加: Operational Stage対応
  operational_stage: "OS-{N}"

  # デフォルトTVDC分類
  tvdc_default: "{Core | VCI | Supporting | Generic}"
  tvdc_rationale: "{分類理由}"

  # V5.6追加: ステージ依存TVDC
  stage_overrides:
    VS1_VS2:
      tvdc: "{Core | VCI | Supporting | Generic}"
      rationale: "{このステージでの分類理由}"

    VS4_VS7:
      tvdc: "{Core | VCI | Supporting | Generic}"
      rationale: "{このステージでの分類理由}"

  # 既存フィールド
  business_operations:
    - id: "BO-X-Y-1"
      name: "{BO名}"
```

### 6.4 Value Portfolio (value-portfolio.yaml)

```yaml
# Value Portfolio定義（V5.6新規）

value_portfolio:
  project_id: "{プロジェクトID}"

  # ステークホルダー別配分
  stakeholder_allocation:
    customer:
      priority: 1
      allocation_percent: 60
    shareholder:
      priority: 2
      allocation_percent: 20
    employee:
      priority: 3
      allocation_percent: 10
    society:
      priority: 4
      allocation_percent: 10

  # 時間軸別配分
  time_allocation:
    current_value:
      definition: "{現在価値の定義}"
      allocation_percent: 60
    future_value:
      definition: "{将来価値の定義}"
      allocation_percent: 25
    sustainable_value:
      definition: "{持続価値の定義}"
      allocation_percent: 15

  # 性質別配分
  nature_allocation:
    functional:
      definition: "{機能的価値}"
      allocation_percent: 50
    emotional:
      definition: "{情緒的価値}"
      allocation_percent: 30
    social:
      definition: "{社会的価値}"
      allocation_percent: 20
```

---

## 7. バリデーションルール

### 7.1 VC完全性バリデーション

```yaml
vc_completeness_rules:
  - rule: "VL3_VC_COVERAGE"
    description: "全VL3にVC構成が定義されていること"
    severity: "ERROR"

  - rule: "VC_IMPORTANCE_SET"
    description: "各VCに重要度（★〜★★★）が設定されていること"
    severity: "WARNING"

  - rule: "PRIMARY_VC_IDENTIFIED"
    description: "★★★のVCが1つ以上あること"
    severity: "WARNING"
```

### 7.2 OS-Capマッピングバリデーション

```yaml
os_cap_mapping_rules:
  - rule: "CAP_NO_STAGE_CROSSING"
    description: "1ケイパビリティが複数OSを跨がないこと"
    severity: "ERROR"

  - rule: "OS_VALUE_ACCUMULATION"
    description: "各OSで価値蓄積が定義されていること"
    severity: "WARNING"

  - rule: "OS_DECISION_POINT"
    description: "OSに判断ポイントが定義されていること"
    severity: "INFO"
```

### 7.3 ステージ依存TVDCバリデーション

```yaml
stage_tvdc_rules:
  - rule: "TVDC_DEFAULT_SET"
    description: "デフォルトTVDC分類が設定されていること"
    severity: "ERROR"

  - rule: "OVERRIDE_RATIONALE"
    description: "ステージオーバーライドに理由が記載されていること"
    severity: "WARNING"

  - rule: "VL3_TVDC_INHERITANCE"
    description: "VL3の価値必然性とTVDCが整合していること"
    severity: "WARNING"
```

---

## 8. 移行ガイド

### 8.1 V5.5からV5.6への移行ステップ

```
Step 1: 既存VL3へのVC分析追加
├── 各VL3に対してVC構成を分析
├── VC別重要度を設定
└── VC構成パターンを識別

Step 2: VS-VC対応の設定
├── 既存VSに対してVC重要度を設定
└── VS-VCマトリクスを作成

Step 3: OS (Operational Stage) の定義
├── 既存VStrをOS単位に分解
├── 「良いOS」の基準で検証
└── OS-Capability対応を設定

Step 4: ステージ依存TVDCの設定
├── 既存TVDC分類をデフォルトとして維持
├── 必要なステージオーバーライドを追加
└── 分類理由を記録

Step 5: VC-Cap対応の明示化
├── 各VCに対応するCapabilityをマッピング
├── ギャップ分析を実施
└── 強化すべきCapabilityを特定

Step 6: Value Portfolioの作成
├── ステークホルダー別配分を設定
├── 時間軸別配分を設定
└── 性質別配分を設定
```

### 8.2 互換性

| 項目 | 互換性 | 備考 |
|------|--------|------|
| VS0-VS7 | 完全互換 | 変更なし |
| VL1-VL3 | 完全互換 | メタデータ追加のみ |
| CL1-CL3 | 完全互換 | フィールド追加のみ |
| VMS | 完全互換 | 変更なし |
| TVDC | 拡張互換 | デフォルト値で動作 |

---

## 9. 用語集

| 用語 | 英語 | 定義 |
|------|------|------|
| **Value Component (VC)** | Value Component | 外向きWHAT。顧客に提供する価値の構成要素（5分類） |
| **Operational Stage (OS)** | Operational Stage | VStr内の運用段階。価値蓄積の区切り |
| **外向きWHAT** | External WHAT | 顧客視点での「何を提供するか」 |
| **内向きWHAT** | Internal WHAT | 組織視点での「何ができるか」（Capability） |
| **ステージ依存TVDC** | Stage-dependent TVDC | VSによって変化するTVDC分類 |
| **3軸価値分解** | Value Decomposition Directions | ステークホルダー/時間/性質軸による価値分析 |
| **Value Portfolio** | Value Portfolio | 価値軸別の投資配分管理 |
| **VS-VCマトリクス** | VS-VC Matrix | 各VSで重要なVCを示すマトリクス |
| **VC-Cap対応** | VC-Cap Correspondence | VCとCapabilityの対応関係 |

---

## 10. 変更履歴

| 日付 | バージョン | 変更内容 |
|------|----------|---------|
| 2026-01-14 | 0.1 | 初版作成 |

---

## 付録A: 検討文書一覧

| 文書 | 内容 |
|------|------|
| `V56-BIZBOK-5W1H-FRAMEWORK.md` | 5W1Hフレームワークの原案とV5適用分析 |
| `V56-VALUE-DECOMPOSITION-DIRECTIONS.md` | 3軸価値分解フレームワーク |
| `V56-STAGE-VS-MAPPING.md` | VS/OS概念整理、Out→In原則 |
| `V56-CAPABILITY-TVDC-CLASSIFICATION.md` | TVDC分類の適用例 |
| `V56-VALUE-COMPONENT-FRAMEWORK.md` | VCフレームワーク詳細 |
| `V56-DEVELOPMENT-PLAN.md` | V5.6開発計画 |
| `V56-TASK-LIST.md` | タスク一覧（優先度・依存関係付き） |
