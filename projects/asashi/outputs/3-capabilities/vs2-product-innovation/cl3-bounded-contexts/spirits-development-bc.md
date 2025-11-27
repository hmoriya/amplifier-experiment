# Bounded Context: spirits-development-bc

**サブドメイン**: spirits-development（スピリッツ開発）
**ドメインタイプ**: Core ★★★☆☆
**所属活動領域**: A3 酒類製品開発
**最終更新**: 2025-11-27

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**spirits-development-bc**（スピリッツ開発バウンデッドコンテキスト）

#### 目的
ウイスキー、スピリッツ、リキュール等の蒸留酒製品の開発を行い、高付加価値カテゴリーとしての成長を実現する。長期熟成を前提とした計画的な製品開発と、プレミアム市場でのブランド価値向上を担う。

#### 責務
1. **ウイスキー開発** - ブレンド・シングルモルトウイスキーの企画・開発
2. **スピリッツ開発** - ジン・ウォッカ等のホワイトスピリッツ開発
3. **熟成管理** - 樽熟成プロセスの品質管理・最適化
4. **ブレンド設計** - 最適なブレンド配合の設計・調整

#### チーム境界
- **開発チーム**: マスターブレンダー、ディスティラー、熟成管理担当
- **品質チーム**: 品質管理担当、官能評価パネリスト
- **技術連携**: fermentation-research-bc からの蒸留用酵母技術受領者

---

### 2. ビジネスオペレーション詳細

#### オペレーション1: ウイスキー開発

**実行手順**:
1. 製品コンセプト策定（ターゲット市場、価格帯、味わいプロファイル）
2. 原酒選定（モルト、グレーンの組み合わせ検討）
3. 熟成計画の策定（樽種類、熟成期間、倉庫選定）
4. fermentation-research-bc への蒸留用酵母相談
5. 蒸留条件の設計（カット点、蒸留回数）
6. パイロット蒸留・熟成
7. 官能評価（熟成途中サンプリング）
8. ブレンド設計（ブレンドウイスキーの場合）
9. 製品仕様確定・ボトリング計画

**業務ルール**:
- シングルモルトは最低3年熟成必須（酒税法準拠）
- ブレンドウイスキーは最低5種類以上の原酒を使用
- 熟成途中サンプリングは年2回（春・秋）実施
- マスターブレンダーの最終承認必須
- 官能評価スコア8.0以上で製品化可能

**入力/出力**:
- **入力**: 市場要件、原酒在庫情報、熟成樽情報
- **出力**: ウイスキー製品仕様書、ブレンドレシピ、熟成計画書

**トリガー**:
- 年間製品計画サイクル
- 熟成原酒の成熟（5年・10年・15年節目）
- プレミアム市場でのビジネス機会

---

#### オペレーション2: スピリッツ開発

**実行手順**:
1. 市場トレンド分析（クラフトジン、プレミアムウォッカ等）
2. ベーススピリッツ設計（原料、蒸留方法）
3. ボタニカル/フレーバー選定（ジンの場合）
4. fermentation-research-bc への酵母・発酵技術相談
5. パイロット蒸留（複数バッチ）
6. 後処理設計（ろ過、加水、フレーバリング）
7. 官能評価・消費者テスト
8. パッケージ設計（プレミアム感の演出）
9. 製品仕様確定

**業務ルール**:
- ジンはジュニパーベリー使用必須（EU規制準拠）
- ウォッカはアルコール度数37.5%以上（国際基準）
- クラフトスピリッツは小規模蒸留器（500L以下）使用
- ボタニカル数は最大12種類（品質管理上の制約）
- 官能評価スコア7.5以上で製品化可能

**入力/出力**:
- **入力**: 市場トレンドデータ、ボタニカルリスト、蒸留技術仕様
- **出力**: スピリッツ製品仕様書、ボタニカルレシピ

**トリガー**:
- クラフトスピリッツ市場の成長
- 新規ボタニカル/フレーバートレンド
- 競合製品の発売

---

