# Bounded Context: brand-experience-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** brand-experience（ブランド体験）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | brand-experience-bc |
| **日本語名** | ブランド体験 |
| **命名パターン** | `-experience`（体験型） |
| **命名理由** | 「イベント管理」「スポンサーシップ管理」ではなく「体験」を採用。ラグビーワールドカップ公式スポンサー、マンチェスター・シティ パートナーシップ、F1スポンサーシップ等を通じた消費者への**直接的なブランド体験の創造**を表現。管理業務ではなく、感動・記憶に残る体験を生み出すという能動的価値創造を強調 |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

**BC名**: brand-experience-bc（ブランド体験バウンデッドコンテキスト）

**目的**:
スポーツスポンサーシップ、音楽・文化イベント、店頭プロモーションを通じて、消費者に直接的かつ記憶に残るブランド体験を提供し、Asahiブランドのプレミアムイメージを強化する。

**責務**:
- スポーツスポンサーシップの企画・契約・活性化（ラグビーW杯、F1、マンチェスター・シティ等）
- 音楽・文化イベントの企画・実行
- 自社ブランド体験イベントの運営
- 店頭プロモーションの企画・実行
- スポンサーシップ・イベントのROI測定

**チーム境界**:
- **担当組織**: マーケティング本部 スポンサーシップ・イベント部
- **チーム構成**:
  - スポンサーシップ戦略チーム（契約交渉、権利管理）
  - イベントプロデュースチーム（企画・制作・運営）
  - 店頭プロモーションチーム（リテール連携）
  - 効果測定チーム（ROI分析、メディア価値算出）
- **推定人員**: 30-45名

---

### 2. ビジネスオペレーション詳細

#### OP1: スポーツスポンサーシップ管理

**業務フロー:**
```
1. スポンサーシップ機会評価
   └─ スポーツプロパティ調査（W杯、F1、プロサッカー等）
   └─ ブランドフィット評価
   └─ 競合スポンサー分析
   └─ 費用対効果予測

2. 契約交渉・締結
   └─ 権利範囲の交渉（呼称権、ロゴ使用、会場権等）
   └─ 法務レビュー
   └─ 契約金額・期間の確定
   └─ 契約締結・権利確保

3. 権利管理
   └─ 権利台帳への登録
   └─ 権利行使スケジュール策定
   └─ 権利使用のモニタリング
   └─ 契約更新・終了管理

4. スポンサーシップ活性化
   └─ 活性化プログラム企画
   └─ キャンペーン・プロモーション連携
   └─ 現地アクティベーション実行
   └─ メディア露出最大化
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | スポンサーシップ契約はブランド戦略との整合性審査を必須とする |
| BR-OP1-02 | 年間1億円以上の契約は経営会議承認を必須とする |
| BR-OP1-03 | 競合排他条項を含む契約は法務レビューを必須とする |
| BR-OP1-04 | 権利行使は契約範囲を厳守し、逸脱時は即時報告する |
| BR-OP1-05 | グローバルスポンサーシップ（W杯、F1等）は本社主導で各地域と連携する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ブランド戦略方針（brand-strategy） | スポンサーシップ契約書 |
| 地域イベント方針（regional-brand-activation） | 権利台帳 |
| 予算計画 | 活性化プログラム |

**トリガー:**
- スポンサーシップ機会の発生（大会開催決定等）
- 既存契約の更新時期
- ブランド戦略変更
- 競合の動向

---

#### OP2: 音楽・文化イベント企画

**業務フロー:**
```
1. イベント機会探索
   └─ 音楽フェスティバル・文化イベント調査
   └─ ターゲット層との親和性評価
   └─ ブランドイメージとの整合確認

2. イベント企画立案
   └─ コンセプト策定
   └─ 協業パートナー選定（アーティスト、主催者）
   └─ プログラム設計
   └─ 体験コンテンツ企画（試飲、限定商品等）

3. 実行準備
   └─ 会場・設備手配
   └─ スタッフ配置計画
   └─ 安全管理計画
   └─ 許認可取得（酒類提供許可等）

4. イベント実行
   └─ 当日運営
   └─ 来場者体験提供
   └─ SNS発信・リアルタイムマーケティング
   └─ メディア対応

