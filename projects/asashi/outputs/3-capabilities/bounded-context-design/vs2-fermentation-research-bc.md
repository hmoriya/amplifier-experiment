# Bounded Context: Fermentation Research (FRM-BC)

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** vs2-fermentation-research (発酵技術研究)
**ドメインタイプ:** Core Domain
**作成日:** 2025-11-26
**分析モード:** zen-architect (ARCHITECT mode) + api-contract-designer

---

## 1. Bounded Context 概要

### 1.1 基本情報

| 項目 | 内容 |
|------|------|
| **BC名 (英語)** | Fermentation Research Bounded Context (FRM-BC) |
| **BC名 (日本語)** | 発酵技術研究境界コンテキスト |
| **ドメインタイプ** | Core Domain |
| **チームトポロジー** | Complicated-Subsystem Team |

### 1.2 目的

競争優位の源泉である酵母・発酵技術の継続的研究と革新を行う。100年以上の蓄積を活かし、模倣困難な技術資産を維持・発展させる。

**具体的責務:**
- 独自酵母株の発見・育種・特性評価・保存
- 発酵プロセスの研究・最適化
- 乳酸菌・枯草菌等の機能性微生物研究
- 新規原料・機能性素材の探索

### 1.3 チーム構成推奨

```
┌────────────────────────────────────────────────────────────┐
│         Fermentation Research Team (Complicated-Subsystem) │
├────────────────────────────────────────────────────────────┤
│  Research Scientists (発酵技術専門家)        3-4名          │
│  Bioinformatics Specialists                  1-2名          │
│  Domain-Driven Developers                    2-3名          │
│  Security/Compliance Engineer                1名            │
│  DevOps Engineer                             1名            │
│  Technical Lead (DDD経験必須)                1名            │
└────────────────────────────────────────────────────────────┘
```

---

## 2. ユビキタス言語 (Ubiquitous Language)

研究者とエンジニアが共通で使用する用語を定義する。

### 2.1 コア概念

| 英語 | 日本語 | 定義 | 使用例 |
|------|--------|------|--------|
| **Yeast Strain** | 酵母株 | 特定の遺伝的特性を持つ単離された酵母の系統。Asahi独自の競争優位資産。 | 「この酵母株は辛口発酵に最適化されている」 |
| **Strain Code** | 株コード | 酵母株を一意に識別するための社内コード体系 (例: AS-Y-0001) | 「株コード AS-Y-0325 を培養庫から取り出す」 |
| **Fermentation Process** | 発酵プロセス | 酵母が糖をアルコールと炭酸ガスに変換する生化学的プロセス | 「発酵プロセスを5日から4日に短縮した」 |
| **Brewing Parameters** | 醸造パラメータ | 発酵を制御する温度・時間・pH等の条件値 | 「最適な醸造パラメータを同定した」 |
| **Attenuation** | 発酵度 | 酵母が糖を消費する能力を示す指標 (%) | 「高発酵度酵母で辛口ビールを実現」 |
| **Flocculation** | 凝集性 | 発酵終了時に酵母が沈殿・凝集する特性 | 「高凝集性により清澄化が容易」 |

### 2.2 研究プロセス

| 英語 | 日本語 | 定義 | 使用例 |
|------|--------|------|--------|
| **Strain Discovery** | 株発見 | 新しい酵母株を自然界や突然変異から発見するプロセス | 「株発見イベントを記録する」 |
| **Strain Breeding** | 株育種 | 交配や遺伝子操作により新しい特性を持つ株を開発 | 「株育種により耐アルコール性を向上」 |
| **Fermentation Experiment** | 発酵実験 | 特定条件下で発酵プロセスを検証する科学的実験 | 「発酵実験 FEX-2025-042 を開始」 |
| **Performance Characterization** | 性能特性評価 | 酵母株の発酵性能を定量的に測定・記録するプロセス | 「新株の性能特性評価を完了」 |
| **Protocol** | プロトコル | 実験手順を標準化した文書 | 「標準プロトコルに従って実験を実施」 |

### 2.3 データ管理

