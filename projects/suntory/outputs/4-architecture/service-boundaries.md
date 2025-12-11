# サービス境界定義

**作成日**: 2025-12-05
**プロジェクト**: サントリーグループ
**Phase**: 4 - Architecture Design
**入力**: Phase 3 CL3 Bounded Context定義（24 BC）

---

## 1. サービス境界設計方針

### 1.1 設計原則

```
┌─────────────────────────────────────────────────────────────────────┐
│                    サービス境界設計原則                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【チーム境界との整合】                                              │
│  ├─ 1サービス = 1チーム（Two Pizza Team）                           │
│  ├─ 明確なオーナーシップ                                            │
│  └─ 独立した意思決定が可能                                          │
│                                                                     │
│  【デプロイ独立性】                                                  │
│  ├─ 各サービスは独立してデプロイ可能                                │
│  ├─ 他サービスへの影響なくリリース                                  │
│  └─ Blue-Green/Canaryデプロイ対応                                   │
│                                                                     │
│  【データ自律性】                                                    │
│  ├─ サービスごとに独自のデータストア                                │
│  ├─ 他サービスのDBへの直接アクセス禁止                              │
│  └─ APIまたはイベント経由でのデータ共有                             │
│                                                                     │
│  【ビジネスケーパビリティ整合】                                      │
│  ├─ ビジネス機能単位でのサービス分割                                │
│  ├─ 技術的理由だけでの分割は避ける                                  │
│  └─ ドメイン境界を尊重                                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 BC統合基準

| 基準 | 統合する | 分離する |
|------|----------|----------|
| チーム | 同一チーム管理 | 異なるチーム |
| デプロイ | 同時デプロイが自然 | 独立デプロイ必要 |
| データ | 強い整合性必要 | 結果整合性で十分 |
| スケール | 同じスケール特性 | 異なるスケール要件 |

---

## 2. サービス一覧

### 2.1 サービス全体マップ

```
┌─────────────────────────────────────────────────────────────────────┐
│                    サントリーサービスアーキテクチャ                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Core Services】 8サービス                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ★ R&D Platform Service                                     │   │
│  │    (RD-WaterScience, RD-Fermentation, RD-HealthFunction,    │   │
│  │     RD-Flavor)                                               │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ★ Brand Management Service                                 │   │
│  │    (BRAND-Corporate, BRAND-Product, BRAND-Quality)          │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ★ Sustainability Service                                   │   │
│  │    (SUST-Environment, SUST-Social, SUST-Governance)         │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ★ Marketing Service × 5 (事業別インスタンス)               │   │
│  │    (MKT-Beverage, MKT-Spirits, MKT-Beer, MKT-Wine, MKT-Health)│  │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ★ Manufacturing Service × 5 (事業別インスタンス)           │   │
│  │    (MFG-Beverage, MFG-Spirits, MFG-Beer, MFG-Wine, MFG-Health)│  │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Supporting Services】 4サービス                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ◆ Supply Chain Service                                     │   │
│  │    (SCM-Procurement, SCM-Logistics)                          │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ◆ Customer Platform Service                                │   │
│  │    (CRM-CDP, CRM-Operations)                                 │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ◆ Compliance Service                                       │   │
│  │    (COMP-Policy, COMP-Regulation)                            │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ◆ R&D Application Service                                  │   │
│  │    (RD-Application per business unit)                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Platform Services】 3サービス                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ○ IT Platform Service                                      │   │
│  │    (IT-Infrastructure, IT-Application, IT-Security)         │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ○ Finance Service                                          │   │
│  │    (FIN-Accounting, FIN-Treasury)                            │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  ○ HR Service                                                │   │
│  │    (HR-Management)                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  合計: 15サービス（事業別インスタンス含め25デプロイユニット）      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Services詳細

### 3.1 R&D Platform Service

```yaml
サービス名: R&D Platform Service
サービスID: svc-rd-platform

含まれるBC:
  - RD-WaterScience (水科学)
  - RD-Fermentation (発酵技術)
  - RD-HealthFunction (健康機能)
  - RD-Flavor (フレーバー)

責務:
  - 水科学研究データ管理
  - 発酵・醸造技術のナレッジ管理
  - 健康機能成分の研究データ管理
  - フレーバー・官能評価データ管理
  - 製造への技術移転サポート

公開API:
  REST API:
    - /api/v1/water-science/*
    - /api/v1/fermentation/*
    - /api/v1/health-function/*
    - /api/v1/flavor/*
  Events (Publish):
    - ResearchCompleted
    - TechnologyTransferReady
    - QualityStandardUpdated

データストア:
  Primary: PostgreSQL (研究データ)
  Document: MongoDB (非構造化研究ドキュメント)
  Search: Elasticsearch (研究論文・レポート検索)

チーム:
  名称: R&D Platform Team
  人数: 8-12名
  責任者: R&D CTO

スケーリング要件: 低〜中
  - 読み取り: 中程度
  - 書き込み: 低
  - ピーク: なし

技術スタック:
  Runtime: Python 3.11+
  Framework: FastAPI
  理由: データサイエンス連携が容易
```

