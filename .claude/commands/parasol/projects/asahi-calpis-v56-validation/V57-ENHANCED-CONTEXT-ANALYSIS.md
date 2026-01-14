# Parasol V5.7: 拡張コンテキスト分析仕様

**Enhanced Context Analysis with Organization Value Inheritance**

---

## 1. 課題: 現行Phase 1の限界

### 現行Phase 1で収集する情報

```yaml
# 現行 V5.6 Phase 1
organization_scope:
  holding_company: "アサヒグループホールディングス"  # 名前のみ
  operating_company: "アサヒ飲料"                    # 名前のみ
  brand: "カルピス"                                  # 名前のみ

# 問題: 以下が欠落
# - 各階層の価値定義
# - 継承関係
# - 顧客セグメント
# - 他のOpCo/Brandとの関係
```

### 不足している情報

| 情報 | 現行 | 必要性 |
|------|------|--------|
| 組織階層名 | ✓ | - |
| 各階層の価値定義 | ✗ | 継承の起点 |
| 顧客セグメント | ✗ | 絞り込み設計 |
| 継承タイプ | ✗ | 変換ルール |
| 兄弟組織 | ✗ | ポートフォリオ分析 |
| トポロジータイプ | ✗ | 継承パターン選択 |

---

## 2. V5.7 拡張コンテキスト分析

### 2.1 収集フロー

```
V5.7 Phase 1 拡張コンテキスト分析フロー
═══════════════════════════════════════

Step 1: 組織トポロジー特定
─────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ Q1: 組織構造のタイプを選択してください                        │
│                                                             │
│   (A) 単一事業型        HD → OpCo → Brand (1系統)           │
│   (B) コングロマリット型  HD → 複数OpCo → 各Brand            │
│   (C) マルチブランド型   HD → OpCo → 複数Brand               │
│   (D) マトリクス型      地域×製品 等の複合軸                 │
│   (E) 複合型           B + C の組み合わせ等                 │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Step 2: HD情報収集（存在する場合）
──────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ Q2: 持株会社/グループ会社の情報                              │
│                                                             │
│   - 名称: [                                            ]    │
│   - 企業理念/ミッション（あれば）:                          │
│     [                                                  ]    │
│   - 主要顧客スコープ: [全世界 / 特定地域 / ...]             │
│                                                             │
│   ※ 上場企業の場合、IR資料から取得可能                      │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Step 3: OpCo情報収集
────────────────────
┌─────────────────────────────────────────────────────────────┐
│ Q3: 事業会社の情報                                          │
│                                                             │
│   - 名称: [                                            ]    │
│   - 事業ミッション（あれば）:                               │
│     [                                                  ]    │
│   - HD価値との関係:                                        │
│     □ 直接継承（ほぼ同じ）                                  │
│     □ 特殊化（領域を絞った）                                │
│     □ 分岐（異なる方向へ）                                  │
│   - 主要顧客スコープ: [                                 ]   │
│                                                             │
│   ※ コングロマリットの場合、複数OpCoを収集                  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Step 4: Brand情報収集
─────────────────────
┌─────────────────────────────────────────────────────────────┐
│ Q4: ブランドの情報                                          │
│                                                             │
│   - 名称: [                                            ]    │
│   - ブランドミッション/価値提案:                            │
│     [                                                  ]    │
│   - OpCo価値との関係:                                      │
│     □ 直接継承                                              │
│     □ セグメント特化                                        │
│     □ 拡張（新価値追加）                                    │
│   - ターゲット顧客:                                         │
│     [                                                  ]    │
│   - 主要な差別化要素:                                       │
│     [                                                  ]    │
│                                                             │
│   ※ マルチブランドの場合、複数Brandを収集                   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Step 5: 継承構造の確認・検証
────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ Q5: 継承構造の確認                                          │
│                                                             │
│   収集した情報から以下を生成・確認:                          │
│                                                             │
│   組織ツリー:                                               │
│     HD: [名称]                                              │
│       └─ OpCo: [名称]                                       │
│            └─ Brand: [名称]                                 │
│                                                             │
│   価値継承チェーン:                                         │
│     HD価値 → OpCo価値 → Brand価値                          │
│     [    ] → [    ] → [    ]                               │
│                                                             │
│   顧客セグメント絞り込み:                                    │
│     HD顧客 ⊃ OpCo顧客 ⊃ Brand顧客                          │
│     [    ] ⊃ [    ] ⊃ [    ]                               │
│                                                             │
│   この構造で正しいですか？ [はい / 修正]                     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 出力YAML仕様

```yaml
# phase1-extended-context.yaml
# V5.7 拡張コンテキスト分析出力

metadata:
  version: "5.7"
  analysis_date: 2025-01-14
  analyst: "..."

