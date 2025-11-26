# Bounded Context: craft-innovation-development-bc

**サブドメイン**: craft-innovation-development（クラフト・革新開発）
**ドメインタイプ**: Core ★★★★☆
**所属活動領域**: A3 酒類製品開発
**最終更新**: 2025-11-26

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**craft-innovation-development-bc**（クラフト・革新開発バウンデッドコンテキスト）

#### 目的
クラフトビール、限定品、革新的製品（ノンアルコール、低糖質、RTD等）の開発を行い、市場差別化と新規顧客獲得を実現する。既存のプレミアムビールとは異なる価値軸で、トレンド対応と実験的製品開発を担う。

#### 責務
1. **クラフト製品開発** - 小規模・個性的なビール製品の企画・開発
2. **革新製品開発** - ノンアルコール、低糖質、機能性ビールの開発
3. **限定品企画・開発** - 季節・地域・コラボ限定品の開発
4. **RTD製品開発** - Ready to Drink缶カクテル等の開発
5. **新技術の製品化検証** - 研究成果を製品に落とし込む実証

#### チーム境界
- **開発チーム**: クラフトビール醸造士、製品企画担当、フレーバーデザイナー
- **マーケティング連携**: トレンドアナリスト、消費者リサーチャー
- **技術連携**: fermentation-research-bc からの技術受領者

---

### 2. ビジネスオペレーション詳細

#### オペレーション1: クラフトビール開発

**実行手順**:
1. 市場トレンド・消費者嗜好の分析
2. コンセプト策定（スタイル、ターゲット、ストーリー）
3. ベースレシピの選定・調整
4. 特殊素材・フレーバーの選定
5. パイロット醸造（複数バッチ）
6. 官能評価・消費者テスト
7. レシピ確定・製品仕様書作成
8. 少量生産・市場テスト

**業務ルール**:
- 1バッチあたり最大1000L（パイロット規模）
- 既存スタイルの模倣ではなく、独自性を持つこと
- 原価率は通常製品の1.5倍まで許容
- 官能評価スコア7.0以上で次工程へ進行可能
- 限定生産の場合は3ヶ月以内の販売終了計画を策定

**入力/出力**:
- **入力**: 市場トレンドデータ、消費者インサイト、特殊素材リスト
- **出力**: クラフト製品仕様書、レシピ、ブランドストーリー

**トリガー**:
- 四半期ごとの新製品企画サイクル
- 市場トレンドの急変（健康志向、サステナビリティ等）
- 競合の革新製品発売

---

#### オペレーション2: ノンアルコール・低アルコール開発

**実行手順**:
1. ターゲット市場・消費シーンの定義
2. 技術方式の選定（脱アルコール、低発酵、ブレンド等）
3. fermentation-research-bc への技術相談・協力依頼
4. ベースレシピ開発（アルコール除去後の味わい設計）
5. 香味補完技術の適用（ホップアロマ、フレーバー添加）
6. 官能評価（ビール感、満足度）
7. 法規制対応確認（表示、成分基準）
8. 製品仕様確定

**業務ルール**:
- ノンアルコール: アルコール度数0.5%未満（法規制準拠）
- 低アルコール: 1.0%〜3.5%の範囲で設計
- 「ビールらしさ」官能評価スコア6.5以上必須
- カロリーは通常ビールの70%以下を目標
- 保存料・人工甘味料は使用制限あり

**入力/出力**:
- **入力**: 技術仕様（fermentation-research-bc）、市場要件
- **出力**: ノンアル製品仕様、栄養成分表、表示案

**トリガー**:
- 健康志向トレンドの高まり
- 法規制変更（酒税法改正等）
- 競合製品の市場シェア変動

---

#### オペレーション3: 限定品企画・開発

**実行手順**:
1. 限定テーマの決定（季節、地域、コラボ、記念）
2. パートナー選定（コラボの場合：蒸留所、農園、シェフ等）
3. 限定要素の調達計画（希少原料、特殊素材）
4. ストーリー・パッケージコンセプト設計
5. レシピ開発（限定素材を活かす）
6. 生産数量・販売チャネル計画
7. プロモーション連携（VS3）
8. 限定期間内の製造・販売実行

**業務ルール**:
- 季節限定: 販売期間最大3ヶ月
- 地域限定: 特定エリアのみ流通（全国展開不可）
- コラボ限定: パートナー承認必須、ロイヤリティ契約
- 生産数量は通常製品の10%以下
- 価格プレミアム: 通常製品の1.2〜2.0倍