#### オペレーション3: 熟成管理

**実行手順**:
1. 新樽/リフィル樽の受入検査
2. 樽への充填・シーリング
3. 熟成倉庫への配置（温湿度条件を考慮）
4. 定期サンプリング・品質モニタリング
5. 熟成進捗の記録（色、香り、味わいの変化）
6. 樽ローテーション（必要に応じて）
7. 熟成完了判定（マスターブレンダー承認）
8. 原酒として払出し/在庫化

**業務ルール**:
- 新樽使用率は年間10%以下（コスト管理）
- リフィル樽は最大3回使用まで
- 熟成倉庫温度: 10-20℃（年間平均）
- 天使の分け前（Angel's Share）: 年2-4%を許容
- 15年以上熟成原酒は特別管理（資産価値）

**入力/出力**:
- **入力**: 蒸留原酒、樽情報、熟成計画
- **出力**: 熟成原酒、熟成品質記録、在庫情報

**トリガー**:
- 新樽/リフィル樽の入荷
- 定期サンプリングスケジュール（春・秋）
- 製品開発からの原酒要求

---

#### オペレーション4: ブレンド設計

**実行手順**:
1. 製品コンセプトの確認（目標味わいプロファイル）
2. 原酒在庫の棚卸し・評価
3. キー原酒の選定（核となる原酒）
4. サポート原酒の選定（複雑性・深みの付加）
5. 試験ブレンド作成（複数バリエーション）
6. 官能評価・比較テスト
7. 最終ブレンド比率の決定
8. スケールアップブレンド検証
9. ブレンドレシピの確定・文書化

**業務ルール**:
- ブレンドレシピは最重要機密（アクセス制限）
- 試験ブレンドは最低5パターン作成
- マスターブレンダー以外のブレンド比率変更不可
- 原酒の品質等級に応じた使用制限あり
- コスト制約内での最適化が必要

**入力/出力**:
- **入力**: 製品コンセプト、原酒在庫、品質データ
- **出力**: ブレンドレシピ、試験ブレンドサンプル、官能評価結果

**トリガー**:
- 新製品開発プロジェクト開始
- 既存製品のリニューアル
- 限定品・記念品の企画

---

### 3. ビジネスルール

#### 熟成管理
| ルール | 内容 | 根拠 |
|--------|------|------|
| BR-SP-001 | ウイスキーは最低3年熟成 | 酒税法 |
| BR-SP-002 | シングルモルトは単一蒸留所の原酒のみ使用 | 業界規定 |
| BR-SP-003 | 熟成倉庫温度10-20℃維持 | 品質管理 |
| BR-SP-004 | 天使の分け前は年4%まで許容 | 品質基準 |

#### 品質基準
| ルール | 内容 | 適用 |
|--------|------|------|
| BR-SP-010 | ウイスキー官能評価8.0以上 | 製品化判定 |
| BR-SP-011 | スピリッツ官能評価7.5以上 | 製品化判定 |
| BR-SP-012 | マスターブレンダー承認必須 | 全製品 |

#### ブレンド管理
| ルール | 内容 | 理由 |
|--------|------|------|
| BR-SP-020 | ブレンドレシピのアクセス制限 | 企業秘密 |
| BR-SP-021 | 試験ブレンド最低5パターン | 品質確保 |
| BR-SP-022 | 原酒等級による使用制限 | 資産管理 |

---

### 4. ユビキタス言語（Ubiquitous Language）

#### 製品関連
- **シングルモルト（Single Malt）**: 単一蒸留所のモルト原酒のみで作られたウイスキー
- **ブレンデッド（Blended）**: 複数の原酒をブレンドしたウイスキー
- **クラフトスピリッツ（Craft Spirits）**: 小規模蒸留所で製造されるプレミアムスピリッツ
- **ボタニカル（Botanical）**: ジン等に使用する植物由来の香味成分

