# Parasol V5.7 拡張提案: 顧客視点価値継承フレームワーク

**Customer-Centric Value Inheritance Framework (CCVIF)**

**提案日**: 2025-01-14
**対応構造**: コングロマリット、マルチブランド、持株会社型

---

## 1. 対応すべき組織トポロジー

### 1.1 トポロジー分類

```
┌─────────────────────────────────────────────────────────────────────┐
│                     組織トポロジー分類                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  (A) 単一事業型          (B) コングロマリット型                      │
│  ┌───┐                   ┌───┐                                      │
│  │HD │                   │HD │                                      │
│  └─┬─┘                   └─┬─┘                                      │
│    │                       ├────────┬────────┐                      │
│  ┌─┴─┐                   ┌─┴─┐    ┌─┴─┐    ┌─┴─┐                    │
│  │OpCo│                  │飲料│   │ビール│  │食品│ ← 異業種         │
│  └─┬─┘                   └─┬─┘    └─┬─┘    └─┬─┘                    │
│    │                       │        │        │                      │
│  ┌─┴─┐                   ┌─┴─┐    ┌─┴─┐    ┌─┴─┐                    │
│  │Brand│                 │Brand│  │Brand│  │Brand│                  │
│  └───┘                   └───┘    └───┘    └───┘                    │
│                                                                     │
│  (C) マルチブランド型     (D) マトリクス型                           │
│  ┌───┐                   ┌───┐                                      │
│  │HD │                   │HD │                                      │
│  └─┬─┘                   └─┬─┘                                      │
│    │                       ├────────┬────────┐                      │
│  ┌─┴─┐                   ┌─┴─┐    ┌─┴─┐    ┌─┴─┐                    │
│  │OpCo│                  │地域A│  │地域B│  │地域C│ ← 地域軸         │
│  └─┬─┘                   └─┬─┘    └─┬─┘    └─┬─┘                    │
│    ├────┬────┐             │  ╲    ╱│        │                      │
│  ┌─┴─┐┌─┴─┐┌─┴─┐         ┌─┴─┐ ╲╱ ┌─┴─┐    ┌─┴─┐                   │
│  │B1 ││B2 ││B3 │         │P1 │ ╱╲ │P2 │    │P3 │ ← 製品軸          │
│  └───┘└───┘└───┘         └───┘╱  ╲└───┘    └───┘                    │
│  ↑                                                                  │
│  複数ブランドが                                                      │
│  異なるセグメントを狙う                                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 アサヒグループの実際の構造

```
アサヒグループHD (コングロマリット型 + マルチブランド型の複合)
═══════════════════════════════════════════════════════════════

              ┌─────────────────────────────────────┐
              │    アサヒグループホールディングス     │
              │    (全世界・全食品飲料消費者)        │
              └─────────────────┬───────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  アサヒビール   │     │  アサヒ飲料    │     │アサヒグループ  │
│  (酒類消費者)  │     │(清涼飲料消費者)│     │  食品         │
│               │     │               │     │(食品消費者)    │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                     │                     │
  ┌─────┼─────┐         ┌─────┼─────┐         ┌─────┼─────┐
  │     │     │         │     │     │         │     │     │
  ▼     ▼     ▼         ▼     ▼     ▼         ▼     ▼     ▼
┌───┐ ┌───┐ ┌───┐   ┌─────┐┌────┐┌────┐   ┌───┐ ┌───┐ ┌───┐
│ｽｰﾊﾟｰ││ｽﾀｲﾙ││ﾄﾞﾗｲ│   │ｶﾙﾋﾟｽ ││三ツ矢││ﾜﾝﾀﾞ│   │ﾐﾝﾄｨｱ││ﾊﾞﾗﾝｽ││...│
│ﾄﾞﾗｲ││ﾌﾘｰ ││ｾﾞﾛ │   │     ││ｻｲﾀﾞｰ││ｺｰﾋｰ│   │    ││ｱｯﾌﾟ││   │
└───┘ └───┘ └───┘   └─────┘└────┘└────┘   └───┘ └───┘ └───┘
 ↑     ↑     ↑        ↑      ↑     ↑
 │     │     │        │      │     │
