# Appendix: Chapter 14 - Capability Definition Implementation Details

This appendix provides detailed code implementations and technical specifications for the capability definition concepts discussed in Chapter 14.

## Complete Type Definitions

### Core Capability Enumerations and Types

```typescript
// Capability Areas - Top level classification
export enum CapabilityArea {
  // Customer-facing activities
  CUSTOMER_ENGAGEMENT = "顧客エンゲージメント",
  SALES_DISTRIBUTION = "販売・流通",
  
  // Value creation activities
  PRODUCT_DEVELOPMENT = "商品開発",
  SERVICE_DELIVERY = "サービス提供",
  
  // Supporting activities
  SUPPLY_CHAIN = "サプライチェーン",
  HUMAN_RESOURCES = "人的資源管理",
  FINANCE_CONTROL = "財務・管理",
  IT_DIGITAL = "IT・デジタル"
}

// Maturity Levels for capability assessment
export enum MaturityLevel {
  INITIAL = 1,      // Ad hoc, chaotic
  REPEATABLE = 2,   // Basic processes established
  DEFINED = 3,      // Documented and standardized
  MANAGED = 4,      // Measured and controlled
  OPTIMIZED = 5     // Continuous improvement
}

// Operation frequency for business operations
export enum OperationFrequency {
  CONTINUOUS = "continuous",
  HOURLY = "hourly",
  DAILY = "daily",
  WEEKLY = "weekly",
  MONTHLY = "monthly",
  QUARTERLY = "quarterly",
  ANNUALLY = "annually",
  AD_HOC = "ad-hoc"
}

// Capability relationship types
export enum RelationshipType {
  DEPENDS_ON = "depends-on",
  SUPPORTS = "supports",
  SHARES_RESOURCES = "shares-resources",
  ENABLES = "enables",
  CONSTRAINS = "constrains"
}
```

### Component Interfaces

```typescript
// People component of a capability
export interface PeopleComponent {
  roles: string[];
  skills: string[];
  count: number;
  organizationUnit?: string;
  competencyLevels?: Map<string, number>;
  certifications?: string[];
  trainingNeeds?: string[];
}

// Process component of a capability
export interface ProcessComponent {
  activities: string[];
  maturityLevel: MaturityLevel;
  documentation?: string;
  standardized: boolean;
  metrics?: string[];
  processOwner?: string;
  complianceRequirements?: string[];
  automationOpportunities?: string[];
}

// Technology component of a capability
export interface TechnologyComponent {
  tools: string[];
  integrations: string[];
  automationLevel?: number; // 0-1 scale
  platforms?: string[];
  apis?: string[];
  dataFormats?: string[];
  securityRequirements?: string[];
  scalabilityNeeds?: string[];
}

// Information component of a capability
export interface InformationComponent {
  inputs: string[];
  outputs: string[];
  dataQuality?: number; // 0-1 scale
  dataSources?: string[];
  updateFrequency?: OperationFrequency;
  storageRequirements?: string;
  privacyClassification?: string;
  retentionPolicy?: string;
}
```

### Main Capability Interfaces

```typescript
// Value contribution structure
export interface ValueContribution {
  directValue: string;
  metrics: string[];
  strategicImportance: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  dependencies?: string[]; // Other capability IDs
  financialImpact?: {
    revenue?: number;
    costSavings?: number;
    efficiency?: number;
  };
}

// Main business capability interface
export interface BusinessCapability {
  id: string;
  name: string;
  area: CapabilityArea;
  description: string;
  
  // Core components
  components: {
    people: PeopleComponent;
    process: ProcessComponent;
    technology: TechnologyComponent;
    information: InformationComponent;
  };
  
  // Assessment
  maturity: MaturityLevel;
  targetMaturity?: MaturityLevel;
  
  // Value and strategy
  valueContribution: ValueContribution;
  
  // Governance
  owner?: string;
  lastReview?: Date;
  nextReview?: Date;
  
  // Improvements
  improvements?: CapabilityImprovement[];
}

// Capability improvement tracking
export interface CapabilityImprovement {
  id: string;
  description: string;
  impact: string;
  effort: "LOW" | "MEDIUM" | "HIGH";
  roi?: number;
  timeline?: {
    start: Date;
    end: Date;
  };
  status?: "PLANNED" | "IN_PROGRESS" | "COMPLETED";
}
```

