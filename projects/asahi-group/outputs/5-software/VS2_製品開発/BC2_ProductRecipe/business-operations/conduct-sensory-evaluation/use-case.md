# Use Case: 官能評価実施 (Conduct Sensory Evaluation)

## 概要

| 項目 | 内容 |
|------|------|
| UC ID | BC2-UC-003 |
| 名称 | 官能評価実施 |
| アクター | 官能評価リーダー、官能パネリスト |
| トリガー | 処方開発時の品質確認、定期品質チェック |
| 関連集約 | SensoryEvaluation, Recipe |

---

## ユースケース記述

### 事前条件 (Preconditions)

1. 官能評価リーダーは認証済みで、評価スケジュール権限を持つ
2. 評価対象の処方が登録済み
3. 評価サンプルが準備済み
4. 資格を持つパネリストが3名以上登録済み

### 事後条件 (Postconditions)

1. 新規SensoryEvaluationエンティティが作成される
2. 全パネリストのスコアが記録される
3. 統計分析（平均、標準偏差）が自動計算される
4. SensoryEvaluationCompletedイベントが発行される
5. 品質判定への入力データとして利用可能

### 基本フロー (Main Flow)

1. **評価スケジュール**: リーダーが評価セッションをスケジュール
   - 評価日時設定
   - 評価タイプ選択（Development/QualityCheck/Benchmark/Consumer）
   - 対象処方とサンプル選択
2. **パネリスト招集**:
   - 資格を持つパネリストリストから選択
   - 最低3名、推奨5-7名
   - 招集通知送信
3. **評価準備**:
   - サンプル準備確認
   - 評価シート生成
   - 評価環境確認（温度、照明等）
4. **評価開始**: リーダーが評価セッションを開始
5. **スコア入力**: 各パネリストが評価項目をスコアリング
   - 外観（色、透明度、泡立ち）
   - 香り（ホップ香、エステル、オフフレーバー）
   - 味（苦味、甘味、酸味、うま味）
   - 口当たり（ボディ、炭酸感）
   - 後味（キレ、余韻）
   - 全体バランス
   - 自由コメント
6. **スコア集計**: 全パネリストのスコア入力完了後に集計
7. **分析レポート生成**:
   - 平均スコア算出
   - 標準偏差計算
   - 外れ値検出
   - パネル一致度評価
8. **評価完了**: リーダーがセッションを完了
9. **結果共有**: 処方担当者に結果通知

### 代替フロー (Alternative Flows)

**A1: ブラインドテスト**
- ステップ3でブラインドテストを選択
- サンプルに識別番号のみ付与
- 結果公開まで製品情報を非表示

**A2: ベンチマーク評価**
- ステップ1で「Benchmark」を選択
- 競合製品または既存製品をリファレンスとして追加
- 比較評価シートを使用

**A3: 消費者パネル**
- ステップ1で「Consumer」を選択
- 一般消費者パネルを招集
- 簡易評価シート（好み中心）を使用

### 例外フロー (Exception Flows)

**E1: パネリスト不足**
- 当日3名未満の場合
- 警告表示、評価続行確認
- 続行の場合、統計的信頼性警告を結果に付与

**E2: スコア入力タイムアウト**
- 設定時間内に入力完了しない場合
- 未入力パネリストに催促通知
- リーダーが延長または除外を判断

**E3: 外れ値検出**
- 統計的外れ値が検出された場合
- リーダーに確認を要求
- 採用/除外/再評価を選択

---

## ビジネスルール

| BR ID | ルール | 検証タイミング |
|-------|--------|----------------|
| BR-120 | 最低3名のパネリストが必要 | 評価開始時 |
| BR-121 | パネリストは有効な資格保持者のみ | パネリスト選択時 |
| BR-122 | 全評価項目のスコア入力が必要 | 集計時 |
| BR-123 | パネル一致度が低い場合は警告 | 分析時 |
| BR-124 | 外れ値は標準偏差2σ超で検出 | 分析時 |
| BR-125 | 評価結果は改ざん不可 | 完了後 |

---

## 評価スコア体系

```yaml
ScoreScale:
  range: 1.0 - 10.0
  precision: 0.5
  anchors:
    1-2: 非常に悪い
    3-4: 悪い
    5-6: 普通
    7-8: 良い
    9-10: 非常に良い

EvaluationAttributes:
  appearance:
    - color: 色調
    - clarity: 透明度
    - foam: 泡立ち・泡持ち
  aroma:
    - hopAroma: ホップ香
    - maltAroma: モルト香
    - ester: エステル香
    - offFlavor: オフフレーバー
  taste:
    - bitterness: 苦味
    - sweetness: 甘味
    - acidity: 酸味
    - umami: うま味
  mouthfeel:
    - body: ボディ
    - carbonation: 炭酸感
    - astringency: 収斂味
  aftertaste:
    - cleanness: キレ
    - lingering: 余韻
  overall:
    - balance: 全体バランス
    - typicality: スタイル適合性
```

---

## データ要件

### 入力データ

```yaml
ScheduleEvaluationInput:
  evaluationType: enum [Development, QualityCheck, Benchmark, Consumer]
  recipeId: uuid (required)
  sampleId: uuid (required)
  evaluationDate: date (required)
  panelistIds: array<uuid> (required, min 3)
  isBlindTest: boolean (default: false)
  benchmarkSamples: array<uuid> (optional)
  timeLimit: integer (minutes, optional)

RecordScoreInput:
  evaluationId: uuid (required)
  panelistId: uuid (required)
  scores: map<attributeId, decimal> (required)
  comments: string (optional)
```

### 出力データ

```yaml
EvaluationResultOutput:
  evaluationId: uuid
  recipeId: uuid
  evaluationType: string
  evaluationDate: date
  panelSize: integer
  results:
    averageScores: map<attributeId, decimal>
    standardDeviations: map<attributeId, decimal>
    overallScore: decimal
    panelConsensus: enum [High, Medium, Low]
  outliers: array<{panelistId, attributeId, deviation}>
  recommendation: enum [Pass, Conditional, Fail]
  reportUrl: string
```

---

## 非機能要件

| 項目 | 要件 |
|------|------|
| 応答時間 | スコア記録: 1秒以内 |
| 同時入力 | 最大15名のパネリスト同時入力対応 |
| リアルタイム | 入力状況のリアルタイム表示 |
| オフライン | タブレットでのオフライン入力対応 |
| 監査 | 全スコア入力の履歴保持 |

---

## 関連API

- POST `/sensory-evaluations` - 評価スケジュール作成
- GET `/sensory-evaluations/{evaluationId}` - 評価詳細取得
- POST `/sensory-evaluations/{evaluationId}/start` - 評価開始
- POST `/sensory-evaluations/{evaluationId}/scores` - スコア記録
- POST `/sensory-evaluations/{evaluationId}/complete` - 評価完了
- GET `/sensory-evaluations/{evaluationId}/report` - レポート取得

---

## 関連ドメインイベント

| イベント | 発行タイミング | 購読者 |
|----------|----------------|--------|
| SensoryEvaluationScheduled | スケジュール作成時 | パネリスト通知 |
| SensoryEvaluationStarted | 評価開始時 | 監査ログ |
| SensoryEvaluationCompleted | 評価完了時 | 品質判定システム、処方担当者 |

---

**作成日**: 2025-11-28
**VS/BC**: VS2/BC2 Product Recipe
