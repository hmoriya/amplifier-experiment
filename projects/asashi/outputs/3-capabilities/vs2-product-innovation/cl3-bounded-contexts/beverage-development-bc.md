# Bounded Context: beverage-development-bc

**サブドメイン**: beverage-development（飲料開発）
**ドメインタイプ**: Core ★★★★☆
**所属活動領域**: A4 飲料・食品開発
**最終更新**: 2025-11-26

---

## 【ビジネス面】

### 1. 責務とビジョン

#### BC名
**beverage-development-bc**（飲料開発バウンデッドコンテキスト）

#### 目的
清涼飲料、乳製品、機能性飲料、健康食品等の非酒類製品の開発を行い、健康・ウェルネス市場への事業多角化を推進する。酒類依存からの脱却と成長市場への対応を担う。

#### 責務
1. **非酒類製品ポートフォリオ管理** - 飲料製品ラインナップの企画・管理
2. **配合・レシピ開発** - 製品の配合研究と最適化
3. **機能性エビデンス構築** - 機能性表示食品の科学的根拠管理
4. **規制対応** - 食品表示法、機能性表示制度への対応
5. **市場適合製品開発** - 健康トレンドに合致した製品創出

#### チーム境界
- **開発チーム**: 食品技術者、フレーバリスト、栄養士
- **規制対応チーム**: 薬事担当、品質保証担当
- **マーケティング連携**: 商品企画担当

---

### 2. ビジネスオペレーション詳細

#### オペレーション1: 清涼飲料開発

**実行手順**:
1. 市場トレンド・消費者ニーズの分析
2. 製品コンセプトの立案（ターゲット、ポジショニング）
3. 配合設計（ベース、フレーバー、甘味料等）
4. 試作品製造と内部評価
5. 安定性試験（賞味期限設定）
6. 官能評価（sensory-evaluationと連携）
7. 量産配合の確定
8. 製造仕様書の作成

**業務ルール**:
- 新製品コンセプトは市場調査データに基づくこと
- 試作は最低3回のイテレーションを実施
- 官能評価スコア80点以上で次ステージへ
- 賞味期限は加速試験で検証（40℃4週間相当）
- 原価率目標は希望小売価格の30%以内

**入力/出力**:
- **入力**: 市場分析レポート、製品コンセプト書、素材情報（ingredient-researchから）
- **出力**: 製品レシピ、製造仕様書、品質規格書

**トリガー**:
- 年間製品開発計画
- 市場トレンド変化（健康志向、低糖質需要等）
- 競合製品の投入

---

#### オペレーション2: 乳製品開発

**実行手順**:
1. 乳酸菌株の選定（functional-ingredientsと連携）
2. 発酵条件の設定（温度、時間、pH目標）
3. 配合設計（乳原料、糖類、香料等）
4. 発酵試験と品質評価
5. 官能評価（酸味、風味、食感）
6. 生菌数安定性の確認
7. パッケージ適性評価
8. 製造工程設計

**業務ルール**:
- 使用乳酸菌は自社保有株または契約株のみ
- 生菌数は製造時10⁸CFU/ml以上を確保
- 賞味期限時の生菌数は規格値の50%以上維持
- 発酵は単一株培養を基本（混合培養は別途承認）
- 乳等省令への適合確認必須

**入力/出力**:
- **入力**: 乳酸菌株情報（functional-ingredientsから）、乳原料規格
- **出力**: 乳製品レシピ、発酵条件書、品質規格書

**トリガー**:
- 新乳酸菌株の供給開始
- 健康効果の新エビデンス取得
- 製品ラインナップ拡充計画

---

#### オペレーション3: 機能性飲料開発

**実行手順**:
1. 機能性成分の選定と配合量決定
2. 機能性エビデンスの確認・収集
3. 機能性表示の検討（届出表示案作成）
4. 配合設計（機能性成分の安定性確保）
5. 臨床試験の計画・実施（必要に応じて）
6. 届出資料の作成
7. 消費者庁への届出
8. 受理後の製品化

**業務ルール**:
- 機能性関与成分は1日摂取目安量で有効量を確保
- エビデンスは査読付き論文または臨床試験データ
- 届出表示は消費者庁ガイドラインに準拠
- 届出前の社内審査（法務・品質保証）必須
- 届出受理まで発売不可

**入力/出力**:
- **入力**: 機能性エビデンスDB（functional-ingredientsから）、成分規格書
- **出力**: 届出資料、機能性飲料レシピ、品質規格書

**トリガー**:
- 新機能性成分の研究完了
- 機能性表示制度の改正
- ヘルスクレーム市場の拡大

---

#### オペレーション4: 健康食品開発

**実行手順**:
1. 健康効果のターゲット設定（疲労回復、腸活等）
2. 有効成分の選定と配合研究
3. 剤形決定（ドリンク、タブレット、ゼリー等）
4. 安定性・溶解性試験
5. 効果実感評価（モニター試験）
6. パッケージ・表示設計
7. 製造委託先選定（必要に応じて）
8. 品質規格の確定

