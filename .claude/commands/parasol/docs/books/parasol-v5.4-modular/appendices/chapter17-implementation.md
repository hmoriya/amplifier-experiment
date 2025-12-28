# 付録：第17章　アーキテクチャパターンの実装詳細

## パターンの体系的定義

```typescript
export enum ArchitecturePatternCategory {
  // 構造パターン
  MONOLITHIC = "モノリシック",
  LAYERED = "レイヤード",
  MICROSERVICES = "マイクロサービス",
  SERVICE_ORIENTED = "サービス指向",
  
  // データパターン
  SHARED_DATABASE = "共有データベース",
  DATABASE_PER_SERVICE = "サービス毎データベース",
  EVENT_SOURCING = "イベントソーシング",
  CQRS = "コマンドクエリ責任分離",
  
  // 通信パターン
  REQUEST_RESPONSE = "要求応答",
  MESSAGING = "メッセージング",
  EVENT_DRIVEN = "イベント駆動",
  STREAMING = "ストリーミング",
  
  // デプロイメントパターン
  SINGLE_DEPLOYMENT = "単一デプロイメント",
  DISTRIBUTED = "分散デプロイメント",
  SERVERLESS = "サーバーレス",
  EDGE_COMPUTING = "エッジコンピューティング"
}

export interface ArchitecturePattern {
  name: string;
  category: ArchitecturePatternCategory;
  
  // パターンの特性
  characteristics: {
    scalability: ScalabilityProfile;
    complexity: ComplexityLevel;
    maintainability: MaintainabilityScore;
    testability: TestabilityScore;
    performance: PerformanceProfile;
  };
  
  // 適用条件
  applicability: {
    problemTypes: ProblemType[];
    teamSize: TeamSizeRange;
    systemScale: SystemScale;
    domainComplexity: ComplexityLevel;
  };
  
  // トレードオフ
  tradeoffs: {
    benefits: string[];
    liabilities: string[];
    risks: Risk[];
  };
}
```

## パターン選択基準の実装

```typescript
export class PatternSelectionCriteria {
  evaluatePattern(
    pattern: ArchitecturePattern,
    context: ProjectContext
  ): PatternFitScore {
    const scores = {
      // 価値への適合性
      valueAlignment: this.assessValueAlignment(
        pattern,
        context.valueStreams
      ),
      
      // ケイパビリティとの整合性
      capabilityFit: this.assessCapabilityFit(
        pattern,
        context.capabilities
      ),
      
      // 制約との適合性
      constraintCompliance: this.assessConstraintCompliance(
        pattern,
        context.constraints
      ),
      
      // 組織との適合性
      organizationalFit: this.assessOrganizationalFit(
        pattern,
        context.organization
      ),
      
      // 技術的適合性
      technicalFit: this.assessTechnicalFit(
        pattern,
        context.technology
      )
    };
    
    const weightedScore = this.calculateWeightedScore(scores, context);
    const risks = this.identifyRisks(pattern, context);
    
    return {
      pattern,
      scores,
      totalScore: weightedScore,
      risks,
      recommendation: this.generateRecommendation(weightedScore, risks)
    };
  }
}
```

## マイクロサービスパターンの詳細実装

