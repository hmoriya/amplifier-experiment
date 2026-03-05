---
description: "Software design - domain language, API, DB (parasol5:architecture)"
---

# Phase 5: Software Design - ソフトウェア設計（パラソル設計）

## 設計哲学

### ソフトウェア設計における原則

Phase 5では、Parasolの「**保守性と変更容易性**」を実装レベルで保証する設計を行います：

1. **明確なドメインモデル**
   - ビジネスロジックを明示的に表現
   - 複雑なフレームワークを避ける
   - テストしやすい構造

2. **オペレーション単位の設計**
   - 独立してテスト・デプロイ可能
   - イテレーション開発に適した粒度
   - 変更の影響範囲を限定

3. **シンプルなAPI設計**
   - RESTfulな設計原則
   - 明確なエラーハンドリング
   - バージョニング戦略

詳細は [PHILOSOPHY.md](./PHILOSOPHY.md) を参照してください。

### AD原則適用

> [zigzag-foundations.md](../philosophy/zigzag-foundations.md#axiomatic-designの2つの公理)

**Phase 5チェック**:
- [ ] Aggregate間の直接参照なし（IDのみ）
- [ ] BCあたりAggregate数 3-7
- [ ] CL3↔BC対応がUncoupled/Decoupled
- [ ] BC数/CL3数比率 0.8-1.2

各サービス/Bounded Contextの詳細設計を行います。

## 使用方法

```bash
/parasol5:architecture:software                          # インタラクティブ選択
/parasol5:architecture:software ProductCatalog Core      # サービスとBCを直接指定
```

## 目的

Phase 3で定義したBO（業務オペレーション）とPhase 4で定義したサービス/BCに対して、実装に必要な詳細設計を行います：

- パラソルドメイン言語定義（Parasol Domain Language）
- API仕様（OpenAPI）
- データベース設計
- **BO展開**（Phase 3のBO定義 → Actor UseCases + View定義）
- **VMS4マイルストーン進捗管理**（顧客が全面的に価値を実感している状態への貢献）

### 入力データ

| Phase | 参照する成果物 | 用途 |
|-------|---------------|------|
| Phase 3 | `3-capabilities/{vs}/cl2-subdomain-design.md` | PDL候補（初期）をBC単位で統合 |
| Phase 3 | `3-capabilities/{vs}/cl3-business-operations/` | PDL候補（拡張）+ BO定義をActor UseCase/Viewに展開 |
| Phase 4 | `4-application-design/services/` | サービス/BC境界に基づく設計 |

## Amplifierサブエージェント連携

Phase 5では以下のサブエージェントとDDDワークフローを活用して、詳細設計を深化させます。

### 使用するサブエージェント

| サブエージェント | 用途 | 起動タイミング |
|-----------------|------|---------------|
| **api-contract-designer** | API仕様設計、エンドポイント設計 | API仕様作成時 |
| **contract-spec-author** | ドメイン言語の正式仕様化 | domain-language.md 作成時 |
| **zen-architect** (ARCHITECT) | ドメインモデリング判断 | Aggregate/Entity設計時 |
| **database-architect** | データベーススキーマ最適化 | database-design.md 作成時 |

### DDD ワークフロー連携

複雑なドメインモデリングでは、Amplifier DDDワークフローと連携します：

```
DDDワークフロー連携手順

1. DDDコンテキストをロード（セッション開始時）
   → /ddd:prime

2. ドメイン言語設計の計画
   → /ddd:1-plan "BC: {bc-name} のドメインモデル詳細設計"

3. ドメイン言語ドキュメント生成
   → /ddd:2-docs

4. 実装コード計画（次Phase用の準備）
   → /ddd:3-code-plan

ポイント:
- /ddd:prime で Phase 4 の成果物を参照可能に
- /ddd:1-plan で Aggregate 設計の計画を立てる
- /ddd:2-docs で domain-language.md を生成
```

### api-contract-designer の活用

API仕様設計時に、整合性の取れたAPI設計を支援：

```
Task tool を使用して api-contract-designer を起動：

プロンプト:
「以下のBounded Context に対して、RESTful API仕様を設計してください。

BC名: {bc-name}
ドメイン言語: {domain-language.md の内容}

設計要件:
1. CRUD操作の基本エンドポイント
2. 検索・フィルタリングエンドポイント
3. バッチ操作（必要に応じて）
4. エラーレスポンスの標準化

出力形式: OpenAPI 3.0 YAML」
```

### contract-spec-author の活用

ドメイン言語を正式な仕様ドキュメントとして整備：

```
Task tool を使用して contract-spec-author を起動：

プロンプト:
「以下のドメインモデルを正式なContract仕様として整備してください。

入力: {domain-language.md の内容}

整備対象:
1. Aggregateの不変条件（Invariants）の形式化
2. Value Objectのバリデーションルール
3. Domain Eventのペイロード仕様
4. Repository契約の明確化

出力形式: Parasol Contract Specification」
```

### database-architect の活用

Phase 4で設計したデータモデルをデータベース設計に変換：

```
Task tool を使用して database-architect を起動：

プロンプト:
「以下のドメインモデルに対して、データベース設計を行ってください。

ドメイン言語: {domain-language.md の内容}
データベース: PostgreSQL 15+

設計対象:
1. テーブル構造（正規化レベル: 3NF基準）
2. インデックス戦略（検索パターン考慮）
3. 外部キー制約
4. 集約境界に基づくトランザクション境界

パフォーマンス考慮:
- 主要クエリパターン: {想定されるクエリ}
- 予想データ量: {概算}」
```

### 設計ストーリー出力

Phase 5では以下の設計判断理由を自動出力します：

| 設計判断 | 出力される理由 |
|----------|---------------|
| Aggregate境界 | なぜこのエンティティをAggregateRootとしたか |
| Value Object選択 | なぜこの概念をValue Objectとしたか |
| API設計 | エンドポイント構造の設計根拠 |
| インデックス | パフォーマンス考慮の背景 |

**出力先**: `outputs/5-software/services/{service}/{bc}/design-story.md`

### ナレッジ蓄積

設計パターンをナレッジベースに蓄積：

```yaml
# outputs/5-software/design-patterns.json
{
  "project": "{project-name}",
  "bc": "{bc-name}",
  "patterns_used": [
    {
      "pattern": "Repository Pattern",
      "applied_to": "ProductRepository",
      "reason": "永続化の抽象化と集約境界の維持"
    },
    {
      "pattern": "Domain Event",
      "applied_to": "ProductCreated",
      "reason": "他BCへの通知とAudit Trail"
    }
  ],
  "created_at": "timestamp"
}
```

## プロジェクト検出

**重要**: このコマンドはParasolプロジェクト内で実行する必要があります。

### 自動検出

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：

1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)
3. **祖父ディレクトリ** (`../..`)