**業務ルール**:
- 医薬品的効能効果の標榜禁止
- 食品衛生法・景品表示法への適合確認
- 有効成分は品質規格（純度、含量）を明確化
- モニター試験は最低30名、4週間以上実施
- 製造委託先はGMP認証取得工場のみ

**入力/出力**:
- **入力**: 健康効果研究データ、素材規格書
- **出力**: 健康食品処方、製品規格書、製造委託仕様書

**トリガー**:
- 健康市場のトレンド変化
- 新素材の供給開始
- 事業ポートフォリオ拡大戦略

---

#### オペレーション5: 低カロリー製品開発

**実行手順**:
1. カロリー削減目標の設定（既存品比○%削減）
2. 代替甘味料・素材の選定
3. 風味プロファイルの設計（甘味質、後味対策）
4. 配合最適化（複数甘味料のブレンド）
5. 官能評価（既存品との比較）
6. 栄養成分分析・表示設計
7. 「カロリーオフ」等の強調表示確認
8. 製品化判定

**業務ルール**:
- 「カロリーオフ」表示は20kcal/100ml以下
- 「カロリーゼロ」表示は5kcal/100ml未満
- 人工甘味料使用時は表示義務遵守
- 官能評価で既存品との差異スコア20%以内
- 原価上昇は希望小売価格の5%以内に抑制

**入力/出力**:
- **入力**: 既存製品レシピ、代替甘味料情報
- **出力**: 低カロリーレシピ、栄養成分表示データ、品質規格書

**トリガー**:
- ダイエット・健康志向の高まり
- 糖質制限トレンド
- 既存製品のリニューアル計画

---

### 3. ビジネスルール

#### 製品開発全般
- 全製品は食品衛生法への適合必須
- アレルゲン表示は7品目＋推奨21品目を確認
- 賞味期限は安全係数0.8を適用
- 製品コードは「BEV-YYYY-NNN」形式で付与

#### 機能性・健康関連
- 機能性表示は消費者庁届出受理後のみ使用可
- 健康強調表示は法務部門の事前承認必須
- エビデンスレベルはシステマティックレビュー以上を推奨

#### 品質管理
- 微生物規格は一般生菌数10⁴CFU/ml以下（清涼飲料）
- 官能評価は5名以上の訓練パネルで実施
- 製品改良時は既存品との同等性確認必須

#### コスト管理
- 開発段階で原価試算を実施
- 目標原価逸脱時は配合見直しまたは承認取得

---

### 4. ユビキタス言語（Ubiquitous Language）

#### 製品関連
- **飲料製品（Beverage Product）**: 非酒類の液体飲料製品
- **清涼飲料（Soft Drink）**: 炭酸・非炭酸の一般飲料
- **乳製品（Dairy Product）**: 乳を主原料とする製品
- **機能性表示食品（Foods with Function Claims）**: 消費者庁届出済みの機能性を表示した食品
- **健康食品（Health Food）**: 健康維持・増進を目的とした食品
- **SKU（Stock Keeping Unit）**: 在庫管理単位となる製品バリエーション

#### 配合・レシピ関連
- **配合（Formulation）**: 製品を構成する原材料とその配合比率
- **ベース（Base）**: 製品の基本となる液体部分
- **フレーバー（Flavor）**: 香味を付与する成分
- **甘味料（Sweetener）**: 甘味を付与する成分（糖類・代替甘味料）
- **Brix（ブリックス）**: 糖度の指標（可溶性固形分%）
- **酸度（Acidity）**: 酸味の指標（クエン酸換算%）

#### 機能性関連
- **機能性関与成分（Functional Component）**: 機能性表示の根拠となる成分
- **エビデンス（Evidence）**: 機能性の科学的根拠
- **届出表示（Notified Claim）**: 消費者庁に届出した機能性表示文言
- **一日摂取目安量（Daily Intake）**: 1日あたりの推奨摂取量
- **臨床試験（Clinical Trial）**: ヒトを対象とした効果検証試験
- **システマティックレビュー（Systematic Review）**: 研究結果の系統的評価

#### 品質関連
- **賞味期限（Best Before Date）**: 品質が保証される期限
- **加速試験（Accelerated Test）**: 高温等で期限を推定する試験
- **安定性試験（Stability Test）**: 経時変化を確認する試験
- **官能評価（Sensory Evaluation）**: 人の感覚による品質評価
- **生菌数（Viable Cell Count）**: 生きた微生物の数

#### 規制関連
- **食品表示法（Food Labeling Act）**: 食品表示に関する法律
- **機能性表示食品制度（FFC System）**: 届出による機能性表示制度
- **乳等省令（Ministerial Ordinance on Milk）**: 乳製品の規格基準
- **強調表示（Emphasis Claim）**: カロリーオフ等の強調した表示

---

## 【技術面】

### 5. 集約（Aggregates）

#### 集約1: BeverageProduct（飲料製品）

**集約ルート**: BeverageProduct

