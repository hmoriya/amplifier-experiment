# 価値根拠検証ルール

**作成日**: 2025-12-13  
**バージョン**: V1.0

---

## 概要

価値根拠検証は、設計判断を支える証拠データの品質と信頼性を保証するルール体系です。客観的で検証可能な根拠のみを認め、推測や憶測に基づく判断を排除します。

## 根拠分類体系

### 一次根拠（Primary Evidence）
直接的な観測・測定・実験から得られるデータ

```yaml
primary_evidence_types:
  market_research:
    - customer_surveys
    - user_interviews
    - focus_groups
    - behavioral_analytics
    reliability_score: 4.5-5.0
    
  financial_analysis:
    - revenue_impact_data
    - cost_analysis
    - roi_calculations
    - budget_allocations
    reliability_score: 4.0-5.0
    
  technical_measurements:
    - performance_benchmarks
    - load_testing_results
    - security_assessments
    - code_quality_metrics
    reliability_score: 4.0-5.0
    
  operational_data:
    - process_efficiency_metrics
    - error_rates
    - response_times
    - resource_utilization
    reliability_score: 4.0-4.5
```

### 二次根拠（Secondary Evidence）
他者による研究・分析・報告から得られる情報

```yaml
secondary_evidence_types:
  industry_reports:
    - market_analysis_reports
    - technology_trend_reports
    - competitive_analysis
    - industry_benchmarks
    reliability_score: 3.0-4.0
    
  academic_research:
    - peer_reviewed_papers
    - research_studies
    - case_studies
    - best_practice_guides
    reliability_score: 3.5-4.5
    
  vendor_information:
    - product_specifications
    - vendor_benchmarks
    - white_papers
    - technical_documentation
    reliability_score: 2.5-3.5
    
  expert_opinions:
    - consultant_recommendations
    - expert_interviews
    - advisory_board_input
    - industry_expert_analysis
    reliability_score: 2.0-3.5
```

### 三次根拠（Tertiary Evidence）
一般的な知識・推定・類推に基づく情報

```yaml
tertiary_evidence_types:
  general_knowledge:
    - common_practices
    - general_principles
    - widely_accepted_methods
    reliability_score: 2.0-3.0
    
  analogies:
    - similar_project_outcomes
    - comparable_company_examples
    - historical_precedents
    reliability_score: 1.5-2.5
    
  assumptions:
    - educated_guesses
    - reasonable_extrapolations
    - logical_inferences
    reliability_score: 1.0-2.0
```

---

## 根拠品質評価基準

### 信頼性評価（Reliability Assessment）

#### データ源信頼性

```yaml
source_credibility_matrix:
  tier_1_sources:
    examples: ["政府統計", "上場企業IR", "査読論文", "国際機関レポート"]
    credibility_score: 4.5-5.0
    verification_level: "high"
    
  tier_2_sources:
    examples: ["業界団体調査", "大手コンサル報告", "技術標準機関", "認証機関"]
    credibility_score: 3.5-4.5
    verification_level: "medium"
    
  tier_3_sources:
    examples: ["専門メディア", "業界専門家", "ベンダー資料", "業界イベント"]
    credibility_score: 2.5-3.5
    verification_level: "low"
    
  tier_4_sources:
    examples: ["ブログ記事", "SNS投稿", "匿名情報", "未検証レポート"]
    credibility_score: 1.0-2.5
    verification_level: "minimal"
```

#### 方法論評価

```yaml
methodology_assessment:
  quantitative_research:
    survey_research:
      sample_size: "minimum_statistical_significance"
      sampling_method: "representative_random_sampling"
      response_rate: "> 30% for_acceptable_quality"
      bias_control: "systematic_bias_mitigation"
      score_range: 3.5-5.0
      
    experimental_design:
      control_groups: "proper_control_conditions"
      variable_isolation: "clear_independent_variables"
      measurement_validity: "validated_instruments"
      statistical_analysis: "appropriate_statistical_tests"
      score_range: 4.0-5.0
      
  qualitative_research:
    interview_studies:
      participant_selection: "purposeful_sampling"
      data_saturation: "theoretical_saturation_reached"
      coding_reliability: "inter_coder_agreement"
      triangulation: "multiple_data_sources"
      score_range: 3.0-4.0
      
    case_studies:
      case_selection: "strategic_case_selection"
      data_collection: "multiple_evidence_sources"
      analysis_rigor: "systematic_analysis_framework"
      generalizability: "analytic_generalization"
      score_range: 2.5-3.5
```

### 新鮮度評価（Freshness Assessment）

```yaml
data_freshness_scoring:
  market_data:
    within_3months: 5.0
    within_6months: 4.5
    within_1year: 4.0
    within_2years: 3.0
    within_3years: 2.0
    older: 1.0
    
  technology_data:
    within_1month: 5.0
    within_3months: 4.5
    within_6months: 4.0
    within_1year: 3.0
    within_18months: 2.0
    older: 1.0
    
  financial_data:
    within_1month: 5.0
    within_1quarter: 4.5
    within_1year: 4.0
    within_2years: 3.0
    within_3years: 2.0
    older: 1.0
    
  operational_data:
    real_time: 5.0
    within_1week: 4.5
    within_1month: 4.0
    within_1quarter: 3.0
    within_6months: 2.0
    older: 1.0
```

