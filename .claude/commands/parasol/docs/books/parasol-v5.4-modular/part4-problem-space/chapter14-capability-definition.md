# 第14章　ケイパビリティ定義 ― 能力の本質を捉える

## はじめに：ケイパビリティとは何か

企業を訪問すると、よく「うちの強みは技術力です」「営業力が自慢です」といった話を聞きます。しかし、それらの「力」の実体は何でしょうか？どのように定義し、測定し、改善すればよいのでしょうか？

ケイパビリティ（Capability）とは、組織が価値を生み出すために必要な「能力」を構造化したものです。それは単なる機能や部門ではなく、人、プロセス、技術、情報が統合された、価値創造の単位なのです。

## ケイパビリティの階層構造

### CL1: ケイパビリティ領域（Activity Areas）

最上位レベルでは、企業活動を大きな領域に分類します：

```typescript
export enum CapabilityArea {
  // 顧客対面活動
  CUSTOMER_ENGAGEMENT = "顧客エンゲージメント",
  SALES_DISTRIBUTION = "販売・流通",
  
  // 価値創造活動
  PRODUCT_DEVELOPMENT = "商品開発",
  SERVICE_DELIVERY = "サービス提供",
  
  // 支援活動
  SUPPLY_CHAIN = "サプライチェーン",
  HUMAN_RESOURCES = "人的資源管理",
  FINANCE_CONTROL = "財務・管理",
  IT_DIGITAL = "IT・デジタル"
}
```

### CL2: ビジネスケイパビリティ（Business Capabilities）

各領域を具体的なケイパビリティに分解します：

```typescript
export interface BusinessCapability {
  id: string;
  name: string;
  area: CapabilityArea;
  description: string;
  
  // ケイパビリティの構成要素
  components: {
    people: PeopleComponent;
    process: ProcessComponent;
    technology: TechnologyComponent;
    information: InformationComponent;
  };
  
  // 成熟度評価
  maturity: MaturityLevel;
  
  // 価値への貢献
  valueContribution: ValueContribution;
}

// 具体例：「顧客ニーズ分析」ケイパビリティ
const customerNeedsAnalysis: BusinessCapability = {
  id: "CAP-CE-001",
  name: "顧客ニーズ分析",
  area: CapabilityArea.CUSTOMER_ENGAGEMENT,
  description: "顧客の明示的・潜在的ニーズを発見し、構造化する能力",
  
  components: {
    people: {
      roles: ["カスタマーアナリスト", "UXリサーチャー"],
      skills: ["インタビュー技術", "データ分析", "共感力"],
      count: 5
    },
    process: {
      activities: [
        "顧客インタビュー実施",
        "行動観察",
        "データ分析",
        "インサイト抽出"
      ],
      maturityLevel: 3
    },
    technology: {
      tools: ["CRM", "分析ツール", "アンケートシステム"],
      integrations: ["営業システム", "マーケティングDB"]
    },
    information: {
      inputs: ["顧客プロファイル", "購買履歴", "問い合わせ履歴"],
      outputs: ["ニーズマップ", "ペルソナ", "カスタマージャーニー"]
    }
  },
  
  maturity: MaturityLevel.DEFINED,
  
  valueContribution: {
    directValue: "顧客満足度向上",
    metrics: ["NPS", "リピート率"],
    strategicImportance: "HIGH"
  }
};
```

### CL3: ビジネス運用能力（Business Operations）

ケイパビリティを実際の運用レベルに展開します：

```typescript
export interface BusinessOperation {
  id: string;
  name: string;
  parentCapability: string;
  
  // 運用の詳細
  operationalDetails: {
    frequency: OperationFrequency;
    volume: number;
    sla: ServiceLevelAgreement;
    dependencies: Dependency[];
  };
  
  // 実行条件
  triggers: Trigger[];
  inputs: Input[];
  outputs: Output[];
  
  // 測定指標
  kpis: KeyPerformanceIndicator[];
}

// 実装例
class CapabilityOperationMapper {
  mapToOperations(
    capability: BusinessCapability
  ): BusinessOperation[] {
    const operations: BusinessOperation[] = [];
    
    // ケイパビリティを構成する運用活動を定義
    switch (capability.id) {
      case "CAP-CE-001": // 顧客ニーズ分析
        operations.push(
          this.createOperation("定期顧客インタビュー", {
            frequency: OperationFrequency.MONTHLY,
            volume: 20, // 月20件
            sla: { responseTime: "48h", quality: "95%" }
          }),
          this.createOperation("購買データ分析", {
            frequency: OperationFrequency.WEEKLY,
            volume: 1000, // 週1000件
            sla: { completionTime: "4h", accuracy: "99%" }
          }),
          this.createOperation("インサイトレポート作成", {
            frequency: OperationFrequency.MONTHLY,
            volume: 1,
            sla: { deliveryTime: "5d", stakeholderSatisfaction: "4/5" }
          })
        );
        break;
        
      // 他のケイパビリティも同様に定義...
    }
    
    return operations;
  }
}
```