### 3.2 Brand Management Service

```yaml
サービス名: Brand Management Service
サービスID: svc-brand-mgmt

含まれるBC:
  - BRAND-Corporate (企業ブランド)
  - BRAND-Product (製品ブランド)
  - BRAND-Quality (品質基準)

責務:
  - 企業理念・VIガイドライン管理
  - 製品ブランド戦略・資産管理
  - 品質基準・監査記録管理
  - ブランド評価データ管理

公開API:
  REST API:
    - /api/v1/corporate-brand/*
    - /api/v1/product-brand/*
    - /api/v1/quality-standards/*
  Events (Publish):
    - BrandGuidelineUpdated
    - QualityStandardUpdated
    - BrandAssetCreated

データストア:
  Primary: PostgreSQL (ブランドマスタ)
  Storage: S3/GCS (ブランド資産)
  Search: Elasticsearch (ガイドライン検索)

チーム:
  名称: Brand Platform Team
  人数: 6-8名
  責任者: Brand Director

スケーリング要件: 低
  - 読み取り: 中程度
  - 書き込み: 低
  - ピーク: 新製品発売時

技術スタック:
  Runtime: Node.js 20+
  Framework: NestJS
  理由: フロントエンド連携が容易
```

### 3.3 Sustainability Service

```yaml
サービス名: Sustainability Service
サービスID: svc-sustainability

含まれるBC:
  - SUST-Environment (環境)
  - SUST-Social (社会)
  - SUST-Governance (ガバナンス)

責務:
  - 環境KPI（CO2、水、廃棄物）管理
  - 社会貢献活動・健康推進管理
  - ESGスコア・開示資料管理
  - ステークホルダー対話記録

公開API:
  REST API:
    - /api/v1/environment/*
    - /api/v1/social/*
    - /api/v1/governance/*
    - /api/v1/esg-reporting/*
  Events (Publish):
    - EnvironmentalDataUpdated
    - ESGScoreUpdated
    - SustainabilityReportPublished

データストア:
  Primary: PostgreSQL (ESGデータ)
  TimeSeries: TimescaleDB (環境計測データ)
  Document: MongoDB (レポート)

チーム:
  名称: Sustainability Tech Team
  人数: 5-7名
  責任者: Sustainability Director

スケーリング要件: 低
  - 読み取り: 低〜中（レポート期間に増加）
  - 書き込み: 中（センサーデータ）
  - ピーク: 四半期・年度末レポート時

技術スタック:
  Runtime: Python 3.11+
  Framework: FastAPI
  理由: データ分析・可視化連携
```

### 3.4 Marketing Service（事業別インスタンス）

```yaml
サービス名: Marketing Service
サービスID: svc-mkt-{business}
インスタンス:
  - svc-mkt-beverage (飲料)
  - svc-mkt-spirits (スピリッツ)
  - svc-mkt-beer (ビール)
  - svc-mkt-wine (ワイン)
  - svc-mkt-health (健康食品)

含まれるBC（各インスタンス）:
  - MKT-{Business}.広告
  - MKT-{Business}.販促
  - MKT-{Business}.チャネル

責務:
  - キャンペーン管理
  - 広告配信・効果測定
  - 販促活動管理
  - チャネル戦略・実績管理
  - マーケティング予算管理

公開API:
  REST API:
    - /api/v1/campaigns/*
    - /api/v1/advertising/*
    - /api/v1/promotions/*
    - /api/v1/channels/*
  Events (Publish):
    - CampaignLaunched
    - CampaignCompleted
    - PromotionActivated

データストア:
  Primary: PostgreSQL (キャンペーン・予算)
  Analytics: BigQuery/Redshift (マーケ分析)
  Cache: Redis (リアルタイム効果測定)

チーム（各インスタンス）:
  名称: {Business} Marketing Tech Team
  人数: 4-6名
  責任者: 事業別マーケティング部長

スケーリング要件: 中〜高
  - 読み取り: 高
  - 書き込み: 中
  - ピーク: キャンペーン開始時、年末年始

技術スタック:
  Runtime: Node.js 20+ or Python 3.11+
  Framework: NestJS or FastAPI
  理由: 事業ごとに最適な選択が可能
```

