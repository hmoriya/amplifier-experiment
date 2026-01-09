# Phase 6: 明治安田生命保険の実装品質

## 1. コード生成標準

### 1.1 開発標準の策定

#### コーディング規約
```yaml
TypeScript標準:
  命名規則:
    - クラス: PascalCase
    - インターフェース: PascalCase（Iプレフィックスなし）
    - メソッド・関数: camelCase
    - 定数: UPPER_SNAKE_CASE
    - ファイル名: kebab-case
  
  ディレクトリ構造:
    src/
      domain/           # ドメイン層
        contract/       # 契約BC
          entities/
          value-objects/
          repositories/
          services/
        shared/         # 共有ドメイン
      
      application/      # アプリケーション層
        use-cases/
        dto/
        mappers/
      
      infrastructure/   # インフラ層
        persistence/
        messaging/
        external/
      
      presentation/     # プレゼンテーション層
        graphql/
        rest/
        grpc/
```

#### ESLint設定
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:security/recommended',
    'prettier'
  ],
  plugins: [
    '@typescript-eslint',
    'security',
    'sonarjs'
  ],
  rules: {
    // 複雑度制限
    'complexity': ['error', 10],
    'max-depth': ['error', 3],
    'max-lines-per-function': ['error', 50],
    'max-params': ['error', 4],
    
    // セキュリティ
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-regexp': 'error',
    
    // 品質
    'sonarjs/cognitive-complexity': ['error', 15],
    'sonarjs/no-duplicate-string': 'error',
    'sonarjs/no-identical-functions': 'error',
    
    // TypeScript固有
    '@typescript-eslint/explicit-function-return-type': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/strict-boolean-expressions': 'error'
  }
};
```

### 1.2 コード生成テンプレート

#### Entity生成テンプレート
```typescript
// templates/entity.template.ts
export const entityTemplate = `
import { Entity, AggregateRoot, DomainEvent } from '@domain/core';
import { Result } from '@shared/core';

export interface {{EntityName}}Props {
  // TODO: Define properties
}

export class {{EntityName}} extends AggregateRoot<{{EntityName}}Props> {
  
  private constructor(props: {{EntityName}}Props, id?: string) {
    super(props, id);
  }
  
  public static create(props: {{EntityName}}Props): Result<{{EntityName}}> {
    // TODO: Add validation logic
    const guardResult = Guard.againstNullOrUndefinedBulk([
      { argument: props.field, argumentName: 'field' }
    ]);
    
    if (guardResult.isFailure) {
      return Result.fail<{{EntityName}}>(guardResult.getErrorValue());
    }
    
    const entity = new {{EntityName}}(props);
    
    // Emit domain event
    entity.addDomainEvent(new {{EntityName}}Created(entity));
    
    return Result.ok<{{EntityName}}>(entity);
  }
  
  // Business logic methods
  public doSomething(): Result<void> {
    // TODO: Implement business logic
    return Result.ok();
  }
}

// Domain Events
export class {{EntityName}}Created implements DomainEvent {
  public dateTimeOccurred: Date;
  
  constructor(public readonly {{camelCase EntityName}}: {{EntityName}}) {
    this.dateTimeOccurred = new Date();
  }
  
  getAggregateId(): string {
    return this.{{camelCase EntityName}}.id.toString();
  }
}
`;

