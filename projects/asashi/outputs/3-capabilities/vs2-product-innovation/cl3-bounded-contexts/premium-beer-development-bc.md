# Bounded Context: premium-beer-development-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** premium-beer-development（プレミアムビール開発）
**作成日:** 2025-11-26
**ステータス:** CL3完了

---

## 【ビジネス面】

### 1. コンテキスト概要

**BC名**: premium-beer-development-bc（プレミアムビール開発バウンデッドコンテキスト）

**目的**:
Asahi Super Dryを中心とするプレミアムビール製品の開発・改良を行い、売上の主軸とブランド価値の源泉を維持・向上させる。

**責務**:
- 新製品コンセプトの策定と承認
- 製品レシピの開発・最適化・管理（最重要機密）
- 品質規格の設計と維持
- パイロット醸造による検証
- 既存製品の継続的改良
- 地域ブランド製品の開発

**チーム境界**:
- **担当組織**: 商品開発本部 ビール開発部
- **チーム構成**:
  - 製品企画チーム（マーケティング連携）
  - レシピ開発チーム（醸造技術者、フレーバーデザイナー）
  - 品質設計チーム（品質エンジニア）
  - パイロット醸造チーム（醸造マイスター）
- **推定人員**: 40-60名

---

### 2. ビジネスオペレーション詳細

#### OP1: 新製品コンセプト策定

**業務フロー:**
```
1. 市場分析・機会特定
   └─ VS1（市場機会発見）からのインサイト受領
   └─ 競合製品分析
   └─ 消費者トレンド分析

2. コンセプト立案
   └─ ターゲット顧客定義
   └─ 製品ポジショニング設定
   └─ フレーバープロファイル目標設定
   └─ 価格帯設定

3. 技術実現性評価
   └─ fermentation-research-bcへの技術確認
   └─ ingredient-research-bcへの素材確認
   └─ 製造可能性評価

4. ビジネスケース作成
   └─ 収益性試算
   └─ 投資回収期間算出
   └─ リスク評価

5. コンセプト承認
   └─ 開発委員会レビュー
   └─ 経営承認
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 新製品コンセプトは開発委員会の承認を必須とする |
| BR-OP1-02 | 技術実現性評価なしにコンセプト承認は不可 |
| BR-OP1-03 | ビジネスケースの投資回収期間は3年以内を原則とする |
| BR-OP1-04 | Asahi Super Dryブランドの拡張は経営会議承認を必須とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 市場インサイト（VS1） | 承認済みコンセプト文書 |
| 技術評価結果 | 製品仕様書（初版） |
| 競合分析データ | ビジネスケース |

**トリガー:**
- 年次製品計画サイクル
- 市場機会の発見
- 競合製品への対応
- 経営戦略の変更

---

#### OP2: レシピ開発・最適化

**業務フロー:**
```
1. ベースレシピ設計
   └─ 酵母株選定（fermentation-research-bcから）
   └─ 麦芽・ホップ選定（ingredient-research-bcから）
   └─ 発酵条件の初期設定

2. 試作・評価サイクル
   └─ ラボスケール試醸
   └─ 成分分析
   └─ 官能評価（sensory-evaluation連携）
   └─ 改良点特定

3. レシピ最適化
   └─ DOE（実験計画法）による最適化
   └─ 複数バリエーション作成
   └─ コスト最適化

4. レシピ確定
   └─ 最終官能評価
   └─ 品質規格との整合確認
   └─ 製造仕様書作成
   └─ レシピ承認（厳重管理）
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | レシピは最高機密（Top Secret）として管理する |
| BR-OP2-02 | レシピ変更は必ず変更履歴を記録する |
| BR-OP2-03 | 最終レシピ確定前に最低10回の試作評価を実施する |
| BR-OP2-04 | Asahi Super Dryのレシピ変更は取締役会承認を必須とする |
| BR-OP2-05 | レシピへのアクセスは認証・ログ記録を必須とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品コンセプト | 確定レシピ（最高機密） |
| 酵母株・発酵技術 | 製造仕様書 |
| 素材知見 | 品質規格案 |

**トリガー:**
- コンセプト承認
- 既存製品改良要求
- コスト削減要求
- 素材変更の必要性

---

#### OP3: 品質設計

