# 価値マイルストーン・フレームワーク V2

**Parasol V5 - 正しい構造に基づく価値実現の設計**

---

## フレームワーク概要

```
1. VL分解（VL1→VL2→VL3）: 価値の階層分解
       ↓
2. VMS導出（VMS5←VMS4←VMS3←VMS2←VMS1）: 顧客価値状態のバックキャスト
       ↓
3. VS設計（VS0-VS7）: バリューストリームマップ設計
       ↓
4. VL×VSマッピング: どの価値がどのステージで実現されるか
       ↓
5. 優先順位決定: VMS達成に必要なVS×VLの特定
```

---

## 根本的な視点転換

### VMS（価値マイルストーン）の正しい定義

| 観点 | 誤った定義（プロセス完了） | 正しい定義（顧客価値状態） |
|------|------------------------|------------------------|
| **主語** | 組織（我々が〜した） | **顧客**（顧客が〜を得ている） |
| **記述** | 活動の完了 | **状態の達成** |
| **測定** | タスク完了率 | **顧客価値の実現度** |
| **例** | 「システム構築完了」 | 「顧客が24時間注文可能な状態」 |

---

## テンプレート 1: 価値分解（VL）テンプレート

### 1.1 VL分解シート

```yaml
# VL分解シート
# 目的: 最上位価値を実行可能な粒度まで分解する

metadata:
  project: "{プロジェクト名}"
  version: "1.0"
  created_at: "{YYYY-MM-DD}"
  last_updated: "{YYYY-MM-DD}"

# ========================================
# VL1: 最上位価値（企業の存在意義レベル）
# ========================================
VL1:
  id: "VL1"
  statement: "{組織が顧客に約束する最上位の価値}"
  # 例: "期待を超える健康とおいしさを届ける"

  customer_impact: |
    この価値が実現されると、顧客は何を得るか？

  success_indicators:
    - indicator: "{測定指標1}"
      target: "{目標値}"
    - indicator: "{測定指標2}"
      target: "{目標値}"

# ========================================
# VL2: 価値グループ（部門レベルの価値）
# ========================================
VL2:
  - id: "VL2-1"
    name: "{価値グループ名}"
    statement: "{具体的な価値文}"
    contributes_to: "VL1"
    contribution_type: "{how it contributes to VL1}"

    customer_outcome: |
      この価値により顧客が得る結果

    measurable_by:
      - "{KPI1}"
      - "{KPI2}"

  - id: "VL2-2"
    name: "{価値グループ名}"
    statement: "{具体的な価値文}"
    contributes_to: "VL1"
    contribution_type: "{how it contributes to VL1}"

    customer_outcome: |
      この価値により顧客が得る結果

    measurable_by:
      - "{KPI1}"

  - id: "VL2-3"
    name: "{価値グループ名}"
    statement: "{具体的な価値文}"
    contributes_to: "VL1"
    contribution_type: "{how it contributes to VL1}"

    customer_outcome: |
      この価値により顧客が得る結果

    measurable_by:
      - "{KPI1}"

# ========================================
# VL3: 詳細価値（実行可能レベル）
# ========================================
VL3:
  # VL2-1配下
  - id: "VL3-1-1"
    name: "{詳細価値名}"
    statement: "{具体的で実行可能な価値}"
    contributes_to: "VL2-1"

    customer_gets: |
      顧客が具体的に手に入れるもの

    realized_through:
      capabilities: []  # Phase 3で特定
      operations: []    # Phase 3で特定

    evidence_of_realization:
      - "{実現を示す証拠1}"
      - "{実現を示す証拠2}"

  - id: "VL3-1-2"
    name: "{詳細価値名}"
    statement: "{具体的で実行可能な価値}"
    contributes_to: "VL2-1"

    customer_gets: |
      顧客が具体的に手に入れるもの

    realized_through:
      capabilities: []
      operations: []

    evidence_of_realization:
      - "{実現を示す証拠}"

  # VL2-2配下
  - id: "VL3-2-1"
    name: "{詳細価値名}"
    statement: "{具体的で実行可能な価値}"
    contributes_to: "VL2-2"

    customer_gets: |
      顧客が具体的に手に入れるもの

    realized_through:
      capabilities: []
      operations: []

    evidence_of_realization:
      - "{実現を示す証拠}"

# ========================================
# 分解の検証チェックリスト
# ========================================
validation:
  VL1_to_VL2:
    - check: "VL2を全て達成するとVL1が実現するか？"
      status: null  # true/false
    - check: "VL2に抜け漏れはないか？"
      status: null
    - check: "VL2間に重複はないか？"
      status: null

  VL2_to_VL3:
    - check: "各VL2配下のVL3を達成するとVL2が実現するか？"
      status: null
    - check: "VL3は実行可能な粒度か？"
      status: null
    - check: "VL3は測定可能か？"
      status: null
```

