# 第31章　APIコントラクトとバージョニング ― 約束の継承

## はじめに：契約書の進化

国際条約は、時代とともに修正や追加議定書を重ねながら、基本的な約束事を維持し続けます。新しい状況に対応しつつ、既存の合意を尊重する必要があるからです。APIコントラクトも同様に、新機能の追加や改善を行いながら、既存のクライアントとの約束を守り続ける必要があります。

本章では、Parasol V5.4におけるAPIコントラクトの設計とバージョニング戦略について解説します。

## APIコントラクトの基礎

### コントラクトファーストアプローチ

```typescript
export interface APIContractDesign {
  principles: {
    stability: "後方互換性の維持";
    clarity: "明確で理解しやすい仕様";
    evolvability: "拡張可能な設計";
    consistency: "一貫性のあるパターン";
    discoverability: "APIの発見可能性";
  };
  
  components: {
    schema: "データ構造の定義";
    endpoints: "エンドポイントの定義";
    parameters: "パラメータの仕様";
    responses: "レスポンス形式";
    errors: "エラー仕様";
  };
  
  lifecycle: {
    design: "設計フェーズ";
    review: "レビュー・承認";
    implementation: "実装";
    testing: "テスト";
    documentation: "ドキュメント化";
    deprecation: "廃止プロセス";
  };
}

export class APIContractManagement {
  // OpenAPI仕様の定義
  defineOpenAPISpecification(): OpenAPISpec {
    return {
      openapi: "3.1.0",
      info: {
        title: "Parasol V5.4 API",
        version: "1.0.0",
        description: "Parasol V5.4 システムのREST API",
        contact: {
          name: "API Support",
          email: "api-support@parasol.com",
          url: "https://api.parasol.com/support"
        },
        license: {
          name: "Apache 2.0",
          url: "https://www.apache.org/licenses/LICENSE-2.0.html"
        }
      },
      
      servers: [
        {
          url: "https://api.parasol.com/v1",
          description: "Production server"
        },
        {
          url: "https://api-staging.parasol.com/v1",
          description: "Staging server"
        }
      ],
      
      paths: {
        "/orders": {
          get: {
            operationId: "listOrders",
            summary: "注文一覧の取得",
            description: "指定された条件に基づいて注文の一覧を取得します",
            tags: ["Orders"],
            parameters: [
              {
                name: "status",
                in: "query",
                description: "注文ステータスでフィルタ",
                required: false,
                schema: {
                  type: "string",
                  enum: ["pending", "confirmed", "shipped", "delivered"],
                  default: "pending"
                }
              },
              {
                name: "page",
                in: "query",
                description: "ページ番号",
                required: false,
                schema: {
                  type: "integer",
                  minimum: 1,
                  default: 1
                }
              },
              {
                name: "limit",
                in: "query",
                description: "1ページあたりの件数",
                required: false,
                schema: {
                  type: "integer",
                  minimum: 1,
                  maximum: 100,
                  default: 20
                }
              }
            ],
            responses: {
              "200": {
                description: "成功",
                content: {
                  "application/json": {
                    schema: {
                      $ref: "#/components/schemas/OrderListResponse"
                    }
                  }
                }
              },
              "400": {
                $ref: "#/components/responses/BadRequest"
              },
              "401": {
                $ref: "#/components/responses/Unauthorized"
              },
              "500": {
                $ref: "#/components/responses/InternalServerError"
              }
            }
          },
          
          post: {
            operationId: "createOrder",
            summary: "注文の作成",
            description: "新しい注文を作成します",
            tags: ["Orders"],
            requestBody: {
              required: true,
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/CreateOrderRequest"
                  }
                }
              }
            },
            responses: {
              "201": {
                description: "作成成功",
                content: {
                  "application/json": {
                    schema: {
                      $ref: "#/components/schemas/Order"
                    }
                  }
                },
                headers: {
                  "Location": {
                    description: "作成された注文のURI",
                    schema: {
                      type: "string"
                    }
                  }
                }
              }
            }
          }
        }
      },
      
      components: {
        schemas: {
          Order: {
            type: "object",
            required: ["id", "customerId", "items", "total", "status"],
            properties: {
              id: {
                type: "string",
                format: "uuid",
                description: "注文ID",
                example: "123e4567-e89b-12d3-a456-426614174000"
              },
              customerId: {
                type: "string",
                description: "顧客ID"
              },
              items: {
                type: "array",
                minItems: 1,
                items: {
                  $ref: "#/components/schemas/OrderItem"
                }
              },
              total: {
                type: "number",
                format: "double",
                minimum: 0,
                description: "合計金額"
              },
              status: {
                $ref: "#/components/schemas/OrderStatus"
              },
              createdAt: {
                type: "string",
                format: "date-time",
                description: "作成日時"
              }
            }
          },
          
          OrderStatus: {
            type: "string",
            enum: ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"],
            description: "注文ステータス"
          }
        },
        
        securitySchemes: {
          bearerAuth: {
            type: "http",
            scheme: "bearer",
            bearerFormat: "JWT"
          },
          apiKey: {
            type: "apiKey",
            in: "header",
            name: "X-API-Key"
          }
        }
      },
      
      security: [
        { bearerAuth: [] },
        { apiKey: [] }
      ]
    };
  }
}
```