各ブランドが異なる顧客セグメントをターゲット
```

---

## 2. 顧客セグメントツリー（Customer Segment Tree）

### 2.1 概念

組織ツリーと並行して**顧客セグメントツリー**を定義し、両者の対応関係を明示化する。

```
組織ツリー                              顧客セグメントツリー
══════════                              ════════════════════

    HD ─────────────────────────────────► 全世界消費者
     │                                          │
     │                                    ┌─────┴─────┐
     │                                    │           │
     ├── OpCo(ビール) ──────────────────► 酒類消費者  │
     │       │                              │         │
     │       ├── スーパードライ ──────────► 辛口嗜好  │
     │       └── スタイルフリー ──────────► 健康志向  │
     │                                                │
     ├── OpCo(飲料) ────────────────────► 清涼飲料消費者
     │       │                              │
     │       ├── カルピス ──────────────► 健康家族層
     │       ├── 三ツ矢サイダー ─────────► 若年層
     │       └── ワンダ ────────────────► ビジネスパーソン
     │
     └── OpCo(食品) ────────────────────► 食品消費者
```

### 2.2 セグメント継承ルール

```yaml
segment_inheritance_rules:
  # ルール1: 子は親の部分集合
  subset_rule:
    definition: "child_segment ⊆ parent_segment"
    validation: true
    example:
      parent: "清涼飲料消費者"
      child: "健康家族層"  # ✓ 清涼飲料消費者の一部

  # ルール2: 兄弟は重複可能（マルチブランド）
  sibling_overlap_rule:
    definition: "siblings MAY overlap"
    validation: warning_only
    example:
      sibling_a: "健康家族層"      # カルピス
      sibling_b: "健康志向成人"    # 三ツ矢（特定保健用食品）
      overlap: "健康志向"          # 重複あり → 警告

  # ルール3: 従兄弟は独立（コングロマリット）
  cousin_independence_rule:
    definition: "cousins are typically independent"
    validation: info_only
    example:
      cousin_a: "健康家族層"       # カルピス（飲料）
      cousin_b: "辛口嗜好"         # スーパードライ（ビール）
      overlap: minimal             # 独立 → 正常
```

---

## 3. 価値継承パターン

### 3.1 コングロマリット型継承

```
コングロマリット価値継承パターン
════════════════════════════════

HD価値（抽象・普遍）
「食を通じて世界の人々の健康で豊かな生活に貢献」
                │
    ┌───────────┼───────────┐
    │ 分岐継承   │           │
    ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│酒類価値  │ │飲料価値  │ │食品価値  │
│         │ │         │ │         │
│"嗜好品で │ │"飲料で  │ │"食品で  │
│ 豊かさ" │ │ 健康"   │ │ 栄養"   │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
 独自発展     独自発展     独自発展
     │           │           │
     ▼           ▼           ▼
 ブランド     ブランド     ブランド
  価値群       価値群       価値群
```

**継承ルール**:
```yaml
conglomerate_inheritance:
  pattern: "divergent_specialization"
  rules:
    - HD価値は十分に抽象的であること
    - OpCo価値はHD価値の一側面を深化
    - OpCo間で価値の重複は最小化
    - 各OpCoは独立した顧客セグメントを持つ
```

### 3.2 マルチブランド型継承

```
マルチブランド価値継承パターン
══════════════════════════════

OpCo価値（事業領域）
「飲料を通じて日本の生活者の健康と潤いに貢献」
                │
    ┌───────────┼───────────┐
    │ 共通継承   │           │
    ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│カルピス  │ │三ツ矢    │ │ワンダ    │