**業務フロー:**
```
1. 品質目標設定
   └─ コンセプトからの品質要件抽出
   └─ 法規制要件確認
   └─ ブランド品質基準との整合

2. 品質規格策定
   └─ 成分規格（アルコール度数、エキス分等）
   └─ 官能規格（色、泡、香り、味）
   └─ 物性規格（炭酸ガス、濁度等）
   └─ 保存性規格（賞味期限設定根拠）

3. 検査方法設定
   └─ 分析試験項目・方法
   └─ 官能検査基準
   └─ サンプリング計画

4. 品質規格承認
   └─ 品質保証部門レビュー
   └─ 規格書発行
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 品質規格は品質保証部門の承認を必須とする |
| BR-OP3-02 | 法規制要件は100%遵守を保証する |
| BR-OP3-03 | 官能規格は訓練パネリストによる評価を基準とする |
| BR-OP3-04 | 品質規格変更はA7（品質保証）との協議を必須とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品コンセプト | 品質規格書 |
| 確定レシピ | 検査基準書 |
| 法規制要件 | サンプリング計画 |

**トリガー:**
- レシピ確定
- 法規制変更
- 品質クレーム発生
- 品質改善要求

---

#### OP4: パイロット醸造

**業務フロー:**
```
1. パイロット計画
   └─ 醸造スケール決定（通常1000L）
   └─ 醸造スケジュール作成
   └─ 原材料手配

2. パイロット醸造実施
   └─ 仕込み
   └─ 発酵管理
   └─ 熟成
   └─ 濾過・充填

3. 評価・検証
   └─ 成分分析
   └─ 官能評価
   └─ 品質規格との照合
   └─ 消費者テスト（必要に応じて）

4. スケールアップ判定
   └─ パイロット結果レビュー
   └─ 製造移管可否判定
   └─ スケールアップ条件設定
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | パイロット醸造は最低3バッチ実施する |
| BR-OP4-02 | バッチ間の品質ばらつきはCV10%以内とする |
| BR-OP4-03 | 官能評価は合格基準を満たすこと |
| BR-OP4-04 | スケールアップ判定は開発・製造・品質の3者合意を必須とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 確定レシピ | パイロット製品 |
| 品質規格 | 評価データ |
| 原材料 | スケールアップ仕様書 |

**トリガー:**
- レシピ確定
- 品質規格承認
- 原材料確保完了

---

#### OP5: 製品改良

**業務フロー:**
```
1. 改良ニーズ特定
   └─ 品質クレーム分析
   └─ 消費者フィードバック分析
   └─ コスト削減要求
   └─ 原材料変更対応

2. 改良方針策定
   └─ 改良目標設定
   └─ 制約条件確認（ブランドイメージ維持等）
   └─ 改良アプローチ選定

3. 改良レシピ開発
   └─ 試作・評価（OP2と同様）
   └─ 既存製品との比較評価
   └─ ブラインドテスト

4. 改良承認・展開
   └─ 改良承認（変更影響度により承認レベル決定）
   └─ 製造への展開計画
   └─ 切替タイミング調整
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | 改良後も既存品質規格を満たすこと |
| BR-OP5-02 | 官能評価で既存製品と同等以上であること |
| BR-OP5-03 | 主力製品の改良は消費者テストを必須とする |
| BR-OP5-04 | コスト削減目的の改良でも品質低下は不可 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 改良要求 | 改良レシピ |
| 既存レシピ | 改良評価報告書 |
| 消費者フィードバック | 切替計画 |

**トリガー:**
- 品質クレーム
- コスト削減要求
- 原材料廃番・変更
- 消費者嗜好変化

---

#### OP6: 地域ブランド開発

**業務フロー:**
```
1. 地域市場分析
   └─ 地域消費者嗜好分析
   └─ 現地競合分析
   └─ 法規制確認（各国食品法）

2. 地域適応コンセプト
   └─ グローバルブランド基準との整合
   └─ 地域特性への適応
   └─ 現地パートナーとの協議

3. 地域レシピ開発
   └─ 現地原材料の活用検討
   └─ 味覚プロファイルの地域適応
   └─ 現地醸造所との技術連携

4. 地域展開
   └─ 現地パイロット醸造
   └─ 現地消費者テスト
   └─ 現地規制承認取得
   └─ 製造展開
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP6-01 | グローバルブランドガイドラインを遵守する |
| BR-OP6-02 | 現地法規制を100%遵守する |
| BR-OP6-03 | 地域ブランドでもAsahi品質基準を維持する |
| BR-OP6-04 | 地域展開は地域本部の承認を必須とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 地域市場分析 | 地域適応レシピ |
| グローバルブランド基準 | 現地規格書 |
| 現地法規制情報 | 現地製造仕様書 |

