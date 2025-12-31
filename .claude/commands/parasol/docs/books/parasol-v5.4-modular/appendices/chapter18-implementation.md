# 付録 18：境界づけられたコンテキストの実装詳細

この付録では、第18章で紹介した境界づけられたコンテキストの概念を実際に実装する際の詳細なコード例、パターン、およびツールについて解説します。

## コンテキストの基本定義

```typescript
export interface BoundedContext {
  // 識別情報
  id: string;
  name: string;
  description: string;
  
  // コンテキストの境界
  boundary: {
    // 含まれる概念
    concepts: DomainConcept[];
    // 責任範囲
    responsibilities: string[];
    // 言語（ユビキタス言語）
    ubiquitousLanguage: LanguageDefinition;
  };
  
  // 実装の詳細
  implementation: {
    // 担当チーム
    team: Team;
    // 技術スタック
    technology: TechnologyStack;
    // データストア
    dataStore: DataStore;
  };
  
  // 他コンテキストとの関係
  relationships: ContextRelationship[];
  
  // 品質属性
  qualities: {
    autonomy: AutonomyLevel;
    cohesion: CohesionScore;
    coupling: CouplingScore;
  };
}

// ドメイン概念
export interface DomainConcept {
  name: string;
  definition: string;
  attributes: ConceptAttribute[];
  behaviors: ConceptBehavior[];
  invariants: BusinessRule[];
}
```

## 境界発見プロセスの実装

```typescript
export class BoundaryDiscovery {
  async discoverBoundaries(
    domain: Domain,
    capabilities: BusinessCapability[]
  ): Promise<BoundedContext[]> {
    // 1. 言語分析による境界の発見
    const linguisticBoundaries = await this.analyzeLinguisticBoundaries(
      domain
    );
    
    // 2. データの一貫性境界
    const consistencyBoundaries = await this.analyzeConsistencyBoundaries(
      domain
    );
    
    // 3. 組織境界
    const organizationalBoundaries = await this.analyzeOrganizationalBoundaries(
      domain
    );
    
    // 4. 変更の頻度による境界
    const volatilityBoundaries = await this.analyzeVolatilityBoundaries(
      domain
    );
    
    // 5. 統合と最適化
    return this.synthesizeBoundaries(
      linguisticBoundaries,
      consistencyBoundaries,
      organizationalBoundaries,
      volatilityBoundaries
    );
  }
  
  private async analyzeLinguisticBoundaries(
    domain: Domain
  ): Promise<LinguisticBoundary[]> {
    const boundaries: LinguisticBoundary[] = [];
    
    // 用語の意味が変わる場所を特定
    const terms = await this.extractDomainTerms(domain);
    
    for (const term of terms) {
      const contexts = await this.findContextsUsingTerm(term);
      
      if (contexts.length > 1) {
        // 同じ用語が異なる意味を持つ場合
        const semanticVariations = await this.analyzeSemanticVariations(
          term,
          contexts
        );
        
        if (semanticVariations.length > 1) {
          boundaries.push({
            type: 'linguistic',
            term: term.name,
            contexts: semanticVariations
          });
        }
      }
    }
    
    return boundaries;
  }
}
```

## コンテキストマッピングの実装

```typescript
export enum ContextRelationshipType {
  SHARED_KERNEL = "共有カーネル",
  CUSTOMER_SUPPLIER = "顧客・供給者",
  CONFORMIST = "追従者",
  ANTICORRUPTION_LAYER = "腐敗防止層",
  OPEN_HOST_SERVICE = "公開ホストサービス",
  PUBLISHED_LANGUAGE = "公表された言語",
  SEPARATE_WAYS = "別々の道",
  PARTNERSHIP = "パートナーシップ"
}

export class ContextMapper {
  mapRelationships(
    contexts: BoundedContext[]
  ): ContextMap {
    const relationships: ContextRelationship[] = [];
    
    // 全てのコンテキストペアを分析
    for (let i = 0; i < contexts.length; i++) {
      for (let j = i + 1; j < contexts.length; j++) {
        const relationship = this.analyzeRelationship(
          contexts[i],
          contexts[j]
        );
        
        if (relationship) {
          relationships.push(relationship);
        }
      }
    }
    
    return {
      contexts,
      relationships,
      visualization: this.createVisualization(contexts, relationships)
    };
  }
  
  private analyzeRelationship(
    context1: BoundedContext,
    context2: BoundedContext
  ): ContextRelationship | null {
    // 依存関係の分析
    const dependencies = this.analyzeDependencies(context1, context2);
    
    if (!dependencies.exists) {
      return null;
    }
    
    // 関係パターンの決定
    if (dependencies.bidirectional && dependencies.tight) {
      return {
        type: ContextRelationshipType.SHARED_KERNEL,
        upstream: null, // 両方向
        downstream: null,
        description: "両コンテキストが密接に連携"
      };
    }
    
    if (dependencies.upstream === context1.id) {
      if (this.hasInfluence(context2, context1)) {
        return {
          type: ContextRelationshipType.CUSTOMER_SUPPLIER,
          upstream: context1.id,
          downstream: context2.id,
          description: "顧客の要求に応じて供給"
        };
      } else {
        return {
          type: ContextRelationshipType.CONFORMIST,
          upstream: context1.id,
          downstream: context2.id,
          description: "上流の変更に追従"
        };
      }
    }
    
    // その他のパターン分析...
  }
}
```