**入力/出力**:
- **入力**: 限定テーマ、パートナー情報、限定素材
- **出力**: 限定製品仕様、数量計画、販売計画

**トリガー**:
- 年間限定品カレンダー（計画的）
- 特別イベント・記念日
- パートナーからのコラボ提案

---

#### オペレーション4: RTD開発

**実行手順**:
1. RTDカテゴリ選定（ハイボール、カクテル、サワー、チューハイ等）
2. ベースアルコール選定（ウォッカ、スピリッツ、焼酎等）
3. フレーバー設計（果汁、香料、甘味のバランス）
4. アルコール度数設定（市場ニーズに応じて3%〜9%）
5. 炭酸・テクスチャ設計
6. パッケージサイズ決定（250ml、350ml、500ml）
7. 官能評価・消費者テスト
8. 製品仕様確定・生産移管

**業務ルール**:
- アルコール度数は3%〜9%の範囲
- 果汁使用の場合は含有率を明記（表示義務）
- 甘味料使用時は「カロリーオフ」表記基準を遵守
- 缶サイズごとにアルコール量を消費者に明示
- 未成年飲酒防止の注意表記必須

**入力/出力**:
- **入力**: 市場トレンド、ベースアルコール、フレーバー候補
- **出力**: RTD製品仕様、栄養成分表、パッケージデザイン案

**トリガー**:
- RTD市場の成長トレンド
- 新規フレーバートレンド（柑橘、ベリー、トロピカル等）
- 競合RTD製品の成功事例

---

#### オペレーション5: 革新技術実証

**実行手順**:
1. fermentation-research-bc からの新技術情報受領
2. 技術の製品適用可能性評価
3. 製品コンセプトへの落とし込み
4. 小規模実証醸造（10L〜100Lスケール）
5. 技術課題の洗い出しと対策
6. 官能評価・品質評価
7. スケールアップ可能性判定
8. 成功技術の製品化移行 or フィードバック

**業務ルール**:
- 実証は最大3回まで（3回失敗で技術返却）
- 実証期間は最長6ヶ月
- 成功基準: 官能評価7.0以上 + 品質安定性確認
- 失敗時は失敗原因と改善提案を fermentation-research-bc へフィードバック
- 成功技術は「革新技術DB」へ登録

**入力/出力**:
- **入力**: 新技術仕様、推奨条件（fermentation-research-bc）
- **出力**: 技術実証レポート、製品化可否判定、改善提案

**トリガー**:
- fermentation-research-bc からの RecipeValidated イベント
- 新酵母株の発見（YeastStrainDiscovered イベント）
- 外部技術の導入検討

---

### 3. ビジネスルール

#### 製品開発全般
| ルール | 内容 | 適用範囲 |
|--------|------|---------|
| BR-CI-001 | 官能評価スコア7.0未満の製品は発売不可 | 全製品 |
| BR-CI-002 | 原価率は標準の1.5倍まで許容 | クラフト・限定品 |
| BR-CI-003 | 開発期間は最長12ヶ月（限定品は6ヶ月） | 全製品 |
| BR-CI-004 | 年間新製品数は最大20SKU | 全カテゴリ |

#### ノンアルコール・低アルコール
| ルール | 内容 | 根拠 |
|--------|------|------|
| BR-CI-010 | アルコール0.5%未満を「ノンアルコール」表記 | 酒税法 |
| BR-CI-011 | 「ビール感」評価6.5以上必須 | 品質基準 |
| BR-CI-012 | カロリー表示は100mlあたりで統一 | 食品表示法 |

#### 限定品
| ルール | 内容 | 理由 |
|--------|------|------|
| BR-CI-020 | 季節限定は3ヶ月以内に販売終了 | ブランド価値維持 |
| BR-CI-021 | コラボ製品はパートナー承認必須 | 契約履行 |
| BR-CI-022 | 地域限定は3都道府県以下 | 希少性維持 |

#### RTD
| ルール | 内容 | 根拠 |
|--------|------|------|
| BR-CI-030 | アルコール度数3%〜9%の範囲 | 市場適合 |
| BR-CI-031 | 缶あたりアルコール量を明示 | 健康配慮表示 |
| BR-CI-032 | 未成年飲酒防止表記必須 | 法規制 |

---

### 4. ユビキタス言語（Ubiquitous Language）