5. 事後評価
   └─ 来場者数・満足度集計
   └─ メディア露出分析
   └─ 改善点抽出
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | 酒類提供イベントは責任ある飲酒ガイドラインを遵守する |
| BR-OP2-02 | 未成年者の飲酒防止策を必須とする |
| BR-OP2-03 | イベント実施は現地法規制を100%遵守する |
| BR-OP2-04 | 大規模イベント（1000名以上）は安全管理計画の事前承認を必須とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ブランド戦略方針 | イベント企画書 |
| キャンペーン計画（campaign-communications） | イベント実施報告書 |
| 予算 | 来場者データ |

**トリガー:**
- 年間イベントカレンダー
- 新製品発売
- ブランドキャンペーン連動
- パートナーからの協業提案

---

#### OP3: ブランド体験イベント運営

**業務フロー:**
```
1. 体験イベント企画
   └─ ブランド体験コンセプト策定（Asahi Super Dry体験等）
   └─ ターゲット顧客設定
   └─ 体験プログラム設計
   └─ 会場・日程選定

2. 参加者募集・管理
   └─ 募集チャネル選定（Web、SNS、店頭等）
   └─ 参加者登録システム運用
   └─ 参加者コミュニケーション

3. イベント実施
   └─ ブランドストーリーテリング
   └─ 製品体験（試飲、醸造所見学等）
   └─ インタラクティブコンテンツ提供
   └─ 参加者データ収集（アンケート等）

4. フォローアップ
   └─ 参加者へのサンクスメール
   └─ CRMへのデータ連携（consumer-engagement）
   └─ 参加者の継続エンゲージメント
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 参加者の個人情報は個人情報保護法・GDPRを遵守して管理する |
| BR-OP3-02 | 体験イベントはブランドガイドラインに準拠する |
| BR-OP3-03 | 参加者データはconsumer-engagementへ48時間以内に連携する |
| BR-OP3-04 | 醸造所見学等の施設イベントは安全管理規定を遵守する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品情報（VS2） | 体験イベント参加者データ |
| ブランドガイドライン（brand-asset-governance） | イベント実績レポート |
| 年間計画 | 参加者フィードバック |

**トリガー:**
- 年間体験イベント計画
- 新製品発売
- 工場・醸造所の定期公開

---

#### OP4: 店頭プロモーション

**業務フロー:**
```
1. 店頭施策企画
   └─ 販促カレンダーとの整合
   └─ リテールパートナーとの協議
   └─ 店頭POP・什器設計
   └─ 試飲・サンプリング計画

2. 施策準備
   └─ 販促物制作・調達
   └─ 店舗配荷計画
   └─ デモンストレーター手配
   └─ 店舗スタッフ研修

3. 施策実行
   └─ 店頭展開実施
   └─ 試飲・サンプリング実行
   └─ 売場モニタリング
   └─ 実施状況レポート

4. 効果測定
   └─ 売上データ分析（VS4連携）
   └─ 来店客数・購買率分析
   └─ 施策改善提案
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 試飲はリテールパートナーの許可を得て実施する |
| BR-OP4-02 | 店頭販促物はブランドガイドライン準拠とする |
| BR-OP4-03 | 試飲・サンプリングは責任ある飲酒ガイドラインを遵守する |
| BR-OP4-04 | 実施結果は週次でVS4（販売・流通）と共有する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 販促計画（VS4） | 店頭施策実績 |
| ブランド資産（brand-asset-governance） | 販促物配荷実績 |
| 製品情報（VS2） | 試飲実施レポート |

**トリガー:**
- 新製品発売
- 季節販促（夏、年末等）
- キャンペーン連動
- リテールパートナーからの要請

---

#### OP5: スポンサーシップROI測定