## ECサイトのコンテキストマップ実装例

```typescript
// ECサイトのコンテキストマップ
const ecommerceContextMap = {
  contexts: [
    {
      id: "product-catalog",
      name: "商品カタログ",
      boundary: {
        concepts: ["Product", "Category", "Brand", "Specification"],
        responsibilities: ["商品情報管理", "カテゴリ管理", "検索"],
        ubiquitousLanguage: {
          "Product": "販売可能な商品の情報",
          "SKU": "在庫管理単位",
          "Category": "商品の分類体系"
        }
      }
    },
    {
      id: "inventory",
      name: "在庫管理",
      boundary: {
        concepts: ["Stock", "Location", "Movement", "Reservation"],
        responsibilities: ["在庫数管理", "在庫移動", "在庫予約"],
        ubiquitousLanguage: {
          "Stock": "特定場所の商品在庫数",
          "Available": "販売可能在庫",
          "Reserved": "注文により確保された在庫"
        }
      }
    },
    {
      id: "order-management",
      name: "注文管理",
      boundary: {
        concepts: ["Order", "OrderLine", "Customer", "Payment"],
        responsibilities: ["注文処理", "注文状態管理", "履歴管理"],
        ubiquitousLanguage: {
          "Order": "顧客の購買意図の記録",
          "Fulfillment": "注文の履行プロセス",
          "Cancellation": "注文の取消処理"
        }
      }
    }
  ],
  
  relationships: [
    {
      type: ContextRelationshipType.CUSTOMER_SUPPLIER,
      upstream: "product-catalog",
      downstream: "order-management",
      contract: {
        interface: "ProductCatalogAPI",
        methods: ["getProduct", "searchProducts", "getPrice"],
        sla: { availability: "99.9%", latency: "<100ms" }
      }
    },
    {
      type: ContextRelationshipType.ANTICORRUPTION_LAYER,
      upstream: "inventory",
      downstream: "order-management",
      implementation: {
        description: "在庫用語を注文用語に変換",
        translator: `
          class InventoryTranslator {
            translateAvailability(stock: Stock): OrderAvailability {
              return {
                canFulfill: stock.available > 0,
                quantity: stock.available,
                leadTime: stock.location.estimatedShipping
              };
            }
          }
        `
      }
    }
  ]
};
```

## モジュール境界の実装

