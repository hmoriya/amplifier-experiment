# ADR-005: API Gateway パターンの採用

## ステータス
承認済み（2025-01-15）

## コンテキスト

8つのマイクロサービスへのアクセスを管理するため、クライアントとサービス間の通信パターンを決定する必要がある。

### 要件

1. **クライアント種別**:
   - Web アプリケーション（社内SCM管理画面）
   - モバイルアプリ（倉庫作業員、配送ドライバー）
   - 外部システム連携（EDI、traevo、日立協創）
   - 内部サービス間通信

2. **機能要件**:
   - 認証・認可の一元管理
   - レート制限（DDoS対策）
   - リクエストルーティング
   - プロトコル変換（REST/gRPC）
   - APIバージョニング

3. **非機能要件**:
   - 低レイテンシ（受注APIは500ms以内）
   - 高可用性（99.9%以上）
   - 監視・ログ集約

## 決定

**API Gatewayパターンを採用し、BFF（Backend for Frontend）と組み合わせる。**

### アーキテクチャ構成

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              クライアント層                                   │
├───────────────────┬───────────────────┬─────────────────────────────────────┤
│    Web App        │   Mobile App      │      External Systems               │
│   (管理画面)       │  (倉庫/配送)       │   (EDI, traevo, 日立協創)            │
└─────────┬─────────┴─────────┬─────────┴──────────────┬──────────────────────┘
          │                   │                        │
          ▼                   ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API Gateway Layer                                  │
├───────────────────┬───────────────────┬─────────────────────────────────────┤
│    Web BFF        │   Mobile BFF      │      Integration Gateway            │
│  (GraphQL)        │  (REST/gRPC)      │      (REST + Protocol Transform)    │
├───────────────────┴───────────────────┴─────────────────────────────────────┤
│                        共通機能                                              │
│  ・認証/認可 (JWT)  ・レート制限  ・ログ集約  ・トレーシング                    │
└─────────────────────────────────────────────────────────────────────────────┘
          │                   │                        │
          ▼                   ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Service Mesh (Internal)                              │
├─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬────────┬────────┤
│  Order  │ Demand  │Transport│Warehouse│ Food    │ Trace-  │ Water  │ Env    │
│ Service │Planning │Planning │ Service │ Safety  │ ability │ Sustain│Report  │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴────────┴────────┘
```

### Gateway構成詳細

```yaml
API_Gateway:
  Type: Kong / AWS API Gateway / Azure API Management

  Web_BFF:
    Protocol: GraphQL
    Purpose: 複雑なデータ集約、柔軟なクエリ
    Clients: 社内Web管理画面
    Features:
      - Schema stitching from multiple services
      - Query optimization
      - Caching (DataLoader)

  Mobile_BFF:
    Protocol: REST (OpenAPI 3.0) + gRPC (高頻度操作)
    Purpose: 軽量レスポンス、オフライン対応
    Clients: 倉庫作業アプリ、配送ドライバーアプリ
    Features:
      - Response compression
      - Optimized payloads for mobile
      - Push notification integration

  Integration_Gateway:
    Protocol: REST + Protocol Transform
    Purpose: 外部システム連携
    Clients: EDI (卸売/小売), traevo, 日立協創
    Features:
      - EDI format conversion (JEDICOS ↔ JSON)
      - Rate limiting per partner
      - ACL (Anti-Corruption Layer)
```

### 認証・認可

```yaml
Authentication:
  Type: OAuth 2.0 + JWT
  Provider: Auth0 / Azure AD B2C / Keycloak

  Token Structure:
    Header:
      alg: RS256
      typ: JWT
    Payload:
      sub: user_id
      roles: [scm_operator, warehouse_staff]
      permissions: [orders:read, orders:write, inventory:read]
      exp: timestamp

