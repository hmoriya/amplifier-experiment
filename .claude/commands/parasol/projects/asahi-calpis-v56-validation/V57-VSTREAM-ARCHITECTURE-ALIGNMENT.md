# Parasol V5.7: 価値構造準拠バリューストリームアーキテクチャ

**Value Structure-Aligned Value Stream Architecture**

---

## 1. 核心原則: Conwayの法則の価値版

> **「企業の価値継承構造が、バリューストリームアーキテクチャを規定する」**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   組織構造 ─────► 価値継承構造 ─────► VStreamアーキテクチャ         │
│                                                                     │
│   Conway's Law:                                                     │
│   「システムを設計する組織は、その組織のコミュニケーション構造を     │
│    反映した設計を生み出す」                                         │
│                                                                     │
│   Parasol V5.7 価値版:                                              │
│   「VStreamを設計する組織は、その組織の価値継承構造を               │
│    反映したVStream設計を生み出す（べきである）」                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. VStreamアーキテクチャパターン

### 2.1 パターン分類

```
VStreamアーキテクチャパターン
══════════════════════════════

┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│  Pattern A: 分離型（Separated）                                   │
│  ─────────────────────────────                                    │
│                                                                   │
│       Brand A              Brand B              Brand C           │
│    ┌──────────┐         ┌──────────┐         ┌──────────┐        │
│    │ VStr-A1  │         │ VStr-B1  │         │ VStr-C1  │        │
│    │ VStr-A2  │         │ VStr-B2  │         │ VStr-C2  │        │
│    │ VStr-A3  │         │ VStr-B3  │         │ VStr-C3  │        │
│    └──────────┘         └──────────┘         └──────────┘        │
│         ↓                    ↓                    ↓               │
│    独立Cap群             独立Cap群             独立Cap群           │
│                                                                   │
│  適用: コングロマリット型（事業間の顧客・価値が大きく異なる）     │
│                                                                   │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Pattern B: 統合型（Unified）                                     │
│  ─────────────────────────────                                    │
│                                                                   │
│              ┌─────────────────────────┐                         │
│              │     共通 VStream群       │                         │
│              │  ┌─────┐ ┌─────┐ ┌─────┐│                         │
│              │  │VStr1│ │VStr2│ │VStr3││                         │
│              │  └──┬──┘ └──┬──┘ └──┬──┘│                         │
│              └─────┼───────┼───────┼───┘                         │
│                    │       │       │                              │
│              ┌─────┴───────┴───────┴───┐                         │
│              │      共通Capability群    │                         │
│              └─────────────────────────┘                         │
│                    ↑       ↑       ↑                              │
│                 Brand A  Brand B  Brand C                         │
│                 (設定差分のみ)                                    │
│                                                                   │
│  適用: 単一ブランド集中型、高度に統合されたエコシステム           │
│                                                                   │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Pattern C: ハイブリッド型（Hybrid）                              │
│  ───────────────────────────────────                              │
│                                                                   │
│              ┌─────────────────────────┐                         │
│              │    共通 VStream 基盤    │                         │
│              │  ┌─────┐     ┌─────┐   │                         │
│              │  │認知 │     │購買 │   │  ← 共通                  │
│              │  │VStr │     │VStr │   │                         │
│              │  └──┬──┘     └──┬──┘   │                         │
│              └─────┼───────────┼──────┘                         │
│                    │           │                                  │
│       ┌────────────┼───────────┼────────────┐                    │
│       │            │           │            │                    │
│       ▼            ▼           ▼            ▼                    │
│   ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐                  │
│   │Brand │    │Brand │    │Brand │    │Brand │                  │
│   │固有   │    │固有   │    │固有   │    │固有   │                  │
│   │VStr  │    │VStr  │    │VStr  │    │VStr  │  ← 固有           │
│   └──────┘    └──────┘    └──────┘    └──────┘                  │
│                                                                   │
│  適用: マルチブランド型（共通基盤＋ブランド固有体験）             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 2.2 パターン選択基準

```yaml
pattern_selection_criteria:

  separated_pattern:
    when:
      - 顧客セグメントが完全に異なる
      - 価値提案が根本的に異なる
      - 購買行動・ジャーニーが異なる
      - 組織（OpCo/BU）が独立している
    examples:
      - アサヒビール vs アサヒ飲料
      - ソフトバンク通信 vs ビジョンファンド
    architecture:
      vstreams: 完全分離
      capabilities: 一部共有可（バックオフィス等）
      data: 分離（顧客IDは別）

  unified_pattern:
    when:
      - 単一ブランドで複数製品
      - 顧客は同一、製品ラインが異なる
      - エコシステム内で顧客が回遊
    examples:
      - Apple（iPhone/Mac/iPad共通体験）
      - Amazon（EC/Prime/AWS統合）
    architecture:
      vstreams: 統合（製品差分は設定）
      capabilities: 完全共有
      data: 統合（単一顧客ID）

  hybrid_pattern:
    when:
      - 同一OpCo内の複数ブランド
      - 基本ジャーニーは類似
      - ブランド固有の体験価値がある
    examples:
      - アサヒ飲料（カルピス/三ツ矢/ワンダ）
      - P&G（Tide/Pampers/Gillette）
    architecture:
      vstreams: 共通基盤＋ブランド固有
      capabilities: 基盤共有＋固有機能
      data: 統合基盤＋ブランド属性