**業務フロー:**
```
1. 測定計画策定
   └─ KPI設定（メディア露出、認知度、売上影響等）
   └─ 測定手法選定
   └─ ベースライン設定
   └─ 測定スケジュール策定

2. データ収集
   └─ メディア露出データ収集（TV、デジタル、SNS）
   └─ ブランド調査実施（認知度、イメージ）
   └─ 売上データ収集（VS4連携）
   └─ イベント参加者データ集計

3. ROI分析
   └─ メディア換算価値（AVE）算出
   └─ ブランドリフト分析
   └─ 売上寄与分析
   └─ 総合ROI算出

4. レポーティング・活用
   └─ ROIレポート作成
   └─ 経営報告
   └─ 次年度計画への反映
   └─ marketing-analyticsへのデータ提供
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | 主要スポンサーシップのROI測定は四半期ごとに実施する |
| BR-OP5-02 | メディア露出価値算出は標準メソッドに準拠する |
| BR-OP5-03 | ROIレポートは契約更新判断の必須資料とする |
| BR-OP5-04 | 測定結果はmarketing-analyticsと統合して分析する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| スポンサーシップ契約情報 | スポンサーシップROIレポート |
| メディア露出データ | メディア換算価値レポート |
| ブランド調査データ | ブランドリフト分析 |
| 売上データ（VS4） | 投資対効果分析 |

**トリガー:**
- スポンサーシップ契約期間中の定期測定
- 大型イベント終了後
- 契約更新検討時
- 経営報告サイクル

---

### 3. ユビキタス言語（Ubiquitous Language）

#### スポンサーシップ用語

| 用語 | 定義 |
|------|------|
| **Sports Property（スポーツプロパティ）** | スポンサーシップ対象となるスポーツ大会・チーム・選手等の権利保有者 |
| **Naming Rights（ネーミングライツ）** | 施設やイベントに企業名・ブランド名を冠する権利 |
| **Activation（アクティベーション）** | スポンサーシップ権利を活用したマーケティング活動 |
| **Ambush Marketing（アンブッシュマーケティング）** | 公式スポンサーでない企業による便乗マーケティング |
| **Exclusivity（排他権）** | カテゴリー内での独占スポンサー権 |
| **Rights Fee（権利料）** | スポンサーシップ契約で支払う権利使用料 |

#### イベント用語

| 用語 | 定義 |
|------|------|
| **Brand Experience（ブランド体験）** | 消費者がブランドと直接接触し、五感で体験する機会 |
| **Sampling（サンプリング）** | 製品を無料で配布し体験させるプロモーション手法 |
| **Demo Staff（デモンストレーター）** | 店頭や会場で製品説明・試飲を行うスタッフ |
| **Pop-up（ポップアップ）** | 期間限定で設置する体験型店舗・スペース |
| **Experiential Marketing（体験型マーケティング）** | 消費者参加型の体験を通じたマーケティング |

#### 効果測定用語

| 用語 | 定義 |
|------|------|
| **AVE（Advertising Value Equivalency）** | メディア露出を広告出稿費用に換算した価値 |
| **Media Exposure（メディア露出）** | スポンサーロゴ等がメディアに露出した量・時間 |
| **Brand Lift（ブランドリフト）** | スポンサーシップ・イベントによるブランド認知・イメージの向上 |
| **ROI（Return on Investment）** | 投資対効果。投資額に対するリターン |
| **Reach（リーチ）** | 施策がリーチした人数・割合 |
| **Engagement（エンゲージメント）** | 消費者の関与・反応の度合い |

#### アサヒグループ固有用語

| 用語 | 定義 |
|------|------|
| **Rugby World Cup Sponsorship** | ラグビーワールドカップの公式ワールドワイドパートナー契約 |
| **Manchester City Partnership** | マンチェスター・シティFCとのグローバルパートナーシップ |
| **F1 Sponsorship** | F1世界選手権へのスポンサー参画 |
| **Asahi Super Dry Experience** | Asahi Super Dryブランドの体験型イベント総称 |
| **Premium Brand Experience** | プレミアム感を訴求するハイエンド体験イベント |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: SponsorshipContract（スポンサーシップ契約）

**責務**: スポンサーシップ契約のライフサイクル管理

```
SponsorshipContract [Aggregate Root]
├── contractId: ContractId [Value Object]
├── propertyInfo: PropertyInfo [Value Object]
│   ├── propertyName: string（ラグビーW杯、マンチェスター・シティ等）
│   ├── propertyType: enum (SPORTS_EVENT, TEAM, LEAGUE, ATHLETE, VENUE)
│   ├── propertyOwner: string（権利保有者）
│   └── category: SportsCategory
├── contractTerms: ContractTerms [Entity]
│   ├── startDate: Date
│   ├── endDate: Date
│   ├── rightsFee: Money
│   ├── paymentSchedule: PaymentSchedule[]
│   └── renewalOption: RenewalOption?
├── rights: SponsorshipRight[] [Entity]
│   ├── rightId: RightId
│   ├── rightType: enum (NAMING, LOGO, VENUE, HOSPITALITY, CONTENT, CATEGORY_EXCLUSIVITY)
│   ├── description: string
│   ├── territory: Territory[]
│   └── restrictions: Restriction[]
├── brandAlignment: BrandAlignment [Value Object]
│   ├── strategicFit: FitScore（1-5）
│   ├── targetAudienceMatch: boolean
│   └── approvedBy: UserId
├── status: ContractStatus [Value Object]
│   └── value: enum (DRAFT, NEGOTIATING, ACTIVE, EXPIRING, EXPIRED, TERMINATED)
├── activations: ActivationProgram[] [Entity]
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-SC-01 | ACTIVE状態への遷移にはbrandAlignment.strategicFitが3以上であること |
| INV-SC-02 | rightsFeeが1億円以上の契約はACTIVE遷移に経営会議承認が必要 |
| INV-SC-03 | endDateはstartDateより後であること |
| INV-SC-04 | CATEGORY_EXCLUSIVITY権利は同カテゴリで重複不可 |