---

## テンプレート 2: 価値マイルストーン（VMS）テンプレート

### 2.1 VMS定義シート（バックキャスト方式）

```yaml
# 価値マイルストーン定義シート
# 重要: VMS5から逆順に定義する（バックキャスト）

metadata:
  project: "{プロジェクト名}"
  version: "1.0"
  created_at: "{YYYY-MM-DD}"
  backcast_from: "VMS5"

# ========================================
# 核心原則: VMSは「顧客が得ている状態」
# ========================================
# 誤: 「システム開発完了」「研修実施済」
# 正: 「顧客が24時間注文できる状態」「顧客が即座に回答を得られる状態」

# ========================================
# VMS5: 理想状態（18ヶ月後）- 最初に定義
# ========================================
VMS5:
  id: "VMS5"
  name: "{顧客価値の完全実現状態}"
  timeframe: "18ヶ月後"

  customer_state: |
    【顧客は〇〇を得ている状態】
    - 顧客が〜できる
    - 顧客が〜を享受している
    - 顧客にとって〜が当たり前になっている

  # 主語は常に「顧客」
  customer_evidence:
    - "顧客は{具体的な価値1}を得ている"
    - "顧客は{具体的な価値2}を体験している"
    - "顧客は{具体的な行動}ができる"

  success_criteria:
    - criterion: "{顧客価値に基づく測定基準1}"
      target: "{目標値}"
      measurement_method: "{測定方法}"
    - criterion: "{顧客価値に基づく測定基準2}"
      target: "{目標値}"
      measurement_method: "{測定方法}"

  realized_VLs:
    - "VL1"  # この状態でVL1が完全実現
    - "VL2-1"
    - "VL2-2"
    - "VL2-3"
    # 全VL3も実現済み

# ========================================
# VMS4: 最適化状態（12ヶ月後）
# ========================================
VMS4:
  id: "VMS4"
  name: "{顧客価値の最適化状態}"
  timeframe: "12ヶ月後"

  # VMS5に到達するために、この時点で顧客が得ている必要があるもの
  prerequisite_for_VMS5: |
    VMS5に到達するには、この時点で顧客が何を得ている必要があるか？

  customer_state: |
    【顧客は〇〇を得ている状態】
    -
    -

  customer_evidence:
    - "顧客は{具体的な価値}を得ている"
    - "顧客は{具体的な行動}ができる"

  success_criteria:
    - criterion: "{測定基準}"
      target: "{目標値}"
      measurement_method: "{測定方法}"

  realized_VLs:
    - "VL2-1"  # 完全実現
    - "VL2-2"  # 完全実現
    - "VL3-1-1"
    - "VL3-1-2"
    # etc.

  gap_to_VMS5:
    - "VMS4→VMS5で追加で顧客が得るもの: {具体的な価値}"

# ========================================
# VMS3: 成熟状態（9ヶ月後）
# ========================================
VMS3:
  id: "VMS3"
  name: "{顧客価値の成熟状態}"
  timeframe: "9ヶ月後"

  prerequisite_for_VMS4: |
    VMS4に到達するには、この時点で顧客が何を得ている必要があるか？

  customer_state: |
    【顧客は〇〇を得ている状態】
    -
    -

  customer_evidence:
    - "顧客は{具体的な価値}を得ている"

  success_criteria:
    - criterion: "{測定基準}"
      target: "{目標値}"
      measurement_method: "{測定方法}"

  realized_VLs:
    - "VL2-1"  # 部分実現
    - "VL3-1-1"
    # etc.

  gap_to_VMS4:
    - "VMS3→VMS4で追加で顧客が得るもの: {具体的な価値}"

# ========================================
# VMS2: 展開状態（6ヶ月後）
# ========================================
VMS2:
  id: "VMS2"
  name: "{顧客価値の展開状態}"
  timeframe: "6ヶ月後"

  prerequisite_for_VMS3: |
    VMS3に到達するには、この時点で顧客が何を得ている必要があるか？

  customer_state: |
    【顧客は〇〇を得ている状態】
    -
    -

  customer_evidence:
    - "顧客は{具体的な価値}を得ている"

  success_criteria:
    - criterion: "{測定基準}"
      target: "{目標値}"
      measurement_method: "{測定方法}"

  realized_VLs:
    - "VL3-1-1"  # 一部実現
    # etc.

  gap_to_VMS3:
    - "VMS2→VMS3で追加で顧客が得るもの: {具体的な価値}"

# ========================================
# VMS1: 基礎状態（3ヶ月後）
# ========================================
VMS1:
  id: "VMS1"
  name: "{顧客価値の基礎状態}"
  timeframe: "3ヶ月後"

  prerequisite_for_VMS2: |
    VMS2に到達するには、この時点で顧客が何を得ている必要があるか？

  customer_state: |
    【顧客は〇〇を得ている状態】
    - 最小限の価値を体験できる
    -

  customer_evidence:
    - "顧客は{最小限の価値}を得ている"

  success_criteria:
    - criterion: "{測定基準}"
      target: "{目標値}"
      measurement_method: "{測定方法}"

  realized_VLs:
    - "VL3-1-1"  # 最小実現

  gap_to_VMS2:
    - "VMS1→VMS2で追加で顧客が得るもの: {具体的な価値}"

# ========================================
# バックキャスト検証
# ========================================
backcast_validation:
  logical_chain:
    - check: "VMS5→VMS4の因果関係が明確か？"
      status: null
    - check: "VMS4→VMS3の因果関係が明確か？"
      status: null
    - check: "VMS3→VMS2の因果関係が明確か？"
      status: null
    - check: "VMS2→VMS1の因果関係が明確か？"
      status: null

  customer_focus:
    - check: "全VMSの主語が顧客になっているか？"
      status: null
    - check: "全VMSが「状態」を記述しているか？"
      status: null
    - check: "全VMSが測定可能か？"
      status: null
```

