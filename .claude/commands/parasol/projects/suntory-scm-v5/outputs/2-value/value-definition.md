# 価値定義（Value Definition）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5
**作成日**: 2025-01-15

---

## 概要

Phase 1のコンテキスト分析結果を基に、SCM（サプライチェーンマネジメント）コンテキストにおける価値階層（VL1→VL2→VL3）を定義します。

### 設計の前提

- **業種パターン**: 標準型（SCMコンテキスト）
- **主要顧客**: 流通チャネル（卸売・小売・飲食店）
- **最終消費者**: 間接顧客（製品を通じた価値提供）
- **コングロマリットスコア**: 7/15（関連多角化）
- **推奨軸**: fusion-axis, platform-axis, capability-axis

---

## 1. 価値ヒエラルキー（VL1→VL2→VL3）

### VL1: 最上位価値

```yaml
VL1:
  id: VL1-SCM
  name: "安定供給と効率的サプライチェーンによる流通価値の最大化"
  description: |
    サントリーグループのSCMは、流通パートナー（卸売・小売・飲食店）に対して
    「必要なときに、必要な量を、効率的に届ける」ことで、
    流通事業の成長と消費者価値の実現を支援する。

  stakeholder_value:
    - 流通顧客: 欠品ゼロ、適正在庫、販促連動による売上最大化
    - サントリー: SCMコスト最適化、市場シェア維持・拡大
    - 最終消費者: いつでも新鮮な製品が手に入る安心感
    - 社会: 環境負荷低減、持続可能なサプライチェーン
```

---

### VL2: 価値グループ

Phase 1の市場評価・ステークホルダー分析から4つの価値グループを導出：

| ID | 価値グループ | 説明 | Phase 1根拠 |
|----|-------------|------|-------------|
| VL2-1 | **安定供給価値** | 欠品なく確実に届ける | 流通顧客の主要ニーズ |
| VL2-2 | **効率化価値** | コスト最適化で競争力を支援 | 2024年問題、物流コスト上昇 |
| VL2-3 | **品質保証価値** | 安全・品質を保証する | 食品衛生法、HACCP、トレーサビリティ |
| VL2-4 | **持続可能性価値** | 環境・社会に配慮する | 規制強化、ESG要請 |

#### VL2-1: 安定供給価値

```yaml
VL2-1:
  name: "安定供給価値"
  parent: VL1-SCM
  description: |
    流通顧客が「いつでも必要な製品を調達できる」状態を実現する。
    欠品による機会損失をゼロにし、販促計画との連動を可能にする。

  customer_need:
    - 欠品ゼロ（売り場に常に商品がある）
    - 納期遵守（約束した日時に届く）
    - 販促連動（キャンペーン時の増量対応）
    - 季節変動対応（夏季需要3倍への対応）

  measurement:
    - 欠品率: 目標 0.5%以下（業界平均1.2%）
    - 納期遵守率: 目標 99.5%以上
    - リードタイム: 発注から納品まで24-48時間
```

#### VL2-2: 効率化価値

```yaml
VL2-2:
  name: "効率化価値"
  parent: VL1-SCM
  description: |
    物流コストの最適化を通じて、流通顧客の競争力を支援する。
    2024年問題への対応として、輸送能力確保と効率化を両立する。

  customer_need:
    - 配送効率（まとめ配送、定期便）
    - 在庫回転率向上（過剰在庫の削減）
    - 発注業務効率化（EDI、自動補充）
    - コスト透明性（物流コストの可視化）

  measurement:
    - 物流コスト対売上比: 目標 8%以下
    - パレット積載効率: 目標 45ケース/パレット（従来比29%向上）
    - 車両回転率: 目標 10%向上

  2024_problem_response:
    - ドライバー時間外労働: 960時間上限対応
    - 異業種共同輸送: 大王グループとの連携
    - traevo導入: 車両位置可視化による待機時間削減
```

#### VL2-3: 品質保証価値

```yaml
VL2-3:
  name: "品質保証価値"
  parent: VL1-SCM
  description: |
    製品の品質・安全性を製造から納品まで一貫して保証する。
    トレーサビリティにより、問題発生時の迅速対応を可能にする。

  customer_need:
    - 製品品質保証（温度管理、鮮度管理）
    - トレーサビリティ（ロット追跡可能）
    - 問題発生時の迅速対応（リコール対応）
    - 品質情報の透明性

  measurement:
    - 品質クレーム率: 目標 0.01%以下
    - トレース完了時間: 目標 30分以内
    - HACCP適合率: 100%

  regulatory_compliance:
    - 食品衛生法: 製造・保管・輸送の衛生管理
    - HACCP: 必須認証
    - ISO 22000: 推奨認証
```

#### VL2-4: 持続可能性価値

