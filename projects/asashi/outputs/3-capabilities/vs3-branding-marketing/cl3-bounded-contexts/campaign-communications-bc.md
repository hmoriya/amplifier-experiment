# Bounded Context: campaign-communications-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** campaign-communications（キャンペーンコミュニケーション）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | campaign-communications-bc |
| **日本語名** | キャンペーンコミュニケーション |
| **命名パターン** | `-communications`（発信型） |
| **命名理由** | 「キャンペーン管理」ではなく「コミュニケーション」を採用。消費者インサイトに基づく統合マーケティングコミュニケーション（IMC）の**対話・発信**という能動的活動を表現。Asahi Super Dry、Peroni等のグローバルブランドメッセージを一貫性をもって消費者に届ける戦略的コミュニケーション活動を強調 |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**campaign-communications-bc**（キャンペーンコミュニケーションバウンデッドコンテキスト）

#### 目的
消費者インサイトに基づく統合マーケティングキャンペーンを企画・実行し、ブランドメッセージを一貫性をもって消費者に届ける。グローバル/リージョナル双方のキャンペーンを統合的に管理し、オンライン・オフラインのタッチポイントを横断した効果的なコミュニケーションを実現する。

#### 責務
- ターゲットセグメント定義・ペルソナ開発
- キャンペーン企画・設計（グローバル/リージョナル）
- クリエイティブ開発・制作ディレクション
- メディアプランニング・バイイング
- タッチポイント統合（IMC実行）
- キャンペーン効果測定・最適化

#### チーム境界
- **担当組織**: マーケティング本部 コミュニケーション部門
- **チーム構成**:
  - インサイトチーム（マーケットリサーチャー、データアナリスト）
  - キャンペーンプランナー（IMCストラテジスト、プロジェクトマネージャー）
  - クリエイティブチーム（クリエイティブディレクター、プロデューサー）
  - メディアチーム（メディアプランナー、バイヤー）
  - 効果測定チーム（マーケティングアナリスト）
- **推定人員**: 60-100名（グローバル含む）

---

### 2. ビジネスオペレーション詳細

#### OP1: ターゲットセグメント定義・ペルソナ開発

**業務フロー:**
```
1. 消費者インサイト収集
   └─ VS1市場機会発見からのインサイト受領
   └─ 定量調査データ分析（認知度、購買意向等）
   └─ 定性調査データ分析（インタビュー、FGI）

2. セグメンテーション実施
   └─ デモグラフィック分析（年齢、性別、地域等）
   └─ サイコグラフィック分析（価値観、ライフスタイル）
   └─ 行動分析（購買頻度、チャネル選好）

3. ペルソナ開発
   └─ 主要セグメント向けペルソナ作成
   └─ ペルソナストーリー・シナリオ作成
   └─ カスタマージャーニーマップ作成

4. 承認・共有
   └─ ブランド戦略チームレビュー
   └─ ペルソナDBへの登録
   └─ 関連チームへの共有
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | ペルソナは最低年1回見直しを実施すること |
| BR-OP1-02 | 主要ブランドにつき3-5個のペルソナを定義すること |
| BR-OP1-03 | ペルソナにはデモグラフィック・サイコグラフィック・行動特性を含めること |
| BR-OP1-04 | Z世代向けペルソナは半年ごとに更新すること |
| BR-OP1-05 | グローバルブランドはグローバル共通ペルソナ＋地域別ペルソナの2層構造とすること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 市場調査データ | セグメント定義書 |
| 消費者インサイト | ペルソナシート |
| 購買データ | カスタマージャーニーマップ |

**トリガー:**
- 年次マーケティング計画策定
- 新製品発売準備
- 市場環境の大きな変化

---

#### OP2: キャンペーン企画・設計

**業務フロー:**
```
1. ブリーフィング
   └─ ビジネス目標の確認（売上、シェア等）
   └─ ブランド戦略との整合確認
   └─ ターゲットペルソナの選定
   └─ 予算・期間の確定