#### 製品関連
- **クラフト製品（Craft Product）**: 小規模・個性的な特徴を持つビール製品
- **限定品（Limited Edition）**: 期間・地域・数量を限定した製品
- **RTD（Ready to Drink）**: すぐ飲める状態の缶カクテル・チューハイ
- **ノンアルコール（Non-Alcoholic）**: アルコール度数0.5%未満の製品
- **低アルコール（Low-Alcohol）**: アルコール度数1.0%〜3.5%の製品

#### 開発プロセス関連
- **コンセプト（Concept）**: 製品の基本構想（ターゲット、味わい、ストーリー）
- **パイロット醸造（Pilot Brewing）**: 小規模試験醸造（最大1000L）
- **官能評価（Sensory Evaluation）**: 専門パネルによる味・香り・外観の評価
- **消費者テスト（Consumer Test）**: 一般消費者による評価
- **製品仕様書（Product Specification）**: 製品の全定義文書

#### 限定品関連
- **季節限定（Seasonal Limited）**: 特定の季節のみ販売する製品
- **地域限定（Regional Limited）**: 特定地域のみで販売する製品
- **コラボ限定（Collaboration Limited）**: 外部パートナーとの協業製品
- **数量限定（Quantity Limited）**: 生産数量を限定した製品

#### 技術関連
- **脱アルコール（De-alcoholization）**: 発酵後にアルコールを除去する技術
- **低発酵（Low Fermentation）**: アルコール生成を抑える発酵方式
- **フレーバー設計（Flavor Design）**: 香味成分の配合設計
- **ホップアロマ（Hop Aroma）**: ホップ由来の香り成分
- **革新技術DB（Innovation Technology DB）**: 製品化成功技術の知見蓄積

#### 市場関連
- **トレンド分析（Trend Analysis）**: 市場・消費者動向の分析
- **消費シーン（Consumption Scene）**: 製品が消費される状況・場面
- **ブランドストーリー（Brand Story）**: 製品の背景・物語
- **価格プレミアム（Price Premium）**: 通常製品に対する価格上乗せ

---

## 【技術面】

### 5. 集約設計（Aggregates）

#### 集約1: CraftProduct（クラフト製品）

**集約ルート**: CraftProduct

**エンティティ**:
```
CraftProduct {
  productId: ProductId (識別子)
  productCode: String (製品コード, 例: "CRAFT-2025-001")
  productName: String (製品名)
  productType: ProductType (craft-beer | non-alcoholic | low-alcohol | rtd | limited)
  concept: ProductConcept (製品コンセプト)
  recipe: RecipeReference (レシピ参照)
  specifications: ProductSpecifications (製品仕様)
  developmentStatus: DevelopmentStatus (draft | in-development | testing | approved | released | discontinued)
  limitedInfo: LimitedInfo? (限定情報, 限定品のみ)
  createdAt: DateTime
  updatedAt: DateTime
  releasedAt: DateTime?
  discontinuedAt: DateTime?
}

ProductConcept {
  targetAudience: String (ターゲット顧客)
  consumptionScene: List<String> (消費シーン)
  flavorProfile: FlavorProfile (味わいプロファイル)
  brandStory: String (ブランドストーリー)
  differentiator: String (差別化ポイント)
}

ProductSpecifications {
  alcoholContent: Percentage (アルコール度数)
  calories: KcalPer100ml (カロリー)
  ingredients: List<Ingredient> (原材料)
  nutritionFacts: NutritionFacts (栄養成分)
  packagingSizes: List<PackageSize> (パッケージサイズ)
  shelfLife: Duration (賞味期限)
}

LimitedInfo {
  limitationType: LimitationType (seasonal | regional | collaboration | quantity)
  availabilityPeriod: DateRange? (販売期間)
  availableRegions: List<Region>? (販売地域)
  productionQuantity: Integer? (生産数量)
  collaborationPartner: Partner? (コラボパートナー)
}

FlavorProfile {
  bitterness: Score (苦味スコア 1-10)
  sweetness: Score (甘味スコア 1-10)
  body: Score (ボディ感 1-10)
  aroma: AromaCharacteristics (香りの特徴)
  color: ColorDescription (色の説明)
}
```

**値オブジェクト**:
- `ProductId`: 製品の一意識別子
- `RecipeReference`: fermentation-research-bc のレシピへの参照
- `NutritionFacts`: 栄養成分表（100mlあたり）
- `PackageSize`: パッケージサイズと容量
- `AromaCharacteristics`: 香りの特徴（フルーティ、スパイシー等）