| 英語 | 日本語 | 定義 | 使用例 |
|------|--------|------|--------|
| **Genetic Profile** | 遺伝子プロファイル | 酵母株のゲノム配列と遺伝子マーカー情報 | 「遺伝子プロファイルをデータベースに登録」 |
| **Genetic Marker** | 遺伝子マーカー | 株の同定や特性予測に使用される特定の遺伝子座位 | 「POF遺伝子マーカーでフェノール産生を確認」 |
| **Culture Collection** | 株保存庫 | 酵母株を長期保存するための設備・システム | 「株保存庫からAS-Y-0142を取り出し」 |
| **Preservation Method** | 保存方法 | 株を長期間維持するための技術 (凍結、凍結乾燥等) | 「凍結乾燥による保存方法を選択」 |

### 2.4 組織・プロジェクト

| 英語 | 日本語 | 定義 | 使用例 |
|------|--------|------|--------|
| **Research Project** | 研究プロジェクト | 特定の研究目標を達成するためのプロジェクト | 「低温発酵プロジェクトが第3マイルストーンに到達」 |
| **Research Milestone** | 研究マイルストーン | プロジェクトの重要な達成点 | 「マイルストーン: 候補株の選定完了」 |
| **IP Disclosure** | 知財開示 | 特許出願可能な発明の社内開示 | 「新製法のIP開示を提出」 |
| **Security Clearance** | セキュリティクリアランス | 機密データへのアクセス権限レベル | 「遺伝子データには極秘クリアランスが必要」 |

### 2.5 微生物研究

| 英語 | 日本語 | 定義 | 使用例 |
|------|--------|------|--------|
| **Lactic Acid Bacteria** | 乳酸菌 | 乳酸発酵を行う細菌群（カルピス等に使用） | 「新しい乳酸菌株を機能性飲料に適用」 |
| **Bacillus subtilis** | 枯草菌 | 納豆菌等、食品発酵に有用な細菌 | 「枯草菌の酵素生産能を評価」 |
| **Functional Ingredient** | 機能性素材 | 健康効果が期待される原料・成分 | 「機能性素材の探索を開始」 |
| **Metabolite** | 代謝産物 | 微生物が産生する化合物（香気成分等） | 「代謝産物プロファイルを分析」 |

---

## 3. 集約 (Aggregates)

### 3.1 YeastStrain 集約 (酵母株)

**集約ルート:** `YeastStrain`

```
┌─────────────────────────────────────────────────────────────┐
│                    YeastStrain Aggregate                    │
├─────────────────────────────────────────────────────────────┤
│  <<Aggregate Root>>                                         │
│  YeastStrain                                                │
│  ├── StrainId (株ID)                                        │
│  ├── StrainCode (株コード)                                  │
│  ├── CommonName (通称)                                      │
│  ├── ScientificName (学名)                                  │
│  ├── Status (状態: Active/Archived/UnderEvaluation)         │
│  ├── SecurityClassification (機密分類)                      │
│  ├── DiscoveredBy (発見者)                                  │
│  └── DiscoveryDate (発見日)                                 │
│                                                             │
│  <<Entities>>                                               │
│  ├── PerformanceCharacteristics (性能特性)                  │
│  │   ├── Attenuation (発酵度)                               │
│  │   ├── Flocculation (凝集性)                              │
│  │   ├── OptimalTemperatureRange (最適温度範囲)             │
│  │   └── AlcoholTolerance (耐アルコール性)                  │
│  │                                                          │
│  └── GeneticProfile (遺伝子プロファイル)                    │
│      ├── GenomeSequence (ゲノム配列 - 暗号化)               │
│      ├── GeneticMarkers (遺伝子マーカー)                    │
│      ├── ParentalLineage (親株系譜)                         │
│      └── SequencingDate (シーケンス日)                      │
│                                                             │
│  <<Value Objects>>                                          │
│  ├── StrainId (値オブジェクト: AS-Y-{NNNN})                 │
│  ├── ScientificName (学名: Genus + Species + Subspecies)    │
│  ├── OptimalTemperatureRange (最適温度範囲: Min-Max)        │
│  ├── AttenuationPercentage (発酵度: 0-100%)                 │
│  ├── FlocculationLevel (凝集性: Low/Medium/High/VeryHigh)   │
│  └── SecurityClassification (機密分類: TopSecret/Secret/Confidential)
└─────────────────────────────────────────────────────────────┘
```