## Implementation Classes

### Capability Derivation from Value Streams

```typescript
export class CapabilityDerivation {
  private existingCapabilities: Map<string, BusinessCapability> = new Map();
  
  constructor(existingCaps?: BusinessCapability[]) {
    existingCaps?.forEach(cap => this.existingCapabilities.set(cap.id, cap));
  }
  
  deriveFromValueStream(valueStream: ValueStream): BusinessCapability[] {
    const requiredCapabilities: BusinessCapability[] = [];
    
    // Analyze each stage in the value stream
    for (const stage of valueStream.stages) {
      const capabilities = this.identifyRequiredCapabilities(stage);
      
      for (const cap of capabilities) {
        const existing = this.findExistingCapability(cap);
        
        if (existing) {
          // Analyze gaps between required and existing
          const gap = this.analyzeGap(existing, cap);
          if (gap.hasGap) {
            // Add improvements to existing capability
            existing.improvements = [
              ...(existing.improvements || []),
              ...gap.improvements
            ];
          }
          requiredCapabilities.push(existing);
        } else {
          // Define new capability
          requiredCapabilities.push(this.defineNewCapability(cap));
        }
      }
    }
    
    // Remove duplicates and optimize structure
    return this.optimizeCapabilities(requiredCapabilities);
  }
  
  private identifyRequiredCapabilities(
    valueStage: ValueStage
  ): CapabilityRequirement[] {
    const requirements: CapabilityRequirement[] = [];
    
    // Analyze each activity in the stage
    for (const activity of valueStage.activities) {
      requirements.push({
        activity: activity.name,
        requiredSkills: this.extractRequiredSkills(activity),
        requiredProcesses: this.extractRequiredProcesses(activity),
        requiredTechnology: this.extractRequiredTechnology(activity),
        requiredInformation: this.extractRequiredInformation(activity),
        expectedOutcome: activity.outcome
      });
    }
    
    return this.consolidateRequirements(requirements);
  }
  
  private analyzeGap(
    existing: BusinessCapability,
    required: CapabilityRequirement
  ): CapabilityGap {
    const gaps = {
      skillGaps: this.findSkillGaps(
        existing.components.people.skills,
        required.requiredSkills
      ),
      processGaps: this.findProcessGaps(
        existing.components.process.activities,
        required.requiredProcesses
      ),
      technologyGaps: this.findTechnologyGaps(
        existing.components.technology.tools,
        required.requiredTechnology
      ),
      informationGaps: this.findInformationGaps(
        existing.components.information,
        required.requiredInformation
      )
    };
    
    const hasGap = Object.values(gaps).some(g => g.length > 0);
    
    return {
      hasGap,
      gaps,
      improvements: hasGap ? this.generateImprovements(gaps) : []
    };
  }
  
  private generateImprovements(gaps: any): CapabilityImprovement[] {
    const improvements: CapabilityImprovement[] = [];
    let improvementId = 1;
    
    // Generate improvements for each gap type
    if (gaps.skillGaps.length > 0) {
      improvements.push({
        id: `IMP-${improvementId++}`,
        description: `Develop skills: ${gaps.skillGaps.join(", ")}`,
        impact: "Enhanced capability to deliver value",
        effort: this.assessEffort(gaps.skillGaps.length),
        roi: this.calculateSkillROI(gaps.skillGaps)
      });
    }
    
    if (gaps.processGaps.length > 0) {
      improvements.push({
        id: `IMP-${improvementId++}`,
        description: `Implement processes: ${gaps.processGaps.join(", ")}`,
        impact: "Standardized operations and quality",
        effort: this.assessEffort(gaps.processGaps.length),
        roi: this.calculateProcessROI(gaps.processGaps)
      });
    }
    
    if (gaps.technologyGaps.length > 0) {
      improvements.push({
        id: `IMP-${improvementId++}`,
        description: `Deploy technology: ${gaps.technologyGaps.join(", ")}`,
        impact: "Increased automation and efficiency",
        effort: this.assessEffort(gaps.technologyGaps.length),
        roi: this.calculateTechnologyROI(gaps.technologyGaps)
      });
    }
    
    return improvements;
  }
  
  private assessEffort(gapCount: number): "LOW" | "MEDIUM" | "HIGH" {
    if (gapCount <= 2) return "LOW";
    if (gapCount <= 5) return "MEDIUM";
    return "HIGH";
  }
}
```

