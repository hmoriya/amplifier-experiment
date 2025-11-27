# Bounded Context: brand-strategy-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** brand-strategy（ブランド戦略）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | brand-strategy-bc |
| **日本語名** | ブランド戦略 |
| **命名パターン** | `-strategy`（戦略型） |
| **命名理由** | 「ブランド管理」ではなく「戦略」を採用。Asahi Super Dryをはじめとするグローバルブランドの**戦略的進化**を表現。グローカル戦略（Global + Local）の中核として、ポートフォリオ最適化・プレミアムポジショニング・バリュー定義等の戦略的意思決定を担う |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

**BC名**: brand-strategy-bc（ブランド戦略バウンデッドコンテキスト）

**目的**:
Asahi Super Dryを中心とするグローバルブランド戦略の策定、ブランドポートフォリオ最適化、プレミアムポジショニング戦略の立案を行い、アサヒグループのグローカル戦略の中核を担う。

**責務**:
- グローバルブランド戦略の策定・更新（Asahi Super Dry世界戦略）
- ブランドポートフォリオの最適配置
- ブランドアーキテクチャ（階層構造）の設計
- プレミアムポジショニング戦略の策定
- ブランドバリュー・パーパスの定義と言語化
- グローバルブランドKPIの設定・モニタリング

**チーム境界**:
- **担当組織**: グローバルブランド本部 ブランド戦略部
- **チーム構成**:
  - グローバルブランド戦略チーム（Asahi Super Dry担当）
  - ポートフォリオ戦略チーム（欧州プレミアムブランド含む）
  - ブランドバリューチーム（パーパス・価値定義）
  - ブランドKPIチーム（測定・分析）
- **推定人員**: 25-35名（グローバル拠点含む）

---

### 2. ビジネスオペレーション詳細

#### OP1: グローバルブランド戦略策定

**業務フロー:**
```
1. 戦略環境分析
   └─ グローバル市場動向分析
   └─ 競合グローバルブランド分析（Heineken、AB InBev等）
   └─ 消費者嗜好変化分析（VS1市場機会発見からのインサイト）
   └─ 内部ケイパビリティ評価

2. 戦略方向性策定
   └─ グローバルブランドビジョン定義
   └─ 成長市場・重点地域の選定
   └─ ブランドパーソナリティの統一方針
   └─ プレミアム化戦略の方向性

3. 戦略施策立案
   └─ 地域別展開計画
   └─ 製品ラインナップ戦略（VS2製品開発との連携）
   └─ 価格戦略フレームワーク
   └─ コミュニケーション戦略骨子

4. 戦略承認・展開
   └─ グローバル経営会議での承認
   └─ 地域本部への戦略展開
   └─ KPI目標設定
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | グローバルブランド戦略はグローバル経営会議の承認を必須とする |
| BR-OP1-02 | 戦略サイクルは年次（毎年4月開始）とし、中間レビューを10月に実施 |
| BR-OP1-03 | Asahi Super Dryの戦略変更は取締役会報告を必須とする |
| BR-OP1-04 | グローカル原則：グローバル一貫性とローカル適応のバランスを明文化 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| グローバル市場調査（VS1） | グローバルブランド戦略書 |
| 競合分析レポート | 地域別展開方針 |
| 消費者インサイト | 年次KPI目標 |
| 前年度実績・反省 | 戦略骨子（経営会議用） |

**トリガー:**
- 年次戦略サイクル開始（1月）
- 市場環境の大幅変化
- M&A・事業再編
- 経営戦略の見直し

---

#### OP2: ブランドポートフォリオ最適化

**業務フロー:**
```
1. ポートフォリオ現状分析
   └─ 全ブランドの市場ポジション評価
   └─ ブランド別収益性分析
   └─ ブランド間カニバリゼーション分析
   └─ 地域別ブランド配置確認