```typescript
export class MicroservicesPattern implements ArchitecturePattern {
  name = "Microservices Architecture";
  category = ArchitecturePatternCategory.MICROSERVICES;
  
  characteristics = {
    scalability: {
      horizontal: "excellent",
      vertical: "good",
      elasticity: "excellent"
    },
    complexity: ComplexityLevel.HIGH,
    maintainability: 0.8,
    testability: 0.9,
    performance: {
      latency: "variable",
      throughput: "high",
      overhead: "significant"
    }
  };
  
  // 実装ガイドライン
  implementationGuidelines = {
    serviceDesign: {
      principles: [
        "Single Responsibility",
        "Autonomous Teams",
        "Decentralized Data Management",
        "Design for Failure"
      ],
      
      serviceBoundaries: (capabilities: BusinessCapability[]) => {
        return capabilities.map(cap => ({
          serviceName: this.deriveServiceName(cap),
          responsibilities: cap.operations,
          dataOwnership: this.identifyOwnedData(cap),
          apis: this.designServiceAPI(cap)
        }));
      },
      
      communicationPatterns: {
        synchronous: {
          when: ["Low latency required", "Simple request-response"],
          implementation: ["REST", "gRPC"]
        },
        asynchronous: {
          when: ["Decoupling required", "Event-driven flow"],
          implementation: ["Message Queue", "Event Streaming"]
        }
      }
    },
    
    dataManagement: {
      strategy: "Database per Service",
      consistency: "Eventual Consistency",
      
      patterns: {
        saga: {
          when: "Distributed transactions needed",
          implementation: "Choreography or Orchestration"
        },
        cqrs: {
          when: "Read/Write workloads differ significantly",
          implementation: "Separate read and write models"
        },
        eventSourcing: {
          when: "Audit trail required",
          implementation: "Event store with projections"
        }
      }
    }
  };
  
  // ECサイトへの適用例
  applyToECommerce(context: ECommerceContext): ServiceArchitecture {
    return {
      services: [
        {
          name: "ProductCatalog",
          responsibilities: ["Product management", "Search", "Categories"],
          technology: ["Node.js", "Elasticsearch", "PostgreSQL"],
          api: {
            rest: ["/products", "/categories", "/search"],
            events: ["ProductCreated", "ProductUpdated", "PriceChanged"]
          }
        },
        {
          name: "ShoppingCart",
          responsibilities: ["Cart management", "Session handling"],
          technology: ["Go", "Redis"],
          api: {
            rest: ["/cart", "/cart/items"],
            events: ["ItemAdded", "ItemRemoved", "CartCheckedOut"]
          }
        },
        {
          name: "OrderManagement",
          responsibilities: ["Order processing", "Order tracking"],
          technology: ["Java Spring", "PostgreSQL"],
          api: {
            rest: ["/orders", "/orders/{id}/status"],
            events: ["OrderPlaced", "OrderShipped", "OrderDelivered"]
          }
        },
        {
          name: "PaymentService",
          responsibilities: ["Payment processing", "Refunds"],
          technology: ["Java Spring", "Oracle DB"],
          api: {
            rest: ["/payments", "/refunds"],
            events: ["PaymentProcessed", "PaymentFailed", "RefundIssued"]
          }
        }
      ],
      
      infrastructure: {
        apiGateway: "Kong",
        serviceMesh: "Istio",
        messageQueue: "RabbitMQ",
        monitoring: ["Prometheus", "Grafana", "Jaeger"]
      }
    };
  }
}
```

## イベント駆動アーキテクチャの実装