// Code Generator
export class EntityGenerator {
  generate(entityName: string, props: PropertyDefinition[]): string {
    const template = entityTemplate
      .replace(/{{EntityName}}/g, entityName)
      .replace(/{{camelCase EntityName}}/g, camelCase(entityName));
    
    // TODO: Replace property definitions
    
    return template;
  }
}
```

#### Use Case生成テンプレート
```typescript
// templates/use-case.template.ts
export const useCaseTemplate = `
import { UseCase } from '@application/core';
import { Result, left, right } from '@shared/core';
import { AppError } from '@shared/errors';

export interface {{UseCaseName}}DTO {
  // TODO: Define input properties
}

export type {{UseCaseName}}Response = Either<
  AppError.UnexpectedError | AppError.ValidationError,
  Result<void>
>;

export class {{UseCaseName}} implements UseCase<{{UseCaseName}}DTO, {{UseCaseName}}Response> {
  
  constructor(
    // TODO: Inject dependencies
    private readonly repository: Repository
  ) {}
  
  async execute(request: {{UseCaseName}}DTO): Promise<{{UseCaseName}}Response> {
    try {
      // 1. Validate input
      const validationResult = this.validate(request);
      if (validationResult.isFailure) {
        return left(new AppError.ValidationError(validationResult.error));
      }
      
      // 2. Execute business logic
      // TODO: Implement use case logic
      
      // 3. Return success
      return right(Result.ok());
      
    } catch (error) {
      return left(new AppError.UnexpectedError(error));
    }
  }
  
  private validate(request: {{UseCaseName}}DTO): Result<void> {
    // TODO: Implement validation
    return Result.ok();
  }
}
`;
```

### 1.3 自動生成CLI

```typescript
// cli/generate-code.ts
import { Command } from 'commander';
import { EntityGenerator } from './generators/entity-generator';
import { UseCaseGenerator } from './generators/use-case-generator';

const program = new Command();

program
  .command('entity <name>')
  .description('Generate a new domain entity')
  .option('-p, --properties <props>', 'Entity properties as JSON')
  .action(async (name, options) => {
    const generator = new EntityGenerator();
    const code = generator.generate(name, options.properties);
    
    await fs.writeFile(
      `src/domain/${kebabCase(name)}/entities/${kebabCase(name)}.entity.ts`,
      code
    );
    
    console.log(`✅ Entity ${name} generated successfully`);
  });

program
  .command('use-case <name>')
  .description('Generate a new use case')
  .option('-d, --domain <domain>', 'Domain context')
  .action(async (name, options) => {
    const generator = new UseCaseGenerator();
    const code = generator.generate(name, options.domain);
    
    await fs.writeFile(
      `src/application/use-cases/${kebabCase(name)}.use-case.ts`,
      code
    );
    
    console.log(`✅ Use case ${name} generated successfully`);
  });

program.parse();
```

## 2. テスト戦略

### 2.1 テストピラミッド

```yaml
テストレベル:
  単体テスト (60%):
    - ドメインロジック
    - 値オブジェクト
    - ユーティリティ関数
    - 純粋関数
  
  統合テスト (30%):
    - リポジトリ
    - 外部API連携
    - データベース操作
    - メッセージング
  
  E2Eテスト (10%):
    - クリティカルパス
    - 主要ユーザーシナリオ
    - APIエンドポイント