#### 熟成関連
- **原酒（Cask Strength Spirit）**: 熟成された蒸留酒（加水前）
- **樽（Cask）**: 熟成に使用する木製容器
- **新樽（Virgin Cask）**: 未使用の樽
- **リフィル樽（Refill Cask）**: 再使用の樽
- **天使の分け前（Angel's Share）**: 熟成中の蒸発ロス
- **熟成年数（Age Statement）**: 最若い原酒の熟成年数

#### ブレンド関連
- **マスターブレンダー（Master Blender）**: ブレンド設計の最高責任者
- **キー原酒（Key Malt）**: ブレンドの核となる原酒
- **サポート原酒（Support Malt）**: 複雑性を加える補助原酒
- **ブレンドレシピ（Blend Recipe）**: 原酒の配合比率

#### 蒸留関連
- **カット点（Cut Point）**: 蒸留時の前留・本留・後留の分離点
- **ポットスチル（Pot Still）**: 単式蒸留器
- **連続式蒸留（Column Still）**: グレーンウイスキー用蒸留器

---

## 【技術面】

### 5. 集約設計（Aggregates）

#### 集約1: SpiritsProduct（スピリッツ製品）

**集約ルート**: SpiritsProduct

**エンティティ**:
```
SpiritsProduct {
  productId: ProductId (識別子)
  productCode: String (製品コード, 例: "WHISKY-2025-001")
  productName: String (製品名)
  productCategory: ProductCategory (single-malt | blended | gin | vodka | liqueur)
  specifications: SpiritsSpecifications (製品仕様)
  blendRecipe: BlendRecipe? (ブレンドレシピ, ブレンド製品のみ)
  maturationInfo: MaturationInfo? (熟成情報, 熟成製品のみ)
  developmentStatus: DevelopmentStatus (concept | development | aging | blending | approved | released)
  masterBlenderApproval: Approval? (マスターブレンダー承認)
  createdAt: DateTime
  updatedAt: DateTime
  releasedAt: DateTime?
}

SpiritsSpecifications {
  alcoholContent: Percentage (アルコール度数)
  volumeOptions: List<Volume> (容量オプション: 700ml, 750ml等)
  tastingNotes: TastingNotes (テイスティングノート)
  ingredients: List<Ingredient> (原材料)
  distilleryOrigin: String? (蒸留所)
  ageStatement: Years? (熟成年数表記)
}

TastingNotes {
  nose: List<String> (香り: スモーキー、フルーティ等)
  palate: List<String> (味わい: スパイシー、甘美等)
  finish: List<String> (余韻: 長い、ドライ等)
  colorDescription: String (色の説明)
}

BlendRecipe {
  recipeId: RecipeId
  recipeVersion: String
  components: List<BlendComponent> (配合成分)
  totalVolume: Liters
  masterBlenderId: BlenderId
  approvedAt: DateTime?
  isConfidential: Boolean = true
}

BlendComponent {
  caskId: CaskId (使用原酒)
  percentage: Percentage (配合比率)
  age: Years (原酒熟成年数)
  type: CaskType (malt | grain)
  role: ComponentRole (key | support | accent)
}
```

**値オブジェクト**:
- `ProductId`: 製品の一意識別子
- `TastingNotes`: 官能評価ノート
- `BlendRecipe`: ブレンド配合（機密情報）
- `Approval`: マスターブレンダー承認記録

**不変条件（Invariants）**:
1. `productCategory == single-malt` の場合、`blendRecipe` は単一蒸留所原酒のみ
2. `ageStatement` は `blendRecipe` 内の最若原酒の年数以下
3. `developmentStatus == released` には `masterBlenderApproval` が必須
4. `alcoholContent` はカテゴリ基準を満たすこと（ウォッカ37.5%以上等）