---

#### 集約2: BrandEvent（ブランドイベント）

**責務**: ブランド体験イベントの企画・実行管理

```
BrandEvent [Aggregate Root]
├── eventId: EventId [Value Object]
├── eventInfo: EventInfo [Value Object]
│   ├── name: string
│   ├── eventType: enum (MUSIC_FESTIVAL, BRAND_EXPERIENCE, TASTING, FACTORY_TOUR, POPUP)
│   ├── concept: string
│   └── targetBrand: BrandId
├── schedule: EventSchedule [Value Object]
│   ├── startDateTime: DateTime
│   ├── endDateTime: DateTime
│   └── venue: Venue
├── program: EventProgram [Entity]
│   ├── sessions: Session[]
│   ├── experiences: Experience[]
│   └── content: Content[]
├── capacity: EventCapacity [Value Object]
│   ├── maxParticipants: number
│   ├── registeredParticipants: number
│   └── waitlist: number
├── participants: Participant[] [Entity]
│   ├── participantId: ParticipantId
│   ├── registrationDate: Date
│   ├── attendanceStatus: enum (REGISTERED, ATTENDED, NO_SHOW, CANCELLED)
│   └── consent: DataConsent
├── safetyPlan: SafetyPlan [Entity]
│   ├── riskAssessment: RiskAssessment
│   ├── emergencyContacts: Contact[]
│   └── approvalStatus: ApprovalStatus
├── status: EventStatus [Value Object]
│   └── value: enum (PLANNING, APPROVED, REGISTRATION_OPEN, IN_PROGRESS, COMPLETED, CANCELLED)
├── results: EventResults [Entity]?
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-BE-01 | REGISTRATION_OPEN状態への遷移にはsafetyPlan.approvalStatusがAPPROVEDであること |
| INV-BE-02 | registeredParticipantsはmaxParticipantsを超えないこと |
| INV-BE-03 | 1000名以上のイベントはsafetyPlanの経営承認が必要 |
| INV-BE-04 | COMPLETED状態への遷移にはresultsが必須 |

---

#### 集約3: StorePromotion（店頭プロモーション）

**責務**: 店頭プロモーション施策の管理

```
StorePromotion [Aggregate Root]
├── promotionId: PromotionId [Value Object]
├── promotionInfo: PromotionInfo [Value Object]
│   ├── name: string
│   ├── promotionType: enum (TASTING, SAMPLING, DISPLAY, DEMO)
│   ├── targetProduct: ProductId
│   └── campaign: CampaignId?
├── period: PromotionPeriod [Value Object]
│   ├── startDate: Date
│   ├── endDate: Date
│   └── peakDays: Date[]
├── stores: StoreAllocation[] [Entity]
│   ├── storeId: StoreId
│   ├── retailPartner: RetailPartnerId
│   ├── allocatedMaterials: MaterialAllocation[]
│   └── demoStaff: DemoStaffAssignment[]
├── materials: PromotionalMaterial[] [Entity]
│   ├── materialId: MaterialId
│   ├── materialType: enum (POP, DISPLAY, SAMPLE, NOVELTY)
│   ├── quantity: number
│   └── distributionStatus: DistributionStatus
├── budget: PromotionBudget [Value Object]
│   ├── totalBudget: Money
│   ├── materialCost: Money
│   ├── staffCost: Money
│   └── actualSpend: Money
├── status: PromotionStatus [Value Object]
│   └── value: enum (PLANNING, APPROVED, PREPARATION, ACTIVE, COMPLETED)
├── results: PromotionResults [Entity]?
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-SP-01 | ACTIVE状態への遷移には全storesへのmaterials配荷完了が必要 |
| INV-SP-02 | tastingを含む施策はretailPartnerの許可証が必要 |
| INV-SP-03 | actualSpendはtotalBudgetの110%を超えないこと（要アラート） |
| INV-SP-04 | COMPLETED状態への遷移にはresultsが必須 |