```

### 2.2 単体テスト実装

#### ドメインエンティティテスト
```typescript
// tests/domain/contract/contract.spec.ts
describe('Contract Entity', () => {
  describe('create', () => {
    it('有効なデータで契約を作成できること', () => {
      // Arrange
      const props: CreateContractProps = {
        policyHolderId: 'customer-123',
        productId: 'product-456',
        coverages: [
          {
            coverageType: CoverageType.DEATH,
            benefitAmount: Money.create(10000000, 'JPY')
          }
        ],
        effectiveDate: new Date('2024-01-01')
      };
      
      // Act
      const result = Contract.create(props);
      
      // Assert
      expect(result.isSuccess).toBe(true);
      expect(result.getValue()).toBeInstanceOf(Contract);
      expect(result.getValue().status).toBe(ContractStatus.PENDING);
    });
    
    it('無効なデータで契約作成が失敗すること', () => {
      // Arrange
      const props: CreateContractProps = {
        policyHolderId: '',  // 無効
        productId: 'product-456',
        coverages: [],       // 空配列
        effectiveDate: new Date('2020-01-01') // 過去日付
      };
      
      // Act
      const result = Contract.create(props);
      
      // Assert
      expect(result.isFailure).toBe(true);
      expect(result.error).toContain('契約者IDが必要です');
    });
  });
  
  describe('activateContract', () => {
    it('条件を満たす場合、契約を有効化できること', () => {
      // Arrange
      const contract = makeValidContract();
      const premium = Premium.create({
        amount: Money.create(10000, 'JPY'),
        status: PremiumStatus.PAID
      });
      contract.addPremium(premium);
      
      // Act
      const result = contract.activateContract();
      
      // Assert
      expect(result.isSuccess).toBe(true);
      expect(contract.status).toBe(ContractStatus.ACTIVE);
      expect(contract.getUncommittedEvents()).toContainEqual(
        expect.objectContaining({
          constructor: { name: 'ContractActivated' }
        })
      );
    });
  });
});
```

#### ユースケーステスト
```typescript
// tests/application/create-contract.use-case.spec.ts
describe('CreateContractUseCase', () => {
  let useCase: CreateContractUseCase;
  let mockContractRepo: jest.Mocked<ContractRepository>;
  let mockProductService: jest.Mocked<ProductService>;
  let mockCustomerService: jest.Mocked<CustomerService>;
  let mockEventBus: jest.Mocked<EventBus>;
  
  beforeEach(() => {
    mockContractRepo = createMock<ContractRepository>();
    mockProductService = createMock<ProductService>();
    mockCustomerService = createMock<CustomerService>();
    mockEventBus = createMock<EventBus>();
    
    useCase = new CreateContractUseCase(
      mockContractRepo,
      mockProductService,
      mockCustomerService,
      mockEventBus
    );
  });
  
  it('正常に契約を作成できること', async () => {
    // Arrange
    const command: CreateContractCommand = {
      customerId: 'customer-123',
      productId: 'product-456',
      coverages: [...],
      effectiveDate: new Date('2024-01-01')
    };
    
    mockCustomerService.findById.mockResolvedValue(mockCustomer);
    mockProductService.findById.mockResolvedValue(mockProduct);
    mockContractRepo.save.mockResolvedValue(undefined);
    mockEventBus.publishAll.mockResolvedValue(undefined);
    
    // Act
    const result = await useCase.execute(command);
    
    // Assert
    expect(result.isSuccess).toBe(true);
    expect(mockContractRepo.save).toHaveBeenCalledTimes(1);
    expect(mockEventBus.publishAll).toHaveBeenCalledWith(
      expect.arrayContaining([
        expect.objectContaining({
          constructor: { name: 'ContractCreated' }
        })
      ])
    );
  });
});
```

### 2.3 統合テスト実装

```typescript
// tests/integration/contract-repository.integration.spec.ts
describe('ContractRepository Integration', () => {
  let repository: ContractRepository;
  let dataSource: DataSource;
  
  beforeAll(async () => {
    // テスト用データベース接続
    dataSource = await createTestDataSource();
    repository = new ContractRepositoryImpl(dataSource);
  });
  
  afterAll(async () => {
    await dataSource.destroy();
  });
  
  beforeEach(async () => {
    // データクリーンアップ
    await cleanDatabase(dataSource);
  });
  
  it('契約を保存して取得できること', async () => {
    // Arrange
    const contract = Contract.create({
      policyHolderId: 'customer-123',
      productId: 'product-456',
      coverages: [...],
      effectiveDate: new Date()
    }).getValue();
    
    // Act
    await repository.save(contract);
    const retrieved = await repository.findById(contract.id);
    
    // Assert
    expect(retrieved).toBeDefined();
    expect(retrieved?.id.equals(contract.id)).toBe(true);
    expect(retrieved?.policyHolderId).toBe('customer-123');
  });
  
  it('イベントも含めて保存されること', async () => {
    // Arrange
    const contract = Contract.create({...}).getValue();
    contract.activateContract();
    
    // Act
    await repository.save(contract);
    
    // Assert
    const events = await dataSource
      .getRepository(EventEntity)
      .find({ where: { aggregateId: contract.id.value } });
    
    expect(events).toHaveLength(2); // Created + Activated
    expect(events[0].eventType).toBe('ContractCreated');
    expect(events[1].eventType).toBe('ContractActivated');
  });
});
```

### 2.4 E2Eテスト実装

```typescript
// tests/e2e/contract-lifecycle.e2e.spec.ts
describe('契約ライフサイクルE2E', () => {
  let app: INestApplication;
  let token: string;
  
  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule]
    }).compile();
    
    app = moduleRef.createNestApplication();
    await app.init();
    
    // 認証トークン取得
    token = await getTestAuthToken(app);
  });
  
  afterAll(async () => {
    await app.close();
  });
  
  it('契約の作成から有効化までのフロー', async () => {
    // 1. 契約作成
    const createResponse = await request(app.getHttpServer())
      .post('/api/v1/contracts')
      .set('Authorization', `Bearer ${token}`)
      .send({
        customerId: 'test-customer',
        productId: 'test-product',
        coverages: [{
          type: 'DEATH',
          amount: 10000000
        }],
        effectiveDate: '2024-01-01'
      })
      .expect(201);
    
    const contractId = createResponse.body.id;
    
    // 2. 保険料支払い記録
    await request(app.getHttpServer())
      .post(`/api/v1/contracts/${contractId}/premiums`)
      .set('Authorization', `Bearer ${token}`)
      .send({
        amount: 50000,
        paymentMethod: 'BANK_TRANSFER',
        paymentDate: '2024-01-01'
      })
      .expect(201);
    
    // 3. 契約有効化
    await request(app.getHttpServer())
      .post(`/api/v1/contracts/${contractId}/activate`)
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
    
    // 4. 状態確認
    const statusResponse = await request(app.getHttpServer())
      .get(`/api/v1/contracts/${contractId}`)
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
    
    expect(statusResponse.body.status).toBe('ACTIVE');
    expect(statusResponse.body.effectiveDate).toBe('2024-01-01');
  });
});
```

## 3. 非機能要件の実装

### 3.1 パフォーマンス最適化

#### データベース最適化
```sql
-- インデックス設計
CREATE INDEX idx_contracts_policy_holder 
  ON contracts(policy_holder_id) 
  WHERE status = 'ACTIVE';

