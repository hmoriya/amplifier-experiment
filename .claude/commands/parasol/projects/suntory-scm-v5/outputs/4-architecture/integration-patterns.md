# 統合パターン設計

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**Phase**: 4 - Application Design

---

## 概要

サントリー SCM システムの統合パターンを定義します。
Parasol V5.1 のデフォルト統合パターンに基づき、シンプルさと実用性を重視した設計を行います。

---

## 1. 採用パターン

### 1.1 Orchestration at the Edge

**適用箇所**:
- フロントエンド（SCM管理画面）からのAPI呼び出し
- モバイルアプリ（倉庫作業者向け）からのAPI呼び出し
- BIダッシュボードからのデータ取得

**理由**:
- SCM業務は計画→実行→報告の明確なフローを持つ
- フロントエンドがフローを制御することでデバッグが容易
- 複雑なイベント駆動の回避

**実装方針**:

```yaml
Frontend_Orchestration:
  planning_flow:
    1. GET /demand-forecasts → DemandPlanningContext
    2. POST /production-plans → DemandPlanningContext
    3. POST /transport-plans → TransportPlanningContext
    4. GET /warehouse-status → WarehouseContext

  execution_flow:
    1. GET /delivery-schedules → TransportPlanningContext
    2. POST /pickup-requests → WarehouseContext
    3. PUT /delivery-status → TransportPlanningContext
    4. POST /quality-records → FoodSafetyContext

  reporting_flow:
    1. GET /water-balance → WaterSustainabilityContext
    2. GET /co2-emissions → EnvironmentalReportingContext
    3. GET /esg-metrics → EnvironmentalReportingContext
```

### 1.2 Integration Hub Pattern

**適用箇所**:
- 基幹システム（SAP等）との統合
- EDI連携（卸売・小売）
- パートナーシステム連携（traevo、日立、大王グループ）

**理由**:
- レガシーシステムの複雑性を隔離
- バッチとリアルタイムの混在を管理
- 外部システム変更からの保護

**統合ハブ設計**:

```yaml
Integration_Hub_Service:

  legacy_integrations:
    sap_erp:
      protocol: RFC/BAPI
      sync_method: バッチ（日次）+ リアルタイム（受注）
      data_flow:
        - 製品マスタ → DemandPlanning, Order
        - 在庫データ → Warehouse
        - 会計データ ← Order

    wms_systems:
      protocol: REST API / File
      sync_method: リアルタイム
      data_flow:
        - 入出庫指示 → 各倉庫WMS
        - 実績データ ← 各倉庫WMS

  partner_integrations:
    traevo:
      protocol: REST API
      sync_method: リアルタイム（ポーリング/Webhook）
      data_mapping:
        traevo_vehicle → internal_Vehicle
        traevo_location → internal_Position
      acl_location: integration-hub

    hitachi_traceability:
      protocol: Blockchain API
      sync_method: イベント駆動
      shared_data:
        - LotTraceRecord
      acl_location: traceability-context

    daio_logistics:
      protocol: Partner API
      sync_method: リアルタイム
      coordination:
        - 共同輸送スケジュール
        - 積載効率計算
      acl_location: integration-hub

  edi_integrations:
    wholesale_retail:
      protocol: JEDICOS / 各社独自
      sync_method: バッチ（複数回/日）
      message_types:
        - D01（発注）
        - D03（出荷案内）
        - D05（受領）
        - D08（請求）
      translation_layer: integration-hub

  cache_strategy:
    master_data:
      ttl: 24時間
      items: 製品マスタ、取引先マスタ

    transaction_data:
      ttl: 5-15分
      items: 在庫状況、車両位置
```

---

## 2. 通信プロトコル標準

### 2.1 同期通信（REST API）

**使用ケース**:
- フロントエンドからのAPI呼び出し
- BC間の直接連携（計画データ取得等）
- 外部パートナーAPI連携

**標準仕様**:

```yaml
REST_API_Standards:
  base_url: /api/v1/{context-name}

  authentication:
    internal: JWT Bearer Token
    external: API Key + OAuth 2.0

  rate_limiting:
    internal: なし（信頼境界内）
    external: 100 req/min

  pagination:
    default_page_size: 50
    max_page_size: 500
    cursor_based: true

  error_format:
    structure:
      code: "ERR_DEMAND_001"
      message: "需要予測データが見つかりません"
      details: {}
      trace_id: "uuid"

  documentation: OpenAPI 3.0
```

### 2.2 非同期通信（イベント駆動）

**使用ケース（限定的）**:
- ロット追跡記録（日立ブロックチェーン連携）
- 品質異常アラート
- 環境データ収集

**理由**:
同期通信を基本とし、非同期は以下の場合のみ使用:
- 外部システムの応答時間が不確定
- 失敗時のリトライが必要
- 疎結合が明確に有利

**標準仕様**:

