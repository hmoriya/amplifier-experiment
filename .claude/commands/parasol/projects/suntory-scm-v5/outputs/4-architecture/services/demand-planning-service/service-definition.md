# Demand Planning Service（需要計画サービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Demand Planning Service |
| **日本語名** | 需要計画サービス |
| **ドメインタイプ** | Core |
| **所有チーム** | SCM戦略部 / 需要計画チーム |
| **リポジトリ** | `suntory/scm-demand-planning` |

---

## 含まれるBounded Contexts

- **DemandPlanningContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/demand-planning-operations.md`
  - 担当CL3: CL3-101〜CL3-107（7オペレーション）

**統合理由**:
需要予測、生産計画、在庫戦略は密接に連携し、同一のドメインエキスパート（需要計画担当者）が管理する。
トランザクション境界も明確で、予測→計画→在庫目標の一連のフローを単一サービスで完結できる。

---

## 責務

### ミッション
飲料・酒類の需要を正確に予測し、最適な生産・在庫計画を立案することで、欠品防止と在庫最適化を両立させる。

### 主要責務
1. **需要予測**: AI/MLモデルを活用した需要予測の実行・精度管理
2. **生産計画**: 工場別・製品別の生産計画立案
3. **在庫戦略**: 安全在庫水準の設定と在庫目標の管理
4. **S&OP連携**: Sales & Operations Planning会議への計画データ提供

---

## ドメインモデル

### Aggregates

```yaml
DemandForecast:
  説明: 需要予測の集約ルート
  Root Entity: DemandForecast
  Entities:
    - ForecastPeriod
    - ForecastRegion
    - ForecastProduct
  Value Objects:
    - ForecastAccuracy
    - ConfidenceInterval
    - SeasonalFactor

ProductionPlan:
  説明: 生産計画の集約ルート
  Root Entity: ProductionPlan
  Entities:
    - PlannedProduction
    - FactoryAssignment
  Value Objects:
    - ProductionCapacity
    - ProductionSchedule
    - MaterialRequirement

InventoryTarget:
  説明: 在庫目標の集約ルート
  Root Entity: InventoryTarget
  Entities:
    - SafetyStockLevel
    - ReorderPoint
  Value Objects:
    - StockCoverage
    - ServiceLevel
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/demand-planning

Endpoints:
  # 需要予測
  GET /demand-forecasts: 需要予測一覧取得
  GET /demand-forecasts/{region}/{period}: 地域・期間別予測取得
  POST /demand-forecasts: 需要予測実行（バッチトリガー）
  GET /demand-forecasts/{id}/accuracy: 予測精度取得

  # 生産計画
  GET /production-plans: 生産計画一覧取得
  GET /production-plans/{factory}/{date}: 工場・日付別計画取得
  POST /production-plans: 生産計画作成
  PUT /production-plans/{id}: 生産計画更新
  POST /production-plans/{id}/approve: 生産計画承認

  # 在庫目標
  GET /inventory-targets: 在庫目標一覧取得
  GET /inventory-targets/{product}: 製品別在庫目標取得
  PUT /inventory-targets/{product}: 在庫目標更新
```

---

## イベント

### Published Events

```yaml
DemandForecastCreated: 需要予測が作成された
DemandForecastUpdated: 需要予測が更新された
ProductionPlanApproved: 生産計画が承認された
InventoryTargetUpdated: 在庫目標が更新された
ForecastAccuracyCalculated: 予測精度が算出された
```

### Subscribed Events

```yaml
OrderReceived: (from OrderContext)
  → 実績データを予測モデルにフィードバック

InventoryUpdated: (from WarehouseContext)
  → 在庫水準を確認し、在庫目標を調整

ExternalPOSDataReceived: (from IntegrationHub)
  → POSデータを需要予測に反映
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: demand_planning
  Tables:
    - demand_forecasts
    - forecast_periods
    - production_plans
    - inventory_targets
    - forecast_accuracy_logs

Analytics Store:
  Type: BigQuery / Redshift
  Purpose: 予測モデル学習用データウェアハウス

Cache:
  Type: Redis
  Purpose: 頻繁にアクセスされる予測データのキャッシュ
  TTL: 15分
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Integration Hub | 外部POSデータ、市場データの取得 |
| Order Service | 受注実績データの取得 |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Transport Planning Service | 需要予測・生産計画データ |
| Warehouse Service | 在庫目標データ |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 中
  Replicas: 2-4
  Note: バッチ処理時にスケールアウト

Availability:
  SLA: 99.5%
  Note: バッチ処理は夜間実行のため日中の可用性重視

Performance:
  予測API応答: 500ms以内
  バッチ処理: 2時間以内（日次）

Storage:
  予測データ保持: 3年
  計画データ保持: 1年
```

---

## バッチ処理

```yaml
Daily_Forecast:
  Schedule: "0 2 * * *"  # 毎日AM2:00
  処理内容:
    - 前日実績の取り込み
    - 予測モデル実行
    - 予測精度評価
  SLA: 2時間以内

Weekly_Planning:
  Schedule: "0 5 * * 1"  # 毎週月曜AM5:00
  処理内容:
    - 週次生産計画の自動生成
    - 承認待ちステータスで保存
```

---

## 設計ストーリー

### なぜCoreドメインか
需要予測の精度はサントリーSCM全体の効率に直結する。
予測が外れれば欠品または過剰在庫となり、両方とも大きな損失をもたらす。
他社との差別化ポイントであり、内製で継続的に改善すべき領域。

### なぜ単一サービスか
需要予測→生産計画→在庫目標は連続したプロセスであり、
分離するとデータ整合性の維持が複雑になる。
同一チームが管理することもあり、凝集度を優先した。

---

**作成**: Parasol V5 Phase 4
