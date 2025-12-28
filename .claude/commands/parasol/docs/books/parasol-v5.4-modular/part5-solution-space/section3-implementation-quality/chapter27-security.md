# 第27章　セキュリティ実装 ― 城壁の構築

## はじめに：多層防御の城

中世の城は、単一の城壁ではなく、外堀、外壁、内壁、天守閣という多層の防御構造を持っていました。一つの防御線が破られても、次の防御線が侵入者を食い止めます。現代のセキュリティも同じ「Defense in Depth（多層防御）」の原則に基づいています。

本章では、Parasol V5.4における包括的なセキュリティ実装について、各層での具体的な防御手法を解説します。

## セキュリティの基本原則

### 多層防御アーキテクチャ

```typescript
export interface SecurityArchitecture {
  layers: {
    perimeter: "WAF、DDoS対策、レート制限";
    network: "ファイアウォール、VPN、セグメンテーション";
    host: "OS強化、パッチ管理、エンドポイント保護";
    application: "認証、認可、入力検証、暗号化";
    data: "暗号化、アクセス制御、監査ログ";
  };
  
  principles: {
    leastPrivilege: "最小権限の原則";
    defenseInDepth: "多層防御";
    failSecurely: "安全な失敗";
    securityByDesign: "設計段階からのセキュリティ";
    zeroTrust: "ゼロトラストアーキテクチャ";
  };
  
  compliance: {
    standards: ["ISO 27001", "SOC 2", "PCI DSS"];
    regulations: ["GDPR", "個人情報保護法", "CCPA"];
    frameworks: ["NIST", "CIS Controls", "OWASP"];
  };
}

export class SecurityImplementation {
  // セキュリティ要件の定義
  defineSecurityRequirements(
    context: BusinessContext
  ): SecurityRequirements {
    return {
      authentication: {
        methods: ["password", "mfa", "biometric", "sso"],
        strength: {
          passwordPolicy: {
            minLength: 12,
            requireUppercase: true,
            requireLowercase: true,
            requireNumbers: true,
            requireSpecialChars: true,
            preventReuse: 5,
            maxAge: 90
          },
          mfaPolicy: {
            required: true,
            methods: ["totp", "sms", "webauthn"],
            backupCodes: 10
          }
        }
      },
      
      authorization: {
        model: "RBAC with ABAC",
        granularity: "resource-level",
        delegation: true,
        audit: "comprehensive"
      },
      
      encryption: {
        atRest: {
          algorithm: "AES-256-GCM",
          keyManagement: "HSM",
          rotation: "quarterly"
        },
        inTransit: {
          protocol: "TLS 1.3",
          cipherSuites: ["TLS_AES_256_GCM_SHA384"],
          certificatePinning: true
        }
      },
      
      dataProtection: {
        classification: ["public", "internal", "confidential", "restricted"],
        retention: "regulatory-compliant",
        disposal: "secure-deletion",
        anonymization: "k-anonymity"
      }
    };
  }
}
```

### 脅威モデリング

