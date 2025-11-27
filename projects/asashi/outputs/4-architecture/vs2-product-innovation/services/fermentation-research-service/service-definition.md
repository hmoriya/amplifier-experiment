# Fermentation Research Service（発酵研究サービス）

**プロジェクト:** asashi (Asahi Group Holdings)
**Value Stream:** VS2 製品開発・イノベーション
**作成日:** 2025-11-27
**ステータス:** 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Fermentation Research Service |
| **日本語名** | 発酵研究サービス |
| **ドメインタイプ** | Core ★★★★★ |
| **所有チーム** | 発酵研究所 |
| **リポジトリ** | `asahi-rnd/fermentation-research-service` |

---

## 含まれるBounded Contexts

- **fermentation-research BC** (CL3定義済み)
  - 参照: `outputs/3-capabilities/vs2-product-innovation/cl3-bounded-contexts/fermentation-research-bc.md`

---

## 責務

### ミッション

100年以上蓄積された醸造技術の中核として、酵母・発酵に関する基盤研究を行い、全製品開発の技術基盤を提供する。アサヒグループの競争優位性の源泉。

### 主要責務

1. 酵母株の探索・収集・育種・保存
2. 発酵条件の最適化研究
3. 発酵実験の実施・検証
4. 技術知見の体系化・特許出願

### スコープ外

- 製品開発（Beer/Spirits/Beverage Development Serviceの責務）
- 素材研究（Ingredient Research Serviceの責務）
- 製造プロセス設計（Process Engineering Serviceの責務）

---

## ドメインモデル

### Aggregates

```yaml
YeastStrain:
  説明: 酵母株とその特性を管理
  Root Entity: YeastStrain
  Entities:
    - StrainCharacteristics（特性情報）
    - GeneticInfo（遺伝子情報）
    - CultureConditions（培養条件）
  Value Objects:
    - StrainId
    - TaxonomyInfo（分類情報）
    - OriginInfo（起源情報）
  不変条件:
    - StrainIdは一意
    - 特性情報は必須

FermentationExperiment:
  説明: 発酵実験の計画・実行・結果を管理
  Root Entity: FermentationExperiment
  Entities:
    - ExperimentConditions（実験条件）
    - MeasurementData（測定データ）
    - AnalysisResults（分析結果）
  Value Objects:
    - ExperimentId
    - TemperatureProfile
    - pHProfile
  不変条件:
    - 実験条件は開始後変更不可
    - 測定データは時系列で記録

ResearchProject:
  説明: 研究プロジェクトの管理
  Root Entity: ResearchProject
  Entities:
    - ProjectMilestones
    - ResourceAllocation
  Value Objects:
    - ProjectId
    - ResearchObjective
  不変条件:
    - プロジェクトは少なくとも1つの目標を持つ

FermentationRecipe:
  説明: 発酵レシピ（製品開発への技術移転用）
  Root Entity: FermentationRecipe
  Entities:
    - ProcessSteps
    - QualityParameters
  Value Objects:
    - RecipeId
    - YeastStrainRef
    - TargetSpecifications
  不変条件:
    - レシピには使用酵母株の参照が必須
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/fermentation-research

Endpoints:
  # 酵母株管理
  GET /yeast-strains:
    説明: 酵母株一覧取得
    Query Parameters:
      - type: string (optional) - フィルタ（beer, distillation, etc.）
      - status: string (optional) - ステータスフィルタ
      - limit: integer (default: 20)
      - offset: integer (default: 0)
    Response: 200 OK - YeastStrainList

  GET /yeast-strains/{id}:
    説明: 酵母株詳細取得
    Path Parameters:
      - id: string (required) - 酵母株ID
    Response: 200 OK - YeastStrain

  POST /yeast-strains:
    説明: 酵母株登録
    Request Body: CreateYeastStrainRequest
    Response: 201 Created - YeastStrain

  PUT /yeast-strains/{id}:
    説明: 酵母株更新
    Request Body: UpdateYeastStrainRequest
    Response: 200 OK - YeastStrain

  # 発酵実験
  GET /experiments:
    説明: 実験一覧取得
    Response: 200 OK - ExperimentList

  POST /experiments:
    説明: 実験登録
    Request Body: CreateExperimentRequest
    Response: 201 Created - FermentationExperiment

  GET /experiments/{id}:
    説明: 実験詳細取得
    Response: 200 OK - FermentationExperiment

  POST /experiments/{id}/measurements:
    説明: 測定データ追加
    Request Body: AddMeasurementRequest
    Response: 201 Created

  # レシピ
  GET /recipes:
    説明: レシピ一覧取得
    Response: 200 OK - RecipeList

  GET /recipes/{id}:
    説明: レシピ詳細取得
    Response: 200 OK - FermentationRecipe

  POST /recipes:
    説明: レシピ作成
    Request Body: CreateRecipeRequest
    Response: 201 Created - FermentationRecipe

  # 研究プロジェクト
  GET /projects:
    説明: プロジェクト一覧
    Response: 200 OK - ProjectList

  POST /projects:
    説明: プロジェクト作成
    Request Body: CreateProjectRequest
    Response: 201 Created - ResearchProject
```