## ケイパビリティの定義プロセス

### ステップ1: トップダウン分解

価値ストリームから必要なケイパビリティを導出します：

```typescript
export class CapabilityDerivation {
  deriveFromValueStream(
    valueStream: ValueStream
  ): BusinessCapability[] {
    const requiredCapabilities: BusinessCapability[] = [];
    
    for (const stage of valueStream.stages) {
      // 各価値ステージで必要な能力を識別
      const capabilities = this.identifyRequiredCapabilities(stage);
      
      // 既存ケイパビリティとのマッピング
      for (const cap of capabilities) {
        const existing = this.findExistingCapability(cap);
        if (existing) {
          // ギャップ分析
          const gap = this.analyzeGap(existing, cap);
          if (gap.hasGap) {
            existing.improvements = gap.improvements;
          }
          requiredCapabilities.push(existing);
        } else {
          // 新規ケイパビリティの定義
          requiredCapabilities.push(this.defineNewCapability(cap));
        }
      }
    }
    
    return this.optimizeCapabilities(requiredCapabilities);
  }
  
  private identifyRequiredCapabilities(
    valueStage: ValueStage
  ): CapabilityRequirement[] {
    const requirements: CapabilityRequirement[] = [];
    
    // 価値ステージの活動を分析
    for (const activity of valueStage.activities) {
      requirements.push({
        activity: activity.name,
        requiredSkills: activity.skills,
        requiredProcesses: activity.processes,
        requiredTechnology: activity.technology,
        expectedOutcome: activity.outcome
      });
    }
    
    return this.consolidateRequirements(requirements);
  }
}
```

### ステップ2: ボトムアップ確認

現場の実態からケイパビリティを検証します：

```typescript
export class CapabilityValidation {
  async validateWithReality(
    definedCapability: BusinessCapability
  ): Promise<ValidationResult> {
    // 現場観察
    const observations = await this.observeActualWork(
      definedCapability.components.people.roles
    );
    
    // ギャップの特定
    const gaps = {
      processGaps: this.compareProcesses(
        definedCapability.components.process,
        observations.actualProcesses
      ),
      skillGaps: this.compareSkills(
        definedCapability.components.people.skills,
        observations.actualSkills
      ),
      technologyGaps: this.compareTechnology(
        definedCapability.components.technology,
        observations.actualTools
      )
    };
    
    // 調整提案
    const adjustments = this.proposeAdjustments(gaps);
    
    return {
      isValid: Object.values(gaps).every(g => g.length === 0),
      gaps,
      adjustments,
      confidenceLevel: this.calculateConfidence(observations)
    };
  }
}
```

### ステップ3: ケイパビリティの構造化

```typescript
// ケイパビリティマップの作成
export class CapabilityMap {
  private capabilities: Map<string, BusinessCapability> = new Map();
  private relationships: CapabilityRelationship[] = [];
  
  buildMap(
    valueStreams: ValueStream[],
    organizationContext: OrganizationContext
  ): void {
    // 1. 価値ストリームからケイパビリティを抽出
    for (const stream of valueStreams) {
      const caps = this.extractCapabilities(stream);
      caps.forEach(c => this.capabilities.set(c.id, c));
    }
    
    // 2. ケイパビリティ間の関係を分析
    this.analyzeRelationships();
    
    // 3. 重複や欠落をチェック
    this.validateCompleteness();
    
    // 4. 最適化
    this.optimizeStructure();
  }
  
  private analyzeRelationships(): void {
    for (const [id1, cap1] of this.capabilities) {
      for (const [id2, cap2] of this.capabilities) {
        if (id1 !== id2) {
          const relationship = this.detectRelationship(cap1, cap2);
          if (relationship) {
            this.relationships.push(relationship);
          }
        }
      }
    }
  }
  
  visualize(): CapabilityMapVisualization {
    return {
      nodes: Array.from(this.capabilities.values()).map(cap => ({
        id: cap.id,
        label: cap.name,
        area: cap.area,
        maturity: cap.maturity,
        size: this.calculateImportance(cap)
      })),
      edges: this.relationships.map(rel => ({
        source: rel.from,
        target: rel.to,
        type: rel.type,
        strength: rel.strength
      }))
    };
  }
}
```

