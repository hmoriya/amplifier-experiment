# 構造的必然性検証ルール

**作成日**: 2025-12-13  
**バージョン**: V1.0

---

## 概要

構造的必然性検証は、すべての設計判断が「想像ではない」ことを技術的に保証するためのルール体系です。4つの基準による厳格な評価により、価値に基づかない判断を自動的にブロックします。

## 4つの検証基準

### 基準1：価値起源の明確性 (Value Origin Clarity)

#### 検証目的
設計判断が明確に定義された価値（VL3）から直接導出されていることを確認する。

#### 検証項目

**必須要件**:
- [ ] VL3価値が具体的に特定されている
- [ ] VL3→VL2→VL1のチェーンが完全に追跡可能
- [ ] 価値階層の論理的整合性が確認されている
- [ ] 判断と価値の直接的関連が説明されている

**評価基準**:

| スコア | 状態 | 条件 | 具体例 |
|--------|------|------|--------|
| 5.0 | 優秀 | VL3価値が明確、チェーン完全、論理完璧 | "VL3「発酵技術による味の革新」から発酵研究ケイパビリティを導出" |
| 4.0 | 良好 | VL3価値特定済み、上位関係明確、論理一貫 | "VL3明確だがVL2との関係に軽微な曖昧さあり" |
| 3.0 | 合格 | VL3価値大まかに特定、関係推測可能、基本論理あり | "価値関係は理解できるが具体性に欠ける" |
| 2.0 | 警告 | 価値言及あるが曖昧、関係不明確、論理飛躍 | "「品質向上のため」程度の抽象的理由" |
| 1.0 | 不合格 | 価値言及なし、技術理由のみ、想像ベース | "使いやすそうだから"、"最新技術だから" |

**NG パターン検出**:
```
警告パターン:
- "〜と思われる"
- "〜のはず"  
- "一般的に〜"
- "エキスパートによると"
- "ベストプラクティスでは"

ブロックパターン:
- "使いやすいから"
- "きれいだから"
- "最新だから"
- "他社もやっているから"
```

#### 自動検証アルゴリズム

```yaml
value_origin_validation:
  step1_vl3_identification:
    - extract_value_references
    - validate_vl3_specificity
    - check_hierarchy_position
    
  step2_chain_verification:
    - trace_vl3_to_vl2
    - trace_vl2_to_vl1
    - verify_logical_progression
    
  step3_relationship_analysis:
    - analyze_decision_value_connection
    - measure_directness_of_derivation
    - assess_logical_consistency
    
  step4_scoring:
    - calculate_weighted_score
    - apply_penalty_for_gaps
    - determine_final_rating
```

---

### 基準2：因果関係の証明 (Causal Relationship Proof)

#### 検証目的
設計判断と価値実現の因果関係が客観的に証明されていることを確認する。

#### 検証項目

**必須要件**:
- [ ] 定量的な因果関係の証明がある
- [ ] 複数の独立したデータソースによる裏付け
- [ ] 測定可能なKPIが設定されている
- [ ] ベースラインとターゲットが明示されている

**評価基準**:

| スコア | 状態 | 条件 | 必要な証拠 |
|--------|------|------|-----------|
| 5.0 | 優秀 | 定量的証明、複数ソース、統計的有意性 | 相関係数、実験データ、統計検定 |
| 4.0 | 良好 | 論理的説明、データ裏付け、測定方法明確 | 論理モデル、定量データ、測定計画 |
| 3.0 | 合格 | 基本的論理関係、一定の根拠、理論説明 | 仮説モデル、部分データ、理論的根拠 |
| 2.0 | 警告 | 推測レベル、限定的根拠、論理に穴 | "効果があるはず"、"他社成功例" |
| 1.0 | 不合格 | 因果関係不明、根拠なし、想像ベース | "きっと良くなる"、"感覚的にわかる" |

