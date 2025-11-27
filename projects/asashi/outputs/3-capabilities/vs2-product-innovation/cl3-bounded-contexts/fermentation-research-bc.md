# Bounded Context: fermentation-research-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** fermentation-research（発酵研究）
**作成日:** 2025-11-26
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | fermentation-research-bc |
| **日本語名** | 発酵研究 |
| **命名パターン** | `-research`（アクション型） |
| **命名理由** | 「発酵管理」ではなく「発酵研究」を採用。100年以上の醸造技術を継続的に**進化**させる探究姿勢を表現。研究（research）は基盤技術の継続的な深化・発展を意味し、静的な「管理」ではなく動的な「研究」活動を強調 |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**fermentation-research-bc**（発酵研究バウンデッドコンテキスト）

#### 目的
100年以上蓄積された醸造技術の中核として、酵母・発酵に関する基盤研究を行い、全製品開発の技術基盤を提供する。アサヒグループの競争優位性の源泉。

#### 責務
- 酵母株の探索・収集・保存・管理
- 酵母の育種・改良による新株開発
- 発酵条件の最適化研究
- 発酵実験の計画・実施・検証
- 技術知見の体系化と知的財産管理
- 製品開発BCsへの技術・酵母株の提供

#### チーム境界
- **担当組織**: R&D本部 発酵研究所
- **チーム構成**:
  - 酵母研究チーム（微生物学者、遺伝学者）
  - 発酵技術チーム（発酵エンジニア、醸造技師）
  - 技術管理チーム（特許専門家、ナレッジマネージャー）
- **推定人員**: 30-50名

---

### 2. ビジネスオペレーション詳細

#### OP1: 酵母株探索・収集

**業務フロー:**
```
1. 探索計画策定
   └─ 目的特性の定義（香り、発酵力、耐性等）
   └─ 探索フィールドの選定（自然環境、既存コレクション）

2. サンプリング実施
   └─ フィールドワーク（土壌、果実、花等から採取）
   └─ 外部機関からの入手（大学、研究機関、酵母バンク）

3. 分離・同定
   └─ 培養・分離作業
   └─ 形態学的・遺伝学的同定
   └─ 基本特性の評価

4. 登録・保存
   └─ 酵母株マスターへの登録
   └─ 初期保存（凍結保存、凍結乾燥）
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 新規酵母株は必ず遺伝学的同定を実施すること |
| BR-OP1-02 | 外部入手株は知的財産権・MTAを確認すること |
| BR-OP1-03 | 登録前に基本発酵試験を完了すること |
| BR-OP1-04 | 全株に一意の株ID（ASAHI-YYYY-NNNN形式）を付与すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 探索計画書 | 酵母サンプル |
| 外部情報（学術論文、特許） | 収集記録 |
| MTA（材料移転契約） | 酵母株マスターエントリ |

**トリガー:**
- 年次研究計画
- 製品開発からの特性要求
- 学術・業界情報

---

#### OP2: 酵母株育種・改良

**業務フロー:**
```
1. 育種目標設定
   └─ 目的特性の定義（香気成分、発酵速度、耐性等）
   └─ 親株の選定

2. 育種実施
   └─ 交配育種（有性生殖による交配）
   └─ 変異育種（UV照射、化学変異原）
   └─ 選抜育種（自然変異の選抜）
   └─ ※遺伝子組換えは規制対応が必要

3. スクリーニング
   └─ 高スループットスクリーニング
   └─ 目的特性の評価
   └─ 安定性確認

4. 最終評価・登録
   └─ 詳細特性評価
   └─ 実用性評価（スケールアップ適性）
   └─ 改良株として登録
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | 親株の系統記録を完全に保持すること |
| BR-OP2-02 | 育種方法は全て記録し、再現可能とすること |
| BR-OP2-03 | 改良株は最低3世代の安定性を確認すること |
| BR-OP2-04 | 遺伝子組換え株は規制対応プロセスを経ること |
| BR-OP2-05 | 有望株は特許出願を検討すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 親株 | 改良酵母株 |
| 育種計画 | 育種記録 |
| 目的特性要件 | 特性評価データ |

