# Appendix A: ZIGZAG Process Implementation Details

This appendix contains detailed code implementations and technical patterns for the ZIGZAG process discussed in Chapter 13.

## Core Type Definitions

```typescript
// Problem Space Types
interface ProblemSpace {
  understanding: string[];
  requirements: Requirement[];
  constraints: Constraint[];
  assumptions: Assumption[];
  stakeholders: Stakeholder[];
}

interface Requirement {
  id: string;
  description: string;
  priority: 'must' | 'should' | 'could' | 'wont';
  rationale: string;
  source: string; // stakeholder or document
  stability: number; // 0-1, how stable is this requirement
}

interface Constraint {
  id: string;
  type: 'business' | 'technical' | 'regulatory' | 'resource';
  description: string;
  impact: 'high' | 'medium' | 'low';
  negotiable: boolean;
}

// Solution Space Types
interface SolutionSpace {
  options: SolutionOption[];
  decisions: Decision[];
  tradeoffs: Tradeoff[];
  risks: Risk[];
  prototypes: Prototype[];
}

interface SolutionOption {
  id: string;
  name: string;
  description: string;
  feasibility: FeasibilityAssessment;
  alignment: ProblemAlignment;
}

interface FeasibilityAssessment {
  technical: number; // 0-1
  resource: number; // 0-1
  schedule: number; // 0-1
  overall: number; // calculated
  notes: string[];
}
```

## ZIGZAG Iteration Manager

```typescript
export class ZigzagIterationManager {
  private iterations: Iteration[] = [];
  private convergenceThreshold = 0.8;
  
  async executeIteration(
    problemSpace: ProblemSpace,
    solutionSpace: SolutionSpace
  ): Promise<IterationResult> {
    const iteration = await this.createIteration();
    
    // 1. Problem space analysis
    const problemInsights = await this.analyzeProblem(problemSpace);
    iteration.record('problem_analysis', problemInsights);
    
    // 2. Solution space exploration
    const solutionOptions = await this.exploreSolutions(
      solutionSpace,
      problemInsights
    );
    iteration.record('solution_exploration', solutionOptions);
    
    // 3. Constraint discovery
    const constraints = await this.identifyConstraints(solutionOptions);
    iteration.record('constraints_discovered', constraints);
    
    // 4. Problem refinement based on solution insights
    const refinedProblem = await this.refineProblem(
      problemSpace,
      constraints
    );
    iteration.record('problem_refinement', refinedProblem);
    
    // 5. Solution adjustment based on refined problem
    const adjustedSolution = await this.adjustSolution(
      solutionOptions,
      refinedProblem
    );
    iteration.record('solution_adjustment', adjustedSolution);
    
    // 6. Convergence calculation
    const convergenceScore = this.calculateConvergence(
      refinedProblem,
      adjustedSolution
    );
    
    // 7. Determine next steps
    const nextSteps = this.determineNextSteps(
      convergenceScore,
      refinedProblem,
      adjustedSolution
    );
    
    this.iterations.push(iteration);
    
    return {
      iteration,
      problem: refinedProblem,
      solution: adjustedSolution,
      convergence: convergenceScore,
      nextSteps
    };
  }
  
  private calculateConvergence(
    problem: ProblemSpace,
    solution: SolutionSpace
  ): ConvergenceScore {
    const factors = {
      requirementCoverage: this.assessRequirementCoverage(problem, solution),
      requirementStability: this.assessRequirementStability(problem),
      solutionConfidence: this.assessSolutionConfidence(solution),
      riskMitigation: this.assessRiskMitigation(solution),
      stakeholderAlignment: this.assessStakeholderAlignment(problem),
    };
    
    const weights = {
      requirementCoverage: 0.25,
      requirementStability: 0.20,
      solutionConfidence: 0.20,
      riskMitigation: 0.20,
      stakeholderAlignment: 0.15
    };
    
    const overallScore = Object.entries(factors).reduce(
      (sum, [key, value]) => sum + value * weights[key],
      0
    );
    
    return {
      overall: overallScore,
      factors,
      isConverged: overallScore >= this.convergenceThreshold
    };
  }
  
  private assessRequirementCoverage(
    problem: ProblemSpace,
    solution: SolutionSpace
  ): number {
    const requirements = problem.requirements.filter(r => r.priority === 'must');
    const covered = requirements.filter(req => 
      solution.decisions.some(dec => 
        dec.addresses.includes(req.id)
      )
    );
    
    return covered.length / requirements.length;
  }
  
  private determineNextSteps(
    convergence: ConvergenceScore,
    problem: ProblemSpace,
    solution: SolutionSpace
  ): NextSteps {
    if (convergence.isConverged) {
      return {
        phase: 'validation',
        actions: [
          'Build proof-of-concept for highest risk areas',
          'Validate with key stakeholders',
          'Prepare for implementation planning'
        ]
      };
    }
    
    const weakestFactor = this.findWeakestFactor(convergence.factors);
    
    switch (weakestFactor) {
      case 'requirementCoverage':
        return {
          phase: 'problem_space_exploration',
          actions: [
            'Identify uncovered requirements',
            'Explore alternative solution approaches',
            'Consider requirement prioritization changes'
          ]
        };
      
      case 'requirementStability':
        return {
          phase: 'problem_space_refinement',
          actions: [
            'Clarify unstable requirements with stakeholders',
            'Identify root causes of instability',
            'Consider incremental delivery approach'
          ]
        };
      
      case 'solutionConfidence':
        return {
          phase: 'solution_space_exploration',
          actions: [
            'Build technical prototypes',
            'Conduct architectural reviews',
            'Research unfamiliar technologies'
          ]
        };
      
      default:
        return {
          phase: 'balanced_iteration',
          actions: [
            'Continue problem-solution dialogue',
            'Focus on specific risk areas',
            'Increase stakeholder engagement'
          ]
        };
    }
  }
}
```

