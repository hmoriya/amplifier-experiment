# Phase 5: 明治安田生命保険のソフトウェア設計

## 1. ドメインモデル設計

### 1.1 契約管理ドメイン

#### 主要なAggregate

##### Contract Aggregate（契約集約）
```typescript
// 契約集約ルート
export class Contract {
  private contractId: ContractId;
  private contractNumber: ContractNumber;
  private policyHolderId: PolicyHolderId;
  private productId: ProductId;
  private status: ContractStatus;
  private coverages: Coverage[];
  private premiums: Premium[];
  private effectiveDate: Date;
  private expirationDate: Date;
  private riders: Rider[];
  private version: number;
  
  // ビジネスロジック
  public activateContract(): Result<void> {
    if (!this.canActivate()) {
      return Result.fail('契約を有効化できません');
    }
    this.status = ContractStatus.ACTIVE;
    this.addDomainEvent(new ContractActivated(this.contractId));
    return Result.ok();
  }
  
  public addRider(rider: Rider): Result<void> {
    if (!this.canAddRider(rider)) {
      return Result.fail('特約を追加できません');
    }
    this.riders.push(rider);
    this.addDomainEvent(new RiderAdded(this.contractId, rider));
    return Result.ok();
  }
  
  private canActivate(): boolean {
    return this.status === ContractStatus.PENDING 
      && this.hasValidCoverages()
      && this.isPremiumPaid();
  }
}

// 保障内容
export class Coverage {
  private coverageId: CoverageId;
  private coverageType: CoverageType;
  private benefitAmount: Money;
  private waitingPeriod: Days;
  private exclusions: Exclusion[];
  
  public isClaimable(claim: ClaimRequest): boolean {
    return !this.isInWaitingPeriod(claim.occurrenceDate)
      && !this.hasExclusion(claim.claimType);
  }
}

// 保険料
export class Premium {
  private premiumId: PremiumId;
  private amount: Money;
  private frequency: PaymentFrequency;
  private dueDate: Date;
  private status: PremiumStatus;
  
  public recordPayment(payment: Payment): Result<void> {
    if (!this.canAcceptPayment(payment)) {
      return Result.fail('支払いを受け付けられません');
    }
    this.status = PremiumStatus.PAID;
    return Result.ok();
  }
}
```

#### Domain Events（ドメインイベント）
```typescript
// 契約関連イベント
export class ContractCreated implements DomainEvent {
  constructor(
    public readonly contractId: ContractId,
    public readonly policyHolderId: PolicyHolderId,
    public readonly productId: ProductId,
    public readonly occurredAt: Date = new Date()
  ) {}
}

export class ContractActivated implements DomainEvent {
  constructor(
    public readonly contractId: ContractId,
    public readonly occurredAt: Date = new Date()
  ) {}
}

export class RiderAdded implements DomainEvent {
  constructor(
    public readonly contractId: ContractId,
    public readonly rider: Rider,
    public readonly occurredAt: Date = new Date()
  ) {}
}

export class PremiumPaid implements DomainEvent {
  constructor(
    public readonly contractId: ContractId,
    public readonly premiumId: PremiumId,
    public readonly amount: Money,
    public readonly occurredAt: Date = new Date()
  ) {}
}
```

### 1.2 保険金・給付金ドメイン

#### Claim Aggregate（保険金請求集約）
```typescript
export class Claim {
  private claimId: ClaimId;
  private contractId: ContractId;
  private claimant: Claimant;
  private claimType: ClaimType;
  private requestedAmount: Money;
  private status: ClaimStatus;
  private documents: ClaimDocument[];
  private assessments: Assessment[];
  private payments: Payment[];
  
  // 請求審査
  public submitForReview(): Result<void> {
    if (!this.hasRequiredDocuments()) {
      return Result.fail('必要書類が不足しています');
    }
    this.status = ClaimStatus.UNDER_REVIEW;
    this.addDomainEvent(new ClaimSubmittedForReview(this.claimId));
    return Result.ok();
  }
  
  // 審査承認
  public approve(assessment: Assessment): Result<void> {
    if (!this.canApprove()) {
      return Result.fail('承認できない状態です');
    }
    this.assessments.push(assessment);
    this.status = ClaimStatus.APPROVED;
    const approvedAmount = this.calculateApprovedAmount();
    this.addDomainEvent(new ClaimApproved(this.claimId, approvedAmount));
    return Result.ok();
  }
  
  // 支払い実行
  public processPayment(payment: Payment): Result<void> {
    if (this.status !== ClaimStatus.APPROVED) {
      return Result.fail('承認されていない請求には支払いできません');
    }
    this.payments.push(payment);
    this.status = ClaimStatus.PAID;
    this.addDomainEvent(new ClaimPaid(this.claimId, payment));
    return Result.ok();
  }
}

// 審査記録
export class Assessment {
  private assessmentId: AssessmentId;
  private assessorId: AssessorId;
  private decision: AssessmentDecision;
  private approvedAmount: Money;
  private comments: string;
  private assessedAt: Date;
  
  public static create(
    assessorId: AssessorId,
    decision: AssessmentDecision,
    approvedAmount: Money,
    comments: string
  ): Assessment {
    return new Assessment({
      assessmentId: AssessmentId.create(),
      assessorId,
      decision,
      approvedAmount,
      comments,
      assessedAt: new Date()
    });
  }
}
```