│         │ │サイダー  │ │コーヒー  │
│"発酵で  │ │"爽快で  │ │"本格で  │
│ 健康"   │ │ 元気"   │ │ 充実"   │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
 共通要素:      共通要素:   共通要素:
 "健康"        "潤い"      "潤い"
 "品質"        "品質"      "品質"
```

**継承ルール**:
```yaml
multi_brand_inheritance:
  pattern: "shared_foundation_with_differentiation"
  rules:
    - OpCo価値の核心要素は全ブランドで共有
    - 差別化要素で異なるセグメントを狙う
    - ブランド間のカニバリゼーション管理
    - ポートフォリオとしての補完性
```

### 3.3 価値継承タイプの拡張

```yaml
inheritance_types:
  # 既存（V5.7提案）
  specialization:
    description: "抽象→具体"
    example: "食→飲料→乳酸菌発酵飲料"

  localization:
    description: "地域・市場限定"
    example: "世界→日本→関東"

  extension:
    description: "新価値次元追加"
    example: "+家族の絆"

  refinement:
    description: "比重変更"
    example: "健康30%→40%"

  # 新規追加（コングロマリット・マルチブランド対応）
  divergence:
    description: "HD価値から異なる方向へ分岐"
    example: "食の豊かさ → 嗜好品の喜び / 飲料の健康"
    use_case: "コングロマリット型"

  segmentation:
    description: "同一OpCo内で顧客セグメント別に分岐"
    example: "清涼飲料価値 → 家族向け / 若者向け / ビジネス向け"
    use_case: "マルチブランド型"

  complementation:
    description: "ポートフォリオ内での補完的価値設計"
    example: "カルピス(健康) + 三ツ矢(爽快) = OpCoポートフォリオ"
    use_case: "マルチブランド型"
```

---

## 4. Phase 0.5: 価値継承分解フェーズ

### 4.1 フェーズ位置づけ

```
Parasol V5.7 フェーズ構成
═══════════════════════════

Phase 0: プロジェクト初期化
    │
    ▼
┌────────────────────────────────────────────┐
│ Phase 0.5: 価値継承分解（NEW）              │
│ ──────────────────────────────────────────  │
│                                            │
│ Input:                                     │
│   - 組織階層構造                           │
│   - HD/OpCo既存価値（あれば）              │
│                                            │
│ Output:                                    │
│   - 組織ツリーと顧客セグメントツリー       │
│   - 各階層の価値定義                       │
│   - 継承関係の明示                         │
│   - セグメント絞り込みの記録               │
└────────────────────────────────────────────┘
    │
    ▼
Phase 1: 組織コンテキスト設定
    │
    ▼
Phase 2: 価値定義（ブランドレベル詳細化）
    │
    ▼
Phase 3以降: 従来通り
```

### 4.2 Phase 0.5 実行フロー

```
Phase 0.5 実行フロー
════════════════════

Step 1: 組織トポロジー特定
─────────────────────────
Q: 組織構造はどのタイプですか？
   (A) 単一事業型
   (B) コングロマリット型
   (C) マルチブランド型
   (D) マトリクス型
   (E) 複合型（B+C等）

         │
         ▼

Step 2: HD価値定義（存在する場合）
──────────────────────────────────
Q: 持株会社/グループの企業理念・ミッションは？
   → HD価値（VL0）として記録

         │
         ▼

Step 3: OpCo価値定義
────────────────────
Q: 対象事業会社の事業ミッションは？
Q: HD価値からどのように継承・特殊化されていますか？
   → 継承タイプを選択
   → OpCo価値（VL0-OpCo）として記録

         │
         ▼

Step 4: 顧客セグメント定義
──────────────────────────
Q: 各階層がターゲットとする顧客セグメントは？
Q: セグメントの絞り込み関係は？
   → 顧客セグメントツリーを構築

         │
         ▼

