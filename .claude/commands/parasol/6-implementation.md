---
description: Software implementation (project:parasol)
---

# Phase 6: Implementation - 実装

Phase 5の設計を基に、実際のコードを生成・実装します。

## 使用方法

```bash
/parasol:6-implementation                    # インタラクティブ選択
/parasol:6-implementation ProductCatalog Core  # サービス/BCを直接指定
```

## 目的

Phase 5で設計したサービス/BCの実装を行い、**MS4マイルストーン完了**を達成します：

- コード骨格の生成
- 実装ガイドの提供
- テストコードの生成
- ドキュメント生成
- **MS4達成状況レポート作成**
- **運用準備度評価実施**

## 🤖 Amplifierサブエージェント連携

Phase 6では以下のサブエージェントとDDDワークフローを活用して、高品質な実装を行います。

### 使用するサブエージェント

| サブエージェント | 用途 | 起動タイミング |
|-----------------|------|---------------|
| **modular-builder** | モジュール単位でのコード生成 | コード骨格生成時 |
| **test-coverage** | テストカバレッジ分析、テストケース提案 | テストコード生成時 |
| **bug-hunter** | 実装中のバグ検出・修正 | エラー発生時 |
| **zen-architect** (REVIEW) | コード品質レビュー | 実装完了時 |

### DDD ワークフロー連携

Phase 5で準備した設計を基に、DDDワークフローで実装を進めます：

```
📋 DDDワークフロー実装手順

1. Phase 5 で作成した計画を確認
   → /ddd:status (現在の進捗確認)

2. コード実装
   → /ddd:4-code "BC: {bc-name} の実装"

3. 実装完了・クリーンアップ
   → /ddd:5-finish

ポイント:
- /ddd:4-code で domain-language.md に基づくコード生成
- modular-builder と組み合わせてモジュール単位で実装
- /ddd:5-finish でクリーンアップと最終確認
```

### modular-builder の活用

「bricks & studs」哲学に基づき、再生成可能なモジュールを構築：

```
Task tool を使用して modular-builder を起動：

プロンプト:
「以下の仕様に基づいて、モジュールを実装してください。

仕様ドキュメント:
- domain-language.md: {パス}
- api-specification.md: {パス}
- database-design.md: {パス}

実装対象:
1. Aggregate: {aggregate-name}
2. Repository: {repository-name}
3. Use Case: {use-case-name}

技術スタック:
- 言語: {language}
- フレームワーク: {framework}

実装原則:
- 各モジュールは自己完結（bricks）
- 公開インターフェースは明確（studs）
- 再生成可能な構造」
```

### test-coverage の活用

テスト戦略の策定とカバレッジ分析：

```
Task tool を使用して test-coverage を起動：

プロンプト:
「以下の実装に対して、テスト戦略を提案してください。

実装コード: {code/ ディレクトリ}
ドメイン言語: {domain-language.md}

分析対象:
1. Unit Test カバレッジ分析
2. Integration Test 必要箇所の特定
3. Edge Case の洗い出し
4. Mock/Stub 戦略

目標:
- Unit Test カバレッジ: 80%以上
- Critical Path: 100%カバー
- 過剰テストの回避」
```

### テスト自動生成（パラソルドメイン言語連携）

パラソルドメイン言語からテストスケルトンを自動生成：

```
テスト生成フロー:

1. ドメインモデルテスト（Unit）
   入力: @parasol:value_objects, @parasol:aggregates
   出力: tests/unit/domain/*.py

   生成内容:
   - Value Object: 境界値テスト、等価性テスト
   - Aggregate: 不変条件テスト、振る舞いテスト
   - Domain Service: ロジックテスト

2. APIテスト（Contract）
   入力: api-specification.md
   出力: tests/contract/api/*.py

   生成内容:
   - エンドポイント契約テスト
   - リクエスト/レスポンス検証
   - 認証・認可テスト

3. Actor UseCaseテスト（Integration）
   入力: @parasol:actor_usecase_flow
   出力: tests/integration/actor-usecases/*.py

   生成内容:
   - 基本フローテスト
   - 代替フローテスト
   - 例外フローテスト

4. UIテスト（Component）
   入力: views/*.md, robustness.md
   出力: tests/component/views/*.spec.ts

   生成内容:
   - 表示テスト
   - 操作テスト
   - BCE連携テスト
```

**テスト定義形式**: `.claude/commands/parasol/_software-design-reference/_templates/test-definition-format.md`

### bug-hunter の活用

実装中のエラーを体系的に解決：

```
Task tool を使用して bug-hunter を起動：

プロンプト:
「以下のエラーを調査・修正してください。

エラー内容: {エラーメッセージ}
発生箇所: {ファイル:行番号}
関連コード: {関連するコードスニペット}

調査項目:
1. 根本原因の特定
2. 修正案の提示
3. 再発防止策

注意: 最小限の変更で修正（過度な抽象化を避ける）」
```

