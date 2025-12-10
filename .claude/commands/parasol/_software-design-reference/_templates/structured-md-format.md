# Parasol V5 構造化Markdown形式仕様

**解析エンジン対応・Mermaid非依存**

## 設計原則

1. **YAML in Markdown**: 構造化データはYAMLコードブロックで記述
2. **マーカーコメント**: パーサーが認識できるブロック境界（`# @parasol:block_type`）
3. **テーブル補完**: 人間可読性が必要な場合はMarkdownテーブルで補足
4. **実装非依存**: 特定のプログラミング言語・DB・フレームワークに依存しない抽象定義

---

## 1. パラソルドメイン言語形式（{bc-name}-domain-language.md）

**重要**: これは「パラソルドメイン言語（Parasol Domain Language）」であり、DDDの「ドメイン言語」とは異なる概念です。

### パラソルドメイン言語の役割

```
パラソルドメイン言語（Single Source of Truth）
    ↓ 解析エンジン
    ↓
┌───────────────────────────────────────────┐
│           生成される設計成果物              │
├─────────────┬─────────────┬───────────────┤
│ドメインモデル │   ER図      │  状態遷移図   │
│(クラス図)    │             │               │
├─────────────┴─────────────┴───────────────┤
│                実装成果物                   │
├─────────────┬─────────────┬───────────────┤
│    UI       │    API      │     DB        │
└─────────────┴─────────────┴───────────────┘
```

- **定義駆動開発**: パラソルドメイン言語が先、設計図と実装は自動生成
- **ドメインモデル生成**: パラソルドメイン言語 → クラス図/ER図/状態遷移図
- **一貫性保証**: 全層で同じルールを適用
- **再生成可能性**: いつでも定義から設計図と実装を再生成

### 生成される成果物

| パラソルドメイン言語セクション | 生成される設計成果物 | 生成される実装成果物 |
|-------------------------------|---------------------|---------------------|
| Aggregates + Relationships | ドメインモデル（クラス図） | Entity/DTO classes |
| Value Objects | 型定義 | Validation rules |
| Domain Events | イベントフロー図 | Event handlers |
| → Tables/Relations生成 | ER図 | DDL/Migration |
| State Machine | 状態遷移図 | State machine code |
| Use Case Flow | フロー図 | Controller logic |

### 1.1 Aggregates（集約）

```yaml
# @parasol:aggregates
aggregates:
  - name: Product
    root_entity: Product
    description: 製品集約

    properties:
      - name: productId
        type: ProductId
        description: 製品識別子
        constraints: [required, immutable]
        # → UI: hidden field
        # → API: path parameter
        # → DB: PRIMARY KEY
      - name: name
        type: ProductName
        description: 製品名
        constraints: [required]
        # → UI: text input (required)
        # → API: request body field
        # → DB: VARCHAR NOT NULL
      - name: status
        type: ProductStatus
        description: ステータス
        constraints: [required]
        default: Draft
        # → UI: select dropdown
        # → API: enum field
        # → DB: VARCHAR with CHECK

    invariants:
      - id: INV-001
        description: 名前は1-200文字
        expression: "1 <= name.length <= 200"
        # → UI: validation rule
        # → API: business rule check
        # → DB: CHECK constraint
      - id: INV-002
        description: アクティブ製品は最低1つの画像が必要
        expression: "status == Active => images.count >= 1"

    behaviors:
      - name: create
        description: 新規製品作成
        returns: Product
        # → UI: create form action
        # → API: POST endpoint
        # → DB: INSERT transaction
      - name: activate
        description: アクティブ化
        returns: void
        preconditions: [has_image]
        # → UI: activate button (conditional)
        # → API: PATCH endpoint
        # → DB: UPDATE transaction

    child_entities:
      - name: ProductImage
        description: 製品画像
        properties:
          - name: imageId
            type: ImageId
            constraints: [required]
          - name: url
            type: ImageUrl
            constraints: [required]
```

### 1.2 Value Objects（値オブジェクト）

**実装非依存**: 抽象型で定義し、各言語/DBに変換時に適切な型にマッピング