**不変条件 (Invariants):**

| ID | 不変条件 | 説明 |
|----|----------|------|
| INV-YS-01 | 株コードは一意 | 同じ株コードを持つ酵母株は存在しない |
| INV-YS-02 | 極秘データの保護 | GeneticProfileは極秘クリアランス保持者のみアクセス可能 |
| INV-YS-03 | 有効な発酵度範囲 | Attenuationは0-100%の範囲内 |
| INV-YS-04 | アーカイブ株は変更不可 | Status=Archivedの株は特性の変更不可 |
| INV-YS-05 | 発見者の記録必須 | 新規株は必ず発見者と発見日が記録される |

---

### 3.2 FermentationExperiment 集約 (発酵実験)

**集約ルート:** `FermentationExperiment`

```
┌─────────────────────────────────────────────────────────────┐
│               FermentationExperiment Aggregate              │
├─────────────────────────────────────────────────────────────┤
│  <<Aggregate Root>>                                         │
│  FermentationExperiment                                     │
│  ├── ExperimentId (実験ID: FEX-YYYY-NNN)                    │
│  ├── Title (タイトル)                                       │
│  ├── Objective (目的)                                       │
│  ├── ProtocolReference (プロトコル参照)                     │
│  ├── Status (状態: Planned/InProgress/Completed/Aborted)    │
│  ├── PrincipalInvestigator (主任研究者)                     │
│  └── ProjectReference (プロジェクト参照)                    │
│                                                             │
│  <<Entities>>                                               │
│  ├── ExperimentConditions (実験条件)                        │
│  │   ├── StrainUsed (使用株)                                │
│  │   ├── Temperature (温度)                                 │
│  │   ├── Duration (期間)                                    │
│  │   ├── InitialGravity (初期比重)                          │
│  │   ├── pH (pH値)                                          │
│  │   └── WortComposition (麦汁組成)                         │
│  │                                                          │
│  ├── Measurement (測定データ) ※複数                        │
│  │   ├── MeasurementId                                      │
│  │   ├── MeasurementType (測定タイプ)                       │
│  │   ├── Value (値)                                         │
│  │   ├── Unit (単位)                                        │
│  │   ├── Timestamp (日時)                                   │
│  │   └── MeasuredBy (測定者)                                │
│  │                                                          │
│  └── ExperimentResult (実験結果)                            │
│      ├── FinalGravity (最終比重)                            │
│      ├── ActualAttenuation (実際の発酵度)                   │
│      ├── AlcoholByVolume (アルコール度数)                   │
│      ├── FlavorProfile (風味プロファイル)                   │
│      └── Conclusion (結論)                                  │
│                                                             │
│  <<Value Objects>>                                          │
│  ├── ExperimentId (実験ID: FEX-YYYY-NNN)                    │
│  ├── TemperatureRange (温度範囲: Min-Max-Unit)              │
│  ├── GravityReading (比重: Value + Unit)                    │
│  └── FlavorProfile (風味プロファイル: List<FlavorNote>)     │
└─────────────────────────────────────────────────────────────┘
```

**不変条件 (Invariants):**

| ID | 不変条件 | 説明 |
|----|----------|------|
| INV-FE-01 | 実験IDは一意 | 同じ実験IDは存在しない |
| INV-FE-02 | 有効な株参照 | 使用する株は存在し、Active状態 |
| INV-FE-03 | 完了実験は変更不可 | Completed/Aborted実験の条件は変更不可 |
| INV-FE-04 | 測定は時系列順 | 測定データは時間順に追記のみ可能 |
| INV-FE-05 | 結果は完了時のみ | ExperimentResultはStatusがCompletedの場合のみ設定可能 |

---

### 3.3 ResearchProject 集約 (研究プロジェクト)

**集約ルート:** `ResearchProject`