```typescript
export class ThreatModeling {
  // STRIDE脅威分析
  performSTRIDEAnalysis(system: SystemArchitecture): ThreatModel {
    const threats: Threat[] = [];
    
    // Spoofing（なりすまし）
    threats.push(...this.analyzeSpoofingThreats(system));
    
    // Tampering（改ざん）
    threats.push(...this.analyzeTamperingThreats(system));
    
    // Repudiation（否認）
    threats.push(...this.analyzeRepudiationThreats(system));
    
    // Information Disclosure（情報漏洩）
    threats.push(...this.analyzeInformationDisclosure(system));
    
    // Denial of Service（サービス拒否）
    threats.push(...this.analyzeDenialOfService(system));
    
    // Elevation of Privilege（権限昇格）
    threats.push(...this.analyzeElevationOfPrivilege(system));
    
    return {
      threats,
      riskMatrix: this.createRiskMatrix(threats),
      mitigations: this.proposeMitigations(threats),
      residualRisk: this.calculateResidualRisk(threats)
    };
  }
  
  // 攻撃ツリー分析
  buildAttackTree(asset: Asset): AttackTree {
    return {
      goal: `Compromise ${asset.name}`,
      nodes: [
        {
          attack: "Direct Access",
          children: [
            {
              attack: "Exploit Authentication Weakness",
              children: [
                { attack: "Password Brute Force", cost: "low", skill: "low" },
                { attack: "Session Hijacking", cost: "medium", skill: "medium" },
                { attack: "MFA Bypass", cost: "high", skill: "high" }
              ]
            },
            {
              attack: "Exploit Authorization Flaw",
              children: [
                { attack: "Privilege Escalation", cost: "medium", skill: "medium" },
                { attack: "IDOR", cost: "low", skill: "low" }
              ]
            }
          ]
        },
        {
          attack: "Indirect Access",
          children: [
            {
              attack: "Social Engineering",
              children: [
                { attack: "Phishing", cost: "low", skill: "medium" },
                { attack: "Pretexting", cost: "medium", skill: "high" }
              ]
            },
            {
              attack: "Supply Chain Attack",
              children: [
                { attack: "Dependency Confusion", cost: "low", skill: "medium" },
                { attack: "Malicious Package", cost: "medium", skill: "high" }
              ]
            }
          ]
        }
      ]
    };
  }
}
```

## 認証と認可の実装

### 認証システム

```typescript
export class AuthenticationSystem {
  // 多要素認証の実装
  async authenticateUser(
    credentials: Credentials
  ): Promise<AuthenticationResult> {
    // 第1要素：パスワード認証
    const passwordValid = await this.verifyPassword(
      credentials.username,
      credentials.password
    );
    
    if (!passwordValid) {
      await this.recordFailedAttempt(credentials.username);
      throw new AuthenticationError("Invalid credentials");
    }
    
    // 第2要素：MFA
    if (await this.isMFARequired(credentials.username)) {
      const mfaResult = await this.verifyMFA(
        credentials.username,
        credentials.mfaCode
      );
      
      if (!mfaResult.valid) {
        throw new AuthenticationError("Invalid MFA code");
      }
    }
    
    // リスクベース認証
    const riskScore = await this.assessRisk(credentials);
    if (riskScore > 0.7) {
      // 追加検証が必要
      await this.requireAdditionalVerification(credentials);
    }
    
    // JWTトークンの生成
    const tokens = await this.generateTokens(credentials.username);
    
    // セッション管理
    await this.createSession({
      userId: credentials.username,
      tokens,
      metadata: {
        ip: credentials.ip,
        userAgent: credentials.userAgent,
        location: await this.getLocation(credentials.ip)
      }
    });
    
    return {
      success: true,
      tokens,
      requiresAction: []
    };
  }
  
  // パスワード管理
  private async hashPassword(password: string): Promise<string> {
    // Argon2id使用（OWASP推奨）
    return await argon2.hash(password, {
      type: argon2.argon2id,
      memoryCost: 65536, // 64MB
      timeCost: 3,
      parallelism: 4,
      hashLength: 32
    });
  }
  
  // JWT実装
  generateTokens(userId: string): TokenPair {
    const payload = {
      sub: userId,
      iat: Math.floor(Date.now() / 1000),
      jti: uuid()
    };
    
    // アクセストークン（短命）
    const accessToken = jwt.sign(
      { ...payload, type: 'access' },
      this.config.accessTokenSecret,
      { 
        expiresIn: '15m',
        algorithm: 'RS256'
      }
    );
    
    // リフレッシュトークン（長命）
    const refreshToken = jwt.sign(
      { ...payload, type: 'refresh' },
      this.config.refreshTokenSecret,
      { 
        expiresIn: '7d',
        algorithm: 'RS256'
      }
    );
    
    return { accessToken, refreshToken };
  }
}
```

### 認可システム

