# Beer Development Service（ビール開発サービス）

**プロジェクト:** asashi (Asahi Group Holdings)
**Value Stream:** VS2 製品開発・イノベーション
**作成日:** 2025-11-27
**ステータス:** 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Beer Development Service |
| **日本語名** | ビール開発サービス |
| **ドメインタイプ** | Core ★★★★★ |
| **所有チーム** | ビール開発部 |
| **リポジトリ** | `asahi-rnd/beer-development-service` |

---

## 含まれるBounded Contexts

- **premium-beer-development BC**
  - 参照: `outputs/3-capabilities/vs2-product-innovation/cl3-bounded-contexts/premium-beer-development-bc.md`
- **craft-innovation-development BC**
  - 参照: `outputs/3-capabilities/vs2-product-innovation/cl3-bounded-contexts/craft-innovation-development-bc.md`

**統合理由:**
- 同一の製品カテゴリ（ビール）
- 開発プロセスの類似性
- 酒税法上の同一カテゴリ
- 技術・ノウハウの共有

---

## 責務

### ミッション

プレミアムビール・クラフトビール・革新製品の開発を行い、「期待を超えるおいしさ」を実現する製品を生み出す。

### 主要責務

1. プレミアムビールの製品開発
2. クラフトビール・革新製品の開発
3. 製品コンセプト設計
4. 試作・評価・改良
5. 規格書作成・製造移管

---

## ドメインモデル

### Aggregates

```yaml
BeerProduct:
  説明: ビール製品
  Root Entity: BeerProduct
  Entities:
    - ProductSpecification
    - QualityStandards
    - PackagingSpec
  Value Objects:
    - ProductId
    - BrandName
    - ProductCategory
    - AlcoholContent

DevelopmentProject:
  説明: 開発プロジェクト
  Root Entity: DevelopmentProject
  Entities:
    - Milestones
    - ResourcePlan
    - RiskAssessment
  Value Objects:
    - ProjectId
    - TargetLaunchDate
    - BudgetInfo

Prototype:
  説明: 試作品
  Root Entity: Prototype
  Entities:
    - PrototypeSpec
    - EvaluationResults
  Value Objects:
    - PrototypeId
    - Version
    - EvaluationScore

ProductRecipe:
  説明: 製品レシピ
  Root Entity: ProductRecipe
  Entities:
    - IngredientList
    - ProcessSteps
    - FermentationParams
  Value Objects:
    - RecipeId
    - RecipeVersion
    - YeastStrainRef
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/beer-development

Endpoints:
  # 製品管理
  GET /products: 製品一覧
  GET /products/{id}: 製品詳細
  POST /products: 製品登録
  PUT /products/{id}: 製品更新

  # プロジェクト管理
  GET /projects: プロジェクト一覧
  POST /projects: プロジェクト作成
  GET /projects/{id}: プロジェクト詳細
  PUT /projects/{id}: プロジェクト更新

  # 試作品管理
  GET /prototypes: 試作品一覧
  POST /prototypes: 試作品登録
  POST /prototypes/{id}/evaluate: 試作品評価依頼

  # レシピ管理
  GET /recipes: レシピ一覧
  GET /recipes/{id}: レシピ詳細
  POST /recipes: レシピ作成
```

---

## イベント

### Published Events

```yaml
ProductConceptApproved: コンセプト承認
PrototypeCreated: 試作品作成
ProductSpecificationFinalized: 製品規格確定
ProductTransferredToManufacturing: 製造移管完了
```

### Subscribed Events

```yaml
YeastStrainRegistered: (from Fermentation Research)
YeastStrainImproved: (from Fermentation Research)
FermentationRecipeCreated: (from Fermentation Research)
IngredientRegistered: (from Ingredient Research)
SensoryEvaluationCompleted: (from R&D Support)
PrototypeBatchCompleted: (from R&D Support)
TechnologyTransferValidated: (from Process Engineering)
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: beer_development

Document Store:
  Type: MongoDB
  Purpose: 製品仕様書、評価レポート

Search Engine:
  Type: Elasticsearch
  Purpose: 製品検索（CQRS Query側）

Object Storage:
  Type: S3/MinIO
  Purpose: 製品画像、パッケージデザイン
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Fermentation Research Service | 酵母株、発酵レシピ |
| Ingredient Research Service | 素材情報、配合知見 |

### 利用先（Downstream services Beer Dev calls）

| サービス | 利用内容 |
|----------|----------|
| R&D Support Service | 官能評価依頼、試作依頼 |
| Process Engineering Service | 技術移管依頼 |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 中
  Reason: 開発プロジェクトのピーク時に負荷増加
  Strategy: Horizontal Scaling
  Replicas: 2-4

SLA: 99.5%
```

---

**作成者:** Claude (Parasol V4 Lite)
**最終更新:** 2025-11-27
