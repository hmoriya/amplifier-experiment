# アーキテクチャ設計 - アサヒグループ（修正版）

## 設計原則

**Parasol原則**: 1つのBC = 1つのVS内

7つの境界コンテキストがそれぞれ1つのVSに属する構成。

---

## 1. BC構成サマリー

| VS | BC | ドメインタイプ | アーキテクチャスタイル |
|----|-----|---------------|---------------------|
| VS1 研究開発 | BC1: Fermentation Platform | Core | Hexagonal + Event Sourcing |
| VS1 研究開発 | BC4: Research Innovation | Supporting | Event-Driven |
| VS1 研究開発 | BC6: Functional Research | Supporting | Hexagonal |
| VS2 製品開発 | BC2: Product Recipe | Core | Hexagonal + CQRS |
| VS2 製品開発 | BC5: Product Innovation | Supporting | Event-Driven |
| VS2 製品開発 | BC7: Functional Products | Supporting | Hexagonal |
| VS3 ブランド | BC3: Brand Portfolio | Core | Modular Monolith |

---

## 2. VS別アーキテクチャ

### VS1: 研究開発

```
┌─────────────────────────────────────────────────────────────────┐
│                        VS1: 研究開発                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ BC1: Fermentation   │  │ BC4: Research       │              │
│  │     Platform        │  │    Innovation       │              │
│  │ [Hexagonal+ES]      │  │ [Event-Driven]      │              │
│  │                     │  │                     │              │
│  │ • 酵母ライブラリ     │  │ • セレンディピティ   │              │
│  │ • 発酵プロセス       │  │ • 産学連携          │              │
│  │ • 微生物学研究       │  │ • 研究ポートフォリオ │              │
│  └──────────┬──────────┘  └──────────┬──────────┘              │
│             │ Shared Kernel          │                         │
│             ▼                        ▼                         │
│  ┌─────────────────────────────────────────────┐               │
│  │         BC6: Functional Research            │               │
│  │              [Hexagonal]                    │               │
│  │                                             │               │
│  │ • 乳酸菌研究  • 機能性成分  • 健康効果実証   │               │
│  └─────────────────────────────────────────────┘               │
│                           │                                     │
│                           │ Events (VS境界)                     │
└───────────────────────────┼─────────────────────────────────────┘
                            ▼
                    ┌───────────────┐
                    │  Event Bus    │
                    │   (Kafka)     │
                    └───────────────┘
```

#### BC1: Fermentation Platform

```
┌─────────────────────────────────────────────────────────────┐
│                  Fermentation Platform                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Application Services                    │   │
│  │  • YeastRecommendationService                       │   │
│  │  • FermentationOptimizationService                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Domain Layer                         │   │
│  │  • YeastStrain (Aggregate Root)                     │   │
│  │  • FermentationProcess (Aggregate Root)             │   │
│  │  • FlavorProfile (Value Object)                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Event Store  │  │ TimescaleDB  │  │   Lab LIMS   │      │
│  │  (History)   │  │ (時系列)      │  │  (Adapter)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

### VS2: 製品開発

```
┌─────────────────────────────────────────────────────────────────┐
│                        VS2: 製品開発                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ BC2: Product        │  │ BC5: Product        │              │
│  │     Recipe          │  │    Innovation       │              │
│  │ [Hexagonal+CQRS]    │  │ [Event-Driven]      │              │
│  │                     │  │                     │              │
│  │ • 処方設計          │  │ • 実験的製品        │              │
│  │ • 品質基準          │  │ • 限定品企画        │              │
│  │ • 官能評価          │  │ • コラボ企画        │              │
│  └──────────┬──────────┘  └──────────┬──────────┘              │
│             │ Partnership            │                         │
│             ▼                        ▼                         │
│  ┌─────────────────────────────────────────────┐               │
│  │         BC7: Functional Products            │               │
│  │              [Hexagonal]                    │               │
│  │                                             │               │
│  │ • ノンアル製品  • 機能性飲料  • 低アル製品   │               │
│  └─────────────────────────────────────────────┘               │
│                           │                                     │
│                           │ Events (VS境界)                     │
└───────────────────────────┼─────────────────────────────────────┘
                            ▼
                    ┌───────────────┐
                    │  Event Bus    │
                    └───────────────┘
```

#### BC2: Product Recipe

```
┌─────────────────────────────────────────────────────────────┐
│                      Product Recipe                          │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐    ┌────────────────────┐          │
│  │   Command Side     │    │    Query Side      │          │
│  │  (Write Model)     │    │   (Read Model)     │          │
│  │ • CreateRecipe     │    │ • RecipeSearch     │          │
│  │ • ApproveQuality   │    │ • RecipeCatalog    │          │
│  └─────────┬──────────┘    └─────────┬──────────┘          │
│            ▼                         ▼                      │
│  ┌────────────────────┐    ┌────────────────────┐          │
│  │   PostgreSQL       │    │   Elasticsearch    │          │
│  │  (Master Data)     │    │ (Search/Analytics) │          │
│  └────────────────────┘    └────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

### VS3: ブランド