### 1.3 顧客管理ドメイン

#### Customer Aggregate（顧客集約）
```typescript
export class Customer {
  private customerId: CustomerId;
  private personalInfo: PersonalInfo;
  private contactInfo: ContactInfo;
  private preferences: CustomerPreferences;
  private contracts: ContractId[];
  private interactions: CustomerInteraction[];
  private riskProfile: RiskProfile;
  
  // 顧客情報更新
  public updateContactInfo(newInfo: ContactInfo): Result<void> {
    const validation = this.validateContactInfo(newInfo);
    if (validation.isFailure) {
      return Result.fail(validation.error);
    }
    
    const oldInfo = this.contactInfo;
    this.contactInfo = newInfo;
    this.addDomainEvent(new ContactInfoUpdated(
      this.customerId,
      oldInfo,
      newInfo
    ));
    return Result.ok();
  }
  
  // リスクプロファイル更新
  public updateRiskProfile(
    healthData: HealthData,
    lifestyleData: LifestyleData
  ): Result<void> {
    const newProfile = RiskProfile.calculate(
      healthData,
      lifestyleData,
      this.personalInfo.age
    );
    
    if (this.hasSignificantRiskChange(newProfile)) {
      this.addDomainEvent(new RiskProfileChanged(
        this.customerId,
        this.riskProfile,
        newProfile
      ));
    }
    
    this.riskProfile = newProfile;
    return Result.ok();
  }
}

// 個人情報（値オブジェクト）
export class PersonalInfo {
  constructor(
    public readonly fullName: FullName,
    public readonly dateOfBirth: Date,
    public readonly gender: Gender,
    public readonly nationalId: NationalId
  ) {}
  
  get age(): number {
    const today = new Date();
    const birthDate = new Date(this.dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || 
      (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    
    return age;
  }
}
```

### 1.4 ユビキタス言語

```yaml
契約管理:
  契約 (Contract): 保険契約の基本単位
  契約者 (PolicyHolder): 保険料を支払う人
  被保険者 (Insured): 保険の対象となる人
  保障 (Coverage): 保険でカバーされる内容
  特約 (Rider): 基本契約に追加される保障
  保険料 (Premium): 保険契約の対価
  
保険金・給付金:
  保険金請求 (Claim): 保険金の支払い請求
  給付金 (Benefit): 契約に基づく給付
  審査 (Assessment): 請求内容の妥当性確認
  支払い (Payment): 保険金・給付金の支払い
  免責事項 (Exclusion): 保険金が支払われない条件
  
顧客管理:
  顧客 (Customer): 保険サービスの利用者
  リスクプロファイル (Risk Profile): 顧客のリスク評価
  顧客接点 (Customer Interaction): 顧客との接触記録
  顧客選好 (Customer Preferences): 顧客の好み・設定
```

## 2. API設計方針

### 2.1 内部API設計

#### GraphQL Schema（契約管理）
```graphql
type Contract {
  id: ID!
  contractNumber: String!
  policyHolder: PolicyHolder!
  product: Product!
  status: ContractStatus!
  coverages: [Coverage!]!
  premiums: [Premium!]!
  effectiveDate: Date!
  expirationDate: Date
  riders: [Rider!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Query {
  contract(id: ID!): Contract
  contractByNumber(contractNumber: String!): Contract
  contractsByPolicyHolder(policyHolderId: ID!): [Contract!]!
}

type Mutation {
  createContract(input: CreateContractInput!): CreateContractPayload!
  activateContract(id: ID!): ActivateContractPayload!
  addRider(contractId: ID!, rider: RiderInput!): AddRiderPayload!
  terminateContract(id: ID!, reason: String!): TerminateContractPayload!
}

input CreateContractInput {
  policyHolderId: ID!
  productId: ID!
  coverages: [CoverageInput!]!
  effectiveDate: Date!
}

type CreateContractPayload {
  contract: Contract
  errors: [Error!]
}
```

