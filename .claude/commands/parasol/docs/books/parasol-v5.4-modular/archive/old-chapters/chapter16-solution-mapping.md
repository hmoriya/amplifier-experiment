# 第16章　ソリューション空間へのマッピング ― 橋を架ける

## はじめに：二つの世界をつなぐ

古代ローマの建築家は、理想の設計図と現実の地形の間に橋を架ける名人でした。同様に、現代のシステム設計者は、ビジネスの問題空間（WHAT）と技術の解決空間（HOW）の間に、確実な橋を架ける必要があります。

本章では、価値ストリーム、ケイパビリティ、制約で構成される問題空間を、具体的な技術ソリューションへとマッピングする体系的な方法を解説します。

## マッピングの基本原理

### 問題空間と解決空間の対応関係

```typescript
export interface ProblemSolutionMapping {
  // 問題空間の要素
  problemSpace: {
    valueStreams: ValueStream[];
    capabilities: BusinessCapability[];
    constraints: Constraint[];
    requirements: Requirement[];
  };
  
  // 解決空間の要素
  solutionSpace: {
    architecture: ArchitectureDesign;
    components: SolutionComponent[];
    technologies: Technology[];
    patterns: DesignPattern[];
  };
  
  // マッピング関係
  mappings: {
    capabilityToComponent: Map<string, string[]>;
    requirementToFeature: Map<string, string[]>;
    constraintToDecision: Map<string, DesignDecision>;
    valueToMetric: Map<string, Metric[]>;
  };
  
  // トレーサビリティ
  traceability: {
    forward: Map<string, string[]>;  // 問題→解決
    backward: Map<string, string[]>; // 解決→問題
    coverage: CoverageMetrics;
  };
}
```

### マッピングの品質基準

```typescript
export class MappingQualityAssessor {
  assessMappingQuality(
    mapping: ProblemSolutionMapping
  ): QualityAssessment {
    const criteria = {
      completeness: this.assessCompleteness(mapping),
      consistency: this.assessConsistency(mapping),
      traceability: this.assessTraceability(mapping),
      alignment: this.assessAlignment(mapping),
      feasibility: this.assessFeasibility(mapping)
    };
    
    const overallScore = this.calculateOverallScore(criteria);
    const issues = this.identifyIssues(criteria);
    const recommendations = this.generateRecommendations(issues);
    
    return {
      score: overallScore,
      criteria,
      issues,
      recommendations
    };
  }
  
  private assessCompleteness(
    mapping: ProblemSolutionMapping
  ): CompletenessScore {
    // すべての問題要素が解決要素にマッピングされているか
    const unmappedCapabilities = this.findUnmappedCapabilities(mapping);
    const unmappedRequirements = this.findUnmappedRequirements(mapping);
    const unaddressedConstraints = this.findUnaddressedConstraints(mapping);
    
    return {
      score: 1 - (unmappedCapabilities.length + 
                  unmappedRequirements.length + 
                  unaddressedConstraints.length) / 
                 (mapping.problemSpace.capabilities.length +
                  mapping.problemSpace.requirements.length +
                  mapping.problemSpace.constraints.length),
      gaps: {
        capabilities: unmappedCapabilities,
        requirements: unmappedRequirements,
        constraints: unaddressedConstraints
      }
    };
  }
}
```

## ケイパビリティからコンポーネントへ

### ケイパビリティ分解戦略

