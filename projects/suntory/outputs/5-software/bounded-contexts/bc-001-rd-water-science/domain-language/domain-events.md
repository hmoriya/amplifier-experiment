# Domain Events - BC-001 R&D 水科学

## 概要

本ドキュメントは、BC-001 R&D 水科学のドメインイベントを定義する。

---

## WaterSourceRegistered 水源登録完了

| 項目 | 値 |
|------|-----|
| 日本語名 | 水源登録完了 |
| 英語名 | WaterSourceRegistered |

### 発行タイミング

新規水源が正常に登録されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| sourceId | UUID | 水源ID |
| name | String | 水源名 |
| sourceType | Enum | 水源種別 |
| location | Location | 位置情報 |
| registeredAt | DateTime | 登録日時 |
| registeredBy | UUID | 登録者ID |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| MapUpdateService | 水源マップを更新 |
| NotificationService | 関係者に通知 |
| SUST-Environment BC | 水源情報を同期（外部） |

---

## WaterQualityTestCompleted 水質検査完了

| 項目 | 値 |
|------|-----|
| 日本語名 | 水質検査完了 |
| 英語名 | WaterQualityTestCompleted |

### 発行タイミング

水質検査が完了し、合否判定が確定したとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| testId | UUID | 検査ID |
| sourceId | UUID | 水源ID |
| productCategory | String | 製品カテゴリ |
| conclusion | Enum | 判定（PASS/FAIL/RETEST） |
| testedAt | DateTime | 検査完了日時 |
| testedBy | UUID | 検査担当者ID |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| DashboardService | ダッシュボードKPIを更新 |
| TrendAnalysisService | トレンド分析データを更新 |
| MFG-* BC | 品質情報を同期（外部） |

---

## WaterQualityTestFailed 水質検査不合格

| 項目 | 値 |
|------|-----|
| 日本語名 | 水質検査不合格 |
| 英語名 | WaterQualityTestFailed |

### 発行タイミング

水質検査がFAIL判定となったとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| testId | UUID | 検査ID |
| sourceId | UUID | 水源ID |
| failedParameters | String[] | 不合格パラメータ |
| testedAt | DateTime | 検査完了日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| AlertService | アラートを発行 |
| NotificationService | 品質管理責任者に通知 |
| WaterSourceService | 水源ステータスを確認 |

---

## QualityStandardUpdated 品質基準更新

| 項目 | 値 |
|------|-----|
| 日本語名 | 品質基準更新 |
| 英語名 | QualityStandardUpdated |

### 発行タイミング

品質基準が承認され、有効になったとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| standardId | UUID | 基準ID |
| productCategory | String | 製品カテゴリ |
| version | String | バージョン |
| effectiveFrom | Date | 有効開始日 |
| approvedBy | UUID | 承認者ID |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| TestingService | 新基準を検査に反映 |
| NotificationService | 関係者に通知 |
| MFG-* BC | 基準情報を同期（外部） |

---

## ConservationActivityRecorded 涵養活動記録完了

| 項目 | 値 |
|------|-----|
| 日本語名 | 涵養活動記録完了 |
| 英語名 | ConservationActivityRecorded |

### 発行タイミング

涵養活動が記録されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| activityId | UUID | 活動ID |
| sourceId | UUID | 水源ID |
| activityType | Enum | 活動種別 |
| area | Decimal | 活動面積（ha） |
| activityDate | Date | 活動日 |
| recordedBy | UUID | 記録者ID |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| AreaCalculationService | 累計面積を更新 |
| MapUpdateService | マップの涵養レイヤーを更新 |
| SUST-Environment BC | 涵養データを同期（外部） |

---

## PurificationProcessDesigned 浄水プロセス設計完了

| 項目 | 値 |
|------|-----|
| 日本語名 | 浄水プロセス設計完了 |
| 英語名 | PurificationProcessDesigned |

### 発行タイミング

浄水プロセスの設計が完了し、レビュー待ちになったとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| processId | UUID | プロセスID |
| sourceId | UUID | 対象水源ID |
| productCategory | String | 製品カテゴリ |
| version | String | バージョン |
| designedBy | UUID | 設計者ID |
| designedAt | DateTime | 設計完了日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | レビュアーに通知 |
| WorkflowService | 承認フローを開始 |

---

## PurificationProcessApproved 浄水プロセス承認

| 項目 | 値 |
|------|-----|
| 日本語名 | 浄水プロセス承認 |
| 英語名 | PurificationProcessApproved |

### 発行タイミング

浄水プロセスが承認されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| processId | UUID | プロセスID |
| version | String | バージョン |
| approvedBy | UUID | 承認者ID |
| approvedAt | DateTime | 承認日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | 設計者・関係者に通知 |
| TransferService | 技術移転が可能になったことを通知 |

---

## TechnologyTransferStarted 技術移転開始

| 項目 | 値 |
|------|-----|
| 日本語名 | 技術移転開始 |
| 英語名 | TechnologyTransferStarted |

### 発行タイミング

技術移転が開始されたとき

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| transferId | UUID | 移転ID |
| processId | UUID | プロセスID |
| targetBusinessUnit | String | 移転先事業部 |
| targetFactory | String | 移転先工場 |
| plannedDate | Date | 移転予定日 |
| transferLead | UUID | 移転責任者ID |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | 製造部門に通知 |
| MFG-* BC | 移転情報を受信（外部） |

---

## TechnologyTransferCompleted 技術移転完了

| 項目 | 値 |
|------|-----|
| 日本語名 | 技術移転完了 |
| 英語名 | TechnologyTransferCompleted |

### 発行タイミング

技術移転が正常に完了したとき（検証テスト合格）

### ペイロード

| フィールド | 型 | 説明 |
|------------|-----|------|
| transferId | UUID | 移転ID |
| processId | UUID | プロセスID |
| targetFactory | String | 移転先工場 |
| completedAt | DateTime | 完了日時 |

### 購読者

| 購読者 | 処理内容 |
|--------|----------|
| NotificationService | 関係者に通知 |
| FollowUpService | フォローアップ期間を開始 |
| MFG-* BC | 移転完了を通知（外部） |

---

## イベント発行ルール

### 発行タイミングの原則

1. **即時発行**: 状態変更が確定したらすぐに発行
2. **トランザクション内**: DB更新と同一トランザクションで発行
3. **冪等性**: 同一イベントの再処理が可能

### イベントストア

| 項目 | 値 |
|------|-----|
| ストレージ | Kafka |
| 保持期間 | 90日 |
| パーティション | sourceId または processId |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