```typescript
export class ModularBoundedContext {
  // パッケージ構造による境界の実装
  implementPackageStructure(context: BoundedContext): PackageStructure {
    return {
      root: `com.company.${context.name.toLowerCase()}`,
      
      layers: {
        domain: {
          path: `${root}/domain`,
          contents: [
            "entities",      // エンティティ
            "valueobjects",  // 値オブジェクト
            "aggregates",    // 集約
            "repositories",  // リポジトリインターフェース
            "services",      // ドメインサービス
            "events"         // ドメインイベント
          ]
        },
        
        application: {
          path: `${root}/application`,
          contents: [
            "commands",      // コマンド
            "queries",       // クエリ
            "handlers",      // ハンドラー
            "services",      // アプリケーションサービス
            "dto"           // データ転送オブジェクト
          ]
        },
        
        infrastructure: {
          path: `${root}/infrastructure`,
          contents: [
            "persistence",   // 永続化実装
            "messaging",     // メッセージング
            "web",          // Web層
            "configuration" // 設定
          ]
        },
        
        interfaces: {
          path: `${root}/interfaces`,
          contents: [
            "rest",         // REST API
            "grpc",         // gRPC
            "events",       // イベントインターフェース
            "ui"           // UI層
          ]
        }
      }
    };
  }
  
  // 集約による境界の実装
  implementAggregate(concept: DomainConcept): AggregateImplementation {
    return {
      // 集約ルート
      root: {
        name: `${concept.name}`,
        code: `
          export class ${concept.name} extends AggregateRoot {
            private constructor(
              private readonly id: ${concept.name}Id,
              private props: ${concept.name}Props
            ) {
              super();
              this.validateInvariants();
            }
            
            static create(props: Create${concept.name}Props): ${concept.name} {
              const id = ${concept.name}Id.generate();
              const ${concept.name.toLowerCase()} = new ${concept.name}(id, props);
              
              ${concept.name.toLowerCase()}.addDomainEvent(
                new ${concept.name}CreatedEvent(id, props)
              );
              
              return ${concept.name.toLowerCase()};
            }
            
            private validateInvariants(): void {
              ${concept.invariants.map(inv => `
                if (!${inv.condition}) {
                  throw new DomainError('${inv.message}');
                }
              `).join('\n')}
            }
          }
        `
      },
      
      // 値オブジェクト
      valueObjects: concept.attributes
        .filter(attr => attr.isValueObject)
        .map(attr => ({
          name: attr.name,
          code: this.generateValueObject(attr)
        })),
      
      // リポジトリインターフェース
      repository: {
        name: `${concept.name}Repository`,
        code: `
          export interface ${concept.name}Repository {
            findById(id: ${concept.name}Id): Promise<${concept.name} | null>;
            save(${concept.name.toLowerCase()}: ${concept.name}): Promise<void>;
            delete(id: ${concept.name}Id): Promise<void>;
          }
        `
      }
    };
  }
}
```

## サービス境界の実装

```typescript
export class ServiceBoundedContext {
  // マイクロサービスとしての実装
  implementAsMicroservice(
    context: BoundedContext
  ): MicroserviceImplementation {
    return {
      service: {
        name: context.name,
        
        api: {
          rest: this.generateRESTAPI(context),
          grpc: this.generateGRPCService(context),
          graphql: this.generateGraphQLSchema(context)
        },
        
        database: {
          type: this.selectDatabaseType(context),
          schema: this.generateDatabaseSchema(context),
          migrations: this.generateMigrations(context)
        },
        
        messaging: {
          events: this.defineEvents(context),
          commands: this.defineCommands(context),
          queries: this.defineQueries(context)
        },
        
        deployment: {
          dockerfile: this.generateDockerfile(context),
          kubernetes: this.generateKubernetesManifests(context),
          cicd: this.generateCICDPipeline(context)
        }
      }
    };
  }
  
  private generateRESTAPI(context: BoundedContext): RESTAPISpecification {
    const openapi = {
      openapi: "3.0.0",
      info: {
        title: `${context.name} API`,
        version: "1.0.0"
      },
      
      paths: {}
    };
    
    // 各集約に対するエンドポイントを生成
    for (const concept of context.boundary.concepts) {
      const resourceName = this.pluralize(concept.name.toLowerCase());
      
      openapi.paths[`/${resourceName}`] = {
        get: {
          summary: `List ${concept.name}s`,
          operationId: `list${concept.name}s`,
          responses: {
            "200": {
              description: "Success",
              content: {
                "application/json": {
                  schema: {
                    type: "array",
                    items: { $ref: `#/components/schemas/${concept.name}` }
                  }
                }
              }
            }
          }
        },
        
        post: {
          summary: `Create ${concept.name}`,
          operationId: `create${concept.name}`,
          requestBody: {
            content: {
              "application/json": {
                schema: { $ref: `#/components/schemas/Create${concept.name}` }
              }
            }
          },
          responses: {
            "201": {
              description: "Created",
              content: {
                "application/json": {
                  schema: { $ref: `#/components/schemas/${concept.name}` }
                }
              }
            }
          }
        }
      };
      
      // 個別リソースのエンドポイント
      openapi.paths[`/${resourceName}/{id}`] = {
        get: { /* ... */ },
        put: { /* ... */ },
        delete: { /* ... */ }
      };
    }
    
    return openapi;
  }
}
```

## 腐敗防止層（ACL）の実装

```typescript
export class AnticorruptionLayer {
  implement(
    upstream: BoundedContext,
    downstream: BoundedContext
  ): ACLImplementation {
    return {
      translators: this.generateTranslators(upstream, downstream),
      adapters: this.generateAdapters(upstream, downstream),
      facades: this.generateFacades(upstream, downstream)
    };
  }
  