## Problem-Solution Dialogue Facilitator

```typescript
export class ProblemSolutionDialogue {
  private insights: Insight[] = [];
  
  async facilitateDialogue(
    problemExpert: ProblemExpert,
    solutionExpert: SolutionExpert,
    timeboxMinutes: number
  ): Promise<DialogueOutcome> {
    const startTime = Date.now();
    const endTime = startTime + timeboxMinutes * 60 * 1000;
    
    const session: DialogueSession = {
      id: generateId(),
      startTime: new Date(startTime),
      participants: [problemExpert.id, solutionExpert.id],
      exchanges: []
    };
    
    while (Date.now() < endTime) {
      // Problem expert shares understanding
      const problemStatement = await problemExpert.articulate();
      session.exchanges.push({
        type: 'problem_statement',
        content: problemStatement,
        timestamp: new Date()
      });
      
      // Solution expert responds with possibilities
      const solutionResponse = await solutionExpert.propose(problemStatement);
      session.exchanges.push({
        type: 'solution_proposal',
        content: solutionResponse,
        timestamp: new Date()
      });
      
      // Extract insights from exchange
      const exchangeInsights = await this.extractInsights(
        problemStatement,
        solutionResponse
      );
      
      this.insights.push(...exchangeInsights);
      
      // Check for breakthrough or impasse
      if (await this.hasBreakthrough(exchangeInsights)) {
        break;
      }
      
      if (await this.hasImpasse(session.exchanges)) {
        await this.introduceNewPerspective(session);
      }
    }
    
    return {
      session,
      insights: this.insights,
      convergenceIndicators: this.analyzeConvergence(session),
      recommendations: this.generateRecommendations(session, this.insights)
    };
  }
  
  private async extractInsights(
    problem: ProblemStatement,
    solution: SolutionResponse
  ): Promise<Insight[]> {
    const insights: Insight[] = [];
    
    // Check for revealed constraints
    if (solution.constraints) {
      insights.push(...solution.constraints.map(c => ({
        type: 'constraint_discovered',
        description: c.description,
        impact: c.impact,
        source: 'solution_analysis'
      })));
    }
    
    // Check for new possibilities
    if (solution.enablers) {
      insights.push(...solution.enablers.map(e => ({
        type: 'possibility_identified',
        description: e.description,
        value: e.potentialValue,
        source: 'solution_exploration'
      })));
    }
    
    // Check for assumption challenges
    const challengedAssumptions = this.findChallengedAssumptions(
      problem.assumptions,
      solution.feedback
    );
    
    insights.push(...challengedAssumptions.map(a => ({
      type: 'assumption_challenged',
      description: `Assumption "${a.original}" may not hold because ${a.reason}`,
      impact: 'high',
      source: 'dialogue'
    })));
    
    return insights;
  }
}
```

## EC Site Recommendation Example Implementation