**トリガー:**
- 製品開発からの特性要求
- 技術課題（発酵効率、品質向上）
- 研究計画

---

#### OP3: 発酵条件最適化

**業務フロー:**
```
1. 最適化目標設定
   └─ 対象酵母株の選定
   └─ 最適化パラメータの定義
   └─ 評価指標の設定

2. 実験計画策定
   └─ 実験計画法（DoE）による設計
   └─ パラメータ範囲の設定
   └─ サンプルサイズ決定

3. 最適化実験実施
   └─ 系統的なパラメータ変更実験
   └─ データ収集・記録

4. データ分析・最適条件決定
   └─ 統計解析
   └─ 最適条件の同定
   └─ 再現性検証

5. レシピ化
   └─ 発酵レシピとして文書化
   └─ 標準作業手順書（SOP）作成
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 実験計画法（DoE）に基づく系統的アプローチを採用すること |
| BR-OP3-02 | 最適条件は最低3回の再現性検証を実施すること |
| BR-OP3-03 | パラメータ変更は一度に1変数を原則とすること（多変量の場合はDoE） |
| BR-OP3-04 | 統計的有意性（p<0.05）を確認すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 対象酵母株 | 最適条件データ |
| 品質要件 | 発酵レシピ |
| 効率目標 | SOP文書 |

**トリガー:**
- 新酵母株の実用化
- 品質改善要求
- コスト削減目標

---

#### OP4: 発酵実験・検証

**業務フロー:**
```
1. 実験計画
   └─ 仮説設定
   └─ 実験条件設計
   └─ 必要リソース確保

2. 実験準備
   └─ 酵母株の活性化（継代培養）
   └─ 培地・設備の準備
   └─ 計測機器のキャリブレーション

3. 実験実施
   └─ 発酵試験の実行
   └─ 経時的サンプリング
   └─ データ記録（自動/手動）

4. 分析・評価
   └─ 分析試験（成分分析、官能評価）
   └─ データ解析
   └─ 仮説検証

5. 報告・アーカイブ
   └─ 実験報告書作成
   └─ データのアーカイブ
   └─ 知見の共有
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 全実験はGLP（Good Laboratory Practice）に準拠すること |
| BR-OP4-02 | 実験ノートは改ざん不可能な形式で記録すること |
| BR-OP4-03 | 対照実験を必ず含めること |
| BR-OP4-04 | データは生データから加工データまで全て保存すること |
| BR-OP4-05 | 失敗実験も含め全て記録・報告すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 研究仮説 | 実験データ |
| 酵母株 | 検証報告書 |
| 実験計画書 | 分析結果 |

**トリガー:**
- 研究仮説の検証
- 製品開発要件
- 問題解決

---

#### OP5: 酵母株保存・管理

**業務フロー:**
```
1. 保存処理
   └─ 保存用培養の調製
   └─ 凍結保存（-80℃、液体窒素）
   └─ 凍結乾燥保存
   └─ 作業株の維持培養

2. 在庫管理
   └─ 保存状態の定期確認
   └─ 生存率チェック
   └─ 在庫数量管理

3. 品質管理
   └─ 定期的な特性確認
   └─ コンタミネーションチェック
   └─ 遺伝的安定性確認

4. 払出管理
   └─ 払出申請受付
   └─ 株の活性化・調製
   └─ 払出記録
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | マスターストック、ワーキングストックの2層管理を維持すること |
| BR-OP5-02 | 継代培養は最大10世代までとし、それ以降はマスターから再取得すること |
| BR-OP5-03 | 生存率は90%以上を維持すること |
| BR-OP5-04 | 年1回以上の特性再確認を実施すること |
| BR-OP5-05 | 払出記録は完全なトレーサビリティを確保すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 新規登録株 | 保存済み酵母株 |
| 払出申請 | 活性化済み酵母株 |
| 品質検査計画 | 品質記録 |

**トリガー:**
- 新株登録
- 払出申請
- 定期品質管理

---

#### OP6: 技術知見の体系化

**業務フロー:**
```
1. 知見収集
   └─ 実験結果からの知見抽出
   └─ 熟練者（杜氏）からの暗黙知収集
   └─ 外部情報の取り込み