CREATE INDEX idx_contracts_effective_date 
  ON contracts(effective_date DESC) 
  INCLUDE (contract_number, status);

CREATE INDEX idx_claims_contract_status 
  ON claims(contract_id, status) 
  WHERE status IN ('SUBMITTED', 'UNDER_REVIEW');

-- パーティショニング
CREATE TABLE contracts_2024 PARTITION OF contracts
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
  
-- マテリアライズドビュー
CREATE MATERIALIZED VIEW contract_summary AS
SELECT 
  c.id,
  c.contract_number,
  c.policy_holder_id,
  c.status,
  c.effective_date,
  COUNT(cov.id) as coverage_count,
  SUM(cov.benefit_amount) as total_benefit
FROM contracts c
JOIN coverages cov ON c.id = cov.contract_id
WHERE c.status = 'ACTIVE'
GROUP BY c.id;

CREATE UNIQUE INDEX ON contract_summary(id);
REFRESH MATERIALIZED VIEW CONCURRENTLY contract_summary;
```

#### キャッシング戦略
```typescript
// Redis キャッシング実装
export class CachingService {
  private redis: Redis;
  private defaultTTL = 3600; // 1時間
  
  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    if (!cached) return null;
    
    return JSON.parse(cached) as T;
  }
  
  async set<T>(
    key: string, 
    value: T, 
    ttl: number = this.defaultTTL
  ): Promise<void> {
    await this.redis.setex(
      key, 
      ttl, 
      JSON.stringify(value)
    );
  }
  
  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}