```
┌─────────────────────────────────────────────────────────────────┐
│                        VS3: ブランド                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              BC3: Brand Portfolio                        │   │
│  │              [Modular Monolith]                         │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │   │
│  │  │   Global     │ │    Local     │ │   Campaign   │     │   │
│  │  │   Brand      │ │    Brand     │ │   Planning   │     │   │
│  │  │   Module     │ │   Module     │ │   Module     │     │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘     │   │
│  │                          │                               │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │          PostgreSQL + Redis Cache               │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 統合アーキテクチャ

### VS間連携（イベント駆動）

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Integration Architecture                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  VS1 研究開発                VS2 製品開発              VS3 ブランド  │
│  ┌───────────┐              ┌───────────┐            ┌───────────┐ │
│  │ BC1       │─── Events ──►│ BC2       │── Events ─►│ BC3       │ │
│  │ BC4       │─── Events ──►│ BC5       │            │           │ │
│  │ BC6       │─── Events ──►│ BC7       │            │           │ │
│  └───────────┘              └───────────┘            └───────────┘ │
│       │                          │                        │        │
│       └──────────────────────────┼────────────────────────┘        │
│                                  ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Event Bus (Apache Kafka)                  │   │
│  │   Topics:                                                    │   │
│  │   • vs1.fermentation.events     (BC1)                       │   │
│  │   • vs1.research-innovation.events (BC4)                    │   │
│  │   • vs1.functional-research.events (BC6)                    │   │
│  │   • vs2.recipe.events           (BC2)                       │   │
│  │   • vs2.product-innovation.events (BC5)                     │   │
│  │   • vs2.functional-products.events (BC7)                    │   │
│  │   • vs3.brand.events            (BC3)                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 連携ルール

| 連携タイプ | パターン | 例 |
|-----------|---------|-----|
| **VS内・同BC** | 直接呼び出し | BC2内のサービス間 |
| **VS内・異BC** | API or Event | BC2 ↔ BC5（Partnership） |
| **VS間** | **Event必須** | BC1 → BC2（VS境界越え） |

### 主要イベント

```yaml
# VS1 → VS2 連携
YeastStrainOptimized:          # BC1 → BC2
  source: vs1.fermentation
  consumer: vs2.recipe
  payload: strainId, optimalConditions

ResearchFindingValidated:      # BC4 → BC5
  source: vs1.research-innovation
  consumer: vs2.product-innovation
  payload: findingId, applicationPotential

FunctionalIngredientApproved:  # BC6 → BC7
  source: vs1.functional-research
  consumer: vs2.functional-products
  payload: ingredientId, evidenceLevel, claims

# VS2 → VS3 連携
ProductApproved:               # BC2 → BC3
  source: vs2.recipe
  consumer: vs3.brand
  payload: productId, productInfo, marketingPoints
```

---

## 4. データアーキテクチャ

### VS別データストア

| VS | BC | Primary Store | Secondary Store |
|----|-----|---------------|-----------------|
| VS1 | BC1 | Event Store + PostgreSQL | TimescaleDB |
| VS1 | BC4 | MongoDB | - |
| VS1 | BC6 | PostgreSQL | - |
| VS2 | BC2 | PostgreSQL | Elasticsearch |
| VS2 | BC5 | MongoDB | - |
| VS2 | BC7 | PostgreSQL | - |
| VS3 | BC3 | PostgreSQL | Redis |

### データ分離原則

```
【原則】
- 各BCは独自のデータストアを持つ
- 他BCのデータは直接参照しない
- データ共有はイベント or API経由

【例外: Shared Kernel】
- VS1内のBC1とBC6は微生物学基礎データを共有
- 共有ライブラリ(microbiology-commons)として提供
```

---

## 5. 技術スタック

### VS別技術選定

| VS | 言語 | フレームワーク | 理由 |
|----|------|---------------|------|
| VS1 研究開発 | Python | FastAPI | データサイエンス連携、研究者親和性 |
| VS2 製品開発 | Java | Spring Boot | エンタープライズ堅牢性 |
| VS3 ブランド | TypeScript | NestJS | マーケティングチーム親和性 |

### 共通インフラ

```yaml
Event Bus: Apache Kafka
Container: Kubernetes
API Gateway: Kong
Observability:
  Logging: ELK Stack
  Metrics: Prometheus + Grafana
  Tracing: Jaeger
CI/CD: GitHub Actions
```

---

## 6. Phase 5用ディレクトリ構造

```
outputs/5-software/
├── VS1_研究開発/
│   ├── BC1_FermentationPlatform/
│   │   ├── domain-language.md
│   │   ├── api-specification.md
│   │   ├── database-design.md
│   │   └── business-operations/
│   │
│   ├── BC4_ResearchInnovation/
│   │   └── ...
│   │
│   └── BC6_FunctionalResearch/
│       └── ...
│
├── VS2_製品開発/
│   ├── BC2_ProductRecipe/
│   │   └── ...
│   │
│   ├── BC5_ProductInnovation/
│   │   └── ...
│   │
│   └── BC7_FunctionalProducts/
│       └── ...
│
└── VS3_ブランド/
    └── BC3_BrandPortfolio/
        └── ...
```

---

## 7. 設計ストーリー

### 修正内容

**旧**: 5つのBC（BC4/BC5がVS横断）
**新**: 7つのBC（全BCが1つのVS内）

### なぜこの構成か

1. **VS = チーム境界**
   - VS1は研究所チーム
   - VS2は商品開発チーム
   - VS3はマーケティングチーム

2. **独立デプロイ可能**
   - VS単位でリリース
   - 他VSに影響なし

3. **技術選択の自由**
   - VS1: Python（研究者向け）
   - VS2: Java（エンタープライズ）
   - VS3: TypeScript（マーケ向け）

---

**作成日**: 2025-11-27（修正版）
**修正内容**: 7BC構成に対応、VS別ディレクトリ構造追加