#### REST API設計（保険金請求）
```yaml
# 請求申請
POST /api/v1/claims
Request:
  {
    "contractId": "string",
    "claimType": "DEATH|HOSPITALIZATION|DISABILITY",
    "requestedAmount": {
      "amount": "number",
      "currency": "JPY"
    },
    "occurrenceDate": "date",
    "description": "string"
  }
Response: 
  201 Created
  {
    "claimId": "string",
    "status": "SUBMITTED",
    "requiredDocuments": ["array of document types"]
  }

# 請求状態照会
GET /api/v1/claims/{claimId}
Response:
  200 OK
  {
    "claimId": "string",
    "status": "string",
    "requestedAmount": "object",
    "approvedAmount": "object",
    "payments": ["array of payments"],
    "timeline": ["array of events"]
  }

# 書類アップロード
POST /api/v1/claims/{claimId}/documents
Request:
  multipart/form-data
  {
    "documentType": "string",
    "file": "binary"
  }
Response:
  201 Created
  {
    "documentId": "string",
    "uploadedAt": "datetime"
  }
```

### 2.2 外部API設計

#### Open API仕様（顧客向け）
```yaml
openapi: 3.0.0
info:
  title: Meiji Yasuda Customer API
  version: 1.0.0
  description: 顧客向け公開API

paths:
  /public/v1/contracts/summary:
    get:
      summary: 契約一覧取得
      security:
        - OAuth2: [read:contracts]
      responses:
        200:
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ContractSummary'
                  
  /public/v1/claims/estimate:
    post:
      summary: 保険金見積もり
      security:
        - OAuth2: [read:contracts]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EstimateRequest'
      responses:
        200:
          description: 見積もり結果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EstimateResponse'

components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.meijiyasuda.co.jp/oauth/authorize
          tokenUrl: https://auth.meijiyasuda.co.jp/oauth/token
          scopes:
            read:contracts: 契約情報の読み取り
            write:claims: 保険金請求の作成
```

### 2.3 セキュリティ設計

#### API認証・認可
```typescript
// JWT Token構造
interface JWTPayload {
  sub: string;          // User ID
  iss: string;          // Issuer
  aud: string[];        // Audience
  exp: number;          // Expiration
  iat: number;          // Issued At
  roles: string[];      // User roles
  permissions: string[]; // Fine-grained permissions
  customerId?: string;   // Customer ID (for customer APIs)
}

// API Gateway認証ミドルウェア
export class AuthenticationMiddleware {
  async authenticate(req: Request): Promise<AuthContext> {
    const token = this.extractToken(req);
    if (!token) {
      throw new UnauthorizedException('トークンが必要です');
    }
    
    const payload = await this.verifyToken(token);
    const permissions = await this.loadPermissions(payload);
    
    return new AuthContext({
      userId: payload.sub,
      roles: payload.roles,
      permissions: permissions,
      customerId: payload.customerId
    });
  }
}

// Permission-based認可
export class AuthorizationService {
  async authorize(
    context: AuthContext,
    resource: string,
    action: string
  ): Promise<boolean> {
    // リソースベースの認可チェック
    const permission = `${resource}:${action}`;
    
    if (context.hasPermission(permission)) {
      return true;
    }
    
    // 動的な認可ルール評価
    return this.evaluateDynamicRules(context, resource, action);
  }
}
```

#### データ暗号化
```typescript
// フィールドレベル暗号化
export class EncryptionService {
  private algorithm = 'aes-256-gcm';
  
  async encryptField(
    plaintext: string,
    context: EncryptionContext
  ): Promise<EncryptedData> {
    const key = await this.deriveKey(context);
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(this.algorithm, key, iv);
    
    const encrypted = Buffer.concat([
      cipher.update(plaintext, 'utf8'),
      cipher.final()
    ]);
    
    const tag = cipher.getAuthTag();
    
    return {
      data: encrypted.toString('base64'),
      iv: iv.toString('base64'),
      tag: tag.toString('base64'),
      keyId: context.keyId,
      algorithm: this.algorithm
    };
  }
  
  // 顧客個人情報の暗号化
  encryptPersonalInfo(info: PersonalInfo): EncryptedPersonalInfo {
    return {
      fullName: this.encryptField(info.fullName, 'PII'),
      nationalId: this.encryptField(info.nationalId, 'PII'),
      dateOfBirth: info.dateOfBirth, // 生年月日は暗号化しない
      gender: info.gender
    };
  }
}
```

