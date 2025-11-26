# Bounded Context: ingredient-research-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** ingredient-research（素材研究）
**作成日:** 2025-11-26
**ステータス:** CL3完了

---

## 【ビジネス面】

### 1. コンテキスト概要

**BC名**: ingredient-research-bc（素材研究バウンデッドコンテキスト）

**目的**:
製品の味・品質・機能性を決定する原材料・素材の研究開発を通じて、製品差別化の源泉となる素材知見を創出・蓄積する。

**責務**:
- 原材料の探索・評価・選定
- 素材特性の科学的分析と知見化
- 最適配合の研究・開発
- サプライヤーの評価・管理
- 素材知見データベースの構築・維持

**チーム境界**:
- **担当組織**: 基盤技術研究部門 素材研究チーム
- **チーム構成**:
  - 醸造原料研究者
  - 飲料素材研究者
  - 分析技術者
  - 調達スペシャリスト
- **推定人員**: 10-15名

---

### 2. ビジネスオペレーション詳細

#### OP1: 原材料探索・評価

**業務フロー:**
```
1. 探索計画立案
   └─ 製品開発ニーズ分析
   └─ 市場トレンド調査（機能性素材、サステナブル原料等）
   └─ 探索対象の優先順位付け

2. 候補素材収集
   └─ サプライヤー情報収集（国内外の産地・品種）
   └─ サンプル取得
   └─ 基礎情報記録（産地、品種、栽培条件、収穫年）

3. 初期スクリーニング
   └─ 官能評価（香り、味、外観）
   └─ 基本分析（成分、品質指標）
   └─ コスト試算

4. 詳細評価
   └─ 試験醸造実施（fermentation-research-bc連携）
   └─ 特性分析
   └─ 安定供給可能性評価

5. 評価結果記録
   └─ 素材評価シート作成
   └─ 素材DBへの登録
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 品質・コスト・安定供給性・サステナビリティの4軸評価を実施 |
| BR-OP1-02 | サンプルはロット管理、保管条件記録、トレーサビリティ確保 |
| BR-OP1-03 | 評価記録は最低5年間保管（特許・品質トレース対応） |
| BR-OP1-04 | 配合候補素材情報は「社外秘」として管理 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品開発ニーズ | 推奨素材リスト |
| 市場トレンド情報 | 素材評価レポート |
| サプライヤー提案 | 素材DBエントリ |

**トリガー:**
- 新製品開発プロジェクト開始
- 既存製品のリニューアル計画
- サプライヤーからの新素材提案
- 定期的な素材探索活動（年2回）

---

#### OP2: 素材特性分析

**業務フロー:**
```
1. 分析計画策定
   └─ 分析目的明確化
   └─ 分析項目選定
   └─ 分析スケジュール作成

2. サンプル準備
   └─ サンプル受領・ロット記録
   └─ 前処理（粉砕、抽出、希釈等）
   └─ 分析用サンプル調製

3. 機器分析実施
   └─ 成分分析（糖、タンパク質、α酸、β酸等）
   └─ 物性測定（粒度分布、溶解性、色度等）
   └─ 微量成分分析（香気成分、ビタミン等）

4. 官能評価実施
   └─ パネル選定（訓練された評価者5名以上）
   └─ 評価項目設定
   └─ ブラインドテスト実施
   └─ 統計解析

5. データ解析・知見化
   └─ 統計処理
   └─ 特性マップ作成
   └─ 知見レポート作成
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | ISO/IEC 17025準拠の分析精度管理 |
| BR-OP2-02 | 官能評価は訓練パネリスト5名以上、統計的有意性（p<0.05）確認 |
| BR-OP2-03 | 測定値のCV（変動係数）10%以内を原則 |
| BR-OP2-04 | サンプルID、分析日時、担当者、機器校正記録の紐付け必須 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 分析依頼 | 分析データ |
| 素材サンプル | 特性レポート |
| | 知見サマリー |