2. 最適化方針策定
   └─ 成長ブランド/維持ブランド/撤退ブランドの分類
   └─ プレミアムポートフォリオ構成（Asahi Super Dry, Peroni, Grolsch, Pilsner Urquell）
   └─ セグメント別カバレッジ設計
   └─ 地域ブランドとの棲み分け

3. 投資配分決定
   └─ ブランド別マーケティング投資配分
   └─ 新規ブランド獲得・育成投資
   └─ ブランド統廃合判断

4. ポートフォリオ実行管理
   └─ 月次ポートフォリオレビュー
   └─ ブランド別KPIモニタリング
   └─ 必要に応じた機動的調整
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | ポートフォリオ変更（ブランド統廃合）は経営会議承認を必須とする |
| BR-OP2-02 | 新規ブランド獲得は戦略的整合性評価を必須とする |
| BR-OP2-03 | プレミアムセグメント比率目標を設定し、四半期レビューを実施 |
| BR-OP2-04 | 欧州プレミアムブランド（Peroni、Grolsch、Pilsner Urquell）は個別戦略を策定 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ブランド別財務データ | ポートフォリオ最適化方針 |
| 市場シェアデータ | ブランド別投資配分 |
| 消費者調査結果 | 統廃合計画（該当時） |
| M&A候補情報 | ポートフォリオレビューレポート |

**トリガー:**
- 年次戦略策定
- M&A・買収完了
- ブランド業績大幅変動
- 市場構造変化

---

#### OP3: ブランドアーキテクチャ設計

**業務フロー:**
```
1. 現行アーキテクチャ評価
   └─ ブランド階層構造の整理
   └─ 親ブランド・子ブランド関係の明確化
   └─ エンドースメント構造の評価
   └─ 消費者認知構造調査

2. アーキテクチャ設計
   └─ マスターブランド戦略（Asahi）の定義
   └─ サブブランド体系の設計
   └─ 地域ブランドの位置づけ
   └─ 製品ブランド命名規則

3. エンドースメント設計
   └─ Asahiロゴの使用ルール
   └─ 各ブランドへのエンドースメントレベル
   └─ コ・ブランディングルール
   └─ ライセンスブランドの扱い

4. アーキテクチャ展開
   └─ ガイドライン文書化（brand-asset-governance連携）
   └─ 地域本部への展開
   └─ 定期的な遵守状況レビュー
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | ブランドアーキテクチャ変更はグローバルブランド委員会の承認を必須とする |
| BR-OP3-02 | 新ブランド・サブブランド追加時はアーキテクチャ適合性評価を必須とする |
| BR-OP3-03 | Asahiマスターブランドへのエンドースメントは品質基準クリアを条件とする |
| BR-OP3-04 | 地域ローカルブランドのアーキテクチャ位置づけは地域本部と協議 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 現行ブランド一覧 | ブランドアーキテクチャ図 |
| 消費者認知調査 | アーキテクチャガイドライン |
| ポートフォリオ方針 | 命名規則書 |
| 競合アーキテクチャ分析 | エンドースメントルール |

**トリガー:**
- 新ブランド獲得・開発
- ポートフォリオ再編
- ブランドリブランディング
- 3年周期の定期見直し

---

#### OP4: プレミアムポジショニング策定

**業務フロー:**
```
1. 市場ポジション分析
   └─ プレミアムセグメント市場調査
   └─ 競合ポジショニング分析
   └─ 消費者のプレミアム認知調査
   └─ 価格帯別市場構造分析

2. ポジショニング戦略策定
   └─ ターゲット顧客セグメント定義
   └─ 差別化ポイント明確化
   └─ 価値提案（バリュープロポジション）策定
   └─ 価格ポジショニング決定

3. ポジショニングマップ作成
   └─ 主要軸の選定（品質/価格、伝統/革新等）
   └─ 自社ブランド配置
   └─ 競合ブランド配置
   └─ ホワイトスペース特定