Authorization:
  Pattern: RBAC (Role-Based Access Control)

  Roles:
    - scm_admin: 全権限
    - scm_operator: 受注・出荷管理
    - warehouse_staff: 倉庫操作
    - delivery_driver: 配送操作（読み取り主体）
    - quality_inspector: 品質検査
    - partner_readonly: 外部パートナー（参照のみ）
```

### レート制限

```yaml
Rate_Limiting:
  Global:
    Default: 1000 req/min per client

  Per_Endpoint:
    /api/orders (POST): 100 req/min  # 受注登録
    /api/orders (GET): 500 req/min   # 受注照会
    /api/inventory: 1000 req/min     # 在庫照会

  Per_Partner:
    EDI_Partners: 200 req/min
    traevo: 500 req/min
    日立協創: 100 req/min
```

## 結果

### 良い影響

1. **クライアント最適化**: BFFにより各クライアントに最適なAPI提供
2. **セキュリティ集約**: 認証・認可を一元管理
3. **運用監視**: 全トラフィックの可視化
4. **バージョニング**: APIバージョン管理が容易
5. **レート制限**: DDoS対策、パートナー別の制御

### トレードオフ

1. **単一障害点リスク**: Gatewayがダウンすると全サービスに影響
   - 軽減策: 高可用性構成（複数AZ、Auto Scaling）
2. **レイテンシ増加**: ホップが1つ増える
   - 軽減策: 軽量なGateway選定、キャッシング
3. **複雑性**: BFF開発・保守の追加コスト
   - 正当化: クライアント体験の大幅な向上

### リスク

1. **Gateway障害**: 全サービスへのアクセス不能
   - 軽減策: サーキットブレーカー、フェイルオーバー
2. **BFF肥大化**: ビジネスロジックがBFFに漏れる
   - 軽減策: BFFは集約・変換のみ、ロジックはサービス側に

## 代替案

### 代替案1: クライアント直接呼び出し
- **メリット**: シンプル、低レイテンシ
- **却下理由**: 認証分散、クライアント複雑化、セキュリティリスク

### 代替案2: 単一API Gateway（BFFなし）
- **メリット**: シンプル、運用容易
- **却下理由**: クライアント別最適化困難、GraphQL/REST混在が困難

### 代替案3: Service Meshのみ（Istio/Linkerd）
- **メリット**: サービス間通信の制御
- **却下理由**: 外部クライアント対応、認証統合が不十分

## API設計標準

### REST API標準

```yaml
REST_Standards:
  Base URL: https://api.suntory-scm.example.com/v1

  Versioning: URL path (v1, v2)

  HTTP Methods:
    GET: リソース取得
    POST: リソース作成
    PUT: リソース更新（全体）
    PATCH: リソース更新（部分）
    DELETE: リソース削除

  Response Format:
    Success:
      status: 200 / 201 / 204
      data: { ... }
      meta: { pagination, ... }

    Error:
      status: 400 / 401 / 403 / 404 / 500
      error:
        code: "ERR_ORDER_NOT_FOUND"
        message: "Order not found"
        details: { ... }
```

### GraphQL標準（Web BFF）

```graphql
# Schema Example
type Query {
  order(id: ID!): Order
  orders(filter: OrderFilter, pagination: Pagination): OrderConnection
  inventoryStatus(warehouseId: ID!): InventoryStatus
}

type Mutation {
  createOrder(input: CreateOrderInput!): Order
  updateOrderStatus(id: ID!, status: OrderStatus!): Order
}

type Subscription {
  orderStatusChanged(orderId: ID!): OrderStatusEvent
}
```

## 関連

- ADR-001: マイクロサービスアーキテクチャの採用
- ADR-002: イベントバスの選択
- 統合パターン: `outputs/4-architecture/integration-patterns.md`
- Context Map: `outputs/4-architecture/context-map.md`

---

**作成者**: Parasol V5 Phase 4
**レビュー者**: セキュリティチーム、フロントエンドチーム、アーキテクチャチーム
