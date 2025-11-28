# /parasol:4-architecture - アプリケーションアーキテクチャ設計

## コマンド: `/parasol:4-architecture`

ビジネス設計を技術アーキテクチャに変換します。境界コンテキスト、マイクロサービス、API仕様を設計します。

## 実行時間
約2-3時間

## 前提条件
- Phase 3（ビジネス設計）の完了
- CL1ケーパビリティの定義
- MS境界の基本設計

## 実行内容

### Task 1: 境界コンテキスト定義（CL1 = Bounded Context）

#### 境界コンテキストマッピング
```yaml
BC-VS0-1: 認証認可コンテキスト
  CL1: VS0-CL1-1 認証認可管理
  責任: ユーザー認証、権限管理、セッション管理
  チーム: プラットフォームチーム
  ユビキタス言語:
    - User: システムを利用する個人
    - Role: 権限のグループ
    - Permission: 特定操作の許可
    - Session: ログイン状態の管理単位

BC-VS0-2: データ管理コンテキスト
  CL1: VS0-CL1-2 データ管理
  責任: マスターデータ、共通データ、データ同期
  チーム: データチーム
  ユビキタス言語:
    - MasterData: 全体で共有される基準データ
    - Entity: ビジネスオブジェクト
    - Sync: データの同期処理

BC-VS1: 認知形成コンテキスト
  CL1: VS1-CL1 認知形成
  責任: マーケティング、広報、導入促進
  チーム: 導入支援チーム
  ユビキタス言語:
    - Campaign: 認知向上施策
    - Awareness: 認知度指標
    - Engagement: 関与度

BC-VS3: 初期実践コンテキスト
  CL1: VS3-CL1 初期実践
  責任: パイロット支援、テンプレート、メンタリング
  チーム: 実践支援チーム
  ユビキタス言語:
    - Pilot: 試験的プロジェクト
    - Template: 再利用可能な雛形
    - Mentor: 指導者
```

### Task 2: コンテキストマップ作成

#### コンテキスト間の関係
```yaml
関係パターン:
  BC-VS0-1 → その他すべて
    関係: Upstream/Downstream
    統合: Published Language (JWT/OAuth2)
    理由: 認証は全サービスの前提

  BC-VS0-2 ⇄ BC-VS3
    関係: Partnership
    統合: Shared Database
    理由: データの密な連携が必要

  BC-VS1 → BC-VS3
    関係: Customer/Supplier
    統合: REST API
    理由: 認知から実践への流れ

腐敗防止層（ACL）:
  外部システム連携:
    既存システム → BC-VS0-2
    パターン: Anti-corruption Layer
    実装: アダプタパターン使用
```

### Task 3: マイクロサービス詳細設計

#### サービス構成
```yaml
MS-AUTH: 認証認可サービス
  エンドポイント:
    POST /api/auth/login
    POST /api/auth/logout
    POST /api/auth/refresh
    GET  /api/auth/profile
    PUT  /api/auth/permissions

  データモデル:
    User:
      - id: UUID
      - email: string
      - passwordHash: string
      - roles: Role[]

    Role:
      - id: UUID
      - name: string
      - permissions: Permission[]

  技術スタック:
    言語: TypeScript/Node.js
    フレームワーク: Express/Fastify
    DB: PostgreSQL
    キャッシュ: Redis

MS-PROJECT: プロジェクト管理サービス
  エンドポイント:
    POST /api/projects
    GET  /api/projects/{id}
    PUT  /api/projects/{id}/status
    GET  /api/projects/{id}/metrics
    POST /api/projects/{id}/templates

  データモデル:
    Project:
      - id: UUID
      - name: string
      - status: ProjectStatus
      - stage: ValueStage
      - metrics: Metrics

    Template:
      - id: UUID
      - name: string
      - type: TemplateType
      - content: JSON

  技術スタック:
    言語: Java
    フレームワーク: Spring Boot
    DB: PostgreSQL
    メッセージ: Kafka
```

### Task 4: API仕様設計