**不変条件（Invariants）**:
1. `alcoholContent < 0.5%` の製品のみ `non-alcoholic` タイプを選択可能
2. `alcoholContent` が 1.0%〜3.5% の製品は `low-alcohol` タイプ
3. `developmentStatus == released` には `releasedAt` が必須
4. `limitedInfo` は `limited` タイプの製品のみに設定可能
5. `seasonal` タイプの `availabilityPeriod` は最大3ヶ月

**ビジネスルールの実装**:
```python
class CraftProduct:
    def can_release(self) -> bool:
        return (
            self.developmentStatus == DevelopmentStatus.APPROVED and
            self.has_passed_sensory_evaluation() and
            self.specifications_complete()
        )

    def is_within_sale_period(self) -> bool:
        if not self.limitedInfo or not self.limitedInfo.availabilityPeriod:
            return True  # 通常製品は常に販売可能
        return self.limitedInfo.availabilityPeriod.contains(datetime.now())

    def validate_alcohol_type(self) -> bool:
        if self.productType == ProductType.NON_ALCOHOLIC:
            return self.specifications.alcoholContent < 0.5
        elif self.productType == ProductType.LOW_ALCOHOL:
            return 1.0 <= self.specifications.alcoholContent <= 3.5
        return True
```

---

#### 集約2: DevelopmentProject（開発プロジェクト）

**集約ルート**: DevelopmentProject

**エンティティ**:
```
DevelopmentProject {
  projectId: ProjectId (プロジェクトID)
  projectName: String (プロジェクト名)
  productType: ProductType (開発製品タイプ)
  concept: ProjectConcept (プロジェクトコンセプト)
  phases: List<DevelopmentPhase> (開発フェーズ)
  pilotBatches: List<PilotBatch> (パイロット醸造)
  evaluations: List<Evaluation> (評価履歴)
  technicalRequests: List<TechnicalRequest> (技術相談履歴)
  status: ProjectStatus (planning | active | on-hold | completed | cancelled)
  targetReleaseDate: Date
  actualReleaseDate: Date?
  projectLead: TeamMemberId
  createdAt: DateTime
  updatedAt: DateTime
}

DevelopmentPhase {
  phaseName: String (フェーズ名)
  phaseType: PhaseType (concept | recipe-dev | pilot | evaluation | approval)
  startDate: Date
  endDate: Date?
  status: PhaseStatus (pending | in-progress | completed | skipped)
  deliverables: List<Deliverable> (成果物)
  gateApproval: GateApproval? (ゲート承認)
}

PilotBatch {
  batchId: BatchId
  batchNumber: Integer (バッチ番号)
  brewingDate: Date
  volume: Liters (醸造量)
  recipeVersion: String (使用レシピバージョン)
  parameters: BrewingParameters (醸造パラメータ)
  results: BatchResults? (結果)
  notes: String (備考)
}

Evaluation {
  evaluationId: EvaluationId
  evaluationType: EvaluationType (sensory | consumer | quality)
  evaluationDate: Date
  batchId: BatchId (評価対象バッチ)
  score: Float (総合スコア)
  details: EvaluationDetails (詳細結果)
  evaluatedBy: String (評価者/パネル)
  passed: Boolean (合格判定)
}

TechnicalRequest {
  requestId: RequestId
  requestDate: Date
  targetBC: String (依頼先BC: fermentation-research-bc等)
  requestType: RequestType (strain-consultation | recipe-optimization | technique-inquiry)
  description: String (依頼内容)
  response: TechnicalResponse? (回答)
  status: RequestStatus (pending | responded | closed)
}
```

**値オブジェクト**:
- `ProjectId`: プロジェクトの一意識別子
- `BrewingParameters`: 醸造条件（温度、期間、酵母量等）
- `EvaluationDetails`: 評価の詳細スコア（各項目別）
- `GateApproval`: ゲート承認（承認者、日付、条件）

**不変条件（Invariants）**:
1. `status == completed` には少なくとも1つの `passed == true` の評価が必要
2. `pilotBatches` は最大10バッチまで
3. 次フェーズ開始には前フェーズの `GateApproval` が必要
4. プロジェクト期間は最長12ヶ月（限定品は6ヶ月）

**ビジネスルールの実装**:
```python
class DevelopmentProject:
    def can_proceed_to_next_phase(self) -> bool:
        current_phase = self.get_current_phase()
        if not current_phase or current_phase.status != PhaseStatus.COMPLETED:
            return False
        return current_phase.gateApproval is not None

    def get_best_batch(self) -> Optional[PilotBatch]:
        evaluated_batches = [
            (batch, self.get_evaluation_for_batch(batch.batchId))
            for batch in self.pilotBatches
        ]
        passed_batches = [
            (batch, eval) for batch, eval in evaluated_batches
            if eval and eval.passed
        ]
        if not passed_batches:
            return None
        return max(passed_batches, key=lambda x: x[1].score)[0]

    def is_overdue(self) -> bool:
        return (
            self.status == ProjectStatus.ACTIVE and
            datetime.now().date() > self.targetReleaseDate
        )
```