```yaml
Event_Driven_Standards:
  message_broker: Amazon SQS / Azure Service Bus

  event_format: CloudEvents v1.0

  event_schema:
    type: "scm.traceability.lot-recorded"
    source: "/suntory/scm/traceability"
    subject: "lot/LOT-2025-001234"
    data:
      lotNumber: "LOT-2025-001234"
      productCode: "PRD-001"
      recordedAt: "2025-01-15T10:30:00Z"

  delivery_guarantees:
    at_least_once: true
    ordering: FIFO（同一ロット内）

  retry_policy:
    max_retries: 3
    backoff: exponential
    dead_letter_queue: true
```

### 2.3 バッチ処理

**使用ケース**:
- 需要予測モデル実行（日次）
- CO2排出量計算（日次）
- EDI連携（複数回/日）
- 環境報告作成（月次/四半期）

**標準仕様**:

```yaml
Batch_Processing_Standards:
  scheduling: cron / 業務カレンダー連動

  patterns:
    daily_forecast:
      trigger: "0 2 * * *"  # 毎日AM2:00
      source: Order, External(POS)
      target: DemandPlanningContext
      duration_sla: 2時間以内

    daily_co2:
      trigger: "0 4 * * *"  # 毎日AM4:00
      source: TransportPlanning, Warehouse
      target: EnvironmentalReportingContext
      duration_sla: 1時間以内

    edi_processing:
      trigger: "0 */4 * * *"  # 4時間ごと
      source: External(EDI)
      target: OrderContext
      duration_sla: 30分以内

  monitoring:
    job_status: SUCCESS / FAILED / RUNNING
    metrics: 処理件数、エラー件数、処理時間
    alerting: 失敗時にSlack/メール通知
```

---

## 3. レジリエンスパターン

### 3.1 Circuit Breaker

**適用箇所**:
- traevo API連携
- 日立ブロックチェーン連携
- EDI連携

**設定**:

```yaml
Circuit_Breaker:
  traevo:
    failure_threshold: 5
    success_threshold: 3
    timeout: 30秒
    half_open_requests: 1
    fallback: 前回位置情報をキャッシュから返却

  hitachi_blockchain:
    failure_threshold: 3
    success_threshold: 2
    timeout: 60秒
    half_open_requests: 1
    fallback: ローカルDBに一時記録、後でリトライ

  edi:
    failure_threshold: 3
    success_threshold: 2
    timeout: 120秒
    fallback: ファイルキューに退避
```

### 3.2 Retry with Exponential Backoff

**適用箇所**:
- 全ての外部API呼び出し
- データベース接続
- メッセージ送信

**設定**:

```yaml
Retry_Policy:
  default:
    max_retries: 3
    initial_delay: 1秒
    max_delay: 30秒
    multiplier: 2
    jitter: 0.1

  blockchain:
    max_retries: 5
    initial_delay: 2秒
    max_delay: 60秒
    multiplier: 2
```

### 3.3 Timeout

**設定**:

```yaml
Timeout_Policy:
  http_client:
    connect_timeout: 5秒
    read_timeout: 30秒

  database:
    connection_timeout: 10秒
    query_timeout: 60秒

  external_api:
    traevo: 30秒
    hitachi: 60秒
    edi: 120秒
```

### 3.4 Bulkhead（リソース分離）

**適用箇所**:
- コネクションプール分離
- スレッドプール分離

**設定**:

```yaml
Bulkhead:
  connection_pools:
    primary_db:
      max_connections: 50
      min_connections: 10

    traevo_api:
      max_connections: 10
      min_connections: 2

    hitachi_api:
      max_connections: 5
      min_connections: 1

  thread_pools:
    batch_processing:
      core_size: 10
      max_size: 20

    event_processing:
      core_size: 5
      max_size: 10
```

---

## 4. データ整合性パターン

### 4.1 Saga Pattern（Choreography）

**適用箇所**:
- 出荷処理フロー（Order → Warehouse → Transport → Quality）

**設計**:

```yaml
Shipment_Saga:
  participants:
    - OrderContext
    - WarehouseContext
    - TransportPlanningContext
    - FoodSafetyContext
    - TraceabilityContext

  happy_path:
    1. Order: 出荷指示作成 → ShipmentOrderCreated
    2. Warehouse: 在庫引当 → InventoryAllocated
    3. Transport: 配車割当 → DeliveryAssigned
    4. FoodSafety: 品質検査 → QualityApproved
    5. Traceability: ロット記録 → LotTraceRecorded
    6. Warehouse: 出庫実行 → ShipmentCompleted

  compensation:
    ShipmentCompleted_failed:
      - LotTraceRecorded → DeleteLotTrace
      - QualityApproved → MarkAsNotShipped
      - DeliveryAssigned → CancelDelivery
      - InventoryAllocated → ReleaseInventory
      - ShipmentOrderCreated → CancelShipmentOrder

  implementation: Choreography（イベント駆動）

  rationale: |
    複数BCにまたがる長いトランザクションをSagaで管理。
    Choreographyを採用し、各BCが独立してイベントを処理。
    失敗時は補償トランザクションで巻き戻し。
```