```
┌─────────────────────────────────────────────────────────────┐
│                   ResearchProject Aggregate                 │
├─────────────────────────────────────────────────────────────┤
│  <<Aggregate Root>>                                         │
│  ResearchProject                                            │
│  ├── ProjectId (プロジェクトID: RP-YYYY-NNN)                │
│  ├── Title (タイトル)                                       │
│  ├── Description (説明)                                     │
│  ├── Status (状態: Planning/Active/Suspended/Completed)     │
│  ├── ProjectLead (プロジェクトリーダー)                     │
│  ├── StartDate (開始日)                                     │
│  └── TargetEndDate (目標終了日)                             │
│                                                             │
│  <<Entities>>                                               │
│  ├── ResearchMilestone (マイルストーン) ※複数              │
│  │   ├── MilestoneId                                        │
│  │   ├── Title (タイトル)                                   │
│  │   ├── Description (説明)                                 │
│  │   ├── TargetDate (目標日)                                │
│  │   ├── Status (状態: Pending/Achieved/Delayed/Cancelled)  │
│  │   └── AchievedDate (達成日)                              │
│  │                                                          │
│  └── IPDisclosure (知財開示) ※複数                         │
│      ├── DisclosureId                                       │
│      ├── Title (発明名)                                     │
│      ├── Description (内容)                                 │
│      ├── Inventors (発明者リスト)                           │
│      ├── SubmissionDate (提出日)                            │
│      └── Status (状態: Draft/Submitted/UnderReview/Filed)   │
│                                                             │
│  <<Value Objects>>                                          │
│  ├── ProjectId (プロジェクトID: RP-YYYY-NNN)                │
│  ├── DateRange (期間: Start-End)                            │
│  └── InventorList (発明者リスト: List<ResearcherId>)        │
└─────────────────────────────────────────────────────────────┘
```

**不変条件 (Invariants):**

| ID | 不変条件 | 説明 |
|----|----------|------|
| INV-RP-01 | プロジェクトIDは一意 | 同じプロジェクトIDは存在しない |
| INV-RP-02 | 有効な日付範囲 | TargetEndDate >= StartDate |
| INV-RP-03 | マイルストーンの順序 | マイルストーンは目標日の時系列順 |
| INV-RP-04 | 完了プロジェクトの制約 | Completedプロジェクトは新規マイルストーン追加不可 |
| INV-RP-05 | IP開示の追跡可能性 | IP開示は必ず1名以上の発明者を持つ |

---

### 3.4 MicrobialCulture 集約 (微生物培養)

**集約ルート:** `MicrobialCulture`

```
┌─────────────────────────────────────────────────────────────┐
│                   MicrobialCulture Aggregate                │
├─────────────────────────────────────────────────────────────┤
│  <<Aggregate Root>>                                         │
│  MicrobialCulture                                           │
│  ├── CultureId (培養ID: MC-{TYPE}-NNNN)                     │
│  ├── MicroorganismType (微生物タイプ: Yeast/LAB/Bacillus)   │
│  ├── SourceStrainId (元株参照: nullable)                    │
│  ├── PreservationMethod (保存方法)                          │
│  ├── StorageLocation (保管場所)                             │
│  ├── CreatedDate (作成日)                                   │
│  └── ExpirationDate (有効期限)                              │
│                                                             │
│  <<Entities>>                                               │
│  ├── VialInventory (バイアル在庫) ※複数                    │
│  │   ├── VialId (バイアルID)                                │
│  │   ├── VialNumber (バイアル番号)                          │
│  │   ├── CreationDate (作成日)                              │
│  │   ├── Status (状態: Available/Used/Expired/Discarded)    │
│  │   └── UsedBy (使用実験参照: nullable)                    │
│  │                                                          │
│  └── ViabilityTest (生存試験結果) ※複数                    │
│      ├── TestId (試験ID)                                    │
│      ├── TestDate (試験日)                                  │
│      ├── ViabilityPercentage (生存率%)                      │
│      ├── TestedBy (試験者)                                  │
│      └── Notes (備考)                                       │
│                                                             │
│  <<Value Objects>>                                          │
│  ├── CultureId (培養ID: MC-{TYPE}-NNNN)                     │
│  ├── PreservationMethod (保存方法: Frozen/Lyophilized/Agar) │
│  ├── StorageLocation (保管場所: Freezer-Shelf-Position)     │
│  └── ViabilityPercentage (生存率: 0-100%)                   │
└─────────────────────────────────────────────────────────────┘
```

