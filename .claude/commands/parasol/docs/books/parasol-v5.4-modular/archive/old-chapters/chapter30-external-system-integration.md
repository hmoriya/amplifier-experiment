# 第30章　外部システム連携 ― 架け橋の構築

## はじめに：諾島を結ぶ橋

日本の瀬戸内海は、無数の島々が点在する美しい海域です。かつて、これらの島々は孤立していましたが、現在では壮大な橋がそれらを結び、人や物の流れを生み出しています。同様に、ビジネスエコシステムでも、外部システムとの連携は新たな価値を創出する重要な架け橋となります。

本章では、Parasol V5.4における外部システムとの安全かつ効率的な連携方法を解説します。

## 外部連携の基本原則

### 連携アーキテクチャ

```typescript
export interface ExternalIntegrationArchitecture {
  principles: {
    isolation: "内部システムの保護";
    abstraction: "外部依存の抽象化";
    resilience: "障害への耐性";
    security: "セキュアな通信";
    monitoring: "外部サービスの監視";
  };
  
  patterns: {
    adapter: "外部APIの抽象化";
    antiCorruption: "腐敗防止層";
    gateway: "ゲートウェイパターン";
    facade: "ファサードパターン";
    orchestration: "オーケストレーション";
  };
  
  challenges: {
    versioning: "APIバージョン管理";
    rateLimit: "レート制限への対応";
    authentication: "認証方式の違い";
    dataFormat: "データ形式の変換";
    reliability: "信頼性の保証";
  };
}

export class ExternalSystemIntegration {
  // 外部システム連携の設計
  designIntegration(
    externalSystem: ExternalSystem,
    requirements: IntegrationRequirements
  ): IntegrationDesign {
    // システム特性の分析
    const characteristics = this.analyzeSystemCharacteristics(externalSystem);
    
    // 適切なパターンの選択
    const pattern = this.selectIntegrationPattern(
      characteristics,
      requirements
    );
    
    // セキュリティ要件の定義
    const security = this.defineSecurityRequirements(
      externalSystem,
      requirements.sensitivity
    );
    
    // エラーハンドリング戦略
    const errorHandling = this.defineErrorHandling(
      characteristics.reliability,
      requirements.criticality
    );
    
    return {
      architecture: pattern,
      security,
      errorHandling,
      monitoring: this.defineMonitoring(externalSystem),
      testing: this.defineTestingStrategy(externalSystem)
    };
  }
}
```

### 腐敗防止層の実装