**ビジネスルールの実装**:
```python
class SpiritsProduct:
    def can_release(self) -> bool:
        return (
            self.developmentStatus == DevelopmentStatus.APPROVED and
            self.masterBlenderApproval is not None and
            self.has_passed_sensory_evaluation()
        )

    def validate_age_statement(self) -> bool:
        if not self.maturationInfo or not self.blendRecipe:
            return True
        youngest_age = min(c.age for c in self.blendRecipe.components)
        return self.specifications.ageStatement <= youngest_age

    def is_single_malt(self) -> bool:
        if self.productCategory != ProductCategory.SINGLE_MALT:
            return False
        if not self.blendRecipe:
            return False
        distilleries = set(c.distillery for c in self.blendRecipe.components)
        return len(distilleries) == 1
```

---

#### 集約2: Cask（樽）

**集約ルート**: Cask

**エンティティ**:
```
Cask {
  caskId: CaskId (樽ID)
  caskNumber: String (樽番号)
  caskType: CaskType (bourbon | sherry | wine | virgin-oak | refill)
  capacity: Liters (容量)
  fillHistory: List<FillRecord> (充填履歴)
  currentFill: FillRecord? (現在の充填)
  location: WarehouseLocation (倉庫位置)
  condition: CaskCondition (active | empty | retired)
  acquiredAt: DateTime
  retiredAt: DateTime?
}

FillRecord {
  fillId: FillId
  spiritType: SpiritType (malt | grain | new-make)
  fillDate: Date
  volume: Liters
  alcoholContent: Percentage
  emptiedDate: Date?
  samplings: List<Sampling> (サンプリング記録)
  qualityRecords: List<QualityRecord> (品質記録)
}

Sampling {
  samplingId: SamplingId
  samplingDate: Date
  volume: Milliliters
  qualityData: QualityData
  notes: String
  sampledBy: StaffId
}

QualityData {
  alcoholContent: Percentage
  color: ColorGrade (1-10)
  nose: Score (1-10)
  palate: Score (1-10)
  finish: Score (1-10)
  overallScore: Score (1-10)
  maturationStage: MaturationStage (young | developing | mature | peak | declining)
}

WarehouseLocation {
  warehouseId: WarehouseId
  rack: String
  row: Integer
  position: Integer
  temperatureZone: TemperatureZone (cool | moderate | warm)
}
```

**値オブジェクト**:
- `CaskId`: 樽の一意識別子
- `QualityData`: 品質データ
- `WarehouseLocation`: 倉庫内位置

**不変条件（Invariants）**:
1. `fillHistory` の回数が3回を超えた樽は `condition = retired`
2. `currentFill` がある場合、`condition` は `active`
3. サンプリングは年2回以上実施
4. 熟成3年以上の原酒は `maturationStage` を記録

**ビジネスルールの実装**:
```python
class Cask:
    def can_refill(self) -> bool:
        if self.condition != CaskCondition.EMPTY:
            return False
        return len(self.fillHistory) < 3

    def get_current_age(self) -> Optional[Years]:
        if not self.currentFill:
            return None
        days = (datetime.now().date() - self.currentFill.fillDate).days
        return days / 365

    def needs_sampling(self) -> bool:
        if not self.currentFill or not self.currentFill.samplings:
            return True
        last_sampling = max(s.samplingDate for s in self.currentFill.samplings)
        days_since = (datetime.now().date() - last_sampling).days
        return days_since > 180  # 6ヶ月以上

    def should_retire(self) -> bool:
        return len(self.fillHistory) >= 3 and self.condition == CaskCondition.EMPTY
```

---

#### 集約3: MaturationPlan（熟成計画）

**集約ルート**: MaturationPlan

**エンティティ**:
```
MaturationPlan {
  planId: PlanId
  planName: String
  targetProduct: ProductReference? (目標製品への参照)
  casks: List<PlannedCask> (計画対象樽)
  targetMaturationYears: Years
  plannedStartDate: Date
  expectedCompletionDate: Date
  status: PlanStatus (planning | active | completed | cancelled)
  milestones: List<Milestone> (マイルストーン)
  createdBy: StaffId
  approvedBy: BlenderId?
}

PlannedCask {
  caskId: CaskId
  role: CaskRole (primary | secondary | experimental)
  targetYears: Years
  notes: String
}

Milestone {
  milestoneId: MilestoneId
  milestoneName: String (例: "3年熟成到達", "中間評価")
  targetDate: Date
  completedDate: Date?
  evaluationResult: EvaluationResult?
}

EvaluationResult {
  evaluationDate: Date
  evaluatedBy: BlenderId
  overallAssessment: Assessment (on-track | ahead | behind | problematic)
  recommendations: List<String>
  nextActions: List<String>
}
```