// キャッシュを利用したリポジトリ
export class CachedContractRepository implements ContractRepository {
  constructor(
    private repository: ContractRepository,
    private cache: CachingService
  ) {}
  
  async findById(id: ContractId): Promise<Contract | null> {
    const cacheKey = `contract:${id.value}`;
    
    // キャッシュチェック
    const cached = await this.cache.get<Contract>(cacheKey);
    if (cached) {
      return this.mapper.toDomain(cached);
    }
    
    // DBから取得
    const contract = await this.repository.findById(id);
    if (contract) {
      await this.cache.set(cacheKey, contract, 3600);
    }
    
    return contract;
  }
  
  async save(contract: Contract): Promise<void> {
    await this.repository.save(contract);
    
    // キャッシュ無効化
    await this.cache.invalidate(`contract:${contract.id.value}*`);
  }
}
```

### 3.2 セキュリティ実装

#### 入力検証とサニタイゼーション
```typescript
// 入力検証デコレータ
export function Validate(schema: Joi.Schema) {
  return function (
    target: any,
    propertyName: string,
    descriptor: PropertyDescriptor
  ) {
    const method = descriptor.value;
    
    descriptor.value = async function (...args: any[]) {
      const [request] = args;
      const { error } = schema.validate(request, {
        abortEarly: false,
        stripUnknown: true
      });
      
      if (error) {
        throw new ValidationError(error.details);
      }
      
      return method.apply(this, args);
    };
  };
}

// 使用例
export class ContractController {
  @Post()
  @Validate(createContractSchema)
  async createContract(
    @Body() dto: CreateContractDTO
  ): Promise<ContractResponse> {
    // DTOは既に検証済み
    return this.useCase.execute(dto);
  }
}

// XSS対策
export class SanitizationService {
  sanitizeHtml(input: string): string {
    return DOMPurify.sanitize(input, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'em'],
      ALLOWED_ATTR: []
    });
  }
  
  sanitizeFilename(filename: string): string {
    return filename
      .replace(/[^a-z0-9\-_.]/gi, '_')
      .substring(0, 255);
  }
}
```

#### 監査ログ実装
```typescript
// 監査ログデコレータ
export function AuditLog(action: string) {
  return function (
    target: any,
    propertyName: string,
    descriptor: PropertyDescriptor
  ) {
    const method = descriptor.value;
    
    descriptor.value = async function (...args: any[]) {
      const context = ExecutionContext.current();
      const startTime = Date.now();
      
      try {
        const result = await method.apply(this, args);
        
        await AuditLogger.log({
          action,
          userId: context.userId,
          resource: target.constructor.name,
          method: propertyName,
          args: sanitizeArgs(args),
          result: 'SUCCESS',
          duration: Date.now() - startTime,
          timestamp: new Date()
        });
        
        return result;
      } catch (error) {
        await AuditLogger.log({
          action,
          userId: context.userId,
          resource: target.constructor.name,
          method: propertyName,
          args: sanitizeArgs(args),
          result: 'FAILURE',
          error: error.message,
          duration: Date.now() - startTime,
          timestamp: new Date()
        });
        
        throw error;
      }
    };
  };
}

// 使用例
export class ClaimService {
  @AuditLog('APPROVE_CLAIM')
  async approveClaim(
    claimId: string,
    assessment: Assessment
  ): Promise<void> {
    // 重要な操作は自動的に監査ログに記録される
    const claim = await this.repository.findById(claimId);
    await claim.approve(assessment);
    await this.repository.save(claim);
  }
}
```

### 3.3 可用性・レジリエンス

#### Circuit Breaker実装
```typescript
// Circuit Breaker パターン
export class CircuitBreaker {
  private failures = 0;
  private lastFailureTime?: Date;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  
  constructor(
    private threshold: number = 5,
    private timeout: number = 60000,
    private resetTimeout: number = 30000
  ) {}
  