```

---

## 3. アサヒグループでの適用

### 3.1 全体アーキテクチャ

```
アサヒグループ VStreamアーキテクチャ
════════════════════════════════════

                    アサヒグループHD
                    ┌────────────────┐
                    │ グループ共通基盤 │
                    │ ・ESG価値管理   │
                    │ ・コーポレート  │
                    │   ブランディング│
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ アサヒビール   │   │ アサヒ飲料    │   │アサヒグループ  │
│ (分離型)      │   │ (ハイブリッド) │   │食品(分離型)   │
│               │   │               │   │               │
│ ┌───────────┐ │   │ ┌───────────┐ │   │ ┌───────────┐ │
│ │ビール固有  │ │   │ │飲料共通基盤│ │   │ │食品固有   │ │
│ │VStream群  │ │   │ │VStream    │ │   │ │VStream群  │ │
│ └───────────┘ │   │ └─────┬─────┘ │   │ └───────────┘ │
│               │   │   ┌───┼───┐   │   │               │
│ 顧客:         │   │   │   │   │   │   │ 顧客:         │
│ 酒類消費者    │   │   ▼   ▼   ▼   │   │ 食品消費者    │
│               │   │ ┌─┐ ┌─┐ ┌─┐ │   │               │
│               │   │ │ｶ│ │三│ │ﾜ│ │   │               │
│               │   │ │ﾙ│ │ﾂ│ │ﾝ│ │   │               │
│               │   │ │ﾋﾟ│ │矢│ │ﾀﾞ│ │   │               │
│               │   │ │ｽ│ │ │ │ │ │   │               │
│               │   │ └─┘ └─┘ └─┘ │   │               │
│               │   │ Brand固有    │   │               │
│               │   │ VStream     │   │               │
└───────────────┘   └───────────────┘   └───────────────┘

        ↓                   ↓                   ↓
    完全分離            ハイブリッド          完全分離
    (顧客が異なる)      (基盤共有+固有)       (顧客が異なる)
```

### 3.2 アサヒ飲料のハイブリッドアーキテクチャ詳細

```
アサヒ飲料 VStreamアーキテクチャ（ハイブリッド型）
═══════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                        共通VStream基盤                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  VStr-Common-1: 認知・選好基盤                                      │
│  ──────────────────────────────                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ OS-C1-1: ブランド認知管理                                    │   │
│  │          → CL2-C1: メディアプランニング [共通]               │   │
│  │                                                              │   │
│  │ OS-C1-2: 販売チャネル管理                                    │   │
│  │          → CL2-C2: 流通・棚割管理 [共通]                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  VStr-Common-2: 購買・配荷基盤                                      │
│  ──────────────────────────────                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ OS-C2-1: 受注管理                                            │   │
│  │          → CL2-C3: 受注処理 [共通]                           │   │
│  │                                                              │   │
│  │ OS-C2-2: 物流管理                                            │   │
│  │          → CL2-C4: サプライチェーン [共通]                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                    │
                    │ 共通基盤を利用
                    │
    ┌───────────────┼───────────────┬───────────────┐
    │               │               │               │
    ▼               ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│カルピス  │   │三ツ矢    │   │ワンダ    │   │...      │
│固有VStr │   │固有VStr │   │固有VStr │   │         │
├─────────┤   ├─────────┤   ├─────────┤   │         │
│         │   │         │   │         │   │         │
│VStr-CP1 │   │VStr-MY1 │   │VStr-WD1 │   │         │
│健康価値 │   │爽快価値 │   │本格価値 │   │         │
│訴求     │   │訴求     │   │訴求     │   │         │
│         │   │         │   │         │   │         │
│VStr-CP2 │   │VStr-MY2 │   │VStr-WD2 │   │         │
│家族体験 │   │若者体験 │   │ビジネス │   │         │
│設計     │   │設計     │   │体験設計 │   │         │
│         │   │         │   │         │   │         │
│VStr-CP3 │   │VStr-MY3 │   │VStr-WD3 │   │         │
│ロイヤル │   │ファン   │   │習慣化   │   │         │
│ティ     │   │コミュニ │   │         │   │         │
│         │   │ティ     │   │         │   │         │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │               │               │
    │               │               │
    ▼               ▼               ▼