```yaml
VL2-4:
  name: "持続可能性価値"
  parent: VL1-SCM
  description: |
    環境負荷を低減し、持続可能なサプライチェーンを構築する。
    流通顧客のESG対応を支援し、社会的価値を共に創造する。

  customer_need:
    - CO2排出削減（環境報告への寄与）
    - 容器リサイクル対応（回収物流）
    - エシカル調達（原材料のトレーサビリティ）
    - ESGレポート用データ提供

  measurement:
    - CO2排出量: 2030年30%削減目標
    - リサイクル率: 目標 90%以上
    - 水源涵養面積: 天然水の森 21,000ha維持

  initiatives:
    - モーダルシフト: 鉄道・船舶活用
    - EVトラック導入
    - 再生可能エネルギー活用
```

---

### VL3: 詳細価値（価値必然性評価付き）

各VL2を実現するための具体的な価値要素を定義。Phase 3へのTVDC分類に向けて価値必然性を評価。

#### VL2-1「安定供給価値」のVL3

| ID | 価値要素 | 説明 | 価値必然性 | VCI候補 |
|----|---------|------|-----------|---------|
| VL3-1-1 | **需要予測精度向上** | AI/ML活用による需要予測 | ★★★ | No |
| VL3-1-2 | **在庫最適化** | 適正在庫水準の維持 | ★★★ | Yes |
| VL3-1-3 | **生産計画連携** | 需要に連動した生産計画 | ★★☆ | No |
| VL3-1-4 | **欠品アラート** | 早期警告システム | ★★☆ | No |
| VL3-1-5 | **販促計画連動** | キャンペーン連携出荷 | ★★☆ | No |

```yaml
VL3-1-1:
  name: "需要予測精度向上"
  parent: VL2-1
  description: "AI/機械学習を活用し、季節・イベント・天候を考慮した需要予測を実現"

  value_necessity:
    score: "★★★"
    evaluation:
      value_impact: "部分低下"
      value_impact_reason: "予測精度が低いと在庫過剰または欠品発生"
      state_transition_required: true
      related_stages: ["VS2", "VS3"]
      transition_reason: "VS2（選好）→VS3（決定）に必要な供給確実性"
      failure_impact: "重大"
      failure_reason: "欠品は販売機会損失、過剰在庫はコスト増"
    vci_candidate: false
    vci_reason: "AI活用は差別化要素となりうる"

  phase3_handoff:
    target_capability: "demand-forecasting"
    inherited_necessity: "★★★"
    differentiation_hints:
      - "競合を上回る予測精度で差別化可能"
      - "リアルタイム予測更新で差別化可能"

VL3-1-2:
  name: "在庫最適化"
  parent: VL2-1
  description: "拠点別・製品別の適正在庫水準を維持し、欠品ゼロと在庫コスト削減を両立"

  value_necessity:
    score: "★★★"
    evaluation:
      value_impact: "完全毀損"
      value_impact_reason: "在庫がなければ供給不可能"
      state_transition_required: true
      related_stages: ["VS3", "VS4"]
      transition_reason: "VS3（決定）→VS4（獲得）に在庫が必須"
      failure_impact: "致命的"
      failure_reason: "在庫切れは直接的な機会損失"
    vci_candidate: true
    vci_reason: "在庫管理は必須だが差別化しにくい基盤機能"

  phase3_handoff:
    target_capability: "inventory-management"
    inherited_necessity: "★★★"
    differentiation_hints:
      - "在庫可視化UXで差別化可能か検討"
      - "自動補充精度で差別化可能か検討"
```

#### VL2-2「効率化価値」のVL3

| ID | 価値要素 | 説明 | 価値必然性 | VCI候補 |
|----|---------|------|-----------|---------|
| VL3-2-1 | **配送ルート最適化** | 効率的な配送計画 | ★★★ | No |
| VL3-2-2 | **共同輸送** | 異業種との配送共同化 | ★★★ | No |
| VL3-2-3 | **荷待ち時間削減** | traevo活用の可視化 | ★★☆ | Yes |
| VL3-2-4 | **パレット効率化** | 積載効率29%向上 | ★★☆ | Yes |
| VL3-2-5 | **発注業務効率化** | EDI/自動発注 | ★★☆ | Yes |