**不変条件 (Invariants):**

| ID | 不変条件 | 説明 |
|----|----------|------|
| INV-MC-01 | 培養IDは一意 | 同じ培養IDは存在しない |
| INV-MC-02 | 有効期限の妥当性 | ExpirationDate > CreatedDate |
| INV-MC-03 | バイアル使用の追跡 | Usedバイアルは使用実験参照が必須 |
| INV-MC-04 | 生存率の範囲 | ViabilityPercentageは0-100% |
| INV-MC-05 | 期限切れバイアル使用禁止 | ExpirationDate超過の培養からバイアル使用不可 |

---

## 4. ドメインイベント (Domain Events)

### 4.1 YeastStrain 関連イベント

| イベント名 | ペイロード | サブスクライバー |
|-----------|-----------|-----------------|
| **YeastStrainDiscovered** | StrainId, StrainCode, CommonName, DiscoveredBy, DiscoveryDate | Recipe Management BC, Product Dev BC |
| **YeastStrainCharacterized** | StrainId, PerformanceCharacteristics (sanitized), CharacterizationDate | Recipe Management BC, Product Dev BC |
| **GeneticProfileCompleted** | StrainId, GeneticMarkers (sanitized), CompletionDate | 内部のみ (極秘) |
| **YeastStrainArchived** | StrainId, ArchivedBy, ArchiveReason, ArchiveDate | Recipe Management BC |
| **YeastStrainReactivated** | StrainId, ReactivatedBy, ReactivationReason | Product Dev BC |

### 4.2 FermentationExperiment 関連イベント

| イベント名 | ペイロード | サブスクライバー |
|-----------|-----------|-----------------|
| **ExperimentStarted** | ExperimentId, Title, StrainUsed, PrincipalInvestigator, StartDate | Project Management |
| **ExperimentMeasurementRecorded** | ExperimentId, MeasurementType, Value, Timestamp | Analytics BC |
| **ExperimentCompleted** | ExperimentId, ResultSummary, CompletionDate | Product Dev BC, Recipe Management BC |
| **ExperimentAborted** | ExperimentId, AbortReason, AbortedBy, AbortDate | Project Management |
| **FermentationProcessOptimized** | ExperimentId, OptimizedParameters, ImprovementPercentage | Recipe Management BC, Product Dev BC |

### 4.3 ResearchProject 関連イベント

| イベント名 | ペイロード | サブスクライバー |
|-----------|-----------|-----------------|
| **ResearchProjectCreated** | ProjectId, Title, ProjectLead, StartDate | Analytics BC |
| **MilestoneAchieved** | ProjectId, MilestoneId, MilestoneTitle, AchievedDate | Management Dashboard |
| **IPDisclosureSubmitted** | ProjectId, DisclosureId, Title, Inventors | Legal/IP Department |
| **ResearchProjectCompleted** | ProjectId, FinalOutcome, CompletionDate | Analytics BC, Management |

### 4.4 MicrobialCulture 関連イベント

| イベント名 | ペイロード | サブスクライバー |
|-----------|-----------|-----------------|
| **CulturePreserved** | CultureId, MicroorganismType, PreservationMethod, VialCount | Culture Repository |
| **CultureVialUsed** | CultureId, VialId, UsedForExperiment, UsedBy, UsageDate | Inventory Management |
| **ViabilityTestPerformed** | CultureId, ViabilityPercentage, TestDate | Quality Assurance |
| **CultureExpired** | CultureId, ExpirationDate | Culture Repository, Inventory |

---

## 5. コンテキストマップ (Context Map)

### 5.1 関係図