### 検出成功

```
✅ プロジェクト検出: {project-name}

プロジェクトディレクトリ: projects/{project-name}/
出力先: projects/{project-name}/outputs/
```

プロジェクト設定を読み込み、Phase進捗を自動記録します。

### 検出失敗

```
❌ Parasolプロジェクトが見つかりません

次のアクションを選択してください:

1. 新しいプロジェクトを作成
   → /value5:init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol5:project list
```

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/value5:context

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/value5:context  # ❌
```

詳細は `.claude/commands/parasol/_project-detection.md` を参照。

## 成果物構造

```
outputs/5-software/
└── {service-name}/                       # サービス（デプロイ単位）
    └── {bc-name}/                        # ★ BCが設計単位（kebab-case）
        │
        ├── domain-language.md            # パラソルドメイン言語（SSOT）
        ├── api-specification.md          # API仕様
        ├── database-design.md            # DB設計（生成物）
        │
        ├── operations/                   # オペレーション群
        │   └── {operation-name}/
        │       ├── operation.md          # オペレーション定義
        │       └── actor-usecases/       # Actor UseCase群
        │           └── {auc-name}/       # Actor UseCase
        │               ├── actor-usecase.md
        │               ├── robustness.md
        │               └── views/        # View群
        │                   └── {view}.md
        │
        └── tests/                        # ★ テスト定義（設計側）
            │
            ├── _bc-release-criteria.yaml    # BCリリース基準
            ├── shared/                      # BC共通（ドメインモデル）
            │   └── unit-spec.yaml           # ← domain-language.mdから生成
            │
            └── {operation-name}/            # ★ オペレーション単位（イテレーション）
                ├── _done-criteria.yaml      # オペレーション完了基準（DoD）
                ├── api-spec.yaml            # ← operation.mdから生成
                ├── ui-spec.yaml             # ← views/*.mdから生成
                └── integration-spec.yaml    # ← actor-usecases/*.mdから生成