  private generateTranslators(
    upstream: BoundedContext,
    downstream: BoundedContext
  ): Translator[] {
    const translators: Translator[] = [];
    
    // 概念間のマッピングを分析
    for (const upstreamConcept of upstream.boundary.concepts) {
      const downstreamConcept = this.findCorrespondingConcept(
        upstreamConcept,
        downstream
      );
      
      if (downstreamConcept) {
        translators.push({
          name: `${upstreamConcept.name}To${downstreamConcept.name}Translator`,
          
          implementation: `
            export class ${upstreamConcept.name}To${downstreamConcept.name}Translator {
              translate(
                source: ${upstream.name}.${upstreamConcept.name}
              ): ${downstream.name}.${downstreamConcept.name} {
                // 属性のマッピング
                return new ${downstream.name}.${downstreamConcept.name}({
                  ${this.mapAttributes(upstreamConcept, downstreamConcept)}
                });
              }
              
              translateBack(
                source: ${downstream.name}.${downstreamConcept.name}
              ): ${upstream.name}.${upstreamConcept.name} {
                // 逆方向のマッピング
                return new ${upstream.name}.${upstreamConcept.name}({
                  ${this.mapAttributesReverse(downstreamConcept, upstreamConcept)}
                });
              }
            }
          `
        });
      }
    }
    
    return translators;
  }
}

// 実装例：注文コンテキストが在庫コンテキストと統合
class OrderInventoryACL {
  constructor(
    private inventoryClient: InventoryServiceClient,
    private translator: InventoryTranslator
  ) {}
  
  async checkProductAvailability(
    productId: ProductId,
    quantity: number
  ): Promise<ProductAvailability> {
    try {
      // 上流サービスの呼び出し
      const inventoryResponse = await this.inventoryClient.getStock({
        sku: productId.toSKU(),
        location: 'all'
      });
      
      // 翻訳
      const availability = this.translator.translateToOrderContext(
        inventoryResponse
      );
      
      // ビジネスルールの適用
      return this.applyOrderingRules(availability, quantity);
      
    } catch (error) {
      // 上流サービスのエラーを下流のコンテキストに適したものに変換
      throw this.translateError(error);
    }
  }
  
  private applyOrderingRules(
    availability: InventoryAvailability,
    requestedQuantity: number
  ): ProductAvailability {
    return {
      canOrder: availability.availableQuantity >= requestedQuantity,
      availableQuantity: availability.availableQuantity,
      estimatedDelivery: this.calculateDeliveryDate(availability),
      backorderAllowed: this.isBackorderAllowed(availability)
    };
  }
}
```

## イベントによる統合の実装

```typescript
export class EventDrivenIntegration {
  implementEventExchange(
    publisher: BoundedContext,
    subscriber: BoundedContext
  ): EventIntegration {
    // イベントの定義
    const events = this.defineIntegrationEvents(publisher, subscriber);
    
    // パブリッシャー側の実装
    const publisherImplementation = {
      eventPublisher: `
        export class ${publisher.name}EventPublisher {
          constructor(private eventBus: EventBus) {}
          
          async publish${events[0].name}(event: ${events[0].name}) {
            // イベントを外部形式に変換
            const integrationEvent = {
              eventId: uuid(),
              eventType: '${publisher.name}.${events[0].name}',
              timestamp: new Date(),
              payload: this.serializePayload(event),
              metadata: {
                source: '${publisher.name}',
                version: '1.0'
              }
            };
            
            await this.eventBus.publish(integrationEvent);
          }
        }
      `
    };
    
    // サブスクライバー側の実装
    const subscriberImplementation = {
      eventHandler: `
        export class ${events[0].name}Handler {
          constructor(
            private translator: ${publisher.name}EventTranslator,
            private commandBus: CommandBus
          ) {}
          
          async handle(integrationEvent: IntegrationEvent) {
            // イベントを内部形式に変換
            const domainEvent = this.translator.translate(integrationEvent);
            
            // 対応するコマンドを生成
            const command = this.createCommand(domainEvent);
            
            // コマンドを実行
            await this.commandBus.execute(command);
          }
        }
      `
    };
    
    return {
      events,
      publisher: publisherImplementation,
      subscriber: subscriberImplementation
    };
  }
}
```

## 境界の進化管理

```typescript
export class ContextSplitter {
  splitContext(
    context: BoundedContext,
    splitCriteria: SplitCriteria
  ): BoundedContext[] {
    // 分割の必要性を評価
    const assessment = this.assessSplitNeed(context, splitCriteria);
    
    if (!assessment.shouldSplit) {
      return [context];
    }
    
    // 分割線の特定
    const splitLines = this.identifySplitLines(context, assessment);
    
    // 新しいコンテキストの生成
    const newContexts = this.createNewContexts(context, splitLines);
    
    // 関係の再定義
    const relationships = this.defineNewRelationships(newContexts);
    
    // 移行計画の作成
    const migrationPlan = this.createMigrationPlan(
      context,
      newContexts,
      relationships
    );
    
    return {
      contexts: newContexts,
      relationships,
      migrationPlan
    };
  }
  
