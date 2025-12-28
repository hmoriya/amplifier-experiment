# 付録：第30章　外部システム連携の実装詳細

## 外部システム統合アーキテクチャ

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

## 腐敗防止層の実装

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
                method: this.mapPaymentMethod(externalData.payment_type),
                processedAt: new Date(externalData.processed_timestamp),
                metadata: this.extractMetadata(externalData)
              });
            }
            
            // ドメインモデルを外部システムの形式に変換
            toExternalFormat(payment: Payment): ExternalPaymentRequest {
              return {
                transaction_id: payment.id.value,
                amount_cents: payment.amount.toCents(),
                currency_code: payment.amount.currency.code,
                payment_type: this.mapMethodToExternal(payment.method),
                customer_id: payment.customerId.value,
                metadata: this.formatMetadata(payment.metadata)
              };
            }
            
            private mapStatus(externalStatus: string): PaymentStatus {
              const statusMap: Record<string, PaymentStatus> = {
                'APPROVED': PaymentStatus.Approved,
                'DECLINED': PaymentStatus.Declined,
                'PENDING': PaymentStatus.Pending,
                'CANCELLED': PaymentStatus.Cancelled
              };
              
              return statusMap[externalStatus] || PaymentStatus.Unknown;
            }
          }
        `,
        
        toExternal: `
          class OrderTranslator {
            // 内部の注文を外部のフォーマットに変換
            toExternalOrder(order: Order): ExternalOrderData {
              return {
                order_ref: order.id.toString(),
                customer_info: {
                  id: order.customer.id.value,
                  email: order.customer.email.value,
                  name: order.customer.name
                },
                line_items: order.items.map(item => ({
                  sku: item.product.sku.value,
                  quantity: item.quantity,
                  unit_price: item.price.amount,
                  currency: item.price.currency.code
                })),
                shipping_address: this.formatAddress(order.shippingAddress),
                billing_address: this.formatAddress(order.billingAddress),
                total_amount: order.total.toCents(),
                created_at: order.createdAt.toISOString()
              };
            }
          }
        `
      },
      
      // アダプター実装
      adapter: {
        client: `
          class ExternalPaymentAdapter implements PaymentGateway {
            constructor(
              private readonly httpClient: HttpClient,
              private readonly translator: PaymentTranslator,
              private readonly config: PaymentConfig
            ) {}
            
            async processPayment(payment: Payment): Promise<PaymentResult> {
              try {
                // ドメインモデルを外部形式に変換
                const externalRequest = this.translator.toExternalFormat(payment);
                
                // 外部APIを呼び出し
                const response = await this.httpClient.post(
                  \`\${this.config.baseUrl}/payments\`,
                  externalRequest,
                  {
                    headers: {
                      'Authorization': \`Bearer \${this.config.apiKey}\`,
                      'X-Idempotency-Key': payment.idempotencyKey
                    }
                  }
                );
                
                // レスポンスをドメインモデルに変換
                const result = this.translator.toDomainModel(response.data);
                
                return PaymentResult.success(result);
              } catch (error) {
                // エラーをドメインの例外に変換
                throw this.translateError(error);
              }
            }
            
            private translateError(error: any): DomainError {
              if (error.response?.status === 402) {
                return new InsufficientFundsError(error.response.data.message);
              }
              
              if (error.response?.status === 429) {
                return new RateLimitExceededError(
                  error.response.headers['x-rate-limit-reset']
                );
              }
              
              return new PaymentProcessingError(error.message);
            }
          }
        `,
        
        cache: `
          class CachedExternalServiceAdapter {
            constructor(
              private readonly service: ExternalService,
              private readonly cache: CacheService,
              private readonly config: CacheConfig
            ) {}
            
            async getData(key: string): Promise<ExternalData> {
              // キャッシュから取得を試みる
              const cached = await this.cache.get(this.getCacheKey(key));
              if (cached && !this.isExpired(cached)) {
                return cached.data;
              }
              
              // キャッシュミスの場合は外部サービスから取得
              const fresh = await this.service.fetchData(key);
              
              // キャッシュに保存
              await this.cache.set(
                this.getCacheKey(key),
                {
                  data: fresh,
                  timestamp: Date.now()
                },
                this.config.ttl
              );
              
              return fresh;
            }
            
            private getCacheKey(key: string): string {
              return \`external_service:\${this.service.name}:\${key}\`;
            }
            
            private isExpired(cached: CachedData): boolean {
              return Date.now() - cached.timestamp > this.config.ttl * 1000;
            }
          }
        `
      },
      
      // 検証層
      validator: {
        input: `
          class ExternalDataValidator {
            validateIncomingData(data: any): ValidationResult {
              const errors: ValidationError[] = [];
              
              // 必須フィールドの検証
              if (!data.id) {
                errors.push({
                  field: 'id',
                  message: 'Required field missing'
                });
              }
              
              // データ型の検証
              if (typeof data.amount !== 'number') {
                errors.push({
                  field: 'amount',
                  message: 'Amount must be a number'
                });
              }
              
              // ビジネスルールの検証
              if (data.amount < 0) {
                errors.push({
                  field: 'amount',
                  message: 'Amount cannot be negative'
                });
              }
              
              // 日付の検証
              if (!this.isValidDate(data.timestamp)) {
                errors.push({
                  field: 'timestamp',
                  message: 'Invalid timestamp format'
                });
              }
              
              return {
                isValid: errors.length === 0,
                errors
              };
            }
          }
        `,
        
        output: `
          class OutgoingDataValidator {
            validateOutgoingData(data: any): void {
              // 個人情報の除去を確認
              if (data.customer?.ssn) {
                throw new Error('SSN should not be sent to external service');
              }
              
              // 必須フィールドの確認
              this.assertRequired(data, ['orderId', 'amount', 'currency']);
              
              // フォーマットの検証
              this.assertFormat(data.currency, /^[A-Z]{3}$/);
              
              // 値の範囲の検証
              this.assertRange(data.amount, 0, 1000000);
            }
          }
        `
      }
    };
  }
}
```

## レジリエンスパターンの実装

<div id="resilience"></div>

```typescript
export class ResiliencePatterns {
  // サーキットブレーカー実装
  implementCircuitBreaker(): CircuitBreakerImplementation {
    return {
      states: {
        CLOSED: "正常動作中",
        OPEN: "回路遮断中",
        HALF_OPEN: "試験的復旧中"
      },
      
      implementation: `
        class CircuitBreaker {
          private state: CircuitState = CircuitState.CLOSED;
          private failureCount: number = 0;
          private lastFailureTime?: Date;
          private successCount: number = 0;
          
          constructor(
            private readonly config: CircuitBreakerConfig
          ) {}
          
          async execute<T>(operation: () => Promise<T>): Promise<T> {
            if (this.state === CircuitState.OPEN) {
              if (this.shouldAttemptReset()) {
                this.state = CircuitState.HALF_OPEN;
              } else {
                throw new CircuitOpenError('Circuit breaker is OPEN');
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
            
            if (this.state === CircuitState.HALF_OPEN) {
              this.successCount++;
              if (this.successCount >= this.config.successThreshold) {
                this.state = CircuitState.CLOSED;
                this.successCount = 0;
              }
            }
          }
          
          private onFailure(): void {
            this.failureCount++;
            this.lastFailureTime = new Date();
            
            if (this.failureCount >= this.config.failureThreshold) {
              this.state = CircuitState.OPEN;
              this.successCount = 0;
            }
          }
          
          private shouldAttemptReset(): boolean {
            return (
              this.lastFailureTime &&
              Date.now() - this.lastFailureTime.getTime() >= this.config.timeout
            );
          }
        }
      `,
      
      configuration: {
        failureThreshold: 5,
        successThreshold: 3,
        timeout: 60000, // 60秒
        monitoringWindow: 10000 // 10秒
      }
    };
  }
  