```

**重要**:
- BC名は `{bc-name}` 形式（kebab-case）。`{capability-name}-bc` 形式は使用しない。
- **イテレーション単位**: オペレーション毎に設計→実装→テストを回す
- **リリース単位**: BC全体（全オペレーション完了時）

例：

```
outputs/5-software/
├── product-service/                      # サービス名（kebab-case）
│   └── product-catalog/                  # BC名（kebab-case）
│       ├── domain-language.md
│       ├── api-specification.md
│       ├── database-design.md
│       ├── operations/
│       │   ├── create-product/           # イテレーション1
│       │   │   ├── operation.md
│       │   │   └── actor-usecases/
│       │   │       └── auc-create-product/
│       │   │           ├── actor-usecase.md
│       │   │           ├── robustness.md
│       │   │           └── views/
│       │   │               └── create-product-form.md
│       │   └── search-products/          # イテレーション2
│       │       └── ...
│       └── tests/
│           ├── _bc-release-criteria.yaml # BCリリース判定
│           ├── shared/                   # BC共通
│           │   └── unit-spec.yaml
│           ├── create-product/           # イテレーション1のテスト
│           │   ├── _done-criteria.yaml
│           │   ├── api-spec.yaml
│           │   ├── ui-spec.yaml
│           │   └── integration-spec.yaml
│           └── search-products/          # イテレーション2のテスト
│               └── ...
│
├── order-service/
│   └── order-management/
│       └── ...
└── ...
```

参照: [capability-bc-test-structure.md](./_software-design-reference/capability-bc-test-structure.md)

## 実行手順

### インタラクティブモード

パラメータなしで実行すると、サービス/BC選択画面を表示：

```
Software Design 対象選択

Phase 4で定義されたサービス:

✅ ProductCatalog/Core
ステータス: 設計完了
成果物: 4/4

⏸️ Order/Management
ステータス: 未着手
成果物: 0/4

⏸️ Order/Payment
ステータス: 未着手
成果物: 0/4

⏸️ Pricing/Core
ステータス: 未着手
成果物: 0/4

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選択してください (番号またはサービス/BC名):
1. ProductCatalog/Core (完了済み - 再編集)
2. Order/Management (推奨: 次に着手)
3. Order/Payment
4. Pricing/Core
...

>
```

### ステップ1: パラソルドメイン言語定義

パラソルドメイン言語（Parasol Domain Language）で、BC内のドメインモデルを定義します。

#### PDL候補の統合

**Phase 3のPDL候補をBC単位で統合・正式化:**

```
【入力: Phase 3 PDL候補】
CL2: PDL候補（初期）
  └── アクター候補、エンティティ候補、状態候補
        ↓
CL3/BO: PDL候補（拡張）
  └── アクター詳細、エンティティ属性、状態遷移詳細
        ↓
【Phase 5: BC単位で統合】
複数ケイパビリティのPDL候補 → 1つのdomain-language.md

統合時の作業:
1. 重複アクターの統合（同一役割の名寄せ）
2. エンティティの集約化（Aggregate Root決定）
3. 状態遷移の整合性確認
4. 業務用語のユビキタス言語化
```

**参照ファイル:**
- `3-capabilities/{vs}/cl2-subdomain-design.md` → PDL候補（初期）
- `3-capabilities/{vs}/cl3-business-operations/{cap}-operations.md` → PDL候補（拡張）

**成果物**: `domain-language.md`

```yaml
# ProductCatalog BC - Domain Language