Step 5: ブランド価値定義（マルチブランドの場合）
────────────────────────────────────────────────
Q: 各ブランドの価値提案は？
Q: OpCo価値からどのように継承されていますか？
Q: 他ブランドとの差別化ポイントは？
   → Brand価値（VL1）として記録

         │
         ▼

Step 6: 継承検証
────────────────
- セグメント包含関係の検証
- 価値継承の一貫性検証
- カニバリゼーションリスク評価
```

### 4.3 YAML出力形式

```yaml
# phase0.5-value-inheritance.yaml

value_inheritance_framework:
  topology_type: conglomerate_multi_brand  # 複合型
  analysis_date: 2025-01-14

# ===== HD階層 =====
holding_company:
  name: アサヒグループホールディングス
  value_definition:
    id: VL0-HD
    description: "食を通じて世界の人々の健康で豊かな生活に貢献"
    core_elements:
      - 食
      - 健康
      - 豊かな生活
      - グローバル

  customer_segment:
    id: CS0-HD
    scope: global
    description: "全世界の食品・飲料消費者"
    size: "100%"

# ===== OpCo階層 =====
operating_companies:
  - name: アサヒ飲料
    id: OpCo-Beverages

    inheritance:
      parent: VL0-HD
      type: specialization
      transformations:
        - element: "食"
          to: "飲料"
        - element: "グローバル"
          to: "日本"

    value_definition:
      id: VL0-OpCo-Bev
      description: "飲料を通じて日本の生活者の健康と潤いに貢献"
      inherited_elements:
        - 健康 (from: HD)
      new_elements:
        - 潤い (differentiation)

    customer_segment:
      id: CS0-OpCo-Bev
      parent: CS0-HD
      scope: japan_domestic
      description: "日本の清涼飲料消費者"
      size: "~2%"
      narrowing:
        dimension: geography
        from: "全世界"
        to: "日本"

    # マルチブランド構成
    brands:
      - name: カルピス
        id: Brand-Calpis

        inheritance:
          parent: VL0-OpCo-Bev
          type: segmentation
          transformations:
            - element: "飲料"
              to: "乳酸菌発酵飲料"
            - element: "生活者"
              to: "家族"

        value_definition:
          id: VL1-Calpis
          description: "乳酸菌発酵で心身の健やかさと家族の絆を支える"
          inherited_elements:
            - 健康 (from: OpCo, weight: 30%→40%)
          new_elements:
            - 家族の絆 (brand-specific)
            - 伝統 (brand-specific)

        customer_segment:
          id: CS1-Calpis
          parent: CS0-OpCo-Bev
          description: "健康意識のある家族層"
          size: "~0.3%"
          narrowing:
            dimension: lifestyle
            from: "清涼飲料消費者"
            to: "健康×家族"
          demographics:
            age: 30-45
            family: with_children
            health_consciousness: high

      - name: 三ツ矢サイダー
        id: Brand-Mitsuya

        inheritance:
          parent: VL0-OpCo-Bev
          type: segmentation
          transformations:
            - element: "潤い"
              to: "爽快"

        value_definition:
          id: VL1-Mitsuya
          description: "爽やかな炭酸で元気と楽しさを届ける"
          inherited_elements:
            - 潤い (from: OpCo, specialized: 爽快)
          new_elements:
            - 楽しさ (brand-specific)
            - 若々しさ (brand-specific)

        customer_segment:
          id: CS1-Mitsuya
          parent: CS0-OpCo-Bev
          description: "爽快感を求める若年層"
          size: "~0.5%"
          narrowing:
            dimension: age
            from: "清涼飲料消費者"
            to: "10-30代"

      - name: ワンダ
        id: Brand-Wonda

        inheritance:
          parent: VL0-OpCo-Bev
          type: segmentation
          transformations:
            - element: "飲料"
              to: "コーヒー"

        value_definition:
          id: VL1-Wonda
          description: "本格コーヒーでビジネスパーソンの毎日を支える"
          inherited_elements:
            - 品質 (from: OpCo)
          new_elements:
            - 本格 (brand-specific)
            - 日常支援 (brand-specific)

        customer_segment:
          id: CS1-Wonda
          parent: CS0-OpCo-Bev
          description: "ビジネスパーソン"
          size: "~0.8%"
          narrowing:
            dimension: occasion
            from: "清涼飲料消費者"
            to: "仕事中の飲用"

  - name: アサヒビール
    id: OpCo-Beer
    # (省略: 同様の構造)

  - name: アサヒグループ食品
    id: OpCo-Food
    # (省略: 同様の構造)

