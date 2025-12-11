# Domain Events - BC-003 CRM-CDP 顧客データプラットフォーム

## 概要

本ドキュメントは、BC-003 CRM-CDPのドメインイベントを定義する。

---

## CustomerProfileCreated 顧客プロファイル作成

| 項目 | 値 |
|------|-----|
| 日本語名 | 顧客プロファイル作成 |
| 英語名 | CustomerProfileCreated |

### 発行タイミング

新規顧客プロファイルが作成されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| customerId | UUID | 統合顧客ID |
| source | String | 作成元データソース |
| initialIdentifiers | Identifier[] | 初期識別子 |
| createdAt | DateTime | 作成日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| SegmentationService | 初期セグメント評価 |
| WelcomeJourneyService | ウェルカムジャーニー開始 |

---

## IdentitiesMerged ID統合完了

| 項目 | 値 |
|------|-----|
| 日本語名 | ID統合完了 |
| 英語名 | IdentitiesMerged |

### 発行タイミング

複数のIDが同一顧客として統合されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| unifiedCustomerId | UUID | 統合後の顧客ID |
| mergedIdentifiers | Identifier[] | 統合されたID |
| matchConfidence | Decimal | マッチ信頼度 |
| mergedAt | DateTime | 統合日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| ProfileService | プロファイル統合 |
| SegmentationService | セグメント再評価 |
| AnalyticsService | 履歴データ統合 |

---

## SegmentMembershipChanged セグメント所属変更

| 項目 | 値 |
|------|-----|
| 日本語名 | セグメント所属変更 |
| 英語名 | SegmentMembershipChanged |

### 発行タイミング

顧客のセグメント所属が変更されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| customerId | UUID | 顧客ID |
| segmentId | UUID | セグメントID |
| changeType | Enum | 変更タイプ（ENTERED/EXITED） |
| changedAt | DateTime | 変更日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| JourneyService | セグメントトリガー評価 |
| BC-002 MKT | キャンペーン対象更新 |

---

## JourneyEntered ジャーニー開始

| 項目 | 値 |
|------|-----|
| 日本語名 | ジャーニー開始 |
| 英語名 | JourneyEntered |

### 発行タイミング

顧客がジャーニーにエントリーしたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| customerId | UUID | 顧客ID |
| journeyId | UUID | ジャーニーID |
| entryCondition | String | エントリー条件 |
| enteredAt | DateTime | エントリー日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| JourneyExecutionService | 最初のステップ実行 |
| AnalyticsService | ジャーニー統計更新 |

---

## JourneyStepCompleted ジャーニーステップ完了

| 項目 | 値 |
|------|-----|
| 日本語名 | ジャーニーステップ完了 |
| 英語名 | JourneyStepCompleted |

### 発行タイミング

ジャーニーの1ステップが完了したとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| customerId | UUID | 顧客ID |
| journeyId | UUID | ジャーニーID |
| stepId | String | ステップID |
| outcome | String | 結果 |
| completedAt | DateTime | 完了日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| JourneyExecutionService | 次ステップ評価 |
| AnalyticsService | ステップ統計更新 |

---

## CommunicationDelivered コミュニケーション配信完了

| 項目 | 値 |
|------|-----|
| 日本語名 | コミュニケーション配信完了 |
| 英語名 | CommunicationDelivered |

### 発行タイミング

コミュニケーションが顧客に配信されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| deliveryId | UUID | 配信ID |
| customerId | UUID | 顧客ID |
| communicationId | UUID | コミュニケーションID |
| channel | Enum | チャネル |
| deliveredAt | DateTime | 配信日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| JourneyService | ジャーニーステップ完了 |
| AnalyticsService | 配信統計更新 |
| ProfileService | 接触履歴更新 |

---

## CommunicationOpened コミュニケーション開封

| 項目 | 値 |
|------|-----|
| 日本語名 | コミュニケーション開封 |
| 英語名 | CommunicationOpened |

### 発行タイミング

顧客がコミュニケーションを開封したとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| deliveryId | UUID | 配信ID |
| customerId | UUID | 顧客ID |
| channel | Enum | チャネル |
| openedAt | DateTime | 開封日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| AnalyticsService | 開封統計更新 |
| EngagementScoreService | エンゲージメントスコア更新 |

---

## ConsentUpdated 同意更新

| 項目 | 値 |
|------|-----|
| 日本語名 | 同意更新 |
| 英語名 | ConsentUpdated |

### 発行タイミング

顧客の同意状態が変更されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| customerId | UUID | 顧客ID |
| consentType | Enum | 同意タイプ |
| newStatus | Boolean | 新しい状態 |
| source | String | 変更元 |
| updatedAt | DateTime | 更新日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| DeliveryService | 配信可否更新 |
| JourneyService | 進行中ジャーニー評価 |
| ProfileService | プロファイル更新 |

---

## イベント発行ルール

### 発行タイミングの原則

1. **状態変更時**: 顧客状態の重要な変更時に発行
2. **トランザクション内**: DB更新と同一トランザクションで発行
3. **冪等性**: 同一イベントの再処理が可能

### イベントストア

| 項目 | 値 |
|------|--------|
| ストレージ | Kafka |
| 保持期間 | 90日 |
| パーティション | customerId |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