```typescript
export class AuthorizationSystem {
  // RBAC + ABAC ハイブリッド実装
  async authorize(
    subject: Subject,
    action: Action,
    resource: Resource,
    context: Context
  ): Promise<AuthorizationResult> {
    // ロールベースのチェック
    const rbacResult = await this.checkRBAC(subject, action, resource);
    
    // 属性ベースのチェック
    const abacResult = await this.checkABAC(subject, action, resource, context);
    
    // ポリシー評価
    const decision = this.evaluatePolicy(rbacResult, abacResult);
    
    // 監査ログ
    await this.auditDecision({
      subject,
      action,
      resource,
      context,
      decision,
      timestamp: new Date()
    });
    
    return decision;
  }
  
  // ポリシー定義
  definePolicy(): PolicySet {
    return {
      policies: [
        {
          id: "order-access-policy",
          effect: "allow",
          subjects: ["role:customer"],
          actions: ["read", "update"],
          resources: ["order:*"],
          conditions: {
            // 自分の注文のみアクセス可能
            "resource.owner": { equals: "subject.id" }
          }
        },
        {
          id: "admin-access-policy",
          effect: "allow",
          subjects: ["role:admin"],
          actions: ["*"],
          resources: ["*"],
          conditions: {
            // 業務時間内のみ
            "context.time": { 
              between: ["09:00", "18:00"] 
            },
            // 特定IPからのみ
            "context.ip": { 
              in: ["10.0.0.0/8"] 
            }
          }
        },
        {
          id: "data-export-policy",
          effect: "deny",
          subjects: ["*"],
          actions: ["export"],
          resources: ["customer:*"],
          conditions: {
            // DLPポリシー
            "resource.classification": { 
              in: ["confidential", "restricted"] 
            }
          }
        }
      ]
    };
  }
  
  // 動的権限評価
  async evaluateDynamicPermission(
    request: PermissionRequest
  ): Promise<boolean> {
    // コンテキスト情報の収集
    const context = await this.gatherContext(request);
    
    // リスクスコアの計算
    const riskScore = await this.calculateRiskScore(context);
    
    // 適応型アクセス制御
    if (riskScore > 0.8) {
      // 高リスク：追加認証が必要
      return this.requireStepUpAuth(request);
    } else if (riskScore > 0.5) {
      // 中リスク：制限付きアクセス
      return this.grantLimitedAccess(request);
    } else {
      // 低リスク：通常アクセス
      return this.grantFullAccess(request);
    }
  }
}
```

## 入力検証とサニタイゼーション

### 包括的入力検証

```typescript
export class InputValidation {
  // 入力検証フレームワーク
  validateInput<T>(
    input: unknown,
    schema: ValidationSchema
  ): ValidatedInput<T> {
    // 1. 型チェック
    if (!this.validateType(input, schema.type)) {
      throw new ValidationError("Invalid type");
    }
    
    // 2. 長さ/サイズチェック
    if (!this.validateSize(input, schema.constraints)) {
      throw new ValidationError("Size constraints violated");
    }
    
    // 3. 形式チェック
    if (!this.validateFormat(input, schema.format)) {
      throw new ValidationError("Invalid format");
    }
    
    // 4. ビジネスルールチェック
    if (!this.validateBusinessRules(input, schema.rules)) {
      throw new ValidationError("Business rule violation");
    }
    
    // 5. サニタイゼーション
    const sanitized = this.sanitize(input, schema.sanitization);
    
    return {
      valid: true,
      value: sanitized as T,
      metadata: {
        validatedAt: new Date(),
        schema: schema.id
      }
    };
  }
  
  // SQLインジェクション対策
  protectAgainstSQLInjection(): SQLProtection {
    return {
      // パラメータ化クエリの強制
      queryBuilder: {
        select: (table: string, conditions: Conditions) => {
          const query = `SELECT * FROM ?? WHERE ?`;
          const params = [table, conditions];
          return { query, params };
        },
        
        insert: (table: string, data: Record<string, any>) => {
          const columns = Object.keys(data);
          const placeholders = columns.map(() => '?').join(', ');
          const query = `INSERT INTO ?? (${columns.join(', ')}) VALUES (${placeholders})`;
          const params = [table, ...Object.values(data)];
          return { query, params };
        }
      },
      
      // ストアドプロシージャの使用
      storedProcedures: {
        getUserOrders: `
          CREATE PROCEDURE GetUserOrders
            @UserId INT,
            @Status NVARCHAR(50) = NULL
          AS
          BEGIN
            SELECT * FROM Orders
            WHERE UserId = @UserId
            AND (@Status IS NULL OR Status = @Status)
          END
        `
      }
    };
  }
  
  // XSS対策
  protectAgainstXSS(): XSSProtection {
    return {
      // コンテキスト別エスケープ
      escaping: {
        html: (input: string) => {
          const map: Record<string, string> = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;'
          };
          return input.replace(/[&<>"'\/]/g, m => map[m]);
        },
        
        javascript: (input: string) => {
          return JSON.stringify(input).slice(1, -1);
        },
        
        url: (input: string) => {
          return encodeURIComponent(input);
        },
        
        css: (input: string) => {
          return input.replace(/[^a-zA-Z0-9]/g, '\\$&');
        }
      },
      
      // CSP（Content Security Policy）
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", "'nonce-{{nonce}}'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          imgSrc: ["'self'", "data:", "https:"],
          connectSrc: ["'self'", "wss://"],
          fontSrc: ["'self'"],
          objectSrc: ["'none'"],
          mediaSrc: ["'self'"],
          frameSrc: ["'none'"],
          baseUri: ["'self'"],
          formAction: ["'self'"],
          frameAncestors: ["'none'"],
          upgradeInsecureRequests: true
        }
      }
    };
  }
}
```

