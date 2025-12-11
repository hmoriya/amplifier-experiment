# Domain Events - BC-002 MKT-Beverage 飲料マーケティング

## 概要

本ドキュメントは、BC-002 MKT-Beverageのドメインイベントを定義する。

---

## BrandStrategyApproved ブランド戦略承認

| 項目 | 値 |
|------|-----|
| 日本語名 | ブランド戦略承認 |
| 英語名 | BrandStrategyApproved |

### 発行タイミング

ブランド戦略が承認されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| brandId | UUID | ブランドID |
| strategyId | UUID | 戦略ID |
| version | String | バージョン |
| approvedBy | UUID | 承認者ID |
| approvedAt | DateTime | 承認日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | 関係者に通知 |
| GuidelineService | ガイドライン更新をトリガー |

---

## BrandGuidelinePublished ブランドガイドライン公開

| 項目 | 値 |
|------|-----|
| 日本語名 | ブランドガイドライン公開 |
| 英語名 | BrandGuidelinePublished |

### 発行タイミング

ブランドガイドラインが公開されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| brandId | UUID | ブランドID |
| guidelineId | UUID | ガイドラインID |
| version | String | バージョン |
| publishedAt | DateTime | 公開日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | 全社に通知 |
| AssetService | 資産パッケージを生成 |
| ExternalAgencySync | 代理店に同期 |

---

## CampaignApproved キャンペーン承認

| 項目 | 値 |
|------|-----|
| 日本語名 | キャンペーン承認 |
| 英語名 | CampaignApproved |

### 発行タイミング

キャンペーンが承認されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| campaignId | UUID | キャンペーンID |
| brandId | UUID | ブランドID |
| approvedBy | UUID | 承認者ID |
| approvedAt | DateTime | 承認日時 |
| startDate | Date | 開始予定日 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | 作成者に通知 |
| SchedulerService | 実行スケジュールを設定 |
| BC-007 SCM | 需要予測に反映 |

---

## CampaignStarted キャンペーン開始

| 項目 | 値 |
|------|-----|
| 日本語名 | キャンペーン開始 |
| 英語名 | CampaignStarted |

### 発行タイミング

キャンペーンの実行が開始されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| campaignId | UUID | キャンペーンID |
| brandId | UUID | ブランドID |
| startedAt | DateTime | 開始日時 |
| channels | String[] | 配信チャネル |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| MonitoringService | 監視を開始 |
| DashboardService | ダッシュボードに表示 |
| BC-003 CRM-CDP | 顧客接触履歴に記録 |

---

## CampaignCompleted キャンペーン完了

| 項目 | 値 |
|------|-----|
| 日本語名 | キャンペーン完了 |
| 英語名 | CampaignCompleted |

### 発行タイミング

キャンペーンが予定通り完了したとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| campaignId | UUID | キャンペーンID |
| brandId | UUID | ブランドID |
| completedAt | DateTime | 完了日時 |
| totalSpend | Decimal | 総消化額 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| AnalyticsService | 分析レポート生成をトリガー |
| NotificationService | 関係者に通知 |
| FinanceService | 精算処理を開始 |

---

## CampaignPerformanceRecorded パフォーマンス記録

| 項目 | 値 |
|------|-----|
| 日本語名 | パフォーマンス記録 |
| 英語名 | CampaignPerformanceRecorded |

### 発行タイミング

日次パフォーマンスデータが記録されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| campaignId | UUID | キャンペーンID |
| date | Date | 日付 |
| impressions | Long | インプレッション |
| spend | Decimal | 消化額 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| DashboardService | ダッシュボードを更新 |
| AlertService | 異常検知をチェック |

---

## BudgetThresholdReached 予算閾値到達

| 項目 | 値 |
|------|-----|
| 日本語名 | 予算閾値到達 |
| 英語名 | BudgetThresholdReached |

### 発行タイミング

予算消化が閾値（80%）に達したとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| campaignId | UUID | キャンペーンID |
| threshold | Integer | 閾値（%） |
| currentSpend | Decimal | 現在消化額 |
| totalBudget | Decimal | 総予算 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| AlertService | アラート発行 |
| NotificationService | 担当者に通知 |
| PacingService | ペーシング調整を検討 |

---

## MarketResearchCompleted 市場調査完了

| 項目 | 値 |
|------|-----|
| 日本語名 | 市場調査完了 |
| 英語名 | MarketResearchCompleted |

### 発行タイミング

市場調査が完了しレポートが作成されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| researchId | UUID | 調査ID |
| researchType | String | 調査タイプ |
| completedAt | DateTime | 完了日時 |
| reportUrl | String | レポートURL |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | 関係者に通知 |
| KnowledgeBaseService | ナレッジベースに登録 |

---

## CompetitorActivityDetected 競合動向検出

| 項目 | 値 |
|------|-----|
| 日本語名 | 競合動向検出 |
| 英語名 | CompetitorActivityDetected |

### 発行タイミング

競合の重要な動きが検出されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| competitorId | UUID | 競合ID |
| activityType | String | 動向タイプ |
| description | String | 概要 |
| detectedAt | DateTime | 検出日時 |
| severity | Enum | 重要度 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| AlertService | 重要度に応じてアラート |
| NotificationService | ウォッチャーに通知 |
| AnalysisService | 影響分析をトリガー |

---

## EmergingTrendIdentified 新興トレンド識別

| 項目 | 値 |
|------|-----|
| 日本語名 | 新興トレンド識別 |
| 英語名 | EmergingTrendIdentified |

### 発行タイミング

新しいトレンドが識別されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| trendId | UUID | トレンドID |
| trendName | String | トレンド名 |
| category | String | カテゴリ |
| growthRate | Decimal | 成長率 |
| relevanceScore | Decimal | 自社関連度 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | アナリストに通知 |
| DashboardService | トレンドダッシュボードに追加 |
| BC-001 RD | 関連度が高い場合、R&Dに通知 |

---

## イベント発行ルール

### 発行タイミングの原則

1. **状態変更時**: エンティティの重要な状態変更時に発行
2. **トランザクション内**: DB更新と同一トランザクションで発行
3. **冪等性**: 同一イベントの再処理が可能

### イベントストア

| 項目 | 値 |
|------|--------|
| ストレージ | Kafka |
| 保持期間 | 90日 |
| パーティション | brandId または campaignId |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