**証拠品質評価**:
```yaml
evidence_quality_criteria:
  data_sources:
    primary_data: 5.0      # 直接測定データ
    secondary_data: 4.0    # 公開統計・研究
    expert_opinion: 3.0    # 専門家意見
    anecdotal: 2.0         # 事例報告
    speculation: 1.0       # 推測・憶測
    
  recency:
    within_6months: 5.0
    within_1year: 4.0
    within_2years: 3.0
    within_5years: 2.0
    older: 1.0
    
  sample_size:
    large_n: 5.0          # n > 1000
    medium_n: 4.0         # n = 100-1000  
    small_n: 3.0          # n = 30-100
    very_small_n: 2.0     # n = 10-30
    insufficient_n: 1.0   # n < 10
```

#### 自動検証アルゴリズム

```yaml
causal_proof_validation:
  step1_evidence_collection:
    - identify_supporting_evidence
    - classify_evidence_types
    - assess_source_credibility
    
  step2_causality_analysis:
    - examine_logical_connections
    - check_temporal_relationships
    - validate_mechanism_explanation
    
  step3_quantitative_assessment:
    - measure_correlation_strength
    - assess_statistical_significance
    - evaluate_effect_size
    
  step4_quality_scoring:
    - weight_evidence_by_quality
    - aggregate_multiple_sources
    - apply_confidence_intervals
```

---

### 基準3：代替案の検討 (Alternative Analysis)

#### 検証目的
複数の選択肢が適切に比較検討され、最適解が選択されていることを確認する。

#### 検証項目

**必須要件**:
- [ ] 3つ以上の代替案が特定されている
- [ ] 系統的な比較分析が実施されている
- [ ] 評価基準マトリクスが使用されている
- [ ] 選択理由が明確に説明されている

**評価基準**:

| スコア | 状態 | 代替案数 | 分析方法 | 成果物 |
|--------|------|----------|----------|--------|
| 5.0 | 優秀 | 5つ以上 | 系統的比較、意思決定マトリクス | 比較表、評価マトリクス、リスク分析 |
| 4.0 | 良好 | 3-4つ | 構造化比較、明確な選択理由 | 代替案リスト、比較項目、選択根拠 |
| 3.0 | 合格 | 2-3つ | 基本的評価、選択理由あり | 主要代替案、簡易比較、理由説明 |
| 2.0 | 警告 | 1-2つ | 限定的検討、表面的比較 | "他に良い方法がない"、"時間がない" |
| 1.0 | 不合格 | 検討なし | 思いつき選択、理由なし | "これしか思いつかない"、"いつもの方法" |

**比較分析フレームワーク**:
```yaml
alternative_analysis_framework:
  identification_methods:
    - brainstorming_sessions
    - best_practice_research
    - competitive_analysis
    - expert_consultation
    
  evaluation_criteria:
    business_value:
      - roi_potential
      - time_to_value
      - strategic_alignment
      
    technical_feasibility:
      - implementation_complexity
      - resource_requirements
      - risk_factors
      
    operational_impact:
      - maintenance_burden
      - scalability
      - integration_complexity
      
  decision_matrix:
    criteria_weighting: "stakeholder_defined"
    scoring_method: "1_to_5_scale"
    aggregation: "weighted_average"
    sensitivity_analysis: "required"
```

#### 自動検証アルゴリズム

```yaml
alternative_analysis_validation:
  step1_option_identification:
    - count_identified_alternatives
    - assess_option_diversity
    - check_completeness_of_coverage
    
  step2_comparison_quality:
    - validate_evaluation_criteria
    - check_scoring_consistency
    - assess_analysis_depth
    
  step3_decision_rationale:
    - examine_selection_logic
    - verify_trade_off_consideration
    - validate_risk_assessment
    
  step4_documentation_completeness:
    - check_required_artifacts
    - assess_explanation_clarity
    - verify_stakeholder_approval
```

---

### 基準4：測定可能性 (Measurability)

#### 検証目的
設計判断の効果が客観的に測定可能であることを確認する。

#### 検証項目

**必須要件**:
- [ ] SMART目標が設定されている
- [ ] 具体的KPIが定義されている
- [ ] 測定方法が確立されている
- [ ] ベースラインデータが取得されている