```yaml
# @parasol:value_objects
value_objects:
  - name: ProductId
    type: Identifier
    description: 製品識別子
    # 実装時: UUID (Python), string (TS), UUID (PostgreSQL)

  - name: ProductName
    type: Text
    description: 製品名
    validation: "1-200文字、空白のみ不可"
    constraints:
      min_length: 1
      max_length: 200
      pattern: "^(?!\\s*$).+"
    # → UI: maxLength="200" required
    # → API: @Length(1, 200)
    # → DB: VARCHAR(200) NOT NULL

  - name: ProductStatus
    type: Enum
    description: 製品ステータス
    values:
      - value: Draft
        description: 下書き
      - value: Active
        description: 有効
      - value: Discontinued
        description: 販売終了
    default: Draft
    # → UI: <select> options
    # → API: Enum class
    # → DB: CHECK constraint

  - name: Temperature
    type: Decimal
    description: 温度
    unit: Celsius
    range: [-273.15, 1000.0]
    precision: 0.1
    # 単位と精度を定義、実装は各環境で最適化

  - name: Money
    type: Composite
    description: 金額
    components:
      - name: amount
        type: Decimal
        precision: 2
      - name: currency
        type: Currency
```

### 1.3 Domain Events（ドメインイベント）

```yaml
# @parasol:domain_events
domain_events:
  - name: ProductCreated
    description: 製品作成イベント
    trigger: Product.create()
    cross_vs: false
    properties:
      - name: productId
        type: ProductId
      - name: name
        type: ProductName
      - name: createdAt
        type: DateTime
    subscribers:
      - SearchIndexService
      - AuditLogService
    # → イベント駆動アーキテクチャ
    # → 非同期処理
    # → 監査ログ

  - name: ProductActivated
    description: 製品アクティブ化イベント
    trigger: Product.activate()
    cross_vs: true
    properties:
      - name: productId
        type: ProductId
      - name: activatedAt
        type: DateTime
    # cross_vs: true → マイクロサービス間通信対象
```

### 1.4 Domain Services（ドメインサービス）

```yaml
# @parasol:domain_services
domain_services:
  - name: ProductSearchService
    description: 製品検索サービス
    responsibility: 複雑な製品検索ロジック
    methods:
      - name: searchByKeyword
        params:
          - name: keyword
            type: Text
          - name: filters
            type: SearchFilters
        returns: List<Product>
        logic:
          - キーワードで全文検索
          - フィルター条件を適用
          - 結果をソート
      - name: searchBySimilarity
        params:
          - name: productId
            type: ProductId
        returns: List<Product>
        logic:
          - 対象製品の特徴を取得
          - 類似製品を算出
```

### 1.5 Repositories（リポジトリ）

```yaml
# @parasol:repositories
repositories:
  - name: ProductRepository
    aggregate: Product
    methods:
      - name: save
        params:
          - name: product
            type: Product
        returns: void
        # → DB: INSERT/UPDATE
      - name: findById
        params:
          - name: id
            type: ProductId
        returns: Product
        # → DB: SELECT by PK
      - name: findByCategory
        params:
          - name: categoryId
            type: CategoryId
        returns: List<Product>
        # → DB: SELECT with FK filter
      - name: delete
        params:
          - name: id
            type: ProductId
        returns: void
        # → DB: DELETE (or soft delete)
```

### 1.6 ユビキタス言語辞書

```yaml
# @parasol:ubiquitous_language
ubiquitous_language:
  - term_ja: 製品
    term_en: Product
    definition: 販売可能な商品の単位
    context: 製品カタログBC
  - term_ja: アクティブ化
    term_en: Activate
    definition: 製品を販売可能状態にする操作
    context: 製品カタログBC
    business_rule: 最低1つの画像が必要
```

### 1.7 関係性定義（Relationships）

```yaml
# @parasol:relationships
relationships:
  - from: Product
    to: Category
    type: references
    cardinality: N:1
    description: 製品はカテゴリに属する
    # → DB: FOREIGN KEY

  - from: Product
    to: ProductImage
    type: contains
    cardinality: 1:N
    cascade_delete: true
    description: 製品は画像を含む（集約内）
    # → DB: ON DELETE CASCADE

  - from: Category
    to: Category
    type: references
    cardinality: N:1
    field: parentId
    description: カテゴリは親カテゴリを持つ（自己参照）
```