2. 戦略策定
   └─ コミュニケーション目標設定（認知、理解、購買意向等）
   └─ キーメッセージ策定
   └─ クリエイティブコンセプト開発
   └─ タッチポイント設計

3. 企画書作成
   └─ キャンペーン企画書の作成
   └─ メディアプラン素案作成
   └─ KPI設定

4. 承認プロセス
   └─ 部門内レビュー
   └─ brand-strategyによるブランド適合性確認
   └─ 予算承認
   └─ 企画確定・登録
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | 全キャンペーンはブランドガイドラインに準拠すること |
| BR-OP2-02 | グローバルブランドキャンペーンはグローバル本部承認が必要 |
| BR-OP2-03 | 1億円以上のキャンペーンは役員承認が必要 |
| BR-OP2-04 | 責任ある飲酒に関するガイドラインを遵守すること |
| BR-OP2-05 | 全キャンペーンにKPIを3つ以上設定すること |
| BR-OP2-06 | リージョナルキャンペーンはローカル適応ガイドに従うこと |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ブランド戦略方針 | キャンペーン企画書 |
| ペルソナ・セグメント情報 | メディアプラン素案 |
| 予算枠 | KPI設計書 |
| 製品情報（VS2より） | 実行スケジュール |

**トリガー:**
- 製品発売（新製品、リニューアル）
- 季節イベント（夏、年末年始等）
- スポンサーシップイベント（ラグビーW杯等）
- 競合動向への対応

---

#### OP3: クリエイティブ開発・制作

**業務フロー:**
```
1. クリエイティブブリーフ作成
   └─ キャンペーンコンセプトの落とし込み
   └─ 必須要素（ロゴ、タグライン、法的表示）の確認
   └─ 制作物一覧・仕様の確定

2. クリエイティブ開発
   └─ 社内/代理店によるコンセプト開発
   └─ 複数案の作成・プレゼンテーション
   └─ コンセプト決定

3. 制作実行
   └─ TV-CM撮影・編集
   └─ デジタル広告制作
   └─ 印刷物・POP制作
   └─ 各種素材のローカライズ（多言語対応）

4. 承認・納品
   └─ 法務チェック（景表法、酒類広告基準）
   └─ ブランド適合性チェック
   └─ 最終承認
   └─ クリエイティブライブラリへの登録
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 全クリエイティブは法務チェックを経ること |
| BR-OP3-02 | TV-CMは放送基準審査を通過すること |
| BR-OP3-03 | 酒類広告基準（未成年者への配慮等）を遵守すること |
| BR-OP3-04 | ブランドロゴはガイドライン通りに使用すること |
| BR-OP3-05 | 制作物はDAMに登録し、メタデータを付与すること |
| BR-OP3-06 | グローバルキャンペーンは最低英語・日本語の2言語を用意すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| キャンペーン企画書 | クリエイティブコンセプト |
| ブランドガイドライン | TV-CM素材 |
| 製品ビジュアル | デジタル広告素材 |
| ローカル適応ガイド | 印刷物・POP |

**トリガー:**
- キャンペーン企画確定
- クリエイティブ更新要求

---

#### OP4: メディアプランニング・バイイング

**業務フロー:**
```
1. メディア戦略策定
   └─ ターゲットリーチ分析
   └─ メディア特性評価
   └─ メディアミックス設計

2. メディアプラン作成
   └─ 媒体選定（TV、デジタル、OOH、雑誌等）
   └─ GRP/インプレッション目標設定
   └─ 予算配分
   └─ 出稿スケジュール作成

3. メディアバイイング
   └─ 媒体社・代理店との交渉
   └─ 枠確保・契約締結
   └─ 広告入稿