```typescript
export class EventDrivenPattern implements ArchitecturePattern {
  name = "Event-Driven Architecture";
  category = ArchitecturePatternCategory.EVENT_DRIVEN;
  
  // イベントの設計
  designEvents(capabilities: BusinessCapability[]): EventCatalog {
    const events: DomainEvent[] = [];
    
    for (const capability of capabilities) {
      const capabilityEvents = this.identifyEvents(capability);
      events.push(...capabilityEvents);
    }
    
    return {
      events,
      eventFlows: this.designEventFlows(events),
      eventStore: this.designEventStore(events),
      projections: this.designProjections(events)
    };
  }
  
  private identifyEvents(
    capability: BusinessCapability
  ): DomainEvent[] {
    const events: DomainEvent[] = [];
    
    // 状態変化からイベントを導出
    for (const operation of capability.operations) {
      const stateChanges = this.analyzeStateChanges(operation);
      
      for (const change of stateChanges) {
        events.push({
          name: this.deriveEventName(change),
          source: capability.name,
          payload: this.definePayload(change),
          metadata: {
            version: "1.0",
            schema: this.generateSchema(change)
          }
        });
      }
    }
    
    return events;
  }
  
  // イベントストアの実装
  implementEventStore(): EventStoreImplementation {
    return {
      storage: {
        engine: "EventStore DB",
        partitioning: "By aggregate ID",
        retention: "Infinite for event sourcing"
      },
      
      api: {
        append: async (streamId: string, events: Event[]) => {
          // イベントの検証
          for (const event of events) {
            await this.validateEvent(event);
          }
          
          // 楽観的並行性制御
          const expectedVersion = await this.getStreamVersion(streamId);
          
          // イベントの永続化
          await this.persistEvents(streamId, events, expectedVersion);
          
          // プロジェクションの更新
          await this.updateProjections(streamId, events);
          
          // イベントの発行
          await this.publishEvents(events);
        },
        
        read: async (streamId: string, fromVersion?: number) => {
          return this.readEventStream(streamId, fromVersion);
        }
      },
      
      projections: {
        continuous: [
          {
            name: "CurrentState",
            query: "SELECT * FROM events WHERE ...",
            destination: "ReadModel"
          }
        ],
        
        oneTime: [
          {
            name: "DataMigration",
            query: "SELECT * FROM events WHERE timestamp < ...",
            destination: "MigrationTable"
          }
        ]
      }
    };
  }
}
```

## サーバーレスパターンの実装

```typescript
export class ServerlessPattern implements ArchitecturePattern {
  name = "Serverless Architecture";
  category = ArchitecturePatternCategory.SERVERLESS;
  
  // 関数の設計
  designFunctions(
    capabilities: BusinessCapability[]
  ): ServerlessDesign {
    const functions: ServerlessFunction[] = [];
    
    for (const capability of capabilities) {
      const capabilityFunctions = this.decomposeToFunctions(capability);
      functions.push(...capabilityFunctions);
    }
    
    return {
      functions,
      triggers: this.designTriggers(functions),
      orchestration: this.designOrchestration(functions),
      dataFlow: this.designDataFlow(functions)
    };
  }
  
  // 実装例：注文処理
  implementOrderProcessing(): ServerlessFunctions {
    return {
      functions: [
        {
          name: "validateOrder",
          runtime: "nodejs18.x",
          memory: 256,
          timeout: 30,
          trigger: "API Gateway POST /orders",
          handler: async (event: APIGatewayEvent) => {
            const order = JSON.parse(event.body);
            
            // 検証ロジック
            const validation = await this.validateOrder(order);
            
            if (validation.isValid) {
              // 次の関数をトリガー
              await this.invokeFunction("processPayment", order);
              
              return {
                statusCode: 202,
                body: JSON.stringify({ orderId: order.id })
              };
            } else {
              return {
                statusCode: 400,
                body: JSON.stringify({ errors: validation.errors })
              };
            }
          }
        },
        
        {
          name: "processPayment",
          runtime: "nodejs18.x",
          memory: 512,
          timeout: 60,
          trigger: "Invocation from validateOrder",
          handler: async (order: Order) => {
            try {
              const payment = await this.processPayment(order);
              
              // イベントの発行
              await this.publishEvent("PaymentProcessed", {
                orderId: order.id,
                amount: payment.amount,
                transactionId: payment.transactionId
              });
              
            } catch (error) {
              await this.publishEvent("PaymentFailed", {
                orderId: order.id,
                reason: error.message
              });
              
              throw error;
            }
          }
        }
      ],
      
      orchestration: {
        type: "StepFunctions",
        definition: {
          startAt: "ValidateOrder",
          states: {
            ValidateOrder: {
              type: "Task",
              resource: "arn:aws:lambda:validateOrder",
              next: "ProcessPayment"
            },
            ProcessPayment: {
              type: "Task",
              resource: "arn:aws:lambda:processPayment",
              next: "UpdateInventory",
              catch: [{
                errorEquals: ["PaymentError"],
                next: "HandlePaymentFailure"
              }]
            }
          }
        }
      }
    };
  }
}
```

