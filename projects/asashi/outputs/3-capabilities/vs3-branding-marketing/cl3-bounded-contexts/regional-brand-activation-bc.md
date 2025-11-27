# Bounded Context: regional-brand-activation-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** regional-brand-activation（リージョナルブランド展開）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | regional-brand-activation-bc |
| **日本語名** | リージョナルブランド展開 |
| **命名パターン** | `-activation`（能動型） |
| **命名理由** | 「地域ブランド管理」ではなく「activation」を採用。Peroni、Grolsch、Pilsner Urquell等の欧州プレミアムブランドの**活性化・発展**を表現。グローバル戦略を各地域で**能動的に展開**するGlocal実践を意図 |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

**BC名**: regional-brand-activation-bc（リージョナルブランド展開バウンデッドコンテキスト）

**目的**:
欧州プレミアムブランド（Peroni、Grolsch、Pilsner Urquell、Kozel等）の地域展開戦略を策定・実行し、3リージョン戦略（日本/東アジア、欧州、アジアパシフィック）の下でGlocal（グローバル戦略＋ローカル実行）アプローチを実践する。

**責務**:
- 地域ブランド戦略の策定（欧州、アジアパシフィック）
- グローバルブランド方針のローカル適応
- 地域別キャンペーンの計画・適応
- 地域マーケティングチームとの連携・調整
- ブランドローカライゼーションガイドラインの策定・運用

**チーム境界**:
- **担当組織**: グローバルマーケティング本部 リージョナルブランド部
- **チーム構成**:
  - 欧州ブランドチーム（Peroni、Grolsch、Pilsner Urquell担当）
  - アジアパシフィックブランドチーム（Kozel、地域ブランド担当）
  - ローカライゼーションチーム（適応ガイドライン、翻訳連携）
  - 地域調整チーム（地域本部との連携）
- **推定人員**: 30-45名（本社＋地域拠点）

---

### 2. ビジネスオペレーション詳細

#### OP1: 地域ブランド戦略策定（欧州、アジアパシフィック）

**業務フロー:**
```
1. グローバル方針の受領
   └─ brand-strategy-bcからのグローバルブランド戦略受領
   └─ Glocal方針の確認
   └─ 3リージョン戦略との整合確認

2. 地域市場分析
   └─ 地域別消費者嗜好分析
   └─ 地域競合ブランド分析
   └─ 規制・文化的要因調査
   └─ チャネル特性分析

3. 地域ブランド戦略立案
   └─ 地域ポジショニング設定
   └─ 地域ターゲット定義
   └─ 地域KPI設定
   └─ 投資配分計画

4. 戦略承認
   └─ 地域本部レビュー
   └─ グローバル本部承認
   └─ 戦略書発行
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 地域戦略はグローバルブランド戦略との整合性を必須とする |
| BR-OP1-02 | 地域戦略策定には現地マーケティングチームの参画を必須とする |
| BR-OP1-03 | 新市場展開は3年ROI見通しを必須とする |
| BR-OP1-04 | 地域戦略は年次で見直し、四半期でレビューする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| グローバルブランド戦略（brand-strategy-bc） | 地域ブランド戦略書 |
| 地域市場調査データ（VS1） | 地域ポジショニングマップ |
| 競合分析データ | 地域投資計画 |

**トリガー:**
- 年次計画サイクル
- グローバル戦略変更
- 新市場参入決定
- 競合動向の大きな変化

---

#### OP2: ローカルブランドポジショニング

**業務フロー:**
```
1. グローバルポジショニングの理解
   └─ マスターブランドの価値・位置づけ確認
   └─ グローバルターゲット層の理解
   └─ 差別化要素の把握

2. ローカル適応分析
   └─ 現地消費者の価値観分析
   └─ 現地競合ポジション分析
   └─ 文化的適応必要性評価
   └─ 価格帯の現地最適化

3. ローカルポジショニング策定
   └─ 現地ターゲットセグメント定義
   └─ 現地価値提案の調整
   └─ 現地コミュニケーションメッセージ開発
   └─ 現地価格戦略設定