**エンティティ**:
```
BeverageProduct {
  productId: ProductId (識別子)
  productCode: String (製品コード, 例: "BEV-2025-001")
  productName: String (製品名)
  productCategory: ProductCategory (清涼飲料|乳製品|機能性飲料|健康食品)
  brandInfo: BrandInfo (ブランド情報)
  formulation: Formulation (配合情報)
  nutritionFacts: NutritionFacts (栄養成分表示)
  functionalClaims: FunctionalClaimSet? (機能性表示情報)
  qualitySpec: QualitySpecification (品質規格)
  shelfLife: ShelfLife (賞味期限情報)
  regulatoryStatus: RegulatoryStatus (規制対応状況)
  developmentHistory: List<DevelopmentMilestone> (開発履歴)
  status: ProductStatus (planning|developing|testing|approved|discontinued)
  createdAt: DateTime
  updatedAt: DateTime
}

BrandInfo {
  brandId: BrandId
  brandName: String
  targetSegment: String (ターゲット層)
  positioning: String (ポジショニング)
}

Formulation {
  formulationId: FormulationId
  version: Version
  ingredients: List<Ingredient> (原材料リスト)
  baseType: BaseType (水性|乳性|果汁)
  brix: Float (糖度)
  acidity: Float (酸度)
  ph: Float
  processingMethod: ProcessingMethod
}

Ingredient {
  ingredientId: IngredientId
  ingredientName: String
  ratio: Percentage (配合比率)
  function: IngredientFunction (甘味|酸味|香味|機能性|増粘等)
  allergenInfo: AllergenInfo? (アレルゲン情報)
  supplier: SupplierId
}

NutritionFacts {
  servingSize: Volume (1回分の量)
  calories: Float (kcal)
  protein: Float (g)
  fat: Float (g)
  carbohydrate: Float (g)
  sugar: Float (g)
  sodium: Float (mg)
  additionalNutrients: Map<String, NutrientValue>
}

QualitySpecification {
  microbialSpec: MicrobialSpec (微生物規格)
  physicalSpec: PhysicalSpec (物理規格: 色調、濁度等)
  chemicalSpec: ChemicalSpec (化学規格: pH、Brix等)
  sensorySpec: SensorySpec (官能規格)
}

ShelfLife {
  daysFromProduction: Integer (製造日からの日数)
  storageCondition: StorageCondition (保存条件)
  validationMethod: ValidationMethod (検証方法)
  safetyFactor: Float (安全係数, 通常0.8)
}
```

**値オブジェクト**:
- `ProductId`: 飲料製品の一意識別子
- `ProductCategory`: 製品カテゴリ列挙
- `NutrientValue`: 栄養成分値（数値、単位、%DV）
- `AllergenInfo`: アレルゲン情報（7品目＋推奨21品目）

**不変条件（Invariants）**:
1. `productCode`は一意でなければならない
2. `status == approved`の製品のみ製造可能
3. 機能性表示食品は`functionalClaims`必須
4. 全原材料のアレルゲン情報を確認済み
5. 栄養成分表示は食品表示法に準拠
6. 賞味期限は安定性試験で検証済み

**ビジネスルールの実装**:
```python
class BeverageProduct:
    def can_launch(self) -> bool:
        return (
            self.status == ProductStatus.APPROVED and
            self.formulation.is_finalized and
            self.quality_spec.is_validated and
            self.regulatory_status.is_compliant and
            (not self.is_functional_food() or self.functional_claims.is_notified)
        )

    def is_functional_food(self) -> bool:
        return self.product_category == ProductCategory.FUNCTIONAL_BEVERAGE

    def calculate_calories_per_100ml(self) -> float:
        serving = self.nutrition_facts.serving_size.to_ml()
        return (self.nutrition_facts.calories / serving) * 100

    def is_calorie_off(self) -> bool:
        return self.calculate_calories_per_100ml() <= 20

    def is_calorie_zero(self) -> bool:
        return self.calculate_calories_per_100ml() < 5
```

---

#### 集約2: FunctionalClaim（機能性表示）

**集約ルート**: FunctionalClaim

**エンティティ**:
```
FunctionalClaim {
  claimId: ClaimId (識別子)
  productId: ProductId (対象製品)
  functionalComponent: FunctionalComponent (機能性関与成分)
  claimStatement: String (届出表示文)
  targetFunction: TargetFunction (対象機能: 疲労軽減|腸内環境等)
  evidencePackage: EvidencePackage (エビデンスパッケージ)
  notificationInfo: NotificationInfo (届出情報)
  reviewHistory: List<ReviewRecord> (審査履歴)
  status: ClaimStatus (drafting|reviewing|notified|rejected|withdrawn)
  createdAt: DateTime
  notifiedAt: DateTime?
}

FunctionalComponent {
  componentId: ComponentId
  componentName: String (成分名)
  dailyIntake: DailyIntake (一日摂取目安量)
  evidenceLevel: EvidenceLevel (SR|RCT|観察研究)
  safetyData: SafetyData (安全性情報)
}

DailyIntake {
  amount: Float
  unit: Unit (mg|g|CFU等)
  frequency: Frequency (1日1回等)
  timing: String? (食前|食後等)
}

EvidencePackage {
  primaryEvidence: Evidence (主たるエビデンス)
  supportingEvidence: List<Evidence> (補足エビデンス)
  systematicReview: SystematicReviewReport? (SR報告書)
  clinicalTrials: List<ClinicalTrialSummary> (臨床試験)
  mechanismOfAction: String (作用機序)
}

Evidence {
  evidenceId: EvidenceId
  evidenceType: EvidenceType (論文|臨床試験|SR)
  citation: Citation (引用情報)
  studyDesign: StudyDesign
  subjects: SubjectInfo (被験者情報)
  outcome: OutcomeData (結果データ)
  qualityScore: Float (品質スコア)
}

NotificationInfo {
  notificationNumber: String? (届出番号)
  submissionDate: Date (届出日)
  acceptanceDate: Date? (受理日)
  publicationDate: Date? (公表日)
  caComments: List<String>? (消費者庁コメント)
}
```

