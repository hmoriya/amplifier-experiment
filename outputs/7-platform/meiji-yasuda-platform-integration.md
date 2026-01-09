# Phase 7: 明治安田生命保険のプラットフォーム統合

## 1. インフラ設計

### 1.1 クラウド戦略

#### マルチクラウド構成
```yaml
プライマリクラウド: AWS
  用途:
    - 本番環境
    - 顧客向けサービス
    - コアビジネスシステム
  
  主要サービス:
    - EKS (Kubernetes)
    - RDS (PostgreSQL)
    - ElastiCache (Redis)
    - MSK (Managed Kafka)
    - CloudFront (CDN)
    - WAF
    
セカンダリクラウド: Azure
  用途:
    - DR環境
    - 開発・テスト環境
    - データ分析基盤
  
  主要サービス:
    - AKS (Kubernetes)
    - Azure Database for PostgreSQL
    - Azure Cache for Redis
    - Event Hubs
    - Azure Front Door
```

### 1.2 Kubernetesアーキテクチャ

#### 名前空間設計
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
---
apiVersion: v1
kind: Namespace
metadata:
  name: shared-services
  labels:
    purpose: infrastructure
```

#### マイクロサービスデプロイメント例
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contract-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: contract-service
  template:
    metadata:
      labels:
        app: contract-service
        version: v1
    spec:
      containers:
      - name: contract-service
        image: meijiyasuda.azurecr.io/contract-service:1.2.3
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
        - name: KAFKA_BROKERS
          value: "kafka-1:9092,kafka-2:9092,kafka-3:9092"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: contract-service
  namespace: production
spec:
  selector:
    app: contract-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: contract-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: contract-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 1.3 ハイブリッド構成

#### オンプレミス連携
```yaml
VPN接続:
  AWS Site-to-Site VPN:
    - 本社データセンター接続
    - 冗長構成（2トンネル）
    - BGPルーティング
  
Direct Connect:
  - 専用線接続（10Gbps）
  - レイテンシ重視のシステム用
  - Virtual Interface (VIF) 設定

ネットワーク設計:
  オンプレミス: 10.0.0.0/8
  AWS VPC: 172.16.0.0/12
  Azure VNet: 192.168.0.0/16
  
  # Transit Gateway設定
  aws_transit_gateway:
    asn: 64512
    routes:
      - destination: 10.0.0.0/8
        attachment: vpn-connection-1
      - destination: 192.168.0.0/16
        attachment: peering-azure
```

#### データ同期戦略
```typescript
// CDC (Change Data Capture) 実装
export class DataSyncService {
  private debeziumConnector: DebeziumConnector;
  
  async setupCDC(): Promise<void> {
    // レガシーDBからのCDC設定
    await this.debeziumConnector.createConnector({
      name: 'legacy-contracts-connector',
      config: {
        'connector.class': 'io.debezium.connector.oracle.OracleConnector',
        'database.hostname': 'legacy-db.onprem.local',
        'database.port': '1521',
        'database.user': 'cdc_user',
        'database.password': '${file:/secrets/oracle-password}',
        'database.dbname': 'CONTRACTS',
        'database.server.name': 'legacy',
        'table.include.list': 'CONTRACTS.CONTRACT,CONTRACTS.COVERAGE',
        'database.history.kafka.bootstrap.servers': 'kafka:9092',
        'database.history.kafka.topic': 'schema-changes.contracts'
      }
    });
  }
  
  // イベント変換
  @KafkaListener(topics = ['legacy.CONTRACTS.CONTRACT'])
  async handleContractChange(event: DebeziumEvent): Promise<void> {
    const operation = event.payload.op; // c=create, u=update, d=delete
    
    switch (operation) {
      case 'c':
      case 'u':
        const contract = this.transformToNewModel(event.payload.after);
        await this.publishDomainEvent(new ContractSynced(contract));
        break;
        
      case 'd':
        await this.handleDeletion(event.payload.before.id);
        break;
    }
  }
}
```

## 2. CI/CD戦略

### 2.1 GitLab CI/CD Pipeline

#### マルチステージパイプライン
```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - package
  - deploy-staging
  - integration-test
  - deploy-production

