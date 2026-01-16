# ADR-002: イベントバスの選択

## ステータス
承認済み（2025-01-15）

## コンテキスト

マイクロサービス間の非同期通信とイベント駆動アーキテクチャを実現するため、イベントバス/メッセージブローカーの選定が必要。

### 要件

1. **イベント種別**:
   - ドメインイベント（OrderReceived, ShipmentCompleted, QualityApproved等）
   - 統合イベント（外部システムとの連携）
   - Sagaイベント（分散トランザクションの調整）

2. **非機能要件**:
   - 高可用性（99.9%以上）
   - イベント順序保証（同一パーティション内）
   - 永続化（監査・リプレイ用）
   - スケーラビリティ（繁忙期対応）

3. **運用要件**:
   - クラウドネイティブ対応
   - 既存インフラとの親和性
   - 運用チームのスキルセット

## 決定

**Apache Kafka（マネージドサービス）をプライマリイベントバスとして採用する。**

### 採用構成

```yaml
Primary Event Bus:
  Type: Apache Kafka (Managed)
  Provider: Amazon MSK / Azure Event Hubs (Kafka API)

Configurations:
  Replication Factor: 3
  Partitions:
    - high-volume topics (orders, inventory): 12
    - low-volume topics (environmental): 3
  Retention: 7 days (default), 30 days (audit topics)
```

### トピック設計

| トピック | プロデューサー | コンシューマー | パーティション数 |
|---------|--------------|---------------|----------------|
| `orders.events` | Order Service | Warehouse, Transport, Demand | 12 |
| `warehouse.events` | Warehouse Service | Order, Transport, Traceability | 12 |
| `quality.events` | Food Safety Service | Traceability, Order | 6 |
| `shipment.events` | Transport Service | Order, Traceability | 12 |
| `sustainability.events` | Water Sustainability | Environmental Reporting | 3 |

### イベントスキーマ標準

```yaml
Event Schema Standard:
  Format: CloudEvents v1.0
  Serialization: Avro (with Schema Registry)

Example:
  specversion: "1.0"
  type: "suntory.scm.order.received"
  source: "/services/order"
  id: "uuid"
  time: "2025-01-15T10:30:00Z"
  datacontenttype: "application/json"
  data:
    orderId: "ORD-2025-000001"
    customerId: "CUST-001"
    orderLines: [...]
```

## 結果

### 良い影響

1. **高スループット**: 繁忙期の1000 events/secにも対応可能
2. **イベント永続化**: リプレイ、監査対応が可能
3. **順序保証**: パーティションキー（orderId, lotNumber）による順序保証
4. **スケーラビリティ**: パーティション単位での水平スケール
5. **エコシステム**: Kafka Connect、ksqlDB等のエコシステム活用可能

### トレードオフ

1. **運用複雑性**: Zookeeper/KRaft、ブローカー管理が必要
   - 軽減策: マネージドサービス（MSK/Event Hubs）の採用
2. **学習コスト**: パーティション設計、コンシューマーグループの理解が必要
3. **コスト**: RabbitMQ等と比較して高コスト
   - 正当化: ミッションクリティカルなSCMシステムでの信頼性確保

### リスク

1. **Schema進化**: スキーマ変更時の互換性維持
   - 軽減策: Schema Registry + Backward Compatibility
2. **パーティション設計ミス**: ホットスポット発生
   - 軽減策: パーティションキーの慎重な選定、監視の実施

## 代替案

### 代替案1: Amazon SQS / Azure Service Bus
- **メリット**: フルマネージド、シンプル
- **却下理由**: イベント永続化・リプレイ機能が限定的、順序保証が困難

### 代替案2: RabbitMQ
- **メリット**: 低レイテンシ、軽量
- **却下理由**: 大量イベントの永続化、水平スケールに課題

### 代替案3: Amazon EventBridge
- **メリット**: サーバーレス、AWS統合が容易
- **却下理由**: ベンダーロックイン、高スループット時のコスト

## 補足: Point-to-Point通信

EDI処理など、特定のユースケースではSQS/Service Busも併用：

```yaml
Supplementary Queue:
  Type: Amazon SQS / Azure Service Bus
  Use Cases:
    - EDIメッセージ処理キュー
    - 非同期ジョブ処理
    - デッドレターキュー
```

## 関連

- ADR-001: マイクロサービスアーキテクチャの採用
- ADR-004: Saga Choreography パターン
- 統合パターン: `outputs/4-architecture/integration-patterns.md`

---

**作成者**: Parasol V5 Phase 4
**レビュー者**: インフラチーム、アーキテクチャチーム