```
                    ┌─────────────────────────────┐
                    │  External Research Partners  │
                    │  (大学・研究機関)            │
                    └──────────────┬──────────────┘
                                   │
                           Partnership (双方向)
                        Open Host Service / ACL
                                   │
    ┌──────────────────────────────┼──────────────────────────────┐
    │                              ▼                              │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │     Fermentation Research BC (FRM-BC)              │    │
    │  │     発酵技術研究コンテキスト                        │    │
    │  │                                                     │    │
    │  │  • YeastStrain Aggregate                           │    │
    │  │  • FermentationExperiment Aggregate                │    │
    │  │  • ResearchProject Aggregate                       │    │
    │  │  • MicrobialCulture Aggregate                      │    │
    │  └──────────────────┬────────────────────────────────┘    │
    │                      │                                     │
    │     ┌────────────────┼────────────────┐                   │
    │     │                │                │                   │
    │     ▼                ▼                ▼                   │
    │ Published       Customer-       Published                 │
    │ Language        Supplier        Language                  │
    │     │                │                │                   │
    │     ▼                ▼                ▼                   │
    │ ┌─────────┐  ┌──────────────┐  ┌───────────────┐         │
    │ │Recipe   │  │Alcoholic     │  │Beverage       │         │
    │ │Mgmt BC  │  │Product Dev BC│  │Product Dev BC │         │
    │ │レシピ管理│  │酒類製品開発  │  │飲料製品開発   │         │
    │ └─────────┘  └──────────────┘  └───────────────┘         │
    │                                                            │
    └────────────────────────────────────────────────────────────┘
                    VS2: 製品開発・イノベーション
```

### 5.2 関係詳細

| 関係タイプ | パートナーBC | 方向 | 説明 |
|-----------|-------------|------|------|
| **Customer-Supplier** | vs2-alcoholic-product-dev | Downstream (顧客) | 酵母株・発酵技術を製品開発チームに提供。FRM-BCが上流(Supplier) |
| **Customer-Supplier** | vs2-beverage-product-dev | Downstream (顧客) | 発酵・微生物技術を飲料開発チームに提供。FRM-BCが上流 |
| **Published Language** | vs2-recipe-management | Downstream | 発酵パラメータを標準化されたフォーマット(Published Language)で提供 |
| **Partnership** | External Research | Bidirectional | 大学・研究機関との共同研究。双方向のデータ交換 |
| **Open Host Service** | External Research | Outbound | 外部パートナー向けの公開API (匿名化・制限されたデータ) |
| **Anti-Corruption Layer** | vs2-recipe-management | Inbound | レシピ管理BCからの要求を翻訳し、内部モデルを保護 |

### 5.3 データフロー制御

```yaml
# 外部公開可能データ (Published Language)
PublicStrainCatalog:
  - StrainCode (株コード)
  - CommonName (通称)
  - Status (状態)
  - PerformanceCharacteristics (性能特性 - 概要のみ)
  - RecommendedUseCase (推奨用途)

# 製品開発BC向け詳細データ (Customer-Supplier)
ProductDevStrainData:
  - All PublicStrainCatalog fields
  - DetailedCharacteristics (詳細特性)
  - OptimalConditions (最適条件)
  - CompatibilityNotes (互換性ノート)

# 内部専用データ (Never Exposed)
InternalOnly:
  - GeneticProfile (遺伝子プロファイル)
  - GenomeSequence (ゲノム配列)
  - BreedingHistory (育種履歴)
  - TradeSecrets (企業秘密)
```

---

## 6. コマンドとクエリ (CQRS)

### 6.1 コマンド (Commands - 書き込み操作)

#### YeastStrain コマンド

| コマンド | 説明 | 必要権限 |
|---------|------|----------|
| `RegisterNewStrain` | 新しい酵母株を登録 | Researcher |
| `UpdateStrainCharacteristics` | 性能特性を更新 | Researcher |
| `RecordGeneticProfile` | 遺伝子プロファイルを記録 | SeniorResearcher + TopSecretClearance |
| `ArchiveStrain` | 株をアーカイブ | TeamLead |
| `ReactivateStrain` | アーカイブ株を再有効化 | TeamLead |

#### FermentationExperiment コマンド

| コマンド | 説明 | 必要権限 |
|---------|------|----------|
| `CreateExperiment` | 新規実験を作成 | Researcher |
| `SetExperimentConditions` | 実験条件を設定 | Researcher |
| `RecordMeasurement` | 測定データを記録 | Researcher |
| `CompleteExperiment` | 実験を完了としてマーク | PrincipalInvestigator |
| `AbortExperiment` | 実験を中止 | PrincipalInvestigator |