2. 体系化・文書化
   └─ 技術文書の作成
   └─ ナレッジベースへの登録
   └─ 分類・タグ付け

3. 知的財産化
   └─ 特許性評価
   └─ 特許出願
   └─ ノウハウの秘匿管理

4. 共有・活用
   └─ 技術報告会
   └─ 教育・研修
   └─ 製品開発への技術移転
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP6-01 | 全技術文書はピアレビューを経ること |
| BR-OP6-02 | 特許出願前の外部発表は禁止 |
| BR-OP6-03 | 機密レベル（極秘/秘/社外秘/一般）を必ず設定すること |
| BR-OP6-04 | 暗黙知は可能な限り形式知化すること |
| BR-OP6-05 | 技術文書は5年ごとに見直しを実施すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 実験報告書 | 技術文書 |
| 熟練者インタビュー | 特許出願 |
| 外部情報 | ナレッジベースエントリ |

**トリガー:**
- 研究成果の創出
- 定期的なナレッジ棚卸し
- 特許調査

---

### 3. ユビキタス言語（Ubiquitous Language）

#### ドメインオブジェクト（業務で扱うモノ・コト）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| YeastStrain | 酵母株 | 遺伝的に同一な酵母細胞の集団。株IDで一意に識別される |
| ParentStrain | 親株 | 育種において遺伝的素材となる酵母株 |
| ImprovedStrain | 改良株 | 育種により目的特性を獲得した酵母株 |
| WildStrain | 野生株 | 自然環境から分離された未改良の酵母株 |
| MasterStock | マスターストック | 長期保存用の酵母株ストック。払出の原本 |
| WorkingStock | ワーキングストック | 日常使用のための酵母株ストック |
| FermentationRecipe | 発酵レシピ | 特定の酵母株と発酵条件の組み合わせ |
| FermentationCondition | 発酵条件 | 温度、pH、糖濃度、酸素量等のパラメータセット |

#### ビジネスルール（業務上の制約・ルール）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| GLP | 優良試験所基準 | 実験の信頼性を保証するための基準 |
| DoE | 実験計画法 | 効率的な実験設計のための統計的手法 |
| Traceability | トレーサビリティ | 酵母株の来歴を追跡できる状態 |
| GenerationLimit | 世代制限 | 継代培養の最大回数（10世代） |
| ViabilityThreshold | 生存率閾値 | 保存株の最低生存率（90%） |

#### プロセス（業務フロー）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| Screening | スクリーニング | 多数の候補から目的特性を持つ株を選抜するプロセス |
| Breeding | 育種 | 目的特性を持つ新株を作出するプロセス |
| Subculture | 継代培養 | 酵母を新しい培地に植え継ぐプロセス |
| Cryopreservation | 凍結保存 | 超低温で酵母を長期保存するプロセス |
| Lyophilization | 凍結乾燥 | 凍結後に乾燥させて保存するプロセス |
| ScaleUp | スケールアップ | ラボスケールから製造スケールへの移行 |
| TechnologyTransfer | 技術移転 | 研究成果を製品開発に引き渡すプロセス |

#### イベント（業務上の重要な出来事）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| StrainRegistered | 株登録完了 | 新規酵母株がマスターに登録された |
| StrainImproved | 株改良完了 | 目的特性を持つ改良株が作出された |
| RecipeOptimized | レシピ最適化完了 | 発酵条件の最適化が完了した |
| ExperimentCompleted | 実験完了 | 発酵実験が完了し検証された |
| KnowHowDocumented | 知見文書化完了 | 技術知見が文書化された |
| PatentFiled | 特許出願 | 技術の特許が出願された |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: YeastStrain（酵母株）

**責務**: 酵母株のライフサイクル管理

