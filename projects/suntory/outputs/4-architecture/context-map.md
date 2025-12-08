# Context Map

**作成日**: 2025-12-05
**プロジェクト**: サントリーグループ
**Phase**: 4 - Architecture Design

---

## 1. Context Map概要

### 1.1 関係パターン定義

| パターン | 略称 | 説明 |
|----------|------|------|
| **Customer-Supplier** | C/S | 上流が下流のニーズに応じてAPIを提供 |
| **Conformist** | CF | 下流が上流のモデルに完全に従う |
| **Anti-Corruption Layer** | ACL | 下流が変換層で自己モデルを保護 |
| **Open Host Service** | OHS | 上流が標準化されたAPIを公開 |
| **Published Language** | PL | 共有の言語・スキーマを使用 |
| **Shared Kernel** | SK | 両者が共有モデルを持つ |
| **Partnership** | P | 対等な協力関係 |
| **Separate Ways** | SW | 統合しない |

---

## 2. 全体Context Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    サントリーグループ Context Map                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────────┐                             │
│                         │   IT Platform       │                             │
│                         │   (OHS/PL)          │                             │
│                         └──────────┬──────────┘                             │
│                                    │ 認証・認可                              │
│            ┌───────────────────────┼───────────────────────┐               │
│            │                       │                       │               │
│            ▼                       ▼                       ▼               │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  R&D Platform   │    │ Brand Management│    │ Sustainability  │        │
│  │    (OHS)        │    │    (OHS)        │    │    (C/S)        │        │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘        │
│           │                      │                      │                  │
│           │ 技術移転             │ ブランド基準          │ 環境データ        │
│           │                      │                      │                  │
│           ▼                      ▼                      │                  │
│  ┌─────────────────────────────────────────────────┐   │                  │
│  │              Manufacturing Services (×5)         │◀──┘                  │
│  │                    (C/S)                         │                      │
│  └────────┬─────────────────────────────┬──────────┘                      │
│           │                             │                                  │
│           │ 生産完了                     │ 出荷指示                         │
│           ▼                             ▼                                  │
│  ┌─────────────────┐           ┌─────────────────┐                        │
│  │   Finance       │◀──────────│  Supply Chain   │                        │
│  │    (CF)         │  費用計上  │    (P)          │                        │
│  └─────────────────┘           └────────┬────────┘                        │
│                                         │                                  │
│                                         │ 在庫・配送                        │
│                                         ▼                                  │
│  ┌─────────────────┐           ┌─────────────────┐                        │
│  │   Compliance    │           │ Customer Platform│                        │
│  │    (OHS)        │           │    (OHS/SK)     │                        │
│  └────────┬────────┘           └────────┬────────┘                        │
│           │                             │                                  │
│           │ 規制準拠                     │ 顧客データ                        │
│           ▼                             ▼                                  │
│  ┌─────────────────────────────────────────────────┐                      │
│  │              Marketing Services (×5)             │                      │
│  │                    (C/S)                         │                      │
│  └──────────────────────────────────────────────────┘                      │
│                                                                             │
│  ┌─────────────────┐                                                       │
│  │      HR         │──────▶ 全サービス（組織・権限情報）                    │
│  │    (OHS)        │                                                       │
│  └─────────────────┘                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. サービス間関係詳細

### 3.1 IT Platform → 全サービス

```yaml
関係:
  上流: IT Platform Service
  下流: 全サービス
  パターン: Open Host Service + Published Language

契約:
  認証API:
    endpoint: /api/v1/auth/token
    protocol: OAuth 2.0 / OIDC
    format: JWT
  認可API:
    endpoint: /api/v1/auth/permissions
    protocol: REST
    format: JSON
  監査ログ:
    protocol: Kafka
    format: CloudEvents

Published Language:
  - JWT Token標準（RFC 7519）
  - RBAC権限モデル
  - CloudEvents監査ログ形式

依存度: 高（全サービスが依存）
SLA要件: 99.99%可用性
```

### 3.2 R&D Platform → Manufacturing