---

#### 集約3: TrendAnalysis（トレンド分析）

**集約ルート**: TrendAnalysis

**エンティティ**:
```
TrendAnalysis {
  analysisId: AnalysisId
  analysisDate: Date
  analysisType: AnalysisType (market | consumer | competitor | technology)
  title: String (分析タイトル)
  summary: String (サマリー)
  findings: List<Finding> (発見事項)
  recommendations: List<Recommendation> (推奨アクション)
  dataSource: List<DataSource> (データソース)
  validUntil: Date (有効期限)
  createdBy: AnalystId
}

Finding {
  findingId: FindingId
  category: FindingCategory (trend | opportunity | threat | insight)
  description: String (説明)
  evidence: List<Evidence> (エビデンス)
  impact: ImpactLevel (high | medium | low)
  confidence: ConfidenceLevel (high | medium | low)
}

Recommendation {
  recommendationId: RecommendationId
  actionType: ActionType (develop-product | monitor | research | partner)
  description: String (推奨内容)
  priority: Priority (urgent | high | medium | low)
  relatedFindings: List<FindingId>
  estimatedEffort: Effort (small | medium | large)
}

DataSource {
  sourceName: String (ソース名)
  sourceType: SourceType (internal-sales | market-research | competitor-analysis | sns | survey)
  collectionDate: Date
  reliability: ReliabilityLevel (high | medium | low)
}
```

**値オブジェクト**:
- `AnalysisId`: 分析の一意識別子
- `Evidence`: エビデンス（データ、グラフ、引用）
- `ImpactLevel`: 影響度レベル

**不変条件（Invariants）**:
1. `validUntil` は `analysisDate` から最大6ヶ月後
2. 各 `Finding` には最低1つの `Evidence` が必要
3. `confidence == high` には最低3つの独立した `DataSource` が必要

---

#### 集約4: InnovationTechnology（革新技術）

**集約ルート**: InnovationTechnology

**エンティティ**:
```
InnovationTechnology {
  technologyId: TechnologyId
  technologyName: String (技術名)
  sourceBC: String (技術元BC: fermentation-research-bc等)
  sourceReference: String (元レシピID or 実験ID)
  description: String (技術説明)
  applicableProducts: List<ProductType> (適用可能製品タイプ)
  proofOfConcepts: List<ProofOfConcept> (実証記録)
  productizationStatus: ProductizationStatus (exploring | poc | validating | ready | in-production | archived)
  limitations: List<Limitation> (制約事項)
  knownIssues: List<KnownIssue> (既知の課題)
  registeredAt: DateTime
  updatedAt: DateTime
}

ProofOfConcept {
  pocId: PocId
  pocDate: Date
  scale: Scale (10L | 100L | 1000L)
  results: PocResults (実証結果)
  success: Boolean
  learnings: String (学び・気づき)
  conductedBy: TeamMemberId
}

PocResults {
  qualityScore: Float (品質スコア)
  stabilityScore: Float (安定性スコア)
  reproducibility: Boolean (再現性)
  costImpact: CostImpact (increase | neutral | decrease)
  technicalFeasibility: FeasibilityLevel (high | medium | low)
}

Limitation {
  limitationType: String (制約タイプ)
  description: String (説明)
  workaround: String? (回避策)
}
```

**値オブジェクト**:
- `TechnologyId`: 技術の一意識別子
- `PocResults`: 実証結果の詳細
- `CostImpact`: コストへの影響

**不変条件（Invariants）**:
1. `productizationStatus == ready` には最低1つの `success == true` の PoC が必要
2. PoC は最大3回まで（3回失敗で `archived`）
3. `in-production` には関連する `CraftProduct` が存在すること

**ビジネスルールの実装**:
```python
class InnovationTechnology:
    def can_productize(self) -> bool:
        successful_pocs = [poc for poc in self.proofOfConcepts if poc.success]
        return (
            len(successful_pocs) >= 1 and
            self.productizationStatus in [
                ProductizationStatus.VALIDATING,
                ProductizationStatus.READY
            ]
        )

    def should_archive(self) -> bool:
        failed_pocs = [poc for poc in self.proofOfConcepts if not poc.success]
        return len(failed_pocs) >= 3

    def get_latest_poc_results(self) -> Optional[PocResults]:
        if not self.proofOfConcepts:
            return None
        return sorted(self.proofOfConcepts, key=lambda x: x.pocDate)[-1].results
```