4. ポジショニング検証
   └─ 現地消費者テスト
   └─ グローバル整合性確認
   └─ ポジショニング承認
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | ローカルポジショニングはグローバルブランドエッセンスを維持する |
| BR-OP2-02 | 価格帯変更は地域本部＋グローバル本部の承認を必須とする |
| BR-OP2-03 | ローカル消費者テストなしにポジショニング確定は不可 |
| BR-OP2-04 | プレミアムブランドの価格帯は現地トップ20%以内を維持する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| グローバルポジショニング | ローカルポジショニングステートメント |
| 現地消費者分析データ | ローカル価値提案書 |
| 競合ポジション情報 | 現地価格戦略 |

**トリガー:**
- 新ブランド地域展開
- 市場環境の変化
- 競合動向の変化
- 消費者嗜好の変化

---

#### OP3: 地域別キャンペーン適応

**業務フロー:**
```
1. グローバルキャンペーンの受領
   └─ グローバルクリエイティブコンセプト受領
   └─ メディアガイドライン確認
   └─ タイムライン確認

2. ローカル適応企画
   └─ 文化的適応ポイント特定
   └─ 言語ローカライゼーション計画
   └─ ビジュアル適応計画
   └─ 現地メディアミックス設計

3. ローカルクリエイティブ開発
   └─ コピーローカライズ
   └─ ビジュアル適応制作
   └─ 現地タレント・インフルエンサー起用検討
   └─ 法規制対応確認

4. キャンペーン実行
   └─ 現地メディア出稿
   └─ デジタル施策連携（digital-marketing-bc）
   └─ 店頭施策連携（brand-experience-bc）

5. 効果測定・報告
   └─ 地域KPI測定
   └─ グローバル報告
   └─ ベストプラクティス共有
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | グローバルクリエイティブのコア要素（ロゴ使用、ブランドカラー等）は変更不可 |
| BR-OP3-02 | 現地法規制（アルコール広告規制等）の100%遵守を必須とする |
| BR-OP3-03 | ローカル適応クリエイティブはbrand-asset-governance-bcの承認を必須とする |
| BR-OP3-04 | キャンペーン効果はグローバル標準KPIで測定・報告する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| グローバルキャンペーンブリーフ | ローカル適応キャンペーン計画 |
| 現地メディア情報 | ローカルクリエイティブ |
| 法規制情報 | キャンペーン効果レポート |

**トリガー:**
- グローバルキャンペーン開始
- 地域特有イベント（祭り、スポーツ大会等）
- 季節性プロモーション
- 製品発売

---

#### OP4: 地域マーケティングチーム連携

**業務フロー:**
```
1. 連携体制構築
   └─ 地域マーケティング担当者のアサイン
   └─ 定例会議体の設定
   └─ コミュニケーションチャネル確立
   └─ 権限・責任の明確化

2. 情報共有
   └─ グローバル方針の共有
   └─ 地域インサイトの収集
   └─ ベストプラクティス共有
   └─ 課題・リスクの共有

3. 協業実行
   └─ 共同キャンペーン企画
   └─ リソース調整
   └─ 予算調整
   └─ スケジュール調整

4. パフォーマンスレビュー
   └─ 地域KPIレビュー
   └─ 課題分析
   └─ 改善計画策定
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 地域マーケティングチームとの定例会議は月次で必須 |
| BR-OP4-02 | 重要施策は地域本部長の承認を必須とする |
| BR-OP4-03 | 地域間のベストプラクティス共有を四半期で実施する |
| BR-OP4-04 | 緊急対応時は24時間以内に関係者へ連絡する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| グローバル方針 | 地域連携計画 |
| 地域インサイト | 共同施策計画 |
| 各地域レポート | 統合レポート |

**トリガー:**
- 月次定例
- グローバル施策開始
- 緊急対応（ブランド危機等）
- 四半期レビュー

---

#### OP5: ブランドローカライゼーション