#### RESTful API設計原則
```yaml
URL設計:
  規則:
    - 複数形を使用: /users, /projects
    - ネスト最大2階層: /projects/{id}/tasks
    - クエリパラメータ: フィルタと並び替え

HTTPメソッド:
  GET: リソース取得
  POST: リソース作成
  PUT: リソース完全更新
  PATCH: リソース部分更新
  DELETE: リソース削除

レスポンス形式:
  成功:
    status: success
    data: {リソース}

  エラー:
    status: error
    error:
      code: ERROR_CODE
      message: エラーメッセージ
```

#### GraphQL スキーマ（一部サービス）
```graphql
type Query {
  project(id: ID!): Project
  projects(filter: ProjectFilter): [Project!]!
  metrics(projectId: ID!): Metrics
  user(id: ID!): User
  currentUser: User
}

type Mutation {
  createProject(input: CreateProjectInput!): Project!
  updateProject(id: ID!, input: UpdateProjectInput!): Project!
  assignTemplate(projectId: ID!, templateId: ID!): Project!
  login(email: String!, password: String!): AuthPayload!
}

type Subscription {
  projectUpdated(projectId: ID!): Project
  metricsUpdated(projectId: ID!): Metrics
}

type Project {
  id: ID!
  name: String!
  status: ProjectStatus!
  stage: ValueStage!
  templates: [Template!]!
  metrics: Metrics
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

### Task 5: 技術アーキテクチャ全体像

#### システム構成
```yaml
フロントエンド層:
  技術: Next.js 14 + TypeScript
  状態管理: Zustand
  API通信: TanStack Query
  UI: Tailwind CSS + shadcn/ui

APIゲートウェイ層:
  技術: Kong / AWS API Gateway
  機能:
    - ルーティング
    - 認証統合
    - レート制限
    - ログ集約

マイクロサービス層:
  通信: REST + GraphQL
  サービス間: gRPC / Message Queue
  サービスメッシュ: Istio（オプション）

データ層:
  RDB: PostgreSQL
  NoSQL: MongoDB
  キャッシュ: Redis
  検索: Elasticsearch
  メッセージ: Kafka/RabbitMQ

インフラ層:
  コンテナ: Docker
  オーケストレーション: Kubernetes
  CI/CD: GitHub Actions
  監視: Prometheus + Grafana
```

## 成果物

以下のファイルが`outputs/4-architecture/`に生成されます：

1. **bounded-contexts.md**
   - 境界コンテキスト定義
   - ユビキタス言語
   - チーム割り当て

2. **context-map.md**
   - コンテキスト間の関係
   - 統合パターン
   - ACL設計

3. **microservices.md**
   - 詳細サービス設計
   - エンドポイント定義
   - データモデル

4. **api-specification.yaml**
   - OpenAPI仕様
   - GraphQLスキーマ
   - 認証仕様

5. **technical-architecture.md**
   - 全体アーキテクチャ図
   - 技術スタック選定理由
   - 非機能要件対応

## 決定記録

**AADR-001: マイクロサービスアーキテクチャ採用**
```yaml
決定: マイクロサービスアーキテクチャの採用
理由:
  - チームの自律性
  - 独立デプロイメント
  - 技術選択の自由度
代替案: モノリス、モジュラーモノリス
影響: 運用複雑性の増加、開発効率の向上
```

**AADR-002: API Gateway パターン**
```yaml
決定: 単一API Gatewayによる統合
理由:
  - 認証の一元化
  - クロスカッティング処理
  - クライアント簡素化
代替案: BFF、直接通信
影響: 単一障害点、パフォーマンスオーバーヘッド
```

## チェックリスト

- [ ] CL1と境界コンテキストが1:1対応しているか
- [ ] コンテキスト間の関係が明確か
- [ ] API仕様が完全で実装可能か
- [ ] 技術選択が要件に適合しているか
- [ ] 非機能要件が考慮されているか

## 次のステップ

アーキテクチャ設計が完了したら、ソフトウェア設計フェーズへ：

```bash
/parasol:5-software
```

---

*アーキテクチャはビジネス要求と技術実装の架け橋です。両方の視点でバランスを取りましょう。*