## Aggregates

Product Aggregate:
Root Entity: Product
Properties:
- productId: ProductId (識別子)
- name: ProductName (名前)
- description: ProductDescription (説明)
- categoryId: CategoryId (カテゴリ)
- status: ProductStatus (ステータス)
- specifications: List<ProductSpecification> (仕様リスト)
- images: List<ProductImage> (画像リスト)
Invariants:
- 名前は必須で1-200文字
- 有効なカテゴリが存在すること
- アクティブ製品は最低1つの画像が必要
Behaviors:
- create(): 新規製品作成
- updateInfo(): 基本情報更新
- addSpecification(): 仕様追加
- addImage(): 画像追加
- activate(): アクティブ化
- discontinue(): 販売終了

Entity: ProductSpecification
Properties:
- specId: SpecificationId
- name: string
- value: string
- unit: string (optional)
Invariants:
- 名前と値は必須

Entity: ProductImage
Properties:
- imageId: ImageId
- url: ImageUrl
- altText: string
- displayOrder: int
- isPrimary: boolean
Invariants:
- URLは有効な形式
- displayOrderは正の整数

Category Aggregate:
Root Entity: Category
Properties:
- categoryId: CategoryId
- name: CategoryName
- parentId: CategoryId (optional)
- path: CategoryPath (階層パス)
- displayOrder: int
Invariants:
- ルートカテゴリ以外は親が必須
- 名前は一意（同一階層内）
- 循環参照なし
Behaviors:
- create(): カテゴリ作成
- updateName(): 名前変更
- move(): 親変更
- reorder(): 表示順変更

## Value Objects

ProductId:
Type: UUID
Validation: 有効なUUID形式

ProductName:
Type: String
Validation: 1-200文字、空白のみ不可

ProductDescription:
Type: String
Validation: 0-5000文字

ProductStatus:
Type: Enum
Values: [Draft, Active, Discontinued]
Default: Draft

CategoryId:
Type: UUID
Validation: 有効なUUID形式

CategoryPath:
Type: String
Format: "/parent/child/grandchild"
Validation: パス形式、最大深さ5階層

ImageUrl:
Type: String
Validation: 有効なHTTP(S) URL、画像拡張子

## Domain Events

ProductCreated:
Properties:
- productId: ProductId
- name: ProductName
- categoryId: CategoryId
- createdAt: DateTime
Trigger: Product.create()

ProductUpdated:
Properties:
- productId: ProductId
- updatedFields: Map<string, any>
- updatedAt: DateTime
Trigger: Product.updateInfo()

ProductDiscontinued:
Properties:
- productId: ProductId
- reason: string
- discontinuedAt: DateTime
Trigger: Product.discontinue()

CategoryCreated:
Properties:
- categoryId: CategoryId
- name: CategoryName
- parentId: CategoryId (optional)
- createdAt: DateTime
Trigger: Category.create()

## Domain Services

ProductSearchService:
Responsibility: 複雑な製品検索ロジック
Methods:
- searchByKeyword(keyword, filters): List<Product>
- searchByCategory(categoryId, includeSubcategories): List<Product>
- searchBySimilarity(productId): List<Product>

CategoryHierarchyService:
Responsibility: カテゴリ階層の操作
Methods:
- getFullPath(categoryId): CategoryPath
- getAllDescendants(categoryId): List<Category>
- validateMove(categoryId, newParentId): ValidationResult

## Repositories

ProductRepository:
Methods:
- save(product: Product): void
- findById(id: ProductId): Product
- findByCategory(categoryId: CategoryId): List<Product>
- delete(id: ProductId): void