## ケイパビリティの評価

### 成熟度モデル

```typescript
export enum MaturityLevel {
  INITIAL = 1,      // 場当たり的
  REPEATABLE = 2,   // 反復可能
  DEFINED = 3,      // 定義済み
  MANAGED = 4,      // 管理された
  OPTIMIZED = 5     // 最適化
}

export class CapabilityMaturityAssessment {
  assess(capability: BusinessCapability): MaturityAssessment {
    const dimensions = {
      process: this.assessProcessMaturity(capability.components.process),
      people: this.assessPeopleMaturity(capability.components.people),
      technology: this.assessTechnologyMaturity(capability.components.technology),
      information: this.assessInformationMaturity(capability.components.information)
    };
    
    // 最も低い次元が全体の成熟度を決定（ボトルネック原理）
    const overallMaturity = Math.min(...Object.values(dimensions));
    
    // 改善提案
    const improvements = this.identifyImprovements(dimensions, capability);
    
    return {
      current: overallMaturity,
      target: capability.targetMaturity || MaturityLevel.MANAGED,
      dimensions,
      improvements,
      estimatedEffort: this.estimateImprovementEffort(improvements)
    };
  }
  
  private assessProcessMaturity(process: ProcessComponent): MaturityLevel {
    const factors = {
      documented: process.documentation ? 1 : 0,
      standardized: process.standardized ? 1 : 0,
      measured: process.metrics ? 1 : 0,
      optimized: process.continuousImprovement ? 1 : 0
    };
    
    const score = Object.values(factors).reduce((a, b) => a + b, 0);
    return this.scoreToMaturityLevel(score);
  }
}
```

### 価値貢献度の測定

```typescript
export class CapabilityValueMeasurement {
  measureValueContribution(
    capability: BusinessCapability,
    valueStreams: ValueStream[]
  ): ValueContributionScore {
    // 直接的な価値貢献
    const directContribution = this.calculateDirectContribution(
      capability,
      valueStreams
    );
    
    // 間接的な価値貢献（他のケイパビリティへの支援）
    const indirectContribution = this.calculateIndirectContribution(
      capability
    );
    
    // 戦略的重要性
    const strategicImportance = this.assessStrategicImportance(
      capability
    );
    
    // 総合スコア
    const totalScore = 
      directContribution * 0.5 +
      indirectContribution * 0.3 +
      strategicImportance * 0.2;
    
    return {
      total: totalScore,
      breakdown: {
        direct: directContribution,
        indirect: indirectContribution,
        strategic: strategicImportance
      },
      insights: this.generateInsights(capability, totalScore)
    };
  }
}
```

## ケイパビリティの実装例

### 小売業の商品調達ケイパビリティ