### gRPC（サービス間高速通信）

```protobuf
service FermentationResearchService {
  rpc GetYeastStrain(GetYeastStrainRequest) returns (YeastStrain);
  rpc ListYeastStrains(ListYeastStrainsRequest) returns (stream YeastStrain);
  rpc GetFermentationRecipe(GetRecipeRequest) returns (FermentationRecipe);
}
```

---

## イベント

### Published Events（発行するイベント）

```yaml
YeastStrainRegistered:
  説明: 新規酵母株が登録された
  Payload:
    strainId: string
    name: string
    type: string
    characteristics: object
  Subscribers:
    - Beer Development Service
    - Spirits Development Service

YeastStrainImproved:
  説明: 酵母株が改良された
  Payload:
    strainId: string
    version: integer
    improvements: array
  Subscribers:
    - Beer Development Service
    - Spirits Development Service

FermentationRecipeCreated:
  説明: 新規発酵レシピが作成された
  Payload:
    recipeId: string
    yeastStrainId: string
    targetProduct: string
  Subscribers:
    - Beer Development Service

ResearchKnowledgeDocumented:
  説明: 技術知見が文書化された
  Payload:
    documentId: string
    category: string
    keywords: array
  Subscribers:
    - (内部利用)
```

### Subscribed Events（購読するイベント）

```yaml
# 現時点では外部イベントの購読なし
# 将来的に以下を検討:
# - MarketInsightDiscovered (VS1から) - 市場ニーズに基づく研究方向性
```

---

## データストア

### Primary Database

```yaml
Type: PostgreSQL 15+
Schema: fermentation_research

主要テーブル:
  yeast_strains:
    - id (UUID, PK)
    - strain_code (VARCHAR, UNIQUE)
    - name (VARCHAR)
    - type (VARCHAR)
    - taxonomy_info (JSONB)
    - origin_info (JSONB)
    - status (VARCHAR)
    - created_at (TIMESTAMP)
    - updated_at (TIMESTAMP)

  strain_characteristics:
    - id (UUID, PK)
    - strain_id (UUID, FK)
    - characteristic_type (VARCHAR)
    - value (JSONB)
    - measured_at (TIMESTAMP)

  fermentation_experiments:
    - id (UUID, PK)
    - experiment_code (VARCHAR, UNIQUE)
    - strain_id (UUID, FK)
    - conditions (JSONB)
    - status (VARCHAR)
    - started_at (TIMESTAMP)
    - completed_at (TIMESTAMP)

  experiment_measurements:
    - id (UUID, PK)
    - experiment_id (UUID, FK)
    - measurement_type (VARCHAR)
    - value (NUMERIC)
    - measured_at (TIMESTAMP)

  fermentation_recipes:
    - id (UUID, PK)
    - recipe_code (VARCHAR, UNIQUE)
    - strain_id (UUID, FK)
    - process_steps (JSONB)
    - quality_parameters (JSONB)
    - version (INTEGER)
    - created_at (TIMESTAMP)

  research_projects:
    - id (UUID, PK)
    - project_code (VARCHAR, UNIQUE)
    - name (VARCHAR)
    - objective (TEXT)
    - status (VARCHAR)
    - started_at (DATE)
    - target_completion (DATE)

  knowledge_documents:
    - id (UUID, PK)
    - title (VARCHAR)
    - category (VARCHAR)
    - content (TEXT)
    - keywords (VARCHAR[])
    - created_at (TIMESTAMP)
```

