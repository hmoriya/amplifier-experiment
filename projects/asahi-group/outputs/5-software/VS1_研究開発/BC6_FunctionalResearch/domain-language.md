# BC6: Functional Research - ドメイン言語定義

## 概要

機能性研究のドメイン。乳酸菌研究、機能性成分の探索、健康効果の実証を担う。

**BCタイプ**: Supporting（VS1内でBC1を支援）
**技術スタック**: Python/FastAPI（VS1統一）
**アーキテクチャ**: Hexagonal Architecture

---

## ユビキタス言語

### 集約（Aggregates）

#### 1. LacticAcidBacteriaResearch（乳酸菌研究）

乳酸菌株の探索、特性解析、機能性評価の研究。

```
LacticAcidBacteriaResearch {
  research_id: ResearchId                   // 研究ID
  strain: LABStrain                         // 乳酸菌株
  characterization: StrainCharacterization  // 特性解析
  functional_screening: list<FunctionalTest>// 機能性スクリーニング
  safety_assessment: SafetyAssessment       // 安全性評価
  application_potential: ApplicationPotential// 応用可能性
  status: ResearchStatus
  created_at: timestamp
  updated_at: timestamp
}
```

**ビジネスルール**:
- 新規株は16S rRNA解析必須
- 食品利用前に安全性評価完了
- 機能性主張にはエビデンスレベルA以上

#### 2. FunctionalIngredient（機能性成分）

健康機能を持つ成分の探索と検証。

```
FunctionalIngredient {
  ingredient_id: IngredientId               // 成分ID
  compound_info: CompoundInformation        // 化合物情報
  source: IngredientSource                  // 由来
  bioactivity: list<Bioactivity>            // 生理活性
  mechanism: MechanismOfAction              // 作用機序
  efficacy_studies: list<EfficacyStudy>     // 有効性研究
  regulatory_status: RegulatoryStatus       // 規制上のステータス
  status: IngredientStatus
}
```

**ビジネスルール**:
- 作用機序の解明が必須
- 用量反応関係の確立
- 既存成分との相互作用確認

#### 3. HealthClaimEvidence（健康効果実証）

健康効果の科学的実証と申請対応。

```
HealthClaimEvidence {
  evidence_id: EvidenceId                   // エビデンスID
  claim: HealthClaim                        // 健康強調表示
  target_ingredient: IngredientRef          // 対象成分
  evidence_package: EvidencePackage         // エビデンスパッケージ
  clinical_trials: list<ClinicalTrial>      // 臨床試験
  systematic_review: SystematicReview       // システマティックレビュー
  regulatory_submission: RegulatorySubmission// 申請情報
  status: EvidenceStatus
}
```

**ビジネスルール**:
- エビデンスレベルはSR/RCTが最高
- 機能性表示食品申請はガイドライン準拠
- ネガティブデータも記録必須

---

### 値オブジェクト（Value Objects）

```
LABStrain {
  strain_id: string
  species: string                           // 菌種
  subspecies: string
  strain_name: string                       // 株名
  isolation_source: string                  // 分離源
  isolation_date: date
  genbank_accession: string                 // GenBank番号
  deposited_at: string                      // 寄託機関
}

StrainCharacterization {
  morphology: Morphology
  growth_conditions: GrowthConditions
  biochemical_profile: BiochemicalProfile
  genomic_features: GenomicFeatures
  metabolite_profile: MetaboliteProfile
}

FunctionalTest {
  test_id: string
  test_type: string  // IMMUNOMODULATION | GUT_HEALTH | METABOLIC | ORAL_HEALTH | etc
  methodology: string
  results: TestResults
  statistical_significance: StatisticalAnalysis
  conclusion: string
}

CompoundInformation {
  compound_name: string
  iupac_name: string
  molecular_formula: string
  molecular_weight: float
  structure: string                         // SMILES or InChI
  cas_number: string
  classification: string                    // POLYPHENOL | PEPTIDE | FIBER | etc
}

Bioactivity {
  activity_type: string
  target: string                            // 標的分子/経路
  potency: string                           // IC50, EC50 etc
  assay_method: string
  evidence_level: string                    // IN_VITRO | IN_VIVO | HUMAN
}

MechanismOfAction {
  primary_mechanism: string
  molecular_targets: list<string>
  signaling_pathways: list<string>
  supporting_evidence: list<string>
  confidence_level: string
}

HealthClaim {
  claim_type: string  // STRUCTURE_FUNCTION | DISEASE_RISK | HEALTH_MAINTENANCE
  claim_text: string
  target_population: string
  conditions: list<string>
  disclaimers: list<string>
}

ClinicalTrial {
  trial_id: string
  registry_number: string                   // UMIN, ClinicalTrials.gov
  design: TrialDesign                       // RCT, crossover, etc
  participants: ParticipantInfo
  intervention: InterventionDetail
  outcomes: list<OutcomeMeasure>
  results: TrialResults
  publication: PublicationInfo
}

EvidencePackage {
  evidence_level: string  // A | B | C | D
  total_studies: int
  rct_count: int
  meta_analysis_available: boolean
  consistency_rating: string
  overall_strength: string
}
```