**値オブジェクト**:
- `PlanId`: 計画の一意識別子
- `EvaluationResult`: 評価結果

**不変条件（Invariants）**:
1. `status == active` には `approvedBy` が必須
2. `expectedCompletionDate` は `plannedStartDate + targetMaturationYears` 以降
3. マイルストーンは時系列順序を維持

---

#### 集約4: BlendingSession（ブレンディングセッション）

**集約ルート**: BlendingSession

**エンティティ**:
```
BlendingSession {
  sessionId: SessionId
  sessionDate: Date
  productTarget: ProductId (目標製品)
  participants: List<BlenderId> (参加ブレンダー)
  masterBlender: BlenderId (マスターブレンダー)
  candidates: List<BlendCandidate> (候補ブレンド)
  selectedCandidate: CandidateId? (選択された候補)
  sessionNotes: String
  decision: SessionDecision? (決定事項)
  status: SessionStatus (scheduled | in-progress | completed | postponed)
}

BlendCandidate {
  candidateId: CandidateId
  candidateName: String (候補名: A案、B案等)
  recipe: BlendRecipe
  sensoryEvaluation: SensoryEvaluation?
  costAnalysis: CostAnalysis
  pros: List<String>
  cons: List<String>
}

SensoryEvaluation {
  evaluationDate: Date
  panelSize: Integer
  averageScore: Float
  scoreBreakdown: ScoreBreakdown
  comments: List<String>
}

ScoreBreakdown {
  appearance: Float
  nose: Float
  palate: Float
  finish: Float
  balance: Float
  complexity: Float
}

CostAnalysis {
  rawMaterialCost: Money
  productionCost: Money
  totalCostPerBottle: Money
  marginAnalysis: MarginAnalysis
}

SessionDecision {
  decisionType: DecisionType (select | modify | reject-all | postpone)
  selectedCandidateId: CandidateId?
  modifications: List<String>?
  rationale: String
  decidedBy: BlenderId
  decidedAt: DateTime
}
```

**値オブジェクト**:
- `SessionId`: セッションの一意識別子
- `SensoryEvaluation`: 官能評価結果
- `CostAnalysis`: コスト分析

**不変条件（Invariants）**:
1. `selectedCandidate` は `candidates` 内の候補のみ選択可能
2. `decision.decisionType == select` には `selectedCandidateId` が必須
3. `status == completed` には `decision` が必須
4. `masterBlender` は `participants` に含まれる

---

### 6. ドメインイベント（Domain Events）

#### イベント1: WhiskyProductReleased（ウイスキー製品発売）

**イベント名**: `WhiskyProductReleased`

**ペイロード**:
```json
{
  "eventId": "evt-sp-2025-001",
  "productId": "WHISKY-2025-015",
  "productName": "山崎 25年",
  "productCategory": "single-malt",
  "specifications": {
    "alcoholContent": 43.0,
    "ageStatement": 25,
    "volumeOptions": ["700ml"]
  },
  "distillery": "山崎蒸溜所",
  "limitedQuantity": 5000,
  "releasedAt": "2025-06-01T00:00:00Z"
}
```

**発生タイミング**:
- `SpiritsProduct.developmentStatus` が `released` に変更された時

**購読者（Subscribers）**:
- **brand-marketing-bc (VS3)**: プレミアムプロモーション開始
- **sales-distribution-bc (VS4)**: 限定販売チャネルへの配荷
- **inventory-bc**: 高価値在庫として管理開始

---

#### イベント2: CaskMaturationCompleted（樽熟成完了）

**イベント名**: `CaskMaturationCompleted`