---

### 6. ドメインイベント（Domain Events）

#### イベント1: CraftProductReleased（クラフト製品発売）

**イベント名**: `CraftProductReleased`

**ペイロード**:
```json
{
  "eventId": "evt-ci-2025-001",
  "productId": "CRAFT-2025-015",
  "productName": "季節限定 桜ペールエール",
  "productType": "limited",
  "limitationType": "seasonal",
  "specifications": {
    "alcoholContent": 5.5,
    "calories": 45,
    "packagingSizes": ["350ml", "500ml"]
  },
  "availabilityPeriod": {
    "start": "2025-03-01",
    "end": "2025-05-31"
  },
  "targetRegions": ["関東", "関西"],
  "releasedAt": "2025-03-01T00:00:00Z"
}
```

**発生タイミング**:
- `CraftProduct.developmentStatus` が `released` に変更された時
- 販売開始日に到達した時

**購読者（Subscribers）**:
- **brand-marketing-bc (VS3)**: プロモーション開始トリガー
- **sales-distribution-bc (VS4)**: 販売チャネルへの配荷開始
- **inventory-bc**: 在庫管理開始

---

#### イベント2: PilotBatchCompleted（パイロット醸造完了）

**イベント名**: `PilotBatchCompleted`

**ペイロード**:
```json
{
  "eventId": "evt-ci-2025-002",
  "projectId": "PROJ-2025-008",
  "batchId": "BATCH-2025-008-03",
  "batchNumber": 3,
  "brewingDate": "2025-01-20",
  "volume": 500,
  "recipeVersion": "v1.2",
  "results": {
    "alcoholContent": 4.8,
    "bitterness": 25,
    "colorSRM": 12
  },
  "completedAt": "2025-02-05T14:00:00Z"
}
```

**発生タイミング**:
- パイロット醸造が完了し、結果が記録された時

**購読者（Subscribers）**:
- **sensory-evaluation-bc**: 官能評価スケジュール登録
- **quality-management-bc**: 品質検査依頼

---

#### イベント3: TechnologyValidated（技術検証成功）

**イベント名**: `TechnologyValidated`

**ペイロード**:
```json
{
  "eventId": "evt-ci-2025-003",
  "technologyId": "TECH-2025-003",
  "technologyName": "低温ホップ添加法",
  "sourceBC": "fermentation-research-bc",
  "pocResults": {
    "qualityScore": 8.5,
    "stabilityScore": 7.8,
    "reproducibility": true,
    "costImpact": "neutral"
  },
  "applicableProducts": ["craft-beer", "limited"],
  "validatedAt": "2025-01-25T16:00:00Z"
}
```

**発生タイミング**:
- `InnovationTechnology.productizationStatus` が `ready` に変更された時
- PoC が成功し、製品化準備が整った時

**購読者（Subscribers）**:
- **fermentation-research-bc**: 技術フィードバック（成功事例として記録）
- **premium-beer-development-bc**: 技術共有（適用検討）
- **notification-bc**: 関係者への通知

---

#### イベント4: LimitedProductDiscontinued（限定品販売終了）

**イベント名**: `LimitedProductDiscontinued`

**ペイロード**:
```json
{
  "eventId": "evt-ci-2025-004",
  "productId": "CRAFT-2024-042",
  "productName": "冬限定 スパイスエール",
  "limitationType": "seasonal",
  "salesSummary": {
    "totalUnits": 50000,
    "salesPeriod": "2024-11-01 to 2025-01-31",
    "averageRating": 4.2
  },
  "discontinuedAt": "2025-02-01T00:00:00Z",
  "reason": "seasonal-end"
}
```

**発生タイミング**:
- 限定品の販売期間が終了した時
- または在庫完売時

**購読者（Subscribers）**:
- **brand-marketing-bc**: プロモーション終了
- **inventory-bc**: 在庫処分計画
- **analytics-bc**: 販売実績分析トリガー

---

#### イベント5: TrendInsightDiscovered（トレンドインサイト発見）

**イベント名**: `TrendInsightDiscovered`