### 4.2 Eventual Consistency

**適用領域**:
- 在庫数量（Warehouse ↔ DemandPlanning）
- CO2排出量（Transport → EnvironmentalReporting）
- 水収支データ（WaterSustainability → EnvironmentalReporting）

**整合性ウィンドウ**:

```yaml
Consistency_Windows:
  inventory:
    source: WarehouseContext
    consumer: DemandPlanningContext
    window: 最大15分
    sync_method: 定期ポーリング + 変更イベント

  co2_emissions:
    source: TransportPlanningContext
    consumer: EnvironmentalReportingContext
    window: 最大24時間（日次バッチ）
    sync_method: 日次バッチ

  water_balance:
    source: WaterSustainabilityContext
    consumer: EnvironmentalReportingContext
    window: 最大1ヶ月（月次報告サイクル）
    sync_method: 月次バッチ
```

---

## 5. API Gateway 設計

### 5.1 構成

```yaml
API_Gateway:
  technology: AWS API Gateway / Azure API Management

  routes:
    /api/v1/demand-planning/*:
      target: demand-planning-service
      auth: JWT

    /api/v1/transport/*:
      target: transport-planning-service
      auth: JWT

    /api/v1/warehouse/*:
      target: warehouse-service
      auth: JWT

    /api/v1/quality/*:
      target: food-safety-service
      auth: JWT

    /api/v1/traceability/*:
      target: traceability-service
      auth: JWT

    /api/v1/sustainability/*:
      target: water-sustainability-service
      auth: JWT

    /api/v1/environment/*:
      target: environmental-reporting-service
      auth: JWT

    /api/v1/orders/*:
      target: order-service
      auth: JWT

    /external/edi/*:
      target: integration-hub-service
      auth: API Key + IP Whitelist

  cross_cutting:
    rate_limiting: 有効
    request_logging: 有効
    cors: 許可（管理画面ドメイン）
    ssl_termination: 有効
```

### 5.2 認証・認可

```yaml
Authentication:
  internal:
    method: JWT Bearer Token
    issuer: Suntory Identity Provider
    token_lifetime: 1時間
    refresh_token: 有効（24時間）

  external_partners:
    traevo:
      method: OAuth 2.0 Client Credentials
    hitachi:
      method: API Key + Certificate
    daio:
      method: OAuth 2.0 Client Credentials

  edi:
    method: API Key + IP Whitelist
    additional: 電子署名（オプション）

Authorization:
  model: RBAC（Role-Based Access Control）

  roles:
    scm_admin: 全BC読み書き
    planner: DemandPlanning, TransportPlanning 読み書き
    warehouse_operator: Warehouse 読み書き
    quality_manager: FoodSafety, Traceability 読み書き
    sustainability_manager: WaterSustainability, EnvironmentalReporting 読み書き
    order_processor: Order 読み書き
    viewer: 全BC読み取りのみ
```

---

## 6. 設計ストーリー

### 6.1 同期通信を基本とした理由

**選択**: REST API による同期通信をデフォルトに

**理由**:
1. **トレーサビリティ**: SCM業務は「いつ・誰が・何を」の追跡が重要
2. **デバッグ容易性**: 問題発生時に呼び出しチェーンが明確
3. **運用シンプル**: メッセージブローカーの運用負荷を回避
4. **業務特性**: 計画→実行の明確なフローがある

**非同期を使う条件**:
- 外部システムの応答が不確定（ブロックチェーン等）
- 失敗時の自動リトライが必要
- 処理時間が長い（バッチ処理）

### 6.2 Integration Hub を採用した理由

**選択**: レガシー・外部システムとの統合にHubパターン

**理由**:
1. **複雑性隔離**: SAP、WMS、EDIの複雑性をHub内に閉じ込め
2. **変更容易性**: 外部システム変更時にHubのみ修正
3. **プロトコル変換**: RFC/BAPI、EDI、REST、Blockchainの統一的な扱い
4. **運用一元化**: 外部連携の監視・ログを一箇所に集約

**Hubを通さない例外**:
- BC間の直接通信（内部）
- フロントエンド→API Gateway→各サービス

### 6.3 Saga をChoreographyで実装した理由

**選択**: Sagaパターン（Orchestration ではなく Choreography）

**理由**:
1. **疎結合維持**: オーケストレータがSPOFにならない
2. **BC独立性**: 各BCが自律的にイベントを処理
3. **スケーラビリティ**: 中央調整なしでスケール可能
4. **障害分離**: 1つのBCの障害が全体に波及しにくい

**トレードオフ**:
- フロー全体の可視性が低下
- デバッグ時に複数サービスのログを追跡必要
→ 分散トレーシング（OpenTelemetry）で対応

---

**作成**: Parasol V5 Phase 4