**ペイロード**:
```json
{
  "eventId": "evt-sp-2025-002",
  "caskId": "CASK-2015-001234",
  "caskNumber": "A-1234",
  "maturationYears": 10,
  "finalQuality": {
    "overallScore": 8.5,
    "maturationStage": "peak",
    "alcoholContent": 58.2
  },
  "recommendedUse": "premium-blending",
  "completedAt": "2025-03-01T00:00:00Z"
}
```

**発生タイミング**:
- 樽の熟成が計画年数に到達し、品質評価が完了した時

**購読者（Subscribers）**:
- **blending-planning**: ブレンド原酒候補として登録
- **inventory-bc**: 原酒在庫として計上
- **asset-management-bc**: 資産価値評価

---

#### イベント3: BlendRecipeApproved（ブレンドレシピ承認）

**イベント名**: `BlendRecipeApproved`

**ペイロード**:
```json
{
  "eventId": "evt-sp-2025-003",
  "recipeId": "RECIPE-2025-008",
  "productId": "WHISKY-2025-020",
  "productName": "響 新発売ブレンド",
  "componentCount": 15,
  "approvedBy": "マスターブレンダー 田中",
  "sensoryScore": 8.8,
  "approvedAt": "2025-02-15T14:00:00Z"
}
```

**発生タイミング**:
- マスターブレンダーがブレンドレシピを正式承認した時

**購読者（Subscribers）**:
- **production-bc**: 生産計画への組み込み
- **quality-management-bc**: 品質基準の登録
- **cost-management-bc**: 製造コスト計算

---

#### イベント4: SamplingDue（サンプリング期限到来）

**イベント名**: `SamplingDue`

**ペイロード**:
```json
{
  "eventId": "evt-sp-2025-004",
  "caskIds": ["CASK-2020-0001", "CASK-2020-0002", "CASK-2020-0003"],
  "samplingType": "scheduled",
  "dueDate": "2025-04-01",
  "maturationPlanId": "PLAN-2020-001",
  "priority": "normal"
}
```

**発生タイミング**:
- 定期サンプリングスケジュール（春・秋）の到来時
- 熟成マイルストーン到達時

**購読者（Subscribers）**:
- **quality-team**: サンプリング作業スケジュール
- **sensory-evaluation-bc**: 官能評価パネル手配

---

### 7. コンテキストマップ（Context Map）

#### 上流（Upstream）コンテキスト

**1. fermentation-research-bc（発酵研究BC）**

**関係パターン**: Customer-Supplier（顧客-供給者）

**依存内容**:
- 蒸留用酵母株
- 発酵技術（蒸留前発酵条件）
- 新規蒸留技術研究

**API依存**:
- `GET /yeast-strains?purpose=distillation` - 蒸留用酵母
- `POST /consultation-requests` - 技術相談

**イベント購読**:
- `YeastStrainDiscovered` → 蒸留適性評価

---

**2. sensory-evaluation-bc（官能評価BC）**

**関係パターン**: Customer-Supplier（顧客-供給者）

**依存内容**:
- 官能評価サービス（原酒、製品）
- マスターブレンダーパネル手配
- 消費者テスト実施

**API依存**:
- `POST /evaluation-requests` - 評価依頼
- `GET /evaluations/{requestId}/results` - 評価結果取得

---

#### 下流（Downstream）コンテキスト

**1. brand-marketing-bc（ブランドマーケティングBC, VS3）**

**関係パターン**: Published Language（公開言語）

**提供内容**:
- 製品情報（仕様、ストーリー、テイスティングノート）
- 限定品情報（数量、価格帯）
- プレミアムブランドストーリー

**API提供**:
- `GET /products?category=spirits` - スピリッツ製品一覧
- `GET /products/{productId}` - 製品詳細
- `GET /products/{productId}/story` - ブランドストーリー

---

**2. sales-distribution-bc（販売・流通BC, VS4）**

**関係パターン**: Published Language（公開言語）