**値オブジェクト**:
- `ClaimId`: 機能性表示の一意識別子
- `EvidenceLevel`: エビデンスレベル（SR > RCT > 観察研究）
- `Citation`: 文献引用情報（著者、タイトル、雑誌、年、DOI）
- `StudyDesign`: 研究デザイン（RCT、クロスオーバー等）

**不変条件（Invariants）**:
1. `status == notified`でないと表示使用不可
2. エビデンスは最低1件の査読付き論文必須
3. 一日摂取目安量は有効量以上
4. 安全性データは必須
5. 届出番号は受理後に付与

**ビジネスルールの実装**:
```python
class FunctionalClaim:
    def can_use_claim(self) -> bool:
        return (
            self.status == ClaimStatus.NOTIFIED and
            self.notification_info.acceptance_date is not None
        )

    def has_sufficient_evidence(self) -> bool:
        if self.evidence_package.systematic_review:
            return True
        return (
            len(self.evidence_package.clinical_trials) >= 1 and
            any(ct.study_design.is_rct() for ct in self.evidence_package.clinical_trials)
        )

    def validate_daily_intake(self) -> bool:
        effective_dose = self.functional_component.get_effective_dose()
        return self.functional_component.daily_intake.amount >= effective_dose

    def submit_notification(self) -> None:
        if not self.has_sufficient_evidence():
            raise InsufficientEvidenceError("エビデンスが不十分です")
        if not self.validate_daily_intake():
            raise InvalidDailyIntakeError("有効量を満たしていません")

        self.status = ClaimStatus.REVIEWING
        self.notification_info.submission_date = date.today()
        self.add_domain_event(FunctionalClaimSubmittedEvent(
            claim_id=self.claimId,
            product_id=self.productId
        ))
```

---

#### 集約3: BeverageRecipe（飲料レシピ）

**集約ルート**: BeverageRecipe

**エンティティ**:
```
BeverageRecipe {
  recipeId: RecipeId (識別子)
  recipeName: String (レシピ名)
  productCategory: ProductCategory (製品カテゴリ)
  targetProduct: ProductId? (対象製品)
  ingredients: IngredientList (原材料リスト)
  processingSteps: List<ProcessingStep> (製造工程)
  qualityTargets: QualityTargets (品質目標)
  costEstimate: CostEstimate (原価見積)
  validationResults: List<ValidationResult> (検証結果)
  version: Version
  status: RecipeStatus (draft|testing|validated|production)
  createdBy: DeveloperId
  createdAt: DateTime
  approvedBy: ApproverId?
  approvedAt: DateTime?
}

IngredientList {
  items: List<RecipeIngredient>
  totalWeight: Weight (総重量)
  waterRatio: Percentage (水分比率)
}

RecipeIngredient {
  ingredientId: IngredientId
  ingredientName: String
  gradeSpec: String (グレード・規格)
  ratio: Percentage (配合比率, 重量%)
  function: IngredientFunction
  alternativeOptions: List<AlternativeIngredient>? (代替原料)
  supplierConstraint: SupplierConstraint? (供給元制約)
}

ProcessingStep {
  stepNumber: Integer
  stepName: String (工程名)
  operation: Operation (混合|加熱|冷却|殺菌|充填等)
  parameters: ProcessParameters (温度、時間、圧力等)
  equipment: EquipmentSpec (使用設備)
  controlPoints: List<ControlPoint> (管理ポイント)
  duration: Duration
}

QualityTargets {
  brixRange: Range<Float> (糖度範囲)
  acidityRange: Range<Float> (酸度範囲)
  phRange: Range<Float> (pH範囲)
  colorSpec: ColorSpec (色調規格)
  flavorProfile: FlavorProfile (風味プロファイル)
  microbiologicalLimit: MicrobiologicalLimit (微生物規格)
}

CostEstimate {
  ingredientCost: Money (原材料費)
  packagingCost: Money (包材費)
  processingCost: Money (加工費)
  totalCost: Money (合計原価)
  targetRetailPrice: Money (希望小売価格)
  costRatio: Percentage (原価率)
}
```

**値オブジェクト**:
- `RecipeId`: レシピの一意識別子
- `ProcessParameters`: 工程パラメータ（温度、時間、圧力等の複合値）
- `FlavorProfile`: 風味プロファイル（甘味、酸味、苦味、香りの多次元評価）
- `ControlPoint`: 管理ポイント（測定項目、基準値、許容範囲）