```typescript
export class CapabilityDecomposer {
  decomposeCapability(
    capability: BusinessCapability
  ): ComponentSpecification[] {
    // ケイパビリティの性質を分析
    const analysis = this.analyzeCapabilityNature(capability);
    
    // 分解戦略の選択
    const strategy = this.selectDecompositionStrategy(analysis);
    
    // コンポーネント候補の生成
    const components = this.generateComponents(capability, strategy);
    
    // 最適化
    return this.optimizeComponentStructure(components);
  }
  
  private analyzeCapabilityNature(
    capability: BusinessCapability
  ): CapabilityAnalysis {
    return {
      complexity: this.measureComplexity(capability),
      volatility: this.measureVolatility(capability),
      dependencies: this.analyzeDependencies(capability),
      dataIntensity: this.measureDataIntensity(capability),
      userInteraction: this.measureUserInteraction(capability),
      businessCriticality: this.assessCriticality(capability)
    };
  }
  
  private selectDecompositionStrategy(
    analysis: CapabilityAnalysis
  ): DecompositionStrategy {
    if (analysis.dataIntensity > 0.7) {
      return DecompositionStrategy.DATA_CENTRIC;
    } else if (analysis.userInteraction > 0.7) {
      return DecompositionStrategy.UI_DRIVEN;
    } else if (analysis.complexity > 0.8) {
      return DecompositionStrategy.LAYERED;
    } else {
      return DecompositionStrategy.FUNCTIONAL;
    }
  }
}

// 実例：注文処理ケイパビリティの分解
const orderProcessingDecomposition = {
  capability: "注文処理",
  
  components: [
    {
      name: "OrderAPI",
      type: "API Gateway",
      responsibilities: [
        "注文の受付",
        "検証",
        "ルーティング"
      ],
      interfaces: {
        inbound: ["REST API", "GraphQL"],
        outbound: ["Event Bus", "Service Calls"]
      }
    },
    {
      name: "OrderOrchestrator",
      type: "Process Engine",
      responsibilities: [
        "注文フローの制御",
        "状態管理",
        "補償トランザクション"
      ],
      patterns: ["Saga", "State Machine"]
    },
    {
      name: "OrderValidator",
      type: "Business Logic",
      responsibilities: [
        "在庫確認",
        "与信チェック",
        "ビジネスルール適用"
      ]
    },
    {
      name: "OrderPersistence",
      type: "Data Service",
      responsibilities: [
        "注文データの永続化",
        "履歴管理",
        "監査証跡"
      ],
      technology: ["PostgreSQL", "Event Store"]
    }
  ]
};
```

### コンポーネント間の関係設計

```typescript
export class ComponentRelationshipDesigner {
  designRelationships(
    components: ComponentSpecification[]
  ): ComponentRelationshipModel {
    // 依存関係の分析
    const dependencies = this.analyzeDependencies(components);
    
    // 通信パターンの決定
    const communicationPatterns = this.decideCommunicationPatterns(
      components,
      dependencies
    );
    
    // インターフェース定義
    const interfaces = this.defineInterfaces(
      components,
      communicationPatterns
    );
    
    // 統合パターンの適用
    const integrationPatterns = this.applyIntegrationPatterns(
      components,
      interfaces
    );
    
    return {
      components,
      dependencies,
      communicationPatterns,
      interfaces,
      integrationPatterns,
      diagram: this.generateDiagram(components, dependencies)
    };
  }
  
  private decideCommunicationPatterns(
    components: ComponentSpecification[],
    dependencies: Dependency[]
  ): CommunicationPattern[] {
    return dependencies.map(dep => {
      const nature = this.analyzeDependencyNature(dep);
      
      if (nature.isRealtime && nature.isRequestResponse) {
        return {
          from: dep.from,
          to: dep.to,
          pattern: "Synchronous REST",
          reasoning: "低遅延の要求応答が必要"
        };
      } else if (nature.isEventDriven) {
        return {
          from: dep.from,
          to: dep.to,
          pattern: "Event Streaming",
          reasoning: "疎結合と非同期処理が適切"
        };
      } else if (nature.isBulkData) {
        return {
          from: dep.from,
          to: dep.to,
          pattern: "Batch Transfer",
          reasoning: "大量データの効率的な転送"
        };
      }
      // その他のパターン...
    });
  }
}
```

## 制約から設計決定へ

### 制約駆動アーキテクチャ決定

