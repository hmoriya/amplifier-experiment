# Spirits Development Service（スピリッツ開発サービス）

**プロジェクト:** asashi (Asahi Group Holdings)
**Value Stream:** VS2 製品開発・イノベーション
**作成日:** 2025-11-27
**ステータス:** 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Spirits Development Service |
| **日本語名** | スピリッツ開発サービス |
| **ドメインタイプ** | Core ★★★★☆ |
| **所有チーム** | スピリッツ開発部 |
| **リポジトリ** | `asahi-rnd/spirits-development-service` |

---

## 含まれるBounded Contexts

- **spirits-development BC**
  - 参照: `outputs/3-capabilities/vs2-product-innovation/cl3-bounded-contexts/spirits-development-bc.md`

**単独サービス理由:**
- ビールとは異なる製造技術（蒸留）
- 異なる規制環境
- 長期熟成が必要な製品特性
- 専門チームによる開発

---

## 責務

### ミッション

ウイスキー・RTD・スピリッツ製品の開発を行い、蒸留技術とブレンディング技術を活かした高品質な製品を生み出す。

### 主要責務

1. ウイスキー・RTD・スピリッツ製品開発
2. 蒸留技術研究
3. 熟成管理
4. ブレンディング

---

## ドメインモデル

### Aggregates

```yaml
SpiritsProduct:
  説明: スピリッツ製品
  Root Entity: SpiritsProduct
  Entities:
    - DistillationSpec
    - MaturationSpec
    - BlendingRecipe
  Value Objects:
    - ProductId
    - SpiritType
    - AgeStatement

MaturationBatch:
  説明: 熟成バッチ
  Root Entity: MaturationBatch
  Entities:
    - CaskInfo
    - MaturationHistory
    - QualityMeasurements
  Value Objects:
    - BatchId
    - CaskType
    - StartDate

DistillationRecipe:
  説明: 蒸留レシピ
  Root Entity: DistillationRecipe
  Entities:
    - ProcessSteps
    - CutPoints
  Value Objects:
    - RecipeId
    - StillType
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/spirits-development

Endpoints:
  # 製品管理
  GET /products: 製品一覧
  POST /products: 製品登録
  GET /products/{id}: 製品詳細

  # 熟成バッチ管理
  GET /maturation-batches: 熟成バッチ一覧
  POST /maturation-batches: 熟成バッチ開始
  GET /maturation-batches/{id}: バッチ詳細
  POST /maturation-batches/{id}/measurements: 測定データ追加

  # 蒸留レシピ
  GET /distillation-recipes: レシピ一覧
  POST /distillation-recipes: レシピ作成
```

---

## イベント

### Published Events

```yaml
SpiritsProductCreated: スピリッツ製品作成
MaturationBatchStarted: 熟成開始
MaturationComplete: 熟成完了
ProductBlendFinalized: ブレンド確定
```

### Subscribed Events

```yaml
YeastStrainImproved: (from Fermentation Research)
SensoryEvaluationCompleted: (from R&D Support)
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: spirits_development

Time Series:
  Type: TimescaleDB (PostgreSQL extension)
  Purpose: 熟成データの時系列管理
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Fermentation Research Service | 蒸留用酵母 |

### 利用先

| サービス | 利用内容 |
|----------|----------|
| R&D Support Service | 官能評価依頼 |
| Process Engineering Service | 技術移管依頼 |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 低
  Replicas: 2

SLA: 99.5%

特記事項:
  - 熟成データは長期保存（10年以上）
  - 時系列データの効率的なクエリが必要
```

---

**作成者:** Claude (Parasol V4 Lite)
**最終更新:** 2025-11-27