## 暗号化とデータ保護

### データ暗号化

```typescript
export class DataEncryption {
  // 暗号化レイヤー
  implementEncryption(): EncryptionStrategy {
    return {
      // 保存時暗号化
      atRest: {
        database: {
          method: "Transparent Data Encryption",
          algorithm: "AES-256",
          keyManagement: "AWS KMS"
        },
        
        fileStorage: {
          method: "Client-side encryption",
          implementation: `
            class FileEncryption {
              async encryptFile(file: Buffer): Promise<EncryptedFile> {
                // データキーの生成
                const dataKey = await crypto.randomBytes(32);
                
                // データキーの暗号化（エンベロープ暗号化）
                const encryptedDataKey = await this.kms.encrypt({
                  KeyId: this.masterKeyId,
                  Plaintext: dataKey
                });
                
                // ファイルの暗号化
                const iv = crypto.randomBytes(16);
                const cipher = crypto.createCipheriv('aes-256-gcm', dataKey, iv);
                
                const encrypted = Buffer.concat([
                  cipher.update(file),
                  cipher.final()
                ]);
                
                const tag = cipher.getAuthTag();
                
                // ゼロ化
                crypto.randomFillSync(dataKey);
                
                return {
                  encrypted,
                  encryptedDataKey: encryptedDataKey.CiphertextBlob,
                  iv,
                  tag
                };
              }
            }
          `
        }
      },
      
      // 転送時暗号化
      inTransit: {
        tls: {
          version: "1.3",
          cipherSuites: [
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256"
          ],
          certificatePinning: true,
          ocspStapling: true
        },
        
        apiEncryption: {
          method: "End-to-end encryption",
          implementation: `
            class E2EEncryption {
              async encryptRequest(data: any): Promise<EncryptedRequest> {
                // 一時的な鍵ペア生成
                const { publicKey, privateKey } = await crypto.subtle.generateKey(
                  { name: 'ECDH', namedCurve: 'P-384' },
                  true,
                  ['deriveBits']
                );
                
                // 共有秘密の導出
                const sharedSecret = await crypto.subtle.deriveBits(
                  { name: 'ECDH', public: serverPublicKey },
                  privateKey,
                  384
                );
                
                // AESキーの導出
                const aesKey = await crypto.subtle.deriveKey(
                  { name: 'HKDF', hash: 'SHA-384', salt, info },
                  sharedSecret,
                  { name: 'AES-GCM', length: 256 },
                  false,
                  ['encrypt']
                );
                
                // データの暗号化
                const iv = crypto.getRandomValues(new Uint8Array(12));
                const encrypted = await crypto.subtle.encrypt(
                  { name: 'AES-GCM', iv },
                  aesKey,
                  new TextEncoder().encode(JSON.stringify(data))
                );
                
                return {
                  encrypted,
                  publicKey: await crypto.subtle.exportKey('spki', publicKey),
                  iv
                };
              }
            }
          `
        }
      }
    };
  }
  
  // 鍵管理
  implementKeyManagement(): KeyManagementSystem {
    return {
      hierarchy: {
        master: "HSM-stored root key",
        kek: "Key Encryption Keys",
        dek: "Data Encryption Keys"
      },
      
      rotation: {
        policy: "90 days",
        implementation: `
          class KeyRotation {
            async rotateKeys(): Promise<void> {
              // 新しい鍵の生成
              const newKey = await this.generateKey();
              
              // 既存データの再暗号化
              await this.reencryptData(newKey);
              
              // 鍵のアーカイブ
              await this.archiveOldKey();
              
              // 新しい鍵のアクティベート
              await this.activateNewKey(newKey);
            }
          }
        `
      }
    };
  }
}
```