```typescript
// Complete implementation of the EC site recommendation service
export class RecommendationService {
  private collaborativeFilter: CollaborativeFilter;
  private contentBasedFilter: ContentBasedFilter;
  private ruleEngine: RuleEngine;
  private cache: RecommendationCache;
  private logger: Logger;
  private metrics: MetricsCollector;
  
  constructor(dependencies: RecommendationDependencies) {
    this.collaborativeFilter = dependencies.collaborativeFilter;
    this.contentBasedFilter = dependencies.contentBasedFilter;
    this.ruleEngine = dependencies.ruleEngine;
    this.cache = dependencies.cache;
    this.logger = dependencies.logger;
    this.metrics = dependencies.metrics;
  }
  
  async getRecommendations(
    userId: string,
    context: RecommendationContext
  ): Promise<ProductRecommendations> {
    const startTime = Date.now();
    
    try {
      // Check cache first (performance requirement: <100ms)
      const cached = await this.cache.get(userId, context);
      if (cached && !cached.isExpired()) {
        this.metrics.increment('cache_hit');
        return cached.recommendations;
      }
      
      // Get user profile with privacy compliance
      const userProfile = await this.getUserProfile(userId);
      
      // Select recommendation strategy based on user data
      let recommendations: Product[];
      
      if (userProfile.hasEnoughHistory()) {
        // Use collaborative filtering for users with history
        recommendations = await this.collaborativeFilter.recommend(
          userId,
          context,
          {
            limit: 20,
            diversityFactor: 0.3,
            timeDecay: true
          }
        );
        this.metrics.increment('collaborative_filter_used');
      } else {
        // Use content-based filtering for new users
        recommendations = await this.contentBasedFilter.recommend(
          userProfile,
          context,
          {
            limit: 20,
            usePopularityBoost: true,
            categoryWeights: this.calculateCategoryWeights(userProfile)
          }
        );
        this.metrics.increment('content_filter_used');
      }
      
      // Apply business rules
      recommendations = await this.ruleEngine.filter(recommendations, {
        excludeOutOfStock: true,
        respectUserPreferences: userProfile.preferences,
        ensurePriceRange: context.priceRange,
        enforceAgeRestrictions: userProfile.ageGroup,
        promoteHighMarginItems: context.includePromotions
      });
      
      // Generate explanations for transparency
      const explanations = await this.generateExplanations(
        recommendations,
        userProfile,
        context
      );
      
      // Build final result
      const result: ProductRecommendations = {
        products: recommendations.slice(0, context.limit || 10),
        explanations,
        generatedAt: new Date(),
        strategyUsed: userProfile.hasEnoughHistory() ? 
          'collaborative' : 'content-based',
        debugInfo: context.includeDebugInfo ? {
          processingTimeMs: Date.now() - startTime,
          cacheStatus: 'miss',
          filtersApplied: ['business_rules'],
          candidateCount: recommendations.length
        } : undefined
      };
      
      // Cache the result
      await this.cache.set(userId, context, result, {
        ttl: this.calculateCacheTTL(context)
      });
      
      // Record metrics
      this.metrics.histogram(
        'recommendation_latency',
        Date.now() - startTime
      );
      
      return result;
      
    } catch (error) {
      this.logger.error('Recommendation failed', {
        userId,
        context,
        error
      });
      
      // Fallback to rule-based recommendations
      return this.getFallbackRecommendations(context);
    }
  }
  
  private async generateExplanations(
    products: Product[],
    userProfile: UserProfile,
    context: RecommendationContext
  ): Promise<Map<string, string>> {
    const explanations = new Map<string, string>();
    
    for (const product of products) {
      const reasons = [];
      
      // Check purchase history
      if (userProfile.purchaseHistory.hasRelatedProduct(product)) {
        reasons.push('あなたが以前購入した商品に関連しています');
      }
      
      // Check browsing behavior
      if (userProfile.browsingHistory.showsInterestIn(product.category)) {
        reasons.push(`${product.category}カテゴリの商品をよくご覧になっています`);
      }
      
      // Check popularity
      if (product.popularityScore > 0.8) {
        reasons.push('多くのお客様に人気の商品です');
      }
      
      // Check promotions
      if (product.hasPromotion && context.includePromotions) {
        reasons.push(`${product.promotionDescription}`);
      }
      
      explanations.set(
        product.id,
        reasons.length > 0 ? reasons.join('。') : '関連性の高い商品です'
      );
    }
    
    return explanations;
  }
  
  private calculateCacheTTL(context: RecommendationContext): number {
    // Shorter TTL for contexts that change frequently
    if (context.includePromotions) {
      return 5 * 60 * 1000; // 5 minutes
    }
    
    if (context.isPersonalized) {
      return 30 * 60 * 1000; // 30 minutes
    }
    
    return 60 * 60 * 1000; // 1 hour for generic recommendations
  }
}
```