```
YeastStrain [Aggregate Root]
├── strainId: StrainId [Value Object]
│   └── format: "ASAHI-YYYY-NNNN"
├── taxonomy: Taxonomy [Value Object]
│   ├── genus: string (例: "Saccharomyces")
│   ├── species: string (例: "cerevisiae")
│   └── strain: string (例: "Asahi-1号")
├── origin: StrainOrigin [Value Object]
│   ├── source: enum (WILD, BRED, ACQUIRED)
│   ├── location: string
│   ├── collectionDate: Date
│   └── parentStrains: StrainId[] (育種の場合)
├── characteristics: StrainCharacteristics [Value Object]
│   ├── fermentationPower: number (発酵力)
│   ├── alcoholTolerance: number (アルコール耐性)
│   ├── temperatureRange: Range (温度範囲)
│   ├── flavorProfile: FlavorProfile[] (香味特性)
│   └── specialTraits: string[] (特殊特性)
├── stocks: Stock[] [Entity]
│   ├── stockId: StockId
│   ├── type: enum (MASTER, WORKING)
│   ├── preservationMethod: enum (FROZEN, LYOPHILIZED, CULTURE)
│   ├── location: StorageLocation
│   ├── quantity: number
│   ├── viability: number (生存率%)
│   └── lastChecked: Date
├── status: StrainStatus [Value Object]
│   └── value: enum (ACTIVE, DEPRECATED, QUARANTINE)
├── intellectualProperty: IPStatus [Value Object]
│   ├── patentNumber: string?
│   ├── filingDate: Date?
│   └── confidentiality: enum (TOP_SECRET, SECRET, INTERNAL, PUBLIC)
└── audit: AuditTrail [Value Object]
    ├── createdAt: Date
    ├── createdBy: UserId
    ├── modifiedAt: Date
    └── modifiedBy: UserId
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-YS-01 | strainIdは一意でASAHI-YYYY-NNNN形式であること |
| INV-YS-02 | BRED originの場合、parentStrainsは1つ以上存在すること |
| INV-YS-03 | 少なくとも1つのMASTER stockが存在すること |
| INV-YS-04 | 全stockのviabilityは0-100%の範囲であること |
| INV-YS-05 | viabilityが90%未満のstockはQUARANTINE対象 |

**主要メソッド:**
```
- registerNewStrain(taxonomy, origin, characteristics): YeastStrain
- addStock(type, preservationMethod, location, quantity): Stock
- updateViability(stockId, viability): void
- deprecate(reason): void
- transferToProductDevelopment(targetBC, quantity): TransferRecord
```

---

#### 集約2: FermentationExperiment（発酵実験）

**責務**: 実験の計画・実施・検証の管理

```
FermentationExperiment [Aggregate Root]
├── experimentId: ExperimentId [Value Object]
├── title: string
├── hypothesis: Hypothesis [Value Object]
│   ├── statement: string
│   └── expectedOutcome: string
├── protocol: ExperimentProtocol [Entity]
│   ├── strainId: StrainId
│   ├── conditions: FermentationCondition[]
│   ├── duration: Duration
│   ├── samplingSchedule: SamplingPoint[]
│   └── controlConditions: FermentationCondition
├── execution: ExperimentExecution [Entity]
│   ├── startDate: Date
│   ├── endDate: Date?
│   ├── status: enum (PLANNED, RUNNING, COMPLETED, ABORTED)
│   ├── samples: Sample[]
│   └── observations: Observation[]
├── results: ExperimentResults [Entity]
│   ├── measurements: Measurement[]
│   ├── analysis: StatisticalAnalysis
│   ├── conclusion: Conclusion
│   └── isHypothesisSupported: boolean
├── researcher: ResearcherId [Value Object]
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-FE-01 | 実験には必ず対照条件（control）が存在すること |
| INV-FE-02 | COMPLETED実験には必ずresultsが存在すること |
| INV-FE-03 | サンプリングポイントは時系列順であること |
| INV-FE-04 | 統計解析はp値を含むこと |
| INV-FE-05 | 実験記録は改ざん不可能（追記のみ）であること |

**主要メソッド:**
```
- createExperiment(title, hypothesis, protocol): FermentationExperiment
- startExecution(): void
- recordSample(sampleData): void
- recordObservation(observation): void
- completeExperiment(results): void
- abortExperiment(reason): void
```

---

#### 集約3: FermentationRecipe（発酵レシピ）

**責務**: 検証済み発酵条件の管理

