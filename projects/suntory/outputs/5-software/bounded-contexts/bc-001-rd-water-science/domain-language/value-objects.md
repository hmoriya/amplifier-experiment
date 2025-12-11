# Value Objects - BC-001 R&D 水科学

## 概要

本ドキュメントは、BC-001 R&D 水科学の値オブジェクトを定義する。

---

## MineralComposition ミネラル組成

| 項目 | 値 |
|------|-----|
| 日本語名 | ミネラル組成 |
| 英語名 | MineralComposition |

### 説明

水中のミネラル成分構成を表す。製品の味と品質に直接影響する。

### 属性

| 属性 | 型 | 単位 | 説明 |
|------|-----|------|------|
| calcium | Decimal | mg/L | カルシウム |
| magnesium | Decimal | mg/L | マグネシウム |
| sodium | Decimal | mg/L | ナトリウム |
| potassium | Decimal | mg/L | カリウム |
| silica | Decimal | mg/L | シリカ |

### 不変条件

- すべての値は0以上
- 小数点以下3桁まで有効

### 導出プロパティ

- `hardness`: 硬度（カルシウム×2.5 + マグネシウム×4.1）

---

## WaterHardness 硬度

| 項目 | 値 |
|------|-----|
| 日本語名 | 硬度 |
| 英語名 | WaterHardness |

### 説明

水の硬度を表す。日本では軟水が主流。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| value | Decimal | 硬度値（mg/L） |
| category | Enum | 分類（SOFT/MEDIUM/HARD） |

### 不変条件

- value >= 0
- category は value に基づき自動決定
  - SOFT: 0-60
  - MEDIUM: 61-120
  - HARD: 121+

---

## Location 位置情報

| 項目 | 値 |
|------|-----|
| 日本語名 | 位置情報 |
| 英語名 | Location |

### 説明

地理的な位置を表す。水源の位置管理に使用。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| latitude | Decimal | 緯度（-90〜90） |
| longitude | Decimal | 経度（-180〜180） |
| altitude | Decimal | 標高（m）※任意 |

### 不変条件

- 緯度: -90 <= latitude <= 90
- 経度: -180 <= longitude <= 180
- 日本国内の範囲チェック可能

### メソッド

- `distanceTo(other: Location)`: 2点間の距離（km）を計算
- `isWithinJapan()`: 日本国内かどうか判定

---

## ParameterRange パラメータ範囲

| 項目 | 値 |
|------|-----|
| 日本語名 | パラメータ範囲 |
| 英語名 | ParameterRange |

### 説明

品質基準のパラメータ許容範囲を表す。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| parameterName | String | パラメータ名 |
| minValue | Decimal | 最小値 |
| maxValue | Decimal | 最大値 |
| targetValue | Decimal | 目標値 |
| unit | String | 単位 |

### 不変条件

- minValue <= targetValue <= maxValue
- minValue <= maxValue

### メソッド

- `isInRange(value: Decimal)`: 値が範囲内か判定
- `deviationFrom(value: Decimal)`: 目標値からの偏差を計算

---

## TestResult 検査結果

| 項目 | 値 |
|------|-----|
| 日本語名 | 検査結果 |
| 英語名 | TestResult |

### 説明

個別検査項目の測定結果を表す。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| parameterName | String | パラメータ名 |
| measuredValue | Decimal | 測定値 |
| unit | String | 単位 |
| standardRange | ParameterRange | 適用した基準範囲 |
| judgment | Enum | 判定（PASS/FAIL/MARGINAL） |

### 不変条件

- measuredValue は数値
- judgment は standardRange との比較で自動決定

---

## ProcessStep 処理ステップ

| 項目 | 値 |
|------|-----|
| 日本語名 | 処理ステップ |
| 英語名 | ProcessStep |

### 説明

浄水プロセスの1処理ステップを表す。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| stepNumber | Integer | ステップ番号 |
| stepType | Enum | ステップ種別（SEDIMENTATION/FILTRATION/ACTIVATED_CARBON/DISINFECTION/MEMBRANE/OTHER） |
| parameters | Map<String, Decimal> | ステップパラメータ |
| retentionTime | Integer | 滞留時間（分） |

### 不変条件

- stepNumber >= 1
- retentionTime >= 0

---

## TransferPhase 移転フェーズ

| 項目 | 値 |
|------|-----|
| 日本語名 | 移転フェーズ |
| 英語名 | TransferPhase |

### 説明

技術移転の1フェーズを表す。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| phaseNumber | Integer | フェーズ番号（1-3） |
| phaseName | String | フェーズ名 |
| status | Enum | ステータス（NOT_STARTED/IN_PROGRESS/COMPLETED） |
| startedAt | DateTime | 開始日時 |
| completedAt | DateTime | 完了日時 |
| notes | String | 備考 |

### 不変条件

- phaseNumber: 1, 2, 3 のいずれか
- 完了時は completedAt が設定されていること

---

## DateRange 日付範囲

| 項目 | 値 |
|------|-----|
| 日本語名 | 日付範囲 |
| 英語名 | DateRange |

### 説明

開始日と終了日の範囲を表す。

### 属性

| 属性 | 型 | 説明 |
|------|-----|------|
| startDate | Date | 開始日 |
| endDate | Date | 終了日 |

### 不変条件

- startDate <= endDate

### メソッド

- `contains(date: Date)`: 日付が範囲内か判定
- `overlaps(other: DateRange)`: 他の範囲と重複するか判定
- `durationInDays()`: 期間の日数を計算

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