```typescript
export class ConstraintDrivenArchitect {
  makeArchitectureDecisions(
    constraints: Constraint[],
    requirements: Requirement[]
  ): ArchitectureDecision[] {
    const decisions: ArchitectureDecision[] = [];
    
    // 制約の優先順位付け
    const prioritizedConstraints = this.prioritizeConstraints(constraints);
    
    // 各制約に対する設計決定
    for (const constraint of prioritizedConstraints) {
      const decision = this.addressConstraint(constraint, requirements);
      decisions.push(decision);
      
      // 決定の影響を他の制約に反映
      this.propagateDecisionImpact(decision, constraints);
    }
    
    // 決定間の整合性確認
    this.validateDecisionConsistency(decisions);
    
    return decisions;
  }
  
  private addressConstraint(
    constraint: Constraint,
    requirements: Requirement[]
  ): ArchitectureDecision {
    switch (constraint.type) {
      case ConstraintType.PERFORMANCE:
        return this.addressPerformanceConstraint(constraint, requirements);
        
      case ConstraintType.REGULATORY:
        return this.addressRegulatoryConstraint(constraint, requirements);
        
      case ConstraintType.TECHNICAL_DEBT:
        return this.addressTechnicalDebtConstraint(constraint, requirements);
        
      // 他の制約タイプ...
    }
  }
  
  private addressPerformanceConstraint(
    constraint: Constraint,
    requirements: Requirement[]
  ): ArchitectureDecision {
    const performanceRequirements = requirements.filter(
      r => r.category === 'performance'
    );
    
    return {
      id: `DEC-PERF-${Date.now()}`,
      constraint: constraint.id,
      decision: "マイクロサービス + キャッシング戦略",
      rationale: "レスポンスタイム100ms以下を達成するため",
      implications: [
        "Redisによる分散キャッシュの導入",
        "CDNでの静的コンテンツ配信",
        "データベースの読み取りレプリカ"
      ],
      alternatives: [
        {
          option: "モノリシック + 垂直スケーリング",
          reason: "却下：スケーラビリティの限界"
        },
        {
          option: "サーバーレス",
          reason: "却下：コールドスタートの遅延"
        }
      ],
      tradeoffs: [
        "複雑性の増加",
        "運用コストの上昇",
        "開発期間の延長"
      ]
    };
  }
}
```

## 要求から機能へ

### 要求の構造化と優先順位付け

```typescript
export class RequirementStructurer {
  structureRequirements(
    rawRequirements: RawRequirement[],
    valueStreams: ValueStream[]
  ): StructuredRequirement[] {
    // 要求の分類
    const categorized = this.categorizeRequirements(rawRequirements);
    
    // 価値ストリームとの関連付け
    const aligned = this.alignWithValueStreams(categorized, valueStreams);
    
    // 優先順位付け
    const prioritized = this.prioritizeRequirements(aligned);
    
    // 依存関係の分析
    const withDependencies = this.analyzeDependencies(prioritized);
    
    return withDependencies;
  }
  
  private prioritizeRequirements(
    requirements: AlignedRequirement[]
  ): PrioritizedRequirement[] {
    return requirements.map(req => {
      const score = this.calculatePriorityScore({
        businessValue: req.businessValue,
        urgency: req.urgency,
        risk: req.risk,
        effort: req.estimatedEffort,
        dependencies: req.dependencies
      });
      
      return {
        ...req,
        priority: score,
        category: this.categorizePriority(score)
      };
    }).sort((a, b) => b.priority - a.priority);
  }
}

// 要求から機能への変換
export class RequirementToFeatureMapper {
  mapToFeatures(
    requirements: StructuredRequirement[]
  ): Feature[] {
    const features: Feature[] = [];
    
    // 要求のグループ化
    const groups = this.groupRelatedRequirements(requirements);
    
    for (const group of groups) {
      const feature = this.synthesizeFeature(group);
      features.push(feature);
    }
    
    return this.optimizeFeatureSet(features);
  }
  
  private synthesizeFeature(
    requirements: StructuredRequirement[]
  ): Feature {
    return {
      id: this.generateFeatureId(),
      name: this.deriveFeatureName(requirements),
      description: this.synthesizeDescription(requirements),
      requirements: requirements.map(r => r.id),
      
      // 機能仕様
      specification: {
        inputs: this.consolidateInputs(requirements),
        processing: this.defineProcessing(requirements),
        outputs: this.consolidateOutputs(requirements),
        rules: this.extractBusinessRules(requirements),
        constraints: this.consolidateConstraints(requirements)
      },
      
      // 実装の指針
      implementation: {
        components: this.identifyComponents(requirements),
        apis: this.defineApis(requirements),
        dataModel: this.designDataModel(requirements),
        ui: this.sketchUserInterface(requirements)
      },
      
      // 受け入れ基準
      acceptanceCriteria: this.defineAcceptanceCriteria(requirements),
      
      // メトリクス
      metrics: this.defineMetrics(requirements)
    };
  }
}
```

## 統合的なマッピングプロセス

### エンドツーエンドマッピング

