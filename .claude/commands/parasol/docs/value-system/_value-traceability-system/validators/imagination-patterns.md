# 想像の設計パターン検出

**作成日**: 2025-12-13  
**バージョン**: V1.0

---

## 概要

想像の設計パターン検出は、価値に基づかない主観的・推測的な判断を自動識別し、技術的にブロックするシステムです。長年のソフトウェア開発で蓄積された「想像の設計」の典型的パターンを体系化し、機械学習により検出精度を向上させます。

## 想像の設計の定義

### 基本概念

**想像の設計 (Imaginary Design)**:
- 観測可能な価値や根拠に基づかない設計判断
- 主観的嗜好や推測に基づく技術選択
- 「きっと〜だろう」「〜のはず」という仮定ベースの判断
- 具体的な測定や検証なしに行われる決定

### Parasolが排除する理由

```yaml
elimination_rationale:
  business_impact:
    - 価値実現の阻害
    - 投資対効果の悪化
    - プロジェクト失敗リスク増加
    
  technical_debt:
    - 不適切なアーキテクチャ選択
    - 保守困難なシステム構築
    - 技術的負債の蓄積
    
  organizational_cost:
    - 開発リソースの浪費
    - ステークホルダー信頼失墜
    - 競争優位性の喪失
```

---

## パターン分類体系

### カテゴリ1：仮定ベース設計 (Assumption-Based Design)

#### 特徴
根拠なき仮定や推測に基づく判断パターン

#### 検出キーワード
```yaml
assumption_keywords:
  certainty_qualifiers:
    - "〜と思われる"
    - "〜のはず"
    - "〜に違いない"
    - "きっと〜だろう"
    - "おそらく〜"
    - "〜と考えられる"
    
  generalization_patterns:
    - "一般的に〜"
    - "普通は〜"
    - "通常〜"
    - "たいてい〜"
    - "多くの場合〜"
    
  speculation_phrases:
    - "〜かもしれない"
    - "〜の可能性がある"
    - "〜と予想される"
    - "〜になりそう"
```

#### 具体例と検出パターン
```yaml
assumption_examples:
  technical_assumptions:
    bad: "マイクロサービス化すればスケーラビリティが向上するはず"
    pattern: "技術選択 + 推測的効果"
    detection: "技術用語 + 「はず」「だろう」"
    
  user_assumptions:
    bad: "ユーザーは直感的に使えると思う"
    pattern: "ユーザー行動の推測"
    detection: "ユーザー言及 + 推測表現"
    
  business_assumptions:
    bad: "競合他社より優位に立てるに違いない"
    pattern: "競争優位性の断定"
    detection: "競合比較 + 確信表現"
```

#### 重要度・ブロックレベル
```yaml
assumption_severity:
  critical_block:
    - アーキテクチャ選択の仮定
    - 投資判断の推測
    - セキュリティの前提
    
  warning:
    - UI/UX設計の推測
    - 運用手順の仮定
    - パフォーマンス予測
```

---

### カテゴリ2：権威依存設計 (Authority-Based Design)

#### 特徴
権威や専門家の意見に盲従する判断パターン

#### 検出キーワード
```yaml
authority_keywords:
  expert_references:
    - "エキスパートが言った"
    - "専門家によると"
    - "有識者の意見では"
    - "業界の権威が推奨"
    
  consulting_references:
    - "コンサルが提案した"
    - "アドバイザーが推奨"
    - "ベンダーが勧めた"
    
  institutional_authority:
    - "有名企業の事例"
    - "大手が採用している"
    - "業界リーダーが使用"
    - "標準的なアプローチ"
```

#### 検出アルゴリズム
```yaml
authority_detection:
  pattern_analysis:
    - authority_mention_without_reasoning
    - lack_of_independent_validation
    - absence_of_contextual_analysis
    - missing_alternative_consideration
    
  context_evaluation:
    - check_authority_relevance
    - validate_expertise_domain
    - assess_conflict_of_interest
    - verify_context_applicability
    
  evidence_gap_identification:
    - insufficient_independent_research
    - lack_of_pilot_validation
    - missing_risk_assessment
    - absent_customization_analysis
```

#### 重要度・ブロックレベル
```yaml
authority_severity:
  high_risk:
    - 技術スタック選択の権威依存
    - セキュリティ方針の外部依存
    - アーキテクチャパターンの盲従
    
  medium_risk:
    - 開発手法の権威採用
    - ツール選択の専門家依存
    - プロセス設計の外部指導
```

---

### カテゴリ3：流行追従設計 (Trend-Following Design)

#### 特徴
技術的流行やバズワードに基づく判断パターン

