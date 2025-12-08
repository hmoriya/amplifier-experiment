# Entities - BC-001 R&D 水科学

## 概要

本ドキュメントは、BC-001 R&D 水科学のエンティティを定義する。

---

## WaterSource 水源

| 項目 | 値 |
|------|-----|
| 日本語名 | 水源 |
| 英語名 | WaterSource |
| 定数名 | WATER_SOURCE |

### 説明

サントリーが利用・保全する水を採取する自然資源。
地下水、湧水、河川など複数の種別がある。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 一意識別子 |
| name | String | Yes | 水源名（例: 阿蘇山系地下水） |
| location | GeoJSON | Yes | 位置情報（Point） |
| address | String | Yes | 所在地住所 |
| sourceType | Enum | Yes | 種別（UNDERGROUND/SPRING/RIVER/OTHER） |
| status | Enum | Yes | 状態（ACTIVE/INACTIVE/UNDER_REVIEW） |
| discoveredAt | Date | Yes | 発見日 |
| owner | String | No | 所有者情報 |
| notes | String | No | 備考 |
| createdAt | DateTime | Yes | 登録日時 |
| updatedAt | DateTime | Yes | 更新日時 |
| createdBy | UUID | Yes | 登録者ID |

### ビジネスルール

- 水源名は一意であること
- 位置情報は日本国内であること
- 半径100m以内に既存水源がないこと（重複防止）

---

## WaterQualityTest 水質検査

| 項目 | 値 |
|------|-----|
| 日本語名 | 水質検査 |
| 英語名 | WaterQualityTest |
| 定数名 | WATER_QUALITY_TEST |

### 説明

水サンプルに対して実施した品質検査の記録。
検査項目ごとの測定値と、品質基準に基づく合否判定を含む。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 検査ID |
| sampleId | UUID | Yes | 水サンプルID |
| sourceId | UUID | Yes | 水源ID（FK） |
| productCategory | String | Yes | 製品カテゴリ |
| standardId | UUID | Yes | 適用した品質基準ID（FK） |
| sampledAt | DateTime | Yes | サンプル採取日時 |
| sampledBy | UUID | Yes | 採取者ID |
| testedAt | DateTime | Yes | 検査完了日時 |
| testedBy | UUID | Yes | 検査担当者ID |
| results | JSON | Yes | 検査結果（項目ごとの測定値） |
| conclusion | Enum | Yes | 判定（PASS/FAIL/RETEST/INVALID） |
| notes | String | No | 備考 |
| createdAt | DateTime | Yes | 登録日時 |

### ビジネスルール

- サンプル採取から48時間以内に検査開始
- 1項目でも基準外ならFAIL判定
- 検査結果は10年以上保持

---

## QualityStandard 品質基準

| 項目 | 値 |
|------|-----|
| 日本語名 | 品質基準 |
| 英語名 | QualityStandard |
| 定数名 | QUALITY_STANDARD |

### 説明

製品カテゴリごとに定義された水質の品質基準。
各パラメータの許容範囲と目標値を定義する。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 基準ID |
| productCategory | String | Yes | 製品カテゴリ |
| version | String | Yes | バージョン（v1.0.0形式） |
| parameters | JSON | Yes | 基準パラメータ（項目ごとの最小/最大/目標） |
| effectiveFrom | Date | Yes | 有効開始日 |
| effectiveTo | Date | No | 有効終了日（次バージョン発効時に設定） |
| status | Enum | Yes | ステータス（DRAFT/PENDING/APPROVED/ACTIVE/EXPIRED） |
| reason | String | Yes | 設定・変更理由 |
| requestedBy | UUID | Yes | 申請者ID |
| approvedBy | UUID | No | 承認者ID |
| approvedAt | DateTime | No | 承認日時 |
| createdAt | DateTime | Yes | 作成日時 |

### ビジネスルール

- 有効開始日は申請日から7営業日以降
- 承認フロー必須
- 緩和変更は追加承認必要
- 全バージョン履歴を無期限保持

---

## ConservationActivity 涵養活動

| 項目 | 値 |
|------|-----|
| 日本語名 | 涵養活動 |
| 英語名 | ConservationActivity |
| 定数名 | CONSERVATION_ACTIVITY |

### 説明

水源涵養のために実施した活動の記録。
植樹、間伐、清掃など様々な活動種別がある。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 活動ID |
| sourceId | UUID | Yes | 水源ID（FK） |
| activityType | Enum | Yes | 活動種別（PLANTING/THINNING/CLEANING/SURVEY/OTHER） |
| activityDate | Date | Yes | 活動日 |
| activityEndDate | Date | No | 活動終了日（複数日の場合） |
| area | Decimal | No | 活動面積（ha） |
| participants | Integer | Yes | 参加人数 |
| description | Text | Yes | 活動内容 |
| attachments | JSON | No | 添付ファイル情報 |
| recordedBy | UUID | Yes | 記録者ID |
| createdAt | DateTime | Yes | 登録日時 |

### ビジネスルール

- 活動日は記録日以前
- 1回の活動は最大100ha
- 添付ファイルは最大10件

---

## PurificationProcess 浄水プロセス

| 項目 | 値 |
|------|-----|
| 日本語名 | 浄水プロセス |
| 英語名 | PurificationProcess |
| 定数名 | PURIFICATION_PROCESS |

### 説明

水源から製品用水を生成するための浄水プロセス設計。
処理ステップとパラメータを定義する。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | プロセスID |
| name | String | Yes | プロセス名 |
| sourceId | UUID | Yes | 対象水源ID（FK） |
| productCategory | String | Yes | 対象製品カテゴリ |
| version | String | Yes | バージョン |
| flowDiagram | Text | Yes | フロー図（SVG） |
| steps | JSON | Yes | 処理ステップ定義 |
| parameters | JSON | Yes | プロセスパラメータ |
| simulationResult | JSON | No | シミュレーション結果 |
| status | Enum | Yes | ステータス（DRAFT/REVIEW/APPROVED） |
| designedBy | UUID | Yes | 設計者ID |
| approvedBy | UUID | No | 承認者ID |
| approvedAt | DateTime | No | 承認日時 |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- シミュレーションで目標品質に到達必須
- 承認済みプロセスのみ技術移転可能
- 全バージョン履歴を保持

---

## TechnologyTransfer 技術移転

| 項目 | 値 |
|------|-----|
| 日本語名 | 技術移転 |
| 英語名 | TechnologyTransfer |
| 定数名 | TECHNOLOGY_TRANSFER |

### 説明

研究開発で確立した浄水技術を製造部門へ移転するプロセスの記録。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 移転ID |
| processId | UUID | Yes | 浄水プロセスID（FK） |
| targetBusinessUnit | String | Yes | 移転先事業部 |
| targetFactory | String | Yes | 移転先工場 |
| plannedDate | Date | Yes | 移転予定日 |
| status | Enum | Yes | ステータス（PLANNED/IN_PROGRESS/COMPLETED/FAILED/CANCELLED） |
| phases | JSON | Yes | フェーズ進捗 |
| documents | JSON | Yes | 技術ドキュメント |
| transferLead | UUID | Yes | 移転責任者ID |
| completedAt | DateTime | No | 完了日時 |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- 承認済みプロセスのみ移転可能
- 3フェーズ（ドキュメント→トレーニング→検証）順次完了
- 検証テスト合格が完了条件
- 完了後3ヶ月はフォローアップ期間

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