---

#### 集約4: SponsorshipROI（スポンサーシップROI）

**責務**: スポンサーシップ投資対効果の測定管理

```
SponsorshipROI [Aggregate Root]
├── roiId: ROIId [Value Object]
├── contractId: ContractId [Value Object]
├── measurementPeriod: MeasurementPeriod [Value Object]
│   ├── startDate: Date
│   ├── endDate: Date
│   └── periodType: enum (QUARTERLY, ANNUAL, EVENT_BASED)
├── investment: InvestmentData [Value Object]
│   ├── rightsFee: Money
│   ├── activationCost: Money
│   ├── totalInvestment: Money
│   └── breakdown: CostBreakdown[]
├── mediaExposure: MediaExposure [Entity]
│   ├── tvExposure: TVExposureData
│   ├── digitalExposure: DigitalExposureData
│   ├── socialExposure: SocialExposureData
│   ├── printExposure: PrintExposureData
│   └── totalAVE: Money（広告換算価値）
├── brandImpact: BrandImpact [Entity]
│   ├── awarenessLift: Percentage
│   ├── imageLift: Percentage
│   ├── considerationLift: Percentage
│   └── surveySource: SurveyId
├── businessImpact: BusinessImpact [Entity]?
│   ├── salesLift: Percentage
│   ├── salesValue: Money
│   └── attributionModel: AttributionModel
├── calculatedROI: ROICalculation [Value Object]
│   ├── roiPercentage: Percentage
│   ├── roiValue: Money
│   └── calculationMethod: string
├── status: ROIStatus [Value Object]
│   └── value: enum (DRAFT, IN_ANALYSIS, COMPLETED, REPORTED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-ROI-01 | COMPLETED状態への遷移にはmediaExposure.totalAVEが算出済みであること |
| INV-ROI-02 | roiPercentageの算出には標準メソッドを適用すること |
| INV-ROI-03 | 主要スポンサーシップは四半期ごとに測定を実施すること |

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **SponsorshipContractSigned** | {contractId, propertyName, rightsFee, startDate, endDate} | 契約締結時 | マーケティング部門、経理部門 |
| **SponsorshipActivated** | {contractId, activationId, activationType, startDate} | 活性化プログラム開始時 | campaign-communications |
| **EventRegistrationOpened** | {eventId, eventName, capacity, registrationDeadline} | 参加登録開始時 | digital-marketing、consumer-engagement |
| **EventCompleted** | {eventId, eventName, actualParticipants, satisfactionScore} | イベント終了時 | marketing-analytics、consumer-engagement |
| **StorePromotionLaunched** | {promotionId, promotionName, storeCount, startDate} | 店頭施策開始時 | VS4（販売・流通） |
| **SponsorshipROIReported** | {roiId, contractId, roiPercentage, totalAVE, periodEnd} | ROIレポート完了時 | brand-strategy、marketing-analytics、経営層 |
| **ParticipantDataCollected** | {eventId, participantCount, consentedForCRM} | 参加者データ収集完了時 | consumer-engagement |

---

### 6. コンテキストマップ（Context Map）

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    │     brand-strategy-bc                │
                    │          (Upstream)                  │
                    │                                      │
                    └──────────────┬───────────────────────┘
                                   │ ブランド戦略方針
                                   ▼
┌─────────────────┐    ┌──────────────────────────────────┐    ┌─────────────────┐
│ regional-brand- │    │                                  │    │ campaign-       │
│ activation-bc   │───►│    brand-experience-bc           │◄──►│ communications- │
│ (Upstream)      │    │                                  │    │ bc              │
│                 │    │                                  │    │ (Partnership)   │
│ 地域イベント方針│    └──────────────┬───────────────────┘    │ キャンペーン連携│
└─────────────────┘                   │                        └─────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ marketing-      │    │ consumer-       │    │ VS4:            │
│ analytics-bc    │    │ engagement-bc   │    │ sales-channel   │
│ (Downstream)    │    │ (Downstream)    │    │ (Partnership)   │
│                 │    │                 │    │                 │
│ ROIデータ受領   │    │ 参加者データ受領│    │ 店頭連携        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                            │
         │                            ▼
         │              ┌─────────────────┐
         └─────────────►│ brand-asset-    │
                        │ governance-bc   │
                        │ (Upstream)      │
                        │                 │
                        │ ブランド資産提供│
                        └─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| brand-strategy-bc | **Customer-Supplier** | ブランド戦略方針の供給を受ける |
| regional-brand-activation-bc | **Customer-Supplier** | 地域イベント方針の供給を受ける |
| campaign-communications-bc | **Partnership** | キャンペーンとイベントの連携で対等に協力 |
| brand-asset-governance-bc | **Customer-Supplier** | ブランド資産（ガイドライン、ロゴ等）の供給を受ける |
| consumer-engagement-bc | **Customer-Supplier** | 参加者データをCRMに提供する |
| marketing-analytics-bc | **Customer-Supplier** | スポンサーシップROI・イベント効果データを提供する |
| VS4 sales-channel | **Partnership** | 店頭プロモーションの実行で対等に協力 |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/sponsorships` | POST | スポンサーシップ契約新規作成 |
| `/sponsorships/{id}/activate` | POST | スポンサーシップをアクティブ化 |
| `/sponsorships/{id}/activations` | POST | 活性化プログラム登録 |
| `/events` | POST | ブランドイベント新規作成 |
| `/events/{id}/open-registration` | POST | 参加登録開始 |
| `/events/{id}/complete` | POST | イベント完了・結果登録 |
| `/promotions` | POST | 店頭プロモーション作成 |
| `/promotions/{id}/launch` | POST | 店頭施策開始 |
| `/sponsorships/{id}/roi` | POST | ROI測定開始 |
| `/sponsorships/{id}/roi/{roiId}/complete` | POST | ROI測定完了 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/sponsorships` | GET | スポンサーシップ契約一覧 |
| `/sponsorships/{id}` | GET | スポンサーシップ契約詳細 |
| `/sponsorships/{id}/rights` | GET | 権利一覧 |
| `/events` | GET | イベント一覧 |
| `/events/{id}` | GET | イベント詳細 |
| `/events/{id}/participants` | GET | 参加者一覧 |
| `/promotions` | GET | 店頭プロモーション一覧 |
| `/promotions/{id}/results` | GET | 施策結果 |
| `/sponsorships/{id}/roi` | GET | ROI測定結果一覧 |
| `/dashboard/upcoming-events` | GET | 今後のイベントダッシュボード |
| `/dashboard/active-sponsorships` | GET | アクティブスポンサーシップダッシュボード |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| brand-strategy-bc | ブランド戦略方針取得 |
| regional-brand-activation-bc | 地域イベント方針取得 |
| brand-asset-governance-bc | ブランドガイドライン・資産取得 |
| campaign-communications-bc | キャンペーン情報連携 |
| VS2 product-development | 製品情報取得 |
| VS4 sales-channel | 売上データ・店舗情報取得 |

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（brand-experience-bc定義）