```typescript
export class AntiCorruptionLayer {
  // 外部システムの抽象化
  implementACL(
    externalService: ExternalService
  ): AntiCorruptionLayerImplementation {
    return {
      // ドメインモデルへの変換
      translator: {
        fromExternal: `
          class PaymentTranslator {
            // 外部システムのデータをドメインモデルに変換
            toDomainModel(externalData: ExternalPayment): Payment {
              // 外部システム固有の構造を隔離
              return new Payment({
                id: new PaymentId(externalData.transaction_id),
                amount: Money.fromCents(
                  externalData.amount_cents,
                  externalData.currency_code
                ),
                status: this.mapStatus(externalData.status),
                timestamp: new Date(externalData.created_at),
                method: this.mapPaymentMethod(externalData.payment_type),
                // 外部システムの詳細はメタデータとして保持
                metadata: {
                  externalId: externalData.transaction_id,
                  externalStatus: externalData.status,
                  rawData: JSON.stringify(externalData)
                }
              });
            }
            
            // ドメインモデルから外部システムへの変換
            toExternalFormat(payment: Payment): ExternalPaymentRequest {
              return {
                transaction_id: payment.id.value,
                amount_cents: payment.amount.toCents(),
                currency_code: payment.amount.currency.code,
                payment_type: this.mapToExternalMethod(payment.method),
                customer_ref: payment.customerId.value,
                metadata: {
                  order_id: payment.orderId?.value,
                  source: "parasol-v5"
                }
              };
            }
            
            // ステータスマッピング
            private mapStatus(externalStatus: string): PaymentStatus {
              const mapping: Record<string, PaymentStatus> = {
                'pending': PaymentStatus.PENDING,
                'processing': PaymentStatus.PROCESSING,
                'completed': PaymentStatus.COMPLETED,
                'failed': PaymentStatus.FAILED,
                'cancelled': PaymentStatus.CANCELLED,
                'refunded': PaymentStatus.REFUNDED
              };
              
              return mapping[externalStatus.toLowerCase()] 
                || PaymentStatus.UNKNOWN;
            }
          }
        `,
        
        toExternal: `
          class OrderTranslator {
            // 注文情報を外部フルフィルメントシステムに変換
            toFulfillmentRequest(order: Order): FulfillmentRequest {
              return {
                shipment_request_id: this.generateRequestId(),
                order_reference: order.id.value,
                recipient: {
                  name: order.shippingAddress.recipientName,
                  address_line1: order.shippingAddress.line1,
                  address_line2: order.shippingAddress.line2,
                  city: order.shippingAddress.city,
                  state_province: order.shippingAddress.state,
                  postal_code: order.shippingAddress.postalCode,
                  country_code: order.shippingAddress.countryCode,
                  phone: order.shippingAddress.phone
                },
                items: order.items.map(item => ({
                  sku: item.product.sku.value,
                  quantity: item.quantity,
                  unit_price: item.price.amount,
                  currency: item.price.currency.code
                })),
                shipping_method: this.mapShippingMethod(order.shippingMethod),
                special_instructions: order.notes
              };
            }
          }
        `
      },
      
      // 外部サービスのラッパー
      serviceWrapper: `
        class PaymentServiceWrapper {
          constructor(
            private readonly externalClient: ExternalPaymentClient,
            private readonly translator: PaymentTranslator,
            private readonly logger: Logger,
            private readonly metrics: MetricsCollector
          ) {}
          
          async processPayment(payment: Payment): Promise<PaymentResult> {
            const timer = this.metrics.startTimer('payment.process');
            
            try {
              // ドメインモデルを外部形式に変換
              const request = this.translator.toExternalFormat(payment);
              
              // 外部サービスの呼び出し
              const response = await this.externalClient.charge(request);
              
              // レスポンスをドメインモデルに変換
              const processedPayment = this.translator.toDomainModel(response);
              
              return PaymentResult.success(processedPayment);
            } catch (error) {
              // 外部システムのエラーをドメインエラーに変換
              if (this.isRateLimitError(error)) {
                throw new PaymentRateLimitError(
                  'Payment service rate limit exceeded'
                );
              }
              
              if (this.isAuthenticationError(error)) {
                throw new PaymentAuthenticationError(
                  'Payment service authentication failed'
                );
              }
              
              throw new PaymentProcessingError(
                'Payment processing failed',
                error
              );
            } finally {
              timer.observe();
            }
          }
        }
      `
    };
  }
}
```

## サードパーティAPI連携

### APIクライアント設計