  private assessSplitNeed(
    context: BoundedContext,
    criteria: SplitCriteria
  ): SplitAssessment {
    const factors = {
      teamSize: this.assessTeamSize(context),
      conceptCount: this.assessConceptComplexity(context),
      changeFrequency: this.assessChangePatterns(context),
      cohesion: this.assessCohesion(context)
    };
    
    const shouldSplit = 
      factors.teamSize > criteria.maxTeamSize ||
      factors.conceptCount > criteria.maxConcepts ||
      factors.cohesion < criteria.minCohesion;
    
    return {
      shouldSplit,
      factors,
      recommendation: this.generateRecommendation(factors)
    };
  }
}
```

## 境界の統合実装

```typescript
export class ContextMerger {
  mergeContexts(
    contexts: BoundedContext[],
    mergeCriteria: MergeCriteria
  ): BoundedContext {
    // 統合の妥当性を検証
    const validation = this.validateMerge(contexts, mergeCriteria);
    
    if (!validation.isValid) {
      throw new Error(`Cannot merge contexts: ${validation.reasons}`);
    }
    
    // 言語の統一
    const unifiedLanguage = this.unifyLanguages(
      contexts.map(c => c.boundary.ubiquitousLanguage)
    );
    
    // 概念の統合
    const mergedConcepts = this.mergeConcepts(contexts);
    
    // チームの再編成
    const mergedTeam = this.reorganizeTeams(contexts);
    
    // 新しい境界づけられたコンテキストの作成
    return {
      id: this.generateMergedId(contexts),
      name: this.generateMergedName(contexts),
      boundary: {
        concepts: mergedConcepts,
        responsibilities: this.mergeResponsibilities(contexts),
        ubiquitousLanguage: unifiedLanguage
      },
      implementation: {
        team: mergedTeam,
        technology: this.selectTechnology(contexts),
        dataStore: this.mergeDataStores(contexts)
      }
    };
  }
}
```

## コンテキストサイズのガイドライン

```typescript
export const ContextSizeGuidelines = {
  // 推奨されるサイズ
  recommended: {
    concepts: { min: 5, max: 15 },
    aggregates: { min: 3, max: 10 },
    teamSize: { min: 3, max: 9 },
    codeSize: { min: "10K", max: "100K" } // LOC
  },
  
  // 警告サイン
  warningSignals: [
    "15以上の概念を含む",
    "10以上のチームメンバー",
    "月間1000以上の変更",
    "50以上の外部依存"
  ],
  
  // 分割の指標
  splitIndicators: {
    highCoupling: "内部結合度 < 0.7",
    lowCohesion: "凝集度 < 0.8",
    teamConflicts: "週3回以上のマージコンフリクト",
    conceptualDistance: "意味的距離 > 0.5"
  }
};
```

## Appendix 18.1: EventStormingワークショップガイド

### 準備事項

```typescript
interface WorkshopPreparation {
  participants: {
    domainExperts: string[];      // ビジネス側の専門家
    technicalExperts: string[];   // 技術側の専門家
    facilitator: string;          // ファシリテーター
  };
  
  materials: {
    stickyNotes: {
      orange: "Domain Events";    // ドメインイベント
      blue: "Commands";           // コマンド
      yellow: "Aggregates";       // 集約
      pink: "External Systems";   // 外部システム
      purple: "Policies";         // ポリシー
    };
    
    wall: {
      length: "8-10 meters";      // 十分な壁面
      timeline: "left to right";  // 時系列の流れ
    };
  };
  
  duration: "1-2 days";
}
```

### ワークショップの進行

#### Phase 1: Big Picture (4時間)

```typescript
class BigPicturePhase {
  execute(): EventFlow {
    // 1. ドメインイベントの洗い出し
    const events = this.brainstormDomainEvents();
    
    // 2. 時系列に配置
    const timeline = this.arrangeChronologically(events);
    
    // 3. ホットスポットの特定
    const hotspots = this.identifyHotspots(timeline);
    
    // 4. 境界の初期仮説
    return this.identifyInitialBoundaries(timeline, hotspots);
  }
  