  // リトライ戦略
  implementRetryStrategy(): RetryStrategyImplementation {
    return {
      strategies: {
        exponentialBackoff: `
          class ExponentialBackoffRetry {
            async execute<T>(
              operation: () => Promise<T>,
              options: RetryOptions
            ): Promise<T> {
              let lastError: Error;
              
              for (let attempt = 0; attempt < options.maxAttempts; attempt++) {
                try {
                  return await operation();
                } catch (error) {
                  lastError = error;
                  
                  if (!this.isRetryable(error)) {
                    throw error;
                  }
                  
                  if (attempt < options.maxAttempts - 1) {
                    const delay = this.calculateDelay(attempt, options);
                    await this.sleep(delay);
                  }
                }
              }
              
              throw new MaxRetriesExceededError(lastError!);
            }
            
            private calculateDelay(attempt: number, options: RetryOptions): number {
              const exponentialDelay = Math.min(
                options.baseDelay * Math.pow(2, attempt),
                options.maxDelay
              );
              
              // ジッターを追加（衝突回避）
              const jitter = Math.random() * options.jitterFactor * exponentialDelay;
              
              return exponentialDelay + jitter;
            }
            
            private isRetryable(error: any): boolean {
              // 一時的なエラーのみリトライ
              if (error.code === 'ECONNRESET' || 
                  error.code === 'ETIMEDOUT' ||
                  error.code === 'ENOTFOUND') {
                return true;
              }
              
              // HTTPステータスコードによる判定
              const status = error.response?.status;
              return status === 429 || status === 503 || status >= 500;
            }
          }
        `,
        
        linearBackoff: `
          class LinearBackoffRetry {
            async execute<T>(
              operation: () => Promise<T>,
              maxAttempts: number = 3,
              delay: number = 1000
            ): Promise<T> {
              for (let i = 0; i < maxAttempts; i++) {
                try {
                  return await operation();
                } catch (error) {
                  if (i === maxAttempts - 1) throw error;
                  await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
                }
              }
              throw new Error('Unreachable');
            }
          }
        `
      },
      
      configuration: {
        maxAttempts: 3,
        baseDelay: 1000,
        maxDelay: 30000,
        jitterFactor: 0.1
      }
    };
  }
  
