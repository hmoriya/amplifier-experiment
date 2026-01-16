# Traceability Service（トレーサビリティサービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Traceability Service |
| **日本語名** | トレーサビリティサービス |
| **ドメインタイプ** | VCI (Value-Critical Infrastructure) |
| **所有チーム** | 品質保証本部 / トレーサビリティチーム |
| **リポジトリ** | `suntory/scm-traceability` |

---

## 含まれるBounded Contexts

- **TraceabilityContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/traceability-operations.md`
  - 担当CL3: CL3-501〜CL3-505（5オペレーション）

**統合理由**:
ロット追跡、原材料追跡、製品追跡は一体的なトレーサビリティ機能であり、
日立協創システムとのブロックチェーン連携を通じて改ざん防止と証跡管理を実現する。
リコール時の影響範囲特定に不可欠な基盤機能。

---

## 責務

### ミッション
製品の原材料から消費者までの全工程を追跡可能にし、リコール時の迅速な影響範囲特定と食品安全の証明を提供する。

### 主要責務
1. **ロット追跡**: 製品ロットの移動・変換履歴の記録
2. **原材料追跡**: 原材料の調達元から製品への紐付け
3. **製品追跡**: 完成品の流通経路追跡
4. **リコール対応**: 影響範囲の迅速な特定と通知

---

## ドメインモデル

### Aggregates

```yaml
LotTrace:
  説明: ロット追跡の集約ルート
  Root Entity: LotTrace
  Entities:
    - TraceEvent
    - LocationRecord
  Value Objects:
    - LotNumber
    - TraceTimestamp
    - MovementType

MaterialTrace:
  説明: 原材料追跡の集約ルート
  Root Entity: MaterialTrace
  Entities:
    - SupplierRecord
    - MaterialLot
  Value Objects:
    - MaterialCode
    - SupplierInfo
    - CertificationStatus

ProductTrace:
  説明: 製品追跡の集約ルート
  Root Entity: ProductTrace
  Entities:
    - DistributionRecord
    - RetailLocation
  Value Objects:
    - ProductCode
    - ShipmentInfo
    - RetailInfo
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/traceability

Endpoints:
  # ロット追跡
  GET /lot-traces: ロット追跡一覧
  GET /lot-traces/{lotNumber}: ロット別追跡履歴
  POST /lot-traces: ロット追跡記録
  GET /lot-traces/{lotNumber}/timeline: ロットタイムライン取得

  # 原材料追跡
  GET /material-traces: 原材料追跡一覧
  GET /material-traces/{materialCode}: 原材料別追跡
  POST /material-traces: 原材料追跡記録

  # 製品追跡
  GET /product-traces/{productCode}: 製品追跡
  GET /product-traces/{lotNumber}/distribution: 流通経路取得

  # リコール対応
  GET /recall-scope/{lotNumber}: リコール影響範囲取得
  POST /recall-alerts: リコールアラート発行
```

---

## イベント

### Published Events

```yaml
LotTraceRecorded: ロット追跡が記録された
MaterialTraceRecorded: 原材料追跡が記録された
ProductDistributionTracked: 製品流通が追跡された
RecallScopeIdentified: リコール影響範囲が特定された
```

### Subscribed Events

```yaml
LotRegistered: (from WarehouseContext)
  → 新規ロットの追跡開始

ShipmentCompleted: (from WarehouseContext)
  → 出荷情報の追跡記録

QualityInspectionCompleted: (from FoodSafetyContext)
  → 品質検査結果の追跡記録
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: traceability
  Tables:
    - lot_traces
    - trace_events
    - material_traces
    - product_traces
    - recall_records

Blockchain Integration:
  Type: Hyperledger Fabric (日立協創システム経由)
  Purpose: 改ざん防止、第三者証明
  Sync: イベント駆動（リアルタイム）

Graph Database:
  Type: Neo4j (オプション)
  Purpose: 複雑な追跡関係のクエリ最適化
```

---

## Partnership: FoodSafety連携

```yaml
Partnership:
  Pattern: Partnership（双方向協力）
  Partner: FoodSafetyContext

Bidirectional_API:
  Traceability_to_FoodSafety:
    - GET /lot-trace/{lotNumber}: ロット追跡情報提供
    - POST /recall-candidates: リコール候補通知

  FoodSafety_to_Traceability:
    - POST /lot-quality-records: 品質検査結果の記録

Shared_Events:
  - LotTraceRecorded
  - QualityInspectionCompleted
  - TemperatureAnomalyDetected
```

---

## 外部連携

### 日立協創システム連携

```yaml
Integration:
  Type: Blockchain API (ACL経由)
  Direction: Bidirectional
  Protocol: REST + Event-Driven

Outbound:
  - ロット追跡記録のブロックチェーン登録
  - 品質検査結果のハッシュ登録

Inbound:
  - ブロックチェーン登録完了通知
  - 改ざん検知アラート

ACL Location: Integration Hub Service
Data Mapping:
  internal_LotTrace → hitachi_BlockRecord
  internal_QualityRecord → hitachi_QualityHash
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Warehouse Service | ロット情報、移動履歴 |
| Food Safety Service | 品質検査結果 |
| Integration Hub | 日立協創システム連携 |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Food Safety Service | ロット追跡情報（リコール時） |
| Environmental Reporting Service | サプライチェーンCO2データ |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 高
  Replicas: 3-6
  Note: リコール時のバースト対応

Availability:
  SLA: 99.9%
  Note: リコール対応は時間との勝負

Performance:
  追跡照会API: 300ms以内
  リコール影響範囲算出: 30秒以内
  ブロックチェーン登録: 5秒以内

Data Integrity:
  ブロックチェーン: 改ざん防止
  監査ログ: 全操作記録
  データ保持: 10年（リコール対応期間）
```

---

## Saga参加

```yaml
Shipment_Saga:
  役割: ロット追跡記録を担当

  参加ステップ:
    Step5: LotTraceRecorded（ロット追跡記録完了）

  補償トランザクション:
    LotTraceRecorded_compensation: DeleteLotTrace（追跡記録削除）
```

---

## 設計ストーリー

### なぜVCIドメインか
トレーサビリティは「失敗が許されない」法規制対応領域。
食品事故時のリコール対応は企業の信頼と法的責任に直結する。
差別化要因ではないが、確実な記録と迅速な追跡が必須のため内製で厳密に管理する。

### なぜPartnershipパターンか
品質検査結果はFoodSafetyから受け取り、
リコール時はFoodSafetyに影響範囲を提供する。
双方向の協力関係があり、どちらが上流・下流とも言えない対等な関係。

### なぜブロックチェーン連携か
日立協創システムとの連携により、
第三者による改ざん検知と証跡の信頼性を確保。
規制当局や消費者に対する証明能力を強化する。

---

**作成**: Parasol V5 Phase 4