4. ポジショニング実行
   └─ コミュニケーション戦略への反映
   └─ 製品開発への反映（VS2連携）
   └─ 価格戦略への反映
   └─ 定期的なポジション確認
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | プレミアムポジショニングは年次で見直しを実施 |
| BR-OP4-02 | 価格ポジショニング変更は収益影響シミュレーションを必須とする |
| BR-OP4-03 | Asahi Super Dryは「グローバルプレミアムラガー」としてポジショニング固定 |
| BR-OP4-04 | 欧州ブランドは各国プレミアムセグメント上位を目標とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 市場調査データ | ポジショニングマップ |
| 競合分析 | バリュープロポジション |
| 消費者調査 | 価格ポジショニング方針 |
| 製品スペック（VS2） | ポジショニングステートメント |

**トリガー:**
- 年次戦略サイクル
- 競合動向変化
- 新製品投入
- 価格改定検討時

---

#### OP5: ブランドバリュー定義

**業務フロー:**
```
1. ブランドエッセンス探索
   └─ ブランドヘリテージ調査
   └─ 創業者精神・企業理念との連携
   └─ 消費者のブランド連想調査
   └─ 内部ステークホルダーヒアリング

2. ブランドパーパス策定
   └─ ブランドの社会的存在意義定義
   └─ 「なぜこのブランドが存在するか」の言語化
   └─ サステナビリティとの連携
   └─ 従業員エンゲージメントとの連携

3. ブランドバリュー体系化
   └─ コアバリュー（3-5個）の定義
   └─ バリューの行動指針への展開
   └─ ブランドパーソナリティの明文化
   └─ ブランドトーン&マナー設定

4. バリュー浸透・活用
   └─ 社内浸透プログラム
   └─ 外部コミュニケーションへの反映
   └─ 製品開発基準への反映
   └─ 定期的なバリュー体現度評価
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | ブランドパーパス・コアバリューの変更は取締役会承認を必須とする |
| BR-OP5-02 | グローバルブランドのバリューは全地域で統一（ローカル解釈は許容） |
| BR-OP5-03 | バリュー定義は消費者調査による検証を必須とする |
| BR-OP5-04 | バリュー体現度はブランドトラッキング調査で測定 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 企業理念・ビジョン | ブランドパーパスステートメント |
| 消費者調査 | コアバリュー定義書 |
| ブランドヘリテージ | ブランドパーソナリティガイド |
| 競合バリュー分析 | トーン&マナーガイド |

**トリガー:**
- 新ブランド立ち上げ
- リブランディング
- 企業理念改定
- 5年周期の定期見直し

---

#### OP6: グローバルブランドKPI設定

**業務フロー:**
```
1. KPIフレームワーク設計
   └─ 戦略目標からのKPI導出
   └─ 財務KPI・非財務KPIのバランス
   └─ 先行指標・遅行指標の設定
   └─ 地域共通KPIと地域固有KPIの設計

2. 具体的KPI設定
   └─ ブランド認知度（Aided/Unaided）
   └─ ブランドエクイティスコア
   └─ NPS（ネットプロモータースコア）
   └─ プレミアム価格プレミアム率
   └─ 市場シェア（金額/数量）
   └─ 購入意向率

3. 目標値設定
   └─ ベンチマーク分析（自社過去/競合）
   └─ ストレッチ目標設定
   └─ 地域別目標設定
   └─ 四半期/年次目標の分解

4. KPIモニタリング体制構築
   └─ 測定方法・頻度の決定
   └─ レポーティングプロセス設計
   └─ ダッシュボード構築（VS6連携）
   └─ レビューミーティング設定
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP6-01 | グローバルKPIは全地域で統一された定義・測定方法を使用 |
| BR-OP6-02 | KPI目標は年次で設定し、中間見直しは原則不可 |
| BR-OP6-03 | ブランドエクイティスコアは第三者調査機関による測定を必須とする |
| BR-OP6-04 | KPI達成状況は月次でグローバルブランド委員会に報告 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ブランド戦略 | KPIフレームワーク |
| 過去実績データ | KPI目標シート |
| ベンチマークデータ | KPIダッシュボード |
| 調査設計 | KPIレビューレポート |

