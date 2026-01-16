# Water Sustainability Service（水資源持続可能性サービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Water Sustainability Service |
| **日本語名** | 水資源持続可能性サービス |
| **ドメインタイプ** | Supporting |
| **所有チーム** | サステナビリティ推進部 / 水資源チーム |
| **リポジトリ** | `suntory/scm-water-sustainability` |

---

## 含まれるBounded Contexts

- **WaterSustainabilityContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/water-sustainability-operations.md`
  - 担当CL3: CL3-601〜CL3-604（4オペレーション）

**統合理由**:
水収支管理、水源涵養、水質管理はサントリーのサステナビリティ戦略の核心であり、
「水と生きる」企業理念を具現化する基盤機能。
環境報告との連携を通じてESG開示に貢献する。

---

## 責務

### ミッション
サントリーグループ全体の水使用量と水源涵養量のバランスを可視化し、
「水のプラスマイナスゼロ」目標の達成を支援する。

### 主要責務
1. **水収支管理**: 取水量・使用量・還元量のバランス計算
2. **水源涵養記録**: 天然水の森活動による涵養量の記録
3. **水質管理**: 工場排水の水質モニタリング
4. **目標追跡**: サステナビリティ目標に対する進捗管理

---

## ドメインモデル

### Aggregates

```yaml
WaterBalance:
  説明: 水収支の集約ルート
  Root Entity: WaterBalance
  Entities:
    - WaterIntake
    - WaterUsage
    - WaterReturn
  Value Objects:
    - WaterVolume
    - MeasurementPeriod
    - FacilityLocation

WaterSourceConservation:
  説明: 水源涵養の集約ルート
  Root Entity: WaterSourceConservation
  Entities:
    - ForestArea
    - ConservationActivity
  Value Objects:
    - ConservationVolume
    - ForestLocation
    - ActivityType

WaterQuality:
  説明: 水質管理の集約ルート
  Root Entity: WaterQuality
  Entities:
    - QualityMeasurement
    - DischargeRecord
  Value Objects:
    - QualityMetric
    - ComplianceStatus
    - MeasurementLocation
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/water-sustainability

Endpoints:
  # 水収支
  GET /water-balance: 水収支サマリー取得
  GET /water-balance/{facility}/{period}: 施設・期間別水収支
  POST /water-intake: 取水量記録
  POST /water-usage: 使用量記録
  POST /water-return: 還元量記録

  # 水源涵養
  GET /conservation: 涵養活動一覧
  GET /conservation/{forest}: 森林別涵養量
  POST /conservation: 涵養活動記録
  GET /conservation/total: 総涵養量取得

  # 水質
  GET /water-quality: 水質測定一覧
  GET /water-quality/{facility}: 施設別水質
  POST /water-quality: 水質測定記録

  # ダッシュボード
  GET /dashboard: 水サステナビリティダッシュボード
  GET /targets/progress: 目標進捗取得
```

---

## イベント

### Published Events

```yaml
WaterBalanceUpdated: 水収支が更新された
ConservationActivityRecorded: 涵養活動が記録された
WaterQualityMeasured: 水質が測定された
SustainabilityTargetProgress: 目標進捗が更新された
```

### Subscribed Events

```yaml
ProductionCompleted: (from DemandPlanningContext)
  → 生産に伴う水使用量の更新トリガー

FacilityOperationData: (from IntegrationHub)
  → 工場からの水使用データ取り込み
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: water_sustainability
  Tables:
    - water_balances
    - water_intakes
    - water_usages
    - water_returns
    - conservation_activities
    - water_quality_measurements

Time-Series Store:
  Type: TimescaleDB
  Purpose: 水使用量・水質の時系列データ
  Retention: 5年

Analytics Store:
  Type: BigQuery / Redshift
  Purpose: 長期トレンド分析、レポート生成
```

---

## 外部連携

### 工場センサーデータ連携

```yaml
Integration:
  Type: IoT Data Pipeline
  Direction: Inbound
  Protocol: MQTT → Integration Hub → REST

Data Types:
  - 取水量（流量計）
  - 排水量（流量計）
  - 水質センサー（pH、BOD、SS等）

Sync Frequency: リアルタイム（1分間隔）
```

### 天然水の森データ連携

```yaml
Integration:
  Type: Manual + Batch
  Direction: Inbound
  Protocol: File Upload / API

Data Types:
  - 森林面積
  - 涵養量推定値
  - 活動記録

Sync Frequency: 月次
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Integration Hub | 工場センサーデータ、森林データ |
| Demand Planning Service | 生産計画（水使用量予測用） |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| Environmental Reporting Service | 水収支データ、涵養量データ |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 低
  Replicas: 2
  Note: バッチ処理中心、リアルタイム要件低

Availability:
  SLA: 99.5%
  Note: レポート生成に影響するが即時性は低い

Performance:
  ダッシュボードAPI: 1秒以内
  水収支計算: 5秒以内
  レポート生成: 30秒以内

Data Retention:
  詳細データ: 5年
  集計データ: 10年（長期トレンド分析用）
```

---

## バッチ処理

```yaml
Daily_Balance:
  Schedule: "0 6 * * *"  # 毎日AM6:00
  処理内容:
    - 前日の水収支集計
    - 異常値検出とアラート
  SLA: 30分以内

Monthly_Report:
  Schedule: "0 8 1 * *"  # 毎月1日AM8:00
  処理内容:
    - 月次水収支レポート生成
    - 目標進捗更新
    - Environmental Reportingへのデータ連携
```

---

## 設計ストーリー

### なぜSupportingドメインか
水資源管理はサントリーの企業理念「水と生きる」の根幹であり、
ESG戦略上も重要な領域。しかし、直接的な収益や競争優位には繋がらず、
SCMのコア機能（需要予測、輸送計画）とは異なる支援的役割。
独自性はあるが、差別化の主戦場ではない。

### なぜ独立サービスか
水資源データは環境報告に必須であり、
専門チーム（サステナビリティ推進部）が管理する。
独立したサービスとすることで、
SCM本体の変更から隔離しつつ、明確なAPIで連携できる。

---

**作成**: Parasol V5 Phase 4