### 実装品質チェック

実装完了時に zen-architect でレビュー：

```
Task tool を使用して zen-architect (REVIEW) を起動：

プロンプト:
「以下の実装をレビューしてください。

実装コード: {code/ ディレクトリ}
設計仕様: {Phase 5 の成果物}

レビュー観点:
1. 設計との整合性
2. SOLID原則の遵守
3. DDDパターンの適用
4. コードの簡潔性（ruthless simplicity）

フィードバック形式:
- Critical: 必ず修正が必要
- Suggestion: 改善推奨
- Note: 参考情報」
```

### 実装ストーリー出力

Phase 6では以下の実装判断理由を自動出力します：

| 実装判断 | 出力される理由 |
|----------|---------------|
| 技術選択 | なぜこのフレームワーク/ライブラリを選んだか |
| パターン適用 | なぜこのデザインパターンを使ったか |
| テスト戦略 | なぜこのテスト構成にしたか |
| エラーハンドリング | どのエラーケースを重視したか |

**出力先**: `outputs/6-implementation/services/{service}/{bc}/implementation-story.md`

### ナレッジ蓄積

実装パターンと学習をナレッジベースに蓄積：

```yaml
# outputs/6-implementation/implementation-learnings.json
{
  "project": "{project-name}",
  "bc": "{bc-name}",
  "learnings": [
    {
      "category": "performance",
      "issue": "N+1クエリ問題",
      "solution": "Eager loadingの適用",
      "context": "ProductRepository.findByCategory()"
    },
    {
      "category": "testing",
      "issue": "外部API依存のテスト",
      "solution": "Contract TestとMockの組み合わせ",
      "context": "PaymentService統合テスト"
    }
  ],
  "created_at": "timestamp"
}
```

## 🔧 プロジェクト検出

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

📋 次のアクションを選択してください:

1. 新しいプロジェクトを作成
   → /parasol:project init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol:project list
```

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/parasol:1-context

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/parasol:1-context  # ❌
```

詳細は `.claude/commands/parasol/_project-detection.md` を参照。

## 成果物

以下を `outputs/6-implementation/services/ServiceName/BCName/` に作成：

