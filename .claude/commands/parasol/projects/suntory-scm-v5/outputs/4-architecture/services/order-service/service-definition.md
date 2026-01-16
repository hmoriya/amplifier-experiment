# Order Service（受注サービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Order Service |
| **日本語名** | 受注サービス |
| **ドメインタイプ** | Core |
| **所有チーム** | SCM運用部 / 受注管理チーム |
| **リポジトリ** | `suntory/scm-order` |

---

## 含まれるBounded Contexts

- **OrderContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/order-operations.md`
  - 担当CL3: CL3-801〜CL3-806（6オペレーション）

**統合理由**:
受注管理、出荷指示、EDI連携は顧客接点の核心機能であり、
卸売・小売との取引を円滑に進めるための基盤。
需要データのリアルタイム把握を通じて需要予測精度向上にも貢献する。

---

## 責務

### ミッション
卸売・小売からの受注を迅速に処理し、正確な納期回答と出荷指示を通じて
顧客満足度と物流効率を最大化する。

### 主要責務
1. **受注管理**: 受注の登録・変更・キャンセル処理
2. **納期回答**: 在庫・配送スケジュールに基づく納期計算
3. **出荷指示**: 倉庫への出荷指示発行
4. **EDI連携**: 卸売・小売とのEDI取引処理

---

## ドメインモデル

### Aggregates

```yaml
Order:
  説明: 受注の集約ルート
  Root Entity: Order
  Entities:
    - OrderLine
    - DeliverySchedule
  Value Objects:
    - OrderNumber
    - OrderStatus
    - CustomerInfo
    - DeliveryAddress

ShipmentOrder:
  説明: 出荷指示の集約ルート
  Root Entity: ShipmentOrder
  Entities:
    - ShipmentLine
    - PickingInstruction
  Value Objects:
    - ShipmentNumber
    - ShipmentStatus
    - Priority

EDITransaction:
  説明: EDI取引の集約ルート
  Root Entity: EDITransaction
  Entities:
    - EDIMessage
    - TransactionLog
  Value Objects:
    - MessageType
    - PartnerCode
    - ProcessingStatus
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/orders

Endpoints:
  # 受注管理
  GET /orders: 受注一覧取得
  GET /orders/{id}: 受注詳細取得
  POST /orders: 受注登録
  PUT /orders/{id}: 受注更新
  DELETE /orders/{id}: 受注キャンセル

  # 納期確認
  POST /orders/delivery-date: 納期照会
  GET /orders/{id}/delivery-status: 配送状況確認

  # 出荷指示
  GET /shipment-orders: 出荷指示一覧
  GET /shipment-orders/{id}: 出荷指示詳細
  POST /shipment-orders: 出荷指示作成
  PUT /shipment-orders/{id}/status: 出荷指示ステータス更新

  # EDI
  POST /edi/receive: EDIメッセージ受信
  POST /edi/send: EDIメッセージ送信
  GET /edi/transactions: EDI取引履歴
```

---

## イベント

### Published Events

```yaml
OrderReceived: 受注が登録された
OrderConfirmed: 受注が確定された
OrderCancelled: 受注がキャンセルされた
ShipmentOrderCreated: 出荷指示が作成された
DeliveryDateConfirmed: 納期が確定された
```

### Subscribed Events

```yaml
InventoryAllocated: (from WarehouseContext)
  → 在庫引当完了後の受注ステータス更新

DeliveryScheduleCreated: (from TransportPlanningContext)
  → 配送スケジュール確定後の納期更新

ShipmentCompleted: (from WarehouseContext)
  → 出荷完了後の受注ステータス更新
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: orders
  Tables:
    - orders
    - order_lines
    - shipment_orders
    - shipment_lines
    - edi_transactions
    - edi_messages

Cache:
  Type: Redis
  Purpose: 納期計算結果のキャッシュ
  TTL: 5分