**不変条件（Invariants）**:
1. `status == production`のレシピは3回以上の検証必須
2. 原材料配合比率の合計は100%
3. 殺菌工程は必須（清涼飲料）
4. 原価率は目標値以内
5. 全工程にCCPまたは管理ポイント設定

**ビジネスルールの実装**:
```python
class BeverageRecipe:
    def can_promote_to_production(self) -> bool:
        return (
            len(self.validation_results) >= 3 and
            all(v.passed for v in self.validation_results) and
            self.cost_estimate.cost_ratio <= 0.30 and  # 30%以内
            self.approved_by is not None
        )

    def calculate_cost_ratio(self) -> float:
        return self.cost_estimate.total_cost / self.cost_estimate.target_retail_price

    def validate_ingredient_ratio(self) -> bool:
        total = sum(ing.ratio for ing in self.ingredients.items)
        return abs(total - 100.0) < 0.1  # 許容誤差0.1%

    def has_sterilization_step(self) -> bool:
        return any(
            step.operation == Operation.STERILIZATION
            for step in self.processing_steps
        )

    def finalize(self, approver: ApproverId) -> None:
        if not self.can_promote_to_production():
            raise RecipeNotReadyError("製造移行の条件を満たしていません")

        self.status = RecipeStatus.PRODUCTION
        self.approved_by = approver
        self.approved_at = datetime.now()
        self.add_domain_event(RecipeValidatedEvent(
            recipe_id=self.recipeId,
            product_category=self.productCategory
        ))
```

---

#### 集約4: DevelopmentProject（開発プロジェクト）

**集約ルート**: DevelopmentProject

**エンティティ**:
```
DevelopmentProject {
  projectId: ProjectId (識別子)
  projectCode: String (プロジェクトコード)
  projectName: String
  productCategory: ProductCategory
  projectType: ProjectType (新製品|リニューアル|ライン拡張)
  marketingBrief: MarketingBrief (マーケティングブリーフ)
  developmentPhase: DevelopmentPhase (企画|開発|試作|量産準備|完了)
  timeline: ProjectTimeline (スケジュール)
  team: ProjectTeam (プロジェクトチーム)
  deliverables: List<Deliverable> (成果物)
  gateReviews: List<GateReview> (ステージゲートレビュー)
  risks: List<ProjectRisk> (リスク)
  status: ProjectStatus (active|on_hold|completed|cancelled)
  createdAt: DateTime
  completedAt: DateTime?
}

MarketingBrief {
  targetConsumer: String (ターゲット消費者)
  productConcept: String (製品コンセプト)
  keyBenefits: List<String> (主要ベネフィット)
  competitivePosition: String (競合ポジショニング)
  pricePoint: PriceRange (価格帯)
  launchTiming: Date (発売時期目標)
  volumeTarget: Volume (販売数量目標)
}

ProjectTimeline {
  startDate: Date
  plannedEndDate: Date
  milestones: List<Milestone>
  criticalPath: List<TaskId>
}

GateReview {
  gateNumber: Integer (ゲート番号)
  gateName: String (G1:コンセプト承認, G2:開発承認, G3:量産承認等)
  reviewDate: Date
  reviewers: List<ReviewerId>
  decision: GateDecision (go|conditional_go|hold|kill)
  conditions: List<String>? (条件付き承認の条件)
  notes: String
}

Deliverable {
  deliverableId: DeliverableId
  deliverableName: String
  deliverableType: DeliverableType (レシピ|規格書|届出資料等)
  dueDate: Date
  status: DeliverableStatus (pending|in_progress|completed|approved)
  documentRef: DocumentReference?
}
```

**値オブジェクト**:
- `ProjectId`: プロジェクトの一意識別子
- `GateDecision`: ゲート判定結果（Go/Conditional Go/Hold/Kill）
- `PriceRange`: 価格帯（下限、上限、目標価格）
- `Milestone`: マイルストーン（名称、日付、依存関係）

**不変条件（Invariants）**:
1. ゲート承認なしで次フェーズ移行不可
2. 必須成果物の完了が次ゲートの前提条件
3. `status == completed`には全ゲート承認必須
4. プロジェクトコードは一意

**ビジネスルールの実装**:
```python
class DevelopmentProject:
    def can_proceed_to_next_phase(self) -> bool:
        current_gate = self.get_current_gate()
        if not current_gate:
            return False
        return current_gate.decision in [GateDecision.GO, GateDecision.CONDITIONAL_GO]

    def get_current_gate(self) -> GateReview | None:
        phase_gate_map = {
            DevelopmentPhase.PLANNING: 1,
            DevelopmentPhase.DEVELOPMENT: 2,
            DevelopmentPhase.PROTOTYPING: 3,
            DevelopmentPhase.PRODUCTION_PREP: 4,
        }
        gate_number = phase_gate_map.get(self.development_phase)
        return next(
            (g for g in self.gate_reviews if g.gate_number == gate_number),
            None
        )

    def complete_gate_review(self, gate: GateReview) -> None:
        self.gate_reviews.append(gate)
        if gate.decision == GateDecision.GO:
            self.advance_phase()
            self.add_domain_event(GatePassedEvent(
                project_id=self.projectId,
                gate_number=gate.gate_number
            ))
        elif gate.decision == GateDecision.KILL:
            self.status = ProjectStatus.CANCELLED
            self.add_domain_event(ProjectCancelledEvent(
                project_id=self.projectId,
                reason="Gate review decision: Kill"
            ))
```