## ZIGZAG Metrics and Tracking

```typescript
export class ZigzagMetricsCollector {
  private storage: MetricsStorage;
  
  async collectIterationMetrics(iteration: Iteration): Promise<IterationMetrics> {
    const metrics: IterationMetrics = {
      iterationNumber: iteration.number,
      duration: iteration.endTime.getTime() - iteration.startTime.getTime(),
      
      problemSpaceMetrics: {
        requirementsAdded: this.countNewRequirements(iteration),
        requirementsModified: this.countModifiedRequirements(iteration),
        requirementsRemoved: this.countRemovedRequirements(iteration),
        stabilityScore: this.calculateStabilityScore(iteration)
      },
      
      solutionSpaceMetrics: {
        optionsExplored: iteration.solutionOptions.length,
        decisionsMAde: iteration.decisions.length,
        prototypesBuilt: iteration.prototypes.length,
        confidenceScore: this.calculateConfidenceScore(iteration)
      },
      
      convergenceMetrics: {
        overallProgress: this.calculateProgress(iteration),
        blockers: this.identifyBlockers(iteration),
        breakthroughs: this.identifyBreakthroughs(iteration)
      }
    };
    
    await this.storage.save(metrics);
    return metrics;
  }
  
  async generateProgressReport(
    projectId: string,
    startDate: Date,
    endDate: Date
  ): Promise<ZigzagProgressReport> {
    const iterations = await this.storage.getIterations(
      projectId,
      startDate,
      endDate
    );
    
    return {
      summary: {
        totalIterations: iterations.length,
        averageDuration: this.calculateAverageDuration(iterations),
        convergenceTrend: this.calculateConvergenceTrend(iterations),
        estimatedIterationsRemaining: this.estimateRemaining(iterations)
      },
      
      insights: {
        mostStableRequirements: this.findStableRequirements(iterations),
        mostVolatileRequirements: this.findVolatileRequirements(iterations),
        keyDecisions: this.extractKeyDecisions(iterations),
        majorRisks: this.aggregateRisks(iterations)
      },
      
      recommendations: this.generateRecommendations(iterations)
    };
  }
}
```

## Integration Patterns

### ZIGZAG with Agile/Scrum

```typescript
export class AgileSprint {
  private zigzagManager: ZigzagIterationManager;
  
  async planSprint(
    productBacklog: ProductBacklogItem[],
    teamCapacity: number,
    sprintNumber: number
  ): Promise<SprintPlan> {
    // Sprint planning is a mini-ZIGZAG process
    const sprintGoal = await this.defineSprintGoal(productBacklog);
    
    // Problem space: What should we achieve?
    const userStories = await this.selectUserStories(
      productBacklog,
      sprintGoal
    );
    
    // Solution space: How will we build it?
    const technicalTasks = await this.breakdownToTasks(userStories);
    
    // Capacity check forces re-evaluation
    const capacityAnalysis = await this.analyzeCapacity(
      technicalTasks,
      teamCapacity
    );
    
    if (capacityAnalysis.overCapacity) {
      // ZIG back to problem space
      const refined = await this.refineScope(
        userStories,
        capacityAnalysis.availableCapacity
      );
      
      // ZAG back to solution space
      technicalTasks = await this.breakdownToTasks(refined.stories);
    }
    
    return {
      goal: sprintGoal,
      stories: userStories,
      tasks: technicalTasks,
      risks: await this.identifySprintRisks(technicalTasks),
      metrics: this.defineSprintMetrics(sprintGoal)
    };
  }
}
```

### ZIGZAG with Event Storming