  // タイムアウト制御
  implementTimeoutControl(): TimeoutImplementation {
    return {
      patterns: {
        simple: `
          async function withTimeout<T>(
            operation: Promise<T>,
            timeout: number
          ): Promise<T> {
            const timeoutPromise = new Promise<never>((_, reject) => {
              setTimeout(() => reject(new TimeoutError()), timeout);
            });
            
            return Promise.race([operation, timeoutPromise]);
          }
        `,
        
        cascading: `
          class CascadingTimeout {
            constructor(
              private readonly timeouts: TimeoutConfig[]
            ) {}
            
            async execute<T>(operation: () => Promise<T>): Promise<T> {
              const controller = new AbortController();
              
              // 各タイムアウトを設定
              const timers = this.timeouts.map(config => {
                return setTimeout(() => {
                  if (config.action === 'abort') {
                    controller.abort();
                  } else if (config.action === 'warn') {
                    console.warn(\`Timeout warning: \${config.message}\`);
                  }
                }, config.duration);
              });
              
              try {
                return await operation();
              } finally {
                // タイマーをクリーンアップ
                timers.forEach(timer => clearTimeout(timer));
              }
            }
          }
        `,
        
        adaptive: `
          class AdaptiveTimeout {
            private history: number[] = [];
            private readonly maxHistory = 100;
            
            calculateTimeout(): number {
              if (this.history.length === 0) {
                return this.defaultTimeout;
              }
              
              // 過去の応答時間の95パーセンタイルを計算
              const sorted = [...this.history].sort((a, b) => a - b);
              const p95Index = Math.floor(sorted.length * 0.95);
              const p95 = sorted[p95Index];
              
              // 安全マージンを追加
              return Math.min(p95 * 1.5, this.maxTimeout);
            }
            
            recordResponseTime(duration: number): void {
              this.history.push(duration);
              if (this.history.length > this.maxHistory) {
                this.history.shift();
              }
            }
          }
        `
      }
    };
  }
  