variables:
  DOCKER_REGISTRY: meijiyasuda.azurecr.io
  SONAR_PROJECT_KEY: meiji-yasuda-insurance

# ビルドステージ
build:
  stage: build
  image: node:20-alpine
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 day
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

# テストステージ
test:unit:
  stage: test
  image: node:20-alpine
  script:
    - npm run test:unit
    - npm run test:coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      junit: coverage/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:integration:
  stage: test
  services:
    - postgres:15
    - redis:7-alpine
  script:
    - npm run test:integration
  
# セキュリティスキャン
security:sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --json --output=sast-report.json .
  artifacts:
    reports:
      sast: sast-report.json

security:dependency:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy fs --security-checks vuln --format json --output vuln-report.json .
  artifacts:
    reports:
      dependency_scanning: vuln-report.json

security:container:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --format json --output container-report.json ${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:${CI_COMMIT_SHA}
  artifacts:
    reports:
      container_scanning: container-report.json

# コンテナビルド
package:
  stage: package
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker build -t ${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:${CI_COMMIT_SHA} .
    - docker tag ${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:${CI_COMMIT_SHA} ${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:latest
    - echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin $DOCKER_REGISTRY
    - docker push ${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:${CI_COMMIT_SHA}
    - docker push ${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:latest

# ステージング環境デプロイ
deploy:staging:
  stage: deploy-staging
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/${CI_PROJECT_NAME} ${CI_PROJECT_NAME}=${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:${CI_COMMIT_SHA} -n staging
    - kubectl rollout status deployment/${CI_PROJECT_NAME} -n staging
  environment:
    name: staging
    url: https://staging.meijiyasuda.co.jp
  only:
    - main

# 統合テスト
integration:test:
  stage: integration-test
  image: node:20-alpine
  script:
    - npm run test:e2e -- --baseUrl=https://staging.meijiyasuda.co.jp
  needs:
    - deploy:staging

# 本番デプロイ（手動承認）
deploy:production:
  stage: deploy-production
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/${CI_PROJECT_NAME} ${CI_PROJECT_NAME}=${DOCKER_REGISTRY}/${CI_PROJECT_NAME}:${CI_COMMIT_SHA} -n production
    - kubectl rollout status deployment/${CI_PROJECT_NAME} -n production
  environment:
    name: production
    url: https://api.meijiyasuda.co.jp
  when: manual
  only:
    - main
```

### 2.2 DevOpsプラクティス

#### Infrastructure as Code (IaC)
```hcl
# terraform/environments/production/main.tf
terraform {
  required_version = ">= 1.0"
  
  backend "s3" {
    bucket         = "meijiyasuda-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "ap-northeast-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

module "eks_cluster" {
  source = "../../modules/eks"
  
  cluster_name    = "meijiyasuda-prod-eks"
  cluster_version = "1.28"
  
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      desired_capacity = 5
      min_capacity     = 3
      max_capacity     = 10
      instance_types   = ["t3.large"]
    }
    
    spot = {
      desired_capacity = 3
      min_capacity     = 1
      max_capacity     = 6
      instance_types   = ["t3.large", "t3a.large"]
      capacity_type    = "SPOT"
    }
  }
  
  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

module "rds" {
  source = "../../modules/rds"
  
  identifier     = "meijiyasuda-prod-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.r6g.2xlarge"
  
  allocated_storage     = 500
  max_allocated_storage = 1000
  
  multi_az               = true
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  vpc_id                 = module.vpc.vpc_id
  subnet_ids             = module.vpc.database_subnet_ids
  
  enable_performance_insights = true
  performance_insights_retention_period = 7
}
```

#### GitOps with ArgoCD
```yaml
# argocd/applications/contract-service.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: contract-service
  namespace: argocd
spec:
  project: production
  
  source:
    repoURL: https://gitlab.meijiyasuda.co.jp/platform/k8s-manifests
    targetRevision: main
    path: services/contract-service
    
    helm:
      valueFiles:
        - values-production.yaml
      parameters:
        - name: image.tag
          value: "1.2.3"
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### 2.3 リリース管理

#### Feature Flags
```typescript
// Feature Flag Service
export class FeatureFlagService {
  private launchDarkly: LDClient;
  
  async isEnabled(
    flagKey: string,
    context: FeatureContext
  ): Promise<boolean> {
    const ldContext = {
      kind: 'multi',
      user: {
        key: context.userId,
        attributes: context.userAttributes
      },
      organization: {
        key: context.organizationId,
        attributes: context.orgAttributes
      }
    };
    
    return this.launchDarkly.variation(
      flagKey,
      ldContext,
      false // デフォルト値
    );
  }
}

// 使用例
@Injectable()
export class ClaimService {
  constructor(
    private featureFlags: FeatureFlagService,
    private newClaimProcessor: NewClaimProcessor,
    private legacyClaimProcessor: LegacyClaimProcessor
  ) {}
  
  async processClaim(claim: Claim): Promise<void> {
    const useNewProcessor = await this.featureFlags.isEnabled(
      'new-claim-processor',
      {
        userId: claim.userId,
        organizationId: claim.organizationId,
        userAttributes: {
          plan: claim.insurancePlan,
          region: claim.region
        }
      }
    );
    
    if (useNewProcessor) {
      return this.newClaimProcessor.process(claim);
    } else {
      return this.legacyClaimProcessor.process(claim);
    }
  }
}
```

#### カナリアデプロイメント
```yaml
# Flagger カナリア設定
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: contract-service
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: contract-service
  
  progressDeadlineSeconds: 60
  
  service:
    port: 80
    targetPort: 8080
    gateways:
    - public-gateway.istio-system.svc.cluster.local
    hosts:
    - api.meijiyasuda.co.jp
  
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 30s
    
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 30s
    
    - name: custom-metric
      templateRef:
        name: error-rate
        namespace: flagger-system
      thresholdRange:
        max: 1
  
  webhooks:
    - name: acceptance-test
      type: pre-rollout
      url: http://flagger-loadtester.test/
      timeout: 30s
      metadata:
        type: bash
        cmd: "curl -sd 'test' http://contract-service-canary/health/check"
    
    - name: load-test
      url: http://flagger-loadtester.test/
      timeout: 5s
      metadata:
        type: cmd
        cmd: "hey -z 1m -q 10 -c 2 http://contract-service-canary/"
```

## 3. 外部システム統合

### 3.1 提携企業との連携

#### API Gateway設定
```yaml
# Kong API Gateway設定
services:
  - name: partner-api-service
    url: http://contract-service.production.svc.cluster.local
    
routes:
  - name: partner-contracts
    service: partner-api-service
    paths:
      - /partner/v1/contracts
    methods:
      - GET
      - POST
    
plugins:
  - name: rate-limiting
    config:
      minute: 100
      hour: 1000
      policy: local
      
  - name: key-auth
    config:
      key_names:
        - api-key
        - X-API-Key
      
  - name: request-transformer
    config:
      add:
        headers:
          X-Partner-Id: "$(consumer.custom_id)"
          
  - name: response-transformer
    config:
      remove:
        headers:
          - X-Internal-Request-Id
          - Server
          
  - name: prometheus
    config:
      per_consumer: true
```

#### パートナーAPI実装
```typescript
// Partner API Controller
@Controller('partner/v1')
@UseGuards(PartnerAuthGuard)
@ApiTags('Partner API')
export class PartnerApiController {
  constructor(
    private contractService: ContractService,
    private rateLimiter: RateLimiterService
  ) {}
  
  @Post('contracts/quote')
  @ApiOperation({ summary: '保険見積もり取得' })
  @UseInterceptors(AuditLogInterceptor)
  async getQuote(
    @Body() dto: QuoteRequestDTO,
    @Partner() partner: PartnerContext
  ): Promise<QuoteResponseDTO> {
    // レート制限チェック
    await this.rateLimiter.checkLimit(
      `partner:${partner.id}:quote`,
      partner.quotaLimits
    );
    
    // パートナー固有のビジネスルール適用
    const quote = await this.contractService.calculateQuote({
      ...dto,
      partnerId: partner.id,
      partnerConfig: partner.configuration
    });
    
    // レスポンス変換（パートナー固有フォーマット）
    return this.transformForPartner(quote, partner);
  }
  
  @Get('contracts/:contractId')
  @ApiOperation({ summary: '契約情報取得' })
  @UseInterceptors(CacheInterceptor)
  async getContract(
    @Param('contractId') contractId: string,
    @Partner() partner: PartnerContext
  ): Promise<ContractDTO> {
    // アクセス権限チェック
    const canAccess = await this.checkPartnerAccess(
      partner.id,
      contractId
    );
    
    if (!canAccess) {
      throw new ForbiddenException(
        'このパートナーは指定された契約にアクセスできません'
      );
    }
    
    const contract = await this.contractService.findById(contractId);
    
    // 情報フィルタリング（パートナーに公開する情報のみ）
    return this.filterContractData(contract, partner.accessLevel);
  }
}

// Partner認証ミドルウェア
@Injectable()
export class PartnerAuthGuard implements CanActivate {
  constructor(
    private partnerService: PartnerService,
    private cryptoService: CryptoService
  ) {}
  
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];
    
    if (!apiKey) {
      throw new UnauthorizedException('APIキーが必要です');
    }
    
    // APIキー検証
    const partner = await this.partnerService.validateApiKey(apiKey);
    if (!partner) {
      throw new UnauthorizedException('無効なAPIキー');
    }
    
    // IP制限チェック
    if (partner.ipWhitelist && partner.ipWhitelist.length > 0) {
      const clientIp = request.ip;
      if (!partner.ipWhitelist.includes(clientIp)) {
        throw new ForbiddenException('アクセスが拒否されました');
      }
    }
    
    // HMAC署名検証（オプション）
    if (partner.requireSignature) {
      const signature = request.headers['x-signature'];
      const isValid = await this.cryptoService.verifyHMAC(
        request.body,
        signature,
        partner.secretKey
      );
      
      if (!isValid) {
        throw new UnauthorizedException('署名検証に失敗しました');
      }
    }
    
    request.partner = partner;
    return true;
  }
}
```

### 3.2 規制当局への報告

#### 定期報告バッチ
```typescript
// 金融庁向けレポート生成
@Injectable()
export class RegulatoryReportingService {
  constructor(
    private dataWarehouse: DataWarehouseService,
    private fileService: FileService,
    private notificationService: NotificationService
  ) {}
  
  @Cron('0 2 1 * *') // 毎月1日 AM2:00
  async generateMonthlyReport(): Promise<void> {
    const lastMonth = moment().subtract(1, 'month');
    const reportPeriod = {
      start: lastMonth.startOf('month').toDate(),
      end: lastMonth.endOf('month').toDate()
    };
    
    try {
      // 1. データ収集
      const reportData = await this.collectReportData(reportPeriod);
      
      // 2. データ検証
      const validation = await this.validateReportData(reportData);
      if (!validation.isValid) {
        await this.handleValidationError(validation.errors);
        return;
      }
      
      // 3. レポート生成
      const reports = await this.generateReports(reportData);
      
      // 4. ファイル作成（複数フォーマット）
      const files = await Promise.all([
        this.generateXBRL(reports.financial),
        this.generateCSV(reports.transaction),
        this.generatePDF(reports.summary)
      ]);
      
      // 5. 暗号化とアップロード
      const encryptedFiles = await this.encryptFiles(files);
      await this.uploadToRegulatory(encryptedFiles);
      
      // 6. 通知
      await this.notificationService.notifyReportCompletion({
        period: reportPeriod,
        files: files.map(f => f.name),
        status: 'SUCCESS'
      });
      
    } catch (error) {
      await this.handleReportError(error, reportPeriod);
    }
  }
  
  private async collectReportData(
    period: DateRange
  ): Promise<RegulatoryData> {
    const queries = {
      // 新契約統計
      newContracts: `
        SELECT 
          product_type,
          COUNT(*) as count,
          SUM(premium_amount) as total_premium,
          AVG(coverage_amount) as avg_coverage
        FROM contracts
        WHERE created_at BETWEEN $1 AND $2
        GROUP BY product_type
      `,
      
      // 保険金支払統計
      claimPayments: `
        SELECT
          claim_type,
          COUNT(*) as count,
          SUM(paid_amount) as total_paid,
          AVG(processing_days) as avg_processing_time
        FROM claims
        WHERE paid_at BETWEEN $1 AND $2
        GROUP BY claim_type
      `,
      
      // ソルベンシー関連
      solvencyMetrics: `
        SELECT
          calculation_date,
          solvency_margin_ratio,
          risk_amount,
          available_capital
        FROM solvency_calculations
        WHERE calculation_date = DATE_TRUNC('month', $2::date)
      `
    };
    
    const results = await Promise.all(
      Object.entries(queries).map(async ([key, query]) => {
        const data = await this.dataWarehouse.query(
          query,
          [period.start, period.end]
        );
        return { key, data };
      })
    );
    
    return this.transformToRegulatoryFormat(results);
  }
  
  private async generateXBRL(
    financialData: FinancialReport
  ): Promise<File> {
    const xbrl = new XBRLBuilder();
    
    // XBRLインスタンス文書作成
    xbrl.setContext({
      entity: 'jp-fsa:MeijiYasudaLifeInsurance',
      period: financialData.period,
      scenario: 'Actual'
    });
    
    // 財務データ追加
    xbrl.addFact('jp-gaap:NetPremiumsWritten', 
      financialData.netPremiums);
    xbrl.addFact('jp-gaap:ClaimsIncurred', 
      financialData.claimsIncurred);
    xbrl.addFact('jp-fsa:SolvencyMarginRatio', 
      financialData.solvencyRatio);
    
    const xbrlDocument = xbrl.build();
    
    return {
      name: `FSA_Report_${financialData.period}.xbrl`,
      content: xbrlDocument,
      mimeType: 'application/xml'
    };
  }
}

// データ品質チェック
export class DataQualityValidator {
  async validateReportData(
    data: RegulatoryData
  ): Promise<ValidationResult> {
    const rules = [
      // 完全性チェック
      {
        name: 'completeness',
        check: () => this.checkCompleteness(data),
        severity: 'ERROR'
      },
      
      // 整合性チェック
      {
        name: 'consistency',
        check: () => this.checkConsistency(data),
        severity: 'ERROR'
      },
      
      // 異常値チェック
      {
        name: 'anomaly',
        check: () => this.checkAnomalies(data),
        severity: 'WARNING'
      },
      
      // 前月比較
      {
        name: 'monthOverMonth',
        check: () => this.checkMonthOverMonth(data),
        severity: 'WARNING'
      }
    ];
    
    const results = await Promise.all(
      rules.map(rule => rule.check())
    );
    
    const errors = results
      .filter(r => !r.isValid && r.severity === 'ERROR');
    const warnings = results
      .filter(r => !r.isValid && r.severity === 'WARNING');
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }
}
```

### 3.3 業界標準システムとの連携

#### 生命保険協会システム連携
```typescript
// 業界共通インターフェース実装
export class IndustryIntegrationService {
  private soapClient: SOAPClient;
  
  async setupLifeInsuranceAssociationClient(): Promise<void> {
    this.soapClient = await createClient(
      'https://api.seiho.or.jp/wsdl/v2/common.wsdl',
      {
        wsdl_headers: {
          Authorization: `Bearer ${this.getAccessToken()}`
        },
        endpoint: 'https://api.seiho.or.jp/services/v2'
      }
    );
  }
  
  // 契約照会（他社転換確認）
  async checkContractPortability(
    request: PortabilityCheckRequest
  ): Promise<PortabilityCheckResponse> {
    const xmlRequest = this.buildXMLRequest({
      MessageHeader: {
        MessageId: uuid(),
        Timestamp: new Date().toISOString(),
        SenderId: 'MEIJI_YASUDA',
        ReceiverId: 'SEIHO_SYSTEM'
      },
      PortabilityCheck: {
        CustomerNationalId: this.encrypt(request.nationalId),
        CustomerName: this.encrypt(request.customerName),
        DateOfBirth: request.dateOfBirth,
        RequestType: 'TRANSFER_CHECK'
      }
    });
    
    try {
      const response = await this.soapClient.CheckPortabilityAsync(
        xmlRequest
      );
      
      return this.parsePortabilityResponse(response);
      
    } catch (error) {
      // エラーハンドリング
      if (error.code === 'ECONNREFUSED') {
        throw new ExternalServiceError(
          '生命保険協会システムに接続できません'
        );
      }
      throw error;
    }
  }
  
  // 業界標準コード変換
  private convertToIndustryCode(
    internalCode: string,
    codeType: 'PRODUCT' | 'COVERAGE' | 'CLAIM'
  ): string {
    const mapping = {
      PRODUCT: {
        'WHOLE_LIFE_001': 'JLI_WL_STD_001',
        'TERM_LIFE_001': 'JLI_TL_STD_001',
        'MEDICAL_001': 'JLI_MD_STD_001'
      },
      COVERAGE: {
        'DEATH_BENEFIT': 'JLI_COV_DTH',
        'DISABILITY': 'JLI_COV_DIS',
        'HOSPITALIZATION': 'JLI_COV_HSP'
      },
      CLAIM: {
        'DEATH_CLAIM': 'JLI_CLM_DTH',
        'HOSPITAL_CLAIM': 'JLI_CLM_HSP',
        'SURGERY_CLAIM': 'JLI_CLM_SRG'
      }
    };
    
    return mapping[codeType][internalCode] || internalCode;
  }
}

// 医療機関連携
export class MedicalInstitutionIntegration {
  constructor(
    private httpClient: HttpService,
    private encryptionService: EncryptionService
  ) {}
  
  // 診断書電子化システム連携
  async fetchDigitalMedicalCertificate(
    requestId: string,
    patientConsent: ConsentToken
  ): Promise<MedicalCertificate> {
    // 患者同意確認
    await this.verifyPatientConsent(patientConsent);
    
    // 医療機関APIへのリクエスト
    const response = await this.httpClient.post(
      'https://medical-cert.jp/api/v1/certificates/retrieve',
      {
        requestId,
        requesterId: 'MEIJI_YASUDA_LIFE',
        consentToken: patientConsent.token,
        requiredFields: [
          'diagnosis',
          'treatmentPeriod',
          'hospitalizationDates',
          'surgeryDetails',
          'doctorStatement'
        ]
      },
      {
        headers: {
          'X-API-Key': process.env.MEDICAL_API_KEY,
          'X-Client-Certificate': this.getClientCertificate()
        }
      }
    );
    
    // 電子署名検証
    const isValid = await this.verifyDigitalSignature(
      response.data.certificate,
      response.data.signature,
      response.data.issuerCertificate
    );
    
    if (!isValid) {
      throw new SecurityError('医療証明書の署名が無効です');
    }
    
    return this.parseMedicalCertificate(response.data);
  }
}
```

## 4. 監視とアラート

### 4.1 Observability Stack

```yaml
# Prometheus設定
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - /etc/prometheus/rules/*.yml
    
    scrape_configs:
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
          - role: endpoints
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        
      - job_name: 'kubernetes-nodes'
        kubernetes_sd_configs:
          - role: node
          
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
            
      - job_name: 'application-metrics'
        kubernetes_sd_configs:
          - role: service
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
            action: keep
            regex: true
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-rules
  namespace: monitoring
data:
  application-rules.yml: |
    groups:
      - name: application
        interval: 30s
        rules:
          - alert: HighErrorRate
            expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
            for: 2m
            labels:
              severity: critical
              team: platform
            annotations:
              summary: "High error rate detected"
              description: "Error rate is {{ $value }} for {{ $labels.service }}"
              
          - alert: SlowResponseTime
            expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 0.5
            for: 5m
            labels:
              severity: warning
              team: platform
            annotations:
              summary: "Slow response time"
              description: "95th percentile response time is {{ $value }}s"
              
          - alert: ClaimProcessingDelay
            expr: avg(claim_processing_duration_seconds) > 300
            for: 10m
            labels:
              severity: warning
              team: business
            annotations:
              summary: "Claim processing is taking too long"
              description: "Average processing time is {{ $value }} seconds"
```

### 4.2 カスタムダッシュボード

```typescript
// Grafana Dashboard as Code
export const businessDashboard = {
  uid: 'meiji-yasuda-business',
  title: '明治安田生命 ビジネスメトリクス',
  tags: ['business', 'production'],
  timezone: 'Asia/Tokyo',
  panels: [
    {
      title: '新規契約数',
      type: 'graph',
      gridPos: { x: 0, y: 0, w: 12, h: 8 },
      targets: [{
        expr: 'sum(rate(contracts_created_total[5m])) by (product_type)',
        legendFormat: '{{product_type}}'
      }]
    },
    {
      title: '保険金請求処理状況',
      type: 'stat',
      gridPos: { x: 12, y: 0, w: 6, h: 4 },
      targets: [{
        expr: 'sum(claims_pending)',
        legendFormat: '処理待ち'
      }]
    },
    {
      title: '平均処理時間',
      type: 'gauge',
      gridPos: { x: 18, y: 0, w: 6, h: 4 },
      targets: [{
        expr: 'avg(claim_processing_duration_seconds)',
        legendFormat: '秒'
      }],
      thresholds: {
        mode: 'absolute',
        steps: [
          { value: 0, color: 'green' },
          { value: 180, color: 'yellow' },
          { value: 300, color: 'red' }
        ]
      }
    }
  ]
};

// アラート通知設定
export class AlertingService {
  async configureAlerts(): Promise<void> {
    // Slack通知
    await this.createAlertChannel({
      name: 'platform-team-slack',
      type: 'slack',
      settings: {
        url: process.env.SLACK_WEBHOOK_URL,
        channel: '#platform-alerts',
        username: 'Prometheus'
      }
    });
    
    // PagerDuty統合
    await this.createAlertChannel({
      name: 'oncall-pagerduty',
      type: 'pagerduty',
      settings: {
        integrationKey: process.env.PAGERDUTY_KEY,
        severity: 'critical'
      }
    });
    
    // メール通知
    await this.createAlertChannel({
      name: 'management-email',
      type: 'email',
      settings: {
        addresses: 'it-management@meijiyasuda.co.jp',
        singleEmail: true
      }
    });
  }
}
```

## 5. 成果と今後の展望

### 5.1 プラットフォーム統合の成果

```yaml
技術的成果:
  インフラ:
    - 自動スケーリング実現: CPU使用率70%で自動拡張
    - 可用性向上: 99.95% → 99.99%
    - DR復旧時間: 4時間 → 30分
    
  開発効率:
    - デプロイ頻度: 月次 → 週次
    - リリース失敗率: 15% → 2%
    - MTTR: 4時間 → 30分
    
  セキュリティ:
    - 脆弱性検出時間: 30日 → 1日
    - パッチ適用時間: 14日 → 3日
    - セキュリティインシデント: 60%削減
    
ビジネス成果:
  - 新商品投入期間: 6ヶ月 → 2ヶ月
  - API連携先: 5社 → 50社
  - 顧客満足度: 15%向上
  - 運用コスト: 30%削減
```

### 5.2 今後のロードマップ

```yaml
2024年度:
  Q1:
    - AIチャットボット統合
    - 音声認識による請求受付
    - ブロックチェーン証明書発行
    
  Q2:
    - IoTデバイス連携（健康データ）
    - リアルタイムリスク評価
    - 予測分析基盤構築
    
  Q3:
    - 完全自動査定システム
    - パーソナライズド商品推奨
    - クロスボーダー決済対応
    
  Q4:
    - 量子暗号通信導入
    - Edge Computing展開
    - Green ITイニシアチブ

技術革新:
  - サーバーレス移行
  - AI/ML統合強化
  - ゼロトラストアーキテクチャ完成
  - カーボンニュートラルデータセンター
```