**トリガー:**
- 新規素材の評価依頼
- 製品トラブル時の原因究明
- 定期的な素材ロット分析
- 研究プロジェクトの進捗

---

#### OP3: 配合研究

**業務フロー:**
```
1. 配合目標設定
   └─ 製品コンセプト理解
   └─ ターゲットフレーバープロファイル定義
   └─ 制約条件確認（コスト、調達可能性、法規制）

2. 初期配合設計
   └─ 素材DB検索
   └─ 配合比率の理論計算
   └─ 初期配合案作成（3-5パターン）

3. 試験醸造・評価
   └─ ラボスケール試験醸造（fermentation-research-bc連携）
   └─ 製品分析
   └─ 官能評価

4. 配合最適化
   └─ DOE（実験計画法）による最適化
   └─ 統計モデル構築
   └─ ロバスト性検証

5. 配合レシピ確定
   └─ 最終配合仕様書作成
   └─ コスト試算
   └─ 調達可能性確認
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 配合レシピは「極秘（Top Secret）」、アクセスログ記録必須 |
| BR-OP3-02 | マイナー変更（±5%）は研究リーダー承認、メジャー変更は部門長承認 |
| BR-OP3-03 | 新規配合は特許性評価必須 |
| BR-OP3-04 | 配合変更履歴の完全記録、理由・承認者記録 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品コンセプト | 配合レシピ |
| 素材特性データ | 配合知見レポート |
| 発酵特性データ | スケールアップ要件 |

**トリガー:**
- 新製品開発プロジェクトのキックオフ
- 既存製品の改良要求
- コストダウン要求
- 素材切り替えの必要性

---

#### OP4: サプライヤー評価

**業務フロー:**
```
1. 評価基準設定
   └─ 品質、コスト、供給安定性、サステナビリティ、技術力の5軸
   └─ 重み付け設定
   └─ 評価スケール定義（5段階）

2. サプライヤー情報収集
   └─ 基本情報
   └─ サンプル提供依頼
   └─ 工場監査（必要に応じて）

3. 品質評価
   └─ サンプル分析
   └─ ロット間変動評価
   └─ 品質管理体制確認

4. 供給能力評価
   └─ 年間供給可能量確認
   └─ リードタイム確認
   └─ BCP確認

5. 総合評価
   └─ スコアリング
   └─ ランク付け（A/B/C）
   └─ リスク評価
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 新規は初回評価後6ヶ月で再評価、既存は年1回定期評価 |
| BR-OP4-02 | A（推奨）80点以上、B（条件付き可）60-79点、C（非推奨）60点未満 |
| BR-OP4-03 | 単一サプライヤー依存度50%超の場合、代替先確保必須 |
| BR-OP4-04 | サステナビリティ項目を20%加点評価 |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| サプライヤー情報 | サプライヤー評価レポート |
| サンプル分析データ | 推奨サプライヤーリスト |
| | リスク評価レポート |

**トリガー:**
- 新規サプライヤー候補の出現
- 既存サプライヤーの定期評価時期
- 品質トラブル発生時
- サプライチェーンリスク顕在化時

---

#### OP5: 素材データベース管理