---

## 2. 生成成果物形式

パラソルドメイン言語から解析エンジンが以下の設計成果物を生成します。
これらは**生成物**であり、直接編集せずパラソルドメイン言語を修正して再生成します。

### 2.1 ドメインモデル（生成: domain-model.yaml）

パラソルドメイン言語の `@parasol:aggregates` + `@parasol:relationships` から生成。

```yaml
# @generated from: {bc-name}-domain-language.md
# @generated_at: 2025-12-09T10:00:00Z
# DO NOT EDIT - Regenerate from Parasol Domain Language

domain_model:
  bounded_context: ProductCatalog

  classes:
    - name: Product
      stereotype: AggregateRoot
      properties:
        - name: productId
          type: ProductId
          visibility: private
        - name: name
          type: ProductName
          visibility: private
        - name: status
          type: ProductStatus
          visibility: private
        - name: images
          type: List<ProductImage>
          visibility: private
      methods:
        - name: create
          visibility: public
          return_type: Product
          parameters: []
        - name: activate
          visibility: public
          return_type: void
          preconditions: ["images.size() >= 1"]
      invariants:
        - "name.length >= 1 && name.length <= 200"
        - "status == Active => images.size() >= 1"

    - name: ProductImage
      stereotype: Entity
      properties:
        - name: imageId
          type: ImageId
          visibility: private
        - name: url
          type: ImageUrl
          visibility: private

  associations:
    - from: Product
      to: ProductImage
      type: composition
      multiplicity: "1..*"
      navigability: unidirectional
    - from: Product
      to: Category
      type: association
      multiplicity: "*..1"
      navigability: unidirectional
```

### 2.2 データベース設計（生成: database-design.yaml）

パラソルドメイン言語から解析エンジンがER図・テーブル定義を生成。

```yaml
# @generated from: {bc-name}-domain-language.md
# @generated_at: 2025-12-09T10:00:00Z
# DO NOT EDIT - Regenerate from Parasol Domain Language

database_design:
  dialect: PostgreSQL

  tables:
    - name: products
      source_aggregate: Product
      columns:
        - name: product_id
          type: UUID
          source: productId (ProductId)
          constraints: [PRIMARY KEY]
        - name: name
          type: VARCHAR(200)
          source: name (ProductName)
          constraints: [NOT NULL]
        - name: status
          type: VARCHAR(20)
          source: status (ProductStatus)
          constraints: [NOT NULL]
          default: "'draft'"
          check: "status IN ('draft', 'active', 'discontinued')"
        - name: category_id
          type: UUID
          source: relationship(Category)
          constraints: [NOT NULL, FK]
        - name: created_at
          type: TIMESTAMP
          constraints: [NOT NULL]
          default: NOW()
        - name: updated_at
          type: TIMESTAMP
          constraints: [NOT NULL]
          default: NOW()
      indexes:
        - name: idx_products_category
          columns: [category_id]
        - name: idx_products_status
          columns: [status]

  relations:
    - parent: categories
      child: products
      cardinality: 1:N
      foreign_key:
        column: category_id
        references: category_id
        on_delete: RESTRICT
    - parent: products
      child: product_images
      cardinality: 1:N
      foreign_key:
        column: product_id
        references: product_id
        on_delete: CASCADE
```

### 2.3 状態遷移（生成: state-machine.yaml）

パラソルドメイン言語の `@parasol:value_objects` (Enum) から状態遷移を生成。

```yaml
# @generated from: {bc-name}-domain-language.md
# @generated_at: 2025-12-09T10:00:00Z

state_machine:
  name: ProductStatus
  source_value_object: ProductStatus
  initial_state: Draft

  states:
    - name: Draft
      transitions:
        - event: activate
          target: Active
          guard: "images.count >= 1"
        - event: delete
          target: Deleted
    - name: Active
      transitions:
        - event: discontinue
          target: Discontinued
        - event: deactivate
          target: Draft
    - name: Discontinued
      transitions:
        - event: reactivate
          target: Active
    - name: Deleted
      terminal: true
```