  // バルクヘッド（区画化）パターン
  implementBulkhead(): BulkheadImplementation {
    return {
      threadPool: `
        class ThreadPoolBulkhead {
          private activeRequests = 0;
          private queue: QueueItem[] = [];
          
          constructor(
            private readonly maxConcurrent: number,
            private readonly maxQueueSize: number
          ) {}
          
          async execute<T>(operation: () => Promise<T>): Promise<T> {
            if (this.activeRequests >= this.maxConcurrent) {
              if (this.queue.length >= this.maxQueueSize) {
                throw new BulkheadRejectedError('Bulkhead queue is full');
              }
              
              // キューに追加
              return new Promise((resolve, reject) => {
                this.queue.push({ operation, resolve, reject });
              });
            }
            
            this.activeRequests++;
            
            try {
              const result = await operation();
              this.processQueue();
              return result;
            } catch (error) {
              this.processQueue();
              throw error;
            } finally {
              this.activeRequests--;
            }
          }
          
          private processQueue(): void {
            if (this.queue.length > 0 && this.activeRequests < this.maxConcurrent) {
              const item = this.queue.shift()!;
              this.execute(item.operation)
                .then(item.resolve)
                .catch(item.reject);
            }
          }
        }
      `,
      
      semaphore: `
        class SemaphoreBulkhead {
          private permits: number;
          
          constructor(maxPermits: number) {
            this.permits = maxPermits;
          }
          
          async acquire(): Promise<void> {
            while (this.permits <= 0) {
              await new Promise(resolve => setTimeout(resolve, 10));
            }
            this.permits--;
          }
          
          release(): void {
            this.permits++;
          }
          
          async execute<T>(operation: () => Promise<T>): Promise<T> {
            await this.acquire();
            try {
              return await operation();
            } finally {
              this.release();
            }
          }
        }
      `
    };
  }
}
```

## セキュリティ実装のベストプラクティス

<div id="security"></div>

```typescript
export class ExternalSecurityImplementation {
  // OAuth 2.0実装
  implementOAuth2(): OAuth2Implementation {
    return {
      clientCredentials: `
        class OAuth2Client {
          private accessToken?: string;
          private tokenExpiry?: Date;
          
          constructor(
            private readonly config: OAuth2Config,
            private readonly httpClient: HttpClient
          ) {}
          
          async getAccessToken(): Promise<string> {
            if (this.isTokenValid()) {
              return this.accessToken!;
            }
            
            const response = await this.httpClient.post(
              this.config.tokenEndpoint,
              {
                grant_type: 'client_credentials',
                client_id: this.config.clientId,
                client_secret: this.config.clientSecret,
                scope: this.config.scope
              },
              {
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded'
                }
              }
            );
            
            this.accessToken = response.data.access_token;
            this.tokenExpiry = new Date(
              Date.now() + response.data.expires_in * 1000
            );
            
            return this.accessToken;
          }
          
          private isTokenValid(): boolean {
            return !!(
              this.accessToken &&
              this.tokenExpiry &&
              this.tokenExpiry > new Date()
            );
          }
          
          async makeAuthenticatedRequest(
            url: string,
            options: RequestOptions = {}
          ): Promise<any> {
            const token = await this.getAccessToken();
            
            return this.httpClient.request({
              ...options,
              url,
              headers: {
                ...options.headers,
                'Authorization': \`Bearer \${token}\`
              }
            });
          }
        }
      `,
      
      authorizationCode: `
        class OAuth2AuthorizationFlow {
          constructor(
            private readonly config: OAuth2Config,
            private readonly stateStore: StateStore
          ) {}
          
          generateAuthorizationUrl(redirectUri: string): string {
            const state = this.generateState();
            this.stateStore.save(state, { redirectUri });
            
            const params = new URLSearchParams({
              response_type: 'code',
              client_id: this.config.clientId,
              redirect_uri: redirectUri,
              scope: this.config.scope,
              state: state
            });
            
            return \`\${this.config.authorizationEndpoint}?\${params}\`;
          }
          
          async handleCallback(
            code: string,
            state: string,
            redirectUri: string
          ): Promise<TokenResponse> {
            // State検証
            const savedState = await this.stateStore.get(state);
            if (!savedState || savedState.redirectUri !== redirectUri) {
              throw new Error('Invalid state parameter');
            }
            
            // トークン交換
            const response = await this.httpClient.post(
              this.config.tokenEndpoint,
              {
                grant_type: 'authorization_code',
                code: code,
                redirect_uri: redirectUri,
                client_id: this.config.clientId,
                client_secret: this.config.clientSecret
              }
            );
            
            // Stateをクリーンアップ
            await this.stateStore.delete(state);
            
            return response.data;
          }
          
          private generateState(): string {
            return crypto.randomBytes(32).toString('base64url');
          }
        }
      `
    };
  }
  