### Capability Map Builder

```typescript
export class CapabilityMap {
  private capabilities: Map<string, BusinessCapability> = new Map();
  private relationships: CapabilityRelationship[] = [];
  
  buildMap(
    valueStreams: ValueStream[],
    organizationContext: OrganizationContext
  ): void {
    // Extract capabilities from all value streams
    for (const stream of valueStreams) {
      const derivation = new CapabilityDerivation(
        Array.from(this.capabilities.values())
      );
      const caps = derivation.deriveFromValueStream(stream);
      
      caps.forEach(c => this.capabilities.set(c.id, c));
    }
    
    // Analyze relationships between capabilities
    this.analyzeRelationships();
    
    // Validate completeness and consistency
    this.validateCompleteness();
    
    // Optimize the overall structure
    this.optimizeStructure();
  }
  
  private analyzeRelationships(): void {
    const capArray = Array.from(this.capabilities.values());
    
    for (let i = 0; i < capArray.length; i++) {
      for (let j = i + 1; j < capArray.length; j++) {
        const relationships = this.detectRelationships(
          capArray[i],
          capArray[j]
        );
        
        this.relationships.push(...relationships);
      }
    }
  }
  
  private detectRelationships(
    cap1: BusinessCapability,
    cap2: BusinessCapability
  ): CapabilityRelationship[] {
    const relationships: CapabilityRelationship[] = [];
    
    // Check for dependencies
    if (cap1.valueContribution.dependencies?.includes(cap2.id)) {
      relationships.push({
        from: cap1.id,
        to: cap2.id,
        type: RelationshipType.DEPENDS_ON,
        strength: this.assessDependencyStrength(cap1, cap2)
      });
    }
    
    // Check for shared resources
    const sharedPeople = this.findSharedElements(
      cap1.components.people.roles,
      cap2.components.people.roles
    );
    const sharedTech = this.findSharedElements(
      cap1.components.technology.tools,
      cap2.components.technology.tools
    );
    
    if (sharedPeople.length > 0 || sharedTech.length > 0) {
      relationships.push({
        from: cap1.id,
        to: cap2.id,
        type: RelationshipType.SHARES_RESOURCES,
        strength: (sharedPeople.length + sharedTech.length) / 10,
        details: { sharedPeople, sharedTech }
      });
    }
    
    // Check for enabling relationships
    const enablement = this.checkEnablement(cap1, cap2);
    if (enablement) {
      relationships.push(enablement);
    }
    
    return relationships;
  }
  
  visualize(): CapabilityMapVisualization {
    const nodes = Array.from(this.capabilities.values()).map(cap => ({
      id: cap.id,
      label: cap.name,
      area: cap.area,
      maturity: cap.maturity,
      size: this.calculateImportance(cap),
      color: this.getAreaColor(cap.area),
      position: this.calculatePosition(cap)
    }));
    
    const edges = this.relationships.map(rel => ({
      source: rel.from,
      target: rel.to,
      type: rel.type,
      strength: rel.strength,
      style: this.getEdgeStyle(rel.type)
    }));
    
    return {
      nodes,
      edges,
      layout: "force-directed",
      settings: {
        nodeSpacing: 50,
        edgeLength: 100,
        centerGravity: 0.1
      }
    };
  }
  
  private calculateImportance(capability: BusinessCapability): number {
    // Base importance on strategic value
    let importance = 0;
    
    switch (capability.valueContribution.strategicImportance) {
      case "CRITICAL": importance = 100; break;
      case "HIGH": importance = 75; break;
      case "MEDIUM": importance = 50; break;
      case "LOW": importance = 25; break;
    }
    
    // Adjust based on dependencies
    const dependentCount = this.relationships
      .filter(r => r.to === capability.id && r.type === RelationshipType.DEPENDS_ON)
      .length;
    
    importance += dependentCount * 5;
    
    // Cap at 100
    return Math.min(importance, 100);
  }
  
  generateReport(): CapabilityMapReport {
    const stats = {
      totalCapabilities: this.capabilities.size,
      byArea: this.groupByArea(),
      byMaturity: this.groupByMaturity(),
      averageMaturity: this.calculateAverageMaturity()
    };
    
    const insights = {
      bottlenecks: this.identifyBottlenecks(),
      improvementPriorities: this.prioritizeImprovements(),
      quickWins: this.identifyQuickWins(),
      strategicGaps: this.identifyStrategicGaps()
    };
    
    return {
      stats,
      insights,
      recommendations: this.generateRecommendations(insights)
    };
  }
}
```