# ===== 継承検証結果 =====
validation_results:
  segment_containment:
    status: passed
    checks:
      - child: CS1-Calpis
        parent: CS0-OpCo-Bev
        result: "✓ 包含関係OK"
      - child: CS1-Mitsuya
        parent: CS0-OpCo-Bev
        result: "✓ 包含関係OK"

  value_consistency:
    status: passed
    checks:
      - brand: カルピス
        inherited: "健康"
        source: OpCo
        result: "✓ 継承一貫性OK"

  cannibalization_risk:
    status: warning
    findings:
      - brands: [カルピス, 三ツ矢サイダー]
        overlap_segment: "健康志向"
        risk_level: low
        recommendation: "健康訴求の差別化を明確に"

# ===== ポートフォリオ分析 =====
portfolio_analysis:
  operating_company: アサヒ飲料
  brands_coverage:
    - segment: 健康家族層
      brand: カルピス
      strength: high

    - segment: 若年層
      brand: 三ツ矢サイダー
      strength: high

    - segment: ビジネスパーソン
      brand: ワンダ
      strength: medium

  white_space:
    - segment: シニア層
      current_coverage: low
      opportunity: "高齢者向け機能性飲料"

    - segment: スポーツ愛好者
      current_coverage: low
      opportunity: "スポーツドリンク領域"
```

---

## 5. 可視化: 価値継承マップ

### 5.1 全体継承マップ

```
アサヒグループ 価値継承マップ（Value Inheritance Map）
════════════════════════════════════════════════════════