```yaml
VL3-2-1:
  name: "配送ルート最適化"
  parent: VL2-2
  description: "AI活用により最適な配送ルートを計算し、燃料コスト・時間を削減"

  value_necessity:
    score: "★★★"
    evaluation:
      value_impact: "部分低下"
      value_impact_reason: "非効率なルートはコスト増加"
      state_transition_required: true
      related_stages: ["VS4"]
      transition_reason: "VS4（価値獲得）の配送実行に直結"
      failure_impact: "重大"
      failure_reason: "2024年問題で効率化は必須要件"
    vci_candidate: false
    vci_reason: "最適化アルゴリズムの精度で差別化可能"

  phase3_handoff:
    target_capability: "route-optimization"
    inherited_necessity: "★★★"
    differentiation_hints:
      - "リアルタイム交通情報連携で差別化"
      - "複数拠点最適化で差別化"

VL3-2-2:
  name: "共同輸送"
  parent: VL2-2
  description: "大王グループ等との異業種共同輸送により輸送能力を確保"

  value_necessity:
    score: "★★★"
    evaluation:
      value_impact: "完全毀損"
      value_impact_reason: "2024年問題で単独輸送は能力不足"
      state_transition_required: true
      related_stages: ["VS4"]
      transition_reason: "輸送能力なければVS4（獲得）不可"
      failure_impact: "致命的"
      failure_reason: "物流能力23%減への対応が必須"
    vci_candidate: false
    vci_reason: "パートナーネットワークで差別化"

  phase3_handoff:
    target_capability: "collaborative-logistics"
    inherited_necessity: "★★★"
    differentiation_hints:
      - "パートナーエコシステム拡大で差別化"
      - "マッチング精度で差別化"
```

#### VL2-3「品質保証価値」のVL3

| ID | 価値要素 | 説明 | 価値必然性 | VCI候補 |
|----|---------|------|-----------|---------|
| VL3-3-1 | **温度管理** | コールドチェーン維持 | ★★★ | Yes |
| VL3-3-2 | **ロットトレース** | 製造から納品まで追跡 | ★★★ | Yes |
| VL3-3-3 | **賞味期限管理** | FIFO/鮮度管理 | ★★★ | Yes |
| VL3-3-4 | **品質検査連携** | 品質データ連携 | ★★☆ | Yes |
| VL3-3-5 | **リコール対応** | 迅速な回収体制 | ★★★ | Yes |

```yaml
VL3-3-1:
  name: "温度管理"
  parent: VL2-3
  description: "製造から納品まで適切な温度帯を維持するコールドチェーン"

  value_necessity:
    score: "★★★"
    evaluation:
      value_impact: "完全毀損"
      value_impact_reason: "温度逸脱は製品価値ゼロ"
      state_transition_required: true
      related_stages: ["VS4", "VS5"]
      transition_reason: "品質維持なければVS5（価値実感）不可"
      failure_impact: "致命的"
      failure_reason: "食品安全に直結、規制違反リスク"
    vci_candidate: true
    vci_reason: "必須だが業界標準、差別化困難"

  phase3_handoff:
    target_capability: "cold-chain-management"
    inherited_necessity: "★★★"
    differentiation_hints:
      - "IoTセンサー精度で差別化可能か"
      - "異常検知速度で差別化可能か"

VL3-3-2:
  name: "ロットトレース"
  parent: VL2-3
  description: "日立との協創によるトレーサビリティシステムで全拠点一元管理"

  value_necessity:
    score: "★★★"
    evaluation:
      value_impact: "完全毀損"
      value_impact_reason: "追跡不能では品質保証できない"
      state_transition_required: true
      related_stages: ["VS5"]
      transition_reason: "問題発生時のVS5維持に必須"
      failure_impact: "致命的"
      failure_reason: "リコール対応不能は致命的"
    vci_candidate: true
    vci_reason: "規制要件であり差別化余地小"

  phase3_handoff:
    target_capability: "traceability"
    inherited_necessity: "★★★"
    differentiation_hints:
      - "トレース時間30分→10分で差別化"
      - "顧客向けトレース情報公開で差別化"
```

#### VL2-4「持続可能性価値」のVL3

| ID | 価値要素 | 説明 | 価値必然性 | VCI候補 |
|----|---------|------|-----------|---------|
| VL3-4-1 | **CO2排出削減** | 輸送効率化によるCO2削減 | ★★☆ | No |
| VL3-4-2 | **リサイクル物流** | 容器回収・リサイクル | ★★☆ | Yes |
| VL3-4-3 | **水源管理** | 天然水の森による持続可能な水源 | ★★★ | No |
| VL3-4-4 | **ESGレポート** | 環境データ提供 | ★☆☆ | Yes |
| VL3-4-5 | **エシカル調達** | 原材料の持続可能性証明 | ★★☆ | No |