## セキュリティ監視とインシデント対応

### セキュリティ監視

```typescript
export class SecurityMonitoring {
  // SIEM実装
  implementSIEM(): SIEMConfiguration {
    return {
      // ログ収集
      logSources: [
        { type: "application", format: "json", retention: "90days" },
        { type: "system", format: "syslog", retention: "180days" },
        { type: "security", format: "cef", retention: "365days" },
        { type: "audit", format: "json", retention: "7years" }
      ],
      
      // 相関ルール
      correlationRules: [
        {
          name: "Brute Force Detection",
          condition: `
            event.type = "authentication_failed" 
            AND count() > 5 
            AND time_window = 5m 
            GROUP BY source_ip
          `,
          severity: "high",
          action: ["alert", "block_ip"]
        },
        {
          name: "Data Exfiltration",
          condition: `
            event.type = "data_access"
            AND sum(bytes_transferred) > 100MB
            AND time_window = 1h
            AND destination_ip NOT IN internal_networks
          `,
          severity: "critical",
          action: ["alert", "suspend_account", "notify_soc"]
        },
        {
          name: "Privilege Escalation",
          condition: `
            event.type = "privilege_change"
            AND new_privileges > old_privileges
            AND actor != approved_admins
          `,
          severity: "critical",
          action: ["alert", "revert_change", "investigate"]
        }
      ],
      
      // リアルタイム分析
      realtimeAnalytics: {
        anomalyDetection: {
          algorithm: "Isolation Forest",
          features: ["login_time", "location", "access_pattern"],
          threshold: 0.95
        },
        
        behaviorAnalysis: {
          baseline: "30 days",
          deviation: "3 sigma",
          adaptiveLearning: true
        }
      }
    };
  }
  
  // インシデントレスポンス
  async handleSecurityIncident(
    incident: SecurityIncident
  ): Promise<IncidentResponse> {
    const response = new IncidentResponse();
    
    // 1. 検知と分析
    const analysis = await this.analyzeIncident(incident);
    response.severity = analysis.severity;
    response.scope = analysis.affectedSystems;
    
    // 2. 封じ込め
    if (analysis.severity >= "high") {
      await this.containThreat({
        isolateSystem: analysis.compromisedSystems,
        blockAccess: analysis.suspiciousAccounts,
        preserveEvidence: true
      });
    }
    
    // 3. 根絶
    await this.eradicateThreat({
      removemalware: analysis.malwareIndicators,
      patchVulnerabilities: analysis.exploitedVulnerabilities,
      resetCredentials: analysis.compromisedCredentials
    });
    
    // 4. 復旧
    await this.recoverSystems({
      restoreData: analysis.affectedData,
      validateIntegrity: true,
      monitorForRecurrence: true
    });
    
    // 5. 事後分析
    const lessons = await this.postIncidentAnalysis(incident, response);
    await this.updateSecurityControls(lessons);
    
    return response;
  }
}
```

### 脆弱性管理

