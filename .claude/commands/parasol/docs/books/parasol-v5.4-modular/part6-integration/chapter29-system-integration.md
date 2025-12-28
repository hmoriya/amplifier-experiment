# 第29章　システム統合 ― 交響曲の指揮

## はじめに：オーケストラの調和

オーケストラでは、異なる楽器セクションが独自の音色と役割を持ちながらも、指揮者のタクトの下で一つの美しい音楽を奏でます。システム統合も同様に、独立したコンポーネントやサービスを調和させ、統一されたビジネス価値を提供する芸術です。

本章では、Parasol V5.4における複雑なシステムの統合戦略と実装パターンを解説します。

## システム統合の基礎

### 統合アーキテクチャパターン

```typescript
export interface IntegrationArchitecture {
  patterns: {
    pointToPoint: "直接的な1対1接続";
    hub: "中央集約型の統合";
    bus: "メッセージバスベースの統合";
    mesh: "サービスメッシュによる統合";
    eventDriven: "イベント駆動型統合";
  };
  
  layers: {
    presentation: "UI/UX層の統合";
    application: "ビジネスロジック層の統合";
    data: "データ層の統合";
    infrastructure: "インフラ層の統合";
  };
  
  challenges: {
    heterogeneity: "異種システムの統合";
    scalability: "スケーラビリティの確保";
    reliability: "信頼性の維持";
    security: "セキュリティの統一";
    monitoring: "統合的な監視";
  };
}

export class SystemIntegrationStrategy {
  // 統合戦略の設計
  designIntegrationStrategy(
    systems: System[],
    requirements: IntegrationRequirements
  ): IntegrationPlan {
    // システム間の依存関係分析
    const dependencies = this.analyzeDependencies(systems);
    
    // 統合ポイントの識別
    const integrationPoints = this.identifyIntegrationPoints(systems);
    
    // 適切なパターンの選択
    const patterns = this.selectPatterns(integrationPoints, requirements);
    
    return {
      architecture: this.designArchitecture(patterns),
      implementation: this.planImplementation(patterns),
      migration: this.planMigration(systems),
      validation: this.defineValidation(requirements)
    };
  }
  
  // 統合複雑度の評価
  assessIntegrationComplexity(
    systems: System[]
  ): ComplexityAssessment {
    const factors = {
      technicalDiversity: this.assessTechnicalDiversity(systems),
      dataHeterogeneity: this.assessDataHeterogeneity(systems),
      processAlignment: this.assessProcessAlignment(systems),
      organizationalImpact: this.assessOrganizationalImpact(systems)
    };
    
    return {
      score: this.calculateComplexityScore(factors),
      risks: this.identifyRisks(factors),
      recommendations: this.generateRecommendations(factors)
    };
  }
}
```

### イベント駆動アーキテクチャ