4. 運用・最適化
   └─ 配信開始・モニタリング
   └─ 効果データに基づく配信調整
   └─ デジタル広告のリアルタイム最適化
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 媒体選定はターゲットペルソナのメディア接触データに基づくこと |
| BR-OP4-02 | デジタル媒体比率は最低40%以上を目安とすること |
| BR-OP4-03 | メディアプランは効果測定可能な設計とすること |
| BR-OP4-04 | 出稿データは日次で記録すること |
| BR-OP4-05 | 1,000万円以上の単一媒体契約は複数見積もりを取得すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| キャンペーン企画書 | メディアプラン |
| 予算 | 媒体契約 |
| ターゲットペルソナ | 出稿スケジュール |
| 過去効果データ | 配信実績データ |

**トリガー:**
- キャンペーン企画確定
- 予算変更
- 効果不振時の調整要求

---

#### OP5: タッチポイント統合（IMC実行）

**業務フロー:**
```
1. 統合計画策定
   └─ 全タッチポイントの洗い出し
   └─ カスタマージャーニー上の配置
   └─ メッセージ一貫性の確認

2. 実行準備
   └─ 各チャネル担当との調整
   └─ スケジュール同期
   └─ コンテンツ・素材の配布

3. 同時展開実行
   └─ TV-CM放映開始
   └─ デジタル広告配信開始
   └─ 店頭プロモーション開始
   └─ SNSキャンペーン開始
   └─ イベント実施

4. 統合モニタリング
   └─ 各チャネルの進捗確認
   └─ 問題発生時の調整
   └─ 日次/週次報告
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | 主要タッチポイントは同一週内に開始すること |
| BR-OP5-02 | 全チャネルで一貫したキービジュアル・メッセージを使用すること |
| BR-OP5-03 | digital-marketing-bcとの連携スケジュールを事前に合意すること |
| BR-OP5-04 | brand-experience-bcイベントとの連動を計画すること |
| BR-OP5-05 | 日次進捗レポートを作成すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| メディアプラン | 統合実行計画 |
| クリエイティブ素材 | チャネル別進捗報告 |
| イベント計画（brand-experience） | 統合キャンペーンレポート |

**トリガー:**
- キャンペーン実行開始日
- イベント連動タイミング

---

#### OP6: キャンペーン効果測定

**業務フロー:**
```
1. 測定計画策定
   └─ 測定KPIの確認
   └─ 測定手法の選定（アンケート、アクセス解析、売上データ等）
   └─ 調査設計

2. データ収集
   └─ 広告効果調査実施
   └─ デジタルデータ収集
   └─ 売上データ収集（VS4より）
   └─ ブランドリフト調査

3. 分析・評価
   └─ KPI達成度分析
   └─ チャネル別効果分析
   └─ ROI算出
   └─ 課題・成功要因の特定

4. 報告・活用
   └─ 効果測定レポート作成
   └─ 関係者への報告
   └─ ナレッジ蓄積（成功事例・失敗事例）
   └─ 次回キャンペーンへの示唆
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP6-01 | 全キャンペーンは終了後2週間以内に速報を作成すること |
| BR-OP6-02 | 1億円以上のキャンペーンは外部調査を含めた詳細分析を実施すること |
| BR-OP6-03 | 効果測定レポートはmarketing-analytics-bcに提供すること |
| BR-OP6-04 | ROIは統一基準で算出すること |
| BR-OP6-05 | 失敗事例も含めナレッジDBに記録すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| キャンペーンKPI | 効果測定レポート |
| 配信実績データ | ROI分析結果 |
| 売上データ | ナレッジ記録 |
| 調査データ | 次回施策提案 |

**トリガー:**
- キャンペーン終了
- 中間レビュータイミング
- 経営報告要求

---

### 3. ユビキタス言語（Ubiquitous Language）