  // APIキー管理
  implementApiKeyManagement(): ApiKeyManagementImplementation {
    return {
      storage: `
        class SecureApiKeyStorage {
          constructor(
            private readonly encryption: EncryptionService,
            private readonly keyVault: KeyVaultService
          ) {}
          
          async storeApiKey(
            service: string,
            apiKey: string,
            metadata?: ApiKeyMetadata
          ): Promise<void> {
            // APIキーを暗号化
            const encrypted = await this.encryption.encrypt(apiKey);
            
            // メタデータと共に保存
            await this.keyVault.store(\`api-key:\${service}\`, {
              encryptedKey: encrypted,
              metadata: {
                ...metadata,
                createdAt: new Date(),
                lastRotated: new Date()
              }
            });
          }
          
          async getApiKey(service: string): Promise<string> {
            const data = await this.keyVault.retrieve(\`api-key:\${service}\`);
            if (!data) {
              throw new Error(\`API key not found for service: \${service}\`);
            }
            
            // 有効期限チェック
            if (data.metadata.expiresAt && data.metadata.expiresAt < new Date()) {
              throw new Error(\`API key expired for service: \${service}\`);
            }
            
            // 復号化して返す
            return this.encryption.decrypt(data.encryptedKey);
          }
          
          async rotateApiKey(
            service: string,
            newApiKey: string
          ): Promise<void> {
            // 古いキーを取得（履歴保存のため）
            const oldData = await this.keyVault.retrieve(\`api-key:\${service}\`);
            
            if (oldData) {
              // 履歴に保存
              await this.keyVault.store(
                \`api-key-history:\${service}:\${Date.now()}\`,
                oldData
              );
            }
            
            // 新しいキーを保存
            await this.storeApiKey(service, newApiKey, {
              rotatedFrom: oldData?.metadata.id
            });
          }
        }
      `,
      
      rotation: `
        class ApiKeyRotationService {
          constructor(
            private readonly keyStorage: SecureApiKeyStorage,
            private readonly notifier: NotificationService
          ) {}
          
          async scheduleRotation(
            service: string,
            interval: number
          ): Promise<void> {
            setInterval(async () => {
              try {
                await this.checkAndRotate(service);
              } catch (error) {
                await this.notifier.sendAlert({
                  severity: 'critical',
                  message: \`Failed to rotate API key for \${service}\`,
                  error
                });
              }
            }, interval);
          }
          
          private async checkAndRotate(service: string): Promise<void> {
            const metadata = await this.keyStorage.getMetadata(service);
            
            const daysSinceRotation = 
              (Date.now() - metadata.lastRotated.getTime()) / (1000 * 60 * 60 * 24);
            
            if (daysSinceRotation >= 90) {
              await this.notifier.sendWarning({
                message: \`API key for \${service} needs rotation\`,
                daysSinceRotation
              });
            }
          }
        }
      `
    };
  }
  