---

### 6. ドメインイベント（Domain Events）

#### イベント1: BeverageProductCreated（飲料製品登録）

**イベント名**: `BeverageProductCreated`

**ペイロード**:
```json
{
  "eventId": "evt-bev-2025-001",
  "productId": "BEV-2025-001",
  "productCode": "BEV-2025-001",
  "productName": "健康サポート緑茶",
  "productCategory": "functional_beverage",
  "brandInfo": {
    "brandId": "brand-health-001",
    "brandName": "ヘルシアプラス"
  },
  "developmentProjectId": "proj-2025-010",
  "createdBy": "developer-005",
  "timestamp": "2025-11-26T10:00:00Z"
}
```

**発生タイミング**:
- 新規飲料製品が`BeverageProduct`集約に登録された時
- 開発プロジェクトから製品マスターに移行した時

**購読者（Subscribers）**:
- **sensory-evaluation-bc**: 官能評価スケジュール登録
- **quality-management-bc**: 品質規格の設定開始
- **notification-bc**: 関係者への通知

---

#### イベント2: RecipeValidated（レシピ検証完了）

**イベント名**: `RecipeValidated`

**ペイロード**:
```json
{
  "eventId": "evt-bev-2025-002",
  "recipeId": "recipe-bev-2025-015",
  "recipeName": "機能性緑茶レシピ v2.0",
  "productCategory": "functional_beverage",
  "validationCount": 3,
  "validationResults": [
    {"date": "2025-11-10", "passed": true, "score": 92},
    {"date": "2025-11-15", "passed": true, "score": 94},
    {"date": "2025-11-20", "passed": true, "score": 95}
  ],
  "costRatio": 0.28,
  "approvedBy": "senior-developer-002",
  "validatedAt": "2025-11-26T14:00:00Z"
}
```

**発生タイミング**:
- レシピが3回以上の検証に成功した時
- 承認者によりレシピが承認され、`status = production`に変更された時

**購読者（Subscribers）**:
- **prototype-production-bc**: 量産試作スケジュール登録
- **production-planning-bc**: 生産計画への組込可否判断
- **cost-management-bc**: 原価データの登録

---

#### イベント3: FunctionalClaimNotified（機能性表示届出受理）

**イベント名**: `FunctionalClaimNotified`

**ペイロード**:
```json
{
  "eventId": "evt-bev-2025-003",
  "claimId": "claim-2025-008",
  "productId": "BEV-2025-001",
  "notificationNumber": "I1234",
  "claimStatement": "本品には〇〇が含まれ、△△の機能があることが報告されています。",
  "functionalComponent": {
    "componentName": "カテキン",
    "dailyIntake": "540mg"
  },
  "submissionDate": "2025-10-01",
  "acceptanceDate": "2025-11-25",
  "timestamp": "2025-11-26T09:00:00Z"
}
```

**発生タイミング**:
- 消費者庁から届出が受理された時
- `FunctionalClaim.status = notified`に変更された時

**購読者（Subscribers）**:
- **marketing-bc**: 機能性表示を活用したプロモーション準備
- **packaging-design-bc**: パッケージ表示の更新
- **legal-compliance-bc**: 表示コンプライアンス確認

---

#### イベント4: GatePassed（ゲート通過）

**イベント名**: `GatePassed`

**ペイロード**:
```json
{
  "eventId": "evt-bev-2025-004",
  "projectId": "proj-2025-010",
  "projectCode": "PROJ-BEV-2025-010",
  "gateNumber": 3,
  "gateName": "量産準備承認",
  "decision": "go",
  "currentPhase": "production_prep",
  "nextMilestone": "量産開始",
  "passedAt": "2025-11-26T16:00:00Z"
}
```

**発生タイミング**:
- ステージゲートレビューでGo判定を受けた時
- プロジェクトが次フェーズに移行した時

**購読者（Subscribers）**:
- **project-management-bc**: プロジェクト進捗更新
- **resource-planning-bc**: リソース配分調整
- **notification-bc**: ステークホルダーへの通知

---

#### イベント5: ProductLaunched（製品発売）

**イベント名**: `ProductLaunched`

**ペイロード**:
```json
{
  "eventId": "evt-bev-2025-005",
  "productId": "BEV-2025-001",
  "productCode": "BEV-2025-001",
  "productName": "健康サポート緑茶",
  "productCategory": "functional_beverage",
  "launchDate": "2025-12-01",
  "launchRegion": "全国",
  "channels": ["convenience_store", "supermarket", "ec"],
  "initialSKUs": ["500ml_PET", "350ml_PET"],
  "timestamp": "2025-12-01T00:00:00Z"
}
```

**発生タイミング**:
- 製品が市場投入された時
- `BeverageProduct.status = launched`に変更された時