#### ResearchProject コマンド

| コマンド | 説明 | 必要権限 |
|---------|------|----------|
| `CreateProject` | 新規プロジェクトを作成 | TeamLead |
| `AddMilestone` | マイルストーンを追加 | ProjectLead |
| `AchieveMilestone` | マイルストーン達成を記録 | ProjectLead |
| `SubmitIPDisclosure` | 知財開示を提出 | Researcher |
| `CompleteProject` | プロジェクトを完了 | TeamLead |

#### MicrobialCulture コマンド

| コマンド | 説明 | 必要権限 |
|---------|------|----------|
| `PreserveCulture` | 新しい培養を保存 | Researcher |
| `UseVial` | バイアルを使用記録 | Researcher |
| `RecordViabilityTest` | 生存試験を記録 | Researcher |
| `DiscardExpiredCulture` | 期限切れ培養を廃棄 | LabTechnician |

### 6.2 クエリ (Queries - 読み取り操作)

#### 株カタログクエリ

| クエリ | 説明 | 必要権限 |
|-------|------|----------|
| `GetStrainById` | 株IDで検索 | Researcher |
| `SearchStrains` | 条件検索 (特性、用途等) | Researcher |
| `GetStrainCatalog` | 公開カタログ取得 | ProductDev (外部BC) |
| `GetStrainGeneticProfile` | 遺伝子情報取得 | SeniorResearcher + TopSecretClearance |
| `GetStrainUsageHistory` | 株の使用履歴 | Researcher |

#### 実験クエリ

| クエリ | 説明 | 必要権限 |
|-------|------|----------|
| `GetExperimentById` | 実験IDで取得 | Researcher |
| `GetExperimentsByStrain` | 株別実験一覧 | Researcher |
| `GetExperimentResults` | 実験結果取得 | Researcher |
| `GetExperimentTimeSeries` | 測定データ時系列 | Researcher |

#### プロジェクトクエリ

| クエリ | 説明 | 必要権限 |
|-------|------|----------|
| `GetProjectStatus` | プロジェクト状況 | Researcher |
| `GetProjectMilestones` | マイルストーン一覧 | Researcher |
| `GetIPDisclosures` | 知財開示一覧 | TeamLead |
| `GetProjectDashboard` | ダッシュボード用集計 | Management |

#### 培養クエリ

| クエリ | 説明 | 必要権限 |
|-------|------|----------|
| `GetCultureInventory` | 培養在庫一覧 | Researcher |
| `GetAvailableVials` | 利用可能バイアル | Researcher |
| `GetCultureViabilityHistory` | 生存率履歴 | Researcher |
| `GetExpiringCultures` | 期限間近培養 | LabTechnician |

---

## 7. 実装推奨事項

### 7.1 技術スタック推奨

```yaml
Backend:
  Language: Python 3.11+
  Framework: FastAPI (async対応、型安全)
  Database:
    Primary: PostgreSQL 15+ (JSONB for flexible data)
    Cache: Redis (for read models)
  Event Store: PostgreSQL with Event Sourcing pattern
  Message Broker: Apache Kafka (for domain events)

Security:
  Authentication: Keycloak (OIDC)
  Authorization: OPA (Open Policy Agent) for ABAC
  Encryption:
    At Rest: AES-256 (PostgreSQL TDE)
    In Transit: TLS 1.3
    Field Level: SQLCipher for genetic data

Infrastructure:
  Container: Docker + Kubernetes
  CI/CD: GitHub Actions
  Monitoring: Prometheus + Grafana
  Logging: ELK Stack (Elasticsearch, Logstash, Kibana)
```

### 7.2 セキュリティ考慮事項

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Network Security                                  │
│  ├── VPC isolation (no public endpoints)                    │
│  ├── WAF (Web Application Firewall)                         │
│  └── DDoS protection                                        │
│                                                             │
│  Layer 2: Application Security                              │
│  ├── OIDC authentication (Keycloak)                         │
│  ├── ABAC authorization (OPA)                               │
│  ├── Input validation                                       │
│  └── Rate limiting                                          │
│                                                             │
│  Layer 3: Data Security                                     │
│  ├── Row-Level Security (PostgreSQL RLS)                    │
│  ├── Field-level encryption (genetic data)                  │
│  ├── Data masking for external APIs                         │
│  └── Audit logging (immutable)                              │
│                                                             │
│  Layer 4: Physical Security                                 │
│  ├── Data center security (SOC 2 Type II)                   │
│  ├── Backup encryption                                      │
│  └── Air-gapped archive for Top Secret data                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**アクセス制御マトリックス:**