CategoryRepository:
Methods:
- save(category: Category): void
- findById(id: CategoryId): Category
- findByParent(parentId: CategoryId): List<Category>
- findAll(): List<Category>
```

### ステップ2: API仕様

OpenAPI 3.0形式でAPI仕様を定義します。

**成果物**: `api-specification.md`

```yaml
openapi: 3.0.3
info:
title: Product Catalog API
version: 1.0.0
description: 製品カタログ管理API

servers:
- url: https://api.example.com/v1
description: Production
- url: https://api-staging.example.com/v1
description: Staging

paths:
/products:
get:
summary: 製品一覧取得
operationId: listProducts
tags: [Products]
parameters:
- name: category
in: query
schema:
type: string
format: uuid
- name: status
in: query
schema:
type: string
enum: [draft, active, discontinued]
- name: keyword
in: query
schema:
type: string
- name: page
in: query
schema:
type: integer
default: 1
- name: pageSize
in: query
schema:
type: integer
default: 20
responses:
'200':
description: 成功
content:
application/json:
schema:
$ref: '#/components/schemas/ProductList'

post:
summary: 製品作成
operationId: createProduct
tags: [Products]
requestBody:
required: true
content:
application/json:
schema:
$ref: '#/components/schemas/CreateProductRequest'
responses:
'201':
description: 作成成功
content:
application/json:
schema:
$ref: '#/components/schemas/Product'
'400':
description: バリデーションエラー
content:
application/json:
schema:
$ref: '#/components/schemas/Error'

/products/{productId}:
get:
summary: 製品詳細取得
operationId: getProduct
tags: [Products]
parameters:
- name: productId
in: path
required: true
schema:
type: string
format: uuid
responses:
'200':
description: 成功
content:
application/json:
schema:
$ref: '#/components/schemas/Product'
'404':
description: 製品が見つからない

put:
summary: 製品更新
operationId: updateProduct
tags: [Products]
parameters:
- name: productId
in: path
required: true
schema:
type: string
format: uuid
requestBody:
required: true
content:
application/json:
schema:
$ref: '#/components/schemas/UpdateProductRequest'
responses:
'200':
description: 更新成功
content:
application/json:
schema:
$ref: '#/components/schemas/Product'

delete:
summary: 製品削除
operationId: deleteProduct
tags: [Products]
parameters:
- name: productId
in: path
required: true
schema:
type: string
format: uuid
responses:
'204':
description: 削除成功

/categories:
get:
summary: カテゴリ一覧取得
operationId: listCategories
tags: [Categories]
responses:
'200':
description: 成功
content:
application/json:
schema:
type: array
items:
$ref: '#/components/schemas/Category'

components:
schemas:
Product:
type: object
properties:
productId:
type: string
format: uuid
name:
type: string
description:
type: string
categoryId:
type: string
format: uuid
status:
type: string
enum: [draft, active, discontinued]
specifications:
type: array
items:
$ref: '#/components/schemas/ProductSpecification'
images:
type: array
items:
$ref: '#/components/schemas/ProductImage'
createdAt:
type: string
format: date-time
updatedAt:
type: string
format: date-time

CreateProductRequest:
type: object
required: [name, categoryId]
properties:
name:
type: string
minLength: 1
maxLength: 200
description:
type: string
maxLength: 5000
categoryId:
type: string
format: uuid

# [その他のスキーマ定義...]
```

### ステップ3: データベース設計

テーブル構造とインデックスを定義します。

**成果物**: `database-design.md`

```yaml
# ProductCatalog BC - Database Design

Database: PostgreSQL 15+

## Tables

products:
Columns:
- product_id: UUID PRIMARY KEY
- name: VARCHAR(200) NOT NULL
- description: TEXT
- category_id: UUID NOT NULL REFERENCES categories(category_id)
- status: VARCHAR(20) NOT NULL DEFAULT 'draft'
- created_at: TIMESTAMP NOT NULL DEFAULT NOW()
- updated_at: TIMESTAMP NOT NULL DEFAULT NOW()
- created_by: UUID
- updated_by: UUID