┌─────────────────────────────────────────────────────┐
│            Brand固有Capability                       │
├─────────────────────────────────────────────────────┤
│ カルピス:                                           │
│   CL2-CP1: 健康エビデンス管理                       │
│   CL2-CP2: 家族体験価値設計                         │
│   CL2-CP3: 希釈レシピ管理                           │
│                                                     │
│ 三ツ矢:                                             │
│   CL2-MY1: 爽快感訴求管理                           │
│   CL2-MY2: 若年層エンゲージメント                   │
│                                                     │
│ ワンダ:                                             │
│   CL2-WD1: コーヒー品質管理                         │
│   CL2-WD2: ビジネスシーン価値設計                   │
└─────────────────────────────────────────────────────┘
```

### 3.3 共有vs固有の判断基準

```yaml
sharing_decision_criteria:

  # 共通基盤に含めるべきVStream/Capability
  shared_components:
    criteria:
      - 全ブランドで同じ業務プロセス
      - 顧客接点ではない（バックオフィス）
      - 規模の経済が効く
      - 品質基準が統一されるべき

    examples:
      - 流通・物流管理
      - 受注処理
      - 品質管理基盤
      - メディアバイイング
      - 法務・コンプライアンス

  # Brand固有にすべきVStream/Capability
  brand_specific_components:
    criteria:
      - 顧客体験に直接影響
      - ブランド価値の差別化要素
      - ターゲットセグメント固有
      - 情緒的価値の表現

    examples:
      - 健康エビデンス訴求（カルピス固有）
      - 家族体験設計（カルピス固有）
      - 爽快感訴求（三ツ矢固有）
      - ビジネスシーン設計（ワンダ固有）

  # 判断フローチャート
  decision_flow: |
    Q1: この機能は顧客体験に直接影響するか？
        YES → Brand固有候補
        NO  → Q2へ

    Q2: この機能はブランド価値の差別化に関わるか？
        YES → Brand固有
        NO  → Q3へ

    Q3: この機能は全ブランドで同じプロセスで良いか？
        YES → 共通基盤
        NO  → Brand固有
```

---

## 4. Capability共有パターン

### 4.1 共有レベル分類

```
Capability共有レベル
════════════════════

Level 0: グループ共有（HD管轄）
─────────────────────────────
┌─────────────────────────────────────────────┐
│ 全OpCo/全Brandで共有                         │
│                                             │
│ ・コーポレートブランディング                 │
│ ・ESG/サステナビリティ管理                   │
│ ・グループIR                                │
│ ・グループ法務                              │
└─────────────────────────────────────────────┘
         │
         ▼
Level 1: OpCo共有（事業会社管轄）
─────────────────────────────────
┌─────────────────────────────────────────────┐
│ 同一OpCo内の全Brandで共有                    │
│                                             │
│ アサヒ飲料:                                 │
│ ・飲料製造管理                              │
│ ・飲料流通管理                              │
│ ・飲料品質基準管理                          │
│ ・飲料メディアプランニング                   │
└─────────────────────────────────────────────┘
         │
         ▼
Level 2: Brand固有（ブランド管轄）
─────────────────────────────────
┌─────────────────────────────────────────────┐
│ 各Brand専用                                  │
│                                             │
│ カルピス:                                   │
│ ・健康エビデンス管理                        │
│ ・家族体験価値設計                          │
│ ・乳酸菌研究管理                            │
│                                             │
│ 三ツ矢:                                     │
│ ・爽快感訴求管理                            │
│ ・若年層エンゲージメント                    │
└─────────────────────────────────────────────┘
```

### 4.2 共有と価値継承の関係

```
価値継承とCapability共有の対応
═════════════════════════════════

価値継承構造              Capability共有構造
────────────              ──────────────────

HD価値                    Level 0 Cap（グループ共有）
「健康で豊かな生活」      ・ESG価値管理
     │                    ・コーポレートブランド
     │ 継承                    │
     ▼                         │
OpCo価値                  Level 1 Cap（OpCo共有）
「飲料で健康と潤い」      ・飲料品質管理
     │                    ・飲料流通管理
     │ 継承                    │
     ▼                         │