  private brainstormDomainEvents(): DomainEvent[] {
    // 参加者全員でイベントを書き出す
    // 過去形で記述: "注文された", "在庫が確保された"
    return [
      { name: "商品が検索された", actor: "顧客" },
      { name: "商品がカートに追加された", actor: "顧客" },
      { name: "注文が確定された", actor: "顧客" },
      { name: "在庫が確保された", actor: "システム" },
      { name: "支払いが処理された", actor: "決済システム" },
      { name: "配送が手配された", actor: "配送システム" }
    ];
  }
}
```

#### Phase 2: Process Modeling (4時間)

```typescript
class ProcessModelingPhase {
  refineModel(bigPicture: EventFlow): DetailedModel {
    // 1. コマンドの追加
    const commands = this.addCommands(bigPicture);
    
    // 2. アクターの明確化
    const actors = this.identifyActors(commands);
    
    // 3. 集約の発見
    const aggregates = this.discoverAggregates(commands);
    
    // 4. ポリシーの定義
    const policies = this.definePolicies(bigPicture);
    
    return {
      events: bigPicture.events,
      commands,
      actors,
      aggregates,
      policies
    };
  }
  
  private discoverAggregates(
    commands: Command[]
  ): Aggregate[] {
    // コマンドを受け取り、イベントを発生させる単位
    return [
      {
        name: "Product",
        commands: ["SearchProduct", "GetProductDetails"],
        events: ["ProductSearched", "ProductViewed"]
      },
      {
        name: "Cart",
        commands: ["AddToCart", "RemoveFromCart"],
        events: ["ProductAddedToCart", "ProductRemovedFromCart"]
      },
      {
        name: "Order",
        commands: ["PlaceOrder", "CancelOrder"],
        events: ["OrderPlaced", "OrderCanceled"]
      }
    ];
  }
}
```

#### Phase 3: Software Design (2時間)

```typescript
class SoftwareDesignPhase {
  designContexts(model: DetailedModel): BoundedContext[] {
    // 1. 言語境界の特定
    const linguisticBoundaries = this.findLinguisticBoundaries(model);
    
    // 2. 組織境界の考慮
    const organizationalBoundaries = this.considerTeams();
    
    // 3. 技術境界の検討
    const technicalBoundaries = this.analyzeTechnicalConstraints();
    
    // 4. 境界づけられたコンテキストの定義
    return this.defineBoundedContexts(
      linguisticBoundaries,
      organizationalBoundaries,
      technicalBoundaries
    );
  }
}
```

### 成果物の例

```typescript
const workshopOutput = {
  contexts: [
    {
      name: "Product Catalog",
      events: ["ProductSearched", "ProductViewed"],
      commands: ["SearchProduct", "GetProductDetails"],
      aggregates: ["Product", "Category"],
      team: "Catalog Team",
      ubiquitousLanguage: {
        "Product": "販売可能な商品の情報",
        "Category": "商品の分類",
        "SKU": "在庫管理単位"
      }
    },
    {
      name: "Shopping Cart",
      events: ["ProductAddedToCart", "CartCheckedOut"],
      commands: ["AddToCart", "Checkout"],
      aggregates: ["Cart", "CartItem"],
      team: "Frontend Team",
      ubiquitousLanguage: {
        "Cart": "購入前の商品の一時保管場所",
        "CartItem": "カート内の商品項目"
      }
    }
  ],
  
  relationships: [
    {
      from: "Shopping Cart",
      to: "Product Catalog",
      type: "Customer/Supplier",
      integration: "REST API"
    }
  ]
};
```

## Appendix 18.2: コンテキストマップパターンカタログ

### 1. Shared Kernel（共有カーネル）

```typescript
interface SharedKernelPattern {
  description: "両チームが共同で管理する小さなモデル";
  
  whenToUse: [
    "チーム間の密接な協力が可能",
    "頻繁な同期が必要",
    "共通の基本概念がある"
  ];
  
  implementation: {
    sharedCode: "shared-kernel/";
    ownership: "joint";
    changeProcess: "両チームの合意が必要";
  };
  
  example: {
    contexts: ["Pricing", "Inventory"],
    sharedConcepts: ["Money", "Currency", "ExchangeRate"],
    code: `
      // shared-kernel/money.ts
      export class Money {
        constructor(
          private amount: number,
          private currency: Currency
        ) {}
        
        add(other: Money): Money {
          if (this.currency !== other.currency) {
            throw new Error("Currency mismatch");
          }
          return new Money(
            this.amount + other.amount,
            this.currency
          );
        }
      }
    `
  };
}
```

### 2. Customer/Supplier（顧客/供給者）

```typescript
interface CustomerSupplierPattern {
  description: "下流が上流に要求を出せる関係";
  
  whenToUse: [
    "下流チームが上流に影響力を持つ",
    "定期的な調整が可能",
    "Win-Winの関係が築ける"
  ];
  