### 完全性評価（Completeness Assessment）

```yaml
completeness_criteria:
  coverage_dimensions:
    stakeholder_coverage:
      all_key_stakeholders: 5.0
      majority_stakeholders: 4.0
      some_stakeholders: 3.0
      limited_stakeholders: 2.0
      minimal_stakeholders: 1.0
      
    functional_coverage:
      all_key_functions: 5.0
      majority_functions: 4.0
      core_functions: 3.0
      limited_functions: 2.0
      minimal_functions: 1.0
      
    temporal_coverage:
      comprehensive_timeframe: 5.0
      adequate_timeframe: 4.0
      basic_timeframe: 3.0
      limited_timeframe: 2.0
      minimal_timeframe: 1.0
      
  data_completeness:
    required_fields:
      all_present: 5.0
      mostly_present: 4.0
      adequately_present: 3.0
      partially_present: 2.0
      minimally_present: 1.0
      
    supporting_context:
      rich_context: 5.0
      adequate_context: 4.0
      basic_context: 3.0
      limited_context: 2.0
      minimal_context: 1.0
```

---

## 根拠検証プロセス

### ステップ1：根拠収集検証

```yaml
evidence_collection_validation:
  source_verification:
    - verify_source_authenticity
    - check_source_credentials
    - validate_publication_details
    - confirm_access_permissions
    
  content_extraction:
    - extract_relevant_data_points
    - identify_key_findings
    - capture_methodology_details
    - document_limitations
    
  metadata_capture:
    - record_collection_timestamp
    - document_extraction_method
    - note_any_transformations
    - track_verification_status
```

### ステップ2：品質評価

```yaml
quality_evaluation_process:
  automated_checks:
    format_validation:
      - data_type_consistency
      - required_field_presence
      - value_range_validation
      - format_compliance
      
    freshness_assessment:
      - publication_date_check
      - data_collection_date_verification
      - update_frequency_analysis
      - obsolescence_evaluation
      
    completeness_analysis:
      - coverage_gap_identification
      - missing_data_assessment
      - consistency_verification
      - cross_reference_validation
      
  manual_review:
    credibility_assessment:
      - source_reputation_check
      - methodology_review
      - bias_assessment
      - conflict_of_interest_check
      
    relevance_evaluation:
      - context_appropriateness
      - scope_alignment
      - applicability_assessment
      - generalizability_review
```

### ステップ3：総合評価

```yaml
composite_scoring:
  quality_dimensions:
    reliability: 
      weight: 0.40
      components: [source_credibility, methodology_quality]
      
    freshness:
      weight: 0.25
      components: [data_recency, update_frequency]
      
    completeness:
      weight: 0.25
      components: [coverage_breadth, data_completeness]
      
    relevance:
      weight: 0.10
      components: [context_fit, applicability]
      
  calculation_formula: |
    evidence_score = (
      reliability_score * 0.40 +
      freshness_score * 0.25 +
      completeness_score * 0.25 +
      relevance_score * 0.10
    )
```

---

## 自動検証アルゴリズム

### パターン認識による品質評価

```yaml
pattern_recognition:
  high_quality_patterns:
    quantitative_data_present:
      - numerical_measurements
      - statistical_analysis
      - confidence_intervals
      - sample_size_reporting
      
    methodology_transparency:
      - clear_method_description
      - reproducible_procedures
      - limitation_acknowledgment
      - bias_mitigation_measures
      
    multiple_source_confirmation:
      - independent_verification
      - triangulation_evidence
      - consensus_findings
      - peer_review_validation
      
  low_quality_patterns:
    speculation_indicators:
      - hypothetical_language
      - uncertain_qualifiers
      - assumption_statements
      - prediction_without_basis
      
    bias_indicators:
      - single_source_dependence
      - conflict_of_interest
      - selective_data_presentation
      - cherry_picking_evidence
      
    outdated_information:
      - obsolete_technology_references
      - superseded_standards
      - historical_data_misuse
      - deprecated_practices
```

### 機械学習による品質予測

```yaml
ml_quality_assessment:
  feature_extraction:
    text_features:
      - vocabulary_sophistication
      - technical_terminology_density
      - citation_frequency
      - quantitative_content_ratio
      
    structural_features:
      - document_organization
      - section_completeness
      - reference_quality
      - methodology_section_presence
      
    meta_features:
      - author_credentials
      - publication_venue_quality
      - citation_count
      - peer_review_status
      
  quality_prediction_model:
    algorithm: "ensemble_random_forest"
    training_data: "expert_annotated_evidence_corpus"
    validation_method: "k_fold_cross_validation"
    accuracy_target: "> 80%"
    
  continuous_improvement:
    feedback_integration: "human_expert_corrections"
    model_retraining: "monthly_updates"
    performance_monitoring: "continuous_accuracy_tracking"
```

