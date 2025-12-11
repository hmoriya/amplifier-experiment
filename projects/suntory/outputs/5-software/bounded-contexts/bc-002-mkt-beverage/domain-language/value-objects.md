# Value Objects - BC-002 MKT-Beverage 飲料マーケティング

## 概要

本ドキュメントは、BC-002 MKT-Beverageの値オブジェクトを定義する。

---

## ColorPalette カラーパレット

| 項目 | 値 |
|------|-----|
| 日本語名 | カラーパレット |
| 英語名 | ColorPalette |

### 説明

ブランドのカラー定義。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| primaryColor | ColorCode | メインカラー |
| secondaryColors | ColorCode[] | サブカラー |
| accentColor | ColorCode | アクセントカラー |
| backgroundColors | ColorCode[] | 背景色 |

### 不変条件

- 全カラーは有効なHEX/RGB形式

---

## ColorCode カラーコード

| 項目 | 値 |
|------|-----|
| 日本語名 | カラーコード |
| 英語名 | ColorCode |

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| name | String | 色名 |
| hex | String | HEXコード |
| rgb | String | RGBコード |
| cmyk | String | CMYKコード |
| pantone | String | PANTONEコード（任意） |

---

## Typography タイポグラフィ

| 項目 | 値 |
|------|-----|
| 日本語名 | タイポグラフィ |
| 英語名 | Typography |

### 説明

フォントと文字スタイルの定義。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| headingFont | FontSpec | 見出しフォント |
| bodyFont | FontSpec | 本文フォント |
| accentFont | FontSpec | アクセントフォント（任意） |
| sizeScale | SizeScale | サイズ階層 |

---

## FontSpec フォント仕様

| 項目 | 値 |
|------|-----|
| 日本語名 | フォント仕様 |
| 英語名 | FontSpec |

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| fontFamily | String | フォントファミリー |
| weights | Integer[] | 使用ウェイト |
| fallbacks | String[] | フォールバック |

---

## Budget 予算

| 項目 | 値 |
|------|-----|
| 日本語名 | 予算 |
| 英語名 | Budget |

### 説明

キャンペーンや調査の予算。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| amount | Decimal | 金額 |
| currency | String | 通貨（JPY） |
| fiscalYear | Integer | 会計年度 |
| category | String | 予算カテゴリ |

### 不変条件

- amount >= 0
- currency = "JPY"

---

## MediaBreakdown メディア配分

| 項目 | 値 |
|------|-----|
| 日本語名 | メディア配分 |
| 英語名 | MediaBreakdown |

### 説明

キャンペーンのメディア予算配分。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| tv | Decimal | TV広告比率 |
| digital | Decimal | デジタル広告比率 |
| ooh | Decimal | OOH比率 |
| print | Decimal | 印刷媒体比率 |
| other | Decimal | その他比率 |

### 不変条件

- 全比率の合計 = 100%
- 各比率 >= 0

### メソッド

- `getDigitalDetail()`: デジタル内訳を取得
- `validateTotal()`: 合計が100%か検証

---

## KPITarget KPI目標

| 項目 | 値 |
|------|-----|
| 日本語名 | KPI目標 |
| 英語名 | KPITarget |

### 説明

キャンペーンのKPI目標値。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| metricName | String | 指標名 |
| targetValue | Decimal | 目標値 |
| unit | String | 単位 |
| priority | Enum | 優先度（PRIMARY/SECONDARY） |

---

## ROICalculation ROI計算

| 項目 | 値 |
|------|-----|
| 日本語名 | ROI計算 |
| 英語名 | ROICalculation |

### 説明

キャンペーンのROI算出結果。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| totalInvestment | Decimal | 総投資額 |
| attributedRevenue | Decimal | アトリビューション売上 |
| roi | Decimal | ROI（%） |
| incrementalSales | Decimal | 増分売上 |
| calculationMethod | String | 算出方法 |

### 導出プロパティ

- `roi`: (attributedRevenue - totalInvestment) / totalInvestment × 100

---

## Persona ペルソナ

| 項目 | 値 |
|------|-----|
| 日本語名 | ペルソナ |
| 英語名 | Persona |

### 説明

ターゲット顧客のペルソナ定義。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| name | String | ペルソナ名 |
| demographics | Demographics | 人口統計 |
| psychographics | Psychographics | 心理特性 |
| behaviors | String[] | 行動特性 |
| painPoints | String[] | 課題 |
| goals | String[] | 目標 |

---

## Demographics 人口統計

| 項目 | 値 |
|------|-----|
| 日本語名 | 人口統計 |
| 英語名 | Demographics |

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| ageRange | String | 年齢層（例: 25-34） |
| gender | String | 性別 |
| occupation | String | 職業 |
| income | String | 所得層 |
| location | String | 居住地域 |
| familyStatus | String | 家族構成 |

---

## MarketShare 市場シェア

| 項目 | 値 |
|------|-----|
| 日本語名 | 市場シェア |
| 英語名 | MarketShare |

### 説明

カテゴリ別の市場シェアデータ。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| category | String | カテゴリ |
| period | String | 期間 |
| sharePercentage | Decimal | シェア率（%） |
| rank | Integer | 順位 |
| changeFromPrevious | Decimal | 前期比（pt） |

---

## TrendData トレンドデータ

| 項目 | 値 |
|------|-----|
| 日本語名 | トレンドデータ |
| 英語名 | TrendData |

### 説明

市場・消費者トレンドの測定データ。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| trendName | String | トレンド名 |
| category | String | カテゴリ |
| volume | Long | ボリューム |
| growthRate | Decimal | 成長率（%） |
| relevanceScore | Decimal | 自社関連度 |
| status | Enum | ステータス（RISING/STABLE/DECLINING） |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