### スキーマバリデーション

```typescript
export class SchemaValidation {
  // JSON Schemaによるバリデーション
  implementSchemaValidation(): ValidationSystem {
    return {
      // リクエストバリデーション
      requestValidation: `
        import Ajv from 'ajv';
        import addFormats from 'ajv-formats';
        
        class RequestValidator {
          private readonly ajv: Ajv;
          private readonly schemas = new Map<string, any>();
          
          constructor() {
            this.ajv = new Ajv({
              allErrors: true,
              coerceTypes: true,
              removeAdditional: true
            });
            
            addFormats(this.ajv);
            this.loadSchemas();
          }
          
          validateRequest(
            operationId: string,
            data: unknown
          ): ValidationResult {
            const validate = this.ajv.getSchema(operationId);
            
            if (!validate) {
              throw new Error(\`Schema not found for \${operationId}\`);
            }
            
            const valid = validate(data);
            
            if (!valid) {
              return {
                valid: false,
                errors: this.formatErrors(validate.errors!)
              };
            }
            
            return { valid: true, data };
          }
          
          private formatErrors(
            errors: ErrorObject[]
          ): ValidationError[] {
            return errors.map(error => ({
              field: error.instancePath || error.schemaPath,
              message: error.message!,
              code: error.keyword,
              params: error.params
            }));
          }
        }
      `,
      
      // レスポンスバリデーション
      responseValidation: `
        class ResponseValidator {
          validateResponse(
            statusCode: number,
            contentType: string,
            body: unknown,
            operation: Operation
          ): void {
            const responseSpec = operation.responses[statusCode];
            
            if (!responseSpec) {
              throw new Error(
                \`Unexpected status code \${statusCode} for \${operation.operationId}\`
              );
            }
            
            const schema = responseSpec.content?.[contentType]?.schema;
            
            if (schema) {
              const valid = this.ajv.validate(schema, body);
              
              if (!valid) {
                // 開発環境では警告、本番環境ではロギング
                this.handleValidationFailure(
                  operation.operationId,
                  this.ajv.errors
                );
              }
            }
          }
        }
      `,
      
      // カスタムバリデーション
      customValidations: {
        businessRules: `
          class BusinessRuleValidator {
            async validateOrder(
              order: CreateOrderRequest
            ): Promise<ValidationResult> {
              const errors: ValidationError[] = [];
              
              // 在庫チェック
              for (const item of order.items) {
                const available = await this.checkInventory(
                  item.productId,
                  item.quantity
                );
                
                if (!available) {
                  errors.push({
                    field: \`items[\${item.productId}].quantity\`,
                    message: 'Insufficient inventory',
                    code: 'INSUFFICIENT_INVENTORY'
                  });
                }
              }
              
              // 最小注文金額チェック
              const total = this.calculateTotal(order.items);
              if (total < this.config.minimumOrderAmount) {
                errors.push({
                  field: 'total',
                  message: \`Order total must be at least \${this.config.minimumOrderAmount}\`,
                  code: 'BELOW_MINIMUM_ORDER'
                });
              }
              
              return errors.length > 0
                ? { valid: false, errors }
                : { valid: true };
            }
          }
        `
      }
    };
  }
}
```

## バージョニング戦略

### セマンティックバージョニング

```typescript
export class APIVersioning {
  // バージョニング戦略の実装
  implementVersioningStrategy(): VersioningStrategy {
    return {
      // URLパスバージョニング
      pathVersioning: {
        pattern: "/api/v{version}/{resource}",
        implementation: `
          // Express.jsルーター設定
          const versionRouter = (version: string) => {
            const router = express.Router();
            
            // バージョン固有のハンドラー
            const handlers = handlersByVersion[version];
            
            if (!handlers) {
              throw new Error(\`Unsupported API version: \${version}\`);
            }
            
            // ルートの設定
            router.get('/orders', handlers.listOrders);
            router.post('/orders', handlers.createOrder);
            router.get('/orders/:id', handlers.getOrder);
            
            return router;
          };
          
          // バージョンの登録
          app.use('/api/v1', versionRouter('v1'));
          app.use('/api/v2', versionRouter('v2'));
        `,
        
        advantages: [
          "明確なバージョン識別",
          "キャッシュフレンドリー",
          "簡単なルーティング"
        ],
        
        disadvantages: [
          "URLの重複",
          "リソースの移行が複雑"
        ]
      },
      
      // ヘッダーバージョニング
      headerVersioning: {
        pattern: "Accept: application/vnd.parasol.v{version}+json",
        implementation: `
          class HeaderVersionMiddleware {
            extractVersion(req: Request): string {
              const acceptHeader = req.headers.accept;
              
              if (!acceptHeader) {
                return this.config.defaultVersion;
              }
              
              const match = acceptHeader.match(
                /application\/vnd\.parasol\.v(\d+)\+json/
              );
              
              return match ? \`v\${match[1]}\` : this.config.defaultVersion;
            }
            
            middleware() {
              return (req: Request, res: Response, next: NextFunction) => {
                const version = this.extractVersion(req);
                
                if (!this.supportedVersions.includes(version)) {
                  return res.status(406).json({
                    error: 'Unsupported API version',
                    supportedVersions: this.supportedVersions
                  });
                }
                
                req.apiVersion = version;
                next();
              };
            }
          }
        `
      },
      
      // コンテンツネゴシエーション
      contentNegotiation: `
        class ContentNegotiator {
          negotiate(
            request: Request,
            availableVersions: Version[]
          ): Version {
            const requestedVersion = this.parseAcceptHeader(
              request.headers.accept
            );
            
            // 完全一致を試みる
            const exactMatch = availableVersions.find(
              v => v.version === requestedVersion
            );
            
            if (exactMatch) {
              return exactMatch;
            }
            
            // 互換性のあるバージョンを探す
            const compatibleVersion = this.findCompatibleVersion(
              requestedVersion,
              availableVersions
            );
            
            if (compatibleVersion) {
              return compatibleVersion;
            }
            
            // デフォルトバージョンを返す
            return availableVersions.find(v => v.isDefault)!;
          }
          
          private findCompatibleVersion(
            requested: string,
            available: Version[]
          ): Version | null {
            const requestedMajor = this.getMajorVersion(requested);
            
            // 同じメジャーバージョンで最新のものを探す
            return available
              .filter(v => this.getMajorVersion(v.version) === requestedMajor)
              .sort((a, b) => this.compareVersions(b.version, a.version))[0]
              || null;
          }
        }
      `
    };
  }
  
  // 後方互換性の維持
  maintainBackwardCompatibility(): BackwardCompatibilityStrategy {
    return {
      // フィールドの追加
      fieldAddition: `
        // 新しいフィールドはオプショナルとして追加
        interface OrderV1 {
          id: string;
          customerId: string;
          total: number;
        }
        
        interface OrderV2 extends OrderV1 {
          // 新しいフィールドはオプショナル
          shippingAddress?: Address;
          billingAddress?: Address;
          // デフォルト値を持つ
          currency?: string; // デフォルト: "JPY"
        }
      `,
      
      // フィールドの削除
      fieldDeprecation: `
        class FieldDeprecation {
          // 廃止予定フィールドのマーキング
          @deprecated('Use shippingAddress instead', '2024-12-31')
          get deliveryAddress(): Address | undefined {
            console.warn(
              'deliveryAddress is deprecated. Use shippingAddress instead.'
            );
            return this.shippingAddress;
          }
          
          // レスポンスでの処理
          toJSON(): any {
            const json = super.toJSON();
            
            // 古いクライアント向けに両方のフィールドを含める
            if (this.apiVersion < 'v2') {
              json.deliveryAddress = json.shippingAddress;
            }
            
            return json;
          }
        }
      `,
      
      // エンドポイントの移行
      endpointMigration: `
        class EndpointMigration {
          // 旧エンドポイントから新エンドポイントへのリダイレクト
          setupMigration(app: Express) {
            // 旧: GET /api/v1/customer/:id/orders
            // 新: GET /api/v1/orders?customerId=:id
            
            app.get('/api/v1/customer/:id/orders', (req, res) => {
              // 廃止予定の警告
              res.setHeader(
                'Deprecation',
                'true'
              );
              res.setHeader(
                'Link',
                '</api/v1/orders?customerId=' + req.params.id + '>; rel="successor-version"'
              );
              
              // 新しいエンドポイントにリダイレクト
              res.redirect(301, \`/api/v1/orders?customerId=\${req.params.id}\`);
            });
          }
        }
      `
    };
  }
}
```

## 破壊的変更の管理

### 移行戦略

```typescript
export class BreakingChangeManagement {
  // 破壊的変更の計画
  planBreakingChanges(): MigrationPlan {
    return {
      timeline: {
        announcement: "2024-01-01",
        deprecationStart: "2024-02-01",
        migrationPeriod: "6 months",
        sunsetDate: "2024-08-01"
      },
      
      communication: `
        class DeprecationNotifier {
          // APIレスポンスでの通知
          addDeprecationHeaders(res: Response, deprecation: Deprecation) {
            res.setHeader('Deprecation', 'true');
            res.setHeader('Sunset', deprecation.sunsetDate.toISOString());
            res.setHeader('Link', 
              \`<\${deprecation.migrationGuideUrl}>; rel="deprecation"\`
            );
          }
          
          // レスポンスボディでの警告
          addDeprecationWarning(response: any, deprecation: Deprecation) {
            response._warnings = response._warnings || [];
            response._warnings.push({
              code: 'DEPRECATION',
              message: deprecation.message,
              sunsetDate: deprecation.sunsetDate,
              migrationGuide: deprecation.migrationGuideUrl
            });
          }
        }
      `,
      
      // 段階的移行
      phasesMigration: [
        {
          phase: "Phase 1: Dual Support",
          duration: "2 months",
          actions: [
            "新しいAPIエンドポイントの公開",
            "旧APIは完全にサポート",
            "ドキュメントの更新",
            "移行ガイドの公開"
          ]
        },
        {
          phase: "Phase 2: Deprecation",
          duration: "3 months",
          actions: [
            "旧APIに廃止予定の警告を追加",
            "新規クライアントは新APIのみ",
            "既存クライアントへの通知",
            "移行サポートの提供"
          ]
        },
        {
          phase: "Phase 3: Migration",
          duration: "1 month",
          actions: [
            "最終警告期間",
            "パフォーマンスの低下警告",
            "サポートチケットの優先対応"
          ]
        },
        {
          phase: "Phase 4: Sunset",
          actions: [
            "旧APIの完全停止",
            "エラーレスポンスのみ返却",
            "移行ガイドへのリダイレクト"
          ]
        }
      ],
      
      // クライアント移行支援
      clientMigration: `
        class MigrationAssistant {
          // 自動移行ツール
          generateMigrationScript(
            clientCode: string,
            fromVersion: string,
            toVersion: string
          ): MigrationScript {
            const analyzer = new CodeAnalyzer();
            const usages = analyzer.findAPIUsages(clientCode);
            
            const migrations: CodeMigration[] = [];
            
            for (const usage of usages) {
              const migration = this.getMigrationRule(
                usage,
                fromVersion,
                toVersion
              );
              
              if (migration) {
                migrations.push({
                  location: usage.location,
                  original: usage.code,
                  replacement: migration.transform(usage.code),
                  description: migration.description
                });
              }
            }
            
            return {
              migrations,
              script: this.generateScript(migrations)
            };
          }
          
          // 互換性レイヤー
          createCompatibilityLayer(
            oldVersion: string,
            newVersion: string
          ): CompatibilityAdapter {
            return {
              transformRequest: (oldRequest) => {
                // 旧形式から新形式への変換
                return this.requestTransformer.transform(
                  oldRequest,
                  oldVersion,
                  newVersion
                );
              },
              
              transformResponse: (newResponse) => {
                // 新形式から旧形式への変換
                return this.responseTransformer.transform(
                  newResponse,
                  newVersion,
                  oldVersion
                );
              }
            };
          }
        }
      `
    };
  }
}
```

## APIドキュメンテーション

### 自動生成とメンテナンス

```typescript
export class APIDocumentation {
  // ドキュメント生成
  generateDocumentation(): DocumentationSystem {
    return {
      // Swagger UIの設定
      swaggerUI: `
        app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(
          openApiSpec,
          {
            customCss: '.swagger-ui .topbar { display: none }',
            customSiteTitle: 'Parasol V5.4 API Documentation',
            customfavIcon: '/favicon.ico'
          }
        ));
      `,
      
      // ReDoc設定
      redoc: `
        app.get('/docs', (req, res) => {
          res.send(\`
            <!DOCTYPE html>
            <html>
              <head>
                <title>Parasol API Documentation</title>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
              </head>
              <body>
                <redoc spec-url='/api/openapi.json'></redoc>
                <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
              </body>
            </html>
          \`);
        });
      `,
      
      // 動的ドキュメント生成
      dynamicDocumentation: `
        class DocumentationGenerator {
          generateFromCode(): OpenAPIDocument {
            const routes = this.extractRoutes();
            const schemas = this.extractSchemas();
            
            const paths: Paths = {};
            
            for (const route of routes) {
              const pathItem = this.generatePathItem(route);
              paths[route.path] = pathItem;
            }
            
            return {
              openapi: '3.1.0',
              info: this.generateInfo(),
              servers: this.config.servers,
              paths,
              components: {
                schemas: this.transformSchemas(schemas)
              }
            };
          }
          
          private extractRoutes(): Route[] {
            const routes: Route[] = [];
            
            // Express.jsのルートを解析
            this.app._router.stack.forEach((layer: any) => {
              if (layer.route) {
                const methods = Object.keys(layer.route.methods);
                routes.push({
                  path: layer.route.path,
                  methods,
                  handler: layer.route.stack[0].handle
                });
              }
            });
            
            return routes;
          }
        }
      `,
      
      // 例示とテスト
      examples: `
        class ExampleGenerator {
          generateExamples(schema: Schema): Examples {
            const faker = new Faker();
            
            return {
              success: this.generateValidExample(schema, faker),
              minimal: this.generateMinimalExample(schema),
              maximal: this.generateMaximalExample(schema, faker),
              edge_cases: this.generateEdgeCases(schema)
            };
          }
          
          // cURLコマンドの生成
          generateCurlExamples(
            operation: Operation
          ): CurlExample[] {
            const examples: CurlExample[] = [];
            
            // 基本的な例
            examples.push({
              title: 'Basic Request',
              command: \`
                curl -X \${operation.method} \\
                  https://api.parasol.com/v1\${operation.path} \\
                  -H 'Authorization: Bearer YOUR_TOKEN' \\
                  -H 'Content-Type: application/json'
              \`.trim()
            });
            
            // リクエストボディを含む例
            if (operation.requestBody) {
              examples.push({
                title: 'With Request Body',
                command: \`
                  curl -X \${operation.method} \\
                    https://api.parasol.com/v1\${operation.path} \\
                    -H 'Authorization: Bearer YOUR_TOKEN' \\
                    -H 'Content-Type: application/json' \\
                    -d '\${JSON.stringify(operation.requestBody.example, null, 2)}'
                \`.trim()
              });
            }
            
            return examples;
          }
        }
      `
    };
  }
}
```

## コントラクトテスト

### Provider/Consumer契約テスト

```typescript
export class ContractTesting {
  // Pactを使用した契約テスト
  implementContractTests(): ContractTestSuite {
    return {
      consumerTests: `
        describe('Order Service Consumer Tests', () => {
          const provider = new PactV3({
            consumer: 'Frontend',
            provider: 'OrderService',
            dir: path.resolve(process.cwd(), 'pacts')
          });
          
          it('gets order details', () => {
            return provider
              .given('an order with ID 123 exists')
              .uponReceiving('a request for order 123')
              .withRequest({
                method: 'GET',
                path: '/api/v1/orders/123',
                headers: {
                  Accept: 'application/json',
                  Authorization: 'Bearer token'
                }
              })
              .willRespondWith({
                status: 200,
                headers: {
                  'Content-Type': 'application/json'
                },
                body: MatchersV3.like({
                  id: '123',
                  customerId: MatchersV3.string('customer-456'),
                  items: MatchersV3.eachLike({
                    productId: MatchersV3.string('product-789'),
                    quantity: MatchersV3.integer(1),
                    price: MatchersV3.decimal(99.99)
                  }),
                  total: MatchersV3.decimal(299.97),
                  status: MatchersV3.regex(
                    'pending|confirmed|shipped',
                    'confirmed'
                  )
                })
              })
              .executeTest(async (mockServer) => {
                const client = new OrderServiceClient(mockServer.url);
                const order = await client.getOrder('123');
                
                expect(order.id).toBe('123');
                expect(order.status).toMatch(/pending|confirmed|shipped/);
              });
          });
        });
      `,
      
      providerTests: `
        describe('Order Service Provider Tests', () => {
          let server: Server;
          
          beforeAll(async () => {
            server = await startServer();
          });
          
          afterAll(async () => {
            await server.close();
          });
          
          it('verifies the provider', () => {
            return new Verifier({
              provider: 'OrderService',
              providerBaseUrl: 'http://localhost:3000',
              pactUrls: [
                path.resolve(__dirname, '../pacts/frontend-orderservice.json')
              ],
              stateHandlers: {
                'an order with ID 123 exists': async () => {
                  await database.orders.insert({
                    id: '123',
                    customerId: 'customer-456',
                    items: [{
                      productId: 'product-789',
                      quantity: 3,
                      price: 99.99
                    }],
                    total: 299.97,
                    status: 'confirmed'
                  });
                }
              },
              requestFilter: (req, res, next) => {
                // テスト用の認証をバイパス
                req.headers.authorization = 'Bearer valid-token';
                next();
              }
            }).verifyProvider();
          });
        });
      `,
      
      // スキーマ進化のテスト
      schemaEvolutionTests: `
        class SchemaEvolutionTester {
          async testBackwardCompatibility(
            oldSchema: Schema,
            newSchema: Schema
          ): Promise<CompatibilityResult> {
            const incompatibilities: Incompatibility[] = [];
            
            // 必須フィールドの追加チェック
            const newRequired = this.getNewRequiredFields(
              oldSchema,
              newSchema
            );
            
            if (newRequired.length > 0) {
              incompatibilities.push({
                type: 'REQUIRED_FIELD_ADDED',
                fields: newRequired,
                severity: 'BREAKING'
              });
            }
            
            // フィールド型の変更チェック
            const typeChanges = this.getTypeChanges(oldSchema, newSchema);
            
            for (const change of typeChanges) {
              if (!this.isCompatibleTypeChange(change)) {
                incompatibilities.push({
                  type: 'INCOMPATIBLE_TYPE_CHANGE',
                  field: change.field,
                  from: change.oldType,
                  to: change.newType,
                  severity: 'BREAKING'
                });
              }
            }
            
            return {
              compatible: incompatibilities.length === 0,
              incompatibilities
            };
          }
        }
      `
    };
  }
}
```

## まとめ

APIコントラクトとバージョニングは、長期的なシステムの成功に不可欠な要素です。Parasol V5.4における成功の鍵：

1. **明確なコントラクト定義** - OpenAPI仕様による厳密な定義
2. **計画的なバージョニング** - セマンティックバージョニングの採用
3. **後方互換性の維持** - 既存クライアントへの配慮
4. **段階的な移行** - 破壊的変更の慎重な管理
5. **包括的なテスト** - 契約テストによる保証

適切に設計されたAPIは、システムの進化を可能にしながら、既存の統合を保護します。

### 次章への架橋

APIコントラクトとバージョニングの重要性を理解しました。第VII部では、これらの原則を実際のプロジェクトで適用する実践的なアプローチを探求します。

---

## 演習問題

1. 既存のREST APIをOpenAPI 3.0仕様で記述し、破壊的変更なしに新機能を追加する方法を設計してください。

2. 以下のシナリオに対して、適切なバージョニング戦略を選択し、移行計画を作成してください：
   - レスポンス形式の大幅な変更
   - 認証方式の変更（Basic認証からOAuth 2.0へ）
   - エンドポイント構造の再編成

3. Pactを使用して、フロントエンドとバックエンド間の契約テストを実装してください。エラーケースと正常系の両方を含めてください。