#### ドメインオブジェクト（業務で扱うモノ・コト）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| Persona | ペルソナ | ターゲット消費者を代表する架空の人物像。デモグラフィック・サイコグラフィック・行動特性を含む |
| Segment | セグメント | 共通の特性を持つ消費者グループ |
| Campaign | キャンペーン | 特定の目的・期間で実施する統合マーケティング活動 |
| CampaignBrief | キャンペーンブリーフ | キャンペーンの目的・ターゲット・予算等を定義した文書 |
| CreativeAsset | クリエイティブ資産 | TV-CM、デジタル広告、印刷物等の広告素材 |
| MediaPlan | メディアプラン | 媒体選定・予算配分・出稿スケジュールをまとめた計画 |
| Touchpoint | タッチポイント | 消費者とブランドの接点（TV、デジタル、店頭、イベント等） |
| IMC | 統合マーケティングコミュニケーション | 全タッチポイントを統合した一貫性のあるコミュニケーション |

#### ビジネスルール（業務上の制約・ルール）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| BrandGuideline | ブランドガイドライン | ブランド表現の使用ルールを定めた文書 |
| ResponsibleDrinking | 責任ある飲酒 | 酒類広告における未成年者配慮等の自主基準 |
| LegalCompliance | 法務適合 | 景表法・酒類広告基準等の法的要件への適合 |
| GRP | 延べ視聴率 | TV広告の到達指標 |
| Impression | インプレッション | デジタル広告の表示回数 |
| ROI | 投資対効果 | 広告投資に対する売上・効果の比率 |

#### プロセス（業務フロー）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| InsightGathering | インサイト収集 | 消費者理解のためのデータ・情報収集プロセス |
| CreativeDevelopment | クリエイティブ開発 | 広告コンセプト・素材を開発するプロセス |
| MediaBuying | メディアバイイング | 広告枠を購入・契約するプロセス |
| IMCExecution | IMC実行 | 統合キャンペーンを各チャネルで同時展開するプロセス |
| EffectivenessMeasurement | 効果測定 | キャンペーン効果を測定・分析するプロセス |
| Localization | ローカライゼーション | グローバル素材を地域市場向けに適応させるプロセス |

#### イベント（業務上の重要な出来事）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| CampaignApproved | キャンペーン承認 | キャンペーン企画が承認された |
| CampaignLaunched | キャンペーン開始 | キャンペーンが全タッチポイントで開始された |
| CampaignCompleted | キャンペーン終了 | キャンペーン期間が終了した |
| CreativeApproved | クリエイティブ承認 | 広告素材が法務・ブランドチェックを通過した |
| EffectivenessReported | 効果報告完了 | 効果測定レポートが作成・共有された |
| PersonaUpdated | ペルソナ更新 | ターゲットペルソナが更新された |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: Campaign（キャンペーン）

**責務**: キャンペーンのライフサイクル管理

