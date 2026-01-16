# Transport Planning Service（輸送計画サービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Transport Planning Service |
| **日本語名** | 輸送計画サービス |
| **ドメインタイプ** | Core |
| **所有チーム** | SCM戦略部 / 物流企画チーム |
| **リポジトリ** | `suntory/scm-transport-planning` |

---

## 含まれるBounded Contexts

- **TransportPlanningContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/transport-planning-operations.md`
  - 担当CL3: CL3-201〜CL3-206（6オペレーション）

**統合理由**:
配車計画、ルート最適化、車両追跡は輸送オペレーションの核心であり、
2024年問題対応（ドライバー労働時間規制）の観点から一体的に管理する必要がある。
traevo連携や大王グループとの共同輸送もこのサービスが統括する。

---

## 責務

### ミッション
2024年問題に対応しながら、配送効率を最大化し、CO2排出量を削減する持続可能な輸送体制を実現する。

### 主要責務
1. **配車計画**: ドライバー労働時間を遵守した最適配車
2. **ルート最適化**: 配送ルートの効率化とCO2削減
3. **車両追跡**: traevo連携によるリアルタイム位置把握
4. **共同輸送**: 大王グループとの共同配送調整

---

## ドメインモデル

### Aggregates

```yaml
DeliverySchedule:
  説明: 配送スケジュールの集約ルート
  Root Entity: DeliverySchedule
  Entities:
    - DeliveryStop
    - DeliveryRoute
  Value Objects:
    - TimeWindow
    - DeliveryPriority
    - LoadCapacity

VehicleAssignment:
  説明: 車両割当の集約ルート
  Root Entity: VehicleAssignment
  Entities:
    - AssignedDriver
    - AssignedVehicle
  Value Objects:
    - DriverWorkingHours
    - VehicleCapacity
    - RestRequirement

JointDelivery:
  説明: 共同輸送の集約ルート
  Root Entity: JointDelivery
  Entities:
    - PartnerAllocation
    - SharedRoute
  Value Objects:
    - CostShare
    - LoadShare
    - PartnerSLA
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/transport

Endpoints:
  # 配送スケジュール
  GET /delivery-schedules: 配送スケジュール一覧
  GET /delivery-schedules/{warehouse}/{date}: 倉庫・日付別スケジュール
  POST /delivery-schedules: 配送スケジュール作成
  PUT /delivery-schedules/{id}: 配送スケジュール更新

  # 配車・ルート
  POST /pickup-requests: 集荷リクエスト作成
  GET /routes/{id}/optimize: ルート最適化提案取得
  POST /routes/{id}/optimize: ルート最適化実行

  # 車両追跡
  GET /vehicles/{id}/location: 車両位置取得（traevo経由）
  GET /vehicles/{id}/eta: 到着予定時刻取得

  # 配送状況
  PUT /delivery-status/{id}: 配送状況更新
  GET /delivery-status/{id}: 配送状況取得

  # 共同輸送
  POST /joint-delivery/requests: 共同配送リクエスト
  GET /joint-delivery/status: 共同配送状況確認
```

---

## イベント

### Published Events

```yaml
DeliveryScheduleCreated: 配送スケジュールが作成された
PickupRequestCreated: 集荷リクエストが作成された
DeliveryCompleted: 配送が完了した
DeliveryDelayed: 配送遅延が発生した
RouteOptimized: ルート最適化が完了した
JointDeliveryConfirmed: 共同配送が確定した
```

### Subscribed Events

```yaml
DemandForecastCreated: (from DemandPlanningContext)
  → 需要予測に基づく輸送計画立案

ProductionPlanApproved: (from DemandPlanningContext)
  → 生産計画に合わせた配車計画調整

InventoryAllocated: (from WarehouseContext)
  → 在庫引当完了後の配送スケジュール確定
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: transport_planning
  Tables:
    - delivery_schedules
    - vehicle_assignments
    - delivery_routes
    - joint_deliveries
    - delivery_status_logs

Geospatial Store:
  Type: PostGIS extension
  Purpose: ルート最適化用地理空間データ

Cache:
  Type: Redis
  Purpose: 車両位置情報のキャッシュ（traevoから取得）
  TTL: 5分
```

---

## 外部連携

### traevo連携

```yaml
Integration:
  Type: REST API (ACL経由)
  Direction: Bidirectional

Inbound:
  - 車両位置情報（5分間隔ポーリング）
  - ルート情報
  - 到着予測

Outbound:
  - アラート通知

ACL Location: Integration Hub Service
Data Mapping:
  traevo_vehicle → internal_Vehicle
  traevo_location → internal_Position
```

### 大王グループ連携

```yaml
Integration:
  Type: Partner API (ACL経由)
  Direction: Bidirectional

Operations:
  - 共同配送リクエスト
  - 積載効率計算
  - コスト分担計算

ACL Location: Integration Hub Service
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Demand Planning Service | 需要予測・生産計画データ |
| Integration Hub | traevo、大王グループ連携 |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Warehouse Service | 配送スケジュール、集荷リクエスト |
| Environmental Reporting Service | CO2排出量データ |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 高
  Replicas: 3-6
  Note: リアルタイム追跡のため常時高可用性

Availability:
  SLA: 99.9%
  Note: 配送中断は顧客影響大のため高SLA

Performance:
  位置取得API: 200ms以内
  ルート最適化: 5秒以内
  配送スケジュール作成: 3秒以内

External Dependencies:
  traevo:
    Circuit Breaker: failure_threshold=5, timeout=30秒
    Fallback: 前回位置情報をキャッシュから返却

  大王グループ:
    Circuit Breaker: failure_threshold=3, timeout=60秒
    Fallback: 単独配送にフォールバック
```

---

## 2024年問題対応

```yaml
Driver_Working_Hours_Management:
  制約:
    - 1日の拘束時間: 13時間以内
    - 連続運転時間: 4時間以内（30分休憩必須）
    - 1週間の拘束時間: 65時間以内

  システム対応:
    - 配車計画時に労働時間を自動計算
    - 違反予測時にアラート発出
    - 休憩ポイントの自動挿入

Joint_Delivery_Strategy:
  目的: ドライバー不足への対応、積載効率向上
  パートナー: 大王グループ（製紙・日用品）
  効果:
    - 積載効率: 20%向上
    - CO2排出: 15%削減
```

---

## 設計ストーリー

### なぜCoreドメインか
2024年問題により、輸送効率化は経営課題となった。
単なるコスト削減ではなく、事業継続性に直結する戦略的領域。
競合との差別化ポイントでもあり、継続的な最適化投資が必要。

### なぜACLでtraevo連携か
traevoは外部ベンダーシステムであり、APIやデータモデルが変更される可能性がある。
ACLで内部モデルを保護し、traevoの変更から独立させることで、
安定した輸送計画機能を維持する。

---

**作成**: Parasol V5 Phase 4