#### 検出キーワード
```yaml
trend_keywords:
  technology_trends:
    - "最新だから"
    - "モダンな技術"
    - "次世代の〜"
    - "トレンドの〜"
    - "話題の〜"
    
  bandwagon_phrases:
    - "みんな使っている"
    - "他社もやっている"
    - "業界標準になった"
    - "デファクトスタンダード"
    
  hype_indicators:
    - "革新的な〜"
    - "画期的な〜"
    - "次世代〜"
    - "未来の〜"
```

#### バズワード検出
```yaml
buzzword_detection:
  technology_buzzwords:
    current_hype:
      - "AI駆動", "機械学習ベース", "クラウドネイティブ"
      - "マイクロサービス", "サーバーレス", "コンテナ化"
      - "DevOps", "アジャイル", "DX推進"
      
    detection_method:
      - buzzword_density_analysis
      - context_appropriateness_check
      - business_justification_verification
      
  marketing_language:
    red_flags:
      - "シームレス", "革新的", "次世代"
      - "ゲームチェンジャー", "パラダイムシフト"
      - "圧倒的", "究極の", "完璧な"
```

#### 重要度・ブロックレベル
```yaml
trend_severity:
  critical_block:
    - 技術選択理由が流行のみ
    - バズワードによるアーキテクチャ決定
    - マーケティング用語での正当化
    
  warning:
    - 最新技術の無批判採用
    - 業界動向への過度の追従
    - 差別化目的の新技術採用
```

---

### カテゴリ4：個人的嗜好設計 (Personal Preference Design)

#### 特徴
客観的根拠なしの個人的好みに基づく判断パターン

#### 検出キーワード
```yaml
preference_keywords:
  aesthetic_preferences:
    - "きれいだから"
    - "美しいUI"
    - "見た目が良い"
    - "デザインが素敵"
    
  subjective_usability:
    - "使いやすいから"
    - "直感的だから"
    - "操作しやすい"
    - "わかりやすい"
    
  personal_comfort:
    - "馴染みがある"
    - "慣れているから"
    - "気に入っている"
    - "好みに合う"
```

#### 客観性欠如の検出
```yaml
objectivity_gap_detection:
  missing_criteria:
    - absence_of_usability_metrics
    - lack_of_user_research
    - missing_accessibility_standards
    - no_performance_benchmarks
    
  subjective_language:
    - emotional_descriptors
    - personal_opinion_markers
    - aesthetic_only_justification
    - comfort_based_reasoning
    
  validation_gaps:
    - no_user_testing
    - no_comparative_analysis
    - no_measurable_criteria
    - no_success_metrics
```

---

### カテゴリ5：慣性思考設計 (Inertial Thinking Design)

#### 特徴
思考停止による既存手法への依存パターン

#### 検出キーワード
```yaml
inertial_keywords:
  thought_stopping:
    - "いつものやり方"
    - "これまでと同じ"
    - "従来通り"
    - "いつものように"
    
  effort_avoidance:
    - "とりあえず"
    - "手っ取り早く"
    - "簡単だから"
    - "時間がないので"
    
  exploration_avoidance:
    - "これしか思いつかない"
    - "他に方法がない"
    - "選択肢がない"
    - "仕方ない"
```

#### 思考停止の検出
```yaml
cognitive_laziness_detection:
  analysis_shortcuts:
    - skip_requirement_analysis
    - avoid_alternative_exploration
    - minimal_research_effort
    - copy_paste_solutions
    
  justification_weakness:
    - circular_reasoning
    - tautological_explanations
    - default_option_bias
    - status_quo_preference
```

---

## 高度検出アルゴリズム

### 自然言語処理による検出

```yaml
nlp_detection_pipeline:
  text_preprocessing:
    - tokenization
    - part_of_speech_tagging
    - named_entity_recognition
    - dependency_parsing
    
  pattern_matching:
    - keyword_pattern_detection
    - phrase_structure_analysis
    - semantic_role_labeling
    - sentiment_analysis
    
  contextual_analysis:
    - discourse_coherence_check
    - argumentation_structure_analysis
    - evidence_claim_relationship
    - logical_fallacy_detection
```

### 機械学習ベース検出

```yaml
ml_detection_system:
  feature_engineering:
    linguistic_features:
      - certainty_markers
      - hedging_language
      - authority_references
      - evidence_indicators
      
    structural_features:
      - argument_complexity
      - reasoning_depth
      - alternative_consideration
      - evidence_diversity
      
  classification_models:
    primary_classifier:
      algorithm: "transformer_based_bert"
      training_data: "annotated_design_decisions"
      accuracy_target: "> 90%"
      
    ensemble_approach:
      - rule_based_classifier
      - svm_classifier  
      - neural_network_classifier
      - voting_ensemble
      
  continuous_learning:
    active_learning: "uncertainty_sampling"
    feedback_integration: "expert_corrections"
    model_updates: "weekly_retraining"
```