---

## 3. ユースケース・フロー定義形式（use-case.md）

パラソルドメイン言語のBehaviorsと連携し、詳細なユースケースフローを定義します。

### 3.1 ユースケースフロー

```yaml
# @parasol:usecase_flow
usecase:
  id: UC-001
  name: 製品作成
  actor: 製品管理者
  preconditions:
    - 製品管理者権限を持つ
    - カテゴリが存在する
  postconditions:
    - 製品がDraftステータスで作成される
    - ProductCreatedイベントが発行される

# @parasol:basic_flow
basic_flow:
  - step: 1
    actor: ユーザー
    action: 「新規製品」を選択
    next: 2
  - step: 2
    actor: システム
    action: 製品作成フォームを表示
    next: 3
  - step: 3
    actor: ユーザー
    action: 製品情報を入力
    inputs: [製品名, 説明, カテゴリ, 仕様, 画像]
    next: 4
  - step: 4
    actor: ユーザー
    action: 「保存」を選択
    next: 5
  - step: 5
    actor: システム
    action: 入力を検証
    next: 6
    alternatives: [ALT-001, ALT-002]
  - step: 6
    actor: システム
    action: 製品を作成（ステータス: Draft）
    next: 7
  - step: 7
    actor: システム
    action: ProductCreatedイベントを発行
    next: 8
  - step: 8
    actor: システム
    action: 成功メッセージを表示、製品詳細画面に遷移
    next: END

# @parasol:alternative_flow
alternative_flows:
  - id: ALT-001
    name: バリデーションエラー
    branch_from: 5
    condition: 入力検証失敗
    steps:
      - step: 5a1
        actor: システム
        action: エラーメッセージを表示
        next: 5a2
      - step: 5a2
        actor: ユーザー
        action: 入力を修正
        next: 4
        note: 基本フロー4に戻る

  - id: ALT-002
    name: 同名製品警告
    branch_from: 5
    condition: 同名製品が存在
    steps:
      - step: 5b1
        actor: システム
        action: 警告ダイアログを表示
        next: 5b2
      - step: 5b2
        actor: ユーザー
        action: 確認または修正を選択
        branches:
          - condition: 確認
            next: 6
          - condition: 修正
            next: 3

# @parasol:exception_flow
exception_flows:
  - id: EXC-001
    name: サーバーエラー
    trigger_point: 6
    condition: データベース接続エラー
    steps:
      - step: 6e1
        actor: システム
        action: エラーログを記録
        next: 6e2
      - step: 6e2
        actor: システム
        action: エラーページを表示
        next: END
    recovery: 再試行可能
```

---

## 4. 状態遷移定義（パラソルドメイン言語に含める場合）

**注意**: 状態遷移は通常、パラソルドメイン言語のValue Objects (Enum) から自動生成されます。
複雑な状態遷移を明示的に定義する必要がある場合のみ、以下の形式を使用します。

```yaml
# @parasol:state_machine
state_machine:
  name: ProductStatus
  initial_state: Draft
  states:
    - name: Draft
      description: 下書き状態
      transitions:
        - event: activate
          target: Active
          guard: has_image
        - event: delete
          target: Deleted
    - name: Active
      description: 有効状態
      transitions:
        - event: discontinue
          target: Discontinued
        - event: deactivate
          target: Draft
    - name: Discontinued
      description: 販売終了状態
      transitions:
        - event: reactivate
          target: Active
    - name: Deleted
      description: 削除済み（終了状態）
      terminal: true
```

---

## 5. シーケンス定義（sequenceDiagram代替）

```yaml
# @parasol:sequence
sequence:
  name: 製品作成API呼び出し
  participants:
    - name: Client
      type: actor
    - name: API Gateway
      type: service
    - name: ProductService
      type: service
    - name: Database
      type: datastore
    - name: EventBus
      type: service

  messages:
    - from: Client
      to: API Gateway
      action: POST /api/products
      payload: CreateProductRequest
      sync: true
    - from: API Gateway
      to: ProductService
      action: createProduct()
      sync: true
    - from: ProductService
      to: Database
      action: INSERT products
      sync: true
    - from: Database
      to: ProductService
      action: return productId
      sync: true
    - from: ProductService
      to: EventBus
      action: publish(ProductCreated)
      sync: false
    - from: ProductService
      to: API Gateway
      action: return Product
      sync: true
    - from: API Gateway
      to: Client
      action: 201 Created
      payload: ProductResponse
      sync: true
```