```typescript
export class VulnerabilityManagement {
  // 脆弱性スキャン
  async performSecurityScan(
    target: ScanTarget
  ): Promise<ScanResults> {
    const results: VulnerabilityReport[] = [];
    
    // 依存関係スキャン
    results.push(await this.scanDependencies(target));
    
    // コードスキャン
    results.push(await this.scanCode(target));
    
    // インフラスキャン
    results.push(await this.scanInfrastructure(target));
    
    // コンテナスキャン
    results.push(await this.scanContainers(target));
    
    return this.aggregateResults(results);
  }
  
  // 依存関係の脆弱性チェック
  private async scanDependencies(
    project: Project
  ): Promise<DependencyVulnerabilities> {
    const scanner = new DependencyScanner();
    
    // package.jsonの解析
    const dependencies = await scanner.parseDependencies(project);
    
    // 既知の脆弱性データベースとの照合
    const vulnerabilities = await scanner.checkVulnerabilities(dependencies, {
      databases: ["NVD", "GitHub Advisory", "Snyk DB"],
      severity: ["critical", "high", "medium", "low"]
    });
    
    // 修正の提案
    const remediation = await scanner.suggestRemediation(vulnerabilities);
    
    return {
      vulnerabilities,
      remediation,
      riskScore: this.calculateRiskScore(vulnerabilities)
    };
  }
  
  // セキュアコーディング検証
  implementSecureCoding(): SecureCodingPractices {
    return {
      // セキュアなデフォルト
      secureDefaults: {
        authentication: "required",
        encryption: "enabled",
        logging: "comprehensive",
        errorHandling: "secure"
      },
      
      // コーディング標準
      standards: {
        inputValidation: "whitelist approach",
        outputEncoding: "context-aware",
        authentication: "multi-factor",
        sessionManagement: "secure tokens",
        accessControl: "least privilege",
        cryptography: "approved algorithms",
        errorHandling: "no information leakage",
        logging: "security events included"
      },
      
      // 自動チェック
      automatedChecks: `
        // ESLintセキュリティルール
        module.exports = {
          plugins: ['security'],
          rules: {
            'security/detect-non-literal-regexp': 'error',
            'security/detect-buffer-noassert': 'error',
            'security/detect-child-process': 'error',
            'security/detect-disable-mustache-escape': 'error',
            'security/detect-eval-with-expression': 'error',
            'security/detect-no-csrf-before-method-override': 'error',
            'security/detect-non-literal-fs-filename': 'error',
            'security/detect-non-literal-require': 'error',
            'security/detect-object-injection': 'error',
            'security/detect-possible-timing-attacks': 'error',
            'security/detect-pseudoRandomBytes': 'error',
            'security/detect-unsafe-regex': 'error'
          }
        };
      `
    };
  }
}
```

## コンプライアンスとガバナンス

### プライバシー保護

```typescript
export class PrivacyProtection {
  // GDPR準拠実装
  implementGDPRCompliance(): GDPRImplementation {
    return {
      // データ主体の権利
      dataSubjectRights: {
        access: async (userId: string) => {
          return await this.exportUserData(userId);
        },
        
        rectification: async (userId: string, corrections: any) => {
          return await this.updateUserData(userId, corrections);
        },
        
        erasure: async (userId: string) => {
          return await this.deleteUserData(userId);
        },
        
        portability: async (userId: string) => {
          return await this.exportUserDataInMachineReadableFormat(userId);
        },
        
        restriction: async (userId: string, restrictions: any) => {
          return await this.restrictProcessing(userId, restrictions);
        }
      },
      
      // 同意管理
      consentManagement: {
        record: async (consent: ConsentRecord) => {
          return await this.storeConsent({
            ...consent,
            timestamp: new Date(),
            version: this.currentConsentVersion,
            ip: this.getClientIP(),
            method: "explicit"
          });
        },
        
        verify: async (userId: string, purpose: string) => {
          const consent = await this.getLatestConsent(userId, purpose);
          return consent && !consent.withdrawn;
        }
      },
      
      // データ最小化
      dataMinimization: {
        collection: "必要最小限のデータのみ収集",
        retention: "目的達成後は削除",
        anonymization: "可能な限り匿名化"
      }
    };
  }
  
  // データマスキング
  implementDataMasking(): DataMaskingStrategy {
    return {
      techniques: {
        static: {
          creditCard: (number: string) => {
            return number.replace(/\d(?=\d{4})/g, '*');
          },
          
          email: (email: string) => {
            const [local, domain] = email.split('@');
            return `${local.substring(0, 2)}***@${domain}`;
          },
          
          phone: (phone: string) => {
            return phone.replace(/\d(?=\d{4})/g, '*');
          }
        },
        
        dynamic: {
          contextual: (data: any, userRole: string) => {
            const maskingRules = this.getMaskingRules(userRole);
            return this.applyMasking(data, maskingRules);
          }
        }
      }
    };
  }
}
```

