# Use Case: 処方作成 (Create Recipe)

## 概要

| 項目 | 内容 |
|------|------|
| UC ID | BC2-UC-001 |
| 名称 | 処方作成 |
| アクター | 製品開発者、醸造技術者 |
| トリガー | 新製品開発プロジェクト開始時、既存製品改良時 |
| 関連集約 | Recipe |

---

## ユースケース記述

### 事前条件 (Preconditions)

1. アクターは認証済みで、処方作成権限を持つ
2. 製品コンセプト（ターゲット、ポジショニング）が決定済み
3. 目標風味プロファイルが定義済み（任意）
4. BC1から酵母株情報が参照可能

### 事後条件 (Postconditions)

1. 新規Recipeエンティティが作成される
2. 一意のRecipeCode（RCP-{ProductType}-YYYYMM-NNN形式）が発行される
3. 初期ステータスは「Draft」
4. RecipeCreatedイベントが発行される

### 基本フロー (Main Flow)

1. **開始**: 開発者が「新規処方作成」を選択
2. **基本情報入力**:
   - 製品名（必須、1-200文字）
   - 製品タイプ（Beer/LowMaltBeer/Happoshu/NonAlcohol/RTD/Spirits）
   - 製品コンセプト（説明、ターゲット消費者、ポジショニング）
3. **原料構成設計**:
   - 原料タイプ選択（Malt/Hop/Yeast/Water/Adjunct/Additive）
   - 各原料の配合比率設定（合計100%）
   - 原料スペック（グレード、産地）設定
4. **製造仕様設定**:
   - 糖化仕様（マッシュ温度、ステップ、時間）
   - 煮沸仕様（時間、ホップ添加タイミング）
   - 発酵仕様（酵母株、接種量、温度、期間）
   - 熟成仕様（温度、期間）
5. **目標風味設定**（任意）:
   - BC1から酵母株の風味プロファイルを参照
   - 目標風味属性の設定
6. **確認・保存**: 入力内容確認後、Draftとして保存
7. **完了**: RecipeCodeと編集画面リンクを表示

### 代替フロー (Alternative Flows)

**A1: 既存処方からの複製**
- ステップ1で「既存処方から複製」を選択
- 既存処方を検索・選択
- 全設定を引き継ぎ、新バージョンとして作成

**A2: テンプレートからの作成**
- ステップ1で「テンプレートから作成」を選択
- 製品タイプに応じた標準テンプレートを選択
- テンプレート値をベースに調整

**A3: BC1酵母推薦からの連携**
- BC1の酵母推薦結果から遷移
- 推薦酵母株と発酵条件がプリセット

### 例外フロー (Exception Flows)

**E1: 配合比率不正**
- 原料配合比率の合計が100%でない場合
- エラーメッセージを表示し、調整を促す

**E2: 酵母株参照エラー**
- 選択した酵母株がBC1で無効化されている場合
- 警告を表示し、代替株の選択を促す

**E3: 必須項目不足**
- 最低限の原料（モルト、水、酵母）が未設定
- エラー箇所を表示し、入力を促す

---

## ビジネスルール

| BR ID | ルール | 検証タイミング |
|-------|--------|----------------|
| BR-101 | RecipeCodeは一意で自動発番 | 保存時 |
| BR-102 | 名称は1-200文字 | 入力時 |
| BR-103 | 原料配合比率の合計は100% | 保存時 |
| BR-104 | Beer/LowMaltBeerはモルト必須 | 保存時 |
| BR-105 | 発酵仕様には有効な酵母株が必要 | 保存時 |
| BR-106 | Draft処方のみ編集可能 | 更新時 |

---

## データ要件

### 入力データ

```yaml
CreateRecipeInput:
  name: string (required, 1-200 chars)
  productType: enum [Beer, LowMaltBeer, Happoshu, NonAlcohol, RTD, Spirits] (required)
  concept:
    description: string (required)
    targetConsumer: string (required)
    positioning: string (optional)
    keyFeatures: array<string> (optional)
    brandId: uuid (optional)
  ingredients: (required, at least 1)
    - ingredientType: enum [Malt, Hop, Yeast, Water, Adjunct, Additive]
      name: string
      ratio: decimal (0-100)
      specification:
        grade: string
        origin: string
  processSpec:
    mashingSpec: (optional for non-beer)
      mashInTemperature: decimal
      mashSteps: array<{temperature, duration, purpose}>
      waterToGrainRatio: decimal
    boilingSpec:
      boilDuration: integer (minutes)
      hopAdditions: array<{hopVariety, amount, additionTime, purpose}>
    fermentationSpec:
      yeastStrainId: uuid (required)
      pitchRate: decimal
      fermentationTemperature: decimal
      fermentationDuration: integer (days)
      attenuationTarget: decimal
    maturationSpec:
      maturationTemperature: decimal
      maturationDuration: integer (days)
  targetProfile: (optional)
    flavorAttributes: map<string, decimal>
  sourceRecipeId: uuid (optional, for cloning)
```

### 出力データ

```yaml
CreateRecipeOutput:
  recipeId: uuid
  recipeCode: string (RCP-BEER-202411-001)
  version: "v1.0.0"
  status: "Draft"
  createdAt: datetime
  editUrl: string
```

---

## 非機能要件

| 項目 | 要件 |
|------|------|
| 応答時間 | 保存処理: 3秒以内 |
| 自動保存 | 5分間隔でドラフト自動保存 |
| 監査ログ | 全作成・編集操作を記録 |
| 同時編集 | 楽観的ロックで競合防止 |

---

## 関連API

- POST `/recipes` - 処方作成
- GET `/recipes/{recipeId}` - 処方詳細取得
- PUT `/recipes/{recipeId}` - 処方更新
- GET `/templates` - テンプレート一覧
- GET `/vs1/yeast-strains/{strainId}` - 酵母株情報取得（BC1連携）

---

## VS間連携

### BC1 FermentationPlatform との連携

- 酵母株情報の参照（strainId, 風味プロファイル）
- 発酵条件の推奨値取得
- YeastStrainOptimizedイベントの購読（処方改訂通知）

---

**作成日**: 2025-11-28
**VS/BC**: VS2/BC2 Product Recipe