```typescript
const productSourcingCapability: BusinessCapability = {
  id: "CAP-SC-002",
  name: "商品調達",
  area: CapabilityArea.SUPPLY_CHAIN,
  description: "市場ニーズに基づいて最適な商品を最適な条件で調達する能力",
  
  components: {
    people: {
      roles: ["バイヤー", "商品企画", "品質管理"],
      skills: [
        "市場分析",
        "交渉力",
        "トレンド予測",
        "サプライヤー管理"
      ],
      count: 15,
      organizationUnit: "商品本部"
    },
    
    process: {
      activities: [
        "市場調査",
        "商品選定",
        "サプライヤー評価",
        "価格交渉",
        "発注管理",
        "品質検査"
      ],
      maturityLevel: 3,
      documentation: "procurement-process-v2.pdf",
      standardized: true,
      metrics: ["調達リードタイム", "調達コスト削減率"]
    },
    
    technology: {
      tools: [
        "調達管理システム",
        "サプライヤーポータル",
        "市場分析ツール",
        "在庫最適化AI"
      ],
      integrations: [
        "在庫管理システム",
        "販売管理システム",
        "会計システム"
      ],
      automationLevel: 0.6
    },
    
    information: {
      inputs: [
        "販売実績データ",
        "市場トレンド情報",
        "在庫状況",
        "サプライヤー情報"
      ],
      outputs: [
        "発注書",
        "商品マスタ",
        "調達計画",
        "サプライヤー評価レポート"
      ],
      dataQuality: 0.85
    }
  },
  
  maturity: MaturityLevel.DEFINED,
  targetMaturity: MaturityLevel.MANAGED,
  
  valueContribution: {
    directValue: "商品原価の最適化による利益率向上",
    metrics: [
      "粗利率",
      "在庫回転率",
      "欠品率"
    ],
    strategicImportance: "HIGH",
    dependencies: ["CAP-CE-001", "CAP-SD-003"]
  }
};

// このケイパビリティの改善計画
class SourcingCapabilityImprovement {
  async planImprovement(
    current: BusinessCapability
  ): Promise<ImprovementPlan> {
    // 現状分析
    const assessment = await this.assessCurrentState(current);
    
    // 改善機会の特定
    const opportunities = {
      processAutomation: {
        description: "定型的な発注業務の自動化",
        impact: "バイヤーの戦略的業務への集中",
        effort: "Medium",
        roi: 2.5
      },
      
      aiIntegration: {
        description: "AI による需要予測の精度向上",
        impact: "在庫最適化による資金効率改善",
        effort: "High",
        roi: 3.2
      },
      
      supplierCollaboration: {
        description: "サプライヤーとのEDI連携強化",
        impact: "リードタイム短縮と事務効率化",
        effort: "Medium",
        roi: 1.8
      }
    };
    
    // 実装ロードマップ
    const roadmap = this.createRoadmap(opportunities, assessment);
    
    return {
      currentState: assessment,
      opportunities,
      roadmap,
      expectedBenefits: this.calculateBenefits(opportunities),
      requiredInvestment: this.estimateInvestment(roadmap)
    };
  }
}
```

## ケイパビリティのガバナンス

### オーナーシップの確立

```typescript
export interface CapabilityOwnership {
  capability: BusinessCapability;
  owner: {
    role: string;
    name: string;
    responsibilities: string[];
  };
  stakeholders: Stakeholder[];
  governanceModel: {
    decisionRights: DecisionRight[];
    performanceReview: ReviewSchedule;
    improvementProcess: Process;
  };
}

export class CapabilityGovernance {
  establishOwnership(capability: BusinessCapability): CapabilityOwnership {
    // オーナーの選定基準
    const ownerCriteria = {
      businessKnowledge: 0.3,
      technicalUnderstanding: 0.2,
      leadershipSkills: 0.3,
      stakeholderRelationships: 0.2
    };
    
    // 候補者の評価
    const candidates = this.identifyCandidates(capability);
    const selectedOwner = this.selectOwner(candidates, ownerCriteria);
    
    // ガバナンスモデルの設計
    const governance = {
      decisionRights: this.defineDecisionRights(capability),
      performanceReview: {
        frequency: "quarterly",
        metrics: this.defineMetrics(capability),
        reviewBoard: this.selectReviewBoard(capability)
      },
      improvementProcess: this.designImprovementProcess(capability)
    };
    
    return {
      capability,
      owner: selectedOwner,
      stakeholders: this.identifyStakeholders(capability),
      governanceModel: governance
    };
  }
}
```

## まとめ

ケイパビリティの適切な定義は、Parasol V5.4の成功の鍵です。重要なポイント：

1. **構造的アプローチ** - CL1→CL2→CL3の階層で体系的に定義
2. **4つの構成要素** - 人、プロセス、技術、情報の統合
3. **価値との接続** - 各ケイパビリティが価値創出にどう貢献するか明確化
4. **継続的改善** - 成熟度評価と改善計画の実施
5. **ガバナンス** - 明確なオーナーシップと責任体制

ケイパビリティは静的な定義ではなく、組織と共に進化する生きた存在として扱うことが重要です。

### 次章への架橋

ケイパビリティの定義方法を理解したところで、次の第15章では、これらのケイパビリティが抱える様々な制約をどのように扱い、調整するかを詳しく見ていきます。

---

## 演習問題

1. 自組織の主要な価値ストリームを1つ選び、それを支えるケイパビリティを3階層で定義してください。

2. 定義したケイパビリティの1つについて、4つの構成要素（人、プロセス、技術、情報）を詳細に記述してください。

3. そのケイパビリティの成熟度を5段階で評価し、改善計画を立案してください。