```typescript
export class ThirdPartyAPIIntegration {
  // 汎用APIクライアント
  implementAPIClient(): APIClientImplementation {
    return {
      // クライアント基本設計
      baseClient: `
        abstract class BaseAPIClient {
          protected readonly baseURL: string;
          protected readonly apiKey: string;
          protected readonly timeout: number;
          protected readonly retryConfig: RetryConfig;
          
          constructor(config: APIClientConfig) {
            this.baseURL = config.baseURL;
            this.apiKey = config.apiKey;
            this.timeout = config.timeout || 30000;
            this.retryConfig = config.retryConfig || {
              maxRetries: 3,
              initialDelay: 1000,
              maxDelay: 30000,
              factor: 2
            };
          }
          
          protected async request<T>(
            options: RequestOptions
          ): Promise<T> {
            return this.withRetry(async () => {
              const response = await this.executeRequest(options);
              return this.handleResponse<T>(response);
            });
          }
          
          private async executeRequest(
            options: RequestOptions
          ): Promise<Response> {
            const controller = new AbortController();
            const timeoutId = setTimeout(
              () => controller.abort(),
              this.timeout
            );
            
            try {
              const response = await fetch(
                \`\${this.baseURL}\${options.path}\`,
                {
                  method: options.method,
                  headers: {
                    ...this.getDefaultHeaders(),
                    ...options.headers
                  },
                  body: options.body 
                    ? JSON.stringify(options.body)
                    : undefined,
                  signal: controller.signal
                }
              );
              
              return response;
            } finally {
              clearTimeout(timeoutId);
            }
          }
          
          private async withRetry<T>(
            operation: () => Promise<T>
          ): Promise<T> {
            let lastError: Error;
            let delay = this.retryConfig.initialDelay;
            
            for (let i = 0; i <= this.retryConfig.maxRetries; i++) {
              try {
                return await operation();
              } catch (error) {
                lastError = error as Error;
                
                if (!this.isRetryable(error) || 
                    i === this.retryConfig.maxRetries) {
                  throw error;
                }
                
                await this.sleep(delay);
                delay = Math.min(
                  delay * this.retryConfig.factor,
                  this.retryConfig.maxDelay
                );
              }
            }
            
            throw lastError!;
          }
          
          protected abstract getDefaultHeaders(): Record<string, string>;
          protected abstract handleResponse<T>(response: Response): Promise<T>;
          protected abstract isRetryable(error: unknown): boolean;
        }
      `,
      
      // 特定APIの実装
      specificImplementations: {
        payment: `
          class StripeClient extends BaseAPIClient {
            constructor(config: StripeConfig) {
              super({
                baseURL: 'https://api.stripe.com/v1',
                apiKey: config.secretKey,
                timeout: 30000
              });
            }
            
            async createPaymentIntent(
              params: PaymentIntentParams
            ): Promise<PaymentIntent> {
              return this.request<PaymentIntent>({
                method: 'POST',
                path: '/payment_intents',
                body: {
                  amount: params.amount,
                  currency: params.currency,
                  payment_method_types: params.paymentMethodTypes,
                  metadata: params.metadata
                }
              });
            }
            
            async confirmPaymentIntent(
              intentId: string,
              params: ConfirmParams
            ): Promise<PaymentIntent> {
              return this.request<PaymentIntent>({
                method: 'POST',
                path: \`/payment_intents/\${intentId}/confirm\`,
                body: params
              });
            }
            
            protected getDefaultHeaders(): Record<string, string> {
              return {
                'Authorization': \`Bearer \${this.apiKey}\`,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Stripe-Version': '2023-10-16'
              };
            }
            
            protected async handleResponse<T>(response: Response): Promise<T> {
              const data = await response.json();
              
              if (!response.ok) {
                throw new StripeError(
                  data.error.message,
                  data.error.type,
                  data.error.code
                );
              }
              
              return data as T;
            }
            
            protected isRetryable(error: unknown): boolean {
              if (error instanceof StripeError) {
                return error.type === 'api_connection_error' ||
                       error.type === 'rate_limit_error';
              }
              return false;
            }
          }
        `,
        
        shipping: `
          class ShippingAPIClient extends BaseAPIClient {
            async calculateRates(
              shipment: ShipmentDetails
            ): Promise<ShippingRate[]> {
              const rates = await Promise.all([
                this.getFedExRates(shipment),
                this.getUPSRates(shipment),
                this.getUSPSRates(shipment)
              ]);
              
              return rates
                .flat()
                .sort((a, b) => a.cost - b.cost);
            }
            
            private async getFedExRates(
              shipment: ShipmentDetails
            ): Promise<ShippingRate[]> {
              try {
                const response = await this.request<FedExRateResponse>({
                  method: 'POST',
                  path: '/rate/v1/rates/quotes',
                  body: this.buildFedExRequest(shipment)
                });
                
                return this.transformFedExRates(response);
              } catch (error) {
                this.logger.warn('FedEx rate calculation failed', error);
                return [];
              }
            }
          }
        `
      },
      
      // レート制限対策
      rateLimiting: `
        class RateLimitManager {
          private readonly limits: Map<string, RateLimit> = new Map();
          
          async executeWithRateLimit<T>(
            key: string,
            operation: () => Promise<T>,
            limits: RateLimitConfig
          ): Promise<T> {
            const limiter = this.getOrCreateLimiter(key, limits);
            
            // トークンの取得を待つ
            await limiter.removeTokens(1);
            
            try {
              return await operation();
            } catch (error) {
              // レート制限エラーの場合はトークンを返却
              if (this.isRateLimitError(error)) {
                limiter.addTokens(1);
              }
              throw error;
            }
          }
          
          private getOrCreateLimiter(
            key: string,
            config: RateLimitConfig
          ): RateLimiter {
            if (!this.limits.has(key)) {
              this.limits.set(key, new RateLimiter({
                tokensPerInterval: config.requests,
                interval: config.window,
                maxBurst: config.burst || config.requests
              }));
            }
            
            return this.limits.get(key)!;
          }
        }
      `
    };
  }
  
  // Webhook実装
  implementWebhooks(): WebhookImplementation {
    return {
      receiver: `
        class WebhookReceiver {
          private readonly handlers = new Map<string, WebhookHandler>();
          
          async handleWebhook(
            request: Request,
            source: string
          ): Promise<Response> {
            try {
              // 署名検証
              const isValid = await this.verifySignature(
                request,
                source
              );
              
              if (!isValid) {
                return new Response('Invalid signature', { status: 401 });
              }
              
              // イベントの解析
              const event = await this.parseEvent(request, source);
              
              // 重複処理の防止
              if (await this.isDuplicate(event)) {
                return new Response('Event already processed', { 
                  status: 200 
                });
              }
              
              // ハンドラーの実行
              const handler = this.handlers.get(\`\${source}:\${event.type}\`);
              if (handler) {
                await handler.handle(event);
              }
              
              // イベントの記録
              await this.recordEvent(event);
              
              return new Response('OK', { status: 200 });
            } catch (error) {
              this.logger.error('Webhook processing failed', error);
              
              // エラーを返すとリトライされる可能性がある
              // 意図的に200を返して非同期処理
              this.queueForRetry(request, source, error);
              return new Response('OK', { status: 200 });
            }
          }
          
          private async verifySignature(
            request: Request,
            source: string
          ): Promise<boolean> {
            switch (source) {
              case 'stripe':
                return this.verifyStripeSignature(request);
              case 'github':
                return this.verifyGitHubSignature(request);
              case 'shopify':
                return this.verifyShopifySignature(request);
              default:
                throw new Error(\`Unknown webhook source: \${source}\`);
            }
          }
          
          private async verifyStripeSignature(
            request: Request
          ): Promise<boolean> {
            const signature = request.headers.get('stripe-signature');
            const body = await request.text();
            const secret = this.config.stripe.webhookSecret;
            
            try {
              const elements = signature!.split(',').reduce((acc, item) => {
                const [key, value] = item.split('=');
                acc[key] = value;
                return acc;
              }, {} as Record<string, string>);
              
              const payload = \`\${elements.t}.\${body}\`;
              const expectedSig = crypto
                .createHmac('sha256', secret)
                .update(payload)
                .digest('hex');
              
              return elements.v1 === expectedSig;
            } catch {
              return false;
            }
          }
        }
      `,
      
      handlers: {
        payment: `
          class PaymentWebhookHandler implements WebhookHandler {
            async handle(event: WebhookEvent): Promise<void> {
              switch (event.type) {
                case 'payment_intent.succeeded':
                  await this.handlePaymentSuccess(event.data);
                  break;
                
                case 'payment_intent.payment_failed':
                  await this.handlePaymentFailure(event.data);
                  break;
                
                case 'charge.dispute.created':
                  await this.handleDispute(event.data);
                  break;
              }
            }
            
            private async handlePaymentSuccess(
              data: PaymentIntentData
            ): Promise<void> {
              // イベントの発行
              await this.eventBus.publish(
                new PaymentCompletedEvent({
                  paymentId: data.id,
                  amount: data.amount,
                  currency: data.currency,
                  metadata: data.metadata
                })
              );
            }
          }
        `
      }
    };
  }
}
```

## レガシーシステム連携

### レガシーAPIラッパー

```typescript
export class LegacySystemIntegration {
  // SOAPサービス連携
  implementSOAPIntegration(): SOAPIntegration {
    return {
      client: `
        class LegacySOAPClient {
          private readonly wsdlUrl: string;
          private client?: soap.Client;
          
          async initialize(): Promise<void> {
            this.client = await soap.createClientAsync(this.wsdlUrl, {
              endpoint: this.config.endpoint,
              escapeXML: true,
              forceSoap12Headers: true
            });
            
            // Basic認証の設定
            this.client.setSecurity(
              new soap.BasicAuthSecurity(
                this.config.username,
                this.config.password
              )
            );
          }
          
          async getCustomerData(
            customerId: string
          ): Promise<CustomerData> {
            const args = {
              CustomerRequest: {
                CustomerId: customerId,
                IncludeHistory: true,
                IncludeOrders: true
              }
            };
            
            try {
              const [result] = await this.client!.GetCustomerAsync(args);
              
              // XMLレスポンスの解析と変換
              return this.transformCustomerResponse(result);
            } catch (error) {
              if (error.root?.Envelope?.Body?.Fault) {
                const fault = error.root.Envelope.Body.Fault;
                throw new LegacySystemError(
                  fault.faultstring || 'SOAP fault',
                  fault.faultcode
                );
              }
              throw error;
            }
          }
          
          private transformCustomerResponse(
            soapResponse: any
          ): CustomerData {
            const customer = soapResponse.GetCustomerResult.Customer;
            
            return {
              id: customer.CustomerId,
              name: customer.CustomerName,
              email: customer.EmailAddress?.toLowerCase(),
              status: this.mapCustomerStatus(customer.StatusCode),
              createdDate: new Date(customer.CreateDate),
              orders: this.transformOrders(customer.Orders?.Order || [])
            };
          }
        }
      `,
      
      // メインフレーム連携
      mainframe: `
        class MainframeConnector {
          private readonly tn3270: TN3270Client;
          
          async executeTransaction(
            transactionCode: string,
            data: TransactionData
          ): Promise<TransactionResult> {
            const session = await this.tn3270.connect({
              host: this.config.host,
              port: this.config.port,
              model: '3278-2'
            });
            
            try {
              // ログイン
              await this.login(session);
              
              // トランザクションの実行
              await session.send(transactionCode);
              await session.wait();
              
              // データ入力
              await this.inputData(session, data);
              
              // 結果の取得
              const screen = await session.getScreen();
              return this.parseTransactionResult(screen);
            } finally {
              await session.disconnect();
            }
          }
          
          private async inputData(
            session: TN3270Session,
            data: TransactionData
          ): Promise<void> {
            // フィールドマッピングに基づいて入力
            for (const [field, value] of Object.entries(data)) {
              const position = this.fieldMap.get(field);
              if (position) {
                await session.moveCursor(position.row, position.col);
                await session.type(this.formatValue(value, position.length));
              }
            }
            
            // Enterキーを送信
            await session.enter();
            await session.wait();
          }
        }
      `,
      
      // ファイルベース連携
      fileTransfer: `
        class LegacyFileTransfer {
          async importBatchFile(
            filePath: string
          ): Promise<BatchImportResult> {
            // 固定長フォーマットの解析
            const parser = new FixedWidthParser({
              schema: [
                { name: 'recordType', start: 0, length: 2 },
                { name: 'customerId', start: 2, length: 10 },
                { name: 'orderDate', start: 12, length: 8 },
                { name: 'amount', start: 20, length: 12, type: 'decimal' },
                { name: 'status', start: 32, length: 1 }
              ]
            });
            
            const records: BatchRecord[] = [];
            const errors: ImportError[] = [];
            
            const stream = fs.createReadStream(filePath, {
              encoding: 'cp1252' // レガシーエンコーディング
            });
            
            let lineNumber = 0;
            for await (const line of readline.createInterface({ input: stream })) {
              lineNumber++;
              
              try {
                const record = parser.parse(line);
                
                // レコードタイプ別の処理
                switch (record.recordType) {
                  case 'HD': // ヘッダー
                    await this.processHeader(record);
                    break;
                  
                  case 'DT': // データ
                    const transformed = await this.transformRecord(record);
                    records.push(transformed);
                    break;
                  
                  case 'TR': // トレーラー
                    await this.validateTotals(record, records);
                    break;
                }
              } catch (error) {
                errors.push({
                  line: lineNumber,
                  content: line,
                  error: error.message
                });
              }
            }
            
            return {
              successCount: records.length,
              errorCount: errors.length,
              records,
              errors
            };
          }
        }
      `
    };
  }
  
  // データ同期戦略
  implementDataSynchronization(): DataSyncStrategy {
    return {
      // CDC（Change Data Capture）
      changeDataCapture: `
        class CDCProcessor {
          async processChanges(
            source: string,
            since: Date
          ): Promise<SyncResult> {
            // 変更ログの取得
            const changes = await this.getChangeLog(source, since);
            
            // 変更のグルーピング
            const grouped = this.groupChangesByEntity(changes);
            
            const results: EntitySyncResult[] = [];
            
            for (const [entity, entityChanges] of grouped) {
              try {
                // エンティティ単位で処理
                const result = await this.syncEntity(
                  entity,
                  entityChanges
                );
                results.push(result);
              } catch (error) {
                // エラーを記録して続行
                this.logger.error(
                  \`Failed to sync \${entity}\`,
                  error
                );
              }
            }
            
            return this.aggregateResults(results);
          }
          
          private async syncEntity(
            entity: string,
            changes: Change[]
          ): Promise<EntitySyncResult> {
            // 変更を時間順にソート
            const sortedChanges = changes.sort(
              (a, b) => a.timestamp.getTime() - b.timestamp.getTime()
            );
            
            let processed = 0;
            let errors = 0;
            
            for (const change of sortedChanges) {
              try {
                await this.applyChange(entity, change);
                processed++;
              } catch (error) {
                errors++;
                
                // 衝突解決
                if (error instanceof ConflictError) {
                  await this.resolveConflict(entity, change, error);
                }
              }
            }
            
            return { entity, processed, errors };
          }
        }
      `,
      
      // イベントソーシングベースの同期
      eventBasedSync: `
        class EventBasedSynchronizer {
          async synchronize(
            sourceEvents: DomainEvent[]
          ): Promise<void> {
            for (const event of sourceEvents) {
              // イベントを外部システムのコマンドに変換
              const commands = this.translateEventToCommands(event);
              
              for (const command of commands) {
                await this.executeCommand(command);
              }
              
              // 同期ポイントの記録
              await this.recordSyncPoint(event);
            }
          }
          
          private translateEventToCommands(
            event: DomainEvent
          ): ExternalCommand[] {
            switch (event.type) {
              case 'OrderCreated':
                return [
                  new CreateCustomerIfNotExists(event.data.customerId),
                  new CreateSalesOrder(event.data)
                ];
              
              case 'OrderShipped':
                return [
                  new UpdateInventory(event.data.items),
                  new CreateShipment(event.data.shipmentDetails),
                  new NotifyCustomer(event.data.customerId)
                ];
              
              default:
                return [];
            }
          }
        }
      `
    };
  }
}
```

## セキュリティと認証

### OAuth 2.0 / OpenID Connect

```typescript
export class ExternalAuthenticationIntegration {
  // OAuthクライアント実装
  implementOAuthClient(): OAuthClientImplementation {
    return {
      authorizationCodeFlow: `
        class OAuthClient {
          // 認可フローの開始
          async initiateAuthorization(
            state: string,
            scopes: string[]
          ): Promise<AuthorizationUrl> {
            const codeVerifier = this.generateCodeVerifier();
            const codeChallenge = await this.generateCodeChallenge(
              codeVerifier
            );
            
            // PKCEパラメータをセッションに保存
            await this.sessionStore.save(state, {
              codeVerifier,
              scopes,
              timestamp: Date.now()
            });
            
            const params = new URLSearchParams({
              response_type: 'code',
              client_id: this.config.clientId,
              redirect_uri: this.config.redirectUri,
              scope: scopes.join(' '),
              state,
              code_challenge: codeChallenge,
              code_challenge_method: 'S256'
            });
            
            return \`\${this.config.authorizationEndpoint}?\${params}\`;
          }
          
          // アクセストークンの取得
          async exchangeCodeForToken(
            code: string,
            state: string
          ): Promise<TokenResponse> {
            // セッションデータの検証
            const sessionData = await this.sessionStore.get(state);
            if (!sessionData) {
              throw new Error('Invalid state parameter');
            }
            
            const response = await fetch(this.config.tokenEndpoint, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              },
              body: new URLSearchParams({
                grant_type: 'authorization_code',
                code,
                redirect_uri: this.config.redirectUri,
                client_id: this.config.clientId,
                client_secret: this.config.clientSecret,
                code_verifier: sessionData.codeVerifier
              })
            });
            
            if (!response.ok) {
              throw new Error('Token exchange failed');
            }
            
            const tokens = await response.json();
            
            // IDトークンの検証（OpenID Connect）
            if (tokens.id_token) {
              await this.validateIdToken(tokens.id_token);
            }
            
            return tokens;
          }
          
          // トークンのリフレッシュ
          async refreshToken(
            refreshToken: string
          ): Promise<TokenResponse> {
            const response = await fetch(this.config.tokenEndpoint, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              },
              body: new URLSearchParams({
                grant_type: 'refresh_token',
                refresh_token: refreshToken,
                client_id: this.config.clientId,
                client_secret: this.config.clientSecret
              })
            });
            
            if (!response.ok) {
              throw new Error('Token refresh failed');
            }
            
            return response.json();
          }
        }
      `,
      
      // トークン管理
      tokenManagement: `
        class TokenManager {
          private readonly cache = new Map<string, CachedToken>();
          
          async getValidToken(
            userId: string
          ): Promise<string> {
            const cached = this.cache.get(userId);
            
            if (cached && !this.isExpired(cached)) {
              return cached.accessToken;
            }
            
            // トークンが期限切れまたは存在しない
            if (cached?.refreshToken) {
              try {
                const newTokens = await this.oauthClient.refreshToken(
                  cached.refreshToken
                );
                
                this.cache.set(userId, {
                  accessToken: newTokens.access_token,
                  refreshToken: newTokens.refresh_token,
                  expiresAt: Date.now() + (newTokens.expires_in * 1000)
                });
                
                return newTokens.access_token;
              } catch (error) {
                // リフレッシュ失敗、再認証が必要
                this.cache.delete(userId);
                throw new ReauthenticationRequiredError();
              }
            }
            
            throw new AuthenticationRequiredError();
          }
          
          private isExpired(token: CachedToken): boolean {
            // 5分のバッファを持って判断
            return Date.now() >= token.expiresAt - 300000;
          }
        }
      `
    };
  }
  
  // APIキー管理
  implementAPIKeyManagement(): APIKeyManagement {
    return {
      rotation: `
        class APIKeyRotation {
          async rotateKeys(): Promise<void> {
            for (const service of this.externalServices) {
              try {
                // 新しいキーの生成
                const newKey = await service.generateNewAPIKey();
                
                // 新キーのテスト
                await this.testNewKey(service, newKey);
                
                // 設定の更新
                await this.updateConfiguration(service.name, newKey);
                
                // 古いキーの無効化スケジュール
                await this.scheduleOldKeyRevocation(
                  service,
                  this.config.gracePeriod
                );
              } catch (error) {
                this.logger.error(
                  \`Key rotation failed for \${service.name}\`,
                  error
                );
              }
            }
          }
        }
      `,
      
      vaultIntegration: `
        class VaultIntegration {
          async getAPIKey(service: string): Promise<string> {
            const path = \`secret/data/external-services/\${service}\`;
            
            try {
              const response = await this.vault.read(path);
              return response.data.data.api_key;
            } catch (error) {
              if (error.statusCode === 404) {
                throw new Error(\`API key not found for \${service}\`);
              }
              throw error;
            }
          }
          
          async storeAPIKey(
            service: string,
            apiKey: string,
            metadata: Record<string, any>
          ): Promise<void> {
            const path = \`secret/data/external-services/\${service}\`;
            
            await this.vault.write(path, {
              data: {
                api_key: apiKey,
                created_at: new Date().toISOString(),
                ...metadata
              }
            });
          }
        }
      `
    };
  }
}
```

## エラーハンドリングとリトライ

### 包括的エラーハンドリング

```typescript
export class ExternalSystemErrorHandling {
  // リトライ戦略
  implementRetryStrategy(): RetryStrategyImplementation {
    return {
      exponentialBackoff: `
        class ExponentialBackoffRetry {
          async execute<T>(
            operation: () => Promise<T>,
            options: RetryOptions = {}
          ): Promise<T> {
            const config = {
              maxAttempts: options.maxAttempts || 3,
              initialDelay: options.initialDelay || 1000,
              maxDelay: options.maxDelay || 30000,
              factor: options.factor || 2,
              jitter: options.jitter !== false
            };
            
            let lastError: Error;
            let delay = config.initialDelay;
            
            for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
              try {
                return await operation();
              } catch (error) {
                lastError = error as Error;
                
                // リトライ可能か判断
                if (!this.isRetryable(error) || 
                    attempt === config.maxAttempts) {
                  throw error;
                }
                
                // ジッターの追加
                const actualDelay = config.jitter
                  ? delay * (0.5 + Math.random() * 0.5)
                  : delay;
                
                this.logger.info(
                  \`Retrying after \${actualDelay}ms (attempt \${attempt})\`
                );
                
                await this.sleep(actualDelay);
                
                // 次の遅延を計算
                delay = Math.min(delay * config.factor, config.maxDelay);
              }
            }
            
            throw lastError!;
          }
          
          private isRetryable(error: any): boolean {
            // ネットワークエラー
            if (error.code === 'ECONNRESET' || 
                error.code === 'ETIMEDOUT' ||
                error.code === 'ENOTFOUND') {
              return true;
            }
            
            // HTTPステータスコード
            if (error.statusCode) {
              // 5xxエラーはリトライ
              if (error.statusCode >= 500) return true;
              
              // 429 Too Many Requests
              if (error.statusCode === 429) return true;
              
              // 408 Request Timeout
              if (error.statusCode === 408) return true;
            }
            
            return false;
          }
        }
      `,
      
      circuitBreaker: `
        class CircuitBreaker {
          private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
          private failureCount = 0;
          private lastFailureTime?: Date;
          private successCount = 0;
          
          async execute<T>(
            operation: () => Promise<T>
          ): Promise<T> {
            if (this.state === 'OPEN') {
              if (this.shouldAttemptReset()) {
                this.state = 'HALF_OPEN';
              } else {
                throw new CircuitBreakerOpenError(
                  'Circuit breaker is open'
                );
              }
            }
            
            try {
              const result = await operation();
              this.onSuccess();
              return result;
            } catch (error) {
              this.onFailure();
              throw error;
            }
          }
          
          private onSuccess(): void {
            this.failureCount = 0;
            
            if (this.state === 'HALF_OPEN') {
              this.successCount++;
              
              if (this.successCount >= this.config.successThreshold) {
                this.state = 'CLOSED';
                this.successCount = 0;
              }
            }
          }
          
          private onFailure(): void {
            this.failureCount++;
            this.lastFailureTime = new Date();
            
            if (this.state === 'HALF_OPEN') {
              this.state = 'OPEN';
              this.successCount = 0;
            } else if (
              this.failureCount >= this.config.failureThreshold
            ) {
              this.state = 'OPEN';
            }
          }
          
          private shouldAttemptReset(): boolean {
            if (!this.lastFailureTime) return false;
            
            const timeSinceLastFailure = 
              Date.now() - this.lastFailureTime.getTime();
            
            return timeSinceLastFailure >= this.config.resetTimeout;
          }
        }
      `
    };
  }
}
```

## まとめ

外部システム連携は、現代のソフトウェアエコシステムにおいて不可欠な要素です。Parasol V5.4における成功の鍵：

1. **腐敗防止層の実装** - 内部システムの保護
2. **堅牢なエラーハンドリング** - リトライとサーキットブレーカー
3. **セキュリティの徹底** - 認証・暗号化・監視
4. **柔軟なデータ変換** - 異なるフォーマットへの対応
5. **監視とログ** - 問題の早期発見

適切に設計された外部連携は、ビジネスの成長を加速し、新たな価値を創出します。

### 次章への架橋

外部システムとの安全な連携方法を学びました。第31章では、サービス間のコントラクトとAPIバージョニングについて詳しく見ていきます。

---

## 演習問題

1. 決済プロバイダー（Stripe、PayPal、銀行振込）を統合するアダプターを設計してください。エラーハンドリングとトランザクション管理を含めてください。

2. レガシーシステム（SOAP API）を新しいREST APIとして公開するファサードを実装してください。

3. 外部APIのレート制限に対応する包括的な戦略を立案し、実装例を示してください。