## ハイブリッドアーキテクチャの設計

```typescript
export class HybridArchitectureDesigner {
  combinePatterns(
    patterns: ArchitecturePattern[],
    context: ProjectContext
  ): HybridArchitecture {
    // パターンの相性分析
    const compatibility = this.analyzeCompatibility(patterns);
    
    // 統合ポイントの設計
    const integrationPoints = this.designIntegrationPoints(
      patterns,
      context
    );
    
    // 境界の定義
    const boundaries = this.defineBoundaries(patterns, context);
    
    return {
      patterns,
      compatibility,
      integrationPoints,
      boundaries,
      implementation: this.createImplementationPlan(patterns, boundaries)
    };
  }
  
  // 実例：マイクロサービス + イベント駆動 + サーバーレス
  createModernECommerceArchitecture(): HybridArchitecture {
    const patterns = [
      new MicroservicesPattern(),
      new EventDrivenPattern(),
      new ServerlessPattern()
    ];
    
    return {
      zones: [
        {
          name: "Core Services",
          pattern: "Microservices",
          services: ["Product", "Order", "Customer", "Inventory"],
          rationale: "Complex business logic requiring team autonomy"
        },
        {
          name: "Integration Layer",
          pattern: "Event-Driven",
          components: ["Event Bus", "Event Store", "Projections"],
          rationale: "Loose coupling between services"
        },
        {
          name: "Edge Functions",
          pattern: "Serverless",
          functions: ["ImageResize", "EmailNotification", "DataExport"],
          rationale: "Variable load, stateless operations"
        }
      ],
      
      interactions: [
        {
          from: "Core Services",
          to: "Integration Layer",
          mechanism: "Publish domain events"
        },
        {
          from: "Integration Layer",
          to: "Edge Functions",
          mechanism: "Trigger on specific events"
        }
      ]
    };
  }
}
```

## アーキテクチャ決定記録（ADR）

```typescript
export interface ArchitectureDecisionRecord {
  id: string;
  title: string;
  status: "proposed" | "accepted" | "deprecated" | "superseded";
  context: string;
  decision: string;
  consequences: {
    positive: string[];
    negative: string[];
    neutral: string[];
  };
  alternatives: {
    option: string;
    prosAndCons: string;
    rejectionReason: string;
  }[];
}

// ADR例：マイクロサービス採用
const adr001: ArchitectureDecisionRecord = {
  id: "ADR-001",
  title: "マイクロサービスアーキテクチャの採用",
  status: "accepted",
  context: `
    - 複数の開発チームが並行して作業
    - 異なるビジネスドメインの統合
    - スケーラビリティ要求の多様性
    - 技術スタックの自由度の必要性
  `,
  decision: `
    コアビジネスロジックにマイクロサービスアーキテクチャを採用する。
    各サービスは単一のビジネスケイパビリティを担当し、
    独自のデータストアを持つ。通信は非同期メッセージングを基本とする。
  `,
  consequences: {
    positive: [
      "チームの独立性向上",
      "技術選択の自由度",
      "個別スケーリング可能",
      "障害の局所化"
    ],
    negative: [
      "運用の複雑性増大",
      "分散トランザクションの課題",
      "ネットワーク遅延",
      "開発環境の複雑化"
    ],
    neutral: [
      "監視・ロギングインフラの刷新が必要",
      "DevOps文化の醸成が必須"
    ]
  },
  alternatives: [
    {
      option: "モジュラーモノリス",
      prosAndCons: "シンプルだが、スケーラビリティに限界",
      rejectionReason: "チーム間の依存性が高くなりすぎる"
    },
    {
      option: "サービス指向アーキテクチャ（SOA）",
      prosAndCons: "実績はあるが、ESBがボトルネックになる",
      rejectionReason: "中央集権的な統合レイヤーを避けたい"
    }
  ]
};
```

## アーキテクチャ進化戦略の実装