| データタイプ | Researcher | SeniorResearcher | TeamLead | ProductDev (外部BC) |
|-------------|------------|------------------|----------|---------------------|
| Strain Basic Info | Read | Read/Write | Read/Write | Read (Catalog) |
| Performance Characteristics | Read | Read/Write | Read/Write | Read (Summary) |
| Genetic Profile | - | Read/Write | Read | - |
| Genome Sequence | - | Read/Write | Read | - |
| Experiment Data | Read/Write (own) | Read/Write | Read/Write | - |
| IP Disclosures | Read (own) | Read/Write | Read/Write | - |

### 7.3 統合パターン

```yaml
# 外部BC向けAPI (Published Language)
StrainCatalogAPI:
  Endpoint: /api/v1/strains/catalog
  Authentication: OAuth2 Client Credentials
  Rate Limit: 1000 req/hour
  Data: Sanitized, public-safe data only
  Format: JSON Schema with OpenAPI spec

# イベント駆動統合
DomainEvents:
  Broker: Kafka
  Topic Pattern: frm-bc.{aggregate}.{event}
  Examples:
    - frm-bc.yeast-strain.discovered
    - frm-bc.experiment.completed
    - frm-bc.fermentation-process.optimized
  Serialization: Avro with Schema Registry
  Security: Event payload sanitization before publish

# Anti-Corruption Layer
RecipeManagementACL:
  Purpose: Translate Recipe BC requests to internal model
  Pattern: Adapter + Translator
  Implementation:
    - Validate incoming requests
    - Map external concepts to internal Ubiquitous Language
    - Filter sensitive data from responses
```

### 7.4 テスト戦略

```yaml
Unit Tests (60%):
  - Aggregate invariant validation
  - Value Object validation
  - Domain event generation
  - Command handlers
  - Query handlers

Integration Tests (30%):
  - Repository implementations
  - Event publishing/subscribing
  - External API contracts (Consumer Driven Contracts)
  - Security policy enforcement

End-to-End Tests (10%):
  - Critical user journeys
  - Security scenarios (unauthorized access attempts)
  - Data migration validation
```

---

## 8. 次のステップ

### 8.1 CL3 継続

他のCoreサブドメインのBounded Context定義:

```bash
# 推奨順序
/parasol:3-capabilities cl3 vs2-alcoholic-product-dev
/parasol:3-capabilities cl3 vs2-recipe-management
```

### 8.2 Phase 4 への進行条件

- [ ] 全CoreサブドメインのBC定義完了
- [ ] Supportingサブドメインの主要BC定義完了
- [ ] コンテキストマップの検証
- [ ] 技術検証 (PoC) の実施

---

## 9. 付録: 用語対応表

| 英語 | 日本語 | カテゴリ |
|------|--------|----------|
| Bounded Context | 境界づけられたコンテキスト | DDD |
| Aggregate | 集約 | DDD |
| Aggregate Root | 集約ルート | DDD |
| Entity | エンティティ | DDD |
| Value Object | 値オブジェクト | DDD |
| Invariant | 不変条件 | DDD |
| Domain Event | ドメインイベント | DDD |
| Ubiquitous Language | ユビキタス言語 | DDD |
| Customer-Supplier | 顧客-供給者 | Context Map |
| Published Language | 公開言語 | Context Map |
| Anti-Corruption Layer | 腐敗防止層 | Context Map |
| Open Host Service | オープンホストサービス | Context Map |
| Partnership | パートナーシップ | Context Map |

---

**作成完了:** 2025-11-26
**ステータス:** CL3 Bounded Context定義完了 (vs2-fermentation-research)
**次のフェーズ:** CL3継続 (vs2-alcoholic-product-dev) または Phase 4へ