---

## 6. パーサー実装ガイド

### 6.1 マーカー認識

```python
# YAMLブロック抽出
import re
import yaml

MARKER_PATTERN = r"```yaml\n# @parasol:(\w+)\n(.*?)```"

def extract_parasol_blocks(md_content: str) -> dict:
    """Markdown内の@parasolマーカー付きYAMLブロックを抽出"""
    blocks = {}
    for match in re.finditer(MARKER_PATTERN, md_content, re.DOTALL):
        block_type = match.group(1)
        yaml_content = match.group(2)
        blocks[block_type] = yaml.safe_load(yaml_content)
    return blocks
```

### 6.2 型定義（TypeScript）

```typescript
interface ParasolAggregate {
  name: string;
  root_entity: string;
  entities: ParasolEntity[];
  invariants: ParasolInvariant[];
}

interface ParasolEntity {
  name: string;
  type: 'root' | 'entity' | 'value_object';
  properties: ParasolProperty[];
  behaviors?: ParasolBehavior[];
}

interface ParasolRelationship {
  from: string;
  to: string;
  type: 'references' | 'contains' | 'has';
  cardinality: '1:1' | '1:N' | 'N:1' | 'N:M';
}
```

---

## 7. パラソルドメイン言語と生成成果物の関係

### 7.1 全体フロー

```
┌─────────────────────────────────────────────────────────────┐
│              パラソルドメイン言語 (Single Source of Truth)    │
│  {bc-name}-domain-language.md                               │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐ │
│  │Aggregates│  Value   │ Domain   │ Domain   │Repositories│ │
│  │          │ Objects  │ Events   │ Services │           │ │
│  └────┬─────┴────┬─────┴────┬─────┴────┬─────┴─────┬─────┘ │
└───────┼──────────┼──────────┼──────────┼───────────┼───────┘
        │          │          │          │           │
        ▼          ▼          ▼          ▼           ▼
┌─────────────────────────────────────────────────────────────┐
│                    解析エンジン                              │
└───────┬──────────┬──────────┬──────────┬───────────┬───────┘
        │          │          │          │           │
        ▼          ▼          ▼          ▼           ▼
┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│ドメイン  ││ER図      ││状態遷移図││シーケンス││フロー図  │
│モデル    ││          ││          ││図        ││          │
│(クラス図)││          ││          ││          ││          │
└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘
     │           │           │           │           │
     ▼           ▼           ▼           ▼           ▼
┌─────────────────────────────────────────────────────────────┐
│                      実装成果物                              │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐ │
│  │ Entity   │  DDL/    │  State   │  API     │Controller │ │
│  │ Classes  │Migration │ Machine  │ Client   │ Logic     │ │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 編集ルール

| 成果物種別 | 編集可否 | 変更方法 |
|-----------|---------|---------|
| パラソルドメイン言語 | **編集可** | 直接編集 |
| ドメインモデル（生成） | 編集不可 | パラソルドメイン言語を修正して再生成 |
| ER図（生成） | 編集不可 | パラソルドメイン言語を修正して再生成 |
| 状態遷移図（生成） | 編集不可 | パラソルドメイン言語を修正して再生成 |
| ユースケースフロー | **編集可** | 詳細フローは直接定義 |
| 実装コード（生成） | 編集不可 | パラソルドメイン言語を修正して再生成 |

### 7.3 Consulting Toolsからの移行

| Consulting Tools形式 | Parasol V5形式 |
|---------------------|----------------|
| Mermaid `classDiagram` | パラソルドメイン言語から**生成** |
| Mermaid `erDiagram` | パラソルドメイン言語から**生成** |
| Mermaid `flowchart` | `@parasol:basic_flow` YAML |
| Mermaid `stateDiagram` | パラソルドメイン言語のEnumから**生成** |
| Mermaid `sequenceDiagram` | `@parasol:sequence` YAML |