### Capability Maturity Assessment

```typescript
export class CapabilityMaturityAssessment {
  private weights = {
    process: 0.3,
    people: 0.3,
    technology: 0.2,
    information: 0.2
  };
  
  assess(capability: BusinessCapability): MaturityAssessment {
    // Assess each dimension
    const dimensions = {
      process: this.assessProcessMaturity(capability.components.process),
      people: this.assessPeopleMaturity(capability.components.people),
      technology: this.assessTechnologyMaturity(capability.components.technology),
      information: this.assessInformationMaturity(capability.components.information)
    };
    
    // Calculate weighted average
    const weightedScore = Object.entries(dimensions).reduce(
      (sum, [key, score]) => sum + score * this.weights[key as keyof typeof this.weights],
      0
    );
    
    // Overall maturity (can't exceed lowest dimension by more than 1 level)
    const minDimension = Math.min(...Object.values(dimensions));
    const overallMaturity = Math.min(
      Math.round(weightedScore),
      minDimension + 1
    ) as MaturityLevel;
    
    // Generate improvement recommendations
    const improvements = this.identifyImprovements(
      dimensions,
      capability,
      overallMaturity
    );
    
    return {
      current: overallMaturity,
      target: capability.targetMaturity || MaturityLevel.MANAGED,
      dimensions,
      gaps: this.calculateGaps(dimensions, capability.targetMaturity),
      improvements,
      estimatedEffort: this.estimateImprovementEffort(improvements),
      roadmap: this.createMaturityRoadmap(capability, dimensions)
    };
  }
  
  private assessProcessMaturity(process: ProcessComponent): MaturityLevel {
    let score = MaturityLevel.INITIAL;
    
    // Level 2: Repeatable
    if (process.activities.length > 0 && process.standardized) {
      score = MaturityLevel.REPEATABLE;
    }
    
    // Level 3: Defined
    if (score >= MaturityLevel.REPEATABLE && 
        process.documentation && 
        process.processOwner) {
      score = MaturityLevel.DEFINED;
    }
    
    // Level 4: Managed
    if (score >= MaturityLevel.DEFINED && 
        process.metrics && 
        process.metrics.length >= 3) {
      score = MaturityLevel.MANAGED;
    }
    
    // Level 5: Optimized
    if (score >= MaturityLevel.MANAGED && 
        process.automationOpportunities && 
        process.maturityLevel >= MaturityLevel.MANAGED) {
      score = MaturityLevel.OPTIMIZED;
    }
    
    return score;
  }
  
  private assessPeopleMaturity(people: PeopleComponent): MaturityLevel {
    let score = MaturityLevel.INITIAL;
    
    // Level 2: Basic roles defined
    if (people.roles.length > 0 && people.count > 0) {
      score = MaturityLevel.REPEATABLE;
    }
    
    // Level 3: Skills and competencies defined
    if (score >= MaturityLevel.REPEATABLE && 
        people.skills.length >= people.roles.length &&
        people.organizationUnit) {
      score = MaturityLevel.DEFINED;
    }
    
    // Level 4: Competency levels tracked
    if (score >= MaturityLevel.DEFINED && 
        people.competencyLevels && 
        people.certifications) {
      score = MaturityLevel.MANAGED;
    }
    
    // Level 5: Continuous learning
    if (score >= MaturityLevel.MANAGED && 
        people.trainingNeeds && 
        people.trainingNeeds.length > 0) {
      score = MaturityLevel.OPTIMIZED;
    }
    
    return score;
  }
  
  private createMaturityRoadmap(
    capability: BusinessCapability,
    currentDimensions: any
  ): MaturityRoadmap {
    const target = capability.targetMaturity || MaturityLevel.MANAGED;
    const phases: RoadmapPhase[] = [];
    
    // Phase 1: Address lowest dimension
    const lowestDim = this.findLowestDimension(currentDimensions);
    if (lowestDim.score < target) {
      phases.push({
        name: `Strengthen ${lowestDim.dimension}`,
        duration: this.estimatePhaseDuration(lowestDim.score, lowestDim.score + 1),
        activities: this.getImprovementActivities(
          lowestDim.dimension,
          lowestDim.score,
          lowestDim.score + 1
        ),
        outcomes: [`${lowestDim.dimension} capability at level ${lowestDim.score + 1}`],
        investment: this.estimatePhaseInvestment(lowestDim.dimension, 1)
      });
    }
    
    // Phase 2: Balance all dimensions
    phases.push({
      name: "Balance capability dimensions",
      duration: "3-6 months",
      activities: this.getBalancingActivities(currentDimensions, target),
      outcomes: ["All dimensions within 1 level of each other"],
      investment: this.estimateBalancingInvestment(currentDimensions, target)
    });
    
    // Phase 3: Reach target maturity
    if (Math.max(...Object.values(currentDimensions)) < target) {
      phases.push({
        name: `Achieve ${MaturityLevel[target]} maturity`,
        duration: "6-12 months",
        activities: this.getTargetActivities(currentDimensions, target),
        outcomes: [`Capability operating at ${MaturityLevel[target]} level`],
        investment: this.estimateTargetInvestment(currentDimensions, target)
      });
    }
    
    return {
      phases,
      totalDuration: this.calculateTotalDuration(phases),
      totalInvestment: this.calculateTotalInvestment(phases),
      risks: this.identifyRoadmapRisks(phases),
      dependencies: this.identifyRoadmapDependencies(capability)
    };
  }
}
```