---

## テンプレート 3: VL×VMSマトリクス

### 3.1 価値とマイルストーンの対応マトリクス

```yaml
# VL×VMSマトリクス
# 目的: どの価値がどのマイルストーンで実現されるかを明示

metadata:
  project: "{プロジェクト名}"
  version: "1.0"

# ========================================
# マトリクス定義
# ========================================
# 実現度レベル:
#   ◎ = 完全実現（100%）
#   ○ = 主要実現（70-99%）
#   △ = 部分実現（30-69%）
#   ▽ = 初期実現（1-29%）
#   - = 未実現（0%）

matrix:
  # 横軸: VMS（時間軸）
  # 縦軸: VL（価値階層）

  VL1:
    VMS1: "-"
    VMS2: "▽"
    VMS3: "△"
    VMS4: "○"
    VMS5: "◎"
    notes: "VL1はVMS5で完全実現"

  VL2-1:
    VMS1: "▽"
    VMS2: "△"
    VMS3: "○"
    VMS4: "◎"
    VMS5: "◎"
    notes: "{VL2-1の実現パス説明}"

  VL2-2:
    VMS1: "-"
    VMS2: "▽"
    VMS3: "△"
    VMS4: "○"
    VMS5: "◎"
    notes: "{VL2-2の実現パス説明}"

  VL2-3:
    VMS1: "-"
    VMS2: "-"
    VMS3: "▽"
    VMS4: "△"
    VMS5: "○"
    notes: "{VL2-3の実現パス説明}"

  VL3-1-1:
    VMS1: "△"
    VMS2: "○"
    VMS3: "◎"
    VMS4: "◎"
    VMS5: "◎"
    notes: "早期に実現し、他の価値の基盤となる"

  VL3-1-2:
    VMS1: "▽"
    VMS2: "△"
    VMS3: "○"
    VMS4: "◎"
    VMS5: "◎"
    notes: ""

  VL3-2-1:
    VMS1: "-"
    VMS2: "▽"
    VMS3: "△"
    VMS4: "○"
    VMS5: "◎"
    notes: ""

# ========================================
# 視覚的マトリクス（Markdownテーブル形式）
# ========================================
visual_matrix: |
  | 価値ID | 価値名 | VMS1 | VMS2 | VMS3 | VMS4 | VMS5 | 備考 |
  |--------|--------|------|------|------|------|------|------|
  | VL1    | {名}   |  -   |  ▽   |  △   |  ○   |  ◎   | 最上位価値 |
  | VL2-1  | {名}   |  ▽   |  △   |  ○   |  ◎   |  ◎   | - |
  | VL2-2  | {名}   |  -   |  ▽   |  △   |  ○   |  ◎   | - |
  | VL2-3  | {名}   |  -   |  -   |  ▽   |  △   |  ○   | - |
  | VL3-1-1| {名}   |  △   |  ○   |  ◎   |  ◎   |  ◎   | 基盤価値 |
  | VL3-1-2| {名}   |  ▽   |  △   |  ○   |  ◎   |  ◎   | - |
  | VL3-2-1| {名}   |  -   |  ▽   |  △   |  ○   |  ◎   | - |

# ========================================
# 各VMSでの価値実現サマリー
# ========================================
vms_summary:
  VMS1:
    primary_values:
      - id: "VL3-1-1"
        realization: "△"
        customer_gets: "顧客が得る具体的なもの"
    total_value_coverage: "10%"

  VMS2:
    primary_values:
      - id: "VL3-1-1"
        realization: "○"
        customer_gets: ""
      - id: "VL3-1-2"
        realization: "△"
        customer_gets: ""
    incremental_value: "VMS1から追加で顧客が得るもの"
    total_value_coverage: "30%"

  VMS3:
    primary_values:
      - id: "VL2-1"
        realization: "○"
        customer_gets: ""
    incremental_value: ""
    total_value_coverage: "55%"

  VMS4:
    primary_values:
      - id: "VL2-1"
        realization: "◎"
        customer_gets: ""
      - id: "VL2-2"
        realization: "○"
        customer_gets: ""
    incremental_value: ""
    total_value_coverage: "80%"

  VMS5:
    primary_values:
      - id: "VL1"
        realization: "◎"
        customer_gets: ""
    total_value_coverage: "100%"

# ========================================
# 検証チェック
# ========================================
validation:
  - check: "全VL3がVMS5で◎または○になっているか？"
    status: null
  - check: "VL2がVL3の実現に依存しているか（上位は下位より遅い）？"
    status: null
  - check: "VL1が全VL2の実現後に◎になっているか？"
    status: null
  - check: "各VMSで明確な価値増分があるか？"
    status: null
```