### 3.5 Manufacturing Service（事業別インスタンス）

```yaml
サービス名: Manufacturing Service
サービスID: svc-mfg-{business}
インスタンス:
  - svc-mfg-beverage (飲料)
  - svc-mfg-spirits (スピリッツ)
  - svc-mfg-beer (ビール)
  - svc-mfg-wine (ワイン)
  - svc-mfg-health (健康食品)

含まれるBC（各インスタンス）:
  - MFG-{Business}.製造
  - MFG-{Business}.品質管理
  - MFG-{Business}.保守

責務:
  - 生産計画・製造指図管理
  - 製造実績・トレーサビリティ
  - 品質検査データ管理
  - 設備管理・保守記録

公開API:
  REST API:
    - /api/v1/production-orders/*
    - /api/v1/production-records/*
    - /api/v1/quality-inspections/*
    - /api/v1/equipment/*
  Events (Publish):
    - ProductionCompleted
    - QualityInspectionCompleted
    - EquipmentMaintenanceRequired
  Events (Subscribe):
    - InventoryReservationRequested

データストア:
  Primary: PostgreSQL (製造データ)
  TimeSeries: InfluxDB/TimescaleDB (センサーデータ)
  Document: MongoDB (検査レポート)

チーム（各インスタンス）:
  名称: {Business} Manufacturing Tech Team
  人数: 6-10名
  責任者: 事業別製造部長

スケーリング要件: 中
  - 読み取り: 中
  - 書き込み: 高（IoTセンサーデータ）
  - ピーク: 繁忙期（夏季：飲料/ビール、年末：スピリッツ/ワイン）

技術スタック:
  Runtime: Go 1.21+ or Java 21+
  Framework: Gin or Spring Boot
  理由: 高スループット・低レイテンシ要件
```

---

## 4. Supporting Services詳細

### 4.1 Supply Chain Service

```yaml
サービス名: Supply Chain Service
サービスID: svc-supply-chain

含まれるBC:
  - SCM-Procurement (調達統括)
  - SCM-Logistics (物流)

責務:
  - サプライヤ管理・調達計画
  - 需要予測・在庫最適化
  - 倉庫管理・配送管理
  - サプライヤリスク管理

公開API:
  REST API:
    - /api/v1/suppliers/*
    - /api/v1/procurement/*
    - /api/v1/logistics/*
    - /api/v1/inventory/*
  Events (Publish):
    - PurchaseOrderCreated
    - ShipmentDispatched
    - InventoryUpdated
  Events (Subscribe):
    - ProductionCompleted
    - DemandForecastUpdated

データストア:
  Primary: PostgreSQL (調達・物流マスタ)
  Cache: Redis (在庫キャッシュ)
  Analytics: BigQuery (需要予測)

チーム:
  名称: Supply Chain Tech Team
  人数: 10-15名
  責任者: SCM CTO

スケーリング要件: 中〜高
  - 読み取り: 高（在庫照会）
  - 書き込み: 中
  - ピーク: 繁忙期、年度末

技術スタック:
  Runtime: Java 21+
  Framework: Spring Boot
  理由: エンタープライズSCMとの連携実績
```

### 4.2 Customer Platform Service

```yaml
サービス名: Customer Platform Service
サービスID: svc-customer-platform

含まれるBC:
  - CRM-CDP (顧客データプラットフォーム)
  - CRM-Operations (顧客運用)

責務:
  - 顧客ID統合・名寄せ
  - 顧客プロファイル管理
  - 同意管理・プライバシー
  - セグメント分析
  - キャンペーン連携

公開API:
  REST API:
    - /api/v1/customers/*
    - /api/v1/profiles/*
    - /api/v1/consents/*
    - /api/v1/segments/*
  Events (Publish):
    - CustomerProfileUpdated
    - SegmentUpdated
    - ConsentChanged
  Events (Subscribe):
    - CampaignInteraction
    - PurchaseCompleted

データストア:
  Primary: PostgreSQL (顧客マスタ)
  Graph: Neo4j (顧客関係)
  Analytics: BigQuery (顧客分析)
  Cache: Redis (プロファイルキャッシュ)

チーム:
  名称: Customer Platform Team
  人数: 8-12名
  責任者: CDP Director

スケーリング要件: 高
  - 読み取り: 非常に高
  - 書き込み: 高
  - ピーク: キャンペーン時

技術スタック:
  Runtime: Go 1.21+
  Framework: Gin
  理由: 高スループット要件
```

### 4.3 Compliance Service