---

### ドメインイベント（Domain Events）

```
# 乳酸菌研究イベント
StrainIsolated                   // 新株分離
CharacterizationCompleted        // 特性解析完了
FunctionalActivityDiscovered     // 機能性発見
SafetyAssessmentPassed           // 安全性評価通過
StrainDeposited                  // 寄託完了

# 機能性成分イベント
IngredientIdentified             // 成分同定
BioactivityConfirmed             // 生理活性確認
MechanismElucidated              // 作用機序解明
DoseResponseEstablished          // 用量反応確立

# 健康効果実証イベント
ClinicalTrialRegistered          // 臨床試験登録
ClinicalTrialCompleted           // 臨床試験完了
EvidencePackageAssembled         // エビデンスパッケージ完成
RegulatorySubmitted              // 申請提出
ClaimApproved                    // 表示承認
```

---

### VS間連携イベント（Kafka）

#### 発行イベント

```json
{
  "event_type": "functional_research.ingredient_validated",
  "payload": {
    "ingredient_id": "string",
    "compound_name": "string",
    "validated_claims": ["string"],
    "evidence_level": "A | B | C",
    "recommended_dosage": {
      "amount": "number",
      "unit": "string"
    },
    "validated_at": "timestamp"
  }
}
```

#### 購読イベント

```json
// BC1からの発酵プロセスデータ
{
  "event_type": "fermentation.metabolite_detected",
  "payload": {
    "process_id": "string",
    "metabolite": "string",
    "concentration": "number"
  }
}
```

---

## ドメインサービス

### LABResearchService

```python
class LABResearchService:
    def isolate_strain(source, isolation_conditions) -> LABStrain
    def characterize_strain(strain_id) -> StrainCharacterization
    def screen_functionality(strain_id, test_types) -> list[FunctionalTest]
    def assess_safety(strain_id) -> SafetyAssessment
    def evaluate_application(strain_id, target_products) -> ApplicationPotential
```

### FunctionalIngredientService

```python
class FunctionalIngredientService:
    def identify_compound(sample, analytical_method) -> CompoundInformation
    def evaluate_bioactivity(ingredient_id, assay_panel) -> list[Bioactivity]
    def elucidate_mechanism(ingredient_id, experimental_data) -> MechanismOfAction
    def establish_dose_response(ingredient_id, study_data) -> DoseResponse
```

### HealthClaimService

```python
class HealthClaimService:
    def assemble_evidence_package(ingredient_id, claim) -> EvidencePackage
    def conduct_systematic_review(topic, search_strategy) -> SystematicReview
    def prepare_regulatory_submission(evidence_id, target_regulation) -> RegulatorySubmission
    def track_submission_status(submission_id) -> SubmissionStatus
```

---

## 用語集

| 日本語 | 英語 | 定義 |
|--------|------|------|
| 乳酸菌 | Lactic Acid Bacteria (LAB) | 乳酸を産生する細菌群 |
| 機能性成分 | Functional Ingredient | 健康機能を持つ成分 |
| 生理活性 | Bioactivity | 生体に対する活性作用 |
| 作用機序 | Mechanism of Action | 効果が発現する仕組み |
| エビデンスレベル | Evidence Level | 科学的根拠の強さ |
| 健康強調表示 | Health Claim | 健康効果を示す表示 |
| システマティックレビュー | Systematic Review | 体系的文献レビュー |