### Capability Value Measurement

```typescript
export class CapabilityValueMeasurement {
  private valueStreams: Map<string, ValueStream> = new Map();
  private capabilityMap: CapabilityMap;
  
  constructor(capabilityMap: CapabilityMap) {
    this.capabilityMap = capabilityMap;
  }
  
  measureValueContribution(
    capability: BusinessCapability,
    valueStreams: ValueStream[]
  ): ValueContributionScore {
    // Store value streams for reference
    valueStreams.forEach(vs => this.valueStreams.set(vs.id, vs));
    
    // Calculate different types of value contribution
    const directContribution = this.calculateDirectContribution(
      capability,
      valueStreams
    );
    
    const indirectContribution = this.calculateIndirectContribution(
      capability
    );
    
    const strategicImportance = this.assessStrategicImportance(
      capability
    );
    
    const riskMitigation = this.assessRiskMitigation(capability);
    
    // Weighted total score
    const totalScore = 
      directContribution * 0.4 +
      indirectContribution * 0.2 +
      strategicImportance * 0.3 +
      riskMitigation * 0.1;
    
    // Generate insights
    const insights = this.generateValueInsights(
      capability,
      { directContribution, indirectContribution, strategicImportance, riskMitigation }
    );
    
    return {
      total: totalScore,
      breakdown: {
        direct: directContribution,
        indirect: indirectContribution,
        strategic: strategicImportance,
        riskMitigation
      },
      insights,
      recommendations: this.generateValueRecommendations(capability, totalScore)
    };
  }
  
  private calculateDirectContribution(
    capability: BusinessCapability,
    valueStreams: ValueStream[]
  ): number {
    let contribution = 0;
    
    for (const stream of valueStreams) {
      // Check if capability directly supports value stream stages
      const supportedStages = stream.stages.filter(stage => 
        this.capabilitySupportsStage(capability, stage)
      );
      
      // Weight by stage criticality
      const stageContribution = supportedStages.reduce((sum, stage) => {
        return sum + (stage.criticalPath ? 10 : 5);
      }, 0);
      
      contribution += stageContribution;
    }
    
    // Normalize to 0-100 scale
    return Math.min(contribution, 100);
  }
  
  private calculateIndirectContribution(
    capability: BusinessCapability
  ): number {
    // Find all capabilities that depend on this one
    const dependentCapabilities = this.capabilityMap
      .getAllCapabilities()
      .filter(cap => cap.valueContribution.dependencies?.includes(capability.id));
    
    // Sum their strategic importance
    let indirectValue = 0;
    
    for (const dependent of dependentCapabilities) {
      switch (dependent.valueContribution.strategicImportance) {
        case "CRITICAL": indirectValue += 25; break;
        case "HIGH": indirectValue += 15; break;
        case "MEDIUM": indirectValue += 10; break;
        case "LOW": indirectValue += 5; break;
      }
    }
    
    return Math.min(indirectValue, 100);
  }
  
  private generateValueInsights(
    capability: BusinessCapability,
    scores: any
  ): string[] {
    const insights: string[] = [];
    
    // Direct contribution insights
    if (scores.directContribution > 80) {
      insights.push(`${capability.name} is a critical value driver directly supporting core value streams`);
    } else if (scores.directContribution < 30) {
      insights.push(`${capability.name} has limited direct value contribution - consider if it's truly needed`);
    }
    
    // Indirect contribution insights
    if (scores.indirectContribution > scores.directContribution) {
      insights.push(`${capability.name} is a key enabler - its value comes from supporting other capabilities`);
    }
    
    // Strategic insights
    if (scores.strategicImportance > 70) {
      insights.push(`${capability.name} is strategically critical for future competitiveness`);
    }
    
    // Risk insights
    if (scores.riskMitigation > 50) {
      insights.push(`${capability.name} provides significant risk mitigation value`);
    }
    
    // Combined insights
    const totalScore = scores.directContribution * 0.4 + 
                      scores.indirectContribution * 0.2 +
                      scores.strategicImportance * 0.3 +
                      scores.riskMitigation * 0.1;
                      
    if (totalScore > 75) {
      insights.push(`Prioritize investment in ${capability.name} - high overall value contribution`);
    } else if (totalScore < 25) {
      insights.push(`Consider consolidating or outsourcing ${capability.name} - low value contribution`);
    }
    
    return insights;
  }
}
```

### Capability Governance Implementation

```typescript
export class CapabilityGovernance {
  private organizationContext: OrganizationContext;
  