```yaml
関係:
  上流: R&D Platform Service
  下流: Manufacturing Service (×5)
  パターン: Customer-Supplier

契約:
  技術仕様API:
    endpoint: /api/v1/fermentation/recipes
    method: GET
    用途: 醸造レシピ取得
  水品質基準API:
    endpoint: /api/v1/water-science/standards
    method: GET
    用途: 製造用水基準取得
  イベント:
    - TechnologyTransferReady
    - QualityStandardUpdated

データフロー:
  R&D Platform:
    提供: 醸造レシピ、水品質基準、熟成条件
  Manufacturing:
    利用: 製造パラメータとして適用

ACL考慮:
  Manufacturing側でR&Dモデルを製造モデルに変換
  例: ResearchRecipe → ProductionRecipe
```

### 3.3 Brand Management → Marketing/Manufacturing

```yaml
関係:
  上流: Brand Management Service
  下流: Marketing Service (×5), Manufacturing Service (×5)
  パターン: Open Host Service

契約:
  ブランドガイドラインAPI:
    endpoint: /api/v1/brand-guidelines/{brandId}
    method: GET
    用途: マーケ資材作成時の基準取得
  品質基準API:
    endpoint: /api/v1/quality-standards/{productId}
    method: GET
    用途: 製造時の品質基準取得
  イベント:
    - BrandGuidelineUpdated
    - QualityStandardUpdated

データフロー:
  Brand Management:
    提供: VIガイドライン、品質基準、ブランド資産
  Marketing:
    利用: キャンペーン資材作成
  Manufacturing:
    利用: 品質検査基準

Conformist度合い:
  下流サービスはブランド基準に完全準拠（Conformist寄り）
```

### 3.4 Customer Platform ↔ Marketing

```yaml
関係:
  参加者: Customer Platform Service, Marketing Service (×5)
  パターン: Shared Kernel + Partnership

Shared Kernel:
  共有エンティティ:
    - CustomerId (統合顧客ID)
    - SegmentId (セグメントID)
  共有イベント:
    - CustomerProfileUpdated
    - SegmentAssigned

契約:
  Customer Platform → Marketing:
    顧客セグメントAPI:
      endpoint: /api/v1/segments/{segmentId}/customers
      method: GET
      用途: ターゲティング
    イベント:
      - SegmentUpdated
      - CustomerProfileUpdated

  Marketing → Customer Platform:
    キャンペーン反応API:
      endpoint: /api/v1/campaigns/{campaignId}/responses
      method: POST
      用途: 顧客行動記録
    イベント:
      - CampaignInteraction
      - ConversionCompleted

調整プロセス:
  - 月次でセグメント定義を共同レビュー
  - 新規セグメント追加は双方合意
```

### 3.5 Manufacturing ↔ Supply Chain

```yaml
関係:
  参加者: Manufacturing Service (×5), Supply Chain Service
  パターン: Partnership

双方向契約:
  Manufacturing → Supply Chain:
    生産計画API:
      endpoint: /api/v1/production-plans
      method: POST
      用途: 原材料所要量連携
    イベント:
      - ProductionCompleted
      - MaterialRequested

  Supply Chain → Manufacturing:
    在庫状況API:
      endpoint: /api/v1/inventory/{skuId}
      method: GET
      用途: 原材料在庫確認
    入荷予定API:
      endpoint: /api/v1/shipments/incoming
      method: GET
      用途: 入荷計画確認
    イベント:
      - MaterialArrived
      - ShipmentDispatched

調整プロセス:
  - 週次で需給調整会議
  - 緊急時はリアルタイム連携
```

### 3.6 Supply Chain → Finance

```yaml
関係:
  上流: Supply Chain Service
  下流: Finance Service
  パターン: Customer-Supplier

契約:
  Supply Chain → Finance:
    発注情報API:
      endpoint: /api/v1/purchase-orders
      method: Webhook
      用途: 買掛計上
    入荷確認API:
      endpoint: /api/v1/goods-receipts
      method: Webhook
      用途: 検収計上
    イベント:
      - PurchaseOrderCreated
      - GoodsReceived
      - InvoiceReceived

  Finance → Supply Chain:
    支払状況API:
      endpoint: /api/v1/payments/{poId}/status
      method: GET
      用途: サプライヤへの支払状況確認

ACL:
  Finance側でSCMモデルを会計モデルに変換
  例: PurchaseOrder → AccountsPayable
```

