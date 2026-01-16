# Warehouse Service（倉庫サービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Warehouse Service |
| **日本語名** | 倉庫サービス |
| **ドメインタイプ** | VCI (Value-Critical Infrastructure) |
| **所有チーム** | SCM運用部 / 倉庫管理チーム |
| **リポジトリ** | `suntory/scm-warehouse` |

---

## 含まれるBounded Contexts

- **WarehouseContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/warehouse-operations.md`
  - 担当CL3: CL3-301〜CL3-306（6オペレーション）

**統合理由**:
入庫、出庫、在庫管理、ロケーション管理は倉庫オペレーションの基本機能であり、
一体的に管理することでトランザクション整合性を確保する。
WMSとの連携もこのサービスが統括する。

---

## 責務

### ミッション
全国約300拠点の倉庫を効率的に管理し、正確な在庫把握と迅速な入出庫を実現する。

### 主要責務
1. **入庫管理**: 製品受入、検品、ロケーション割当
2. **出庫管理**: ピッキング、梱包、出荷
3. **在庫管理**: リアルタイム在庫把握、棚卸
4. **ロット追跡**: FoodSafety/Traceabilityへのロット情報提供

---

## ドメインモデル

### Aggregates

```yaml
Inventory:
  説明: 在庫の集約ルート
  Root Entity: InventoryItem
  Entities:
    - InventoryLot
    - InventoryLocation
  Value Objects:
    - StockQuantity
    - ExpirationDate
    - StorageCondition

InboundShipment:
  説明: 入庫の集約ルート
  Root Entity: InboundShipment
  Entities:
    - ReceivedItem
    - InspectionResult
  Value Objects:
    - ReceiptQuantity
    - QualityGrade
    - LocationAssignment

OutboundShipment:
  説明: 出庫の集約ルート
  Root Entity: OutboundShipment
  Entities:
    - PickedItem
    - PackedUnit
  Value Objects:
    - ShipmentQuantity
    - PackingSpec
    - ShippingLabel
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/warehouse

Endpoints:
  # 在庫管理
  GET /inventory: 在庫一覧取得
  GET /inventory/{product}: 製品別在庫取得
  GET /inventory/location/{locationId}: ロケーション別在庫
  PUT /inventory/{id}/adjust: 在庫調整（棚卸差異等）

  # 入庫
  POST /inbound: 入庫予定登録
  PUT /inbound/{id}/receive: 入庫実績登録
  GET /inbound/{id}/status: 入庫状況確認

  # 出庫
  POST /outbound: 出庫指示作成
  PUT /outbound/{id}/pick: ピッキング完了登録
  PUT /outbound/{id}/ship: 出荷完了登録
  GET /outbound/{id}/status: 出庫状況確認

  # 倉庫状況
  GET /warehouse-status: 全倉庫状況サマリー
  GET /warehouse-status/{warehouseId}: 倉庫別状況
```

---

## イベント

### Published Events

```yaml
InventoryAllocated: 在庫引当が完了した
InventoryUpdated: 在庫が更新された
InboundCompleted: 入庫が完了した
OutboundCompleted: 出庫が完了した
ShipmentCompleted: 出荷が完了した
LotRegistered: 新しいロットが登録された
```

### Subscribed Events

```yaml
DeliveryScheduleCreated: (from TransportPlanningContext)
  → 配送スケジュールに基づく出庫準備

PickupRequestCreated: (from TransportPlanningContext)
  → 集荷リクエストに基づくピッキング開始

InventoryTargetUpdated: (from DemandPlanningContext)
  → 在庫目標に基づく補充アラート
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: warehouse
  Tables:
    - inventory_items
    - inventory_lots
    - inventory_locations
    - inbound_shipments
    - outbound_shipments
    - warehouse_transactions

Cache:
  Type: Redis
  Purpose: リアルタイム在庫数量のキャッシュ
  TTL: 1分（頻繁に更新されるため短め）
```

---

## 外部連携

### WMS連携

```yaml
Integration:
  Type: REST API / File
  Direction: Bidirectional

Outbound:
  - 入出庫指示
  - 在庫調整指示

Inbound:
  - 入出庫実績
  - 棚卸結果

Protocol: 倉庫事業者ごとに異なる（Integration Hub経由で統一）
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Transport Planning Service | 配送スケジュール、集荷リクエスト |
| Demand Planning Service | 在庫目標データ |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Food Safety Service | ロット情報、保管条件 |
| Traceability Service | ロット移動履歴 |
| Environmental Reporting Service | 倉庫エネルギー消費データ |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 高
  Replicas: 3-6
  Note: 全国300拠点からの同時アクセスに対応

Availability:
  SLA: 99.9%
  Note: 在庫操作の中断は出荷遅延に直結

Performance:
  在庫照会API: 100ms以内
  在庫引当処理: 500ms以内
  在庫更新: 200ms以内

Consistency:
  在庫数量: 強整合性（二重引当防止）
  在庫履歴: 結果整合性（15分以内）
```

---

## Published Language（共有語彙）

```yaml
Shared_Vocabulary:
  FoodSafetyContextとの共有:
    - LotNumber: ロット番号体系（LOT-YYYY-NNNNNN形式）
    - Location: 保管場所コード（WH-XXX-YY-ZZ形式）
    - StorageCondition: 保管条件（温度帯: 常温/冷蔵/冷凍）

  TraceabilityContextとの共有:
    - LotNumber: 同上
    - MovementType: 移動種別（入庫/出庫/倉庫間移動）
```

---

## Saga参加

```yaml
Shipment_Saga:
  役割: 在庫引当・出庫実行を担当

  参加ステップ:
    Step2: InventoryAllocated（在庫引当完了）
    Step6: ShipmentCompleted（出庫完了）

  補償トランザクション:
    InventoryAllocated_compensation: ReleaseInventory（引当解除）
    ShipmentCompleted_compensation: CancelShipment（出庫取消）
```

---

## 設計ストーリー

### なぜVCIドメインか
在庫管理は「失敗が許されない」基盤機能。
二重引当や在庫不整合は直接的な出荷遅延・欠品を引き起こす。
差別化要因ではないが、品質維持が必須のため内製で厳密に管理する。

### なぜPublished Languageか
ロット番号はFoodSafety、Traceabilityと共有する必要がある。
採番ルールを統一することで、システム間のデータ連携を簡素化。
WarehouseContextが「発行者」として語彙を定義し、他BCが準拠する。

---

**作成**: Parasol V5 Phase 4