```typescript
export class EventDrivenIntegration {
  // イベントバスの実装
  implementEventBus(): EventBusArchitecture {
    return {
      broker: {
        type: "Apache Kafka",
        configuration: {
          clusters: ["kafka-1:9092", "kafka-2:9092", "kafka-3:9092"],
          replicationFactor: 3,
          minInSyncReplicas: 2,
          retentionMs: 604800000 // 7 days
        }
      },
      
      topics: {
        naming: {
          pattern: "{domain}.{entity}.{event-type}.v{version}",
          examples: [
            "order.order.created.v1",
            "inventory.stock.updated.v1",
            "payment.transaction.completed.v1"
          ]
        },
        
        partitioning: {
          strategy: "key-based",
          keys: ["customerId", "orderId", "productId"]
        },
        
        schemas: {
          format: "Avro",
          registry: "http://schema-registry:8081",
          evolution: "backward-compatible"
        }
      },
      
      producers: {
        configuration: {
          acks: "all",
          retries: 3,
          batchSize: 16384,
          lingerMs: 10,
          compressionType: "snappy"
        },
        
        errorHandling: {
          deadLetterQueue: true,
          retryPolicy: {
            maxRetries: 3,
            backoffMs: 1000,
            maxBackoffMs: 30000
          }
        }
      },
      
      consumers: {
        configuration: {
          groupIdPrefix: "parasol-v5",
          enableAutoCommit: false,
          isolationLevel: "read_committed",
          maxPollRecords: 500
        },
        
        patterns: {
          competingConsumer: "負荷分散処理",
          fanout: "ブロードキャスト配信",
          contentBasedRouting: "内容ベースルーティング"
        }
      }
    };
  }
  
  // イベントソーシング実装
  implementEventSourcing(): EventSourcingSystem {
    return {
      eventStore: {
        implementation: "EventStore",
        storage: {
          primary: "PostgreSQL",
          snapshots: "S3",
          projections: "MongoDB"
        }
      },
      
      aggregates: {
        Order: {
          events: [
            "OrderCreated",
            "ItemAdded",
            "ItemRemoved",
            "OrderConfirmed",
            "PaymentProcessed",
            "OrderShipped",
            "OrderDelivered"
          ],
          
          commandHandlers: `
            class OrderAggregate {
              private events: DomainEvent[] = [];
              private version: number = 0;
              
              static create(command: CreateOrderCommand): OrderAggregate {
                const aggregate = new OrderAggregate();
                
                // ビジネスルールの検証
                if (!command.customerId || command.items.length === 0) {
                  throw new InvalidCommandError("Invalid order data");
                }
                
                // イベントの生成
                aggregate.apply(new OrderCreatedEvent({
                  orderId: command.orderId,
                  customerId: command.customerId,
                  items: command.items,
                  timestamp: new Date()
                }));
                
                return aggregate;
              }
              
              addItem(command: AddItemCommand): void {
                // 不変条件の検証
                if (this.status !== "CREATED") {
                  throw new InvalidStateError("Cannot add items to confirmed order");
                }
                
                this.apply(new ItemAddedEvent({
                  orderId: this.id,
                  item: command.item,
                  timestamp: new Date()
                }));
              }
              
              private apply(event: DomainEvent): void {
                this.events.push(event);
                this.version++;
                this.updateState(event);
              }
            }
          `
        }
      },
      
      projections: {
        OrderSummary: {
          source: ["OrderCreated", "OrderConfirmed", "OrderShipped"],
          target: "MongoDB.orderSummaries",
          transform: `
            function projectOrderSummary(event: DomainEvent): void {
              switch (event.type) {
                case "OrderCreated":
                  db.orderSummaries.insert({
                    orderId: event.data.orderId,
                    customerId: event.data.customerId,
                    status: "CREATED",
                    total: calculateTotal(event.data.items)
                  });
                  break;
                  
                case "OrderConfirmed":
                  db.orderSummaries.update(
                    { orderId: event.data.orderId },
                    { $set: { status: "CONFIRMED" } }
                  );
                  break;
              }
            }
          `
        }
      }
    };
  }
}
```

## API統合戦略

### API Gateway実装