---

## テンプレート 4: VL×VSマッピング

### 4.1 価値とバリューステージの対応

```yaml
# VL×VSマッピング
# 目的: どの価値がどのバリューステージで実現されるかを明示

metadata:
  project: "{プロジェクト名}"
  version: "1.0"

# ========================================
# VS定義（顧客状態として）
# ========================================
value_stages:
  VS0:
    name: "潜在ニーズ状態"
    customer_state: "顧客がまだ気づいていないが、この価値を必要としている"

  VS1:
    name: "認知到達状態"
    customer_state: "顧客がこの価値の存在を知った"

  VS2:
    name: "選好形成状態"
    customer_state: "顧客がこの価値を選びたいと思う"

  VS3:
    name: "意思決定状態"
    customer_state: "顧客がこの価値を得ることを決めた"

  VS4:
    name: "価値獲得状態"
    customer_state: "顧客が価値を手に入れた"

  VS5:
    name: "価値実感状態"
    customer_state: "顧客が価値を体験し、満足している"

  VS6:
    name: "価値継続状態"
    customer_state: "顧客にとってこの価値が日常の一部になった"

  VS7:
    name: "価値共創状態"
    customer_state: "顧客が価値を広め、新たな価値を共に創る"

# ========================================
# VL×VSマッピングマトリクス
# ========================================
# 記号:
#   ● = この価値がこのステージで「主に」実現される
#   ○ = この価値がこのステージで「部分的に」実現される
#   △ = この価値がこのステージで「準備」される
#   - = 関係なし

mapping_matrix:
  # 横軸: VS（顧客状態ステージ）
  # 縦軸: VL（価値階層）

  VL3-1-1:
    name: "{価値名}"
    stages:
      VS0: "-"
      VS1: "△"
      VS2: "○"
      VS3: "●"
      VS4: "○"
      VS5: "-"
      VS6: "-"
      VS7: "-"
    primary_stage: "VS3"
    explanation: "この価値は顧客の意思決定時に主に実現される"

  VL3-1-2:
    name: "{価値名}"
    stages:
      VS0: "-"
      VS1: "-"
      VS2: "△"
      VS3: "○"
      VS4: "●"
      VS5: "○"
      VS6: "-"
      VS7: "-"
    primary_stage: "VS4"
    explanation: "この価値は顧客が価値を獲得する時に主に実現される"

  VL3-2-1:
    name: "{価値名}"
    stages:
      VS0: "-"
      VS1: "-"
      VS2: "-"
      VS3: "-"
      VS4: "○"
      VS5: "●"
      VS6: "○"
      VS7: "-"
    primary_stage: "VS5"
    explanation: "この価値は顧客が価値を実感する時に主に実現される"

# ========================================
# 視覚的マトリクス
# ========================================
visual_matrix: |
  | 価値ID | 価値名 | VS0 | VS1 | VS2 | VS3 | VS4 | VS5 | VS6 | VS7 | 主要VS |
  |--------|--------|-----|-----|-----|-----|-----|-----|-----|-----|--------|
  | VL3-1-1| {名}   |  -  |  △  |  ○  |  ●  |  ○  |  -  |  -  |  -  | VS3 |
  | VL3-1-2| {名}   |  -  |  -  |  △  |  ○  |  ●  |  ○  |  -  |  -  | VS4 |
  | VL3-2-1| {名}   |  -  |  -  |  -  |  -  |  ○  |  ●  |  ○  |  -  | VS5 |

# ========================================
# VS別の価値集約
# ========================================
vs_value_summary:
  VS0:
    primary_values: []
    supporting_values: []
    preparation_values: []

  VS1:
    primary_values: []
    supporting_values: []
    preparation_values:
      - "VL3-1-1"

  VS2:
    primary_values: []
    supporting_values:
      - "VL3-1-1"
    preparation_values:
      - "VL3-1-2"

  VS3:
    primary_values:
      - "VL3-1-1"
    supporting_values:
      - "VL3-1-2"
    preparation_values: []

  VS4:
    primary_values:
      - "VL3-1-2"
    supporting_values:
      - "VL3-1-1"
      - "VL3-2-1"
    preparation_values: []

  VS5:
    primary_values:
      - "VL3-2-1"
    supporting_values:
      - "VL3-1-2"
    preparation_values: []

  VS6:
    primary_values: []
    supporting_values:
      - "VL3-2-1"
    preparation_values: []

  VS7:
    primary_values: []
    supporting_values: []
    preparation_values: []

# ========================================
# 洞察と分析
# ========================================
insights:
  value_concentration:
    high_concentration_stages:
      - stage: "VS3"
        value_count: 3
        observation: "意思決定段階に価値が集中"
      - stage: "VS4"
        value_count: 2
        observation: ""

    low_concentration_stages:
      - stage: "VS7"
        value_count: 0
        observation: "共創段階の価値定義が不足している可能性"

  gaps:
    - "VS7に紐づく価値がない → 顧客との共創価値を検討すべき"
    - "{その他のギャップ}"
```

