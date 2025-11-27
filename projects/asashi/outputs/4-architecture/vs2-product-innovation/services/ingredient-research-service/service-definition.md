# Ingredient Research Service（素材研究サービス）

**プロジェクト:** asashi (Asahi Group Holdings)
**Value Stream:** VS2 製品開発・イノベーション
**作成日:** 2025-11-27
**ステータス:** 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Ingredient Research Service |
| **日本語名** | 素材研究サービス |
| **ドメインタイプ** | Core ★★★★☆ |
| **所有チーム** | 素材研究所 |
| **リポジトリ** | `asahi-rnd/ingredient-research-service` |

---

## 含まれるBounded Contexts

- **ingredient-research BC**
  - 参照: `outputs/3-capabilities/vs2-product-innovation/cl3-bounded-contexts/ingredient-research-bc.md`
- **functional-ingredients BC**
  - 機能性成分（乳酸菌等）の研究

**統合理由:**
- 両BCとも「素材」を扱う研究領域
- 機能性成分は素材の一種として管理
- 同一チームが担当
- データの重複回避

---

## 責務

### ミッション

製品の味・品質・機能性を決定する原材料・素材の研究を行い、製品差別化の源泉となる素材知見を蓄積する。

### 主要責務

1. 原材料の探索・評価・分析
2. 配合研究・レシピ開発
3. 機能性成分（乳酸菌等）の研究
4. 健康効果のエビデンス構築
5. サプライヤー評価

---

## ドメインモデル

### Aggregates

```yaml
Ingredient:
  説明: 原材料・素材の管理
  Root Entity: Ingredient
  Entities:
    - ChemicalProfile
    - PhysicalProperties
    - SupplierInfo
  Value Objects:
    - IngredientId
    - IngredientCategory
    - NutritionalInfo

FormulationRecipe:
  説明: 配合レシピ
  Root Entity: FormulationRecipe
  Entities:
    - RecipeComponents
    - ProcessParameters
  Value Objects:
    - RecipeId
    - TargetProfile
    - CostEstimate

FunctionalCompound:
  説明: 機能性成分
  Root Entity: FunctionalCompound
  Entities:
    - HealthClaims
    - ClinicalEvidence
  Value Objects:
    - CompoundId
    - FunctionalCategory

MicrobialStrain:
  説明: 乳酸菌等の微生物株
  Root Entity: MicrobialStrain
  Entities:
    - StrainCharacteristics
    - FunctionalProperties
  Value Objects:
    - StrainId
    - TaxonomyInfo

Supplier:
  説明: サプライヤー情報
  Root Entity: Supplier
  Entities:
    - QualityAssessment
    - ContractInfo
  Value Objects:
    - SupplierId
    - QualityScore
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/ingredient-research

Endpoints:
  # 素材管理
  GET /ingredients: 素材一覧取得
  GET /ingredients/{id}: 素材詳細取得
  POST /ingredients: 素材登録
  PUT /ingredients/{id}: 素材更新

  # 配合レシピ
  GET /formulations: 配合レシピ一覧
  GET /formulations/{id}: 配合レシピ詳細
  POST /formulations: 配合レシピ作成

  # 機能性成分
  GET /functional-compounds: 機能性成分一覧
  GET /functional-compounds/{id}: 機能性成分詳細
  POST /functional-compounds: 機能性成分登録

  # サプライヤー
  GET /suppliers: サプライヤー一覧
  GET /suppliers/{id}: サプライヤー詳細
  GET /suppliers/{id}/assessments: サプライヤー評価履歴
  POST /suppliers/{id}/assessments: 評価追加
```

---

## イベント

### Published Events

```yaml
IngredientRegistered: 素材登録完了
FormulationRecipeCreated: 配合レシピ作成完了
FunctionalEvidenceValidated: 機能性エビデンス検証完了
SupplierAssessmentCompleted: サプライヤー評価完了
```

### Subscribed Events

```yaml
# 現時点では外部イベントの購読なし
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: ingredient_research

Document Store:
  Type: MongoDB
  Purpose: 非構造化データ（分析レポート、エビデンス文書）

Object Storage:
  Type: S3/MinIO
  Purpose: 分析データファイル、証明書類
```

---

## 依存関係

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Beer Development Service | 麦芽・ホップ素材知見 |
| Beverage Development Service | 飲料素材・機能性成分 |

### 連携先（Partnership）

| サービス | 連携内容 |
|----------|----------|
| Fermentation Research Service | 素材×酵母の組み合わせ研究 |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 低
  Strategy: Vertical Scaling
  Replicas: 2

SLA: 99.5%
```

---

**作成者:** Claude (Parasol V4 Lite)
**最終更新:** 2025-11-27