  constructor(context: OrganizationContext) {
    this.organizationContext = context;
  }
  
  establishOwnership(capability: BusinessCapability): CapabilityOwnership {
    // Define ownership criteria with weights
    const ownerCriteria = {
      businessKnowledge: 0.3,
      technicalUnderstanding: 0.2,
      leadershipSkills: 0.3,
      stakeholderRelationships: 0.2
    };
    
    // Identify potential owners
    const candidates = this.identifyCandidates(capability);
    
    // Score and select best owner
    const scoredCandidates = candidates.map(candidate => ({
      candidate,
      score: this.scoreCandidate(candidate, capability, ownerCriteria)
    }));
    
    const selectedOwner = scoredCandidates
      .sort((a, b) => b.score - a.score)[0]
      .candidate;
    
    // Design governance model
    const governanceModel = this.designGovernanceModel(capability);
    
    // Identify stakeholders
    const stakeholders = this.identifyStakeholders(capability);
    
    return {
      capability,
      owner: {
        role: selectedOwner.role,
        name: selectedOwner.name,
        responsibilities: this.defineOwnerResponsibilities(capability)
      },
      stakeholders,
      governanceModel
    };
  }
  
  private defineOwnerResponsibilities(
    capability: BusinessCapability
  ): string[] {
    const baseResponsibilities = [
      `Maintain and improve ${capability.name} capability`,
      "Define capability strategy and roadmap",
      "Ensure capability meets performance targets",
      "Manage capability budget and resources",
      "Report on capability health and value delivery"
    ];
    
    // Add specific responsibilities based on capability type
    const specificResponsibilities = this.getSpecificResponsibilities(capability);
    
    return [...baseResponsibilities, ...specificResponsibilities];
  }
  