**業務フロー:**
```
1. ローカライゼーション要件定義
   └─ 対象ブランド・市場の特定
   └─ 適応レベルの決定
   └─ 優先順位付け

2. ガイドライン策定
   └─ 言語ローカライゼーションガイドライン
   └─ ビジュアル適応ガイドライン
   └─ トーン&マナーガイドライン
   └─ 禁止事項リスト

3. ローカライゼーション実行
   └─ 翻訳・トランスクリエーション
   └─ ビジュアル適応制作
   └─ 品質チェック
   └─ 承認取得

4. ローカライズ資産管理
   └─ ローカライズ版の登録
   └─ バージョン管理
   └─ 使用状況追跡
   └─ 更新管理
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | ブランド名のローカライズは原則禁止（例外は本部承認要） |
| BR-OP5-02 | ローカライズ資産はbrand-asset-governance-bcに登録必須 |
| BR-OP5-03 | 現地語キャッチコピーはネイティブスピーカーの確認を必須とする |
| BR-OP5-04 | 文化的禁忌（宗教、政治等）のチェックを必須とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| グローバルブランド資産 | ローカライゼーションガイドライン |
| 現地文化情報 | ローカライズ版資産 |
| 法規制情報 | ローカライズ品質レポート |

**トリガー:**
- 新市場展開
- グローバル資産更新
- ローカル法規制変更
- ブランドリニューアル

---

### 3. ユビキタス言語（Ubiquitous Language）

#### 地域戦略用語

| 用語 | 定義 |
|------|------|
| **Glocal（グローカル）** | Global + Localの造語。グローバル戦略を維持しながら、ローカル実行を最適化するアプローチ |
| **Regional Strategy（地域戦略）** | 特定地域（欧州、アジアパシフィック等）向けのブランド展開戦略 |
| **Local Adaptation（ローカル適応）** | グローバル施策を現地市場に合わせて調整すること |
| **Cross-Border Expansion（クロスボーダー展開）** | ブランドを新しい国・地域に展開すること |
| **Regional Portfolio（地域ポートフォリオ）** | 特定地域内でのブランド群の構成と配置 |

#### 欧州ブランド用語

| 用語 | 定義 |
|------|------|
| **Peroni Nastro Azzurro** | イタリア発祥のプレミアムラガー。「イタリアンスタイル」を体現 |
| **Grolsch** | オランダ発祥のプレミアムラガー。独自のスイングトップボトルが特徴 |
| **Pilsner Urquell** | チェコ発祥の元祖ピルスナー。1842年創業の歴史的ブランド |
| **Kozel** | チェコ発祥のラガービール。親しみやすい価格帯のブランド |
| **Heritage Brand（ヘリテージブランド）** | 歴史・伝統を価値の源泉とするブランド |

#### ローカライゼーション用語

| 用語 | 定義 |
|------|------|
| **Transcreation（トランスクリエーション）** | 翻訳を超えた創造的適応。意味・感情を現地文化に合わせて再創造 |
| **Localization（ローカライゼーション）** | コンテンツを現地市場向けに適応させるプロセス |
| **Cultural Adaptation（文化的適応）** | 現地の文化・価値観に合わせた調整 |
| **Tone & Manner（トーン&マナー）** | ブランドコミュニケーションの語調と表現スタイル |
| **Regulatory Compliance（規制遵守）** | 現地のアルコール広告規制等への適合 |

#### 3リージョン戦略用語

| 用語 | 定義 |
|------|------|
| **Japan/East Asia Region（日本・東アジア地域）** | 日本、韓国、中国等を含む地域。Asahi Super Dryの本拠地 |
| **Europe Region（欧州地域）** | 欧州市場。Peroni、Grolsch、Pilsner Urquell等のホームマーケット |
| **Asia Pacific Region（アジアパシフィック地域）** | 東南アジア、オーストラリア等を含む成長市場 |
| **Regional Hub（地域ハブ）** | 地域マーケティング活動の拠点 |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: RegionalBrandStrategy（地域ブランド戦略）

**責務**: 地域ブランド戦略のライフサイクル管理

```
RegionalBrandStrategy [Aggregate Root]
├── strategyId: RegionalStrategyId [Value Object]
├── region: Region [Value Object]
│   └── value: enum (EUROPE, ASIA_PACIFIC, JAPAN_EAST_ASIA)
├── targetBrands: BrandReference[] [Value Object]
│   ├── brandId: BrandId
│   └── brandName: BrandName (Peroni, Grolsch, etc.)
├── positioningStrategy: RegionalPositioning [Value Object]
│   ├── targetSegment: SegmentDefinition
│   ├── valueProposition: string
│   ├── pricePosition: PricePosition (PREMIUM, SUPER_PREMIUM)
│   └── differentiators: string[]
├── investmentPlan: RegionalInvestment [Entity]
│   ├── fiscalYear: FiscalYear
│   ├── totalBudget: Money
│   ├── allocationByBrand: Map<BrandId, Money>
│   └── allocationByChannel: Map<Channel, Money>
├── kpis: RegionalKPI[] [Entity]
│   ├── kpiName: string
│   ├── target: number
│   ├── actual: number?
│   └── period: Period
├── status: StrategyStatus [Value Object]
│   └── value: enum (DRAFT, UNDER_REVIEW, APPROVED, ACTIVE, ARCHIVED)
├── approvals: StrategyApproval[] [Entity]
│   ├── approverRole: ApproverRole
│   ├── approvedBy: UserId
│   └── approvedAt: Date
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-RS-01 | APPROVED状態への遷移には地域本部長承認を必須とする |
| INV-RS-02 | targetBrandsは最低1ブランドを含む |
| INV-RS-03 | investmentPlanの合計はtotalBudgetと一致する |
| INV-RS-04 | ACTIVE状態の戦略は同一region・fiscalYearで1件のみ |

