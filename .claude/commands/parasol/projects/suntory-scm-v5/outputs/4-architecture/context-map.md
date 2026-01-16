# Context Map

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5
**作成日**: 2025-01-15
**Phase**: 4 - Application Design

---

## 概要

8つの Bounded Context（BC）間の関係性を Context Map として定義します。
統合パターンと依存関係を明確化し、サービス間のコミュニケーション設計の基盤とします。

---

## 1. Context Map 全体図

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              サントリー SCM Context Map                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────┐      U/D        ┌─────────────────┐                               │
│  │ DemandPlanning  │ ───────────────▶│TransportPlanning│                               │
│  │    Context      │                 │    Context      │                               │
│  │    [Core]       │                 │    [Core]       │                               │
│  └────────┬────────┘                 └────────┬────────┘                               │
│           │                                   │                                         │
│           │ Published                         │ U/D                                     │
│           │ Language                          ▼                                         │
│           │                          ┌─────────────────┐                               │
│           │                          │   Warehouse     │                               │
│           │                          │    Context      │                               │
│           │                          │    [VCI]        │                               │
│           │                          └────────┬────────┘                               │
│           │                                   │                                         │
│           │                                   │ Published                               │
│           ▼                                   │ Language                                │
│  ┌─────────────────┐                          ▼                                         │
│  │     Order       │◀─────────────────┌─────────────────┐      Partnership             │
│  │    Context      │                  │  FoodSafety     │◀────────────────▶┌─────────┐ │
│  │   [Generic]     │                  │    Context      │                  │Traceabil│ │
│  └────────┬────────┘                  │    [VCI]        │                  │  ity    │ │
│           │                           └─────────────────┘                  │Context  │ │
│           │ Open Host                                                      │ [VCI]   │ │
│           │ Service                                                        └────┬────┘ │
│           ▼                                                                     │      │
│  ┌─────────────────┐                                                            │      │
│  │   External      │                 ┌─────────────────┐                        │      │
│  │   Systems       │                 │    Water        │      Conformist        │      │
│  │ (EDI/卸売/小売) │                 │ Sustainability  │◀─────────────────┐     │      │
│  └─────────────────┘                 │    Context      │                  │     │      │
│                                      │    [Core]       │          ┌───────┴─────┴───┐  │
│                                      └─────────────────┘          │ Environmental   │  │
│                                                                   │   Reporting     │  │
│                                                                   │    Context      │  │
│                                                                   │  [Supporting]   │  │
│                                                                   └─────────────────┘  │
│                                                                                         │
│  【外部パートナー連携】                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────┐      │
│  │ traevo ──API──▶ TransportPlanning                                           │      │
│  │ 日立協創 ──Blockchain──▶ Traceability                                       │      │
│  │ 大王グループ ──Partner API──▶ TransportPlanning                             │      │
│  └──────────────────────────────────────────────────────────────────────────────┘      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. BC 間関係の詳細

### 2.1 DemandPlanning → TransportPlanning (Upstream/Downstream)

```yaml
Relationship:
  type: Customer-Supplier (U/D)
  upstream: DemandPlanningContext
  downstream: TransportPlanningContext

Contract:
  published_events:
    - DemandForecastCreated
    - ProductionPlanApproved
    - InventoryTargetUpdated

  api_endpoints:
    - GET /demand-forecasts/{region}/{period}
    - GET /production-plans/{factory}/{date}

Rationale: |
  需要予測と生産計画が確定した後に輸送計画を立案する。
  DemandPlanningが計画を「供給」し、TransportPlanningが「消費」する
  明確な上下関係。
```

### 2.2 TransportPlanning → Warehouse (Upstream/Downstream)

```yaml
Relationship:
  type: Customer-Supplier (U/D)
  upstream: TransportPlanningContext
  downstream: WarehouseContext

Contract:
  published_events:
    - DeliveryScheduleCreated
    - PickupRequestCreated
    - DeliveryCompleted

  api_endpoints:
    - GET /delivery-schedules/{warehouse}/{date}
    - POST /pickup-requests

Rationale: |
  輸送計画に基づいて倉庫への入出庫が発生する。
  TransportPlanningが配送計画を「供給」し、
  Warehouseがオペレーションを「実行」する。
```

### 2.3 FoodSafety ↔ Traceability (Partnership)