### 3.7 Sustainability ← 複数サービス

```yaml
関係:
  下流: Sustainability Service
  上流: R&D Platform, Manufacturing (×5), Supply Chain
  パターン: Customer-Supplier (Sustainability側がCustomer)

契約:
  R&D Platform → Sustainability:
    水源涵養データAPI:
      endpoint: /api/v1/water-science/conservation
      method: GET
      用途: 水資源保全実績

  Manufacturing → Sustainability:
    環境データAPI:
      endpoint: /api/v1/environmental-data
      method: Webhook
      用途: CO2排出量、水使用量、廃棄物量
    イベント:
      - EnvironmentalDataRecorded

  Supply Chain → Sustainability:
    サプライヤ環境評価API:
      endpoint: /api/v1/suppliers/{id}/environmental-score
      method: GET
      用途: Scope3排出量計算

データ集約:
  Sustainabilityサービスが各サービスからデータを収集・集約
  ESGレポート用に統合
```

### 3.8 Compliance → Marketing/Manufacturing

```yaml
関係:
  上流: Compliance Service
  下流: Marketing Service (×5), Manufacturing Service (×5)
  パターン: Open Host Service

契約:
  規制情報API:
    endpoint: /api/v1/regulations/{category}
    method: GET
    用途: 適用規制の取得
  コンプライアンスチェックAPI:
    endpoint: /api/v1/compliance/check
    method: POST
    用途: 広告・表示のコンプライアンス確認
  イベント:
    - RegulationUpdated
    - ComplianceAlertRaised

適用例:
  Marketing:
    - 酒類広告規制チェック
    - 特定保健用食品表示確認
  Manufacturing:
    - 食品表示法準拠確認
    - 容器包装規制確認

Conformist度合い:
  規制準拠は必須のためConformist
```

---

## 4. イベントフロー

### 4.1 主要イベント一覧

```yaml
ドメインイベント:

R&D Platform:
  - ResearchCompleted
  - TechnologyTransferReady
  - QualityStandardUpdated

Brand Management:
  - BrandGuidelineUpdated
  - ProductBrandCreated
  - QualityStandardUpdated

Sustainability:
  - EnvironmentalDataUpdated
  - ESGScoreUpdated
  - SustainabilityReportPublished

Manufacturing:
  - ProductionOrderCreated
  - ProductionCompleted
  - QualityInspectionCompleted
  - EquipmentMaintenanceRequired

Marketing:
  - CampaignLaunched
  - CampaignCompleted
  - ConversionCompleted

Supply Chain:
  - PurchaseOrderCreated
  - GoodsReceived
  - ShipmentDispatched
  - InventoryUpdated

Customer Platform:
  - CustomerProfileUpdated
  - SegmentUpdated
  - ConsentChanged

Compliance:
  - PolicyUpdated
  - RegulationChanged
  - ComplianceAlertRaised

Finance:
  - JournalEntryCreated
  - PaymentProcessed
  - BudgetExceeded

HR:
  - EmployeeJoined
  - EmployeeLeft
  - OrganizationChanged
```

### 4.2 イベント購読マトリクス

```
発行者 →
購読者 ↓    RD   BRAND SUST  MKT  MFG  SCM  CRM  COMP  IT   FIN  HR
──────────────────────────────────────────────────────────────────────
R&D         -     -     -    -    -    -    -     -    ●    -    -
BRAND       -     -     -    -    -    -    -     -    ●    -    -
SUST        ●     -     -    -    ●    ●    -     -    ●    -    -
MKT         ●     ●     -    -    -    -    ●     ●    ●    -    -
MFG         ●     ●     -    -    -    ●    -     ●    ●    -    -
SCM         -     -     -    -    ●    -    -     -    ●    -    -
CRM         -     -     -    ●    -    -    -     -    ●    -    -
COMP        -     -     -    -    -    -    -     -    ●    -    -
IT          -     -     -    -    -    -    -     -    -    -    ●
FIN         -     -     -    -    ●    ●    -     -    ●    -    ●
HR          -     -     -    -    -    -    -     -    ●    -    -

● = 購読あり
```

