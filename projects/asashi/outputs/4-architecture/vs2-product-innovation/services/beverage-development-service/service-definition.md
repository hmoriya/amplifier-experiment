# Beverage Development Service（飲料開発サービス）

**プロジェクト:** asashi (Asahi Group Holdings)
**Value Stream:** VS2 製品開発・イノベーション
**作成日:** 2025-11-27
**ステータス:** 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Beverage Development Service |
| **日本語名** | 飲料開発サービス |
| **ドメインタイプ** | Core ★★★★☆ |
| **所有チーム** | 飲料開発部 |
| **リポジトリ** | `asahi-rnd/beverage-development-service` |

---

## 含まれるBounded Contexts

- **beverage-development BC**
  - 参照: `outputs/3-capabilities/vs2-product-innovation/cl3-bounded-contexts/beverage-development-bc.md`

**単独サービス理由:**
- 酒類とは異なる規制環境
- 機能性表示食品対応
- 短い製品ライフサイクル
- 異なる市場動向

---

## 責務

### ミッション

清涼飲料・乳製品・機能性飲料・ノンアルコール飲料の開発を行い、健康志向の消費者ニーズに応える製品を生み出す。

### 主要責務

1. 清涼飲料・乳製品の開発
2. 機能性飲料の開発
3. ノンアルコール飲料の開発
4. 健康訴求製品の開発
5. 規制対応（機能性表示食品届出等）

---

## ドメインモデル

### Aggregates

```yaml
BeverageProduct:
  説明: 飲料製品
  Root Entity: BeverageProduct
  Entities:
    - ProductSpec
    - NutritionalInfo
    - HealthClaims
  Value Objects:
    - ProductId
    - BeverageCategory
    - CalorieInfo

FunctionalBeverage:
  説明: 機能性飲料（特化した管理が必要）
  Root Entity: FunctionalBeverage
  Entities:
    - FunctionalClaims
    - RegulatoryApproval
  Value Objects:
    - ClaimType
    - ApprovalStatus

DevelopmentProject:
  説明: 開発プロジェクト
  Root Entity: DevelopmentProject
  Entities:
    - Milestones
    - ResourcePlan
  Value Objects:
    - ProjectId
    - TargetLaunchDate
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/beverage-development

Endpoints:
  # 製品管理
  GET /products: 製品一覧
  POST /products: 製品登録
  GET /products/{id}: 製品詳細
  PUT /products/{id}: 製品更新

  # 機能性表示
  GET /functional-claims: 機能性表示一覧
  POST /functional-claims: 機能性表示申請
  GET /functional-claims/{id}: 表示詳細

  # 規制対応
  POST /regulatory-submissions: 届出提出
  GET /regulatory-submissions/{id}/status: 届出ステータス

  # プロジェクト管理
  GET /projects: プロジェクト一覧
  POST /projects: プロジェクト作成
```

---

## イベント

### Published Events

```yaml
BeverageProductCreated: 飲料製品作成
FunctionalClaimSubmitted: 機能性表示申請
RegulatoryApprovalReceived: 規制承認取得
```

### Subscribed Events

```yaml
IngredientRegistered: (from Ingredient Research)
FunctionalEvidenceValidated: (from Ingredient Research)
SensoryEvaluationCompleted: (from R&D Support)
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: beverage_development
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Ingredient Research Service | 飲料素材、機能性成分、エビデンス |

### 利用先

| サービス | 利用内容 |
|----------|----------|
| R&D Support Service | 官能評価依頼 |
| Process Engineering Service | 技術移管依頼 |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 中
  Reason: 飲料は製品サイクルが短く、開発頻度が高い
  Replicas: 2-3

SLA: 99.5%

特記事項:
  - 規制対応データの長期保存
  - 機能性表示のエビデンス管理
```

---

**作成者:** Claude (Parasol V5)
**最終更新:** 2025-11-27