### Secondary Storage

```yaml
Object Storage (S3/MinIO):
  Bucket: fermentation-research-files
  用途:
    - 実験データファイル（CSV, Excel）
    - 分析レポート（PDF）
    - 顕微鏡画像
    - 遺伝子解析データ

Cache (Redis):
  用途:
    - 頻繁にアクセスされるレシピ
    - 酵母特性データのキャッシュ
  TTL: 1時間
```

---

## 依存関係

### 提供先（Downstream）

| サービス | 提供内容 | パターン |
|----------|----------|----------|
| Beer Development Service | 酵母株、発酵レシピ | Customer-Supplier |
| Spirits Development Service | 蒸留用酵母 | Customer-Supplier |

### 連携先（Partnership）

| サービス | 連携内容 |
|----------|----------|
| Ingredient Research Service | 素材×酵母の組み合わせ研究 |

### 依存先（Upstream）

現時点ではなし

---

## 非機能要件

### スケーリング

```yaml
Requirement: 低〜中
Reason: 研究業務は高トランザクションではない
Strategy: Vertical Scaling優先
Replicas: 2-3（可用性確保）

リソース目安:
  CPU: 2 cores
  Memory: 4GB
  Storage: 100GB（データ増加に応じて拡張）
```

### パフォーマンス

```yaml
API Response Time:
  Target: P95 < 500ms
  Acceptable: P99 < 1s

Database Queries:
  Target: P95 < 100ms
```

### 可用性

```yaml
SLA: 99.5%
許容ダウンタイム: 月間約3.6時間
RTO: 4時間
RPO: 1時間
```

---

## セキュリティ

### 認証・認可

```yaml
認証: JWT (OAuth 2.0)
認可: RBAC

ロール:
  researcher:
    - 酵母株の読み書き
    - 実験の作成・実行
    - レシピの作成
  senior_researcher:
    - researcherの全権限
    - プロジェクト管理
    - 知見の公開承認
  viewer:
    - 読み取りのみ
  admin:
    - 全権限
```

### データ保護

```yaml
機密レベル: 高（企業秘密を含む）
暗号化:
  転送中: TLS 1.3
  保存時: AES-256（特に遺伝子情報、レシピ）
アクセスログ: 全操作を記録
```

---

## 監視・運用

### ヘルスチェック

```yaml
Endpoint: /health
チェック項目:
  - Database接続
  - Redis接続
  - Object Storage接続

Liveness: /health/live
Readiness: /health/ready
```

### メトリクス

```yaml
Endpoint: /metrics (Prometheus形式)

主要メトリクス:
  - fermentation_research_yeast_strains_total
  - fermentation_research_experiments_active
  - fermentation_research_recipes_created_total
  - fermentation_research_api_request_duration_seconds
```

### アラート

```yaml
Critical:
  - Database接続エラー
  - API エラー率 > 5%

Warning:
  - API レイテンシ P95 > 1s
  - ディスク使用率 > 80%
```

---

## 開発・デプロイ

### 技術スタック

```yaml
Language: Python 3.11+
Framework: FastAPI
ORM: SQLAlchemy 2.0
Testing: pytest
Container: Docker
Orchestration: Kubernetes
```

### CI/CD

```yaml
Repository: asahi-rnd/fermentation-research-service
Pipeline:
  - Lint (ruff)
  - Type Check (pyright)
  - Unit Tests
  - Integration Tests
  - Build Docker Image
  - Deploy to Staging
  - E2E Tests
  - Deploy to Production
```

---

**作成者:** Claude (Parasol V4 Lite)
**最終更新:** 2025-11-27