# ===== 組織トポロジー =====
organization_topology:
  type: conglomerate_multi_brand  # 選択されたタイプ
  description: "持株会社の下に複数事業会社、各事業会社に複数ブランド"

# ===== 組織階層と価値継承 =====
organization_hierarchy:

  # ----- HD階層 -----
  holding_company:
    name: "アサヒグループホールディングス"
    established: 2011

    # HD価値定義
    value_definition:
      id: VL0-HD
      statement: "食を通じて世界の人々の健康で豊かな生活に貢献"
      source: "企業理念（IR資料）"
      core_elements:
        - keyword: "食"
          meaning: "人間の基本的ニーズとしての食"
        - keyword: "健康"
          meaning: "身体的・精神的wellbeing"
        - keyword: "豊かな生活"
          meaning: "QOL向上全般"
        - keyword: "世界"
          meaning: "グローバルスケール"

    # HD顧客スコープ
    customer_scope:
      id: CS0-HD
      description: "全世界の食品・飲料消費者"
      geographic: global
      demographic: all
      size_indicator: "100%"

  # ----- OpCo階層（複数可） -----
  operating_companies:
    - id: OpCo-Beverages
      name: "アサヒ飲料"
      established: 1982

      # 継承関係
      inheritance:
        parent: VL0-HD
        type: specialization
        transformations:
          - from_element: "食"
            to_element: "飲料"
            rationale: "飲料事業への領域特化"
          - from_element: "世界"
            to_element: "日本"
            rationale: "国内市場フォーカス"

      # OpCo価値定義
      value_definition:
        id: VL0-OpCo-Bev
        statement: "飲料を通じて日本の生活者の健康と潤いに貢献"
        source: "事業ミッション"
        inherited_elements:
          - "健康" # HDから継承
        new_elements:
          - keyword: "潤い"
            meaning: "飲料ならではの渇きを癒す価値"

      # OpCo顧客スコープ
      customer_scope:
        id: CS0-OpCo-Bev
        parent: CS0-HD
        description: "日本の清涼飲料消費者"
        geographic: japan_domestic
        category: soft_drinks
        size_indicator: "~2%"
        narrowing:
          dimension: "geography × category"
          from: "全世界の食品消費者"
          to: "日本の清涼飲料消費者"

    - id: OpCo-Beer
      name: "アサヒビール"
      # (省略: 同様の構造)

    - id: OpCo-Food
      name: "アサヒグループ食品"
      # (省略: 同様の構造)

  # ----- Brand階層（複数可） -----
  brands:
    - id: Brand-Calpis
      name: "カルピス"
      parent_opco: OpCo-Beverages
      established: 1919

      # 継承関係
      inheritance:
        parent: VL0-OpCo-Bev
        type: segmentation
        transformations:
          - from_element: "飲料"
            to_element: "乳酸菌発酵飲料"
            rationale: "製品特性による特化"
          - from_element: "生活者"
            to_element: "家族"
            rationale: "消費シーンによる特化"
          - add_element: "家族の絆"
            rationale: "ブランド固有の情緒的価値"

      # Brand価値定義（= VL1）
      value_definition:
        id: VL1-Calpis
        statement: "乳酸菌発酵で心身の健やかさと家族の絆を支える"
        inherited_elements:
          - element: "健康"
            from: OpCo
            transformation: "心身の健やかさ"
        new_elements:
          - keyword: "家族の絆"
            meaning: "世代を超えた共有体験"
          - keyword: "乳酸菌発酵"
            meaning: "カルピス固有の製造技術"

      # Brand顧客スコープ（ターゲットセグメント）
      customer_scope:
        id: CS1-Calpis
        parent: CS0-OpCo-Bev
        description: "健康意識のある家族層"
        size_indicator: "~0.3%"
        narrowing:
          dimension: "lifestyle × family_structure"
          from: "日本の清涼飲料消費者"
          to: "健康意識のある家族層"

        # 詳細セグメント定義
        segment_detail:
          demographics:
            primary_decision_maker:
              age: 30-45
              gender: female_skew
              role: "母親"
            household:
              structure: "子供あり"
              children_age: "0-15"
          psychographics:
            health_consciousness: high
            family_orientation: high
            tradition_appreciation: medium_high
          behaviors:
            purchase_frequency: "月2-4回"
            purchase_channel: "スーパー、ドラッグストア"
            consumption_scene: "家庭内、家族一緒"

    - id: Brand-Mitsuya
      name: "三ツ矢サイダー"
      parent_opco: OpCo-Beverages
      # (省略: 同様の構造)

    - id: Brand-Wonda
      name: "ワンダ"
      parent_opco: OpCo-Beverages
      # (省略: 同様の構造)

