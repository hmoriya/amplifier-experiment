# Food Safety Service（食品安全サービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Food Safety Service |
| **日本語名** | 食品安全サービス |
| **ドメインタイプ** | VCI (Value-Critical Infrastructure) |
| **所有チーム** | 品質保証本部 / 食品安全チーム |
| **リポジトリ** | `suntory/scm-food-safety` |

---

## 含まれるBounded Contexts

- **FoodSafetyContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/food-safety-operations.md`
  - 担当CL3: CL3-401〜CL3-405（5オペレーション）

**統合理由**:
HACCP管理、品質検査、温度監視は食品安全の三本柱であり、
規制対応の観点から一体的に管理し、監査証跡を確保する必要がある。
独立した品質保証チームが担当し、他事業部門から独立して運営する。

---

## 責務

### ミッション
食品安全法規制（HACCP義務化）を遵守し、製品の安全性を確保することで、消費者の信頼を維持する。

### 主要責務
1. **HACCP管理**: 重要管理点（CCP）の監視と逸脱対応
2. **品質検査**: 入荷・出荷時の品質検査と記録
3. **温度監視**: コールドチェーン全体の温度追跡
4. **異常対応**: 品質異常検知時の即時アラートとリコール準備

---

## ドメインモデル

### Aggregates

```yaml
HACCPRecord:
  説明: HACCP記録の集約ルート
  Root Entity: HACCPRecord
  Entities:
    - CriticalControlPoint
    - MonitoringResult
    - CorrectiveAction
  Value Objects:
    - CriticalLimit
    - DeviationReport
    - VerificationResult

QualityInspection:
  説明: 品質検査の集約ルート
  Root Entity: QualityInspection
  Entities:
    - InspectionItem
    - TestResult
  Value Objects:
    - InspectionCriteria
    - QualityGrade
    - InspectionStatus

TemperatureLog:
  説明: 温度記録の集約ルート
  Root Entity: TemperatureLog
  Entities:
    - TemperatureReading
    - AlertRecord
  Value Objects:
    - TemperatureRange
    - SensorLocation
    - AlertThreshold
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/quality

Endpoints:
  # HACCP管理
  GET /haccp-records: HACCP記録一覧
  GET /haccp-records/{lot}: ロット別HACCP記録
  POST /haccp-records: HACCP記録作成
  POST /haccp-records/{id}/deviation: 逸脱報告

  # 品質検査
  GET /inspections: 品質検査一覧
  GET /inspections/{lot}: ロット別検査結果
  POST /inspections: 品質検査実施
  PUT /inspections/{id}/approve: 検査結果承認

  # 温度監視
  GET /temperature-logs: 温度記録一覧
  GET /temperature-logs/{lot}: ロット別温度履歴
  POST /temperature-alerts: 温度異常アラート

  # リコール準備
  GET /recall-candidates/{lot}: リコール対象候補取得
  POST /recall-initiate: リコール開始（Traceability連携）
```

---

## イベント

### Published Events

```yaml
QualityInspectionCompleted: 品質検査が完了した
QualityApproved: 品質が承認された
QualityRejected: 品質が不合格となった
TemperatureAnomalyDetected: 温度異常が検知された
HACCPDeviationReported: HACCP逸脱が報告された
RecallCandidatesIdentified: リコール候補が特定された
```

### Subscribed Events

```yaml
LotRegistered: (from WarehouseContext)
  → 新規ロットのHACCP記録初期化

ShipmentCompleted: (from WarehouseContext)
  → 出荷前最終品質確認トリガー

LotTraceRecorded: (from TraceabilityContext)
  → ロット追跡情報との整合性確認
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: food_safety
  Tables:
    - haccp_records
    - critical_control_points
    - quality_inspections
    - temperature_logs
    - deviation_reports

Compliance Archive:
  Type: S3 / Azure Blob Storage
  Purpose: 規制対応用長期保存（7年以上）
  Format: PDF/A形式（改ざん防止）

Time-Series Store:
  Type: TimescaleDB / InfluxDB
  Purpose: 温度データの高頻度記録
```

---

## Partnership: Traceability連携

```yaml
Partnership:
  Pattern: Partnership（双方向協力）
  Partner: TraceabilityContext

Bidirectional_API:
  FoodSafety_to_Traceability:
    - POST /lot-quality-records: 品質検査結果の記録

  Traceability_to_FoodSafety:
    - GET /lot-trace/{lotNumber}: ロット追跡情報取得
    - POST /recall-candidates: リコール候補通知

Shared_Events:
  - QualityInspectionCompleted
  - LotTraceRecorded
  - TemperatureAnomalyDetected
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Warehouse Service | ロット情報、保管条件 |
| Traceability Service | ロット追跡情報（リコール時） |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Traceability Service | 品質検査結果 |
| Order Service | 品質承認ステータス |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 中
  Replicas: 2-4
  Note: 検査業務は業務時間帯に集中

Availability:
  SLA: 99.9%
  Note: 品質問題の見逃しは重大リスク

Performance:
  品質照会API: 200ms以内
  温度アラート: リアルタイム（1分以内）
  検査記録保存: 500ms以内

Compliance:
  データ保持: 7年（食品衛生法対応）
  監査ログ: 全操作を記録
  改ざん防止: 検査記録は追記のみ（削除不可）
```

---

## 規制対応

```yaml
HACCP:
  適用規制: 食品衛生法（2021年6月完全義務化）
  対応内容:
    - 7原則12手順に基づく管理計画
    - CCPの継続的モニタリング
    - 逸脱時の是正措置記録
    - 検証手順の文書化

Food_Labeling:
  適用規制: 食品表示法
  対応内容:
    - アレルゲン情報の管理
    - 原産地情報の追跡
    - 賞味期限管理

Audit_Readiness:
  監査種別:
    - 内部監査（四半期）
    - 外部監査（年次）
    - 行政監査（不定期）
  対応:
    - 全記録の即時出力機能
    - 監査証跡の完全性保証
```

---

## Saga参加

```yaml
Shipment_Saga:
  役割: 品質検査・承認を担当

  参加ステップ:
    Step4: QualityApproved（品質承認完了）

  補償トランザクション:
    QualityApproved_compensation: MarkAsNotShipped（未出荷マーク）
```

---

## 設計ストーリー

### なぜVCIドメインか
食品安全は「失敗が許されない」法規制対応領域。
HACCP違反は行政処分、リコールは巨額の損失と信頼失墜を招く。
差別化要因ではないが、コンプライアンス維持のため内製で厳密に管理する。

### なぜPartnershipパターンか
品質検査結果はTraceabilityに記録され、
リコール時はTraceabilityから影響範囲を特定する。
双方向の協力関係があり、どちらが上流・下流とも言えない対等な関係。
日立協創システムとの連携でこの関係がさらに強化される。

---

**作成**: Parasol V5 Phase 4