**購読者（Subscribers）**:
- **sales-management-bc**: 販売開始
- **inventory-management-bc**: 在庫管理開始
- **customer-feedback-bc**: VOC収集開始

---

### 7. コンテキストマップ（Context Map）

#### 上流（Upstream）コンテキスト

**1. functional-ingredients-bc（機能性成分研究BC）**

**関係パターン**: Customer-Supplier（顧客-供給者）

**依存内容**:
- 乳酸菌株情報（株名、特性、培養条件）
- 機能性成分のエビデンスデータ
- 微生物バンクからの株供給

**API依存**:
- `GET /functional-components/{componentId}` - 機能性成分詳細取得
- `GET /lactic-acid-bacteria/{strainId}` - 乳酸菌株情報
- `GET /evidence/{componentId}` - エビデンスパッケージ取得

**データ同期**:
- 新エビデンス取得時にイベント連携
- 乳酸菌株の供給可否をリアルタイム確認

---

**2. ingredient-research-bc（素材研究BC）**

**関係パターン**: Customer-Supplier（顧客-供給者）

**依存内容**:
- 飲料素材の特性データ
- 配合技術の知見
- サプライヤー評価情報

**API依存**:
- `GET /ingredients/{ingredientId}` - 素材詳細取得
- `GET /ingredients/search?category=beverage` - 飲料用素材検索
- `GET /formulation-guides` - 配合ガイドライン

---

#### 下流（Downstream）コンテキスト

**1. sensory-evaluation-bc（官能評価BC）**

**関係パターン**: Customer-Supplier（当BCが供給者）

**提供内容**:
- 評価対象製品の情報
- 品質規格・評価基準
- 試作品サンプル手配

**API提供**:
- `POST /evaluation-requests` - 官能評価依頼
- `GET /products/{productId}/evaluation-spec` - 評価基準取得

**イベント連携**:
- `BeverageProductCreated` → 官能評価スケジュール登録
- `RecipeValidated` → 最終官能評価の実施

---

**2. prototype-production-bc（試作生産BC）**

**関係パターン**: Customer-Supplier（当BCが供給者）

**提供内容**:
- 検証済みレシピ
- 製造仕様・工程条件
- 品質規格

**API提供**:
- `GET /recipes/{recipeId}` - レシピ詳細取得
- `GET /recipes/{recipeId}/production-spec` - 製造仕様取得
- `POST /prototype-requests` - 試作依頼

---

**3. production-planning-bc（生産計画BC）**

**関係パターン**: Published Language（公開言語）

**提供内容**:
- 量産用レシピ（`status=production`のみ）
- 製品マスター情報
- 品質規格

**API提供**:
- `GET /production-recipes` - 量産用レシピ一覧
- `GET /products/{productId}/master` - 製品マスター取得

---

#### 連携（Peer）コンテキスト

**1. quality-management-bc（品質管理BC）**

**関係パターン**: Shared Kernel（共有カーネル）

**共有概念**:
- 品質規格（微生物、理化学、官能）
- 賞味期限設定基準
- アレルゲン管理基準

**双方向API**:
- `POST /quality-specs` - 品質規格登録（当BC→品質管理）
- `GET /quality-standards` - 品質基準取得（品質管理→当BC）
- `POST /shelf-life-validation` - 賞味期限検証依頼

---

#### 汎用サブドメイン（Generic Subdomain）との関係

**1. regulatory-compliance-bc（規制対応BC）**

**関係パターン**: Anti-Corruption Layer（腐敗防止層）

**連携内容**:
- 機能性表示届出の代行
- 食品表示法チェック
- 規制動向情報の提供

**アダプター層**:
```python
class RegulatoryComplianceAdapter:
    def submit_functional_claim(self, claim: FunctionalClaim) -> SubmissionResult:
        # 当BCのドメインモデルを規制対応BCのフォーマットに変換
        submission_data = self.transform_to_submission_format(claim)
        return regulatory_service.submit(submission_data)

    def check_labeling_compliance(self, product: BeverageProduct) -> ComplianceResult:
        labeling_data = self.extract_labeling_info(product)
        return regulatory_service.validate_labeling(labeling_data)
```

---

### コンテキストマップ図

```
[functional-ingredients-bc]     [ingredient-research-bc]
         │                              │
         │ (Customer-Supplier)          │ (Customer-Supplier)
         ↓                              ↓
    ┌────────────────────────────────────────┐
    │                                        │
    │    [beverage-development-bc]          │
    │                                        │
    └──────────────┬─────────────────────────┘
                   │
         ┌─────────┼─────────┬─────────────┐
         │         │         │             │
         ↓         ↓         ↓             ↓
[sensory-      [prototype-  [production-  [quality-
 evaluation]    production]  planning]    management]
                                          (Shared Kernel)

         ↓ (ACL)
[regulatory-compliance-bc] (Generic)
```

---

### 8. API概要（参考）

#### 提供API（Downstream BCsへ）

**1. 製品管理API**

