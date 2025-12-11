# Entities - BC-003 CRM-CDP 顧客データプラットフォーム

## 概要

本ドキュメントは、BC-003 CRM-CDPのエンティティを定義する。

---

## CustomerProfile 顧客プロファイル

| 項目 | 値 |
|------|-----|
| 日本語名 | 顧客プロファイル |
| 英語名 | CustomerProfile |
| 定数名 | CUSTOMER_PROFILE |

### 説明

統合された顧客の360度ビュー。複数チャネルのデータを統合した単一顧客像。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 統合顧客ID |
| identityGraph | IdentityGraph | Yes | ID連携グラフ |
| demographics | Demographics | No | 人口統計属性 |
| contactInfo | ContactInfo | No | 連絡先情報 |
| preferences | Preferences | No | 設定・好み |
| consents | Consent[] | Yes | 同意情報 |
| scores | CustomerScore[] | No | 各種スコア |
| segments | UUID[] | No | 所属セグメントID |
| firstSeen | DateTime | Yes | 初回認識日時 |
| lastSeen | DateTime | Yes | 最終認識日時 |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- 統合顧客IDは不変
- 個人情報は暗号化して保存
- 同意情報は必須

---

## Segment セグメント

| 項目 | 値 |
|------|-----|
| 日本語名 | セグメント |
| 英語名 | Segment |
| 定数名 | SEGMENT |

### 説明

共通の特性を持つ顧客グループの定義。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | セグメントID |
| name | String | Yes | セグメント名 |
| description | Text | No | 説明 |
| type | Enum | Yes | タイプ（STATIC/DYNAMIC/PREDICTIVE） |
| conditions | SegmentCondition[] | Yes | 抽出条件 |
| memberCount | Long | Yes | メンバー数 |
| updateFrequency | Enum | Yes | 更新頻度 |
| status | Enum | Yes | ステータス（ACTIVE/INACTIVE/ARCHIVED） |
| createdBy | UUID | Yes | 作成者ID |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- メンバー数は10人以上（個人特定防止）
- DYNAMIC型は自動更新

---

## Journey カスタマージャーニー

| 項目 | 値 |
|------|-----|
| 日本語名 | カスタマージャーニー |
| 英語名 | Journey |
| 定数名 | JOURNEY |

### 説明

顧客の状態遷移に基づく自動化コミュニケーションフロー。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | ジャーニーID |
| name | String | Yes | ジャーニー名 |
| description | Text | No | 説明 |
| entryCondition | Condition | Yes | エントリー条件 |
| steps | JourneyStep[] | Yes | ステップ定義 |
| exitConditions | Condition[] | Yes | 終了条件 |
| status | Enum | Yes | ステータス（DRAFT/ACTIVE/PAUSED/COMPLETED） |
| statistics | JourneyStatistics | No | 実行統計 |
| createdBy | UUID | Yes | 作成者ID |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- 無限ループ禁止
- 終了条件必須

---

## Communication コミュニケーション

| 項目 | 値 |
|------|-----|
| 日本語名 | コミュニケーション |
| 英語名 | Communication |
| 定数名 | COMMUNICATION |

### 説明

顧客への配信コンテンツ定義。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | コミュニケーションID |
| name | String | Yes | 名前 |
| channel | Enum | Yes | チャネル（EMAIL/PUSH/SMS/LINE） |
| content | Content | Yes | コンテンツ |
| personalization | PersonalizationRule[] | No | パーソナライズルール |
| status | Enum | Yes | ステータス |
| createdBy | UUID | Yes | 作成者ID |
| createdAt | DateTime | Yes | 作成日時 |

---

## DeliveryLog 配信ログ

| 項目 | 値 |
|------|-----|
| 日本語名 | 配信ログ |
| 英語名 | DeliveryLog |
| 定数名 | DELIVERY_LOG |

### 説明

コミュニケーション配信の記録。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | ログID |
| customerId | UUID | Yes | 顧客ID |
| communicationId | UUID | Yes | コミュニケーションID |
| journeyId | UUID | No | ジャーニーID |
| channel | Enum | Yes | チャネル |
| status | Enum | Yes | 配信ステータス |
| sentAt | DateTime | Yes | 送信日時 |
| deliveredAt | DateTime | No | 配信日時 |
| openedAt | DateTime | No | 開封日時 |
| clickedAt | DateTime | No | クリック日時 |
| errorCode | String | No | エラーコード |

---

## PredictionModel 予測モデル

| 項目 | 値 |
|------|-----|
| 日本語名 | 予測モデル |
| 英語名 | PredictionModel |
| 定数名 | PREDICTION_MODEL |

### 説明

顧客行動を予測する機械学習モデル。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | モデルID |
| name | String | Yes | モデル名 |
| type | Enum | Yes | タイプ（CHURN/PURCHASE/LTV/ENGAGEMENT） |
| version | String | Yes | バージョン |
| features | FeatureDefinition[] | Yes | 使用特徴量 |
| metrics | ModelMetrics | Yes | 精度指標 |
| status | Enum | Yes | ステータス |
| trainedAt | DateTime | Yes | 学習日時 |
| createdAt | DateTime | Yes | 作成日時 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