---

#### 集約2: LocalBrandPositioning（ローカルブランドポジショニング）

**責務**: 各市場でのブランドポジショニング管理

```
LocalBrandPositioning [Aggregate Root]
├── positioningId: PositioningId [Value Object]
├── brandId: BrandId [Value Object]
├── market: Market [Value Object]
│   ├── country: CountryCode
│   └── region: Region
├── globalAlignment: GlobalAlignmentReference [Value Object]
│   └── globalPositioningId: PositioningId
├── localPositioning: LocalPositioningSpec [Value Object]
│   ├── localTargetSegment: SegmentDefinition
│   ├── localValueProposition: string
│   ├── localMessaging: MessagingGuideline
│   └── localPricePosition: PricePosition
├── culturalAdaptations: CulturalAdaptation[] [Entity]
│   ├── adaptationType: AdaptationType
│   ├── originalElement: string
│   ├── adaptedElement: string
│   └── rationale: string
├── competitiveContext: CompetitiveContext [Entity]
│   ├── mainCompetitors: Competitor[]
│   └── differentiationPoints: string[]
├── validationResults: ValidationResult[] [Entity]
│   ├── testType: TestType (CONSUMER_TEST, FOCUS_GROUP)
│   ├── testDate: Date
│   ├── results: TestResults
│   └── passed: boolean
├── status: PositioningStatus [Value Object]
│   └── value: enum (DRAFT, TESTING, APPROVED, ACTIVE, DEPRECATED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-LP-01 | APPROVED状態への遷移には消費者テスト結果(passed=true)を必須とする |
| INV-LP-02 | globalAlignmentは有効なグローバルポジショニングを参照する |
| INV-LP-03 | pricePositionはPREMIUM以上を維持する |
| INV-LP-04 | 同一brandId・marketでACTIVE状態は1件のみ |

---

#### 集約3: RegionalCampaign（地域キャンペーン）

**責務**: 地域別キャンペーンの計画・実行管理

```
RegionalCampaign [Aggregate Root]
├── campaignId: RegionalCampaignId [Value Object]
├── globalCampaignRef: GlobalCampaignReference [Value Object]
│   └── globalCampaignId: CampaignId?
├── region: Region [Value Object]
├── targetMarkets: Market[] [Value Object]
├── campaignSpec: CampaignSpec [Value Object]
│   ├── name: CampaignName
│   ├── objective: string
│   ├── startDate: Date
│   ├── endDate: Date
│   └── budget: Money
├── localAdaptation: LocalAdaptation [Entity]
│   ├── creativeAdaptations: CreativeAdaptation[]
│   ├── messagingAdaptations: MessagingAdaptation[]
│   ├── mediaAdaptations: MediaAdaptation[]
│   └── regulatoryAdjustments: RegulatoryAdjustment[]
├── localCreatives: LocalCreative[] [Entity]
│   ├── creativeId: CreativeId
│   ├── type: CreativeType
│   ├── language: LanguageCode
│   ├── assetUrl: URL
│   └── approvalStatus: ApprovalStatus
├── mediaPlanning: RegionalMediaPlan [Entity]
│   ├── channels: MediaChannel[]
│   ├── spend: Money
│   └── schedule: MediaSchedule
├── performance: CampaignPerformance [Entity]
│   ├── reach: number
│   ├── impressions: number
│   ├── engagement: number
│   └── roi: number?
├── status: CampaignStatus [Value Object]
│   └── value: enum (PLANNING, APPROVED, LIVE, COMPLETED, CANCELLED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-RC-01 | LIVE状態への遷移にはlocalCreativesの全承認を必須とする |
| INV-RC-02 | regulatoryAdjustmentsは対象市場の規制を100%遵守する |
| INV-RC-03 | globalCampaignRefがある場合、コア要素は変更不可 |
| INV-RC-04 | COMPLETED状態への遷移にはperformanceデータを必須とする |

---

#### 集約4: LocalizationGuideline（ローカライゼーションガイドライン）

**責務**: ブランドローカライゼーションガイドラインの管理

```
LocalizationGuideline [Aggregate Root]
├── guidelineId: GuidelineId [Value Object]
├── brandId: BrandId [Value Object]
├── targetMarket: Market [Value Object]
├── languageGuidelines: LanguageGuideline [Entity]
│   ├── primaryLanguage: LanguageCode
│   ├── translationGuidelines: TranslationRule[]
│   ├── forbiddenTerms: ForbiddenTerm[]
│   ├── preferredTerminology: TerminologyMap
│   └── toneOfVoice: ToneSpec
├── visualGuidelines: VisualGuideline [Entity]
│   ├── colorAdaptations: ColorAdaptation[]
│   ├── imageryGuidelines: ImageryRule[]
│   ├── layoutAdaptations: LayoutRule[]
│   └── localIconography: IconographySpec
├── culturalGuidelines: CulturalGuideline [Entity]
│   ├── culturalSensitivities: Sensitivity[]
│   ├── forbiddenSymbols: Symbol[]
│   ├── localCelebrations: Celebration[]
│   └── religiousConsiderations: Consideration[]
├── regulatoryGuidelines: RegulatoryGuideline [Entity]
│   ├── advertisingRestrictions: Restriction[]
│   ├── requiredDisclaimer: Disclaimer[]
│   ├── ageRestrictionRules: AgeRule[]
│   └── packagingRequirements: PackagingRule[]
├── version: Version [Value Object]
├── status: GuidelineStatus [Value Object]
│   └── value: enum (DRAFT, APPROVED, ACTIVE, DEPRECATED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-LG-01 | ACTIVE状態への遷移にはbrand-asset-governance-bcの承認を必須とする |
| INV-LG-02 | regulatoryGuidelinesは最新法規制を反映する |
| INV-LG-03 | 同一brandId・targetMarketでACTIVE状態は1件のみ |
| INV-LG-04 | version更新時は変更履歴を記録する |

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **RegionalStrategyApproved** | {strategyId, region, targetBrands, approvedBy, approvedAt} | 地域戦略承認時 | campaign-communications-bc, brand-experience-bc |
| **LocalPositioningActivated** | {positioningId, brandId, market, activatedAt} | ローカルポジショニング有効化時 | campaign-communications-bc |
| **RegionalCampaignLaunched** | {campaignId, region, targetMarkets, startDate} | 地域キャンペーン開始時 | digital-marketing-bc, brand-experience-bc |
| **RegionalCampaignCompleted** | {campaignId, region, performance, completedAt} | 地域キャンペーン終了時 | marketing-analytics-bc |
| **LocalizationGuidelinePublished** | {guidelineId, brandId, targetMarket, version} | ローカライゼーションガイドライン発行時 | brand-asset-governance-bc |
| **CrossBorderExpansionInitiated** | {brandId, sourceMarket, targetMarket, initiatedAt} | クロスボーダー展開開始時 | brand-strategy-bc, VS4販売・流通 |

---

### 6. コンテキストマップ（Context Map）

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    │        brand-strategy-bc             │
                    │          (Upstream)                  │
                    │                                      │
                    │  グローバルブランド戦略方針提供      │
                    └──────────────┬───────────────────────┘
                                   │ グローバル戦略・Glocal方針
                                   ▼
┌─────────────────┐    ┌──────────────────────────────────┐    ┌─────────────────┐
│ brand-asset-    │    │                                  │    │ campaign-       │
│ governance-bc   │───►│  regional-brand-activation-bc    │───►│ communications  │
│ (Upstream)      │    │                                  │    │ -bc             │
│                 │    │  ※このBC                         │    │ (Downstream)    │
│ ブランド資産・  │    │                                  │    │                 │
│ ガイドライン    │    └──────────────┬───────────────────┘    │ 地域キャンペーン│
│ 提供            │                   │                        │ 方針受領        │
└─────────────────┘                   │                        └─────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ digital-        │    │ brand-          │    │ marketing-      │
│ marketing-bc    │    │ experience-bc   │    │ analytics-bc    │
│ (Downstream)    │    │ (Downstream)    │    │ (Downstream)    │
│                 │    │                 │    │                 │
│ デジタル施策    │    │ 地域イベント    │    │ 地域KPIデータ   │
│ 連携            │    │ 方針受領        │    │ 提供            │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                            │
         │                            │
         ▼                            ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    VS4: 販売・流通                           │
│                    (Partnership)                            │
│                                                             │
│                 地域チャネル戦略連携                        │
└─────────────────────────────────────────────────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| brand-strategy-bc | **Conformist** | グローバルブランド戦略に準拠する |
| brand-asset-governance-bc | **Customer-Supplier** | ブランド資産・ガイドラインの供給を受ける |
| campaign-communications-bc | **Customer-Supplier** | 地域キャンペーン方針を提供する |
| digital-marketing-bc | **Customer-Supplier** | デジタル施策連携のための方針を提供する |
| brand-experience-bc | **Customer-Supplier** | 地域イベント方針を提供する |
| marketing-analytics-bc | **Customer-Supplier** | 地域KPIデータを提供する |
| VS4販売・流通 | **Partnership** | 地域チャネル戦略で対等に協力 |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/regional-strategies` | POST | 新規地域戦略作成 |
| `/regional-strategies/{id}/approve` | POST | 地域戦略承認 |
| `/regional-strategies/{id}/activate` | POST | 地域戦略有効化 |
| `/local-positionings` | POST | ローカルポジショニング作成 |
| `/local-positionings/{id}/activate` | POST | ローカルポジショニング有効化 |
| `/regional-campaigns` | POST | 地域キャンペーン作成 |
| `/regional-campaigns/{id}/approve` | POST | 地域キャンペーン承認 |
| `/regional-campaigns/{id}/launch` | POST | 地域キャンペーン開始 |
| `/regional-campaigns/{id}/complete` | POST | 地域キャンペーン終了・効果登録 |
| `/localization-guidelines` | POST | ローカライゼーションガイドライン作成 |
| `/localization-guidelines/{id}/publish` | POST | ガイドライン発行 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/regional-strategies` | GET | 地域戦略一覧（region, year, statusでフィルタ可） |
| `/regional-strategies/{id}` | GET | 地域戦略詳細 |
| `/local-positionings` | GET | ローカルポジショニング一覧 |
| `/local-positionings/{id}` | GET | ローカルポジショニング詳細 |
| `/regional-campaigns` | GET | 地域キャンペーン一覧 |
| `/regional-campaigns/{id}` | GET | 地域キャンペーン詳細 |
| `/regional-campaigns/{id}/performance` | GET | キャンペーン効果データ |
| `/localization-guidelines` | GET | ガイドライン一覧 |
| `/localization-guidelines/{id}` | GET | ガイドライン詳細 |
| `/brands/{brandId}/regional-info` | GET | ブランド地域展開情報 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| brand-strategy-bc | グローバルブランド戦略・ポジショニング参照 |
| brand-asset-governance-bc | ブランド資産・ガイドライン参照、承認依頼 |
| VS1市場機会発見 | 地域市場調査データ参照 |

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（regional-brand-activation-bc定義）