**提供内容**:
- 製品仕様（配荷情報）
- 限定品の販売数量・チャネル
- 価格帯情報

---

#### 同格（Partnership）コンテキスト

**1. craft-innovation-development-bc（クラフト・革新開発BC）**

**関係パターン**: Partnership（パートナーシップ）

**共有内容**:
- RTD向けベーススピリッツの供給
- 蒸留技術の共有
- クラフトスピリッツの知見共有

---

### コンテキストマップ図

```
[fermentation-research-bc]
        │
        │ (Customer-Supplier)
        │ - 蒸留用酵母
        │ - 発酵技術
        ↓
┌──────────────────────────────────────────────────────────────┐
│               spirits-development-bc                          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │SpiritsProduct│  │    Cask     │  │Maturation   │          │
│  │             │  │             │  │Plan         │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌─────────────┐                                             │
│  │Blending     │                                             │
│  │Session      │                                             │
│  └─────────────┘                                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
        │                         │
        │ (Published Language)    │ (Partnership)
        ↓                         ↓
[brand-marketing-bc]    [craft-innovation-development-bc]
[sales-distribution-bc]

        ↓ (Customer-Supplier)
[sensory-evaluation-bc]
```

---

### 8. API概要（参考）

#### 提供API（Downstream BCsへ）

**1. 製品API**

```
GET /api/spirits-products
  Query: category, status, ageStatement
  Response: List<SpiritsProductSummary>

GET /api/spirits-products/{productId}
  Response: SpiritsProductDetail

GET /api/spirits-products/{productId}/tasting-notes
  Response: TastingNotes
```

**2. 原酒API（内部向け）**

```
GET /api/casks
  Query: status, maturationYears, caskType
  Response: List<CaskSummary>

GET /api/casks/{caskId}/quality-history
  Response: List<QualityRecord>

GET /api/available-stock
  Query: minAge, maxAge, caskType
  Response: AvailableStockSummary
```

---

#### 依存API（Upstream BCsから）

**1. fermentation-research-bc への依存**

```
GET /api/yeast-strains?purpose=distillation
  Purpose: 蒸留用酵母株の取得

POST /api/consultation-requests
  Purpose: 蒸留技術相談
```

**2. sensory-evaluation-bc への依存**

```
POST /api/evaluation-requests
  Purpose: 官能評価依頼
  Request: EvaluationRequest

GET /api/evaluations/{requestId}/results
  Purpose: 評価結果取得
```

---

## 実装優先順位

### Phase 1: Core Aggregates（最優先）
1. **SpiritsProduct集約** - 製品管理の基盤
2. **Cask集約** - 熟成管理の核心
3. **基本イベント** - WhiskyProductReleased, CaskMaturationCompleted

### Phase 2: Blending（次優先）
4. **BlendingSession集約** - ブレンド設計
5. **MaturationPlan集約** - 熟成計画
6. **BlendRecipeApproved イベント**

### Phase 3: Integration（統合）
7. **Context Map実装** - fermentation-research-bc との連携
8. **API公開** - マーケティング・販売BCへのサービス提供

---

## まとめ

このBounded Context定義は：

**ビジネス面**:
- スピリッツ開発の4つの主要オペレーションを詳細化
- 長期熟成という特殊な時間軸を持つ製品開発プロセスを構造化
- マスターブレンダーを中心とした品質管理体制を明確化
- ブレンドレシピの機密管理ルールを定義

**技術面**:
- 4つの集約でスピリッツ開発ドメインをモデル化
- 熟成管理（Cask）という長期資産管理の仕組み
- ブレンディングセッションによる意思決定プロセス
- ドメインイベントで他BCとの疎結合な連携

**DDD原則**:
- ユビキタス言語による業務-技術の一致（マスターブレンダー、原酒、天使の分け前等）
- 集約境界による一貫性保証
- イベント駆動による自律性
- 明示的なコンテキスト境界

この定義により、長期的な視点での製品開発と、高付加価値市場でのブランド価値向上を支えるシステムを構築できます。