```typescript
export class APIGatewayImplementation {
  // ゲートウェイ設計
  designGateway(): GatewayArchitecture {
    return {
      routing: {
        rules: [
          {
            path: "/api/v1/orders/*",
            target: "http://order-service:8080",
            methods: ["GET", "POST", "PUT", "DELETE"]
          },
          {
            path: "/api/v1/products/*",
            target: "http://product-service:8080",
            methods: ["GET"]
          },
          {
            path: "/api/v1/users/*",
            target: "http://user-service:8080",
            methods: ["GET", "POST", "PUT"]
          }
        ],
        
        loadBalancing: {
          algorithm: "round-robin",
          healthCheck: {
            path: "/health",
            interval: 10,
            timeout: 5,
            unhealthyThreshold: 3
          }
        }
      },
      
      security: {
        authentication: {
          type: "JWT",
          issuer: "https://auth.parasol.com",
          audience: "parasol-api",
          algorithms: ["RS256"]
        },
        
        authorization: {
          type: "RBAC",
          policies: [
            {
              path: "/api/v1/orders/*",
              roles: ["customer", "admin"],
              scopes: ["orders:read", "orders:write"]
            }
          ]
        },
        
        rateLimiting: {
          default: {
            requests: 100,
            window: "1m",
            keyBy: "ip"
          },
          
          authenticated: {
            requests: 1000,
            window: "1m",
            keyBy: "userId"
          }
        }
      },
      
      transformation: {
        request: {
          headers: {
            add: {
              "X-Request-ID": "${requestId}",
              "X-Forwarded-For": "${clientIp}"
            },
            remove: ["Authorization"]
          },
          
          body: {
            jsonPath: {
              "$.password": "[REDACTED]",
              "$.creditCard": "[MASKED]"
            }
          }
        },
        
        response: {
          headers: {
            add: {
              "X-Response-Time": "${responseTime}",
              "Cache-Control": "no-store"
            }
          },
          
          body: {
            envelope: {
              success: true,
              data: "${body}",
              metadata: {
                timestamp: "${timestamp}",
                version: "v1"
              }
            }
          }
        }
      },
      
      caching: {
        strategy: "Redis",
        rules: [
          {
            path: "/api/v1/products/*",
            ttl: 300,
            keyPattern: "${method}:${path}:${queryString}"
          }
        ]
      }
    };
  }
  
  // GraphQL Federation
  implementGraphQLFederation(): GraphQLFederationConfig {
    return {
      gateway: {
        server: "Apollo Gateway",
        services: [
          {
            name: "users",
            url: "http://users-graphql:4001/graphql"
          },
          {
            name: "products",
            url: "http://products-graphql:4002/graphql"
          },
          {
            name: "orders",
            url: "http://orders-graphql:4003/graphql"
          }
        ]
      },
      
      schemas: {
        users: `
          type User @key(fields: "id") {
            id: ID!
            email: String!
            name: String!
            orders: [Order!]!
          }
          
          extend type Query {
            user(id: ID!): User
            users(filter: UserFilter): [User!]!
          }
        `,
        
        products: `
          type Product @key(fields: "id") {
            id: ID!
            name: String!
            price: Float!
            inventory: Int!
          }
          
          extend type Query {
            product(id: ID!): Product
            products(category: String): [Product!]!
          }
        `,
        
        orders: `
          type Order @key(fields: "id") {
            id: ID!
            user: User!
            items: [OrderItem!]!
            total: Float!
            status: OrderStatus!
          }
          
          type OrderItem {
            product: Product!
            quantity: Int!
            price: Float!
          }
          
          extend type User @key(fields: "id") {
            id: ID! @external
            orders: [Order!]!
          }
        `
      }
    };
  }
}
```

## データ統合パターン

### ETL/ELTプロセス