  implementation: {
    communication: "定期的なミーティング";
    contract: "明確なAPI契約";
    testing: "下流による受け入れテスト";
  };
  
  example: {
    supplier: "ProductCatalog",
    customer: "OrderManagement",
    contract: `
      interface ProductCatalogAPI {
        getProduct(id: string): Promise<Product>;
        checkAvailability(id: string): Promise<boolean>;
        reserveProduct(id: string, quantity: number): Promise<Reservation>;
      }
    `,
    negotiation: "月次の要求調整会議"
  };
}
```

### 3. Conformist（追従者）

```typescript
interface ConformistPattern {
  description: "下流が上流の変更に無条件で従う";
  
  whenToUse: [
    "上流への影響力がない",
    "上流のモデルで十分",
    "独自性より統合の容易さを優先"
  ];
  
  risks: [
    "上流の変更に振り回される",
    "下流の要求が反映されない"
  ];
  
  implementation: `
    class OrderService {
      constructor(private externalPaymentAPI: PaymentAPI) {}
      
      async processPayment(order: Order) {
        // 外部APIのモデルをそのまま使用
        const paymentRequest = {
          merchantId: this.merchantId,
          amount: order.total,
          currency: order.currency,
          // 外部APIの要求に完全に従う
          ...this.externalPaymentAPI.requiredFields
        };
        
        return this.externalPaymentAPI.process(paymentRequest);
      }
    }
  `;
}
```

### 4. Anticorruption Layer（腐敗防止層）

```typescript
interface AnticorruptionLayerPattern {
  description: "上流モデルから下流を保護する変換層";
  
  whenToUse: [
    "上流のモデルが下流に適さない",
    "レガシーシステムとの統合",
    "外部システムからの独立性が必要"
  ];
  
  components: {
    facade: "シンプルなインターフェース",
    adapter: "プロトコル変換",
    translator: "モデル変換"
  };
  
  implementation: `
    class LegacyInventoryACL {
      constructor(
        private legacySystem: LegacyInventorySystem,
        private translator: LegacyTranslator
      ) {}
      
      async checkStock(productId: ProductId): Promise<StockLevel> {
        // レガシーシステムの複雑な呼び出し
        const legacyCode = this.translator.toSKU(productId);
        const rawData = await this.legacySystem.QRYSTK(legacyCode);
        
        // 現代的なモデルに変換
        return this.translator.toStockLevel(rawData);
      }
    }
  `;
}
```

### 5. Open Host Service（公開ホストサービス）

```typescript
interface OpenHostServicePattern {
  description: "多数のクライアント向けの標準化されたプロトコル";
  
  characteristics: [
    "明確に文書化されたAPI",
    "バージョニング戦略",
    "後方互換性の維持"
  ];
  
  implementation: {
    protocol: "REST/GraphQL/gRPC",
    documentation: "OpenAPI/Schema",
    versioning: "URL/Header based"
  };
  
  example: `
    // OpenAPI 3.0 定義
    openapi: 3.0.0
    info:
      title: Product Catalog API
      version: 2.0.0
    paths:
      /v2/products:
        get:
          summary: List all products
          parameters:
            - name: category
              in: query
              schema:
                type: string
          responses:
            200:
              description: Success
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ProductList'
  `;
}
```

### 6. Published Language（公表された言語）

```typescript
interface PublishedLanguagePattern {
  description: "ドメイン間の共通交換フォーマット";
  
  examples: [
    "業界標準 (HL7, SWIFT)",
    "会社標準イベントスキーマ",
    "共通データフォーマット"
  ];
  
  implementation: `
    // 会社全体の標準イベントフォーマット
    interface StandardDomainEvent {
      eventId: string;
      eventType: string;
      timestamp: Date;
      aggregateId: string;
      aggregateType: string;
      payload: Record<string, unknown>;
      metadata: {
        userId: string;
        correlationId: string;
        causationId: string;
      };
    }
    
    // 各コンテキストはこの形式でイベントを公開
    class OrderContext {
      publishOrderPlaced(order: Order) {
        const event: StandardDomainEvent = {
          eventId: uuid(),
          eventType: 'OrderPlaced',
          timestamp: new Date(),
          aggregateId: order.id,
          aggregateType: 'Order',
          payload: this.serializeOrder(order),
          metadata: this.buildMetadata()
        };
        
        this.eventBus.publish(event);
      }
    }
  `;
}
```

### 7. Separate Ways（別々の道）

```typescript
interface SeparateWaysPattern {
  description: "統合のコストが利益を上回る場合の独立";
  
