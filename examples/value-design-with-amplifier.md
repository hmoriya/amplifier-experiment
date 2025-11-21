# Amplifier Designer × パラソル価値定義 実践例

## 🚀 実践例: ECサイトの価値定義

### Step 1: 生のアイデアから開始

```bash
# ラフな価値のアイデアを投げる
/designer value "オンラインショッピングを、実店舗のような温かい体験にしたい。
でも効率性も失いたくない。売上は30%アップを目指したい。"
```

### Step 2: Designer による価値の解釈と構造化

**Nine Dimensions による分析:**

```yaml
価値構造:
  Style: "デジタル効率 × 人間的温かさ"
  Motion: "スムーズな購買フロー + じっくり選ぶ楽しさ"
  Voice: "親切な店員 + スマートなレコメンド"
  Space: "個人の買い物体験 → コミュニティ形成"
  Color: "信頼の青 + 温かみのオレンジ"
  Typography: "明確な商品情報 + ストーリーテリング"
  Proportion: "60% 効率 : 40% 体験"
  Texture: "直感的UI + 深い商品理解"
  Body: "機能的な検索 + 感情的な発見"
```

### Step 3: パラソル能力階層への展開

```yaml
L1_Strategic_Capability: "Digital Commerce Excellence"
  価値命題: "効率と温かさの両立で売上30%向上"

  L2_Tactical_Capabilities:
    - id: "L2-001"
      name: "Personalized Shopping Journey"
      価値貢献: "顧客満足度20%向上"

    - id: "L2-002"
      name: "Community Commerce"
      価値貢献: "リピート率15%向上"

    - id: "L2-003"
      name: "Smart Recommendation"
      価値貢献: "平均購買単価25%向上"

  L3_Operational_Capabilities:
    - parent: "L2-001"
      operations:
        - "商品検索・フィルタリング"
        - "パーソナライズドホームページ"
        - "購買履歴分析"

    - parent: "L2-002"
      operations:
        - "レビュー・評価システム"
        - "Q&Aコミュニティ"
        - "ソーシャル共有機能"

    - parent: "L2-003"
      operations:
        - "AIレコメンデーション"
        - "関連商品提案"
        - "在庫連動提案"
```

## 🎯 実践例: プロジェクト管理ツールの価値定義

### Step 1: 感覚的な価値表現

```bash
/designer value "月曜日の朝が楽しみになるような、
プロジェクト管理。チームが自然に協力したくなる感じ。"
```

### Step 2: Five Pillars による深化

```yaml
価値の柱:
  Purpose:
    - "仕事を作業から創造へ変える"
    - "チームの潜在能力を解放"

  Craft:
    - "AI による自動タスク分配"
    - "感情分析による最適なチーム編成"

  Constraints:
    - "既存ツールからの移行コスト"
    - "学習曲線の最小化"

  Incompleteness:
    - "Phase 1: 基本的なタスク管理"
    - "Phase 2: AI支援機能"
    - "Phase 3: チーム最適化"

  Humans:
    - "達成感の可視化"
    - "貢献の認識と称賛"
```

### Step 3: 測定可能なKPIへ

```yaml
価値指標:
  定量的指標:
    - プロジェクト完了率: +25%
    - 平均リードタイム: -30%
    - チーム生産性: +40%

  定性的指標:
    - 従業員満足度: 8.5/10以上
    - チーム協力度: +35%
    - 月曜日の出社意欲: +50%
```

## 🔄 統合ワークフローの実行

### 1. 価値定義セッション

```bash
# Amplifier Designer で価値を探索
/designer value "あなたの製品/サービスの価値アイデア"

# 出力を parasol/phases/01-value-analysis/ に保存
```

### 2. パラソル変換

```bash
# Designer の出力をパラソル形式に変換
./tools/cli/parasol transform-value \
  --input="designer-output.md" \
  --output="value-definition.yaml"
```

### 3. DDD ワークフローへ接続

```bash
# 価値定義を基にDDDを開始
/ddd:1-plan "価値定義に基づいた実装計画"

# 自動的に以下が生成:
# - ドメインモデル
# - ユースケース
# - アーキテクチャ選択
```

## 📊 Before/After 比較

### Before (従来の価値定義)
```
"プロジェクト管理を効率化したい"
→ 曖昧、測定不可、共感しにくい
```

### After (Designer × パラソル)
```yaml
価値定義:
  ビジョン: "月曜日が楽しみになるプロジェクト管理"

  価値の次元:
    効率性: "タスク完了時間30%削減"
    体験性: "使う喜び満足度8.5/10"
    協調性: "チーム連携スコア40%向上"

  実現方法:
    L1: "Team Productivity Excellence"
    L2: ["Smart Planning", "Joyful Execution", "Continuous Learning"]
    L3: [具体的な20のオペレーション]

  成功指標:
    - 3ヶ月でROI実現
    - NPS 50以上
    - 継続利用率90%
```

## 🎯 次のステップ

1. **実際に試す**
   ```bash
   cd projects/consulting-dashboard
   /designer value "コンサルティング業務の価値向上"
   ```

2. **価値定義を保存**
   ```bash
   mkdir -p parasol/value-definitions
   # Designer の出力を保存
   ```

3. **実装へ進む**
   ```bash
   /ddd:1-plan "定義された価値の実装"
   ```

## 💡 Tips

- **最初は曖昧でOK**: "なんとなくこんな感じ" から始める
- **Designer が洗練**: 9.5/10 のクオリティに引き上げる
- **あなたのビジョンを保持**: 100% あなたの価値観を反映
- **測定可能に変換**: KPI と成功指標を明確化

---

*"Your value spark → Designer refinement → Parasol structure → Implementation"*