### 論理構造解析

```yaml
logical_analysis:
  argument_structure:
    premise_identification: "extract_supporting_claims"
    conclusion_detection: "identify_main_decision"
    logical_connection: "trace_reasoning_chain"
    
  fallacy_detection:
    common_fallacies:
      - circular_reasoning
      - false_dichotomy
      - appeal_to_authority
      - bandwagon_fallacy
      - correlation_causation
      
  evidence_analysis:
    evidence_presence: "check_supporting_data"
    evidence_quality: "assess_source_reliability"
    evidence_relevance: "validate_context_match"
    evidence_sufficiency: "evaluate_coverage"
```

---

## 検出精度向上メカニズム

### 文脈考慮アルゴリズム

```yaml
contextual_refinement:
  domain_adaptation:
    technical_context: "adjust_for_technical_decisions"
    business_context: "adapt_for_business_decisions"
    operational_context: "modify_for_process_decisions"
    
  stakeholder_consideration:
    decision_level: "adjust_for_decision_authority"
    expertise_level: "consider_decision_maker_background"
    responsibility_scope: "account_for_decision_impact"
    
  project_phase_awareness:
    early_phase: "allow_more_speculation"
    design_phase: "require_more_rigor"
    implementation_phase: "enforce_strict_standards"
```

### 偽陽性・偽陰性の最小化

```yaml
accuracy_optimization:
  false_positive_reduction:
    legitimate_uncertainty:
      - appropriate_risk_acknowledgment
      - honest_limitation_disclosure
      - reasonable_assumption_stating
      
    contextual_appropriateness:
      - early_stage_exploration
      - brainstorming_sessions
      - hypothesis_formation
      
  false_negative_prevention:
    subtle_imagination_patterns:
      - sophisticated_rationalization
      - pseudo_scientific_justification
      - complex_circular_reasoning
      
    detection_enhancement:
      - multi_level_analysis
      - cross_reference_validation
      - longitudinal_consistency_check
```

---

## 実時間検出・ブロックシステム

### Phase実行中の監視

```yaml
real_time_monitoring:
  input_analysis:
    user_input_screening:
      - immediate_keyword_detection
      - pattern_recognition
      - confidence_scoring
      
    context_enrichment:
      - historical_decision_analysis
      - project_phase_consideration
      - stakeholder_role_accounting
      
  intervention_triggers:
    immediate_block:
      - high_confidence_imagination_detection
      - critical_decision_points
      - investment_related_decisions
      
    warning_issuance:
      - medium_confidence_detection
      - routine_decisions
      - clarification_opportunities
```

### ユーザー教育・ガイダンス

```yaml
user_guidance_system:
  detection_feedback:
    explanation_provision:
      - pattern_identification_explanation
      - risk_illustration
      - improvement_suggestions
      
    educational_content:
      - imagination_pattern_examples
      - value_based_reasoning_guidance
      - evidence_collection_methods
      
  improvement_support:
    alternative_approaches:
      - suggest_evidence_gathering
      - recommend_validation_methods
      - provide_analysis_frameworks
      
    skill_development:
      - reasoning_quality_training
      - evidence_evaluation_skills
      - decision_making_frameworks
```

---

## パフォーマンス・品質指標

### 検出性能メトリクス

```yaml
detection_metrics:
  accuracy_measures:
    overall_accuracy: "> 90%"
    precision: "> 85%"
    recall: "> 88%"
    f1_score: "> 86%"
    
  response_time:
    real_time_detection: "< 500ms"
    batch_analysis: "< 5s per document"
    complex_analysis: "< 30s per decision"
    
  reliability_measures:
    consistency: "> 95%"
    stability: "> 98%"
    availability: "> 99.9%"
```

### 継続改善プロセス

```yaml
continuous_improvement:
  performance_monitoring:
    accuracy_tracking: "continuous"
    error_analysis: "weekly"
    pattern_evolution: "monthly"
    
  model_enhancement:
    new_pattern_integration: "as_discovered"
    algorithm_optimization: "quarterly"
    training_data_expansion: "monthly"
    
  user_feedback_integration:
    false_positive_correction: "immediate"
    missed_pattern_addition: "weekly_batch"
    accuracy_validation: "monthly_expert_review"
```

---

この想像の設計パターン検出システムにより、Parasolは「想像の設計を技術的に不可能にする」という目標を達成し、すべての設計判断が観測可能な価値と客観的根拠に基づくことを保証します。