```typescript
export class E2ESolutionMapper {
  async mapProblemToSolution(
    problemSpace: ProblemSpace
  ): Promise<SolutionSpace> {
    // 1. 価値ストリームの分析
    const valueAnalysis = await this.analyzeValueStreams(
      problemSpace.valueStreams
    );
    
    // 2. ケイパビリティマッピング
    const capabilityMappings = await this.mapCapabilities(
      problemSpace.capabilities,
      valueAnalysis
    );
    
    // 3. 制約の考慮
    const constraintDecisions = await this.addressConstraints(
      problemSpace.constraints,
      capabilityMappings
    );
    
    // 4. アーキテクチャ設計
    const architecture = await this.designArchitecture(
      capabilityMappings,
      constraintDecisions
    );
    
    // 5. 詳細設計
    const detailedDesign = await this.createDetailedDesign(
      architecture,
      problemSpace.requirements
    );
    
    // 6. 検証
    const validation = await this.validateMapping(
      problemSpace,
      detailedDesign
    );
    
    return {
      architecture,
      components: detailedDesign.components,
      services: detailedDesign.services,
      dataModel: detailedDesign.dataModel,
      infrastructure: detailedDesign.infrastructure,
      validation,
      traceability: this.establishTraceability(problemSpace, detailedDesign)
    };
  }
}

// 実践例：ECサイトのマッピング
class ECommerceMapping {
  async mapECommerceSolution(): Promise<SolutionSpace> {
    const problemSpace = {
      valueStreams: [
        {
          name: "顧客購買ジャーニー",
          stages: ["商品発見", "選択", "購入", "受取", "アフターサービス"]
        }
      ],
      
      capabilities: [
        {
          name: "商品推奨",
          area: "顧客エンゲージメント",
          maturity: 3
        },
        {
          name: "在庫管理",
          area: "サプライチェーン",
          maturity: 4
        },
        {
          name: "決済処理",
          area: "取引処理",
          maturity: 5
        }
      ],
      
      constraints: [
        {
          type: "PERFORMANCE",
          description: "ピーク時10万同時ユーザー"
        },
        {
          type: "REGULATORY",
          description: "PCI-DSS準拠"
        }
      ]
    };
    
    const solution = await new E2ESolutionMapper().mapProblemToSolution(
      problemSpace
    );
    
    return solution;
  }
}
```

## マッピングの検証と最適化

### トレーサビリティマトリクス

```typescript
export class TraceabilityManager {
  buildTraceabilityMatrix(
    mapping: ProblemSolutionMapping
  ): TraceabilityMatrix {
    const matrix = new TraceabilityMatrix();
    
    // 前方トレース（問題→解決）
    for (const capability of mapping.problemSpace.capabilities) {
      const components = mapping.mappings.capabilityToComponent.get(
        capability.id
      ) || [];
      
      matrix.addForwardTrace(capability.id, components);
    }
    
    // 後方トレース（解決→問題）
    for (const component of mapping.solutionSpace.components) {
      const capabilities = this.findSourceCapabilities(
        component,
        mapping
      );
      
      matrix.addBackwardTrace(component.id, capabilities);
    }
    
    // カバレッジ分析
    const coverage = matrix.analyzeCoverage();
    
    // ギャップ識別
    const gaps = matrix.identifyGaps();
    
    return {
      matrix,
      coverage,
      gaps,
      recommendations: this.generateRecommendations(gaps)
    };
  }
}

// 可視化
export class MappingVisualizer {
  visualizeMapping(
    mapping: ProblemSolutionMapping
  ): MappingVisualization {
    return {
      sankeyDiagram: this.createSankeyDiagram(mapping),
      matrixHeatmap: this.createMatrixHeatmap(mapping),
      networkGraph: this.createNetworkGraph(mapping),
      coverageReport: this.generateCoverageReport(mapping)
    };
  }
  
  private createSankeyDiagram(
    mapping: ProblemSolutionMapping
  ): SankeyDiagram {
    const nodes = [
      ...mapping.problemSpace.capabilities.map(c => ({
        id: c.id,
        label: c.name,
        type: 'capability'
      })),
      ...mapping.solutionSpace.components.map(c => ({
        id: c.id,
        label: c.name,
        type: 'component'
      }))
    ];
    
    const links = [];
    mapping.mappings.capabilityToComponent.forEach((components, capability) => {
      components.forEach(component => {
        links.push({
          source: capability,
          target: component,
          value: this.calculateMappingStrength(capability, component)
        });
      });
    });
    
    return { nodes, links };
  }
}
```