**SMART目標検証**:
```yaml
smart_criteria:
  Specific (具体的):
    - clear_objective_definition
    - unambiguous_scope
    - precise_target_setting
    
  Measurable (測定可能):
    - quantitative_metrics
    - qualitative_indicators
    - measurement_methods
    
  Achievable (達成可能):
    - realistic_targets
    - resource_availability
    - capability_assessment
    
  Relevant (関連性):
    - business_value_alignment
    - strategic_importance
    - stakeholder_relevance
    
  Time-bound (期限):
    - clear_deadlines
    - milestone_schedule
    - progress_checkpoints
```

**評価基準**:

| スコア | 状態 | KPI設定 | 測定方法 | ベースライン |
|--------|------|---------|----------|-------------|
| 5.0 | 優秀 | SMART目標完備、複数KPI | 自動測定可能 | 取得済み、履歴あり |
| 4.0 | 良好 | KPI明確、測定計画あり | 手動測定可能 | 取得済み |
| 3.0 | 合格 | KPI候補、測定方向性明確 | 測定方法案 | 取得計画あり |
| 2.0 | 警告 | 抽象的指標、方法不明 | "効果は測れるはず" | 計画なし |
| 1.0 | 不合格 | 測定計画なし、主観のみ | "感覚的にわかる" | 測定不可 |

#### 自動検証アルゴリズム

```yaml
measurability_validation:
  step1_kpi_assessment:
    - validate_smart_criteria
    - check_kpi_specificity
    - assess_measurement_feasibility
    
  step2_baseline_verification:
    - confirm_baseline_availability
    - check_data_quality
    - assess_historical_context
    
  step3_measurement_plan:
    - validate_measurement_methods
    - check_tool_availability
    - assess_resource_requirements
    
  step4_target_validation:
    - verify_target_realism
    - check_timeline_feasibility
    - assess_risk_factors
```

---

## 総合評価アルゴリズム

### スコア計算

```yaml
necessity_score_calculation:
  formula: |
    total_score = (
      value_origin_score * 0.30 +
      causal_proof_score * 0.30 +
      alternatives_score * 0.20 +
      measurability_score * 0.20
    )
    
  weighting_rationale:
    value_origin: 0.30      # 最重要：価値との直接的関連
    causal_proof: 0.30      # 最重要：客観的根拠の存在
    alternatives: 0.20      # 重要：選択の妥当性
    measurability: 0.20     # 重要：効果検証の可能性
    
  scoring_scale:
    range: "1.0 - 5.0"
    precision: "0.1"
    threshold_pass: 3.5
    threshold_warning: 3.0
    threshold_fail: 2.5
```

### 最終判定

```yaml
final_judgment:
  pass_conditions:
    - total_score: ">= 3.5"
    - all_criteria: ">= 3.0"
    - no_blocking_patterns: true
    
  warning_conditions:
    - total_score: "3.0 - 3.4"
    - some_criteria: "< 3.0"
    - minor_imagination_patterns: present
    
  fail_conditions:
    - total_score: "< 3.0"
    - any_criteria: "< 2.0"
    - blocking_patterns: detected
    
  actions:
    pass: "承認・記録"
    warning: "改善提案付き承認"
    fail: "ブロック・修正要求"
```

---

## 実装ガイドライン

### 自動検証の実装

```yaml
implementation_steps:
  1_data_extraction:
    - parse_decision_context
    - extract_value_references
    - identify_evidence_sources
    
  2_criterion_evaluation:
    - run_parallel_validations
    - collect_evaluation_results
    - calculate_individual_scores
    
  3_aggregation:
    - apply_weighting_formula
    - calculate_composite_score
    - determine_final_judgment
    
  4_reporting:
    - generate_detailed_report
    - provide_improvement_suggestions
    - record_evaluation_history
```

### 品質保証

```yaml
quality_assurance:
  validation_accuracy:
    target: "> 85%"
    measurement: "human_expert_comparison"
    
  false_positive_rate:
    target: "< 10%"
    mitigation: "conservative_thresholds"
    
  false_negative_rate:
    target: "< 5%"
    mitigation: "multiple_detection_methods"
    
  continuous_improvement:
    feedback_collection: "systematic"
    model_refinement: "quarterly"
    threshold_adjustment: "data_driven"
```

---

この構造的必然性検証ルールにより、Parasolシステムは「想像の設計を技術的に不可能にする」という目標を達成し、すべての設計判断が観測可能な価値に基づくことを保証します。