Indexes:
- PRIMARY KEY (product_id)
- INDEX idx_products_category (category_id)
- INDEX idx_products_status (status)
- INDEX idx_products_name (name) USING gin(to_tsvector('english', name))
- INDEX idx_products_created (created_at DESC)

Constraints:
- CHECK (status IN ('draft', 'active', 'discontinued'))
- CHECK (LENGTH(name) >= 1)

Triggers:
- update_timestamp: updated_atを自動更新

product_specifications:
Columns:
- spec_id: UUID PRIMARY KEY
- product_id: UUID NOT NULL REFERENCES products(product_id) ON DELETE CASCADE
- name: VARCHAR(100) NOT NULL
- value: VARCHAR(500) NOT NULL
- unit: VARCHAR(50)
- display_order: INTEGER NOT NULL DEFAULT 0

Indexes:
- PRIMARY KEY (spec_id)
- INDEX idx_spec_product (product_id)
- UNIQUE INDEX idx_spec_product_name (product_id, name)

Constraints:
- CHECK (LENGTH(name) >= 1)
- CHECK (LENGTH(value) >= 1)

product_images:
Columns:
- image_id: UUID PRIMARY KEY
- product_id: UUID NOT NULL REFERENCES products(product_id) ON DELETE CASCADE
- url: VARCHAR(1000) NOT NULL
- alt_text: VARCHAR(200)
- display_order: INTEGER NOT NULL DEFAULT 0
- is_primary: BOOLEAN NOT NULL DEFAULT FALSE
- created_at: TIMESTAMP NOT NULL DEFAULT NOW()

Indexes:
- PRIMARY KEY (image_id)
- INDEX idx_images_product (product_id, display_order)
- INDEX idx_images_primary (product_id, is_primary) WHERE is_primary = TRUE

Constraints:
- CHECK (url LIKE 'http%')

categories:
Columns:
- category_id: UUID PRIMARY KEY
- name: VARCHAR(100) NOT NULL
- parent_id: UUID REFERENCES categories(category_id)
- path: VARCHAR(500) NOT NULL
- display_order: INTEGER NOT NULL DEFAULT 0
- created_at: TIMESTAMP NOT NULL DEFAULT NOW()
- updated_at: TIMESTAMP NOT NULL DEFAULT NOW()

Indexes:
- PRIMARY KEY (category_id)
- INDEX idx_categories_parent (parent_id)
- INDEX idx_categories_path (path) USING btree
- UNIQUE INDEX idx_categories_parent_name (COALESCE(parent_id, '00000000-0000-0000-0000-000000000000'::UUID), name)

Constraints:
- CHECK (category_id != parent_id) -- 自己参照防止
- CHECK (LENGTH(name) >= 1)

## Views

active_products_view:
Definition: |
CREATE VIEW active_products_view AS
SELECT
p.product_id,
p.name,
p.description,
c.name AS category_name,
c.path AS category_path,
COUNT(pi.image_id) AS image_count
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN product_images pi ON p.product_id = pi.product_id
WHERE p.status = 'active'
GROUP BY p.product_id, p.name, p.description, c.name, c.path

## Functions

update_product_updated_at():
Purpose: updated_atを自動更新
Definition: |
CREATE OR REPLACE FUNCTION update_product_updated_at()
RETURNS TRIGGER AS $$
BEGIN
NEW.updated_at = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

## Migration Strategy

初期マイグレーション:
- V001__create_categories_table.sql
- V002__create_products_table.sql
- V003__create_product_specifications_table.sql
- V004__create_product_images_table.sql
- V005__create_indexes.sql
- V006__create_views.sql
- V007__insert_initial_data.sql

データ投入:
- サンプルカテゴリ
- テスト製品データ

## Data Retention

製品データ:
- 削除されたら論理削除（deleted_atカラム追加検討）
- 監査ログは別テーブルで永続保存