```
GET /api/beverage-products
  Query: category=[soft_drink|dairy|functional|health_food], status=[developing|approved]
  Response: List<BeverageProductSummary>

GET /api/beverage-products/{productId}
  Response: BeverageProductDetail (配合、栄養成分、品質規格)

GET /api/beverage-products/{productId}/formulation
  Response: FormulationDetail (原材料リスト、配合比率)

POST /api/beverage-products/{productId}/evaluation-request
  Request: EvaluationRequestData
  Response: EvaluationRequestId
```

**2. レシピ管理API**

```
GET /api/recipes
  Query: category, status=[draft|testing|validated|production]
  Response: List<RecipeSummary>

GET /api/recipes/{recipeId}
  Response: RecipeDetail (原材料、工程、品質目標)

GET /api/recipes/{recipeId}/production-spec
  Response: ProductionSpecification (量産用製造仕様)

POST /api/recipes/{recipeId}/validation-result
  Request: ValidationResultData
  Response: ValidationRecordId
```

**3. 機能性表示API**

```
GET /api/functional-claims
  Query: status=[drafting|notified], productId
  Response: List<FunctionalClaimSummary>

GET /api/functional-claims/{claimId}
  Response: FunctionalClaimDetail (届出表示、エビデンス)

GET /api/functional-claims/{claimId}/evidence-package
  Response: EvidencePackageDetail (エビデンス詳細)

POST /api/functional-claims
  Request: FunctionalClaimCreateRequest
  Response: ClaimId
```

**4. プロジェクト管理API**

```
GET /api/development-projects
  Query: status=[active|completed], category
  Response: List<ProjectSummary>

GET /api/development-projects/{projectId}
  Response: ProjectDetail (フェーズ、成果物、ゲートレビュー)

GET /api/development-projects/{projectId}/timeline
  Response: ProjectTimeline (スケジュール、マイルストーン)

POST /api/development-projects/{projectId}/gate-reviews
  Request: GateReviewData
  Response: GateReviewResult
```

---

#### 依存API（Upstream BCsから）

**1. functional-ingredients-bcへの依存**

```
GET /api/functional-components/{componentId}
  Purpose: 機能性関与成分の詳細取得
  Usage: 機能性飲料開発時

GET /api/lactic-acid-bacteria/available
  Purpose: 使用可能な乳酸菌株リスト取得
  Usage: 乳製品開発時

GET /api/evidence-packages/{componentId}
  Purpose: エビデンスパッケージ取得
  Usage: 機能性表示届出準備時
```

**2. ingredient-research-bcへの依存**

```
GET /api/ingredients?category=beverage
  Purpose: 飲料用素材の検索
  Usage: 配合設計時

GET /api/ingredients/{ingredientId}/spec
  Purpose: 素材規格詳細取得
  Usage: レシピ作成時
```

---

#### イベント駆動API（Async Integration）

**発行イベント**:
```
BeverageProductCreated
RecipeValidated
FunctionalClaimNotified
GatePassed
ProductLaunched
```

**購読イベント**:
```
FunctionalEvidenceUpdated (from functional-ingredients-bc)
  → 機能性エビデンスの更新反映

IngredientSpecUpdated (from ingredient-research-bc)
  → 素材規格変更時のレシピ見直し

SensoryEvaluationCompleted (from sensory-evaluation-bc)
  → 官能評価結果の製品情報反映

QualityStandardUpdated (from quality-management-bc)
  → 品質規格の更新反映
```

---

## 実装優先順位

### Phase 1: Core Aggregates（最優先）
1. **BeverageProduct集約** - 飲料製品管理の基盤
2. **BeverageRecipe集約** - レシピ管理
3. **基本イベント** - BeverageProductCreated, RecipeValidated

### Phase 2: 機能性対応（次優先）
4. **FunctionalClaim集約** - 機能性表示管理
5. **エビデンス連携** - functional-ingredients-bcとの統合
6. **届出管理** - 機能性表示届出フロー

### Phase 3: プロジェクト管理（統合）
7. **DevelopmentProject集約** - 開発プロジェクト管理
8. **ゲートレビュー** - ステージゲートプロセス
9. **Context Map実装** - 他BCとの連携

---

## まとめ

このBounded Context定義は：

**ビジネス面**:
- 5つの主要オペレーション（清涼飲料、乳製品、機能性飲料、健康食品、低カロリー製品）を詳細化
- 機能性表示食品制度への対応を業務フローに組込み
- 食品業界特有の規制・品質要件をビジネスルールに反映
- 健康・ウェルネス市場への戦略的対応を構造化

**技術面**:
- 4つの集約（製品、機能性表示、レシピ、プロジェクト）で飲料開発ドメインをモデル化
- 不変条件でビジネスルール（規制対応、品質基準）を技術的に保証
- ドメインイベントで関連BCとの疎結合な連携
- コンテキストマップで機能性成分研究・素材研究との依存関係を明確化

**DDD原則**:
- ユビキタス言語による業務-技術の一致（食品業界用語の統一）
- 集約境界による一貫性保証
- イベント駆動による自律性
- 明示的なコンテキスト境界と統合パターン

この定義により、成長市場（健康・ウェルネス）への事業多角化を支える飲料開発ドメインを、規制対応と品質保証を組み込んだシステムとして実装できます。