**トリガー:**
- 地域展開戦略
- 現地パートナーからの要請
- 新市場参入計画

---

### 3. ユビキタス言語（Ubiquitous Language）

#### 製品開発用語

| 用語 | 定義 |
|------|------|
| **Recipe（レシピ）** | 製品の製造に必要な原材料配合と製造条件の完全な仕様。最高機密 |
| **Concept（コンセプト）** | 製品の目指す価値提案、ターゲット、ポジショニングを定義した文書 |
| **Pilot Brew（パイロット醸造）** | 製造スケールに近い条件（通常1000L）での試験醸造 |
| **Scale-Up（スケールアップ）** | パイロットから商業製造規模への移行 |
| **Reformulation（リフォーミュレーション）** | 既存製品のレシピ変更・改良 |

#### 品質用語

| 用語 | 定義 |
|------|------|
| **Quality Specification（品質規格）** | 製品が満たすべき品質基準の文書 |
| **Sensory Evaluation（官能評価）** | 訓練された評価者による五感での製品評価 |
| **IBU（International Bitterness Units）** | ビールの苦味の国際単位 |
| **OG（Original Gravity）** | 発酵前の麦汁比重。エキス分の指標 |
| **FG（Final Gravity）** | 発酵後のビール比重。残糖の指標 |
| **ABV（Alcohol By Volume）** | アルコール度数（体積%） |

#### プロセス用語

| 用語 | 定義 |
|------|------|
| **Mashing（マッシング）** | 麦芽を温水で糖化する工程 |
| **Lautering（ロータリング）** | 麦汁と麦芽粕を分離する工程 |
| **Boiling（ボイリング）** | 麦汁を煮沸しホップを添加する工程 |
| **Fermentation（発酵）** | 酵母が糖をアルコールと炭酸ガスに変換する工程 |
| **Maturation（熟成）** | 発酵後にビールを熟成させる工程 |
| **Filtration（濾過）** | ビールから酵母や濁りを除去する工程 |

#### ブランド用語

| 用語 | 定義 |
|------|------|
| **Master Brand（マスターブランド）** | Asahiの統一ブランドアイデンティティ |
| **Regional Brand（地域ブランド）** | 特定地域向けに適応されたブランド |
| **Premium Segment（プレミアムセグメント）** | 高品質・高価格帯のビール市場区分 |
| **Brand Equity（ブランドエクイティ）** | ブランドの資産価値 |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: ProductConcept（製品コンセプト）

**責務**: 製品コンセプトのライフサイクル管理

```
ProductConcept [Aggregate Root]
├── conceptId: ConceptId [Value Object]
├── name: ConceptName [Value Object]
│   ├── workingName: string（開発コード名）
│   └── marketingName: string（市場名、確定後）
├── targetProfile: TargetProfile [Value Object]
│   ├── targetCustomer: CustomerSegment
│   ├── positioning: string
│   └── priceRange: PriceRange
├── flavorGoal: FlavorGoal [Value Object]
│   ├── tasteProfile: TasteProfile
│   ├── aromaProfile: AromaProfile
│   └── bodyProfile: BodyProfile
├── businessCase: BusinessCase [Entity]
│   ├── expectedRevenue: Money
│   ├── investmentRequired: Money
│   ├── paybackPeriod: Duration
│   └── riskAssessment: RiskLevel
├── technicalFeasibility: TechnicalFeasibility [Entity]
│   ├── fermentationFeasible: boolean
│   ├── ingredientAvailable: boolean
│   └── manufacturingFeasible: boolean
├── approvalStatus: ApprovalStatus [Value Object]
│   ├── status: enum (DRAFT, UNDER_REVIEW, APPROVED, REJECTED)
│   ├── approvedBy: UserId?
│   └── approvedAt: Date?
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-PC-01 | APPROVED状態への遷移には全技術実現性がtrueであること |
| INV-PC-02 | paybackPeriodは36ヶ月以内であること（例外承認可） |
| INV-PC-03 | REJECTED状態からの復帰は不可（新規コンセプトとして作成） |

---

#### 集約2: Recipe（レシピ）

**責務**: 製品レシピの管理（最高機密）

```
Recipe [Aggregate Root]
├── recipeId: RecipeId [Value Object]
├── productConceptId: ConceptId [Value Object]
├── version: RecipeVersion [Value Object]
├── ingredients: RecipeIngredient[] [Entity]
│   ├── ingredientId: IngredientId
│   ├── amount: Amount
│   ├── timing: ProcessTiming（投入タイミング）
│   └── purpose: string
├── fermentationSpec: FermentationSpec [Value Object]
│   ├── yeastStrainId: StrainId
│   ├── pitchingRate: number
│   ├── fermentationTemp: TemperatureProfile
│   └── fermentationDuration: Duration
├── processSpec: ProcessSpec [Value Object]
│   ├── mashingProfile: MashingProfile
│   ├── boilingDuration: Duration
│   ├── hoppingSchedule: HoppingSchedule
│   └── maturationSpec: MaturationSpec
├── status: RecipeStatus [Value Object]
│   └── value: enum (DRAFT, TESTING, VALIDATED, PRODUCTION, DEPRECATED)
├── confidentiality: ConfidentialityLevel [Value Object]
│   └── value: TOP_SECRET（固定）
├── changeHistory: RecipeChange[] [Entity]
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-RC-01 | confidentialityは常にTOP_SECRET |
| INV-RC-02 | PRODUCTION状態のレシピは直接編集不可（新バージョン作成） |
| INV-RC-03 | 全変更はchangeHistoryに記録必須 |
| INV-RC-04 | VALIDATED状態への遷移には10回以上の試作評価が必要 |
| INV-RC-05 | アクセスは全てログ記録 |