  whenToUse: [
    "統合コストが非常に高い",
    "ビジネス価値が低い",
    "独立して機能できる"
  ];
  
  tradeoffs: {
    pros: ["完全な自律性", "シンプルさ", "独立した進化"],
    cons: ["データ重複", "一貫性の欠如", "手動統合の必要性"]
  };
  
  example: {
    context1: "Marketing Campaign",
    context2: "Order Fulfillment",
    rationale: "キャンペーン分析と注文処理は独立して機能可能",
    integration: "必要時のみバッチでデータ交換"
  };
}
```

### 8. Partnership（パートナーシップ）

```typescript
interface PartnershipPattern {
  description: "相互依存する2チームの密接な協力";
  
  characteristics: [
    "共同での計画立案",
    "同期的な開発",
    "相互のCI/CD統合"
  ];
  
  implementation: `
    class PartnershipIntegration {
      // 両チームが共同で管理するインターフェース
      interface OrderInventoryContract {
        // 注文チームのニーズ
        checkAvailability(items: OrderItem[]): Promise<Availability[]>;
        reserveItems(items: OrderItem[]): Promise<Reservation>;
        
        // 在庫チームのニーズ
        notifyOrderPlaced(order: Order): Promise<void>;
        notifyOrderCanceled(orderId: string): Promise<void>;
      }
      
      // 共同のテストスイート
      describe('Order-Inventory Integration', () => {
        it('should reserve items when order is placed', async () => {
          // 両チームで合意したシナリオ
        });
      });
    }
  `;
}
```

## Appendix 18.3: 境界リファクタリング手法

### Branch by Abstraction

```typescript
class BranchByAbstraction {
  // Step 1: 抽象化の導入
  interface InventoryService {
    checkStock(productId: string): Promise<number>;
  }
  
  // Step 2: 既存実装をラップ
  class LegacyInventoryAdapter implements InventoryService {
    async checkStock(productId: string): Promise<number> {
      // 既存の実装を呼び出す
      return LegacyInventory.getStock(productId);
    }
  }
  
  // Step 3: 新実装を並行開発
  class NewInventoryService implements InventoryService {
    async checkStock(productId: string): Promise<number> {
      // 新しいコンテキストの実装
      const response = await this.inventoryAPI.get(`/stock/${productId}`);
      return response.available;
    }
  }
  
  // Step 4: 切り替え
  class InventoryServiceFactory {
    static create(): InventoryService {
      if (featureFlag.useNewInventory) {
        return new NewInventoryService();
      }
      return new LegacyInventoryAdapter();
    }
  }
}
```

### Parallel Run（並行実行）

```typescript
class ParallelRunMigration {
  async executeWithComparison<T>(
    oldImplementation: () => Promise<T>,
    newImplementation: () => Promise<T>
  ): Promise<T> {
    // 両方を並行実行
    const [oldResult, newResult] = await Promise.all([
      this.captureResult(oldImplementation),
      this.captureResult(newImplementation)
    ]);
    
    // 結果を比較
    if (!this.compareResults(oldResult, newResult)) {
      this.logDiscrepancy({
        old: oldResult,
        new: newResult,
        timestamp: new Date()
      });
    }
    
    // 移行期間中は古い実装の結果を使用
    return oldResult.value;
  }
  
  private async captureResult<T>(impl: () => Promise<T>) {
    const start = Date.now();
    try {
      const value = await impl();
      return {
        value,
        duration: Date.now() - start,
        error: null
      };
    } catch (error) {
      return {
        value: null,
        duration: Date.now() - start,
        error
      };
    }
  }
}
```

### データ移行戦略

```typescript
class DataMigrationStrategy {
  // 段階的データ移行
  async migrateInPhases() {
    // Phase 1: 読み取り専用の複製
    await this.replicateForReading();
    
    // Phase 2: 書き込みの複製
    await this.enableDualWrites();
    
    // Phase 3: 読み取りの切り替え
    await this.switchReadToNew();
    
    // Phase 4: 書き込みの切り替え
    await this.switchWriteToNew();
    
    // Phase 5: 旧システムの廃止
    await this.decommissionOld();
  }
  
  private async enableDualWrites() {
    class DualWriteRepository {
      async save(entity: Entity) {
        // 両方のシステムに書き込む
        await Promise.all([
          this.oldRepo.save(entity),
          this.newRepo.save(this.transform(entity))
        ]);
      }
      
      async find(id: string): Promise<Entity> {
        // まだ古いシステムから読む
        return this.oldRepo.find(id);
      }
    }
  }
}
```