画像データ:
- S3等のオブジェクトストレージに保存
- URLのみDBに保存
```

### ステップ4: BO展開（Actor UseCase + View定義）

**Phase 3で定義されたBO（業務オペレーション）** を基に、Actor UseCaseとView定義を作成します。

#### WHAT/HOW軸の確認

```
【WHAT軸: Capability階層】         【HOW軸: Process階層】
CL3（詳細能力）                    BO（業務オペレーション）
  │                                 │
  │ uses (N:M)                      │ decomposes
  └─────────────────────────────────┘
                                    ↓
                              Actor UseCase（単一アクター）
                                    ↓
                                  View
```

**重要**:
- CL3（WHAT）とBO（HOW）は**並列な2軸**（BIZBOK Capability/Process分離に準拠）
- BOはCL3を「使用」して業務を実行（N:M関係）
- Actor UseCaseはBOをさらに単一アクター操作に分解

> **入力**: Phase 3の `3-capabilities/cl3-bo-definitions/{capability}/bo-*.md`（使用するCL3含む）
> **出力**: Actor UseCase定義とView定義

**成果物**: `operations/{operation-name}/actor-usecases/{auc-name}/actor-usecase.md`, `views/{view}.md`

#### actor-usecase.md の例

```yaml
# Actor UseCase: 製品作成

## 概要
新しい製品をカタログに追加する（単一ユーザの完結操作）

## アクター
- Primary: 製品管理者
- Secondary: システム

## 前提条件
- ユーザーは製品管理者権限を持つ
- カテゴリが存在する

## 基本フロー
1. ユーザーが「新規製品」を選択
2. システムが製品作成フォームを表示
3. ユーザーが製品情報を入力:
- 製品名（必須）
- 説明
- カテゴリ選択（必須）
- 仕様（複数）
- 画像（複数）
4. ユーザーが「保存」を選択
5. システムが入力を検証
6. システムが製品を作成（ステータス: Draft）
7. システムがProductCreatedイベントを発行
8. システムが成功メッセージを表示
9. システムが製品詳細画面に遷移

## 代替フロー

### 3a. バリデーションエラー
3a1. システムがエラーメッセージを表示
3a2. ユーザーが入力を修正
3a3. 基本フロー4に戻る

### 5a. 同名製品が存在
5a1. システムが警告を表示
5a2. ユーザーが確認するか修正
5a3. 基本フロー4に戻る

## 事後条件
- 製品がDraftステータスで作成される
- ProductCreatedイベントが発行される
- 監査ログに記録される

## ビジネスルール
- BR-001: 製品名は1-200文字
- BR-002: カテゴリは必須
- BR-003: アクティブ化には最低1つの画像が必要

## 非機能要件
- パフォーマンス: 3秒以内にレスポンス
- 可用性: 99.9%
- セキュリティ: 製品管理者権限必須
```

#### view.md の例

```yaml
# View: 製品作成画面

## View ID
create-product-view

## URL
/products/new

## レイアウト
- Header: アプリケーションヘッダー
- Main: 製品作成フォーム
- Footer: アクションボタン

## コンポーネント

### ProductCreateForm
Type: Form
Fields:
- productName:
Label: 製品名
Type: TextInput
Required: true
MaxLength: 200
Placeholder: "製品名を入力"
Validation: "1-200文字"

- description:
Label: 説明
Type: TextArea
Required: false
MaxLength: 5000
Rows: 5
Placeholder: "製品の詳細説明"

- categoryId:
Label: カテゴリ
Type: Select
Required: true
Options: カテゴリAPI（/api/categories）から取得
EmptyOption: "カテゴリを選択"

- specifications:
Label: 仕様
Type: DynamicList
ItemFields:
- name: TextInput (required)
- value: TextInput (required)
- unit: TextInput (optional)
AddButtonLabel: "+ 仕様を追加"
RemoveButtonLabel: "削除"

- images:
Label: 画像
Type: FileUpload
Multiple: true
Accept: "image/*"
MaxFiles: 10
MaxFileSize: 5MB
PreviewMode: true

### ActionButtons
Buttons:
- Save:
Label: "保存"
Type: Primary
Action: POST /api/products
SuccessRedirect: /products/{productId}