---

## 5. 共有カーネル定義

### 5.1 顧客ID（Customer Platform ↔ Marketing）

```yaml
Shared Kernel: 顧客ID

共有エンティティ:
  UnifiedCustomerId:
    type: string
    format: UUID
    生成元: Customer Platform
    利用者: Marketing (×5)

  CustomerSegment:
    id: string
    name: string
    criteria: object
    管理者: Customer Platform
    参照者: Marketing (×5)

変更管理:
  - 変更提案: 双方から可能
  - 承認: CDP Teamが最終決定
  - 通知: SegmentUpdatedイベント
```

### 5.2 製品マスタ（Brand ↔ Manufacturing/Marketing）

```yaml
Shared Kernel: 製品マスタ

共有エンティティ:
  ProductId:
    type: string
    format: "PRD-{category}-{seq}"
    生成元: Brand Management
    利用者: Manufacturing, Marketing, Supply Chain

  ProductMaster:
    id: ProductId
    name: string
    brand: BrandId
    category: Category
    管理者: Brand Management
    参照者: 全サービス

変更管理:
  - 新規追加: Brand Managementが発行
  - 変更通知: ProductUpdatedイベント
  - 廃止: 論理削除のみ
```

### 5.3 組織マスタ（HR ↔ 全サービス）

```yaml
Shared Kernel: 組織マスタ

共有エンティティ:
  OrganizationId:
    type: string
    format: "ORG-{level}-{seq}"
    生成元: HR Service
    利用者: 全サービス

  OrganizationHierarchy:
    id: OrganizationId
    name: string
    parent: OrganizationId
    level: int
    管理者: HR Service
    参照者: 全サービス

変更管理:
  - 組織変更: HR Serviceが発行
  - 通知: OrganizationChangedイベント
  - 同期: 日次バッチ + リアルタイムイベント
```

---

## 6. Anti-Corruption Layer定義

### 6.1 Manufacturing ← R&D Platform

```yaml
ACL: Manufacturing Service内

目的: R&Dの研究モデルを製造モデルに変換

変換マッピング:
  ResearchRecipe:
    fermentationConditions → ProductionParameters
    qualityTargets → InspectionCriteria
    maturationSpec → AgingConfiguration

  WaterQualityStandard:
    analysisResults → ProductionWaterSpec
    purificationProcess → TreatmentPlan

実装:
  class RDTranslator:
    def to_production_parameters(research_recipe)
    def to_inspection_criteria(quality_targets)
    def to_water_spec(water_standard)
```

### 6.2 Finance ← Supply Chain

```yaml
ACL: Finance Service内

目的: SCMの調達モデルを会計モデルに変換

変換マッピング:
  PurchaseOrder:
    orderId → DocumentNumber
    supplier → VendorId
    items → LineItems
    totalAmount → AccountingAmount

  GoodsReceipt:
    receiptId → ReceiptDocument
    poId → ReferenceDocument
    items → ReceiptLineItems

実装:
  class SCMAccountingTranslator:
    def to_accounts_payable(purchase_order)
    def to_goods_receipt_posting(goods_receipt)
    def to_invoice_verification(invoice)
```

---

## 7. Context Map検証

### 7.1 循環依存チェック

```
✅ 循環依存なし

依存グラフ（簡略化）:
IT Platform
    ↓
┌───┴───┐
R&D    Brand    HR
 │       │       │
 └───┬───┘       │
     ↓           │
Manufacturing ←──┘
     │
     ↓
Supply Chain ──→ Finance
     │
     ↓
Customer Platform
     │
     ↓
Marketing

※ 全て上から下への依存、循環なし
```

### 7.2 結合度評価

| サービスペア | 結合度 | 理由 |
|--------------|--------|------|
| IT Platform → 全サービス | 高 | 認証必須 |
| Customer Platform ↔ Marketing | 中 | Shared Kernel |
| Manufacturing ↔ Supply Chain | 中 | Partnership |
| R&D Platform → Manufacturing | 低 | 参照のみ |
| Sustainability ← 複数 | 低 | データ収集のみ |

---

**Context Map完了**: 2025-12-05
**次ステップ**: Integration Patterns作成