```
Campaign [Aggregate Root]
├── campaignId: CampaignId [Value Object]
│   └── format: "CMP-YYYY-NNNN"
├── name: string
├── brandId: BrandId [Value Object] (brand-strategyからの参照)
├── scope: CampaignScope [Value Object]
│   └── value: enum (GLOBAL, REGIONAL, LOCAL)
├── regions: Region[] [Value Object]
│   └── value: enum (JAPAN, EUROPE, OCEANIA, APAC)
├── brief: CampaignBrief [Entity]
│   ├── objective: string
│   ├── targetPersonas: PersonaId[]
│   ├── keyMessage: string
│   ├── period: DateRange
│   ├── budget: Budget
│   │   ├── amount: Money
│   │   └── allocation: BudgetAllocation[]
│   └── kpis: KPI[]
│       ├── metric: enum (AWARENESS, CONSIDERATION, PURCHASE_INTENT, SALES)
│       ├── target: number
│       └── unit: string
├── creatives: CreativeAsset[] [Entity]
│   ├── assetId: AssetId
│   ├── type: enum (TV_CM, DIGITAL_VIDEO, DISPLAY, PRINT, OOH, SNS)
│   ├── format: string
│   ├── status: enum (DRAFT, UNDER_REVIEW, APPROVED, ACTIVE, ARCHIVED)
│   ├── legalApproval: LegalApproval
│   └── languages: Language[]
├── mediaPlan: MediaPlan [Entity]
│   ├── channels: MediaChannel[]
│   │   ├── channel: enum (TV, DIGITAL, OOH, PRINT, RADIO)
│   │   ├── budget: Money
│   │   ├── targetGRP: number?
│   │   └── targetImpressions: number?
│   ├── schedule: PublishingSchedule[]
│   └── buyingStatus: enum (PLANNED, NEGOTIATING, CONFIRMED, EXECUTING)
├── status: CampaignStatus [Value Object]
│   └── value: enum (DRAFT, APPROVED, PREPARING, LIVE, COMPLETED, CANCELLED)
├── effectiveness: EffectivenessSummary [Entity]
│   ├── kpiResults: KPIResult[]
│   ├── roi: number?
│   └── reportUrl: string?
└── audit: AuditTrail [Value Object]
    ├── createdAt: Date
    ├── createdBy: UserId
    ├── modifiedAt: Date
    └── modifiedBy: UserId
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-CM-01 | campaignIdは一意でCMP-YYYY-NNNN形式であること |
| INV-CM-02 | APPROVEDステータスにはbriefの全必須項目が完了していること |
| INV-CM-03 | LIVEステータスには最低1つのAPPROVEDクリエイティブが必要 |
| INV-CM-04 | 予算合計はbriefのbudgetを超えないこと |
| INV-CM-05 | GLOBALスコープのキャンペーンは最低2つのregionを含むこと |
| INV-CM-06 | 酒類キャンペーンはresponsibleDrinkingチェック済みであること |

**主要メソッド:**
```
- createCampaign(name, brandId, scope, brief): Campaign
- addCreative(type, format, languages): CreativeAsset
- approveCreative(assetId, legalApproval): void
- setMediaPlan(mediaPlan): void
- launchCampaign(): void
- completeCampaign(effectivenessData): void
- cancelCampaign(reason): void
```

---

#### 集約2: Persona（ペルソナ）

**責務**: ターゲットペルソナの定義・管理

```
Persona [Aggregate Root]
├── personaId: PersonaId [Value Object]
│   └── format: "PRS-BRAND-NNN"
├── name: string (例: "健康志向ミドル佐藤さん")
├── brandId: BrandId [Value Object]
├── scope: PersonaScope [Value Object]
│   └── value: enum (GLOBAL, REGIONAL, LOCAL)
├── demographics: Demographics [Value Object]
│   ├── ageRange: Range
│   ├── gender: enum (MALE, FEMALE, ALL)
│   ├── occupation: string[]
│   ├── income: IncomeLevel
│   └── location: string[]
├── psychographics: Psychographics [Value Object]
│   ├── values: string[]
│   ├── lifestyle: string[]
│   ├── interests: string[]
│   └── mediaHabits: MediaHabit[]
├── behavior: BehaviorPattern [Value Object]
│   ├── purchaseFrequency: enum (HEAVY, MEDIUM, LIGHT, NON_USER)
│   ├── preferredChannels: Channel[]
│   ├── decisionFactors: string[]
│   └── brandPerception: string
├── customerJourney: CustomerJourney [Entity]
│   ├── stages: JourneyStage[]
│   │   ├── stage: enum (AWARENESS, INTEREST, CONSIDERATION, PURCHASE, LOYALTY)
│   │   ├── touchpoints: Touchpoint[]
│   │   └── painPoints: string[]
│   └── keyMoments: KeyMoment[]
├── status: PersonaStatus [Value Object]
│   └── value: enum (ACTIVE, DEPRECATED, DRAFT)
├── validUntil: Date
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-PS-01 | personaIdは一意でPRS-BRAND-NNN形式であること |
| INV-PS-02 | ACTIVEペルソナはvalidUntilが未来日であること |
| INV-PS-03 | customerJourneyは最低3つのstageを含むこと |
| INV-PS-04 | GLOBALスコープペルソナはローカルペルソナの親として参照可能であること |