  private designGovernanceModel(
    capability: BusinessCapability
  ): GovernanceModel {
    return {
      decisionRights: [
        {
          decision: "Capability investment > $100K",
          approver: "Capability Owner + CFO",
          consulted: ["Stakeholders", "Enterprise Architecture"]
        },
        {
          decision: "Process changes",
          approver: "Capability Owner",
          consulted: ["Process Participants", "Quality Team"]
        },
        {
          decision: "Technology selection",
          approver: "Capability Owner + CTO",
          consulted: ["IT Architecture", "Security Team"]
        },
        {
          decision: "Organizational changes",
          approver: "Capability Owner + HR Director",
          consulted: ["Affected Teams", "Union Representatives"]
        }
      ],
      
      performanceReview: {
        frequency: "quarterly",
        metrics: this.defineCapabilityMetrics(capability),
        reviewBoard: [
          "Capability Owner",
          "Business Unit Head",
          "Finance Representative",
          "Customer Representative"
        ],
        escalationPath: "Steering Committee → Executive Committee"
      },
      
      improvementProcess: {
        continuousImprovement: {
          method: "Kaizen",
          frequency: "monthly",
          participants: "Capability team members"
        },
        majorChanges: {
          method: "Business case + pilot",
          approvalRequired: true,
          minimumROI: 1.5
        }
      }
    };
  }
  
  monitorCapabilityHealth(ownership: CapabilityOwnership): HealthReport {
    const capability = ownership.capability;
    
    // Collect performance data
    const performanceMetrics = this.collectPerformanceMetrics(capability);
    
    // Assess health dimensions
    const healthDimensions = {
      performance: this.assessPerformance(performanceMetrics),
      maturity: this.assessMaturityProgress(capability),
      resources: this.assessResourceAdequacy(capability),
      risk: this.assessRiskExposure(capability),
      value: this.assessValueDelivery(capability)
    };
    
    // Calculate overall health score
    const overallHealth = this.calculateOverallHealth(healthDimensions);
    
    // Generate alerts if needed
    const alerts = this.generateHealthAlerts(healthDimensions);
    
    // Recommend actions
    const recommendations = this.generateHealthRecommendations(
      healthDimensions,
      capability
    );
    
    return {
      capability: capability.id,
      reportDate: new Date(),
      overallHealth,
      dimensions: healthDimensions,
      metrics: performanceMetrics,
      alerts,
      recommendations,
      nextReviewDate: this.calculateNextReviewDate(overallHealth)
    };
  }
}
```

## Utility Functions and Helpers

### Capability Analysis Utilities

```typescript
// Helper types
export interface CapabilityRequirement {
  activity: string;
  requiredSkills: string[];
  requiredProcesses: string[];
  requiredTechnology: string[];
  requiredInformation: string[];
  expectedOutcome: string;
}

export interface CapabilityGap {
  hasGap: boolean;
  gaps: {
    skillGaps: string[];
    processGaps: string[];
    technologyGaps: string[];
    informationGaps: string[];
  };
  improvements: CapabilityImprovement[];
}

export interface CapabilityRelationship {
  from: string;
  to: string;
  type: RelationshipType;
  strength: number; // 0-1 scale
  details?: any;
}

// Visualization types
export interface CapabilityMapVisualization {
  nodes: CapabilityNode[];
  edges: CapabilityEdge[];
  layout: string;
  settings: any;
}

export interface CapabilityNode {
  id: string;
  label: string;
  area: CapabilityArea;
  maturity: MaturityLevel;
  size: number;
  color: string;
  position?: { x: number; y: number };
}

export interface CapabilityEdge {
  source: string;
  target: string;
  type: RelationshipType;
  strength: number;
  style: any;
}

// Assessment types
export interface MaturityAssessment {
  current: MaturityLevel;
  target: MaturityLevel;
  dimensions: {
    process: MaturityLevel;
    people: MaturityLevel;
    technology: MaturityLevel;
    information: MaturityLevel;
  };
  gaps: any;
  improvements: CapabilityImprovement[];
  estimatedEffort: string;
  roadmap: MaturityRoadmap;
}

