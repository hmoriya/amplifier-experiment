# Domain Services - BC-003 CRM-CDP 顧客データプラットフォーム

## 概要

本ドキュメントは、BC-003 CRM-CDPのドメインサービスを定義する。

---

## IdentityResolutionService ID統合サービス

| 項目 | 値 |
|------|-----|
| 日本語名 | ID統合サービス |
| 英語名 | IdentityResolutionService |

### 責務

異なるチャネル・システムの顧客IDを統合し、同一顧客を識別する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| resolveIdentity | Identifier[] | UnifiedCustomerId | ID統合を実行 |
| findMatches | Identifier | MatchCandidate[] | マッチ候補を検索 |
| mergeProfiles | profileId1, profileId2 | CustomerProfile | プロファイルをマージ |
| splitProfile | profileId, identifiers | CustomerProfile[] | 誤統合を分離 |

### ビジネスルール

- 決定論的マッチ（完全一致）を優先
- 確率的マッチは信頼度0.8以上で自動統合
- マージ履歴を完全に保持

---

## SegmentationService セグメンテーションサービス

| 項目 | 値 |
|------|-----|
| 日本語名 | セグメンテーションサービス |
| 英語名 | SegmentationService |

### 責務

セグメントの作成、メンバー計算、更新を行う。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| createSegment | SegmentDefinition | Segment | セグメント作成 |
| calculateMembers | segmentId | MembershipResult | メンバー計算 |
| estimateSize | conditions | SizeEstimate | サイズ見積もり |
| compareSegments | segmentIds[] | ComparisonResult | セグメント比較 |

### ビジネスルール

- メンバー数10人以上必須
- リアルタイムセグメントは条件制限あり

---

## CustomerAnalyticsService 顧客分析サービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 顧客分析サービス |
| 英語名 | CustomerAnalyticsService |

### 責務

顧客行動の分析とインサイト導出を行う。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| analyzeBehavior | segmentId, analysisType | BehaviorAnalysis | 行動分析 |
| identifyPatterns | segmentId | Pattern[] | パターン識別 |
| generateInsights | analysisId | Insight[] | インサイト生成 |
| predictChurn | customerId | ChurnPrediction | 離反予測 |

### ビジネスルール

- 分析結果は匿名化
- 統計的有意性を確認

---

## JourneyOrchestrationService ジャーニーオーケストレーションサービス

| 項目 | 値 |
|------|-----|
| 日本語名 | ジャーニーオーケストレーションサービス |
| 英語名 | JourneyOrchestrationService |

### 責務

カスタマージャーニーの実行を制御する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| enterJourney | customerId, journeyId | JourneyEntry | ジャーニー開始 |
| advanceStep | customerId, journeyId | StepResult | ステップ進行 |
| evaluateCondition | customerId, condition | Boolean | 条件評価 |
| exitJourney | customerId, journeyId, reason | ExitResult | ジャーニー終了 |

### ビジネスルール

- 同一ジャーニーへの重複エントリー制御
- 終了条件成立で強制終了
- ステップ間の待機時間制御

---

## DeliveryService 配信サービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 配信サービス |
| 英語名 | DeliveryService |

### 責務

各チャネルへのコミュニケーション配信を実行する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| sendEmail | recipient, content | DeliveryResult | メール送信 |
| sendPush | recipient, content | DeliveryResult | Push送信 |
| sendSms | recipient, content | DeliveryResult | SMS送信 |
| checkDeliveryStatus | deliveryId | DeliveryStatus | 配信状況確認 |

### ビジネスルール

- オプトアウト顧客には配信しない
- 配信時間制限（深夜配信禁止）
- 頻度制限の遵守

---

## PersonalizationService パーソナライゼーションサービス

| 項目 | 値 |
|------|-----|
| 日本語名 | パーソナライゼーションサービス |
| 英語名 | PersonalizationService |

### 責務

顧客に合わせたコンテンツのパーソナライゼーションを行う。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| personalize | customerId, context, slots | PersonalizedContent | コンテンツパーソナライズ |
| recommend | customerId, context | Recommendation[] | 推奨生成 |
| selectVariant | customerId, experiment | Variant | A/Bテストバリアント選択 |
| trackExposure | customerId, content | TrackingResult | 表示追跡 |

### ビジネスルール

- 100ms以内でレスポンス
- フォールバックコンテンツ必須
- A/Bテストは統計的に管理

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