```typescript
export class EventStormingFacilitator {
  async facilitate(
    domain: string,
    participants: Participant[]
  ): Promise<EventStormingOutcome> {
    const session = new EventStormingSession(domain, participants);
    
    // Phase 1: Chaotic exploration (Problem Space)
    const events = await session.brainstormEvents();
    
    // Phase 2: Enforce timeline (Solution Space constraint)
    const timeline = await session.orderEvents(events);
    
    // Phase 3: Find pivotal events (Problem Space pattern)
    const pivotalEvents = await session.identifyPivotalEvents(timeline);
    
    // Phase 4: Define aggregates (Solution Space structure)
    const aggregates = await session.defineAggregates(pivotalEvents);
    
    // Phase 5: Identify bounded contexts (Problem/Solution boundary)
    const boundedContexts = await session.identifyBoundedContexts(
      aggregates,
      timeline
    );
    
    // ZIGZAG refinement
    const refinedModel = await this.zigzagRefinement(
      boundedContexts,
      aggregates,
      timeline
    );
    
    return {
      events: timeline,
      aggregates: refinedModel.aggregates,
      boundedContexts: refinedModel.boundedContexts,
      insights: session.getInsights()
    };
  }
  
  private async zigzagRefinement(
    contexts: BoundedContext[],
    aggregates: Aggregate[],
    timeline: Event[]
  ): Promise<RefinedModel> {
    // Check if aggregates properly handle all events
    const unmanagedEvents = this.findUnmanagedEvents(timeline, aggregates);
    
    if (unmanagedEvents.length > 0) {
      // Refine aggregates or contexts
      const refined = await this.refineModel(
        contexts,
        aggregates,
        unmanagedEvents
      );
      
      return this.zigzagRefinement(
        refined.contexts,
        refined.aggregates,
        timeline
      );
    }
    
    return { contexts, aggregates };
  }
}
```

## Decision Tracking System

```typescript
export class DecisionTracker {
  private decisions: Map<string, DecisionRecord> = new Map();
  private subscriptions: DecisionSubscription[] = [];
  
  recordDecision(decision: {
    id: string;
    type: 'problem' | 'solution' | 'tradeoff';
    description: string;
    rationale: string;
    alternatives: Alternative[];
    impacts: Impact[];
    iteration: number;
    confidence: number;
  }): void {
    const record: DecisionRecord = {
      ...decision,
      timestamp: new Date(),
      status: 'active',
      revisitTriggers: this.identifyRevisitTriggers(decision),
      relatedDecisions: this.findRelatedDecisions(decision)
    };
    
    this.decisions.set(decision.id, record);
    this.checkConsistency();
    this.notifySubscribers(record);
  }
  
  private identifyRevisitTriggers(decision: Decision): Trigger[] {
    const triggers: Trigger[] = [];
    
    // Time-based triggers
    if (decision.confidence < 0.7) {
      triggers.push({
        type: 'time',
        condition: '2 weeks',
        reason: 'Low confidence decision should be revisited'
      });
    }
    
    // Event-based triggers
    if (decision.assumptions.length > 0) {
      triggers.push({
        type: 'assumption_invalidated',
        condition: decision.assumptions,
        reason: 'Decision based on assumptions that may change'
      });
    }
    
    // Metric-based triggers
    if (decision.impacts.some(i => i.measurable)) {
      triggers.push({
        type: 'metric_threshold',
        condition: decision.impacts.filter(i => i.measurable),
        reason: 'Decision impact can be measured and evaluated'
      });
    }
    
    return triggers;
  }
  
  async evaluateDecisions(): Promise<DecisionEvaluation[]> {
    const evaluations: DecisionEvaluation[] = [];
    
    for (const [id, decision] of this.decisions) {
      if (decision.status !== 'active') continue;
      
      const triggered = await this.checkTriggers(decision);
      if (triggered.length > 0) {
        evaluations.push({
          decision,
          triggers: triggered,
          recommendation: this.recommendAction(decision, triggered)
        });
      }
    }
    
    return evaluations;
  }
}
```

## Usage Examples and Patterns

See Chapter 13 for conceptual understanding and practical application guidance.

### Quick Reference: Common ZIGZAG Patterns

1. **Requirements Discovery Pattern**
   - Start with high-level business goal
   - Explore technical options
   - Discover constraints
   - Refine requirements based on constraints
   - Iterate until stable

2. **Architecture Evolution Pattern**
   - Begin with ideal architecture
   - Map to business capabilities
   - Identify misalignments
   - Adjust both architecture and capability definitions
   - Converge on practical design

3. **Risk Mitigation Pattern**
   - List known risks
   - Prototype highest risk areas
   - Discover unknown risks
   - Adjust approach based on findings
   - Repeat until acceptable risk level

### Anti-Pattern Reference

1. **Thrashing**: Too many iterations without progress
   - Solution: Set iteration limits, force decisions

2. **Premature Convergence**: Stopping too early
   - Solution: Minimum 3 alternatives rule

3. **Analysis Paralysis**: Over-analyzing without action
   - Solution: Time-box analysis, prototype early

### Metrics to Track

- Iterations to convergence
- Requirement stability over iterations
- Decision confidence trends
- Risk discovery rate
- Stakeholder alignment scores