---

## テンプレート 5: 優先順位決定マトリクス

### 5.1 VMS達成に必要なVS×VLの優先順位

```yaml
# 優先順位決定マトリクス
# 目的: 次のVMS達成に必要なVS×VLの組み合わせを優先順位付け

metadata:
  project: "{プロジェクト名}"
  version: "1.0"
  current_milestone: "VMS{N}"
  target_milestone: "VMS{N+1}"

# ========================================
# 現状分析
# ========================================
current_state:
  milestone: "VMS{N}"
  achieved_values:
    - id: "VL3-1-1"
      realization_level: "△"
      vs_coverage: ["VS2", "VS3"]
  remaining_gaps:
    - gap: "VL3-1-1をVS4まで拡張"
      impact: "high"
    - gap: "VL3-1-2を開始"
      impact: "medium"

# ========================================
# ターゲットVMS分析
# ========================================
target_state:
  milestone: "VMS{N+1}"
  required_values:
    - id: "VL3-1-1"
      required_level: "○"
      required_vs_coverage: ["VS2", "VS3", "VS4"]
    - id: "VL3-1-2"
      required_level: "△"
      required_vs_coverage: ["VS2", "VS3"]

# ========================================
# VS×VL優先順位マトリクス
# ========================================
priority_matrix:
  # 優先度基準:
  #   P1 = 最優先（MS達成に必須）
  #   P2 = 高優先（MS達成に重要）
  #   P3 = 中優先（MS達成に貢献）
  #   P4 = 低優先（次期以降）
  #   - = 対象外

  items:
    - id: "VL3-1-1@VS4"
      value: "VL3-1-1"
      stage: "VS4"
      priority: "P1"
      rationale: "VMS{N+1}達成に必須。VS3まで実現済みなので次はVS4"
      effort: "medium"
      dependencies: ["VL3-1-1@VS3"]

    - id: "VL3-1-2@VS2"
      value: "VL3-1-2"
      stage: "VS2"
      priority: "P1"
      rationale: "VMS{N+1}達成に必須。この価値の開始が必要"
      effort: "high"
      dependencies: []

    - id: "VL3-1-2@VS3"
      value: "VL3-1-2"
      stage: "VS3"
      priority: "P2"
      rationale: "VMS{N+1}達成に重要。VS2実現後に進める"
      effort: "medium"
      dependencies: ["VL3-1-2@VS2"]

    - id: "VL3-2-1@VS4"
      value: "VL3-2-1"
      stage: "VS4"
      priority: "P3"
      rationale: "次期VMSへの準備として開始"
      effort: "low"
      dependencies: []

# ========================================
# 視覚的優先順位マトリクス
# ========================================
visual_priority_matrix: |
  | 価値ID | VS2 | VS3 | VS4 | VS5 | VS6 | 備考 |
  |--------|-----|-----|-----|-----|-----|------|
  | VL3-1-1| ✓   | ✓   | P1  | P3  | -   | VS4を優先 |
  | VL3-1-2| P1  | P2  | P4  | -   | -   | VS2から開始 |
  | VL3-2-1| -   | -   | P3  | P4  | -   | 準備開始 |

  凡例: ✓=達成済, P1=最優先, P2=高優先, P3=中優先, P4=低優先

# ========================================
# 実行計画
# ========================================
execution_plan:
  phase_1:
    name: "最優先（P1）"
    timeframe: "1-4週"
    items:
      - id: "VL3-1-1@VS4"
        actions:
          - "VS4ケーパビリティの設計"
          - "VS4オペレーションの実装"
          - "顧客検証"
        success_criterion: "顧客がVS4状態に到達可能"
        owner: "{担当}"

      - id: "VL3-1-2@VS2"
        actions:
          - "VS2ケーパビリティの設計"
          - "VS2オペレーションの実装"
        success_criterion: "顧客がVS2状態に到達可能"
        owner: "{担当}"

  phase_2:
    name: "高優先（P2）"
    timeframe: "5-8週"
    items:
      - id: "VL3-1-2@VS3"
        actions:
          - "VS3ケーパビリティの設計"
          - "VS3オペレーションの実装"
        success_criterion: "顧客がVS3状態に到達可能"
        owner: "{担当}"

  phase_3:
    name: "中優先（P3）"
    timeframe: "9-12週"
    items:
      - id: "VL3-2-1@VS4"
        actions:
          - "準備作業"
        success_criterion: ""
        owner: "{担当}"

# ========================================
# 依存関係図
# ========================================
dependency_diagram: |
  ```mermaid
  graph LR
    A[VL3-1-1@VS3 ✓] --> B[VL3-1-1@VS4 P1]
    C[VL3-1-2@VS2 P1] --> D[VL3-1-2@VS3 P2]
    B --> E[MS達成]
    D --> E
  ```

# ========================================
# リスクと対策
# ========================================
risks:
  - risk: "VL3-1-2@VS2の工数オーバー"
    probability: "medium"
    impact: "high"
    mitigation: "スコープを最小限に絞る"

  - risk: "依存関係による遅延"
    probability: "low"
    impact: "medium"
    mitigation: "並行開発で対応"

# ========================================
# 検証チェックリスト
# ========================================
validation:
  - check: "P1項目を全て達成するとVMS{N+1}に到達できるか？"
    status: null
  - check: "P1項目の依存関係が解決可能か？"
    status: null
  - check: "リソースがP1項目に集中配置されているか？"
    status: null
  - check: "顧客視点での価値増分が明確か？"
    status: null
```

