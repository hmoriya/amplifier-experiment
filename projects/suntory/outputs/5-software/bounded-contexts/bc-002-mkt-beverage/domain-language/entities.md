# Entities - BC-002 MKT-Beverage 飲料マーケティング

## 概要

本ドキュメントは、BC-002 MKT-Beverageのエンティティを定義する。

---

## Brand ブランド

| 項目 | 値 |
|------|-----|
| 日本語名 | ブランド |
| 英語名 | Brand |
| 定数名 | BRAND |

### 説明

サントリーが展開する飲料ブランド。製品群を統括し、ブランド価値を管理する。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | ブランドID |
| name | String | Yes | ブランド名 |
| nameEn | String | Yes | 英語名 |
| category | Enum | Yes | カテゴリ（WATER/TEA/COFFEE/CARBONATED/OTHER） |
| status | Enum | Yes | ステータス（ACTIVE/DORMANT/DISCONTINUED） |
| launchDate | Date | Yes | 発売日 |
| description | Text | Yes | ブランド説明 |
| targetAudience | JSON | Yes | ターゲット定義 |
| positioning | Text | Yes | ポジショニング |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- ブランド名は一意
- ACTIVEブランドには有効なガイドラインが必須

---

## BrandStrategy ブランド戦略

| 項目 | 値 |
|------|-----|
| 日本語名 | ブランド戦略 |
| 英語名 | BrandStrategy |
| 定数名 | BRAND_STRATEGY |

### 説明

ブランドの中長期的な戦略を定義したドキュメント。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 戦略ID |
| brandId | UUID | Yes | ブランドID（FK） |
| version | String | Yes | バージョン |
| vision | Text | Yes | ビジョン |
| mission | Text | Yes | ミッション |
| values | String[] | Yes | ブランドバリュー |
| positioning | Text | Yes | ポジショニングステートメント |
| targetPersonas | JSON | Yes | ターゲットペルソナ |
| status | Enum | Yes | ステータス（DRAFT/REVIEW/APPROVED/ACTIVE/ARCHIVED） |
| effectiveFrom | Date | No | 有効開始日 |
| effectiveTo | Date | No | 有効終了日 |
| approvedBy | UUID | No | 承認者ID |
| approvedAt | DateTime | No | 承認日時 |
| createdAt | DateTime | Yes | 作成日時 |

### ビジネスルール

- 1ブランドにつき有効な戦略は1つのみ
- 承認フロー必須

---

## BrandGuideline ブランドガイドライン

| 項目 | 値 |
|------|-----|
| 日本語名 | ブランドガイドライン |
| 英語名 | BrandGuideline |
| 定数名 | BRAND_GUIDELINE |

### 説明

ブランドの視覚的・言語的アイデンティティを定義したガイドライン。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | ガイドラインID |
| brandId | UUID | Yes | ブランドID（FK） |
| version | String | Yes | バージョン |
| logoRules | JSON | Yes | ロゴ使用ルール |
| colorPalette | JSON | Yes | カラーパレット |
| typography | JSON | Yes | タイポグラフィ |
| toneOfVoice | Text | Yes | トーン&マナー |
| dosDonts | JSON | Yes | OK/NG例 |
| status | Enum | Yes | ステータス（DRAFT/PUBLISHED/ARCHIVED） |
| publishedAt | DateTime | No | 公開日時 |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- 必須セクション：ロゴ、カラー、タイポグラフィ、トーン
- 全バージョン履歴を保持

---

## Campaign キャンペーン

| 項目 | 値 |
|------|-----|
| 日本語名 | キャンペーン |
| 英語名 | Campaign |
| 定数名 | CAMPAIGN |

### 説明

マーケティングキャンペーンの計画と実行を管理する。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | キャンペーンID |
| name | String | Yes | キャンペーン名 |
| brandId | UUID | Yes | ブランドID（FK） |
| objective | Enum | Yes | 目的（AWARENESS/CONSIDERATION/PURCHASE/LOYALTY） |
| description | Text | Yes | 説明 |
| targetSegments | UUID[] | Yes | ターゲットセグメントID |
| startDate | Date | Yes | 開始日 |
| endDate | Date | Yes | 終了日 |
| budget | Decimal | Yes | 予算 |
| channels | String[] | Yes | 使用チャネル |
| status | Enum | Yes | ステータス（DRAFT/PENDING/APPROVED/ACTIVE/PAUSED/COMPLETED/CANCELLED） |
| kpis | JSON | Yes | KPI設定 |
| createdBy | UUID | Yes | 作成者ID |
| approvedBy | UUID | No | 承認者ID |
| createdAt | DateTime | Yes | 作成日時 |
| updatedAt | DateTime | Yes | 更新日時 |

### ビジネスルール

- 予算は承認済み枠内
- KPIは定量的に設定必須
- 承認済みのみ実行可能

---

## CampaignPerformance キャンペーンパフォーマンス

| 項目 | 値 |
|------|-----|
| 日本語名 | キャンペーンパフォーマンス |
| 英語名 | CampaignPerformance |
| 定数名 | CAMPAIGN_PERFORMANCE |

### 説明

キャンペーンの実行結果とパフォーマンスデータ。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | パフォーマンスID |
| campaignId | UUID | Yes | キャンペーンID（FK） |
| date | Date | Yes | 日付 |
| impressions | Long | Yes | インプレッション数 |
| reach | Long | Yes | リーチ数 |
| clicks | Long | Yes | クリック数 |
| conversions | Long | Yes | コンバージョン数 |
| spend | Decimal | Yes | 消化額 |
| channelBreakdown | JSON | Yes | チャネル別内訳 |
| createdAt | DateTime | Yes | 作成日時 |

---

## MarketResearch 市場調査

| 項目 | 値 |
|------|-----|
| 日本語名 | 市場調査 |
| 英語名 | MarketResearch |
| 定数名 | MARKET_RESEARCH |

### 説明

市場調査プロジェクトの管理と結果。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 調査ID |
| name | String | Yes | 調査名 |
| type | Enum | Yes | 調査タイプ（QUANTITATIVE/QUALITATIVE/MIXED） |
| objective | Text | Yes | 調査目的 |
| methodology | Text | Yes | 調査手法 |
| targetAudience | JSON | Yes | 調査対象 |
| sampleSize | Integer | No | サンプルサイズ |
| startDate | Date | Yes | 開始日 |
| endDate | Date | No | 終了日 |
| status | Enum | Yes | ステータス（PLANNING/IN_PROGRESS/ANALYSIS/COMPLETED） |
| budget | Decimal | Yes | 予算 |
| vendor | String | No | 委託先 |
| leadAnalyst | UUID | Yes | 主担当ID |
| createdAt | DateTime | Yes | 作成日時 |

---

## CompetitorProfile 競合プロファイル

| 項目 | 値 |
|------|-----|
| 日本語名 | 競合プロファイル |
| 英語名 | CompetitorProfile |
| 定数名 | COMPETITOR_PROFILE |

### 説明

競合他社の情報を管理する。

### 属性

| 属性 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | UUID | Yes | 競合ID |
| companyName | String | Yes | 企業名 |
| brands | String[] | Yes | 主要ブランド |
| categories | String[] | Yes | 参入カテゴリ |
| marketShare | JSON | No | 市場シェア（カテゴリ別） |
| strengths | Text | No | 強み |
| weaknesses | Text | No | 弱み |
| recentActivities | JSON | No | 最近の動向 |
| updatedAt | DateTime | Yes | 更新日時 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