---

#### 集約3: QualitySpecification（品質規格）

**責務**: 製品品質規格の管理

```
QualitySpecification [Aggregate Root]
├── specId: QualitySpecId [Value Object]
├── recipeId: RecipeId [Value Object]
├── chemicalSpec: ChemicalSpec [Value Object]
│   ├── abv: Range（アルコール度数範囲）
│   ├── originalGravity: Range
│   ├── finalGravity: Range
│   ├── ibu: Range
│   ├── color: Range（EBC）
│   └── pH: Range
├── sensorySpec: SensorySpec [Value Object]
│   ├── appearance: SensoryStandard
│   ├── aroma: SensoryStandard
│   ├── taste: SensoryStandard
│   ├── mouthfeel: SensoryStandard
│   └── overall: SensoryStandard
├── physicalSpec: PhysicalSpec [Value Object]
│   ├── carbonation: Range（炭酸ガス量）
│   ├── turbidity: Range（濁度）
│   └── foamStability: Range（泡持ち）
├── shelfLife: ShelfLife [Value Object]
│   ├── duration: Duration
│   └── storageCondition: StorageCondition
├── regulatoryCompliance: RegulatoryCompliance [Entity]
│   ├── applicableRegulations: Regulation[]
│   └── complianceStatus: boolean
├── approvalStatus: ApprovalStatus [Value Object]
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-QS-01 | regulatoryCompliance.complianceStatusがtrueでないと承認不可 |
| INV-QS-02 | 全Range値は下限≤上限であること |
| INV-QS-03 | APPROVED状態の規格変更は新バージョン作成 |

---

#### 集約4: PilotBrew（パイロット醸造）

**責務**: パイロット醸造の計画・実施・評価管理

```
PilotBrew [Aggregate Root]
├── pilotBrewId: PilotBrewId [Value Object]
├── recipeId: RecipeId [Value Object]
├── batchNumber: BatchNumber [Value Object]
├── scale: BrewScale [Value Object]
│   └── volume: number（通常1000L）
├── plan: PilotPlan [Entity]
│   ├── scheduledDate: Date
│   ├── ingredients: IngredientAllocation[]
│   └── equipment: EquipmentReservation
├── execution: PilotExecution [Entity]
│   ├── actualStartDate: Date
│   ├── actualEndDate: Date
│   ├── processLog: ProcessLog[]
│   └── deviations: Deviation[]
├── evaluation: PilotEvaluation [Entity]
│   ├── chemicalAnalysis: ChemicalAnalysisResult
│   ├── sensoryEvaluation: SensoryEvaluationResult
│   ├── qualitySpecCompliance: boolean
│   └── overallJudgment: Judgment
├── status: PilotStatus [Value Object]
│   └── value: enum (PLANNED, IN_PROGRESS, COMPLETED, PASSED, FAILED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-PB-01 | PASSED判定にはqualitySpecComplianceがtrueであること |
| INV-PB-02 | COMPLETED状態にはevaluationが必須 |
| INV-PB-03 | 同一レシピで最低3バッチのPASSEDが必要（VALIDATED遷移条件） |

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **ConceptApproved** | {conceptId, name, targetProfile, approvedBy, approvedAt} | コンセプト承認時 | レシピ開発チーム |
| **RecipeValidated** | {recipeId, version, validationCount, validatedAt} | レシピがVALIDATED状態に遷移時 | 品質設計チーム、製造部門 |
| **PilotBrewCompleted** | {pilotBrewId, recipeId, batchNumber, judgment, completedAt} | パイロット醸造評価完了時 | レシピ開発チーム |
| **QualitySpecApproved** | {specId, recipeId, approvedBy, approvedAt} | 品質規格承認時 | 製造部門、品質保証部門 |
| **RecipePromotedToProduction** | {recipeId, version, promotedAt} | レシピがPRODUCTION状態に遷移時 | 製造部門、VS3（ブランディング） |
| **RegionalBrandLaunched** | {recipeId, region, launchedAt} | 地域ブランド製品発売時 | 地域本部、VS3 |

---

### 6. コンテキストマップ（Context Map）

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    │   fermentation-research-bc           │
                    │        (Upstream)                    │
                    │                                      │
                    └──────────────┬───────────────────────┘
                                   │ 酵母株・発酵技術提供
                                   ▼
┌─────────────────┐    ┌──────────────────────────────────┐    ┌─────────────────┐
│ ingredient-     │    │                                  │    │ VS3:            │
│ research-bc     │───►│  premium-beer-development-bc     │───►│ branding-bc     │
│ (Upstream)      │    │                                  │    │ (Downstream)    │
│                 │    │                                  │    │                 │
│ 素材知見提供    │    └──────────────┬───────────────────┘    │ 製品情報受領    │
└─────────────────┘                   │                        └─────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ sensory-        │    │ prototype-      │    │ production-     │
│ evaluation-bc   │    │ production-bc   │    │ technology-bc   │
│ (Partnership)   │    │ (Partnership)   │    │ (Downstream)    │
│                 │    │                 │    │                 │
│ 官能評価連携    │    │ 試作生産連携    │    │ 製造仕様受領    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| fermentation-research-bc | **Customer-Supplier** | 酵母株・発酵技術の供給を受ける |
| ingredient-research-bc | **Customer-Supplier** | 素材知見・配合技術の供給を受ける |
| sensory-evaluation-bc | **Partnership** | 官能評価の実施で対等に協力 |
| prototype-production-bc | **Partnership** | パイロット醸造の実施で対等に協力 |
| production-technology-bc | **Customer-Supplier** | 製造仕様を提供する |
| branding-bc (VS3) | **Customer-Supplier** | 製品情報・ストーリーを提供する |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/concepts` | POST | 新規コンセプト作成 |
| `/concepts/{id}/approve` | POST | コンセプト承認 |
| `/recipes` | POST | 新規レシピ作成 |
| `/recipes/{id}/validate` | POST | レシピ検証完了 |
| `/recipes/{id}/promote` | POST | PRODUCTION昇格 |
| `/quality-specs` | POST | 品質規格作成 |
| `/quality-specs/{id}/approve` | POST | 品質規格承認 |
| `/pilot-brews` | POST | パイロット醸造計画作成 |
| `/pilot-brews/{id}/complete` | POST | パイロット醸造完了・評価登録 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/concepts` | GET | コンセプト一覧 |
| `/concepts/{id}` | GET | コンセプト詳細 |
| `/recipes/{id}` | GET | レシピ詳細（高機密、厳格認証） |
| `/quality-specs/{id}` | GET | 品質規格詳細 |
| `/pilot-brews` | GET | パイロット醸造一覧 |
| `/products/{id}/info` | GET | 製品情報（VS3向け公開情報） |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| fermentation-research-bc | 酵母株情報、発酵レシピ参照 |
| ingredient-research-bc | 素材情報、配合レシピ参照 |
| sensory-evaluation-bc | 官能評価依頼・結果取得 |
| prototype-production-bc | パイロット醸造依頼・結果取得 |

---

**作成完了:** 2025-11-26
**ステータス:** CL3完了（premium-beer-development-bc定義）