**主要メソッド:**
```
- createPersona(name, brandId, scope, demographics, psychographics): Persona
- updateDemographics(demographics): void
- updatePsychographics(psychographics): void
- setBehaviorPattern(behavior): void
- mapCustomerJourney(journey): void
- deprecate(replacementPersonaId?): void
- extend(validUntil): void
```

---

#### 集約3: CreativeLibrary（クリエイティブライブラリ）

**責務**: クリエイティブ資産の一元管理

```
CreativeLibrary [Aggregate Root]
├── libraryId: LibraryId [Value Object]
├── brandId: BrandId [Value Object]
├── assets: CreativeAssetEntry[] [Entity]
│   ├── assetId: AssetId
│   ├── campaignId: CampaignId?
│   ├── type: CreativeType
│   ├── title: string
│   ├── description: string
│   ├── fileUrl: string
│   ├── thumbnail: string
│   ├── metadata: AssetMetadata
│   │   ├── format: string
│   │   ├── resolution: string?
│   │   ├── duration: number? (動画の場合)
│   │   ├── languages: Language[]
│   │   └── usageRights: UsageRights
│   ├── status: enum (ACTIVE, ARCHIVED, EXPIRED)
│   ├── expirationDate: Date?
│   └── tags: Tag[]
├── categories: Category[] [Value Object]
└── accessControl: AccessControl [Value Object]
    ├── publicAccess: boolean
    └── allowedRegions: Region[]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-CL-01 | 全assetにはfileUrlとthumbnailが存在すること |
| INV-CL-02 | ACTIVE資産は有効期限内であること |
| INV-CL-03 | 各assetには最低1つのtagが付与されていること |
| INV-CL-04 | usageRightsは法務承認済みであること |

**主要メソッド:**
```
- registerAsset(campaignId, type, title, fileUrl, metadata): CreativeAssetEntry
- updateMetadata(assetId, metadata): void
- archiveAsset(assetId): void
- searchAssets(criteria): CreativeAssetEntry[]
- getAssetsByCampaign(campaignId): CreativeAssetEntry[]
```

---

#### 集約4: MediaExecution（メディア実行）

**責務**: メディア出稿の実行・実績管理

```
MediaExecution [Aggregate Root]
├── executionId: ExecutionId [Value Object]
├── campaignId: CampaignId [Value Object]
├── mediaPlanId: MediaPlanId [Value Object]
├── channels: ChannelExecution[] [Entity]
│   ├── channel: enum (TV, DIGITAL, OOH, PRINT, RADIO)
│   ├── vendor: string
│   ├── contract: ContractInfo
│   │   ├── contractId: string
│   │   ├── amount: Money
│   │   └── period: DateRange
│   ├── placements: Placement[]
│   │   ├── placementId: PlacementId
│   │   ├── spot: string (枠情報)
│   │   ├── scheduledDate: Date
│   │   ├── actualDate: Date?
│   │   ├── creativeAssetId: AssetId
│   │   └── status: enum (SCHEDULED, DELIVERED, FAILED)
│   └── performance: ChannelPerformance
│       ├── impressions: number
│       ├── reach: number
│       ├── grp: number? (TVの場合)
│       ├── clicks: number? (デジタルの場合)
│       └── ctr: number? (デジタルの場合)
├── totalSpend: Money [Value Object]
├── status: ExecutionStatus [Value Object]
│   └── value: enum (PREPARING, EXECUTING, COMPLETED, SUSPENDED)
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-ME-01 | totalSpendはmediaPlan予算を超えないこと |
| INV-ME-02 | 全placementには有効なcreativeAssetIdが設定されていること |
| INV-ME-03 | COMPLETEDステータスには全placementがDELIVERED or FAILEDであること |