## セキュリティテストと検証

### セキュリティテスト自動化

```typescript
export class SecurityTesting {
  // ペネトレーションテスト
  async performPenetrationTest(
    target: Application
  ): Promise<PenTestResults> {
    const results: TestResult[] = [];
    
    // 認証バイパステスト
    results.push(await this.testAuthenticationBypass(target));
    
    // インジェクション攻撃テスト
    results.push(await this.testInjectionAttacks(target));
    
    // セッション管理テスト
    results.push(await this.testSessionManagement(target));
    
    // アクセス制御テスト
    results.push(await this.testAccessControl(target));
    
    // ビジネスロジックテスト
    results.push(await this.testBusinessLogic(target));
    
    return this.generatePenTestReport(results);
  }
  
  // セキュリティ回帰テスト
  createSecurityRegressionSuite(): TestSuite {
    return {
      tests: [
        {
          name: "SQL Injection Prevention",
          test: async () => {
            const payloads = [
              "' OR '1'='1",
              "1; DROP TABLE users--",
              "' UNION SELECT * FROM users--"
            ];
            
            for (const payload of payloads) {
              const response = await this.testEndpoint('/api/search', {
                query: payload
              });
              
              expect(response.status).not.toBe(500);
              expect(response.body).not.toContain('SQL');
            }
          }
        },
        {
          name: "XSS Prevention",
          test: async () => {
            const payloads = [
              "<script>alert('XSS')</script>",
              "javascript:alert('XSS')",
              "<img src=x onerror=alert('XSS')>"
            ];
            
            for (const payload of payloads) {
              const response = await this.testEndpoint('/api/comment', {
                text: payload
              });
              
              const rendered = await this.renderComment(response.id);
              expect(rendered).not.toContain('<script>');
              expect(rendered).not.toContain('javascript:');
              expect(rendered).not.toContain('onerror=');
            }
          }
        }
      ]
    };
  }
}
```

## まとめ

セキュリティは、システム開発の後付けではなく、設計段階から組み込むべき重要な要素です。Parasol V5.4における成功の鍵：

1. **多層防御** - 単一の対策に依存せず、複数の層で防御
2. **最小権限の原則** - 必要最小限のアクセス権限のみ付与
3. **継続的な監視** - リアルタイムでの脅威検知と対応
4. **セキュアバイデザイン** - 設計段階からセキュリティを考慮
5. **定期的な検証** - 脆弱性スキャンとペネトレーションテスト

適切に実装されたセキュリティは、ビジネスとユーザーの信頼を守る強固な基盤となります。

### 次章への架橋

システムのセキュリティを確保する方法を学びました。第28章では、システムを安定的に運用するための監視とロギングについて詳しく見ていきます。

---

## 演習問題

1. 以下のコードのセキュリティ脆弱性を特定し、修正案を提示してください：
   ```typescript
   app.post('/login', async (req, res) => {
     const { username, password } = req.body;
     const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
     const user = await db.query(query);
     
     if (user) {
       req.session.userId = user.id;
       res.json({ success: true, user });
     } else {
       res.json({ success: false, error: 'Invalid credentials' });
     }
   });
   ```

2. Webアプリケーションの多層防御戦略を設計してください。各層で実装すべきセキュリティ対策を具体的に挙げてください。

3. GDPRに準拠したユーザーデータ削除機能を実装する際の考慮事項と実装手順を説明してください。