**トリガー:**
- 年次計画サイクル
- 戦略変更
- 新ブランド追加
- M&A完了

---

### 3. ドメインイベント

#### 発行イベント（Published Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **GlobalBrandStrategyApproved** | {strategyId, brandId, year, keyDirections, approvedBy, approvedAt} | グローバルブランド戦略承認時 | regional-brand-activation, campaign-communications |
| **PortfolioOptimizationDecided** | {portfolioId, decisions[], investmentAllocation, decidedAt} | ポートフォリオ最適化決定時 | regional-brand-activation, marketing-analytics |
| **BrandArchitectureUpdated** | {architectureId, version, changes[], updatedAt} | ブランドアーキテクチャ更新時 | brand-asset-governance |
| **PremiumPositioningDefined** | {brandId, positioning, valueProposition, targetSegment, definedAt} | プレミアムポジショニング策定時 | campaign-communications, VS2製品開発 |
| **BrandValuesDefined** | {brandId, purpose, coreValues[], personality, definedAt} | ブランドバリュー定義時 | brand-asset-governance, campaign-communications |
| **BrandKPITargetsSet** | {brandId, year, kpiTargets[], setAt} | KPI目標設定時 | marketing-analytics, regional-brand-activation |

#### 購読イベント（Subscribed Events）

| イベント名 | 発行元 | 購読理由 |
|-----------|--------|---------|
| **MarketInsightDiscovered** | VS1 market-opportunity-discovery | 戦略策定への市場インサイト反映 |
| **BrandTrackingCompleted** | marketing-analytics | KPI実績把握、戦略見直しトリガー |
| **NewProductLaunched** | VS2 premium-beer-development | ポートフォリオ・ポジショニングへの反映 |
| **RegionalPerformanceReported** | regional-brand-activation | 地域戦略の評価・調整 |
| **CompetitorActionDetected** | marketing-analytics | 競合動向への戦略対応 |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: GlobalBrandStrategy（グローバルブランド戦略）

**責務**: グローバルブランド戦略のライフサイクル管理

```
GlobalBrandStrategy [Aggregate Root]
├── strategyId: StrategyId [Value Object]
├── brandId: BrandId [Value Object]
├── strategyYear: Year [Value Object]
├── vision: BrandVision [Value Object]
│   ├── statement: string
│   ├── timeHorizon: Duration（通常3-5年）
│   └── keyAspiraitons: string[]
├── strategicDirections: StrategicDirection[] [Entity]
│   ├── directionId: DirectionId
│   ├── area: enum (MARKET_EXPANSION, PREMIUM_GROWTH, DIGITAL_TRANSFORMATION, SUSTAINABILITY)
│   ├── description: string
│   ├── targetOutcome: string
│   └── priority: Priority
├── targetMarkets: TargetMarket[] [Value Object]
│   ├── region: Region
│   ├── priority: enum (PRIMARY, SECONDARY, EMERGING)
│   └── growthTarget: Percentage
├── investmentPlan: InvestmentPlan [Entity]
│   ├── totalBudget: Money
│   ├── allocationByRegion: Map<Region, Money>
│   └── allocationByActivity: Map<ActivityType, Money>
├── kpiTargets: KPITarget[] [Value Object]
│   ├── kpiType: KPIType
│   ├── targetValue: number
│   └── measurementFrequency: Frequency
├── approvalStatus: ApprovalStatus [Value Object]
│   ├── status: enum (DRAFT, UNDER_REVIEW, APPROVED, SUPERSEDED)
│   ├── approvedBy: UserId?
│   └── approvedAt: Date?
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-GBS-01 | APPROVED状態への遷移にはグローバル経営会議承認を必須とする |
| INV-GBS-02 | 同一brandId・strategyYearのAPPROVED戦略は最大1つ |
| INV-GBS-03 | 新戦略承認時、前年戦略は自動的にSUPERSEDED状態に遷移 |
| INV-GBS-04 | investmentPlanの合計は予算上限を超えないこと |

---

#### 集約2: BrandPortfolio（ブランドポートフォリオ）

**責務**: ブランドポートフォリオ構成と最適化方針の管理

```
BrandPortfolio [Aggregate Root]
├── portfolioId: PortfolioId [Value Object]
├── asOfDate: Date [Value Object]
├── brands: PortfolioBrand[] [Entity]
│   ├── brandId: BrandId
│   ├── name: BrandName
│   ├── segment: enum (PREMIUM, MAINSTREAM, VALUE)
│   ├── role: enum (FLAGSHIP, GROWTH_DRIVER, CASH_COW, NICHE, EMERGING)
│   ├── regions: Region[]
│   ├── revenue: Money
│   ├── marketShare: Percentage
│   └── strategicPriority: Priority
├── premiumPortfolio: PremiumPortfolio [Value Object]
│   ├── flagshipBrand: BrandId（Asahi Super Dry）
│   ├── europeanPremium: BrandId[]（Peroni, Grolsch, Pilsner Urquell）
│   └── targetPremiumRatio: Percentage
├── optimizationDecisions: OptimizationDecision[] [Entity]
│   ├── decisionId: DecisionId
│   ├── brandId: BrandId
│   ├── decisionType: enum (INVEST, MAINTAIN, HARVEST, DIVEST, MERGE)
│   ├── rationale: string
│   └── decidedAt: Date
├── investmentAllocation: BrandInvestment[] [Value Object]
│   ├── brandId: BrandId
│   ├── budget: Money
│   └── allocationRatio: Percentage
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-BP-01 | investmentAllocation合計は100%であること |
| INV-BP-02 | FLAGSHIPロールのブランドは最低1つ存在すること |
| INV-BP-03 | DIVESTの決定は経営会議承認済みであること |
| INV-BP-04 | Asahi Super DryはFLAGSHIPロールから変更不可 |