---

## 統合フロー図

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        価値マイルストーン設計フロー                        │
└─────────────────────────────────────────────────────────────────────────┘

Step 1: VL分解
┌─────────────────────────────────────────────────────────────────────────┐
│  VL1「期待を超える健康とおいしさ」                                       │
│    ├─ VL2-1「製品イノベーション価値」                                    │
│    │    ├─ VL3-1-1「発酵技術による味の革新」                            │
│    │    └─ VL3-1-2「健康成分の製品化」                                  │
│    ├─ VL2-2「信頼性価値」                                               │
│    │    └─ VL3-2-1「品質保証の可視化」                                  │
│    └─ VL2-3「利便性価値」                                               │
│         └─ VL3-3-1「購入体験の最適化」                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
Step 2: VMSバックキャスト（顧客価値状態として）
┌──────────────────────────────────────────────────────────────────────────┐
│  VMS5「顧客が期待を超える価値を日常的に享受している状態」← 起点            │
│    ↑                                                                     │
│  VMS4「顧客が全製品ラインで価値を実感している状態」                         │
│    ↑                                                                     │
│  VMS3「顧客が主要製品で価値を体験できる状態」                              │
│    ↑                                                                     │
│  VMS2「顧客が価値を認識し選択できる状態」                                  │
│    ↑                                                                     │
│  VMS1「顧客が最初の価値を体験できる状態」                                  │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
Step 3: VS設計（顧客状態遷移）
┌─────────────────────────────────────────────────────────────────────────┐
│  VS0 → VS1 → VS2 → VS3 → VS4 → VS5 → VS6 → VS7                         │
│  潜在   認知   選好   決定   獲得   実感   継続   共創                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
Step 4: VL×VSマッピング
┌─────────────────────────────────────────────────────────────────────────┐
│          VS0  VS1  VS2  VS3  VS4  VS5  VS6  VS7                         │
│  VL3-1-1  -    △    ○    ●    ○    -    -    -                         │
│  VL3-1-2  -    -    △    ○    ●    ○    -    -                         │
│  VL3-2-1  -    -    -    -    ○    ●    ○    -                         │
│  VL3-3-1  -    -    ○    ●    ○    -    -    -                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
Step 5: 優先順位決定
┌──────────────────────────────────────────────────────────────────────────┐
│  現在: VMS1達成済み                                                       │
│  目標: VMS2達成                                                           │
│                                                                          │
│  P1（最優先）: VL3-1-1@VS4, VL3-3-1@VS3                                  │
│  P2（高優先）: VL3-1-2@VS3                                               │
│  P3（中優先）: VL3-2-1@VS4                                               │
│                                                                          │
│  → 実行計画に落とし込み                                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 使用ガイド