# ===== 継承構造サマリー =====
inheritance_summary:

  # 価値継承チェーン
  value_chain:
    - level: HD
      id: VL0-HD
      value: "食を通じて世界の人々の健康で豊かな生活に貢献"
    - level: OpCo
      id: VL0-OpCo-Bev
      value: "飲料を通じて日本の生活者の健康と潤いに貢献"
      inheritance_type: specialization
    - level: Brand
      id: VL1-Calpis
      value: "乳酸菌発酵で心身の健やかさと家族の絆を支える"
      inheritance_type: segmentation

  # 顧客セグメント絞り込みチェーン
  segment_chain:
    - level: HD
      id: CS0-HD
      segment: "全世界消費者"
      size: "100%"
    - level: OpCo
      id: CS0-OpCo-Bev
      segment: "日本の清涼飲料消費者"
      size: "~2%"
      narrowing_ratio: "50x"
    - level: Brand
      id: CS1-Calpis
      segment: "健康意識のある家族層"
      size: "~0.3%"
      narrowing_ratio: "~7x"

  # 価値要素の追跡
  element_traceability:
    - hd_element: "健康"
      opco_element: "健康"
      brand_element: "心身の健やかさ"
      transformation: "継承→具体化"

    - hd_element: "豊かな生活"
      opco_element: "潤い"
      brand_element: "家族の絆"
      transformation: "継承→飲料特化→情緒的拡張"

# ===== 検証結果 =====
validation:
  segment_containment:
    status: passed
    checks:
      - child: CS1-Calpis
        parent: CS0-OpCo-Bev
        result: "✓ 包含関係OK（健康家族層 ⊂ 清涼飲料消費者）"

  value_inheritance:
    status: passed
    checks:
      - child: VL1-Calpis
        parent: VL0-OpCo-Bev
        result: "✓ 「健康」要素が継承されている"

  warnings:
    - type: sibling_overlap
      brands: [Brand-Calpis, Brand-Mitsuya]
      overlap: "健康志向"
      recommendation: "健康訴求の差別化を明確に"
```

---

## 3. 収集質問テンプレート

### 3.1 基本質問（全タイプ共通）

```markdown
## Phase 1 拡張コンテキスト分析

### 1. 組織構造について

**Q1.1**: 分析対象の組織構造を教えてください
- 持株会社名: _______________
- 事業会社名: _______________
- ブランド名: _______________

**Q1.2**: 組織構造のタイプは？
- [ ] 単一事業型（HD→OpCo→Brand が1系統）
- [ ] コングロマリット型（複数の異なる事業を持つ）
- [ ] マルチブランド型（1事業会社が複数ブランドを持つ）
- [ ] その他: _______________

### 2. 持株会社/グループの価値について

**Q2.1**: 企業理念・ミッション・パーパスはありますか？
- [ ] はい → 内容: _______________
- [ ] いいえ / 不明

**Q2.2**: その企業理念が想定している顧客は？
- [ ] 全世界の消費者
- [ ] 特定地域（地域名: _______________）
- [ ] 特定カテゴリ（カテゴリ: _______________）

### 3. 事業会社の価値について

**Q3.1**: 事業ミッション・ビジョンはありますか？
- [ ] はい → 内容: _______________
- [ ] いいえ / 持株会社と同じ

**Q3.2**: 持株会社の価値からどう特化していますか？
- [ ] 領域を絞った（例: 食→飲料）
- [ ] 地域を絞った（例: 世界→日本）
- [ ] 顧客を絞った（例: 全員→特定層）
- [ ] その他: _______________

**Q3.3**: 事業会社がターゲットとする顧客は？
_______________

### 4. ブランドの価値について

**Q4.1**: ブランドミッション・価値提案は？
_______________

**Q4.2**: 事業会社の価値からどう特化していますか？
- [ ] 製品特性で特化（例: 飲料→乳酸菌飲料）
- [ ] 顧客セグメントで特化（例: 消費者→家族層）
- [ ] 新しい価値を追加（例: +家族の絆）
- [ ] その他: _______________

**Q4.3**: ブランドのターゲット顧客は？
（できるだけ具体的に）
_______________

### 5. 確認

以下の継承構造で正しいですか？

```
[HD名] 「[HD価値]」
  │     顧客: [HDスコープ]
  │
  └─► [OpCo名] 「[OpCo価値]」
        │     顧客: [OpCoスコープ]
        │
        └─► [Brand名] 「[Brand価値]」
              顧客: [Brandスコープ]
```

- [ ] はい、正しい
- [ ] 修正が必要
```

### 3.2 コングロマリット追加質問

```markdown
### 6. 他の事業会社について（コングロマリットの場合）

**Q6.1**: 他にどのような事業会社がありますか？
- 事業会社1: _______________ （事業内容: _______________）
- 事業会社2: _______________ （事業内容: _______________）
- 事業会社3: _______________ （事業内容: _______________）