VL0-HD: 食を通じて世界の人々の健康で豊かな生活に貢献
顧客: 全世界消費者 (100%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            │
   ┌────────┼────────┬────────┐
   │diverge │diverge │diverge │
   ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ビール │ │ 飲料 │ │ 食品 │ │ 海外 │
│OpCo  │ │ OpCo │ │ OpCo │ │ OpCo │
│      │ │      │ │      │ │      │
│嗜好で │ │飲料で │ │食品で │ │...   │
│豊かさ │ │健康  │ │栄養  │ │      │
└──┬───┘ └──┬───┘ └──┬───┘ └──────┘
   │        │        │
   │     ┌──┴──┬─────┐
   │  segment segment segment
   │     │     │     │
   ▼     ▼     ▼     ▼
┌────┐┌─────┐┌────┐┌────┐
│ｽｰﾊﾟｰ││ｶﾙﾋﾟｽ ││三ツ矢││ﾜﾝﾀﾞ │
│ﾄﾞﾗｲ ││     ││    ││    │
│    ││発酵で││爽快で││本格で│
│辛口 ││健康 ││元気 ││充実 │
│    ││+絆  ││+楽  ││+日常│
└────┘└─────┘└────┘└────┘
  ↓      ↓      ↓      ↓
辛口   健康   若年   ビジネス
嗜好   家族   爽快   パーソン
```

### 5.2 セグメント絞り込みファネル

```
顧客セグメント絞り込みファネル
══════════════════════════════

┌─────────────────────────────────────────────────────┐
│              全世界消費者 (100%)                     │  HD
│                     │                               │
│              ┌──────┴──────┐                        │
│              ▼             ▼                        │
│     ┌─────────────┐  ┌───────────────┐             │
│     │ 日本市場    │  │ 海外市場       │             │
│     │ (~2%)      │  │ (対象外)       │             │
│     └──────┬──────┘  └───────────────┘             │
├────────────┼────────────────────────────────────────┤
│            ▼                                        │  OpCo
│     ┌─────────────┐                                 │
│     │清涼飲料消費者│                                 │
│     │ (~2%)      │                                 │
│     └──────┬──────┘                                 │
│            │                                        │
│     ┌──────┼──────┬──────┐                         │
│     ▼      ▼      ▼      ▼                         │
├─────────────────────────────────────────────────────┤
│  ┌─────┐┌─────┐┌─────┐┌─────┐                      │  Brand
│  │健康 ││若年 ││ﾋﾞｼﾞﾈｽ││その他│                      │
│  │家族 ││爽快 ││ﾊﾟｰｿﾝ ││     │                      │
│  │層   ││層   ││     ││     │                      │
│  │0.3% ││0.5% ││0.8% ││...  │                      │
│  └──┬──┘└──┬──┘└──┬──┘└─────┘                      │
│     │      │      │                                │
│     ▼      ▼      ▼                                │
│  ｶﾙﾋﾟｽ   三ツ矢   ﾜﾝﾀﾞ                              │
└─────────────────────────────────────────────────────┘
```

---

## 6. 検証ルールと警告

### 6.1 必須検証（エラー）

```yaml
mandatory_validations:
  - name: "セグメント包含"
    rule: "child.segment ⊆ parent.segment"
    violation: ERROR
    message: "子セグメントが親セグメントを超えています"

  - name: "価値継承存在"
    rule: "child.value references parent.value"
    violation: ERROR
    message: "価値継承の参照が不正です"

  - name: "継承チェーン完全性"
    rule: "all nodes have valid parent except root"
    violation: ERROR
    message: "継承チェーンが不完全です"
```

### 6.2 推奨検証（警告）

```yaml
recommended_validations:
  - name: "カニバリゼーション検出"
    rule: "sibling.segment overlap < 30%"
    violation: WARNING
    message: "兄弟ブランド間でセグメント重複が大きい"

  - name: "価値次元大幅変更"
    rule: "|value_dimension_change| < 20%"
    violation: WARNING
    message: "親から価値次元が大幅に変更されています"

  - name: "ホワイトスペース検出"
    rule: "coverage_gap detected"
    violation: INFO
    message: "カバーされていないセグメントがあります"
```

---

## 7. まとめ: V5.7 CCVIF の価値

### 7.1 対応可能な組織構造

| 構造タイプ | V5.6 | V5.7 CCVIF |
|-----------|------|------------|
| 単一事業型 | △ | ✓ |
| コングロマリット型 | ✗ | ✓ |
| マルチブランド型 | ✗ | ✓ |
| マトリクス型 | ✗ | ✓ |
| 複合型 | ✗ | ✓ |

### 7.2 顧客視点での価値

```
Before (V5.6):
  組織構造 ────────► 価値定義
  （組織起点）

After (V5.7 CCVIF):
  顧客セグメント ◄────► 価値定義 ◄────► 組織構造
  （顧客視点で連動）
```

### 7.3 期待効果

1. **戦略整合性**: HD→OpCo→Brandの価値が追跡可能
2. **ポートフォリオ最適化**: マルチブランドの補完性を設計
3. **カニバリ防止**: ブランド間重複を早期検出
4. **M&A支援**: 新ブランド統合時の価値整合性検証
5. **顧客中心設計**: セグメント起点での価値設計

---

## 8. 次のステップ

- [ ] Phase 0.5 の詳細仕様策定
- [ ] YAML スキーマ定義
- [ ] 検証ルールエンジン設計
- [ ] カルピス事例での完全適用検証
- [ ] アサヒグループ全体での概念実証

---

**作成日**: 2025-01-14
**バージョン**: V5.7 CCVIF Draft 1.0
**ステータス**: 提案（フィードバック募集中）
