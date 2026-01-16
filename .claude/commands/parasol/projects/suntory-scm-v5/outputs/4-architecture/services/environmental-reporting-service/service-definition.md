# Environmental Reporting Service（環境報告サービス）

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5.1
**作成日**: 2025-01-15
**ステータス**: 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | Environmental Reporting Service |
| **日本語名** | 環境報告サービス |
| **ドメインタイプ** | Generic |
| **所有チーム** | サステナビリティ推進部 / 報告チーム |
| **リポジトリ** | `suntory/scm-environmental-reporting` |

---

## 含まれるBounded Contexts

- **EnvironmentalReportingContext**
  - CL3参照: `outputs/3-capabilities/cl3-business-operations/environmental-reporting-operations.md`
  - 担当CL3: CL3-701〜CL3-705（5オペレーション）

**統合理由**:
CO2排出量計算、ESG指標管理、環境報告書作成は
規制対応とステークホルダーコミュニケーションのための標準的な機能。
GHGプロトコル、TCFD、CDPなどの国際基準に準拠したレポーティングを提供する。

---

## 責務

### ミッション
SCMデータを環境指標に変換し、規制当局・投資家・消費者に対する
透明性の高い環境報告を実現する。

### 主要責務
1. **CO2排出量計算**: Scope 1/2/3の排出量算出
2. **ESG指標管理**: 環境・社会・ガバナンス指標の統合管理
3. **報告書生成**: TCFD、CDP、統合報告書向けデータ提供
4. **目標追跡**: SBTi等の環境目標に対する進捗管理

---

## ドメインモデル

### Aggregates

```yaml
CarbonEmission:
  説明: CO2排出量の集約ルート
  Root Entity: CarbonEmission
  Entities:
    - EmissionSource
    - EmissionFactor
  Value Objects:
    - CO2Volume
    - EmissionScope
    - CalculationMethod

ESGMetric:
  説明: ESG指標の集約ルート
  Root Entity: ESGMetric
  Entities:
    - MetricValue
    - TargetProgress
  Value Objects:
    - MetricType
    - ReportingPeriod
    - ComplianceStatus

EnvironmentalReport:
  説明: 環境報告書の集約ルート
  Root Entity: EnvironmentalReport
  Entities:
    - ReportSection
    - DataSource
  Value Objects:
    - ReportFormat
    - ReportingStandard
    - PublicationStatus
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/environmental-reporting

Endpoints:
  # CO2排出量
  GET /co2-emissions: CO2排出量サマリー
  GET /co2-emissions/{scope}/{period}: スコープ・期間別排出量
  POST /co2-emissions/calculate: CO2排出量計算実行
  GET /co2-emissions/breakdown: 排出源別内訳

  # ESG指標
  GET /esg-metrics: ESG指標一覧
  GET /esg-metrics/{category}: カテゴリ別指標
  PUT /esg-metrics/{id}: ESG指標更新
  GET /esg-metrics/targets: 目標進捗一覧

  # 報告書
  GET /reports: 報告書一覧
  GET /reports/{id}: 報告書取得
  POST /reports/generate: 報告書生成
  GET /reports/{id}/export: 報告書エクスポート（PDF/Excel）

  # ダッシュボード
  GET /dashboard: 環境ダッシュボード
  GET /dashboard/trends: トレンド分析
```

---

## イベント

### Published Events

```yaml
CO2EmissionsCalculated: CO2排出量が計算された
ESGMetricUpdated: ESG指標が更新された
EnvironmentalReportGenerated: 環境報告書が生成された
TargetProgressUpdated: 目標進捗が更新された
```

### Subscribed Events

```yaml
DeliveryCompleted: (from TransportPlanningContext)
  → 輸送CO2排出量の計算トリガー

WaterBalanceUpdated: (from WaterSustainabilityContext)
  → 水資源指標の更新

InventoryUpdated: (from WarehouseContext)
  → 倉庫エネルギー消費データの取り込み
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: environmental_reporting
  Tables:
    - carbon_emissions
    - emission_sources
    - emission_factors
    - esg_metrics
    - environmental_reports
    - target_progress

Analytics Store:
  Type: BigQuery / Redshift
  Purpose: 長期トレンド分析、ベンチマーキング

Document Store:
  Type: S3 / Azure Blob Storage
  Purpose: 生成された報告書の保存
  Format: PDF, Excel, JSON
```

---

## 外部連携

### 排出係数データベース連携

```yaml
Integration:
  Type: REST API / File
  Direction: Inbound
  Sources:
    - 環境省排出係数データベース
    - GHGプロトコル排出係数

Sync Frequency: 年次（排出係数更新時）
```

### CDP/TCFD報告連携

```yaml
Integration:
  Type: File Export
  Direction: Outbound
  Formats:
    - CDP質問票形式
    - TCFD開示フォーマット
    - 統合報告書用データ

Sync Frequency: 年次（報告期限に合わせて）
```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| Transport Planning Service | 輸送距離、CO2排出量 |
| Warehouse Service | 倉庫エネルギー消費 |
| Water Sustainability Service | 水収支データ |
| Traceability Service | サプライチェーンCO2 |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| (外部) | CDP、TCFD、統合報告書 |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 低
  Replicas: 2
  Note: バッチ処理中心、報告期限時のみ負荷増

Availability:
  SLA: 99.0%
  Note: 内部レポート用途、即時性要件低

Performance:
  ダッシュボードAPI: 2秒以内
  CO2計算: 1分以内
  報告書生成: 5分以内

Data Retention:
  排出量データ: 10年（長期トレンド・監査対応）
  報告書: 永久保存
```

---

## バッチ処理

```yaml
Daily_CO2:
  Schedule: "0 4 * * *"  # 毎日AM4:00
  処理内容:
    - 前日の輸送CO2計算
    - 倉庫エネルギーCO2計算
  SLA: 1時間以内

Monthly_ESG:
  Schedule: "0 6 1 * *"  # 毎月1日AM6:00
  処理内容:
    - 月次ESG指標集計
    - 目標進捗更新
    - ダッシュボードデータ更新

Quarterly_Report:
  Schedule: "0 0 1 1,4,7,10 *"  # 四半期初日
  処理内容:
    - 四半期環境報告書生成
    - CDP/TCFD用データ準備
```

---

## 計算ロジック

### CO2排出量計算（GHGプロトコル準拠）

```yaml
Scope1:
  定義: 直接排出（自社所有の燃焼等）
  計算: 活動量 × 排出係数
  データ源: 工場エネルギー消費

Scope2:
  定義: 間接排出（購入電力等）
  計算: 電力使用量 × 電力排出係数
  データ源: 電力使用量データ

Scope3:
  定義: その他間接排出
  カテゴリ:
    - Category 4: 輸送（Transport Planning連携）
    - Category 1: 購入品（Traceability連携）
  計算: 輸送距離 × 車種別排出係数
```

---

## 設計ストーリー

### なぜGenericドメインか
環境報告は業界標準（GHGプロトコル、TCFD、CDP）に準拠した
汎用的な機能であり、差別化要因にはならない。
正確性と透明性が重要だが、独自性は求められない。
将来的にはSaaS化や外部サービス活用も検討可能。

### なぜ独立サービスか
環境報告は複数のSCMサービスからデータを集約する必要があり、
独立したサービスとすることで各サービスとの疎結合を維持。
報告期限に合わせた独自のバッチスケジュールを持つ。

---

**作成**: Parasol V5 Phase 4