```yaml
Relationship:
  type: Partnership
  partners:
    - FoodSafetyContext
    - TraceabilityContext

Contract:
  shared_events:
    - QualityInspectionCompleted
    - LotTraceRecorded
    - TemperatureAnomalyDetected

  bidirectional_api:
    FoodSafety_to_Traceability:
      - POST /lot-quality-records
    Traceability_to_FoodSafety:
      - GET /lot-trace/{lotNumber}
      - POST /recall-candidates

Rationale: |
  品質管理とトレーサビリティは双方向の協力関係。
  品質検査結果はトレーサビリティに記録され、
  リコール時はトレーサビリティから品質情報を参照する。
  日立協創システムとの連携でこの関係が強化される。
```

### 2.4 WaterSustainability → EnvironmentalReporting (Customer-Supplier)

```yaml
Relationship:
  type: Customer-Supplier with Conformist
  upstream: WaterSustainabilityContext
  downstream: EnvironmentalReportingContext
  pattern: Conformist

Contract:
  published_data:
    - WaterBalanceReport
    - ForestCarbonSequestration
    - BiodiversityMetrics

  api_endpoints:
    - GET /water-balance/{year}
    - GET /forest-carbon/{area}/{period}

Rationale: |
  水源涵養データをそのまま環境報告に使用。
  EnvironmentalReportingはWaterSustainabilityの
  データモデルに「準拠（Conformist）」する。
  変換不要で効率的。
```

### 2.5 Order → External Systems (Open Host Service)

```yaml
Relationship:
  type: Open Host Service
  host: OrderContext
  external_systems:
    - 卸売業者（EDI）
    - 小売チェーン（EDI）
    - サプライヤー（発注）

Contract:
  published_language: EDI標準（JEDICOS等）

  api_endpoints:
    - POST /orders (受注)
    - POST /purchase-orders (発注)
    - GET /order-status/{orderId}

Rationale: |
  業界標準のEDIフォーマットで外部と連携。
  OrderContextが「ホスト」として標準インターフェースを提供。
  内部モデルと外部モデルの変換は境界で実施。
```

### 2.6 DemandPlanning → Order (Published Language)

```yaml
Relationship:
  type: Published Language
  publisher: DemandPlanningContext
  consumer: OrderContext

Contract:
  shared_vocabulary:
    - ProductCode: "製品コード体系"
    - SKU: "在庫管理単位"
    - Region: "販売地域コード"
    - CustomerSegment: "顧客セグメント"

Rationale: |
  製品・顧客に関する共通語彙を定義。
  需要予測で使用する製品コードと
  受注で使用する製品コードを統一。
```

### 2.7 Warehouse → FoodSafety (Published Language)

```yaml
Relationship:
  type: Published Language
  publisher: WarehouseContext
  consumer: FoodSafetyContext

Contract:
  shared_vocabulary:
    - LotNumber: "ロット番号体系"
    - Location: "保管場所コード"
    - StorageCondition: "保管条件（温度帯等）"

Rationale: |
  倉庫で管理するロット情報を品質管理で使用。
  ロット番号の採番ルールを共通化。
```

---

## 3. 外部システム連携

### 3.1 traevo 連携（TransportPlanning）

```yaml
Integration:
  system: traevo（車両位置追跡システム）
  boundary: TransportPlanningContext

Pattern: Anti-Corruption Layer (ACL)

API:
  direction: TransportPlanning → traevo
  protocol: REST API
  endpoints:
    - GET /vehicles/{vehicleId}/location
    - GET /vehicles/{vehicleId}/route
    - POST /vehicles/{vehicleId}/alert

Data_mapping:
  traevo_vehicle → internal_Vehicle
  traevo_location → internal_Position
  traevo_route → internal_DeliveryRoute

Rationale: |
  traevoは外部ベンダーシステム。
  ACLで内部モデルを保護し、
  traevoのモデル変更から独立させる。
```

### 3.2 日立協創トレーサビリティ連携（Traceability）

```yaml
Integration:
  system: 日立協創ブロックチェーン基盤
  boundary: TraceabilityContext

Pattern: Shared Kernel (読み取り専用)

API:
  direction: Bidirectional
  protocol: Blockchain API
  operations:
    - recordLotTrace: ロット情報記録
    - queryLotHistory: 履歴照会
    - initiateRecall: リコール開始

Shared_data:
  - LotTraceRecord（ブロックチェーン上）
  - ManufactureInfo
  - ShipmentHistory

Rationale: |
  日立との協創プロジェクトで共同開発したシステム。
  ブロックチェーン上のデータは両社で共有（Shared Kernel）。
  ただしサントリー側は読み取り中心、書き込みは制御下で実施。
```

### 3.3 大王グループ連携（TransportPlanning）