- Cancel:
Label: "キャンセル"
Type: Secondary
Action: Navigate /products

## API呼び出し

### カテゴリ取得
Endpoint: GET /api/categories
Timing: ページ読み込み時
Response: カテゴリツリー

### 製品作成
Endpoint: POST /api/products
Timing: 保存ボタン押下時
Request Body:
- name
- description
- categoryId
- specifications[]
Response: 作成された製品

### 画像アップロード
Endpoint: POST /api/products/images
Timing: 画像選択時
Request: FormData (multipart)
Response: 画像URL

## バリデーション

クライアント側:
- 製品名: 必須、1-200文字
- カテゴリ: 必須
- 仕様名: 入力時は必須
- 画像: 形式チェック、サイズチェック

サーバー側:
- 全ての入力の再検証
- カテゴリ存在確認
- 重複チェック

## エラーハンドリング

- バリデーションエラー: フィールド下にエラーメッセージ表示
- ネットワークエラー: トースト通知
- サーバーエラー: エラーページ

## アクセシビリティ

- 全フィールドにラベル
- エラーメッセージはaria-describedby
- キーボードナビゲーション対応
- スクリーンリーダー対応

## レスポンシブ

- Desktop: 2カラムレイアウト
- Tablet: 1カラム、画像プレビュー縮小
- Mobile: スタックレイアウト、画像は1列
```

## 完了条件

選択したサービス/BCに対して以下が作成されたら完了：

- ✅ domain-language.md
- ✅ api-specification.md
- ✅ database-design.md
- ✅ operations/ (最低3オペレーション、各Actor UseCase + View定義)

## 完了メッセージ

```
✅ Phase 5: Software Design (ProductCatalog/Core) が完了しました

成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ outputs/5-software/services/ProductCatalog/Core/
├── domain-language.md
│   Aggregates: 2 (Product, Category)
│   Value Objects: 7
│   Domain Events: 4
│
├── api-specification.md
│   Endpoints: 8
│   Schemas: 12
│
├── database-design.md
│   Tables: 4
│   Indexes: 11
│   Views: 1
│
└── operations/
├── create-product/ (Actor UseCase + View)
├── search-products/ (Actor UseCase + View)
└── manage-categories/ (Actor UseCase + View)

ステータス確認:
→ `/value5:init status services`

次のアクション:
1. 他のサービス/BCの設計を続ける
`/parasol5:architecture:software Order Management`

2. 全サービス完了後、Phase 6へ
`/parasol5:implementation:code`
```

## エラーケース

**前提条件未満足:**
```
❌ Phase 4が完了していません

Phase 4でサービス境界を定義してください:
→ `/parasol5:architecture:application`
```

**無効なサービス/BC指定:**
```
❌ 無効なサービス/BC: InvalidService/InvalidBC

Phase 4で定義されたサービス/BC:
- ProductCatalog/Core
- Order/Management
- Order/Payment
- Pricing/Core
...

確認: `/value5:init status phase4`
```

## 参考資料

- **consultingTool参照**: `/Users/hmoriya/Develop/github/github.com/hmoriya/consultingTool`

### テンプレート（Mermaid非依存・解析エンジン対応）

- **構造化MD形式仕様**: `.claude/commands/parasol/_software-design-reference/_templates/structured-md-format.md`
  - パラソルドメイン言語の`@parasol:`マーカー形式
  - YAML in Markdownによる解析可能な定義
  - ドメインモデル・ER図・状態遷移図の自動生成

- **テスト定義形式仕様**: `.claude/commands/parasol/_software-design-reference/_templates/test-definition-format.md`
  - 5層テストピラミッド対応
  - パラソルドメイン言語からのテスト自動生成
  - 品質ゲート基準

### パラソルドメイン言語ガイド

- **パラソルドメイン言語ガイド**: `.claude/commands/parasol/_parasol-domain-language-guide.md`
  - Single Source of Truthの原則
  - 6セクション構成（Aggregates/ValueObjects/Events/Services/Repositories/Dictionary）
  - AI駆動開発との連携