## 3. テクノロジースタック

### 3.1 バックエンド技術選定
```yaml
言語・フレームワーク:
  - TypeScript 5.x
  - Node.js 20.x LTS
  - NestJS（APIフレームワーク）
  - TypeORM（ORマッパー）
  
API層:
  - GraphQL（Apollo Server）
  - REST（OpenAPI 3.0）
  - gRPC（内部サービス間通信）
  
データストア:
  - PostgreSQL 15（トランザクショナルデータ）
  - MongoDB 7.0（ドキュメントストア）
  - Redis 7.x（キャッシュ・セッション）
  - Apache Kafka（イベントストリーミング）
  
監視・ロギング:
  - Prometheus + Grafana
  - Elasticsearch + Kibana
  - Jaeger（分散トレーシング）
```

### 3.2 開発標準
```yaml
コーディング標準:
  - ESLint + Prettier設定
  - コミットメッセージ規約（Conventional Commits）
  - コードレビュー必須（2名以上）
  
テスト戦略:
  - 単体テスト: Jest（カバレッジ80%以上）
  - 統合テスト: Supertest
  - E2Eテスト: Playwright
  - 契約テスト: Pact
  
CI/CD:
  - GitLab CI/CD
  - SonarQube（コード品質）
  - Trivy（セキュリティスキャン）
  - Semantic Release（自動バージョニング）
```

## 4. 実装例

### 4.1 ユースケース実装
```typescript
// 契約作成ユースケース
export class CreateContractUseCase {
  constructor(
    private contractRepo: ContractRepository,
    private productService: ProductService,
    private customerService: CustomerService,
    private eventBus: EventBus
  ) {}
  
  async execute(
    command: CreateContractCommand
  ): Promise<Result<ContractId>> {
    // 1. 顧客存在確認
    const customer = await this.customerService
      .findById(command.customerId);
    if (!customer) {
      return Result.fail('顧客が見つかりません');
    }
    
    // 2. 商品情報取得
    const product = await this.productService
      .findById(command.productId);
    if (!product) {
      return Result.fail('商品が見つかりません');
    }
    
    // 3. 契約作成
    const contractOrError = Contract.create({
      policyHolderId: command.customerId,
      productId: command.productId,
      coverages: command.coverages,
      effectiveDate: command.effectiveDate
    });
    
    if (contractOrError.isFailure) {
      return Result.fail(contractOrError.error);
    }
    
    const contract = contractOrError.getValue();
    
    // 4. 保存
    await this.contractRepo.save(contract);
    
    // 5. イベント発行
    const events = contract.getUncommittedEvents();
    await this.eventBus.publishAll(events);
    
    return Result.ok(contract.id);
  }
}
```

### 4.2 リポジトリ実装
```typescript
// 契約リポジトリ実装
export class ContractRepositoryImpl implements ContractRepository {
  constructor(
    private db: DataSource,
    private mapper: ContractMapper
  ) {}
  
  async save(contract: Contract): Promise<void> {
    const entity = this.mapper.toPersistence(contract);
    
    await this.db.transaction(async manager => {
      // 契約本体の保存
      await manager.save(ContractEntity, entity);
      
      // 保障内容の保存
      await manager.save(
        CoverageEntity,
        entity.coverages
      );
      
      // イベントの保存
      const events = contract.getUncommittedEvents();
      const eventEntities = events.map(e => 
        this.mapper.eventToPersistence(e)
      );
      await manager.save(EventEntity, eventEntities);
    });
    
    contract.markEventsAsCommitted();
  }
  
  async findById(id: ContractId): Promise<Contract | null> {
    const entity = await this.db
      .getRepository(ContractEntity)
      .findOne({
        where: { id: id.value },
        relations: ['coverages', 'premiums', 'riders']
      });
      
    if (!entity) {
      return null;
    }
    
    return this.mapper.toDomain(entity);
  }
}
```