```
FermentationRecipe [Aggregate Root]
├── recipeId: RecipeId [Value Object]
├── name: string
├── targetProduct: ProductType [Value Object]
│   └── value: enum (BEER, WINE, SAKE, SPIRITS, OTHER)
├── yeastStrain: StrainId [Value Object]
├── conditions: OptimizedConditions [Entity]
│   ├── temperature: TemperatureProfile
│   │   ├── initial: number
│   │   ├── fermentation: number
│   │   └── maturation: number
│   ├── initialGravity: number (初期比重)
│   ├── targetFinalGravity: number (目標最終比重)
│   ├── pH: pHRange
│   ├── oxygenation: OxygenLevel
│   ├── pitchingRate: number (酵母投入量)
│   └── fermentationTime: Duration
├── expectedOutcome: ExpectedOutcome [Value Object]
│   ├── alcoholContent: Range
│   ├── flavorProfile: FlavorProfile
│   └── qualityMetrics: QualityMetric[]
├── validationHistory: Validation[] [Entity]
│   ├── validationId: ValidationId
│   ├── experimentId: ExperimentId
│   ├── result: enum (PASSED, FAILED)
│   └── date: Date
├── version: Version [Value Object]
├── status: RecipeStatus [Value Object]
│   └── value: enum (DRAFT, VALIDATED, PRODUCTION, DEPRECATED)
└── confidentiality: ConfidentialityLevel [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-FR-01 | PRODUCTIONステータスには最低3回のVALIDATED検証が必要 |
| INV-FR-02 | 参照するyeastStrainはACTIVEステータスであること |
| INV-FR-03 | 温度プロファイルの値は-10℃～50℃の範囲であること |
| INV-FR-04 | バージョン番号は単調増加すること |
| INV-FR-05 | 機密レベルはTOP_SECRET以上の場合、アクセス制限が必要 |

**主要メソッド:**
```
- createRecipe(name, targetProduct, strain, conditions): FermentationRecipe
- updateConditions(newConditions): void
- addValidation(experimentId, result): void
- promoteToProduction(): void
- deprecate(reason, replacementRecipeId?): void
```

---

#### 集約4: TechnicalKnowHow（技術知見）

**責務**: 技術知見・ナレッジの管理

```
TechnicalKnowHow [Aggregate Root]
├── knowHowId: KnowHowId [Value Object]
├── title: string
├── category: KnowHowCategory [Value Object]
│   └── value: enum (FERMENTATION, YEAST, PROCESS, TROUBLESHOOTING, TACIT)
├── content: KnowHowContent [Entity]
│   ├── summary: string
│   ├── detail: string (markdown)
│   ├── attachments: Attachment[]
│   └── relatedExperiments: ExperimentId[]
├── source: KnowHowSource [Value Object]
│   ├── type: enum (EXPERIMENT, EXPERT, LITERATURE, INCIDENT)
│   ├── sourceId: string
│   └── expertName: string? (暗黙知の場合)
├── applicability: Applicability [Value Object]
│   ├── strains: StrainId[]
│   ├── products: ProductType[]
│   └── conditions: string[]
├── intellectualProperty: IPStatus [Value Object]
│   ├── patentable: boolean
│   ├── patentId: string?
│   └── confidentiality: ConfidentialityLevel
├── review: ReviewStatus [Entity]
│   ├── status: enum (DRAFT, UNDER_REVIEW, APPROVED, ARCHIVED)
│   ├── reviewers: ReviewerId[]
│   └── approvedDate: Date?
├── tags: Tag[] [Value Object]
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-TK-01 | APPROVEDステータスには最低1名のレビューが必要 |
| INV-TK-02 | patentable=trueの場合、外部公開は禁止 |
| INV-TK-03 | TACITカテゴリにはsource.expertNameが必須 |
| INV-TK-04 | 関連実験がある場合、experimentIdは有効であること |