```typescript
export class DataIntegration {
  // ETLパイプライン実装
  implementETLPipeline(): ETLPipeline {
    return {
      extraction: {
        sources: [
          {
            type: "database",
            name: "legacy_orders",
            connection: {
              type: "oracle",
              host: "legacy-db.internal",
              query: `
                SELECT 
                  order_id,
                  customer_id,
                  order_date,
                  total_amount,
                  status
                FROM orders
                WHERE last_modified > :last_sync_time
              `
            }
          },
          {
            type: "api",
            name: "external_inventory",
            connection: {
              endpoint: "https://supplier.api/inventory",
              auth: "bearer-token",
              pagination: "cursor-based"
            }
          },
          {
            type: "file",
            name: "customer_data",
            connection: {
              protocol: "sftp",
              host: "ftp.partner.com",
              pattern: "customers_*.csv"
            }
          }
        ],
        
        scheduling: {
          frequency: "0 */4 * * *", // 4時間ごと
          retryPolicy: {
            maxAttempts: 3,
            backoff: "exponential"
          }
        }
      },
      
      transformation: {
        pipeline: [
          {
            stage: "cleansing",
            operations: [
              { type: "trim", fields: ["*"] },
              { type: "nullToEmpty", fields: ["description"] },
              { type: "standardizeDate", fields: ["order_date"], format: "ISO8601" }
            ]
          },
          {
            stage: "enrichment",
            operations: [
              {
                type: "lookup",
                source: "customer_master",
                join: "customer_id",
                fields: ["customer_name", "customer_segment"]
              },
              {
                type: "calculate",
                expressions: {
                  "order_value_tier": "CASE WHEN total > 1000 THEN 'HIGH' ELSE 'NORMAL' END"
                }
              }
            ]
          },
          {
            stage: "aggregation",
            operations: [
              {
                type: "groupBy",
                keys: ["customer_id", "order_month"],
                aggregates: {
                  "total_orders": "COUNT(*)",
                  "total_value": "SUM(total_amount)",
                  "avg_order_value": "AVG(total_amount)"
                }
              }
            ]
          }
        ],
        
        errorHandling: {
          strategy: "partial-failure",
          errorTable: "etl_errors",
          alerting: {
            threshold: 0.05, // 5%エラー率でアラート
            channels: ["email", "slack"]
          }
        }
      },
      
      loading: {
        targets: [
          {
            type: "dataWarehouse",
            destination: "Snowflake",
            schema: "analytics",
            table: "fact_orders",
            loadStrategy: "merge",
            mergeKeys: ["order_id"]
          },
          {
            type: "cache",
            destination: "Redis",
            keyPattern: "order:{order_id}",
            ttl: 86400
          }
        ],
        
        optimization: {
          batchSize: 10000,
          parallelism: 4,
          compression: "gzip"
        }
      }
    };
  }
  
  // リアルタイムデータ統合
  implementStreamingIntegration(): StreamingPipeline {
    return {
      ingestion: {
        sources: [
          {
            type: "kafka",
            topics: ["orders", "inventory", "payments"],
            consumerGroup: "analytics-pipeline"
          },
          {
            type: "kinesis",
            streams: ["clickstream-data"],
            startingPosition: "LATEST"
          }
        ]
      },
      
      processing: {
        framework: "Apache Flink",
        
        jobs: [
          {
            name: "OrderEnrichment",
            sql: `
              SELECT 
                o.order_id,
                o.customer_id,
                o.order_time,
                c.customer_name,
                c.customer_segment,
                p.product_name,
                p.category,
                o.quantity * p.price as line_total
              FROM orders o
              JOIN customers FOR SYSTEM_TIME AS OF o.order_time c
                ON o.customer_id = c.customer_id
              JOIN products FOR SYSTEM_TIME AS OF o.order_time p
                ON o.product_id = p.product_id
            `,
            
            watermark: "order_time - INTERVAL '5' MINUTE",
            
            windows: [
              {
                type: "tumbling",
                size: "1 HOUR",
                aggregation: "SUM(line_total) as hourly_revenue"
              },
              {
                type: "sliding",
                size: "24 HOURS",
                slide: "1 HOUR",
                aggregation: "COUNT(DISTINCT customer_id) as unique_customers"
              }
            ]
          }
        ],
        
        stateManagement: {
          backend: "RocksDB",
          checkpointing: {
            interval: "1m",
            minPause: "30s",
            timeout: "10m"
          }
        }
      },
      
      sinks: [
        {
          type: "elasticsearch",
          index: "orders-enriched",
          mapping: {
            dynamic: false,
            properties: {
              order_time: { type: "date" },
              customer_segment: { type: "keyword" },
              line_total: { type: "float" }
            }
          }
        },
        {
          type: "s3",
          bucket: "data-lake",
          format: "parquet",
          partitioning: ["year", "month", "day"]
        }
      ]
    };
  }
}
```

## マイクロサービス統合

### サービスメッシュ実装