**ペイロード**:
```json
{
  "eventId": "evt-ci-2025-005",
  "analysisId": "TREND-2025-Q1-003",
  "insightType": "opportunity",
  "title": "低アルコールRTD市場の急成長",
  "summary": "20-30代女性を中心に、アルコール3%以下のRTD需要が前年比40%増加",
  "impact": "high",
  "confidence": "high",
  "recommendedActions": [
    {
      "actionType": "develop-product",
      "description": "3%以下のフルーツRTD新製品開発",
      "priority": "urgent"
    }
  ],
  "discoveredAt": "2025-01-15T10:00:00Z"
}
```

**発生タイミング**:
- トレンド分析で重要な発見があった時
- `Finding.impact == high` かつ `confidence == high` の場合

**購読者（Subscribers）**:
- **strategy-planning-bc (VS0)**: 戦略検討インプット
- **product-planning-bc**: 製品企画への反映
- **executive-dashboard-bc**: 経営ダッシュボード表示

---

### 7. コンテキストマップ（Context Map）

#### 上流（Upstream）コンテキスト

**1. fermentation-research-bc（発酵研究BC）**

**関係パターン**: Conformist（順応者） - 発酵研究BCの用語・構造に従う

**依存内容**:
- 検証済み発酵レシピ
- 特殊酵母株（クラフト向け、ノンアル向け）
- 新発酵技術・手法
- 技術相談・アドバイス

**API依存**:
- `GET /yeast-strains?purpose=craft-beer` - クラフト向け酵母株
- `GET /recipes?status=validated&purpose=craft-beer` - クラフト向けレシピ
- `POST /consultation-requests` - 技術相談

**イベント購読**:
- `YeastStrainDiscovered` → 新酵母の製品適用可能性評価
- `RecipeValidated` → 新レシピの製品化検討
- `ExperimentCompleted` → 新技術の実証検討

---

**2. ingredient-research-bc（素材研究BC）**

**関係パターン**: Customer-Supplier（顧客-供給者）

**依存内容**:
- 特殊素材・フレーバー情報
- 新規原材料の評価データ
- 季節・地域限定素材の調達情報

**API依存**:
- `GET /ingredients?category=specialty` - 特殊素材一覧
- `GET /ingredients/{id}/availability` - 素材の調達可能性

---

**3. sensory-evaluation-bc（官能評価BC）**

**関係パターン**: Customer-Supplier（顧客-供給者）

**依存内容**:
- 官能評価サービス
- 消費者テストの実施
- 評価パネルの手配

**API依存**:
- `POST /evaluation-requests` - 評価依頼
- `GET /evaluations/{requestId}/results` - 評価結果取得

---

#### 下流（Downstream）コンテキスト

**1. brand-marketing-bc（ブランドマーケティングBC, VS3）**

**関係パターン**: Published Language（公開言語）

**提供内容**:
- 製品情報（仕様、ストーリー、ビジュアル）
- 限定品情報（期間、数量、地域）
- 発売スケジュール

**API提供**:
- `GET /products?status=released` - 発売中製品一覧
- `GET /products/{productId}` - 製品詳細
- `GET /products/upcoming` - 発売予定製品

**イベント発行**:
- `CraftProductReleased` → プロモーション開始
- `LimitedProductDiscontinued` → プロモーション終了

---

**2. sales-distribution-bc（販売・流通BC, VS4）**

**関係パターン**: Published Language（公開言語）

**提供内容**:
- 製品仕様（配荷情報）
- 限定品の販売地域・期間
- 数量計画

**API提供**:
- `GET /products/{productId}/distribution-info` - 配荷情報
- `GET /limited-products/schedule` - 限定品スケジュール

---

#### 同格（Partnership）コンテキスト

**1. premium-beer-development-bc（プレミアムビール開発BC）**

**関係パターン**: Partnership（パートナーシップ） - 技術共有

**共有内容**:
- 醸造技術の相互共有
- 成功事例・失敗事例の共有
- 官能評価基準の統一

**連携API**:
- `GET /shared-learnings` - 技術学習の共有
- `POST /technology-share` - 技術情報の共有

---

### コンテキストマップ図

```
                        [ingredient-research-bc]
                                │
                                │ (Customer-Supplier)
                                ↓
[fermentation-research-bc] ────────────────────────────────────┐
        │                                                      │
        │ (Conformist)                                         │
        │ - 酵母株                                              │
        │ - レシピ                                              │
        │ - 新技術                                              │
        ↓                                                      │
┌──────────────────────────────────────────────────────────────┤
│            craft-innovation-development-bc                    │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │CraftProduct │  │Development  │  │Innovation   │          │
│  │             │  │Project      │  │Technology   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌─────────────┐                                             │
│  │TrendAnalysis│                                             │
│  └─────────────┘                                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
        │                         │
        │ (Published Language)    │ (Partnership)
        ↓                         ↓
[brand-marketing-bc]    [premium-beer-development-bc]
[sales-distribution-bc]

        ↓ (Customer-Supplier)
[sensory-evaluation-bc]
```