export interface ValueContributionScore {
  total: number;
  breakdown: {
    direct: number;
    indirect: number;
    strategic: number;
    riskMitigation: number;
  };
  insights: string[];
  recommendations: string[];
}

// Helper functions
export function createCapabilityId(area: CapabilityArea, sequence: number): string {
  const areaCode = area.substring(0, 2).toUpperCase();
  return `CAP-${areaCode}-${String(sequence).padStart(3, '0')}`;
}

export function calculateCapabilityComplexity(capability: BusinessCapability): number {
  const factors = {
    peopleCount: capability.components.people.count,
    processCount: capability.components.process.activities.length,
    toolCount: capability.components.technology.tools.length,
    integrationCount: capability.components.technology.integrations.length,
    dataSourceCount: capability.components.information.inputs.length
  };
  
  // Weighted complexity score
  return (
    factors.peopleCount * 0.2 +
    factors.processCount * 0.25 +
    factors.toolCount * 0.2 +
    factors.integrationCount * 0.25 +
    factors.dataSourceCount * 0.1
  );
}

export function identifyCapabilityBottlenecks(
  capabilities: BusinessCapability[],
  relationships: CapabilityRelationship[]
): string[] {
  const bottlenecks: string[] = [];
  
  for (const cap of capabilities) {
    // Count dependencies
    const dependencyCount = relationships
      .filter(r => r.to === cap.id && r.type === RelationshipType.DEPENDS_ON)
      .length;
    
    // Check maturity vs dependency count
    if (cap.maturity <= MaturityLevel.REPEATABLE && dependencyCount > 3) {
      bottlenecks.push(cap.id);
    }
    
    // Check strategic importance vs maturity mismatch
    if (cap.valueContribution.strategicImportance === "CRITICAL" && 
        cap.maturity < MaturityLevel.DEFINED) {
      bottlenecks.push(cap.id);
    }
  }
  
  return [...new Set(bottlenecks)]; // Remove duplicates
}
```

## Configuration and Constants

```typescript
// Capability configuration
export const CAPABILITY_CONFIG = {
  maturityWeights: {
    process: 0.3,
    people: 0.3,
    technology: 0.2,
    information: 0.2
  },
  
  valueContributionWeights: {
    direct: 0.4,
    indirect: 0.2,
    strategic: 0.3,
    riskMitigation: 0.1
  },
  
  improvementROIThresholds: {
    minimum: 1.2,
    target: 2.0,
    excellent: 3.0
  },
  
  governanceReviewFrequencies: {
    CRITICAL: "monthly",
    HIGH: "quarterly",
    MEDIUM: "semi-annually",
    LOW: "annually"
  }
};

// Industry-specific capability templates
export const INDUSTRY_CAPABILITY_TEMPLATES = {
  retail: [
    { name: "Customer Experience Management", area: CapabilityArea.CUSTOMER_ENGAGEMENT },
    { name: "Inventory Management", area: CapabilityArea.SUPPLY_CHAIN },
    { name: "Merchandising", area: CapabilityArea.PRODUCT_DEVELOPMENT },
    { name: "Store Operations", area: CapabilityArea.SERVICE_DELIVERY }
  ],
  
  manufacturing: [
    { name: "Production Planning", area: CapabilityArea.SERVICE_DELIVERY },
    { name: "Quality Assurance", area: CapabilityArea.SERVICE_DELIVERY },
    { name: "Supply Chain Management", area: CapabilityArea.SUPPLY_CHAIN },
    { name: "Equipment Maintenance", area: CapabilityArea.IT_DIGITAL }
  ],
  
  financial: [
    { name: "Risk Management", area: CapabilityArea.FINANCE_CONTROL },
    { name: "Compliance", area: CapabilityArea.FINANCE_CONTROL },
    { name: "Customer Onboarding", area: CapabilityArea.CUSTOMER_ENGAGEMENT },
    { name: "Transaction Processing", area: CapabilityArea.SERVICE_DELIVERY }
  ]
};
```

This implementation appendix provides the complete technical foundation for implementing capability definition as described in Chapter 14. The code is modular, extensible, and ready for use in real-world Parasol implementations.