Brand価値                 Level 2 Cap（Brand固有）
「発酵で健康と絆」        ・健康エビデンス管理
                          ・家族体験設計

ルール:
  継承される価値要素 → 上位で共有Cap
  追加される価値要素 → 当該レベルで固有Cap
```

---

## 5. VStreamアーキテクチャ設計プロセス

### 5.1 設計フロー

```
VStreamアーキテクチャ設計フロー
═══════════════════════════════

Step 1: 価値継承構造の確認
─────────────────────────
Input: Phase 0.5/Phase 1 の出力
       ・組織トポロジー
       ・バリエーションポイント
       ・価値継承チェーン

         │
         ▼

Step 2: アーキテクチャパターン選択
─────────────────────────────────
┌───────────────────────────────────────┐
│ 判断基準:                             │
│                                       │
│ Q1: OpCo間で顧客が完全に異なるか？    │
│     YES → OpCo間は分離型              │
│     NO  → OpCo間も統合検討            │
│                                       │
│ Q2: Brand間で顧客が完全に異なるか？   │
│     YES → Brand間は分離型             │
│     NO  → ハイブリッド型検討          │
│                                       │
│ Q3: 共通の購買チャネルがあるか？      │
│     YES → 共通VStream基盤必要         │
│     NO  → 分離可能                    │
└───────────────────────────────────────┘

         │
         ▼

Step 3: 共有/固有の切り分け
──────────────────────────
┌───────────────────────────────────────┐
│ 各VStream/Capabilityについて判断:     │
│                                       │
│ ・顧客体験影響 → Brand固有            │
│ ・差別化要素   → Brand固有            │
│ ・業務プロセス → 共通基盤候補         │
│ ・バックオフィス → 共通基盤           │
└───────────────────────────────────────┘

         │
         ▼

Step 4: 統合アーキテクチャ図作成
────────────────────────────────
Output:
  ・VStreamアーキテクチャ図
  ・共有レベル別Capability一覧
  ・Brand固有VStream定義
```

### 5.2 YAML出力形式

```yaml
# phase3-vstream-architecture.yaml

vstream_architecture:
  metadata:
    organization: アサヒ飲料
    pattern: hybrid
    design_date: 2025-01-14

  # アーキテクチャパターン選択理由
  pattern_rationale:
    selected: hybrid
    reasons:
      - "同一OpCo内の複数ブランド"
      - "購買チャネル（スーパー、コンビニ）は共通"
      - "ブランドごとに異なる顧客体験価値"

  # 共通VStream基盤
  shared_vstream_foundation:
    level: opco
    owner: アサヒ飲料

    vstreams:
      - id: VStr-Common-Awareness
        name: "認知・選好共通基盤"
        description: "全ブランド共通の認知獲得プロセス"
        operational_stages:
          - id: OS-C-1
            name: "メディア露出管理"
            capability: CL2-C1-MediaPlanning
            sharing_level: opco

          - id: OS-C-2
            name: "販売チャネル管理"
            capability: CL2-C2-ChannelManagement
            sharing_level: opco

      - id: VStr-Common-Distribution
        name: "流通・配荷共通基盤"
        description: "全ブランド共通の流通プロセス"
        operational_stages:
          - id: OS-C-3
            name: "受注処理"
            capability: CL2-C3-OrderProcessing
            sharing_level: opco

          - id: OS-C-4
            name: "物流管理"
            capability: CL2-C4-Logistics
            sharing_level: opco

  # Brand固有VStream
  brand_specific_vstreams:

    - brand: カルピス
      brand_id: Brand-Calpis

      vstreams:
        - id: VStr-CP-HealthValue
          name: "健康価値訴求ストリーム"
          description: "カルピス固有の健康価値訴求"
          value_delivered: [VL3-1-1-2, VL3-1-1-3]
          operational_stages:
            - id: OS-CP-1
              name: "健康エビデンス訴求"
              capability: CL2-CP1-HealthEvidence
              sharing_level: brand
              tvdc_by_stage:
                VS0-1: Supporting
                VS1-2: VCI
                VS3-6: Core

        - id: VStr-CP-FamilyExperience
          name: "家族体験ストリーム"
          description: "カルピス固有の家族体験価値"
          value_delivered: [VL3-2-2-1]
          operational_stages:
            - id: OS-CP-2
              name: "家族体験設計"
              capability: CL2-CP2-FamilyExperience
              sharing_level: brand

    - brand: 三ツ矢サイダー
      brand_id: Brand-Mitsuya

      vstreams:
        - id: VStr-MY-RefreshValue
          name: "爽快価値訴求ストリーム"
          description: "三ツ矢固有の爽快価値訴求"
          operational_stages:
            - id: OS-MY-1
              name: "爽快感訴求"
              capability: CL2-MY1-RefreshAppeal
              sharing_level: brand

  # Capability共有マトリクス
  capability_sharing_matrix:
    - capability_id: CL2-C1-MediaPlanning
      sharing_level: opco
      used_by: [カルピス, 三ツ矢, ワンダ, ...]

    - capability_id: CL2-CP1-HealthEvidence
      sharing_level: brand
      used_by: [カルピス]

    - capability_id: CL2-MY1-RefreshAppeal
      sharing_level: brand
      used_by: [三ツ矢]
