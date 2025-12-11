# Value Objects - BC-003 CRM-CDP 顧客データプラットフォーム

## 概要

本ドキュメントは、BC-003 CRM-CDPの値オブジェクトを定義する。

---

## IdentityGraph ID連携グラフ

| 項目 | 値 |
|------|-----|
| 日本語名 | ID連携グラフ |
| 英語名 | IdentityGraph |

### 説明

顧客の各種IDの連携関係を表すグラフ。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| unifiedId | UUID | 統合顧客ID |
| identifiers | Identifier[] | 連携ID一覧 |
| edges | IdentityEdge[] | ID間の連携 |

---

## Identifier 識別子

| 項目 | 値 |
|------|-----|
| 日本語名 | 識別子 |
| 英語名 | Identifier |

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| type | Enum | タイプ（EMAIL/PHONE/COOKIE/DEVICE_ID/MEMBER_ID） |
| value | String | 識別子の値（ハッシュ化） |
| source | String | データソース |
| confidence | Decimal | 信頼度（0-1） |

---

## CustomerScore 顧客スコア

| 項目 | 値 |
|------|-----|
| 日本語名 | 顧客スコア |
| 英語名 | CustomerScore |

### 説明

顧客に付与された予測スコア。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| scoreType | Enum | スコアタイプ |
| value | Decimal | スコア値（0-100） |
| percentile | Integer | パーセンタイル |
| calculatedAt | DateTime | 計算日時 |
| modelVersion | String | モデルバージョン |

---

## SegmentCondition セグメント条件

| 項目 | 値 |
|------|-----|
| 日本語名 | セグメント条件 |
| 英語名 | SegmentCondition |

### 説明

セグメント抽出の条件定義。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| attribute | String | 属性名 |
| operator | Enum | 演算子 |
| value | Any | 比較値 |
| logicalOperator | Enum | 論理演算子（AND/OR） |

---

## JourneyStep ジャーニーステップ

| 項目 | 値 |
|------|-----|
| 日本語名 | ジャーニーステップ |
| 英語名 | JourneyStep |

### 説明

ジャーニー内の1ステップ。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| stepId | String | ステップID |
| type | Enum | タイプ（ACTION/WAIT/CONDITION/SPLIT） |
| config | JSON | ステップ設定 |
| nextSteps | String[] | 次ステップID |
| position | Position | キャンバス上の位置 |

---

## Consent 同意

| 項目 | 値 |
|------|-----|
| 日本語名 | 同意 |
| 英語名 | Consent |

### 説明

顧客のマーケティング同意状況。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| type | Enum | 同意タイプ（EMAIL/PUSH/SMS/POSTAL） |
| status | Boolean | 同意状態 |
| grantedAt | DateTime | 同意日時 |
| revokedAt | DateTime | 撤回日時 |
| source | String | 取得経路 |

---

## ContactInfo 連絡先情報

| 項目 | 値 |
|------|-----|
| 日本語名 | 連絡先情報 |
| 英語名 | ContactInfo |

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| email | String | メールアドレス（暗号化） |
| phone | String | 電話番号（暗号化） |
| postalCode | String | 郵便番号 |
| prefecture | String | 都道府県 |
| lineId | String | LINE ID |

---

## Demographics 人口統計属性

| 項目 | 値 |
|------|-----|
| 日本語名 | 人口統計属性 |
| 英語名 | Demographics |

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| gender | Enum | 性別 |
| birthYear | Integer | 生年 |
| ageGroup | String | 年齢層 |
| occupation | String | 職業 |
| familyStructure | String | 家族構成 |

---

## PersonalizationContext パーソナライズコンテキスト

| 項目 | 値 |
|------|-----|
| 日本語名 | パーソナライズコンテキスト |
| 英語名 | PersonalizationContext |

### 説明

パーソナライズ判定に使用するコンテキスト情報。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| customerId | UUID | 顧客ID |
| channel | Enum | チャネル |
| device | DeviceInfo | デバイス情報 |
| location | GeoLocation | 位置情報 |
| currentPage | String | 現在のページ |
| sessionData | JSON | セッションデータ |
| timestamp | DateTime | タイムスタンプ |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