```yaml
サービス名: Compliance Service
サービスID: svc-compliance

含まれるBC:
  - COMP-Policy (方針統括)
  - COMP-Regulation (規制対応)

責務:
  - コンプライアンス方針管理
  - 教育・研修記録
  - 内部通報管理
  - 規制対応（酒類、食品、環境）
  - 監査記録

公開API:
  REST API:
    - /api/v1/policies/*
    - /api/v1/training/*
    - /api/v1/whistleblowing/*
    - /api/v1/regulations/*
  Events (Publish):
    - PolicyUpdated
    - RegulationChanged
    - ComplianceAlertRaised

データストア:
  Primary: PostgreSQL (方針・規制マスタ)
  Document: MongoDB (監査レポート)
  Audit: 専用監査ログDB

チーム:
  名称: Compliance Tech Team
  人数: 4-6名
  責任者: Compliance Officer

スケーリング要件: 低
  - 読み取り: 低〜中
  - 書き込み: 低
  - ピーク: 監査時

技術スタック:
  Runtime: Java 21+
  Framework: Spring Boot
  理由: 監査ログ・セキュリティ要件
```

---

## 5. Platform Services詳細

### 5.1 IT Platform Service

```yaml
サービス名: IT Platform Service
サービスID: svc-it-platform

含まれるBC:
  - IT-Infrastructure (インフラ)
  - IT-Application (アプリケーション)
  - IT-Security (セキュリティ)

責務:
  - クラウドインフラ管理
  - 認証・認可（IdP）
  - API Gateway
  - 監視・ログ集約
  - セキュリティ監査

公開API:
  REST API:
    - /api/v1/auth/*
    - /api/v1/users/*
    - /api/v1/roles/*
  Internal:
    - 認証Token発行
    - 権限検証
    - ログ収集

データストア:
  Primary: PostgreSQL (ユーザー・権限)
  Cache: Redis (セッション)
  Log: Elasticsearch (ログ)

チーム:
  名称: Platform Engineering Team
  人数: 12-18名
  責任者: Platform CTO

スケーリング要件: 高
  - 読み取り: 非常に高（認証）
  - 書き込み: 中
  - ピーク: 業務開始時

技術スタック:
  Runtime: Go 1.21+
  Framework: 自社開発 or Kong/Keycloak
  理由: 高可用性・低レイテンシ要件

推奨マネージドサービス:
  - 認証: Auth0 or Azure AD
  - API Gateway: Kong or AWS API Gateway
  - 監視: Datadog or New Relic
```

### 5.2 Finance Service

```yaml
サービス名: Finance Service
サービスID: svc-finance

含まれるBC:
  - FIN-Accounting (会計)
  - FIN-Treasury (資金)

責務:
  - 財務会計・管理会計
  - 連結会計
  - 資金管理
  - 為替管理

公開API:
  REST API:
    - /api/v1/accounting/*
    - /api/v1/budgets/*
    - /api/v1/treasury/*
  Events (Subscribe):
    - PurchaseOrderCreated
    - SalesCompleted
    - PayrollProcessed

データストア:
  Primary: PostgreSQL (会計データ)
  DWH: BigQuery/Redshift (財務分析)

チーム:
  名称: Finance Tech Team
  人数: 6-10名
  責任者: Finance IT Director

スケーリング要件: 中
  - 読み取り: 中
  - 書き込み: 中
  - ピーク: 月末・期末

技術スタック:
  Runtime: Java 21+
  Framework: Spring Boot
  理由: ERPとの連携、トランザクション整合性

推奨連携:
  - ERP: SAP S/4HANA or Oracle
  - 連携方式: バッチ + リアルタイムAPI
```

### 5.3 HR Service

```yaml
サービス名: HR Service
サービスID: svc-hr

含まれるBC:
  - HR-Management (人事管理)

責務:
  - 人事制度管理
  - 採用・育成
  - 勤怠・労務
  - タレントマネジメント
  - 組織管理

公開API:
  REST API:
    - /api/v1/employees/*
    - /api/v1/organization/*
    - /api/v1/training/*
    - /api/v1/attendance/*
  Events (Publish):
    - EmployeeJoined
    - EmployeeLeft
    - OrganizationChanged

データストア:
  Primary: PostgreSQL (人事マスタ)
  Document: MongoDB (評価・育成記録)

チーム:
  名称: HR Tech Team
  人数: 5-8名
  責任者: HR IT Director

スケーリング要件: 低〜中
  - 読み取り: 中
  - 書き込み: 低
  - ピーク: 評価期間、入社期

技術スタック:
  Runtime: Node.js 20+ or Java 21+
  Framework: NestJS or Spring Boot
  理由: HRシステムとの連携

推奨連携:
  - HRM: Workday or SAP SuccessFactors
```