```typescript
export class ServiceMeshIntegration {
  // Istio設定
  configureServiceMesh(): ServiceMeshConfig {
    return {
      trafficManagement: {
        virtualServices: [
          {
            name: "order-service",
            hosts: ["order-service"],
            http: [
              {
                match: [{ headers: { "x-version": { exact: "v2" } } }],
                route: [{ destination: { host: "order-service", subset: "v2" } }]
              },
              {
                route: [
                  { destination: { host: "order-service", subset: "v1" }, weight: 90 },
                  { destination: { host: "order-service", subset: "v2" }, weight: 10 }
                ]
              }
            ]
          }
        ],
        
        destinationRules: [
          {
            name: "order-service",
            host: "order-service",
            trafficPolicy: {
              connectionPool: {
                tcp: { maxConnections: 100 },
                http: { 
                  http1MaxPendingRequests: 50,
                  http2MaxRequests: 100
                }
              },
              outlierDetection: {
                consecutiveErrors: 5,
                interval: "30s",
                baseEjectionTime: "30s"
              }
            },
            subsets: [
              { name: "v1", labels: { version: "v1" } },
              { name: "v2", labels: { version: "v2" } }
            ]
          }
        ]
      },
      
      security: {
        peerAuthentication: {
          default: {
            mtls: { mode: "STRICT" }
          }
        },
        
        authorizationPolicies: [
          {
            name: "order-service-authz",
            namespace: "production",
            selector: { matchLabels: { app: "order-service" } },
            rules: [
              {
                from: [{ source: { principals: ["cluster.local/ns/production/sa/frontend"] } }],
                to: [{ operation: { methods: ["GET"], paths: ["/api/orders/*"] } }]
              }
            ]
          }
        ]
      },
      
      observability: {
        telemetry: {
          metrics: [
            {
              providers: [{ name: "prometheus" }],
              dimensions: {
                request_protocol: "request.protocol",
                response_code: "response.code"
              }
            }
          ],
          
          tracing: [
            {
              providers: [{ name: "jaeger" }],
              randomSamplingPercentage: 1.0
            }
          ]
        }
      }
    };
  }
  
  // サービス間通信パターン
  implementCommunicationPatterns(): CommunicationPatterns {
    return {
      synchronous: {
        restful: {
          client: `
            class OrderServiceClient {
              private readonly httpClient: HttpClient;
              private readonly circuitBreaker: CircuitBreaker;
              
              async getOrder(orderId: string): Promise<Order> {
                return this.circuitBreaker.execute(async () => {
                  const response = await this.httpClient.get(
                    \`\${this.baseUrl}/orders/\${orderId}\`,
                    {
                      headers: {
                        'X-Request-ID': generateRequestId(),
                        'X-B3-TraceId': getTraceId()
                      },
                      timeout: 5000
                    }
                  );
                  
                  if (!response.ok) {
                    throw new ServiceError(\`Failed to get order: \${response.status}\`);
                  }
                  
                  return response.json();
                });
              }
            }
          `,
          
          resilience: {
            circuitBreaker: {
              errorThreshold: 50,
              resetTimeout: 30000,
              monitoringPeriod: 10000
            },
            
            retry: {
              maxAttempts: 3,
              delay: 1000,
              maxDelay: 10000,
              backoffMultiplier: 2
            },
            
            timeout: {
              request: 5000,
              connection: 2000
            }
          }
        },
        
        grpc: {
          proto: `
            syntax = "proto3";
            
            service OrderService {
              rpc GetOrder(GetOrderRequest) returns (Order);
              rpc ListOrders(ListOrdersRequest) returns (stream Order);
              rpc CreateOrder(CreateOrderRequest) returns (Order);
            }
            
            message Order {
              string id = 1;
              string customer_id = 2;
              repeated OrderItem items = 3;
              double total = 4;
              OrderStatus status = 5;
            }
          `,
          
          interceptors: [
            "authentication",
            "logging",
            "metrics",
            "tracing"
          ]
        }
      },
      
      asynchronous: {
        messaging: {
          patterns: {
            requestReply: {
              implementation: "Correlation ID based",
              timeout: 30000
            },
            
            publishSubscribe: {
              topics: ["order-events", "inventory-events"],
              durability: "persistent"
            },
            
            saga: {
              orchestration: "Centralized",
              compensations: "Automatic rollback"
            }
          }
        }
      }
    };
  }
}
```

## 統合テストとバリデーション

### 統合テスト戦略

```typescript
export class IntegrationTesting {
  // コントラクトテスト
  implementContractTesting(): ContractTestStrategy {
    return {
      consumerDrivenContracts: {
        framework: "Pact",
        
        consumerTests: `
          describe('Order Service Consumer', () => {
            it('should fetch order details', async () => {
              await provider.addInteraction({
                state: 'an order exists',
                uponReceiving: 'a request for order details',
                withRequest: {
                  method: 'GET',
                  path: '/orders/123',
                  headers: { Accept: 'application/json' }
                },
                willRespondWith: {
                  status: 200,
                  headers: { 'Content-Type': 'application/json' },
                  body: {
                    id: '123',
                    customerId: 'customer-456',
                    total: 99.99,
                    status: 'CONFIRMED'
                  }
                }
              });
              
              const order = await orderClient.getOrder('123');
              expect(order.id).toBe('123');
            });
          });
        `,
        
        providerVerification: `
          describe('Order Service Provider', () => {
            it('should verify consumer contracts', async () => {
              const opts = {
                provider: 'OrderService',
                providerBaseUrl: 'http://localhost:8080',
                pactUrls: ['./pacts/frontend-orderservice.json'],
                stateHandlers: {
                  'an order exists': async () => {
                    await seedDatabase({ orderId: '123' });
                  }
                }
              };
              
              await new Verifier(opts).verifyProvider();
            });
          });
        `
      },
      
      integrationScenarios: [
        {
          name: "完全な注文フロー",
          steps: [
            "ユーザーが商品をカートに追加",
            "在庫サービスが在庫を確認",
            "注文サービスが注文を作成",
            "決済サービスが支払いを処理",
            "通知サービスが確認メールを送信"
          ],
          
          validations: [
            "各サービスのレスポンスが期待通り",
            "データの整合性が保たれる",
            "エラー時の補償トランザクション"
          ]
        }
      ]
    };
  }
  