---

#### 集約3: BrandArchitecture（ブランドアーキテクチャ）

**責務**: ブランド階層構造とエンドースメントルールの管理

```
BrandArchitecture [Aggregate Root]
├── architectureId: ArchitectureId [Value Object]
├── version: Version [Value Object]
├── effectiveDate: Date [Value Object]
├── masterBrand: MasterBrand [Entity]
│   ├── brandId: BrandId（Asahi）
│   ├── positioning: string
│   └── endorsementPolicy: EndorsementPolicy
├── brandHierarchy: BrandNode[] [Entity]
│   ├── brandId: BrandId
│   ├── brandName: BrandName
│   ├── level: enum (MASTER, SUB_BRAND, PRODUCT_BRAND, ENDORSED_BRAND)
│   ├── parentBrandId: BrandId?
│   ├── endorsementLevel: enum (STRONG, MODERATE, LIGHT, NONE)
│   └── namingPattern: NamingPattern
├── namingRules: NamingRule[] [Value Object]
│   ├── ruleId: RuleId
│   ├── brandLevel: BrandLevel
│   ├── pattern: string
│   └── examples: string[]
├── endorsementRules: EndorsementRule[] [Value Object]
│   ├── ruleId: RuleId
│   ├── sourceLevel: BrandLevel
│   ├── targetLevel: BrandLevel
│   ├── visualTreatment: string
│   └── restrictions: string[]
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-BA-01 | MASTERレベルのブランドは1つのみ（Asahi） |
| INV-BA-02 | 全ブランドはいずれかのレベルに属すること |
| INV-BA-03 | 親子関係に循環参照は不可 |
| INV-BA-04 | バージョン変更時は変更履歴を記録 |

---

#### 集約4: BrandPositioning（ブランドポジショニング）

**責務**: ブランドの市場ポジショニングと差別化要素の管理

```
BrandPositioning [Aggregate Root]
├── positioningId: PositioningId [Value Object]
├── brandId: BrandId [Value Object]
├── effectiveDate: Date [Value Object]
├── targetSegment: TargetSegment [Value Object]
│   ├── demographics: Demographics
│   ├── psychographics: Psychographics
│   └── occasions: ConsumptionOccasion[]
├── positioningStatement: PositioningStatement [Value Object]
│   ├── targetAudience: string
│   ├── category: string
│   ├── benefitPromise: string
│   └── reasonToBelieve: string
├── valueProposition: ValueProposition [Value Object]
│   ├── functionalBenefits: string[]
│   ├── emotionalBenefits: string[]
│   └── selfExpressiveBenefits: string[]
├── differentiators: Differentiator[] [Value Object]
│   ├── factor: string
│   ├── competitiveAdvantage: string
│   └── sustainability: enum (SUSTAINABLE, TEMPORARY, AT_RISK)
├── pricePositioning: PricePositioning [Value Object]
│   ├── tier: enum (SUPER_PREMIUM, PREMIUM, PREMIUM_MAINSTREAM, MAINSTREAM)
│   ├── indexVsCategory: Percentage（カテゴリ平均比）
│   └── indexVsCompetitor: Map<CompetitorId, Percentage>
├── positioningMap: PositioningMapCoordinates [Value Object]
│   ├── primaryAxis: AxisPosition
│   └── secondaryAxis: AxisPosition
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-POS-01 | Asahi Super DryはPREMIUMまたはSUPER_PREMIUMティアのみ |
| INV-POS-02 | positioningStatementの全項目が設定されていること |
| INV-POS-03 | differentiatorは最低1つ必須 |
| INV-POS-04 | pricePositioning変更は収益影響評価済みであること |