Message Queue:
  Type: Amazon SQS / Azure Service Bus
  Purpose: EDIメッセージ処理キュー
```

---

## 外部連携

### EDI連携（卸売・小売）

```yaml
Integration:
  Type: EDI via Integration Hub
  Direction: Bidirectional
  Protocol: JEDICOS / 各社独自フォーマット

Message Types:
  Inbound:
    - D01（発注）: 受注登録トリガー
    - D05（受領）: 納品確認

  Outbound:
    - D03（出荷案内）: 出荷情報通知
    - D08（請求）: 請求データ送信

Processing:
  Frequency: 4時間ごとバッチ + リアルタイム（大口顧客）
  ACL Location: Integration Hub Service
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Warehouse Service | 在庫情報、出荷可能数 |
| Transport Planning Service | 配送スケジュール |
| Integration Hub | EDI連携 |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Warehouse Service | 出荷指示 |
| Transport Planning Service | 出荷予定データ |
| Demand Planning Service | 受注実績データ |
| Food Safety Service | 品質承認ステータス |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 高
  Replicas: 3-6
  Note: 繁忙期（年末年始、お中元/お歳暮）のバースト対応

Availability:
  SLA: 99.9%
  Note: 受注停止は直接的な売上損失

Performance:
  受注登録API: 500ms以内
  納期照会API: 1秒以内
  出荷指示作成: 2秒以内

Peak Load:
  通常時: 100 orders/min
  繁忙期: 500 orders/min
  設計マージン: 2x（1000 orders/min対応）
```

---

## Saga参加

```yaml
Shipment_Saga:
  役割: 出荷処理の起点（Sagaオーケストレーション開始）

  参加ステップ:
    Step1: ShipmentOrderCreated（出荷指示作成）

  補償トランザクション:
    ShipmentOrderCreated_compensation: CancelShipmentOrder（出荷指示取消）

  Saga開始条件:
    - 受注確定（OrderConfirmed）
    - 在庫引当完了（InventoryAllocated from Warehouse）
    - 配車割当完了（DeliveryAssigned from Transport）

  Saga完了条件:
    - 全ステップ成功 → OrderStatus = Shipped
    - いずれかのステップ失敗 → 補償トランザクション実行
```

---

## 受注フロー

```yaml
Standard_Order_Flow:
  1. EDI受信 / API受注
     ↓
  2. 受注登録（OrderReceived）
     ↓
  3. 在庫照会（Warehouse API）
     ↓
  4. 納期計算（Transport Planning API）
     ↓
  5. 受注確定（OrderConfirmed）
     ↓
  6. 出荷指示作成（ShipmentOrderCreated）
     ↓
  7. Shipment_Saga開始
     ↓
  8. 出荷完了（OrderStatus = Shipped）
     ↓
  9. EDI送信（D03出荷案内）

Exception_Handling:
  在庫不足:
    - バックオーダー登録
    - 分納提案
    - 代替品提案

  配送遅延:
    - 納期変更通知
    - 優先度調整

  品質異常:
    - 出荷保留
    - 代替ロット割当
```

---

## 設計ストーリー

### なぜCoreドメインか
受注管理は顧客との接点であり、SCMの起点となる重要機能。
正確で迅速な受注処理は顧客満足度と売上に直結する。
EDI連携の効率化、納期回答の精度向上は競争優位に繋がる。

### なぜSagaの起点か
出荷処理は複数のサービス（在庫引当、配車、品質検査、追跡）を
跨ぐ長いトランザクションであり、受注サービスがその起点となる。
Choreographyパターンにより、各サービスが独立してイベントを処理し、
失敗時は補償トランザクションで巻き戻す。

### なぜEDI連携をこのサービスに
EDIは受注・出荷案内など受注業務と密接に関連するメッセージが中心。
Integration Hubがプロトコル変換を担当し、
OrderServiceがビジネスロジック（受注登録、出荷案内生成）を担当する分離構成。

---

**作成**: Parasol V5 Phase 4