**業務フロー:**
```
1. データ登録
   └─ 素材マスター登録
   └─ 分析データ登録
   └─ 配合レシピ登録
   └─ メタデータ付与

2. データ品質管理
   └─ 妥当性チェック
   └─ 重複チェック
   └─ 整合性検証

3. データ更新・維持
   └─ 定期レビュー（年1回）
   └─ 古いデータのアーカイブ
   └─ 法規制変更対応

4. データ検索・提供
   └─ 検索インターフェース提供
   └─ API提供（他BCへ）
   └─ レポート生成

5. アクセス管理
   └─ 権限設定
   └─ アクセスログ記録
   └─ 定期権限レビュー
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | 素材マスター（永久）、分析データ（10年）、配合レシピ（永久） |
| BR-OP5-02 | 配合レシピ詳細は「極秘」、アクセス認証必須 |
| BR-OP5-03 | 変更履歴の完全記録 |
| BR-OP5-04 | APIアクセスは認証必須、レート制限あり |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 素材情報 | 素材検索結果 |
| 分析データ | 分析レポート |
| 配合レシピ | API応答 |

**トリガー:**
- 新規素材情報取得
- 分析完了
- 配合レシピ確定
- データ検索リクエスト

---

### 3. ユビキタス言語（Ubiquitous Language）

#### 素材関連

| 用語 | 定義 |
|------|------|
| **Ingredient（素材）** | 製品の原材料となる物質の総称 |
| **Malt（麦芽）** | 大麦を発芽・乾燥させた醸造用原料 |
| **Hop（ホップ）** | ビールの苦味・香りを付与するハーブ |
| **Alpha Acid（α酸）** | ホップの苦味成分 |
| **Adjunct（副原料）** | 麦芽以外の発酵性糖源 |
| **Functional Ingredient（機能性素材）** | 健康機能性を付与する素材 |

#### 評価・分析関連

| 用語 | 定義 |
|------|------|
| **Sensory Evaluation（官能評価）** | 人間の五感による製品評価 |
| **Trained Panelist（訓練パネリスト）** | 官能評価の専門訓練を受けた評価者 |
| **Flavor Profile（フレーバープロファイル）** | 製品の風味特性を多次元的に表現したもの |
| **Characteristic Map（特性マップ）** | 素材の特性を多次元的に可視化したマップ |
| **Lot（ロット）** | 同一条件で製造された素材の単位 |
| **Traceability（トレーサビリティ）** | 素材の履歴を追跡可能な状態 |

#### 配合関連

| 用語 | 定義 |
|------|------|
| **Formulation（配合）** | 製品を構成する素材とその比率の組み合わせ |
| **Formulation Recipe（配合レシピ）** | 配合の詳細仕様書。最高機密 |
| **Target Profile（ターゲットプロファイル）** | 配合研究で目指す製品の風味特性 |
| **DOE（Design of Experiments）** | 実験計画法 |
| **Robustness（ロバスト性）** | 素材ロット変動への配合の安定性 |

#### サプライヤー関連

| 用語 | 定義 |
|------|------|
| **Supplier（サプライヤー）** | 素材の供給業者 |
| **Supplier Rank（サプライヤーランク）** | A/B/Cの格付け |
| **Single Dependency Ratio（単一依存度）** | 特定サプライヤーへの依存度 |
| **BCP（Business Continuity Plan）** | 事業継続計画 |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: Ingredient（素材）

**責務**: 素材情報のライフサイクル管理

```
Ingredient [Aggregate Root]
├── ingredientId: IngredientId [Value Object]
├── name: IngredientName [Value Object]
│   ├── japaneseName: string
│   ├── englishName: string
│   └── scientificName: string?
├── category: IngredientCategory [Value Object]
│   └── value: enum (MALT, HOP, ADJUNCT, FUNCTIONAL, WATER)
├── basicCharacteristics: BasicCharacteristics [Value Object]
│   ├── origin: string
│   ├── harvestYear: int
│   ├── grade: string
│   └── certification: CertificationType?
├── currentSupplierId: SupplierId [Value Object]
├── status: IngredientStatus [Value Object]
│   └── value: enum (ACTIVE, UNDER_EVALUATION, ARCHIVED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-IN-01 | 名前（和名、英名）は必須 |
| INV-IN-02 | ACTIVEステータスの素材のみ配合レシピで使用可能 |
| INV-IN-03 | ARCHIVEDへの遷移は一方向（復元不可） |

---

#### 集約2: IngredientAnalysis（素材分析）

**責務**: 分析データの管理

```
IngredientAnalysis [Aggregate Root]
├── analysisId: AnalysisId [Value Object]
├── ingredientId: IngredientId [Value Object]
├── sampleId: SampleId [Value Object]
├── analysisDate: Date
├── analysisType: AnalysisType [Value Object]
│   └── value: enum (CHEMICAL, SENSORY, PHYSICAL)
├── results: AnalysisResult[] [Value Object]
│   ├── parameterName: string
│   ├── value: decimal
│   ├── unit: string
│   └── cv: decimal
├── sensoryProfile: SensoryProfile? [Value Object]
│   ├── aromaScore: ScoreValue
│   ├── tasteScore: ScoreValue
│   ├── overallScore: ScoreValue
│   └── panelistCount: int
├── qualityControlStatus: QCStatus [Value Object]
│   └── value: enum (PASSED, FAILED, UNDER_REVIEW)
├── analystId: UserId [Value Object]
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-IA-01 | CVは10%以内 |
| INV-IA-02 | 官能評価のpanelistCountは5名以上 |
| INV-IA-03 | PASSEDのみ素材DBに正式登録 |
| INV-IA-04 | 分析データの事後修正は禁止 |

---

#### 集約3: Formulation（配合）

**責務**: 配合レシピの管理（最高機密）

```
Formulation [Aggregate Root]
├── formulationId: FormulationId [Value Object]
├── name: FormulationName [Value Object]
│   ├── displayName: string
│   ├── codeName: string
│   └── version: string
├── productType: ProductType [Value Object]
│   └── value: enum (PREMIUM_BEER, LOW_ALCOHOL, BEVERAGE)
├── targetProfile: FlavorProfile [Value Object]
│   ├── sweetness: int (1-10)
│   ├── bitterness: int (1-10)
│   ├── acidity: int (1-10)
│   └── aroma: string[]
├── ingredients: FormulationIngredient[] [Entity]
│   ├── ingredientId: IngredientId
│   ├── ratio: decimal (%)
│   ├── amount: decimal
│   └── roleInFormulation: string
├── totalCost: Money [Value Object]
├── developmentHistory: DevelopmentHistory [Value Object]
├── status: FormulationStatus [Value Object]
│   └── value: enum (DRAFT, UNDER_TESTING, APPROVED, IN_PRODUCTION)
├── confidentiality: ConfidentialityLevel [Value Object]
│   └── value: TOP_SECRET（固定）
├── approvedBy: UserId? [Value Object]
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-FM-01 | 配合素材の合計比率は100%（±0.1%許容） |
| INV-FM-02 | 各ingredientIdはACTIVEステータスの素材のみ |
| INV-FM-03 | DRAFT状態のみ編集可能 |
| INV-FM-04 | メジャー変更（±5%超）は部門長承認必須 |
| INV-FM-05 | confidentialityは常にTOP_SECRET |

---

#### 集約4: Supplier（サプライヤー）

**責務**: サプライヤー情報の管理

```
Supplier [Aggregate Root]
├── supplierId: SupplierId [Value Object]
├── companyName: CompanyName [Value Object]
│   ├── legalName: string
│   ├── tradeName: string
│   └── country: string
├── contactInfo: ContactInfo [Value Object]
│   ├── address: Address
│   ├── phoneNumber: string
│   ├── email: string
│   └── contactPerson: string
├── supplyCapability: SupplyCapability [Value Object]
│   ├── annualCapacity: decimal
│   ├── leadTimeDays: int
│   ├── minimumOrderQuantity: decimal
│   └── bcp: BCPInfo
├── evaluation: SupplierEvaluation [Value Object]
│   ├── evaluationDate: Date
│   ├── qualityScore: int (0-100)
│   ├── costScore: int
│   ├── stabilityScore: int
│   ├── sustainabilityScore: int
│   ├── techCapabilityScore: int
│   ├── totalScore: int
│   ├── rank: SupplierRank (A/B/C)
│   └── nextEvaluationDate: Date
├── status: SupplierStatus [Value Object]
│   └── value: enum (ACTIVE, ON_HOLD, TERMINATED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-SP-01 | 各評価スコアは0-100の範囲 |
| INV-SP-02 | Rank: A（80点以上）、B（60-79点）、C（60点未満） |
| INV-SP-03 | ACTIVEのみ新規発注可能 |
| INV-SP-04 | 評価は年1回以上実施 |

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **NewIngredientRegistered** | {ingredientId, name, category, registeredBy, timestamp} | 新規素材登録時 | premium-beer-dev, beverage-dev |
| **IngredientArchived** | {ingredientId, name, reason, archivedBy, timestamp} | 素材アーカイブ時 | formulation-bc |
| **IngredientAnalysisCompleted** | {analysisId, ingredientId, type, qcStatus, findings, timestamp} | 分析QC完了時 | fermentation-research, premium-beer-dev |
| **FormulationApproved** | {formulationId, name, productType, approvedBy, timestamp} | 配合レシピ承認時 | premium-beer-dev, production-tech |
| **SupplierEvaluationCompleted** | {supplierId, companyName, evaluation, timestamp} | サプライヤー評価完了時 | 調達部門 |
| **SupplierRankDowngraded** | {supplierId, companyName, oldRank, newRank, totalScore, timestamp} | サプライヤーランクダウン時 | 調達部門、リスク管理 |

---

### 6. コンテキストマップ（Context Map）

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    │     ingredient-research-bc           │
                    │           (Upstream)                 │
                    │                                      │
                    └──────────────┬───────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ premium-beer-   │    │ beverage-       │    │ production-     │
│ development-bc  │    │ development-bc  │    │ technology-bc   │
│ (Downstream)    │    │ (Downstream)    │    │ (Downstream)    │
│                 │    │                 │    │                 │
│ [Customer-      │    │ [Customer-      │    │ [Customer-      │
│  Supplier]      │    │  Supplier]      │    │  Supplier]      │
└─────────────────┘    └─────────────────┘    └─────────────────┘

         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│ fermentation-   │    │ functional-     │
│ research-bc     │    │ ingredients-bc  │
│                 │    │                 │
│ [Partnership]   │    │ [Partnership]   │
└─────────────────┘    └─────────────────┘

         │
         ▼
┌─────────────────┐
│ regulatory-     │
│ compliance-bc   │
│                 │
│ [Conformist]    │
└─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| premium-beer-development-bc | **Customer-Supplier** | 素材知見・配合レシピを提供 |
| beverage-development-bc | **Customer-Supplier** | 飲料用素材知見を提供 |
| production-technology-bc | **Customer-Supplier** | スケールアップ要件を提供 |
| fermentation-research-bc | **Partnership** | 素材と発酵の組み合わせ研究で協力 |
| functional-ingredients-bc | **Partnership** | 機能性素材の共同研究 |
| regulatory-compliance-bc | **Conformist** | 法規制に従う |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/ingredients` | POST | 新規素材登録 |
| `/ingredients/{id}/archive` | POST | 素材アーカイブ |
| `/analyses` | POST | 新規分析登録 |
| `/analyses/{id}/complete` | POST | 分析QC完了 |
| `/formulations` | POST | 新規配合作成 |
| `/formulations/{id}/approve` | POST | 配合承認 |
| `/suppliers` | POST | 新規サプライヤー登録 |
| `/suppliers/{id}/evaluate` | POST | サプライヤー評価登録 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/ingredients/search` | GET | 素材検索 |
| `/ingredients/{id}` | GET | 素材詳細 |
| `/ingredients/{id}/flavor-profile` | GET | フレーバープロファイル |
| `/formulations/{id}` | GET | 配合詳細（高機密） |
| `/suppliers/recommended` | GET | 推奨サプライヤー一覧 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| fermentation-research-bc | 発酵適性評価依頼 |
| regulatory-compliance-bc | 法規制適合性チェック |

---

**作成完了:** 2025-11-26
**ステータス:** CL3完了（ingredient-research-bc定義）