---

#### 集約5: BrandValue（ブランドバリュー）

**責務**: ブランドパーパス・コアバリュー・パーソナリティの管理

```
BrandValue [Aggregate Root]
├── valueId: BrandValueId [Value Object]
├── brandId: BrandId [Value Object]
├── version: Version [Value Object]
├── purpose: BrandPurpose [Value Object]
│   ├── statement: string（例："Delivering great taste and refreshment to the world"）
│   ├── socialImpact: string
│   └── heritage: string
├── coreValues: CoreValue[] [Value Object]
│   ├── valueName: string（例：Challenge, Innovation, Quality, Diversity）
│   ├── definition: string
│   └── behaviors: string[]（価値を体現する行動）
├── personality: BrandPersonality [Value Object]
│   ├── traits: PersonalityTrait[]（例：Confident, Modern, Authentic, Dynamic）
│   └── archetype: BrandArchetype（例：The Explorer, The Creator）
├── toneOfVoice: ToneOfVoice [Value Object]
│   ├── characteristics: string[]
│   ├── doList: string[]
│   └── dontList: string[]
├── visualIdentity: VisualIdentityPrinciples [Value Object]
│   ├── colorPrinciples: string
│   ├── typographyPrinciples: string
│   └── imageryPrinciples: string
├── approvalStatus: ApprovalStatus [Value Object]
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-BV-01 | purposeは取締役会承認済みであること |
| INV-BV-02 | coreValuesは3-5個の範囲であること |
| INV-BV-03 | バージョン変更時は全地域への通知を必須とする |
| INV-BV-04 | グローバルブランドのvalueはローカル変更不可（解釈の追加のみ許容） |

---

#### 集約6: BrandKPI（ブランドKPI）

**責務**: ブランドKPIの目標設定と実績管理

```
BrandKPI [Aggregate Root]
├── kpiId: BrandKPIId [Value Object]
├── brandId: BrandId [Value Object]
├── year: Year [Value Object]
├── globalTargets: KPITarget[] [Entity]
│   ├── kpiType: KPIType
│   │   └── value: enum (BRAND_AWARENESS_AIDED, BRAND_AWARENESS_UNAIDED,
│   │                    BRAND_EQUITY_SCORE, NPS, PURCHASE_INTENT,
│   │                    MARKET_SHARE_VALUE, MARKET_SHARE_VOLUME,
│   │                    PRICE_PREMIUM_INDEX, CONSIDERATION_RATE)
│   ├── targetValue: number
│   ├── baselineValue: number
│   ├── stretch: boolean
│   └── measurementMethod: MeasurementMethod
├── regionalTargets: RegionalKPITarget[] [Entity]
│   ├── region: Region
│   ├── kpiTargets: KPITarget[]
│   └── localAdjustments: string[]
├── actuals: KPIActual[] [Entity]
│   ├── period: Period（月/四半期/年）
│   ├── kpiType: KPIType
│   ├── actualValue: number
│   ├── variance: Percentage
│   └── commentary: string
├── trackingSchedule: TrackingSchedule [Value Object]
│   ├── frequency: enum (MONTHLY, QUARTERLY, ANNUAL)
│   ├── surveyProvider: string
│   └── nextTrackingDate: Date
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-KPI-01 | globalTargetsは全KPIType（必須項目）をカバーすること |
| INV-KPI-02 | targetValueはbaselineValue以上であること（改善目標） |
| INV-KPI-03 | actualsは測定完了後のみ登録可 |
| INV-KPI-04 | 年次目標の中間変更は経営会議承認を必須とする |