---

## 6. サービス数量サマリー

### 6.1 サービス分類別集計

| 分類 | サービス数 | デプロイユニット | 備考 |
|------|------------|-----------------|------|
| Core | 3 + 2×5 | 13 | 事業別インスタンス含む |
| Supporting | 4 | 4 | |
| Platform | 3 | 3 | |
| **合計** | **15** | **20** | |

### 6.2 BC-サービスマッピング

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BC → サービス マッピング                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  24 Bounded Contexts → 15 Services                                  │
│                                                                     │
│  【統合されたBC】                                                    │
│  ├─ R&D 4 BC → 1 Service (R&D Platform)                            │
│  ├─ BRAND 3 BC → 1 Service (Brand Management)                      │
│  ├─ SUST 3 BC → 1 Service (Sustainability)                         │
│  ├─ SCM 2 BC → 1 Service (Supply Chain)                            │
│  ├─ CRM 2 BC → 1 Service (Customer Platform)                       │
│  ├─ COMP 2 BC → 1 Service (Compliance)                             │
│  ├─ IT 3 BC → 1 Service (IT Platform)                              │
│  └─ FIN 2 BC → 1 Service (Finance)                                 │
│                                                                     │
│  【事業別インスタンス】                                              │
│  ├─ MKT 1 BC × 5事業 → 5 Instances (Marketing)                     │
│  └─ MFG 1 BC × 5事業 → 5 Instances (Manufacturing)                 │
│                                                                     │
│  【独立サービス】                                                    │
│  └─ HR 1 BC → 1 Service (HR)                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. サービス間依存関係

### 7.1 依存関係マトリクス

```
提供側 →
受領側 ↓     RD   BRAND SUST  MKT  MFG  SCM  CRM  COMP  IT   FIN  HR
───────────────────────────────────────────────────────────────────────
R&D          -     ←     →    →    →    ←    -     -    ←    -    -
BRAND        →     -     →    →    →    -    -     -    ←    -    -
SUST         ←     ←     -    -    ←    ←    -     -    ←    -    -
MKT          ←     ←     -    -    -    →    ↔    -    ←    ←    -
MFG          ←     ←     →    -    -    ↔    -     -    ←    ←    -
SCM          →     -     →    ←    ↔    -    -     -    ←    ←    -
CRM          -     -     -    ↔    -    -    -     -    ←    -    -
COMP         -     -     -    -    -    -    -     -    ←    -    -
IT           →     →     →    →    →    →    →     →    -    →    →
FIN          -     -     -    →    →    →    -     -    ←    -    ←
HR           -     -     -    -    -    -    -     -    ←    →    -

凡例: → 依存（自分が提供）、← 依存（相手から受領）、↔ 双方向
```

### 7.2 クリティカルパス

```
┌─────────────────────────────────────────────────────────────────────┐
│                    クリティカルサービス依存                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【認証フロー】（全サービス共通）                                    │
│  IT Platform → 全サービス                                           │
│                                                                     │
│  【製造フロー】                                                      │
│  R&D Platform → Manufacturing → Supply Chain → Finance             │
│       ↓                                                             │
│  Brand (品質基準)                                                   │
│                                                                     │
│  【マーケティングフロー】                                            │
│  Customer Platform ↔ Marketing → Supply Chain                      │
│       ↓                                                             │
│  Brand (ブランドガイドライン)                                       │
│                                                                     │
│  【ESGレポートフロー】                                               │
│  R&D + Manufacturing + Supply Chain → Sustainability → Brand       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 8. 実装優先度

### 8.1 フェーズ別実装計画

| Phase | サービス | 理由 | 期間目安 |
|-------|----------|------|----------|
| **Phase 1** | IT Platform | 全サービスの基盤 | 3-4ヶ月 |
| | Finance | 財務基盤 | |
| | HR | 組織・権限の基盤 | |
| **Phase 2** | Customer Platform | 顧客データ統合 | 4-6ヶ月 |
| | Brand Management | 全社ブランド基盤 | |
| | R&D Platform | コア技術基盤 | |
| **Phase 3** | Supply Chain | 調達・物流最適化 | 6-8ヶ月 |
| | Manufacturing (×5) | 製造DX | |
| **Phase 4** | Marketing (×5) | マーケDX | 4-6ヶ月 |
| | Compliance | コンプラ強化 | |
| **Phase 5** | Sustainability | ESG強化 | 3-4ヶ月 |

---

**サービス境界定義完了**: 2025-12-05
**次ステップ**: Context Map作成