1. **code/** - 生成されたコード
2. **tests/** - テストコード
3. **docs/** - 実装ドキュメント
4. **implementation-guide.md** - 実装ガイド

## 実行手順

### ステップ1: 実装ガイド生成

Phase 5の設計を基に、実装の手順書を作成します。

**成果物**: `implementation-guide.md`

```markdown
# ProductCatalog/Core - Implementation Guide

## 概要
Phase 5の設計に基づいて実装を行います。

## 技術スタック
- 言語: [選択された言語]
- フレームワーク: [選択されたフレームワーク]
- データベース: PostgreSQL
- API: REST + gRPC

## 実装順序

### Week 1: 基盤構築
1. プロジェクト構造作成
2. データベースマイグレーション
3. 基本的なCRUD操作

### Week 2: ドメインロジック
1. Aggregate実装
2. Domain Service実装
3. Repository実装

### Week 3: API実装
1. REST API実装
2. gRPC実装（必要な場合）
3. イベント発行

### Week 4: テストと統合
1. ユニットテスト
2. 統合テスト
3. E2Eテスト

## 実装の詳細

### 1. Productリ Aggregate

\`\`\`typescript
// src/domain/aggregates/product.aggregate.ts

export class Product extends AggregateRoot {
private constructor(
private readonly id: ProductId,
private name: ProductName,
private description: ProductDescription,
private categoryId: CategoryId,
private status: ProductStatus,
private specifications: ProductSpecification[],
private images: ProductImage[]
) {
super();
}

static create(
name: ProductName,
categoryId: CategoryId,
description?: ProductDescription
): Product {
const product = new Product(
ProductId.generate(),
name,
description || ProductDescription.empty(),
categoryId,
ProductStatus.draft(),
[],
[]
);

product.addDomainEvent(
new ProductCreatedEvent(product.id, product.name, product.categoryId)
);

return product;
}

updateInfo(name: ProductName, description: ProductDescription): void {
this.name = name;
this.description = description;

this.addDomainEvent(
new ProductUpdatedEvent(this.id, { name, description })
);
}

addSpecification(spec: ProductSpecification): void {
this.specifications.push(spec);
}

addImage(image: ProductImage): void {
this.images.push(image);
}

activate(): void {
if (this.images.length === 0) {
throw new DomainException('Cannot activate product without images');
}
this.status = ProductStatus.active();
}

discontinue(reason: string): void {
this.status = ProductStatus.discontinued();
this.addDomainEvent(
new ProductDiscontinuedEvent(this.id, reason)
);
}
}
\`\`\`

### 2. ProductRepository

\`\`\`typescript
// src/domain/repositories/product.repository.ts

export interface ProductRepository {
save(product: Product): Promise<void>;
findById(id: ProductId): Promise<Product | null>;
findByCategory(categoryId: CategoryId): Promise<Product[]>;
delete(id: ProductId): Promise<void>;
}

// src/infrastructure/repositories/product.repository.impl.ts

export class ProductRepositoryImpl implements ProductRepository {
constructor(private readonly db: Database) {}

async save(product: Product): Promise<void> {
// ORMまたは生SQL
await this.db.products.upsert({
product_id: product.id.value,
name: product.name.value,
description: product.description.value,
category_id: product.categoryId.value,
status: product.status.value,
});

// Domain Eventsの発行
await this.publishDomainEvents(product);
}

async findById(id: ProductId): Promise<Product | null> {
const row = await this.db.products.findOne({ product_id: id.value });
return row ? this.toDomain(row) : null;
}

private toDomain(row: any): Product {
// DBレコードをDomainオブジェクトに変換
}
}
\`\`\`

### 3. REST API

\`\`\`typescript
// src/api/controllers/products.controller.ts

@Controller('/products')
export class ProductsController {
constructor(
private readonly createProductUseCase: CreateProductUseCase,
private readonly getProductUseCase: GetProductUseCase
) {}

@Post('/')
async createProduct(@Body() dto: CreateProductDto): Promise<ProductResponse> {
const command = new CreateProductCommand(
dto.name,
dto.categoryId,
dto.description
);

const product = await this.createProductUseCase.execute(command);

return ProductResponse.from(product);
}

@Get('/:id')
async getProduct(@Param('id') id: string): Promise<ProductResponse> {
const query = new GetProductQuery(id);
const product = await this.getProductUseCase.execute(query);

if (!product) {
throw new NotFoundException('Product not found');
}

return ProductResponse.from(product);
}
}
\`\`\`

### 4. Use Case

\`\`\`typescript
// src/application/use-cases/create-product.use-case.ts

export class CreateProductUseCase {
constructor(
private readonly productRepository: ProductRepository,
private readonly categoryRepository: CategoryRepository,
private readonly eventBus: EventBus
) {}

async execute(command: CreateProductCommand): Promise<Product> {
// バリデーション
const category = await this.categoryRepository.findById(
new CategoryId(command.categoryId)
);

if (!category) {
throw new ValidationException('Category not found');
}

// Aggregate作成
const product = Product.create(
new ProductName(command.name),
category.id,
new ProductDescription(command.description)
);

// 永続化
await this.productRepository.save(product);

// イベント発行
await this.eventBus.publishAll(product.domainEvents);

return product;
}
}
\`\`\`

## テスト戦略

### Unit Tests
- Domain Logic（Aggregates, Value Objects）
- Use Cases
- Domain Services

### Integration Tests
- Repository（実DBまたはTestcontainers使用）
- API Endpoints

### E2E Tests
- 主要なユーザーフロー
- エラーケース

## デプロイメント

1. Docker Image作成
2. K8s Manifestデプロイ
3. データベースマイグレーション実行
4. サービス起動確認
5. ヘルスチェック

## チェックリスト

実装完了の基準:
- [ ] 全てのAggregateが実装されている
- [ ] 全てのRepositoryが実装されている
- [ ] APIエンドポイントが実装されている
- [ ] ユニットテストのカバレッジ80%以上
- [ ] 統合テストが通る
- [ ] ドキュメントが更新されている
- [ ] コードレビュー完了
```

### ステップ2: コード骨格生成

設計に基づいてコードの骨格を生成します（実際の生成はプロジェクトの技術スタック次第）。

### ステップ3: テストコード生成

テストケースのテンプレートを生成します。

### ステップ4: ドキュメント生成

API仕様書、README、開発ガイドを生成します。

## 完了条件

選択したサービス/BCに対して以下が作成されたら完了：

- ✅ implementation-guide.md
- ✅ code/ (骨格またはサンプル)
- ✅ tests/ (テストテンプレート)
- ✅ docs/ (実装ドキュメント)

## 完了メッセージ

```
✅ Phase 6: Implementation (ProductCatalog/Core) が完了しました

成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ outputs/6-implementation/services/ProductCatalog/Core/
├── implementation-guide.md
│   実装手順とコード例
│   
├── code/
│   生成されたコード骨格
│   
├── tests/
│   テストテンプレート
│   
└── docs/
API仕様書、開発ガイド

🎯 次のアクション:
1. 実装ガイドに従って開発開始
2. 他のサービス/BCの実装準備
`/parasol:6-implementation Order Management`
3. 全実装完了後、Phase 7へ
`/parasol:7-platform`
```

## エラーケース

**前提条件未満足:**
```
❌ Phase 5が完了していません

Phase 5でソフトウェア設計を完了してください:
→ `/parasol:5-software-design`
```

## 参考資料

- **Phase 5設計**: `outputs/5-software/services/`