  // mTLS実装
  implementMutualTLS(): MutualTLSImplementation {
    return {
      client: `
        class MutualTLSClient {
          private agent: https.Agent;
          
          constructor(
            private readonly config: MutualTLSConfig
          ) {
            this.agent = new https.Agent({
              cert: fs.readFileSync(config.clientCertPath),
              key: fs.readFileSync(config.clientKeyPath),
              ca: fs.readFileSync(config.caCertPath),
              rejectUnauthorized: true
            });
          }
          
          async request(options: RequestOptions): Promise<any> {
            return axios({
              ...options,
              httpsAgent: this.agent,
              // ピンニング検証
              validateStatus: (status) => {
                return status >= 200 && status < 300;
              }
            });
          }
          
          validateServerCertificate(cert: any): boolean {
            // CN検証
            if (cert.subject.CN !== this.config.expectedServerCN) {
              return false;
            }
            
            // 有効期限検証
            const now = new Date();
            if (now < new Date(cert.valid_from) || now > new Date(cert.valid_to)) {
              return false;
            }
            
            // CA検証
            return cert.issuer.CN === this.config.expectedCACN;
          }
        }
      `,
      
      server: `
        class MutualTLSServer {
          createServer(app: Express): https.Server {
            const options = {
              cert: fs.readFileSync(this.config.serverCertPath),
              key: fs.readFileSync(this.config.serverKeyPath),
              ca: fs.readFileSync(this.config.caCertPath),
              requestCert: true,
              rejectUnauthorized: true
            };
            
            const server = https.createServer(options, app);
            
            // クライアント証明書の検証
            server.on('tlsClientError', (err, socket) => {
              console.error('TLS client error:', err);
              socket.destroy();
            });
            
            return server;
          }
          
          validateClientCertificate(req: Request): void {
            const cert = req.socket.getPeerCertificate();
            
            if (!cert || !cert.subject) {
              throw new UnauthorizedError('Client certificate required');
            }
            
            // 許可リストとの照合
            if (!this.isAllowedClient(cert.subject.CN)) {
              throw new UnauthorizedError('Client not authorized');
            }
            
            // 証明書の有効性確認
            if (!this.isCertificateValid(cert)) {
              throw new UnauthorizedError('Invalid client certificate');
            }
          }
        }
      `
    };
  }
}
```

## 外部サービスのモニタリング

```typescript
export class ExternalServiceMonitoring {
  // SLA監視
  implementSLAMonitoring(): SLAMonitoringImplementation {
    return {
      metrics: {
        availability: `
          class AvailabilityMonitor {
            private uptimeData: Map<string, UptimeRecord> = new Map();
            
            async checkAvailability(service: ExternalService): Promise<boolean> {
              try {
                const start = Date.now();
                const response = await this.healthCheck(service);
                const duration = Date.now() - start;
                
                this.recordSuccess(service.name, duration);
                return true;
              } catch (error) {
                this.recordFailure(service.name, error);
                return false;
              }
            }
            
            calculateUptime(service: string, period: number): number {
              const record = this.uptimeData.get(service);
              if (!record) return 0;
              
              const totalChecks = record.successCount + record.failureCount;
              if (totalChecks === 0) return 0;
              
              return (record.successCount / totalChecks) * 100;
            }
            
            private recordSuccess(service: string, responseTime: number): void {
              const record = this.getOrCreateRecord(service);
              record.successCount++;
              record.responseTimes.push(responseTime);
              
              // 応答時間の統計を更新
              this.updateResponseTimeStats(record);
            }
            
            private updateResponseTimeStats(record: UptimeRecord): void {
              const times = record.responseTimes;
              times.sort((a, b) => a - b);
              
              record.stats = {
                min: times[0],
                max: times[times.length - 1],
                avg: times.reduce((a, b) => a + b, 0) / times.length,
                p50: this.percentile(times, 50),
                p95: this.percentile(times, 95),
                p99: this.percentile(times, 99)
              };
            }
          }
        `,
        
        performance: `
          class PerformanceMonitor {
            private metricsBuffer: MetricBuffer = new MetricBuffer();
            
            async measureOperation<T>(
              service: string,
              operation: string,
              fn: () => Promise<T>
            ): Promise<T> {
              const startTime = process.hrtime.bigint();
              const startCpu = process.cpuUsage();
              const startMem = process.memoryUsage();
              
              try {
                const result = await fn();
                
                const duration = Number(process.hrtime.bigint() - startTime) / 1e6;
                const cpuUsage = process.cpuUsage(startCpu);
                const memUsage = process.memoryUsage();
                
                this.recordMetrics({
                  service,
                  operation,
                  duration,
                  cpu: cpuUsage,
                  memory: {
                    heapUsed: memUsage.heapUsed - startMem.heapUsed,
                    external: memUsage.external - startMem.external
                  },
                  timestamp: new Date()
                });
                
                return result;
              } catch (error) {
                this.recordError(service, operation, error);
                throw error;
              }
            }
            
            getPerformanceReport(service: string): PerformanceReport {
              const metrics = this.metricsBuffer.getMetrics(service);
              
              return {
                service,
                period: this.metricsBuffer.getPeriod(),
                operations: this.aggregateByOperation(metrics),
                trends: this.calculateTrends(metrics),
                anomalies: this.detectAnomalies(metrics)
              };
            }
          }
        `
      },
      
      alerting: `
        class ExternalServiceAlerting {
          private alertThresholds: Map<string, AlertThreshold> = new Map();
          
          configureAlerts(service: string, thresholds: AlertThreshold): void {
            this.alertThresholds.set(service, thresholds);
          }
          
          async checkAndAlert(service: string, metrics: ServiceMetrics): Promise<void> {
            const thresholds = this.alertThresholds.get(service);
            if (!thresholds) return;
            
            const alerts: Alert[] = [];
            
            // 可用性チェック
            if (metrics.availability < thresholds.minAvailability) {
              alerts.push({
                severity: 'critical',
                service,
                metric: 'availability',
                value: metrics.availability,
                threshold: thresholds.minAvailability,
                message: \`Service availability (\${metrics.availability}%) below threshold\`
              });
            }
            
            // レスポンスタイムチェック
            if (metrics.p95ResponseTime > thresholds.maxResponseTime) {
              alerts.push({
                severity: 'warning',
                service,
                metric: 'response_time_p95',
                value: metrics.p95ResponseTime,
                threshold: thresholds.maxResponseTime,
                message: \`P95 response time (\${metrics.p95ResponseTime}ms) exceeds threshold\`
              });
            }
            
            // エラー率チェック
            if (metrics.errorRate > thresholds.maxErrorRate) {
              alerts.push({
                severity: 'critical',
                service,
                metric: 'error_rate',
                value: metrics.errorRate,
                threshold: thresholds.maxErrorRate,
                message: \`Error rate (\${metrics.errorRate}%) exceeds threshold\`
              });
            }
            
            // アラート送信
            for (const alert of alerts) {
              await this.sendAlert(alert);
            }
          }
          
          private async sendAlert(alert: Alert): Promise<void> {
            // 重複アラートの抑制
            if (this.isDuplicateAlert(alert)) {
              return;
            }
            
            // アラート送信
            await Promise.all([
              this.notificationService.sendEmail(alert),
              this.notificationService.sendSlack(alert),
              this.incidentManager.createIncident(alert)
            ]);
            
            // アラート履歴に記録
            this.recordAlert(alert);
          }
        }
      `
    };
  }
}
```