```

---

## 6. 組織構造とアーキテクチャの整合性検証

### 6.1 検証ルール

```yaml
architecture_validation_rules:

  # ルール1: 価値継承とCapability共有の整合性
  rule_value_capability_alignment:
    description: "継承された価値を実現するCapabilityは共有されるべき"
    check: |
      IF value_element is inherited from parent
      THEN capability_for_value should be shared at parent level
    example:
      inherited_value: "健康" (HD→OpCo→Brand)
      expected: "品質管理Cap" should be shared at OpCo level

  # ルール2: 分岐価値とBrand固有Capの対応
  rule_diverged_value_brand_cap:
    description: "追加された価値を実現するCapabilityはBrand固有であるべき"
    check: |
      IF value_element is added at brand level
      THEN capability_for_value should be brand-specific
    example:
      added_value: "家族の絆" (カルピスで追加)
      expected: "家族体験設計Cap" should be Calpis-specific

  # ルール3: 顧客セグメントとVStreamの対応
  rule_segment_vstream_alignment:
    description: "異なるセグメントを持つBrandは固有VStreamを持つべき"
    check: |
      IF brand_segment != sibling_brand_segment
      THEN brand should have specific vstreams for differentiation

  # ルール4: 共通プロセスの共有
  rule_common_process_sharing:
    description: "全Brandで同一のプロセスは共通基盤化すべき"
    check: |
      IF process is identical across all brands
      THEN capability should be shared at opco level
```

### 6.2 検証レポート例

```
VStreamアーキテクチャ検証レポート
═══════════════════════════════════

対象: アサヒ飲料 VStreamアーキテクチャ

検証結果サマリー
────────────────
  ✓ 価値継承-Capability整合性: PASSED
  ✓ 分岐価値-Brand固有Cap: PASSED
  ✓ セグメント-VStream対応: PASSED
  ⚠ 共通プロセス共有: WARNING

詳細
────
[PASSED] 価値継承-Capability整合性
  - 「健康」継承 → 品質管理Cap共有 ✓
  - 「潤い」継承 → 飲料製造Cap共有 ✓

[PASSED] 分岐価値-Brand固有Cap
  - 「家族の絆」追加 → 家族体験CapはBrand固有 ✓
  - 「爽快」追加 → 爽快訴求CapはBrand固有 ✓

[PASSED] セグメント-VStream対応
  - カルピス「健康家族層」→ 健康価値VStr固有 ✓
  - 三ツ矢「若年層」→ 爽快価値VStr固有 ✓

[WARNING] 共通プロセス共有
  - 「SNS管理」が各Brandで重複実装
  - 推奨: OpCo共通基盤化を検討
```

---

## 7. まとめ

### 7.1 核心メッセージ

```
企業構造 → 価値継承構造 → VStreamアーキテクチャ
═════════════════════════════════════════════════

1. 企業構造がVStreamアーキテクチャを規定する

2. パターン選択:
   ・コングロマリット → 分離型
   ・マルチブランド → ハイブリッド型
   ・単一ブランド → 統合型

3. 共有/固有の切り分け:
   ・継承された価値 → 共有Cap
   ・追加された価値 → 固有Cap

4. 検証:
   ・価値継承とCap共有の整合性
   ・組織構造とアーキテクチャの対応
```

### 7.2 V5.7での追加機能

| 機能 | 内容 |
|------|------|
| アーキテクチャパターン選択 | 組織構造に基づくパターン判定 |
| 共有レベル定義 | HD/OpCo/Brand別のCap共有 |
| 統合アーキテクチャ図 | 共通基盤+Brand固有の可視化 |
| 整合性検証 | 価値継承とアーキテクチャの検証 |

---

**作成日**: 2025-01-14
**バージョン**: V5.7 VStream Architecture Alignment Draft 1.0