**主要メソッド:**
```
- createExecution(campaignId, mediaPlanId): MediaExecution
- addChannel(channel, vendor, contract): ChannelExecution
- schedulePlacement(channelId, spot, date, assetId): Placement
- confirmDelivery(placementId, actualDate): void
- updatePerformance(channelId, performance): void
- completeExecution(): void
```

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **CampaignCreated** | {campaignId, brandId, scope, regions, createdAt} | キャンペーン作成時 | digital-marketing-bc, brand-experience-bc |
| **CampaignApproved** | {campaignId, brief, approvedBy, approvedAt} | キャンペーン承認時 | regional-brand-activation-bc, marketing-analytics-bc |
| **CampaignLaunched** | {campaignId, channels, startDate, launchedAt} | キャンペーン開始時 | digital-marketing-bc, brand-experience-bc, consumer-engagement-bc |
| **CampaignCompleted** | {campaignId, effectiveness, roi, completedAt} | キャンペーン終了時 | marketing-analytics-bc, brand-strategy-bc |
| **CreativeApproved** | {assetId, campaignId, type, approvedAt} | クリエイティブ承認時 | brand-asset-governance-bc |
| **PersonaUpdated** | {personaId, brandId, scope, changes, updatedAt} | ペルソナ更新時 | digital-marketing-bc, consumer-engagement-bc |
| **MediaPerformanceRecorded** | {executionId, channelPerformance, recordedAt} | メディア実績記録時 | marketing-analytics-bc |

---

### 6. コンテキストマップ（Context Map）