```typescript
export class ArchitectureEvolution {
  planEvolution(
    current: ArchitecturePattern,
    target: ArchitecturePattern,
    constraints: Constraint[]
  ): EvolutionRoadmap {
    // 現状分析
    const currentState = this.analyzeCurrentArchitecture(current);
    
    // ギャップ分析
    const gaps = this.identifyGaps(currentState, target);
    
    // 移行ステップの設計
    const steps = this.designMigrationSteps(gaps, constraints);
    
    // リスク評価
    const risks = this.assessMigrationRisks(steps);
    
    return {
      phases: [
        {
          name: "Foundation",
          duration: "3 months",
          activities: [
            "Set up CI/CD pipeline",
            "Establish monitoring",
            "Create first microservice"
          ],
          successCriteria: ["Pipeline operational", "Monitoring coverage > 80%"]
        },
        {
          name: "Decomposition",
          duration: "6 months",
          activities: [
            "Extract core services",
            "Implement service mesh",
            "Migrate critical features"
          ],
          successCriteria: ["3+ services in production", "< 2% error rate"]
        },
        {
          name: "Optimization",
          duration: "3 months",
          activities: [
            "Performance tuning",
            "Cost optimization",
            "Complete migration"
          ],
          successCriteria: ["All services migrated", "Cost targets met"]
        }
      ],
      
      rollbackPlan: this.createRollbackPlan(steps),
      communicationPlan: this.createCommunicationPlan(steps)
    };
  }
  
  // Strangler Figパターンの実装
  implementStranglerFig(
    legacySystem: System,
    newArchitecture: ArchitecturePattern
  ): StranglerImplementation {
    return {
      facade: {
        description: "API Gateway routing to legacy and new services",
        implementation: {
          tool: "Kong/Nginx",
          rules: [
            {
              path: "/api/v2/*",
              target: "new-services",
              percentage: 100
            },
            {
              path: "/api/v1/*",
              target: "legacy",
              percentage: 100,
              deprecation: "2024-12-31"
            }
          ]
        }
      },
      
      migrationOrder: [
        {
          component: "User Authentication",
          reason: "Stateless and well-defined boundaries",
          effort: "2 sprints"
        },
        {
          component: "Product Catalog",
          reason: "Read-heavy, easy to replicate",
          effort: "3 sprints"
        },
        {
          component: "Order Processing",
          reason: "Core business logic, requires careful migration",
          effort: "5 sprints"
        }
      ],
      
      dataSync: {
        strategy: "Event-based sync",
        implementation: "CDC (Change Data Capture) with Debezium"
      }
    };
  }
}
```

## 金融サービスのアーキテクチャ選択例

```typescript
class FinancialServicesArchitecture {
  selectArchitecture(context: FinancialContext): ArchitectureDecision {
    const requirements = {
      regulatory: ["PCI-DSS", "SOX", "GDPR"],
      performance: {
        transactionLatency: "<100ms",
        throughput: "10K TPS",
        availability: "99.99%"
      },
      security: {
        encryption: "end-to-end",
        auditTrail: "complete",
        accessControl: "role-based"
      }
    };
    
    // パターン評価
    const evaluation = {
      microservices: {
        score: 0.85,
        fit: "High for service isolation and compliance",
        concerns: ["Distributed transaction complexity"]
      },
      eventSourcing: {
        score: 0.90,
        fit: "Excellent for audit trail and compliance",
        concerns: ["Learning curve", "Storage costs"]
      },
      cqrs: {
        score: 0.80,
        fit: "Good for read/write optimization",
        concerns: ["Eventual consistency handling"]
      }
    };
    
    // 推奨アーキテクチャ
    return {
      primary: "Event Sourcing + CQRS",
      secondary: "Microservices for service boundaries",
      rationale: `
        Event Sourcing provides immutable audit trail required for compliance.
        CQRS optimizes for different read/write patterns in trading vs reporting.
        Microservices provide necessary isolation for regulatory boundaries.
      `,
      implementation: this.createImplementationPlan(evaluation)
    };
  }
}
```