  async execute<T>(
    fn: () => Promise<T>
  ): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime!.getTime() > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess(): void {
    this.failures = 0;
    this.state = 'CLOSED';
  }
  
  private onFailure(): void {
    this.failures++;
    this.lastFailureTime = new Date();
    
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}

// 外部サービス統合での使用
export class ExternalPaymentService {
  private circuitBreaker = new CircuitBreaker();
  
  async processPayment(payment: Payment): Promise<PaymentResult> {
    return this.circuitBreaker.execute(async () => {
      const response = await axios.post(
        'https://payment.provider.com/api/process',
        payment,
        { timeout: 5000 }
      );
      
      return response.data;
    });
  }
}
```

#### ヘルスチェック実装
```typescript
// ヘルスチェックエンドポイント
@Controller('health')
export class HealthController {
  constructor(
    private db: DataSource,
    private redis: Redis,
    private kafka: Kafka
  ) {}
  
  @Get()
  async check(): Promise<HealthCheckResult> {
    const checks = await Promise.allSettled([
      this.checkDatabase(),
      this.checkRedis(),
      this.checkKafka()
    ]);
    
    const results = {
      database: this.parseCheckResult(checks[0]),
      redis: this.parseCheckResult(checks[1]),
      kafka: this.parseCheckResult(checks[2])
    };
    
    const isHealthy = Object.values(results)
      .every(r => r.status === 'healthy');
    
    return {
      status: isHealthy ? 'healthy' : 'unhealthy',
      timestamp: new Date(),
      services: results
    };
  }
  
  private async checkDatabase(): Promise<ServiceHealth> {
    const start = Date.now();
    await this.db.query('SELECT 1');
    
    return {
      status: 'healthy',
      responseTime: Date.now() - start
    };
  }
  
  private async checkRedis(): Promise<ServiceHealth> {
    const start = Date.now();
    await this.redis.ping();
    
    return {
      status: 'healthy',
      responseTime: Date.now() - start
    };
  }
}
```

## 4. 監視とロギング

### 4.1 構造化ロギング
```typescript
// ロガー設定
export const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new winston.transports.File({
      filename: 'error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: 'combined.log'
    })
  ]
});

// コンテキスト付きロガー
export class ContextLogger {
  constructor(
    private context: string,
    private metadata: Record<string, any> = {}
  ) {}
  
  info(message: string, meta?: Record<string, any>): void {
    logger.info(message, {
      context: this.context,
      ...this.metadata,
      ...meta
    });
  }
  
  error(message: string, error?: Error, meta?: Record<string, any>): void {
    logger.error(message, {
      context: this.context,
      error: error?.stack,
      ...this.metadata,
      ...meta
    });
  }
}
```

### 4.2 メトリクス収集
```typescript
// Prometheusメトリクス
export class MetricsService {
  private httpDuration = new Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status']
  });
  
  private dbQueryDuration = new Histogram({
    name: 'db_query_duration_seconds',
    help: 'Duration of database queries in seconds',
    labelNames: ['operation', 'table']
  });
  
  private businessMetrics = {
    contractsCreated: new Counter({
      name: 'contracts_created_total',
      help: 'Total number of contracts created',
      labelNames: ['product_type']
    }),
    
    claimsProcessed: new Counter({
      name: 'claims_processed_total',
      help: 'Total number of claims processed',
      labelNames: ['status', 'claim_type']
    }),
    
    activeContracts: new Gauge({
      name: 'active_contracts',
      help: 'Number of active contracts',
      labelNames: ['product_type']
    })
  };
  
  recordHttpRequest(
    method: string,
    route: string,
    status: number,
    duration: number
  ): void {
    this.httpDuration
      .labels(method, route, status.toString())
      .observe(duration / 1000);
  }
  
  recordContractCreated(productType: string): void {
    this.businessMetrics.contractsCreated
      .labels(productType)
      .inc();
  }
}
```