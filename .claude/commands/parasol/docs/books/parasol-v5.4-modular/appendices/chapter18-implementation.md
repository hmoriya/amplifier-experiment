# 付録：第18章　境界づけられたコンテキストの実装詳細

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