```yaml
Integration:
  system: 大王グループ物流システム
  boundary: TransportPlanningContext

Pattern: Partnership with ACL

API:
  direction: Bidirectional
  protocol: Partner API
  endpoints:
    - POST /joint-delivery/requests  # 共同配送依頼
    - GET /joint-delivery/status     # 状況確認
    - POST /joint-delivery/confirm   # 配送確定

Coordination:
  - 共同輸送スケジュール調整
  - 積載効率の最適化
  - コスト分担計算

Rationale: |
  2024年問題対応の共同輸送パートナー。
  対等なパートナーシップ関係。
  ACLで両社のモデル差異を吸収。
```

### 3.4 EDI 連携（Order）

```yaml
Integration:
  system: EDI基盤（卸売・小売）
  boundary: OrderContext

Pattern: Open Host Service

Protocols:
  - JEDICOS（日本標準）
  - 各社独自EDI

Message_types:
  - 発注データ（D01）
  - 出荷案内（D03）
  - 受領報告（D05）
  - 請求データ（D08）

Translation:
  - EDIメッセージ ↔ 内部Order
  - 取引先コード ↔ 内部CustomerCode

Rationale: |
  業界標準のEDIで卸売・小売と連携。
  Open Host Serviceパターンで
  標準インターフェースを提供。
```

---

## 4. 統合パターンサマリー

| 関係 | パターン | 理由 |
|------|---------|------|
| DemandPlanning → TransportPlanning | U/D | 計画の供給→消費 |
| TransportPlanning → Warehouse | U/D | 計画→実行 |
| FoodSafety ↔ Traceability | Partnership | 双方向協力 |
| WaterSustainability → EnvironmentalReporting | Conformist | データ準拠 |
| Order ↔ External | Open Host Service | 標準IF提供 |
| DemandPlanning ↔ Order | Published Language | 共通語彙 |
| Warehouse ↔ FoodSafety | Published Language | 共通語彙 |
| TransportPlanning ↔ traevo | ACL | 外部保護 |
| Traceability ↔ 日立 | Shared Kernel | 協創共有 |
| TransportPlanning ↔ 大王 | Partnership + ACL | パートナー連携 |

---

## 5. 依存関係のフロー図

### 5.1 計画→実行フロー

```
┌──────────────────────────────────────────────────────────────────┐
│                     計画フェーズ                                 │
│  DemandPlanning ─────▶ 需要予測・生産計画確定                    │
│        │                                                        │
│        ▼                                                        │
│  TransportPlanning ──▶ 輸送計画・配車計画確定                    │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                     実行フェーズ                                 │
│  Warehouse ──────────▶ 入出庫オペレーション                      │
│        │                                                        │
│        ▼                                                        │
│  FoodSafety ─────────▶ 品質管理・HACCP記録                       │
│        │                                                        │
│        ▼                                                        │
│  Traceability ───────▶ ロット追跡記録                            │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 サステナビリティフロー

```
┌──────────────────────────────────────────────────────────────────┐
│  WaterSustainability ─▶ 水源涵養データ収集・水収支計算           │
│        │                                                        │
│        ▼ (Conformist)                                           │
│  EnvironmentalReporting ▶ CO2計算・ESG/規制報告作成              │
└──────────────────────────────────────────────────────────────────┘
```

### 5.3 受発注フロー

```
┌──────────────────────────────────────────────────────────────────┐
│  External (EDI) ◀─────▶ Order Context ◀─────▶ DemandPlanning    │
│                             │                                    │
│                             ▼                                    │
│                     TransportPlanning                            │
│                     (配送指示生成)                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. 設計上の考慮事項

### 6.1 循環依存の回避

現在のContext Mapに循環依存はありません。

**確認済みの依存方向**:
- DemandPlanning → TransportPlanning → Warehouse（一方向）
- WaterSustainability → EnvironmentalReporting（一方向）
- FoodSafety ↔ Traceability（双方向だがPartnership）

### 6.2 障害分離

| BC | 障害時の影響範囲 | 対策 |
|----|----------------|------|
| DemandPlanning | TransportPlanningに波及 | 前日計画をフォールバック |
| TransportPlanning | Warehouseに波及 | 手動配車対応 |
| traevo | TransportPlanningの追跡機能 | 電話連絡フォールバック |
| 日立協創 | Traceabilityの記録 | ローカルDB一時記録 |
| EDI | Orderの受発注 | FAX/メールフォールバック |

### 6.3 将来の拡張性

**追加BC候補**:
- SupplierContext: サプライヤー管理の独立化
- AnalyticsContext: 分析・BI機能の分離
- NotificationContext: 通知機能の共通化

---

**作成**: Parasol V5 Phase 4
