# Amplifier Designer × パラソル価値分析統合ガイド

## 🎯 統合コンセプト

Amplifierの `/designer` コマンドを活用して、パラソルの価値分析フェーズを強化します。

```
生の価値アイデア → Designer変換 → 洗練された価値定義
```

## 📊 価値定義プロセス

### Phase 1: 価値スパークの収集

```bash
# ビジネス価値のラフなアイデアを投げかける
/designer value "顧客の業務効率を30%向上させたい、でも人間味を失わずに"

# 価値のバイブを表現
/designer value "朝のコーヒーのように、毎日使いたくなるダッシュボード"

# 不完全なビジョンから始める
/designer value "何か...プロジェクトが楽しくなるような管理ツール"
```

### Phase 2: Nine Dimensions による価値構造化

Designer の Nine Dimensions を価値定義に適用：

1. **Style（スタイル）** → ビジネススタイル
   - フォーマル vs カジュアル
   - 企業向け vs スタートアップ向け

2. **Motion（動き）** → 価値の伝達速度
   - 即座の価値 vs 段階的な価値
   - 短期的インパクト vs 長期的成長

3. **Voice（声）** → 価値メッセージング
   - 技術的価値 vs ビジネス価値
   - 定量的価値 vs 定性的価値

4. **Space（空間）** → 価値の範囲
   - 個人価値 vs チーム価値 vs 組織価値
   - 局所的価値 vs 全体的価値

5. **Color（色）** → 価値の感情的側面
   - 安心感 vs 革新性
   - 信頼性 vs 柔軟性

6. **Typography（文字）** → 価値の表現方法
   - データドリブン vs ストーリーテリング
   - 数値指標 vs ナラティブ

7. **Proportion（比率）** → 価値のバランス
   - 効率性 vs 創造性
   - 自動化 vs 人間中心

8. **Texture（質感）** → 価値体験の深さ
   - 表面的な改善 vs 根本的な変革
   - 単純な効率化 vs 複雑な最適化

9. **Body（本体）** → 価値の実体
   - 機能的価値 vs 感情的価値
   - 直接的価値 vs 間接的価値

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
# Step 1: 初期のスパーク
/designer value "コンサルタントの生産性を向上させつつ、
クライアントとの関係性も深めたい"

# Step 2: Designer による解釈
# → "生産性と関係性のバランス、効率化と人間味の両立"

# Step 3: Nine Dimensions 適用
/designer value system "productivity-relationship balance"
```

**出力例:**
```yaml
value_definition:
  core_value: "効率と信頼の調和"

  dimensions:
    style: "プロフェッショナル with 温かみ"
    motion: "即座の効率化 + 段階的な信頼構築"
    voice: "データドリブン + ヒューマンストーリー"
    space: "個人の生産性 → チームの協働 → 組織の成長"
    color: "信頼のブルー + 活力のオレンジ"
    typography: "明確な数値 + 豊かなコンテキスト"
    proportion: "70% 効率化 : 30% 関係構築"
    texture: "スムーズなワークフロー + 深い洞察"
    body: "機能的な時短 + 感情的な満足"

  pillars:
    purpose: "コンサルタントとクライアントの共創"
    craft: "AI支援 + 人間の判断"
    constraints: "学習曲線、既存システムとの統合"
    incompleteness: "段階的な機能追加、継続的なフィードバック"
    humans: "使う喜び、成長の実感"
```

### 例2: タスク管理システムの価値定義

```bash
# ラフなアイデアから開始
/designer value "タスクが楽しくなる、ゲームみたいな達成感"

# Designerが変換
/designer value component "task-gamification"
```

## 🔄 パラソル6フェーズへの接続

### 価値分析（Phase 1）→ 能力設計（Phase 2）

```bash
# Designer で価値を定義
/designer value "30% productivity improvement with human touch"

# パラソル能力階層へ変換
L1_Capability: "Productivity Excellence"
  L2_Capability: "Task Automation"
    L3_Capability: "Smart Assignment"
  L2_Capability: "Relationship Building"
    L3_Capability: "Client Collaboration"
```

## 📝 統合ワークフロー

```bash
# 1. Amplifier Designer で価値のコンセプトデザイン
/designer value "your raw value idea"

# 2. パラソル価値分析テンプレートへ適用
./tools/cli/parasol apply-value --from-designer

# 3. DDDワークフローと連携
/ddd:1-plan "Designer定義の価値を実装"

# 4. 価値メトリクスの設定
/designer metrics "value KPIs and measurements"
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

## 🔧 カスタムエージェント追加案

```yaml
# 価値定義専門エージェントの登録
value-architect:
  keywords: [value, worth, benefit, impact, roi, kpi, outcome]
  owns: "価値定義、KPI設計、ROI分析"
  example: "Define business value for dashboard project"
```

## 📚 参考リンク

- [Amplifier Designer Documentation](.claude/commands/designer.md)
- [Parasol Value Analysis](../01-value-analysis/)
- [DDD Workflow Integration](../../ai_working/ddd/)