---

## 品質しきい値と判定基準

### 根拠品質レベル

```yaml
quality_levels:
  excellent:
    score_range: "4.5 - 5.0"
    description: "最高品質の根拠"
    characteristics:
      - multiple_high_credibility_sources
      - rigorous_methodology
      - recent_data
      - comprehensive_coverage
      
  good:
    score_range: "3.5 - 4.4"
    description: "高品質の根拠"
    characteristics:
      - credible_sources
      - sound_methodology
      - reasonably_recent_data
      - adequate_coverage
      
  acceptable:
    score_range: "2.5 - 3.4"
    description: "最低限受入可能な根拠"
    characteristics:
      - some_credible_sources
      - basic_methodology
      - somewhat_dated_data
      - partial_coverage
      
  poor:
    score_range: "1.5 - 2.4"
    description: "品質不十分な根拠"
    characteristics:
      - low_credibility_sources
      - weak_methodology
      - outdated_data
      - limited_coverage
      
  unacceptable:
    score_range: "1.0 - 1.4"
    description: "受入不可能な根拠"
    characteristics:
      - unreliable_sources
      - flawed_methodology
      - obsolete_data
      - inadequate_coverage
```

### 最低品質要件

```yaml
minimum_quality_requirements:
  critical_decisions:
    minimum_score: 4.0
    required_sources: 3
    maximum_age: "6_months"
    methodology_requirement: "rigorous"
    
  standard_decisions:
    minimum_score: 3.5
    required_sources: 2
    maximum_age: "1_year"
    methodology_requirement: "sound"
    
  routine_decisions:
    minimum_score: 3.0
    required_sources: 1
    maximum_age: "18_months"
    methodology_requirement: "basic"
```

---

## エラーパターンと対処法

### 一般的な根拠品質問題

```yaml
common_quality_issues:
  insufficient_evidence:
    symptoms:
      - single_source_dependence
      - limited_data_points
      - narrow_perspective
      
    solutions:
      - require_multiple_sources
      - expand_data_collection
      - seek_diverse_perspectives
      
  outdated_information:
    symptoms:
      - obsolete_technology_data
      - historical_market_conditions
      - superseded_standards
      
    solutions:
      - update_data_sources
      - verify_current_relevance
      - supplement_with_recent_data
      
  biased_sources:
    symptoms:
      - vendor_only_information
      - conflict_of_interest
      - selective_data_presentation
      
    solutions:
      - seek_independent_sources
      - disclose_potential_bias
      - balance_opposing_viewpoints
      
  weak_methodology:
    symptoms:
      - unclear_data_collection
      - inadequate_sample_size
      - poor_experimental_design
      
    solutions:
      - require_methodology_disclosure
      - validate_research_design
      - supplement_with_rigorous_studies
```

### 自動修正アクション

```yaml
auto_correction_actions:
  quality_enhancement:
    low_score_triggers:
      - suggest_additional_sources
      - recommend_methodology_improvements
      - provide_quality_guidelines
      
    freshness_issues:
      - flag_outdated_data
      - suggest_current_alternatives
      - recommend_update_schedule
      
    completeness_gaps:
      - identify_missing_dimensions
      - suggest_coverage_improvements
      - recommend_additional_research
      
  validation_support:
    source_verification:
      - provide_credibility_assessment
      - suggest_verification_methods
      - recommend_cross_validation
      
    methodology_review:
      - provide_quality_checklists
      - suggest_improvement_approaches
      - recommend_expert_consultation
```

---

## 実装ガイドライン

### システム統合

```yaml
integration_specifications:
  trace_system_integration:
    - evidence_automatic_capture
    - quality_real_time_assessment
    - score_continuous_updating
    
  necessity_judge_integration:
    - evidence_quality_feeding
    - decision_support_provision
    - validation_result_incorporation
    
  gate_system_integration:
    - quality_threshold_enforcement
    - evidence_completeness_checking
    - approval_gate_conditioning
```

### パフォーマンス要件

```yaml
performance_requirements:
  evaluation_speed:
    real_time_assessment: "< 2 seconds"
    batch_processing: "< 30 seconds per item"
    large_dataset_processing: "< 5 minutes for 1000 items"
    
  accuracy_targets:
    quality_prediction: "> 85% accuracy"
    freshness_assessment: "> 95% accuracy"
    completeness_evaluation: "> 80% accuracy"
    
  scalability:
    concurrent_evaluations: "> 100 simultaneous"
    data_volume: "> 10GB evidence database"
    user_capacity: "> 1000 users"
```

---

この価値根拠検証ルールにより、Parasolシステムは高品質で信頼性の高い根拠に基づく意思決定を保証し、推測や憶測による判断を技術的に排除します。