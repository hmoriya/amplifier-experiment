# Use Case: 酵母株登録 (Register Yeast Strain)

## 概要

| 項目 | 内容 |
|------|------|
| UC ID | BC1-UC-001 |
| 名称 | 酵母株登録 |
| アクター | 研究員、微生物学者 |
| トリガー | 新規酵母株の採取・取得・育種完了時 |
| 関連集約 | YeastStrain |

---

## ユースケース記述

### 事前条件 (Preconditions)

1. アクターは認証済みで、酵母株登録権限を持つ
2. 酵母株の基本特性データが取得済み
3. 由来情報（採取地、親株など）が確定している

### 事後条件 (Postconditions)

1. 新規YeastStrainエンティティが作成される
2. 一意のStrainCode（ASH-YYYY-NNNN形式）が発行される
3. 初期ステータスは「Research」
4. YeastStrainRegisteredイベントが発行される

### 基本フロー (Main Flow)

1. **開始**: 研究員が「新規酵母株登録」を選択
2. **基本情報入力**:
   - 名称（必須、1-100文字）
   - 由来情報（source, location, collectedAt）
3. **特性情報入力**:
   - アルコール耐性
   - 適温範囲
   - 凝集性（Low/Medium/High）
   - 発酵度範囲
   - 酸素要求量
4. **風味プロファイル入力**（任意）:
   - エステル/フェノール/硫黄レベル
   - フルーティ/スパイシー/クリーン度
5. **確認**: システムが入力データを検証
6. **登録**: データが有効な場合、酵母株を登録
7. **完了**: StrainCodeと登録完了メッセージを表示

### 代替フロー (Alternative Flows)

**A1: 育種株の登録**
- ステップ2で「Bred」を選択した場合
- 親株（parentStrainIds）の入力が必須
- 親株は既存の有効な酵母株でなければならない

**A2: 取得株の登録**
- ステップ2で「Acquired」を選択した場合
- 取得元機関の情報入力が必須

### 例外フロー (Exception Flows)

**E1: 重複チェック失敗**
- 類似の特性を持つ既存株が検出された場合
- 警告を表示し、継続/中止の選択肢を提示

**E2: バリデーションエラー**
- 必須項目未入力またはフォーマット不正
- エラー箇所をハイライトし、修正を促す

---

## ビジネスルール

| BR ID | ルール | 検証タイミング |
|-------|--------|----------------|
| BR-001 | StrainCodeは一意で自動発番 | 登録時 |
| BR-002 | 名称は1-100文字 | 入力時 |
| BR-003 | characteristicsは最低1項目必須 | 登録時 |
| BR-004 | Bredの場合はparentStrainIds必須 | 登録時 |
| BR-005 | 実験用株(Research)は商用利用不可 | ステータス変更時 |

---

## データ要件

### 入力データ

```yaml
RegisterYeastStrainInput:
  name: string (required, 1-100 chars)
  origin:
    source: enum [Natural, Bred, Modified, Acquired] (required)
    location: string (required)
    collectedAt: date (required)
    parentStrainIds: array<uuid> (required if Bred)
  characteristics: (at least one required)
    alcoholTolerance: percentage
    temperatureRange: {min, max}
    flocculationLevel: enum
    attenuationRange: {min, max}
    oxygenRequirement: enum
  flavorProfile: (optional)
    esterLevel: FlavorLevel
    phenolLevel: FlavorLevel
    sulfurLevel: FlavorLevel
    fruitiness: FlavorLevel
    spiciness: FlavorLevel
    cleanness: FlavorLevel
    notes: array<string>
```

### 出力データ

```yaml
RegisterYeastStrainOutput:
  strainId: uuid
  strainCode: string (ASH-YYYY-NNNN)
  status: "Research"
  registeredAt: datetime
```

---

## 非機能要件

| 項目 | 要件 |
|------|------|
| 応答時間 | 登録処理: 2秒以内 |
| 可用性 | 99.5% |
| 監査ログ | 全登録操作を記録 |

---

## 関連API

- POST `/yeast-strains` - 酵母株登録
- GET `/yeast-strains/{strainId}` - 登録確認

---

**作成日**: 2025-11-28
**VS/BC**: VS1/BC1 Fermentation Platform