**主要メソッド:**
```
- createKnowHow(title, category, content, source): TechnicalKnowHow
- submitForReview(): void
- approve(reviewerId): void
- linkToExperiment(experimentId): void
- filePatent(patentApplication): void
- archive(reason): void
```

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **YeastStrainRegistered** | {strainId, taxonomy, characteristics, registeredAt} | 新規酵母株の登録完了時 | premium-beer-dev, craft-innovation-dev, spirits-dev |
| **YeastStrainImproved** | {strainId, parentStrains, improvements, improvedAt} | 改良株の作出完了時 | premium-beer-dev, craft-innovation-dev |
| **FermentationRecipeOptimized** | {recipeId, strainId, conditions, validationCount, optimizedAt} | レシピがPRODUCTION昇格時 | premium-beer-dev, craft-innovation-dev, process-engineering |
| **ExperimentCompleted** | {experimentId, strainId, hypothesis, isSupported, completedAt} | 実験完了・検証時 | internal（知見体系化用） |
| **TechnicalKnowHowApproved** | {knowHowId, category, applicability, approvedAt} | 技術知見承認時 | process-engineering, 全製品開発BC |

---

### 6. コンテキストマップ（Context Map）

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    │     fermentation-research-bc         │
                    │           (Upstream)                 │
                    │                                      │
                    └──────────────┬───────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ premium-beer-   │    │ craft-          │    │ spirits-        │
│ development-bc  │    │ innovation-     │    │ development-bc  │
│ (Downstream)    │    │ development-bc  │    │ (Downstream)    │
│                 │    │ (Downstream)    │    │                 │
│ [Customer-      │    │ [Customer-      │    │ [Customer-      │
│  Supplier]      │    │  Supplier]      │    │  Supplier]      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│ ingredient-     │    │ process-        │
│ research-bc     │    │ engineering-bc  │
│                 │    │                 │
│ [Partnership]   │    │ [Conformist]    │
└─────────────────┘    └─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| premium-beer-development-bc | **Customer-Supplier** | 発酵研究が酵母株・技術を供給。開発BCのニーズを考慮 |
| craft-innovation-development-bc | **Customer-Supplier** | 特殊酵母・革新技術を供給 |
| spirits-development-bc | **Customer-Supplier** | 蒸留用酵母を供給 |
| ingredient-research-bc | **Partnership** | 素材と発酵の組み合わせ研究で対等に協力 |
| process-engineering-bc | **Conformist** | 製造プロセス設計が発酵研究の知見に従う |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/strains` | POST | 新規酵母株の登録 |
| `/strains/{id}/stocks` | POST | ストックの追加 |
| `/strains/{id}/transfer` | POST | 製品開発BCへの株移転 |
| `/experiments` | POST | 新規実験の作成 |
| `/experiments/{id}/complete` | POST | 実験完了・結果登録 |
| `/recipes` | POST | 新規レシピ作成 |
| `/recipes/{id}/validate` | POST | レシピ検証結果の追加 |
| `/recipes/{id}/promote` | POST | PRODUCTION昇格 |
| `/knowhow` | POST | 技術知見の登録 |
| `/knowhow/{id}/approve` | POST | 知見の承認 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/strains` | GET | 酵母株一覧取得（フィルタ対応） |
| `/strains/{id}` | GET | 酵母株詳細取得 |
| `/strains/search` | GET | 特性による酵母株検索 |
| `/recipes` | GET | レシピ一覧取得 |
| `/recipes/{id}` | GET | レシピ詳細取得 |
| `/recipes/for-product/{productType}` | GET | 製品タイプ別レシピ検索 |
| `/knowhow/search` | GET | 技術知見検索 |
| `/experiments/{id}` | GET | 実験詳細取得 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| ingredient-research-bc | 素材情報の参照（素材と酵母の相性評価） |
| identity-management-bc | 研究者認証・権限管理 |
| audit-logging-bc | 監査ログの記録 |

---

## 次のステップ

### CL3完了後の推奨アクション

1. **他のCore サブドメインのCL3定義**
   - premium-beer-development-bc
   - ingredient-research-bc

2. **Phase 4: Architecture への移行**
   - Context Map統合設計
   - イベント駆動アーキテクチャ設計
   - 技術スタック選定

3. **API契約の詳細設計**
   - api-contract-designer による詳細仕様作成

---

**作成完了:** 2025-11-26
**ステータス:** CL3完了（fermentation-research-bc定義）
**次のフェーズ:** 他Core SDのCL3 または Phase 4: Architecture