**Q6.2**: 各事業会社は異なる顧客セグメントを持っていますか？
- [ ] はい、完全に異なる
- [ ] 一部重複あり
- [ ] かなり重複している
```

### 3.3 マルチブランド追加質問

```markdown
### 7. 他のブランドについて（マルチブランドの場合）

**Q7.1**: 同じ事業会社の下に他にどのようなブランドがありますか？
- ブランド1: _______________ （ターゲット: _______________）
- ブランド2: _______________ （ターゲット: _______________）
- ブランド3: _______________ （ターゲット: _______________）

**Q7.2**: ブランド間で顧客セグメントの重複はありますか？
- [ ] いいえ、明確に分かれている
- [ ] 一部重複あり（重複: _______________）
- [ ] かなり重複している

**Q7.3**: ブランド間の差別化ポイントは？
_______________
```

---

## 4. 情報源ガイド

### 4.1 HD価値の情報源

```
優先度1（公式）:
  ├─ IR資料（統合報告書、アニュアルレポート）
  ├─ 企業Webサイト（About Us、企業理念ページ）
  └─ プレスリリース（経営方針発表）

優先度2（推定）:
  ├─ 代表者インタビュー
  ├─ 採用ページ（パーパス記載）
  └─ ESG/サステナビリティレポート

例: アサヒグループHD
  → 統合報告書2024 p.2「グループ理念」
  → https://www.asahigroup-holdings.com/company/philosophy/
```

### 4.2 OpCo価値の情報源

```
優先度1（公式）:
  ├─ 事業会社Webサイト
  ├─ 事業報告書
  └─ 事業方針説明資料

優先度2（推定）:
  ├─ 事業会社代表インタビュー
  ├─ 採用ページ
  └─ HD資料内の事業説明

例: アサヒ飲料
  → https://www.asahiinryo.co.jp/company/
  → 「飲料を通じて、日本の生活者の健康と潤いに貢献」
```

### 4.3 Brand価値の情報源

```
優先度1（公式）:
  ├─ ブランドサイト
  ├─ 製品パッケージ
  └─ 広告コピー（CM、ポスター）

優先度2（推定）:
  ├─ ブランドマネージャーインタビュー
  ├─ SNS公式アカウント
  └─ 消費者調査（ブランドイメージ）

例: カルピス
  → https://www.calpis.co.jp/
  → 「カラダにピース。」
  → 100周年広告「カルピスは、いつだって、家族の味。」
```

---

## 5. Phase 1 → Phase 2 の接続

```
Phase 1 拡張コンテキスト分析
          │
          │ Output: phase1-extended-context.yaml
          │   - organization_hierarchy
          │   - inheritance_summary
          │   - customer_scope（各階層）
          │
          ▼
Phase 2 価値詳細化
          │
          │ Input: Brand価値（VL1）from Phase 1
          │   - VL1-Calpis: 「乳酸菌発酵で心身の健やかさと家族の絆を支える」
          │   - ターゲット: 健康意識のある家族層
          │
          │ Task: VL1 → VL2 → VL3 分解
          │   - 継承された価値要素を展開
          │   - ターゲット顧客のニーズに基づき詳細化
          │
          ▼
Phase 3 バリューストリーム設計
          │
          │ Input:
          │   - VL3詳細価値（from Phase 2）
          │   - ターゲット顧客（from Phase 1）
          │
          │ Task: VL3をどう届けるか設計
          │   - 顧客セグメントの購買行動に基づく
          │   - 継承された価値をどの段階で訴求するか
          │
          ▼
以降のPhase
```

---

## 6. まとめ

### 6.1 V5.6 vs V5.7 Phase 1 比較

| 収集項目 | V5.6 | V5.7 |
|----------|------|------|
| 組織名（HD/OpCo/Brand） | ✓ | ✓ |
| 組織トポロジータイプ | ✗ | ✓ |
| HD価値定義 | ✗ | ✓ |
| OpCo価値定義 | ✗ | ✓ |
| Brand価値定義（VL1） | Phase 2で定義 | Phase 1で収集 |
| 継承タイプ・変換 | ✗ | ✓ |
| 顧客スコープ（各階層） | ✗ | ✓ |
| セグメント絞り込み関係 | ✗ | ✓ |
| 兄弟組織情報 | ✗ | ✓ |
| 継承検証 | ✗ | ✓ |

### 6.2 追加による効果

```
Before (V5.6):
  Phase 1: 組織名だけ収集
  Phase 2: ブランドから価値定義開始（上位との関係不明）

After (V5.7):
  Phase 1: 組織構造＋全階層の価値＋継承関係を収集
  Phase 2: 継承された価値を詳細化（トレーサビリティ確保）
```

---

**作成日**: 2025-01-14
**バージョン**: V5.7 Enhanced Context Analysis Specification Draft 1.0