### 1. 順序を守る

必ず以下の順序で進める：

1. **VL分解を先に完了** → 価値の全体像を把握
2. **VMSをバックキャスト** → 顧客価値状態として定義
3. **VSを設計** → 顧客状態遷移を定義
4. **VL×VSマッピング** → 価値の所在を可視化
5. **優先順位決定** → 実行計画に落とし込み

### 2. 顧客視点を徹底

- VMSの主語は常に「顧客」
- 「システム完成」「機能リリース」ではなく「顧客が〇〇できる状態」
- 測定も顧客視点で（顧客満足度、利用率、価値実感スコアなど）

### 3. バックキャストの厳守

- VMS5から逆順に定義
- 「VMS5に到達するにはVMS4で何が必要か？」という問いで導出
- フォワードキャスト（VMS1→VMS2→...）は行わない

### 4. マッピングによる可視化

- VL×VMSマトリクスで「いつ価値が実現するか」を明示
- VL×VSマトリクスで「どこで価値が実現するか」を明示
- ギャップや集中を分析

### 5. 優先順位による実行判断

- VMS達成に必要なVS×VLを特定
- P1（最優先）を明確にして集中投資
- 依存関係を考慮した実行計画

---

## 関連ドキュメント

- [価値方法論リファレンス](./../_value-methodology.md)
- [価値トレースコマンド](../../_commands-v5/value-management/value-trace.md)
- [マイルストーン管理](../../../parasol/_commands-v5/milestone-management/milestone.md)

---

**更新履歴:**
- 2025-12-15: V2として新規作成（正しい構造に再設計）