```yaml
VL3-4-3:
  name: "水源管理"
  parent: VL2-4
  description: "天然水の森21,000haによる持続可能な水源確保と生態系保全"

  value_necessity:
    score: "★★★"
    evaluation:
      value_impact: "完全毀損"
      value_impact_reason: "水がなければ飲料製造不可"
      state_transition_required: true
      related_stages: ["VS0", "VS1"]
      transition_reason: "サントリーの価値の根幹、VS0の潜在価値に直結"
      failure_impact: "致命的"
      failure_reason: "水資源枯渇は事業継続不可"
    vci_candidate: false
    vci_reason: "サントリー独自の差別化資産"

  phase3_handoff:
    target_capability: "water-resource-management"
    inherited_necessity: "★★★"
    differentiation_hints:
      - "競合にない独自資産"
      - "ブランド価値の源泉"
```

---

## 2. 価値必然性サマリー

### VCI候補リスト（価値必然性★★★かつ差別化困難）

| ID | 価値要素 | 分類予測 | 理由 |
|----|---------|---------|------|
| VL3-1-2 | 在庫最適化 | Supporting | 必須だが業界標準機能 |
| VL3-2-3 | 荷待ち時間削減 | Generic | 業界共通課題 |
| VL3-2-4 | パレット効率化 | Generic | 業界標準化推進中 |
| VL3-2-5 | 発注業務効率化 | Generic | EDIは業界標準 |
| VL3-3-1 | 温度管理 | Supporting | 規制要件、差別化困難 |
| VL3-3-2 | ロットトレース | Supporting | 規制要件 |
| VL3-3-3 | 賞味期限管理 | Generic | 業界標準 |
| VL3-3-4 | 品質検査連携 | Supporting | 業界標準機能 |
| VL3-3-5 | リコール対応 | Supporting | 規制要件 |
| VL3-4-2 | リサイクル物流 | Generic | 業界共通義務 |
| VL3-4-4 | ESGレポート | Generic | 業界共通要件 |

### 差別化候補リスト（価値必然性★★★かつ差別化可能）

| ID | 価値要素 | 分類予測 | 差別化ポイント |
|----|---------|---------|--------------|
| VL3-1-1 | 需要予測精度向上 | Core | AI精度、リアルタイム性 |
| VL3-2-1 | 配送ルート最適化 | Core | アルゴリズム精度 |
| VL3-2-2 | 共同輸送 | Core | パートナーネットワーク |
| VL3-4-3 | 水源管理 | Core | サントリー独自資産 |

---

## 3. Phase 2設計ストーリー

### なぜこの価値構造なのか

#### VL1選定の理由

**「安定供給と効率的サプライチェーンによる流通価値の最大化」**を最上位価値とした理由：

1. **Phase 1の分析結果**: 流通顧客（卸売・小売・飲食店）がSCMの主要価値提供先
2. **2024年問題**: 物流危機への対応が喫緊の経営課題
3. **競争環境**: コカ・コーラ、アサヒ、キリンとの競争で差別化必要
4. **サントリーの強み**: DX先行投資（traevo、トレーサビリティ）を活かせる

#### VL2グループ分けの理由

4つの価値グループに分けた理由：

1. **安定供給価値**: 流通顧客の最も基本的なニーズ（欠品は機会損失）
2. **効率化価値**: 2024年問題への対応として必須（コスト上昇対策）
3. **品質保証価値**: 食品業界の規制要件（HACCP、食品衛生法）
4. **持続可能性価値**: ESG要請の高まり、サントリーの水源管理という強み

この4軸は、Phase 1で特定した主要制約（2024年問題、規制環境、競合状況）と直接対応している。

#### VL3詳細化の理由

各VL2を5つ程度のVL3に分解した理由：

1. **Phase 3での実装単位**: CL（Capability Level）として実装可能な粒度
2. **測定可能性**: KPIを設定し効果測定できる粒度
3. **差別化判定**: VCI候補か差別化可能かを判断できる粒度

---

## 4. Phase 3への引継ぎ情報

### CL1候補ドメイン

| ドメイン | 関連VL3 | 分類予測 |
|---------|--------|---------|
| **demand-management** | VL3-1-1, VL3-1-2, VL3-1-3 | Core |
| **logistics-optimization** | VL3-2-1, VL3-2-2, VL3-2-3, VL3-2-4 | Core |
| **quality-assurance** | VL3-3-1, VL3-3-2, VL3-3-3, VL3-3-4, VL3-3-5 | Supporting |
| **sustainability** | VL3-4-1, VL3-4-2, VL3-4-3, VL3-4-4, VL3-4-5 | Core/Supporting混在 |
| **order-management** | VL3-2-5 | Generic |

### 設計上の考慮事項

1. **2024年問題対応の優先度**: VL3-2-1, VL3-2-2は最優先で実装
2. **規制対応の必須性**: VL3-3-1〜VL3-3-5は規制要件として必須
3. **差別化投資**: VL3-1-1（需要予測）、VL3-4-3（水源管理）に重点投資

---

**作成**: Parasol V5 Phase 2