---

### 5. コンテキストマップ（Context Map）

```
                              ┌──────────────────────────────────────┐
                              │                                      │
                              │   VS0: strategy-planning-bc          │
                              │        (Upstream)                    │
                              │                                      │
                              │   グローカル戦略方針                   │
                              └──────────────┬───────────────────────┘
                                             │ 経営戦略方針
                                             ▼
        ┌─────────────────┐    ┌──────────────────────────────────┐    ┌─────────────────┐
        │ VS1: market-    │    │                                  │    │ VS2: premium-   │
        │ opportunity-    │───►│     brand-strategy-bc            │◄───│ beer-           │
        │ discovery-bc    │    │                                  │    │ development-bc  │
        │ (Upstream)      │    │                                  │    │ (Partnership)   │
        │                 │    └──────────────┬───────────────────┘    │                 │
        │ 市場インサイト   │                   │                        │ 製品情報・能力   │
        └─────────────────┘                   │                        └─────────────────┘
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              │                               │                               │
              ▼                               ▼                               ▼
    ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
    │ regional-brand- │         │ campaign-       │         │ brand-asset-    │
    │ activation-bc   │         │ communications  │         │ governance-bc   │
    │ (Downstream)    │         │ -bc             │         │ (Partnership)   │
    │                 │         │ (Downstream)    │         │                 │
    │ 地域展開方針受領 │         │ メッセージ受領  │         │ アイデンティティ │
    └─────────────────┘         └─────────────────┘         └─────────────────┘
                                              │
                                              ▼
                              ┌─────────────────┐
                              │ marketing-      │
                              │ analytics-bc    │
                              │ (Upstream)      │
                              │                 │
                              │ KPI実績提供      │
                              └─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| VS0 strategy-planning-bc | **Conformist** | 経営戦略・グローカル戦略方針に準拠 |
| VS1 market-opportunity-discovery-bc | **Customer-Supplier** | 市場インサイト・消費者トレンドの供給を受ける |
| VS2 premium-beer-development-bc | **Partnership** | 製品戦略とブランド戦略の整合。製品開発能力の共有 |
| regional-brand-activation-bc | **Customer-Supplier** | グローバル戦略方針を提供、地域戦略を受領 |
| campaign-communications-bc | **Customer-Supplier** | ブランドメッセージ・バリュープロポジションを提供 |
| brand-asset-governance-bc | **Partnership** | アイデンティティ定義とガイドライン管理で対等に協力 |
| marketing-analytics-bc | **Customer-Supplier** | KPI実績・ブランドトラッキングデータの供給を受ける |

---

### 6. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/strategies` | POST | グローバルブランド戦略作成 |
| `/strategies/{id}/approve` | POST | 戦略承認 |
| `/strategies/{id}/supersede` | POST | 戦略更新（旧戦略を置換） |
| `/portfolios` | POST | ポートフォリオ作成・更新 |
| `/portfolios/{id}/optimize` | POST | ポートフォリオ最適化決定登録 |
| `/architectures` | POST | アーキテクチャ作成 |
| `/architectures/{id}/update` | POST | アーキテクチャ更新 |
| `/positionings` | POST | ポジショニング策定 |
| `/positionings/{id}/update` | POST | ポジショニング更新 |
| `/brand-values` | POST | ブランドバリュー定義 |
| `/brand-values/{id}/approve` | POST | バリュー承認 |
| `/kpis` | POST | KPI目標設定 |
| `/kpis/{id}/actuals` | POST | KPI実績登録 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/strategies` | GET | 戦略一覧 |
| `/strategies/{id}` | GET | 戦略詳細 |
| `/strategies/current/{brandId}` | GET | 現行戦略取得 |
| `/portfolios/{id}` | GET | ポートフォリオ詳細 |
| `/portfolios/current` | GET | 現行ポートフォリオ |
| `/architectures/current` | GET | 現行アーキテクチャ |
| `/positionings/{brandId}/current` | GET | ブランド別現行ポジショニング |
| `/brand-values/{brandId}/current` | GET | ブランド別現行バリュー |
| `/kpis/{brandId}/{year}` | GET | ブランド別年次KPI |
| `/kpis/{brandId}/dashboard` | GET | KPIダッシュボードデータ |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| VS1 market-opportunity-discovery-bc | 市場調査結果、消費者インサイト参照 |
| VS2 premium-beer-development-bc | 製品ロードマップ、製品スペック参照 |
| marketing-analytics-bc | ブランドトラッキングデータ、競合分析データ参照 |

---

### 7. ユビキタス言語（Ubiquitous Language）

#### 戦略用語

| 用語 | 定義 |
|------|------|
| **Glocal Strategy（グローカル戦略）** | Global + Local。グローバルな一貫性とローカルな適応を両立させるアサヒグループの戦略アプローチ |
| **Global Flagship Brand（グローバルフラッグシップブランド）** | Asahi Super Dry。世界展開の中核となる主力ブランド |
| **European Premium Portfolio（欧州プレミアムポートフォリオ）** | Peroni、Grolsch、Pilsner Urquell等、買収により獲得した欧州プレミアムブランド群 |
| **Premium Positioning（プレミアムポジショニング）** | 高品質・高価格帯での市場ポジション。アサヒグループの成長戦略の柱 |

#### ブランド管理用語

| 用語 | 定義 |
|------|------|
| **Brand Architecture（ブランドアーキテクチャ）** | ブランド間の階層構造と関係性を定義したフレームワーク |
| **Master Brand（マスターブランド）** | Asahi。全てのブランドの親となる企業ブランド |
| **Endorsement（エンドースメント）** | マスターブランドによるサブブランドへの品質保証・支持 |
| **Brand Portfolio（ブランドポートフォリオ）** | 企業が保有するブランド群の構成 |

#### 価値・ポジショニング用語

| 用語 | 定義 |
|------|------|
| **Brand Purpose（ブランドパーパス）** | ブランドの社会的存在意義。なぜこのブランドが存在するかの回答 |
| **Core Values（コアバリュー）** | ブランドの中核となる価値観（3-5個程度） |
| **Brand Personality（ブランドパーソナリティ）** | ブランドを人格化した場合の特性 |
| **Value Proposition（バリュープロポジション）** | ブランドが消費者に提供する価値の約束 |

#### KPI用語

| 用語 | 定義 |
|------|------|
| **Brand Equity Score（ブランドエクイティスコア）** | ブランドの資産価値を数値化した指標 |
| **Brand Awareness（ブランド認知度）** | Aided（助成想起）/Unaided（純粋想起）の2種類で測定 |
| **NPS（Net Promoter Score）** | 推奨意向から批判意向を引いた顧客ロイヤルティ指標 |
| **Price Premium Index（価格プレミアム指数）** | カテゴリ平均価格に対する自社ブランド価格の比率 |

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（brand-strategy-bc定義）