```
                              ┌──────────────────────────────────────┐
                              │                                      │
                              │    brand-strategy-bc (Upstream)      │
                              │                                      │
                              └──────────────────┬───────────────────┘
                                                 │
                                    [Customer-Supplier]
                                                 │
                              ┌──────────────────▼───────────────────┐
                              │                                      │
                              │   campaign-communications-bc         │
                              │                                      │
                              │   • キャンペーン企画・実行           │
                              │   • クリエイティブ開発               │
                              │   • メディアプランニング             │
                              │   • IMC統合実行                      │
                              │                                      │
                              └───┬─────────────┬─────────────┬──────┘
                                  │             │             │
         ┌────────────────────────┼─────────────┼─────────────┼────────────────────┐
         │                        │             │             │                    │
         ▼                        ▼             ▼             ▼                    ▼
┌─────────────────┐    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  ┌─────────────────┐
│ digital-        │    │ brand-          │ │ brand-asset-    │ │ marketing-      │  │ consumer-       │
│ marketing-bc    │    │ experience-bc   │ │ governance-bc   │ │ analytics-bc    │  │ engagement-bc   │
│ (Downstream)    │    │ (Downstream)    │ │ (Shared Kernel) │ │ (Downstream)    │  │ (Downstream)    │
│                 │    │                 │ │                 │ │                 │  │                 │
│ [Partnership]   │    │ [Partnership]   │ │                 │ │ [Conformist]    │  │ [Customer-      │
│                 │    │                 │ │                 │ │                 │  │  Supplier]      │
└─────────────────┘    └─────────────────┘ └─────────────────┘ └─────────────────┘  └─────────────────┘

                              ┌──────────────────────────────────────┐
                              │                                      │
                              │  regional-brand-activation-bc        │
                              │           (Sibling)                  │
                              │                                      │
                              │  [Partnership] 地域キャンペーン連携   │
                              │                                      │
                              └──────────────────────────────────────┘

                    ┌─────────────────────────────────────────────────────────────┐
                    │                     External Systems                         │
                    │                                                             │
                    │  ┌──────────────────┐  ┌──────────────────┐                │
                    │  │ VS1 市場機会発見  │  │ VS2 製品開発     │                │
                    │  │ [Upstream]       │  │ [Upstream]       │                │
                    │  │ 消費者インサイト  │  │ 製品情報         │                │
                    │  └──────────────────┘  └──────────────────┘                │
                    │                                                             │
                    │  ┌──────────────────┐                                       │
                    │  │ VS4 販売・流通    │                                       │
                    │  │ [Downstream]     │                                       │
                    │  │ 店頭施策連携      │                                       │
                    │  └──────────────────┘                                       │
                    │                                                             │
                    └─────────────────────────────────────────────────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| brand-strategy-bc | **Customer-Supplier** | ブランド戦略方針・メッセージを受領。キャンペーン要件を伝達 |
| regional-brand-activation-bc | **Partnership** | グローバル/リージョナルキャンペーンで対等に協力 |
| digital-marketing-bc | **Partnership** | デジタル施策で密接に連携。タッチポイント統合 |
| brand-experience-bc | **Partnership** | イベント連動キャンペーンで協力 |
| brand-asset-governance-bc | **Shared Kernel** | ブランドガイドライン・資産を共有 |
| marketing-analytics-bc | **Customer-Supplier** | 効果測定データを提供。分析結果を受領 |
| consumer-engagement-bc | **Customer-Supplier** | キャンペーン接点データを提供 |
| VS1 市場機会発見 | **Upstream (ACL)** | 消費者インサイトを受領（Anti-Corruption Layer経由） |
| VS2 製品開発 | **Upstream (ACL)** | 製品情報・ストーリーを受領 |
| VS4 販売・流通 | **Downstream** | 店頭プロモーション方針を提供 |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/campaigns` | POST | 新規キャンペーン作成 |
| `/campaigns/{id}/approve` | POST | キャンペーン承認 |
| `/campaigns/{id}/launch` | POST | キャンペーン開始 |
| `/campaigns/{id}/complete` | POST | キャンペーン終了・効果登録 |
| `/campaigns/{id}/creatives` | POST | クリエイティブ追加 |
| `/campaigns/{id}/creatives/{assetId}/approve` | POST | クリエイティブ承認 |
| `/campaigns/{id}/media-plan` | PUT | メディアプラン設定 |
| `/personas` | POST | ペルソナ作成 |
| `/personas/{id}` | PUT | ペルソナ更新 |
| `/creative-library/assets` | POST | クリエイティブ資産登録 |
| `/media-executions` | POST | メディア実行作成 |
| `/media-executions/{id}/performance` | POST | メディア実績記録 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/campaigns` | GET | キャンペーン一覧取得 |
| `/campaigns/{id}` | GET | キャンペーン詳細取得 |
| `/campaigns/by-brand/{brandId}` | GET | ブランド別キャンペーン取得 |
| `/campaigns/active` | GET | 実行中キャンペーン一覧 |
| `/personas` | GET | ペルソナ一覧取得 |
| `/personas/{id}` | GET | ペルソナ詳細取得 |
| `/personas/by-brand/{brandId}` | GET | ブランド別ペルソナ取得 |
| `/creative-library/search` | GET | クリエイティブ検索 |
| `/media-executions/{id}` | GET | メディア実行詳細取得 |
| `/media-executions/{id}/performance` | GET | メディア実績取得 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| brand-strategy-bc | ブランド情報・戦略方針の参照 |
| brand-asset-governance-bc | ブランドガイドライン・資産の参照 |
| regional-brand-activation-bc | 地域ブランド方針・ローカル適応ガイドの参照 |
| VS1 市場機会発見 | 消費者インサイト・市場調査データの参照 |
| VS2 製品開発 | 製品情報・製品ストーリーの参照 |
| identity-management-bc | ユーザー認証・権限管理 |
| audit-logging-bc | 監査ログの記録 |

---

## 次のステップ

### CL3完了後の推奨アクション

1. **他のCore サブドメインのCL3定義**
   - brand-strategy-bc
   - digital-marketing-bc
   - brand-experience-bc

2. **Phase 4: Architecture への移行**
   - VS3内Context Map統合設計
   - イベント駆動アーキテクチャ設計
   - 技術スタック選定

3. **API契約の詳細設計**
   - api-contract-designer による詳細仕様作成
   - OpenAPI仕様書作成

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（campaign-communications-bc定義）
**次のフェーズ:** 他Core SDのCL3 または Phase 4: Architecture