## マッピングパターンとアンチパターン

### 推奨パターン

```typescript
export const MappingPatterns = {
  // 1. 単一責任マッピング
  SINGLE_RESPONSIBILITY: {
    description: "1つのケイパビリティは1つの主要コンポーネントに対応",
    when: "ケイパビリティが明確に定義されている場合",
    benefits: ["明確な責任境界", "保守性の向上"],
    example: "決済処理ケイパビリティ → PaymentServiceコンポーネント"
  },
  
  // 2. ファサードパターン
  FACADE: {
    description: "複雑なケイパビリティを単純なインターフェースで包む",
    when: "レガシーシステムとの統合が必要な場合",
    benefits: ["複雑性の隠蔽", "段階的な移行"],
    example: "統合顧客管理 → CustomerAPIファサード → 複数のバックエンドシステム"
  },
  
  // 3. イベント駆動マッピング
  EVENT_DRIVEN: {
    description: "ケイパビリティ間の相互作用をイベントで実現",
    when: "疎結合が重要な場合",
    benefits: ["拡張性", "非同期処理"],
    example: "注文→在庫→配送の連携をイベントストリームで実現"
  }
};

// アンチパターン
export const MappingAntiPatterns = {
  // 1. ビッグボールオブマッド
  BIG_BALL_OF_MUD: {
    description: "すべてを1つのコンポーネントにマッピング",
    symptoms: ["巨大なコンポーネント", "不明確な責任"],
    consequences: ["保守困難", "テスト困難"],
    remedy: "ケイパビリティの再分析と分割"
  },
  
  // 2. 過度な分散
  OVER_DISTRIBUTION: {
    description: "1つのケイパビリティを過度に多くのコンポーネントに分散",
    symptoms: ["過剰なネットワーク通信", "複雑な調整"],
    consequences: ["性能劣化", "運用複雑性"],
    remedy: "関連機能の適切な集約"
  }
};
```

## 継続的なマッピング改善

```typescript
export class MappingEvolution {
  evolveMappings(
    currentMapping: ProblemSolutionMapping,
    feedback: OperationalFeedback
  ): ImprovedMapping {
    // パフォーマンス問題の分析
    const performanceIssues = this.analyzePerformanceBottlenecks(
      feedback.performanceMetrics
    );
    
    // マッピングの調整提案
    const adjustments = this.proposeAdjustments(
      currentMapping,
      performanceIssues
    );
    
    // 影響分析
    const impact = this.analyzeAdjustmentImpact(adjustments);
    
    // 段階的適用計画
    const evolutionPlan = this.createEvolutionPlan(
      adjustments,
      impact
    );
    
    return {
      current: currentMapping,
      proposed: this.applyAdjustments(currentMapping, adjustments),
      plan: evolutionPlan,
      expectedBenefits: this.calculateBenefits(adjustments)
    };
  }
}
```

## まとめ

問題空間から解決空間へのマッピングは、Parasol V5.4の中核的な活動です。成功のポイント：

1. **体系的アプローチ** - 価値→ケイパビリティ→コンポーネントの順序でマッピング
2. **制約の積極的活用** - 制約を設計の指針として活用
3. **トレーサビリティの確保** - 双方向の追跡可能性を維持
4. **継続的な検証** - マッピングの品質を定期的に評価
5. **進化的改善** - 運用フィードバックに基づく継続的な最適化

適切なマッピングにより、ビジネスの要求と技術の実装が確実につながり、価値の実現が保証されます。

### 次章への架橋

問題空間から解決空間への橋渡しを理解したところで、次の第17章からは、具体的な解決空間でのアーキテクチャ設計に入っていきます。

---

## 演習問題

1. 自組織の主要なケイパビリティを1つ選び、それを実現するコンポーネント構成を設計してください。

2. 現在のプロジェクトにおける主要な制約を3つ選び、それぞれに対応するアーキテクチャ決定を文書化してください。

3. 要求から機能へのマッピングで、トレーサビリティマトリクスを作成し、カバレッジを分析してください。