  // エンドツーエンドテスト
  implementE2ETesting(): E2ETestStrategy {
    return {
      framework: "Cypress",
      
      setup: {
        environment: "staging",
        dataPreparation: {
          method: "API seeding",
          cleanup: "After each test"
        }
      },
      
      scenarios: `
        describe('Order Creation Flow', () => {
          beforeEach(() => {
            cy.task('seedTestData');
            cy.login('test@example.com', 'password');
          });
          
          it('should create order successfully', () => {
            // 商品選択
            cy.visit('/products');
            cy.get('[data-testid="product-123"]').click();
            cy.get('[data-testid="add-to-cart"]').click();
            
            // カート確認
            cy.visit('/cart');
            cy.get('[data-testid="cart-items"]').should('have.length', 1);
            cy.get('[data-testid="checkout"]').click();
            
            // 支払い情報
            cy.get('[data-testid="payment-method"]').select('credit-card');
            cy.fillPaymentDetails(testPaymentData);
            
            // 注文確認
            cy.get('[data-testid="place-order"]').click();
            
            // 検証
            cy.url().should('include', '/order-confirmation');
            cy.get('[data-testid="order-id"]').should('exist');
            
            // バックエンドの状態確認
            cy.task('verifyOrderInDatabase').then((order) => {
              expect(order.status).to.equal('CONFIRMED');
              expect(order.paymentStatus).to.equal('COMPLETED');
            });
          });
        });
      `,
      
      monitoring: {
        synthetic: {
          frequency: "5m",
          locations: ["us-east-1", "eu-west-1", "ap-northeast-1"],
          alerting: {
            consecutiveFailures: 3,
            channels: ["slack", "pagerduty"]
          }
        }
      }
    };
  }
}
```

## 統合の運用と監視

### 統合監視ダッシュボード

```typescript
export class IntegrationMonitoring {
  // 監視メトリクス定義
  defineMonitoringMetrics(): MonitoringConfiguration {
    return {
      businessMetrics: {
        orderFlow: {
          metrics: [
            "orders_created_per_minute",
            "order_completion_rate",
            "average_order_processing_time",
            "payment_success_rate"
          ],
          
          dashboards: {
            executive: {
              widgets: [
                {
                  type: "timeseries",
                  title: "Revenue Trend",
                  query: "sum(order_total) by (hour)"
                },
                {
                  type: "gauge",
                  title: "System Health",
                  query: "avg(service_health_score)"
                }
              ]
            }
          }
        }
      },
      
      technicalMetrics: {
        integration: {
          latency: {
            p50: { threshold: 100, unit: "ms" },
            p95: { threshold: 500, unit: "ms" },
            p99: { threshold: 1000, unit: "ms" }
          },
          
          errorRates: {
            overall: { threshold: 0.1, unit: "%" },
            perService: { threshold: 1.0, unit: "%" },
            perEndpoint: { threshold: 5.0, unit: "%" }
          },
          
          throughput: {
            requests: { min: 1000, unit: "rpm" },
            messages: { min: 5000, unit: "mpm" },
            data: { min: 100, unit: "mbps" }
          }
        }
      },
      
      alerting: {
        rules: [
          {
            name: "Integration Failure",
            condition: "error_rate > 5% for 5m",
            severity: "critical",
            actions: ["page", "slack", "create_incident"]
          },
          {
            name: "Latency Degradation",
            condition: "p95_latency > 1s for 10m",
            severity: "warning",
            actions: ["slack", "email"]
          }
        ]
      }
    };
  }
  
