# パラソル・ビジネス価値分析ガイド

## 🎯 価値分析コンセプト

Parasolの Business Nine Dimensions フレームワークを活用して、ビジネス価値を構造的に分析・定義します。

```
生の価値アイデア → Business Nine Dimensions → 洗練された価値定義
```

## 📊 価値定義プロセス

### Phase 1: 価値スパークの収集

```bash
# ビジネス価値のラフなアイデアから始める
/parasol analyze "顧客の業務効率を30%向上させたい、でも人間味を失わずに"

# 体験的な価値ビジョン
/parasol analyze "朝のコーヒーのように、毎日使いたくなるダッシュボード"

# 不完全なアイデアからでもOK
/parasol analyze "何か...プロジェクトが楽しくなるような管理ツール"
```

### Phase 2: Business Nine Dimensions による価値構造化

Parasol の Business Nine Dimensions を価値定義に適用：

1. **Impact（インパクト）** → 業務変革の深度と広がり
   - 効率性向上 vs 品質改善
   - 個人レベル vs 組織レベルの改善

2. **Velocity（速度）** → 価値実現までのスピード
   - 即効性のある改善 vs 段階的な価値構築
   - 短期的ROI vs 長期的戦略価値

3. **Messaging（メッセージング）** → 価値の伝達と共有
   - 定量的指標 vs 定性的体験
   - 技術的効果 vs ビジネス成果

4. **Reach（リーチ）** → 影響範囲と波及効果
   - 個人価値 vs チーム価値 vs 組織価値
   - 局所的改善 vs 全社的変革

5. **Sentiment（感情価値）** → 心理的・文化的価値
   - 安心感 vs 達成感
   - 信頼性 vs イノベーション

6. **Metrics（指標）** → 価値の測定と可視化
   - パフォーマンス指標 vs エンゲージメント指標
   - 数値的成果 vs 体感的改善

7. **Balance（バランス）** → 投資と効果の最適配分
   - 効率性 vs 創造性
   - 自動化 vs 人間中心

8. **Depth（深度）** → 変革の根深さと持続性
   - 表面的改善 vs 構造的変化
   - 一時的効果 vs 持続的価値

9. **Foundation（基盤）** → 価値を支える土台
   - 技術基盤 vs 人材基盤
   - プロセス改善 vs 文化変革

### Phase 3: Five Pillars による価値深化

1. **Purpose（目的）**
   - なぜこの価値が重要か？
   - 誰のための価値か？

2. **Craft（技巧）**
   - どのように価値を実現するか？
   - 必要な能力は何か？

3. **Constraints（制約）**
   - 価値実現の制限は？
   - トレードオフは？

4. **Incompleteness（不完全性）**
   - 段階的な価値実現
   - 継続的な改善余地

5. **Humans（人間）**
   - 人間中心の価値設計
   - 感情的な共感

## 🚀 実践例

### 例1: コンサルティングダッシュボードの価値定義

```bash
# Step 1: 初期のビジネス価値スパーク
/parasol analyze "コンサルタントの生産性を向上させつつ、
クライアントとの関係性も深めたい"

# Step 2: Business Nine Dimensions による構造化分析
# → "生産性と関係性のバランス、効率化と人間味の両立"

# Step 3: ビジネス価値システムとして定義
/parasol value-framework "productivity-relationship balance"
```

**出力例:**
```yaml
business_value_definition:
  core_value: "効率と信頼の調和"

  business_dimensions:
    impact: "個人生産性30%向上 + クライアント満足度向上"
    velocity: "即効性ツール + 段階的な信頼関係構築"
    messaging: "ROI指標 + 関係性成熟度"
    reach: "個人効率 → チーム協働 → 組織成長"
    sentiment: "達成感と信頼感の醸成"
    metrics: "作業時間削減率 + クライアント継続率"
    balance: "70% 効率化 : 30% 関係構築"
    depth: "プロセス改善 + 文化的変化"
    foundation: "技術基盤 + 人材育成基盤"

  five_pillars:
    purpose: "コンサルタントとクライアントの持続的共創"
    craft: "AI支援分析 + 人間的コミュニケーション"
    constraints: "学習コスト、既存システム統合"
    incompleteness: "段階的価値提供、継続改善"
    humans: "使う喜び、成長の実感、誇りのある仕事"
```

### 例2: タスク管理システムの価値定義

```bash
# ビジネス価値のラフなアイデアから開始
/parasol analyze "タスクが楽しくなる、ゲームみたいな達成感でチームが活性化"

# Business Nine Dimensionsで価値構造化
/parasol value-framework "engagement-driven productivity"
```

## 🔄 パラソル6フェーズへの接続

### 価値分析（Phase 1）→ 能力設計（Phase 2）

```bash
# Business Nine Dimensions で価値を定義
/parasol analyze "30% productivity improvement with human touch"

# パラソル能力階層へ変換
L1_Capability: "Human-Centered Productivity Excellence"
  L2_Capability: "Intelligent Task Automation" 
    L3_Capability: "Context-Aware Assignment"
  L2_Capability: "Relationship-Enhanced Collaboration"
    L3_Capability: "Empathetic Client Interaction"
```

## 📝 統合ワークフロー

```bash
# 1. Business Nine Dimensions でビジネス価値の構造化
/parasol analyze "your raw business value idea"

# 2. パラソル価値分析フレームワークへ適用
./tools/cli/parasol value-framework --business-dimensions

# 3. DDDワークフローと連携
/ddd:1-plan "ビジネス価値定義を技術実装へ変換"

# 4. 価値メトリクスとKPIの設定
/parasol metrics "business KPIs and value measurements"
```

## 🎯 期待される成果

1. **明確な価値定義**
   - 曖昧なアイデアが構造化される
   - 9.5/10 のクオリティ基準

2. **ステークホルダーの共感**
   - "これが私たちの求めていた価値だ"
   - 想像を超えた洗練度

3. **実装への明確なパス**
   - 価値→能力→実装の流れ
   - 測定可能なKPI

## 🔧 ビジネス価値分析エージェント

```yaml
# ビジネス価値分析専門の機能
business-value-architect:
  keywords: [value, worth, benefit, impact, roi, kpi, outcome, business]
  owns: "ビジネス価値定義、KPI設計、ROI分析、価値測定"
  framework: "Business Nine Dimensions + Five Pillars"
  example: "Define business value for productivity dashboard"
```

## 📚 参考リンク

- [Business Nine Dimensions Framework](../value-definition/)
- [Parasol Value Analysis Guide](../01-value-analysis/)  
- [Five Pillars Philosophy](../../../PHILOSOPHY.md)
- [DDD Workflow Integration](../../ai_working/ddd/)