---

### 8. API概要（参考）

#### 提供API（Downstream BCsへ）

**1. 製品API**

```
GET /api/craft-products
  Query: productType, status, limitationType
  Response: List<CraftProductSummary>

GET /api/craft-products/{productId}
  Response: CraftProductDetail

GET /api/craft-products/upcoming
  Query: releaseDate (from-to)
  Response: List<UpcomingProduct>

GET /api/craft-products/{productId}/story
  Response: BrandStory (マーケティング用ストーリー)
```

**2. 限定品API**

```
GET /api/limited-products/schedule
  Query: year, quarter, limitationType
  Response: LimitedProductSchedule

GET /api/limited-products/{productId}/availability
  Response: AvailabilityInfo (期間、地域、数量)
```

**3. トレンドAPI（内部向け）**

```
GET /api/trends/latest
  Query: category, minImpact
  Response: List<TrendSummary>

GET /api/trends/{analysisId}
  Response: TrendAnalysisDetail
```

---

#### 依存API（Upstream BCsから）

**1. fermentation-research-bc への依存**

```
GET /api/yeast-strains?purpose=craft-beer
  Purpose: クラフト製品向け酵母株の取得

GET /api/recipes/{recipeId}
  Purpose: ベースレシピの詳細取得

POST /api/consultation-requests
  Purpose: 技術相談の依頼
  Request: ConsultationRequest
  Response: ConsultationId
```

**2. sensory-evaluation-bc への依存**

```
POST /api/evaluation-requests
  Purpose: 官能評価の依頼
  Request: EvaluationRequest (batchId, evaluationType)
  Response: EvaluationRequestId

GET /api/evaluations/{requestId}/results
  Purpose: 評価結果の取得
  Response: EvaluationResults
```

---

#### イベント駆動API（Async Integration）

**発行イベント**:
```
CraftProductReleased
PilotBatchCompleted
TechnologyValidated
LimitedProductDiscontinued
TrendInsightDiscovered
```

**購読イベント**:
```
YeastStrainDiscovered (from fermentation-research-bc)
  → 新酵母の製品適用可能性評価

RecipeValidated (from fermentation-research-bc)
  → 新レシピの製品化検討

ExperimentCompleted (from fermentation-research-bc)
  → 新技術の実証検討

EvaluationCompleted (from sensory-evaluation-bc)
  → 開発プロジェクトへの評価結果反映
```

---

## 実装優先順位

### Phase 1: Core Aggregates（最優先）
1. **CraftProduct集約** - 製品管理の基盤
2. **DevelopmentProject集約** - 開発プロセス管理
3. **基本イベント** - CraftProductReleased, PilotBatchCompleted

### Phase 2: Supporting（次優先）
4. **InnovationTechnology集約** - 技術管理
5. **TrendAnalysis集約** - トレンド分析
6. **技術連携イベント** - TechnologyValidated

### Phase 3: Integration（統合）
7. **Context Map実装** - fermentation-research-bc との連携
8. **API公開** - マーケティング・販売BCへのサービス提供
9. **イベント駆動統合** - 非同期連携の完成

---

## まとめ

このBounded Context定義は：

**ビジネス面**:
- クラフト・革新製品の5つの主要オペレーションを詳細化
- 限定品管理（季節・地域・コラボ）のルールを明確化
- ノンアルコール・RTDの法規制対応を業務ルールに反映
- 市場トレンドに基づく製品開発プロセスを構造化

**技術面**:
- 4つの集約でクラフト・革新開発ドメインをモデル化
- 不変条件でビジネスルールを技術的に保証
- ドメインイベントで他BCとの疎結合な連携
- コンテキストマップで境界と関係性を明確化

**DDD原則**:
- ユビキタス言語による業務-技術の一致
- 集約境界による一貫性保証
- イベント駆動による自律性
- 明示的なコンテキスト境界

この定義により、市場トレンドに迅速に対応し、差別化された製品を開発するためのシステムを構築できます。fermentation-research-bcから技術を受け取り、premium-beer-development-bcと技術を共有しながら、革新的な製品を市場に送り出す役割を担います。