  // 分散トレーシング
  implementDistributedTracing(): TracingConfiguration {
    return {
      instrumentation: {
        automatic: {
          frameworks: ["express", "grpc", "kafka"],
          databases: ["postgresql", "mongodb", "redis"],
          httpClients: ["axios", "fetch"]
        },
        
        manual: `
          class TracingMiddleware {
            trace(operationName: string, tags?: Tags) {
              return async (req: Request, res: Response, next: NextFunction) => {
                const span = tracer.startSpan(operationName, {
                  childOf: extractSpanContext(req.headers),
                  tags: {
                    'http.method': req.method,
                    'http.url': req.url,
                    'user.id': req.user?.id,
                    ...tags
                  }
                });
                
                // スパンをリクエストコンテキストに追加
                req.span = span;
                
                // レスポンスの監視
                const originalSend = res.send;
                res.send = function(data) {
                  span.setTag('http.status_code', res.statusCode);
                  span.finish();
                  return originalSend.call(this, data);
                };
                
                // エラーハンドリング
                const originalNext = next;
                next = function(error?: any) {
                  if (error) {
                    span.setTag('error', true);
                    span.log({ event: 'error', message: error.message });
                  }
                  return originalNext(error);
                };
                
                next();
              };
            }
          }
        `
      },
      
      sampling: {
        strategy: "adaptive",
        rules: [
          { service: "frontend", operation: "GET /health", sample: 0.01 },
          { service: "*", operation: "*", sample: 0.1 },
          { tag: "error=true", sample: 1.0 }
        ]
      },
      
      storage: {
        backend: "Elasticsearch",
        retention: "7d",
        indexing: {
          shards: 5,
          replicas: 1
        }
      }
    };
  }
}
```

## まとめ

システム統合は、個別のコンポーネントを調和させ、ビジネス価値を創出する重要なプロセスです。Parasol V5.4における成功の鍵：

1. **適切なパターンの選択** - コンテキストに応じた統合アプローチ
2. **イベント駆動の活用** - 疎結合で拡張可能なシステム
3. **堅牢なAPI設計** - 明確なコントラクトと進化可能性
4. **包括的なテスト** - 統合の信頼性確保
5. **継続的な監視** - 問題の早期発見と対応

適切に設計された統合アーキテクチャは、システムの柔軟性と信頼性を高め、ビジネスの成長を支えます。

### 次章への架橋

システム統合の基本的なアプローチを理解しました。第30章では、外部システムとの連携について、より具体的な実装パターンを探求します。

---

## 演習問題

1. マイクロサービスアーキテクチャにおいて、注文処理フローを実装する際の統合戦略を設計してください。必要なサービス、通信パターン、エラーハンドリングを含めてください。

2. レガシーシステムから新システムへのデータ移行において、ゼロダウンタイムを実現するETLパイプラインを設計してください。

3. 以下のシナリオに対して、適切な統合パターンを選択し、その理由を説明してください：
   - リアルタイムの在庫同期
   - バッチ処理による売上レポート生成
   - 複数の決済プロバイダーとの統合