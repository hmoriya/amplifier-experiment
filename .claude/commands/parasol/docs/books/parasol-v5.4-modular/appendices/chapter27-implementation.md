# Appendix: Chapter 27 Implementation - Security Controls and Frameworks

## Authentication and Authorization Implementation

### Multi-Factor Authentication System

```typescript
export class MultiFactorAuthentication {
  async authenticateUser(
    username: string, 
    password: string,
    mfaToken?: string,
    context: AuthenticationContext = {}
  ): Promise<AuthenticationResult> {
    // Primary factor - password verification
    const user = await this.verifyPassword(username, password);
    if (!user) {
      await this.recordFailedAttempt(username, context);
      return { success: false, reason: "Invalid credentials" };
    }
    
    // Risk assessment for context-aware authentication
    const riskScore = await this.assessRisk(user, context);
    
    if (riskScore >= RiskLevel.HIGH || user.requiresMFA) {
      if (!mfaToken) {
        const challenge = await this.generateMFAChallenge(user);
        return {
          success: false,
          requiresMFA: true,
          challenge,
          sessionToken: this.createTemporarySession(user.id)
        };
      }
      
      const mfaValid = await this.verifyMFA(user, mfaToken);
      if (!mfaValid) {
        return { success: false, reason: "Invalid MFA token" };
      }
    }
    
    // Generate authenticated session
    const session = await this.createSession(user, context);
    await this.recordSuccessfulAuthentication(user, context);
    
    return {
      success: true,
      session,
      user: this.sanitizeUserData(user)
    };
  }
  
  private async assessRisk(
    user: User, 
    context: AuthenticationContext
  ): Promise<RiskScore> {
    const factors = [];
    
    // Location-based risk
    const locationRisk = await this.assessLocationRisk(user, context.ipAddress);
    factors.push(locationRisk);
    
    // Device-based risk
    if (context.deviceFingerprint) {
      const deviceRisk = await this.assessDeviceRisk(user, context.deviceFingerprint);
      factors.push(deviceRisk);
    }
    
    // Time-based risk
    const timeRisk = this.assessTimeRisk(user, context.timestamp);
    factors.push(timeRisk);
    
    // Behavioral risk
    const behaviorRisk = await this.assessBehaviorRisk(user, context);
    factors.push(behaviorRisk);
    
    return this.calculateCompositeRisk(factors);
  }
  
  // TOTP (Time-based One-Time Password) implementation
  async setupTOTP(userId: string): Promise<TOTPSetup> {
    const secret = this.generateTOTPSecret();
    const qrCode = this.generateQRCode(userId, secret);
    
    // Store secret temporarily until confirmed
    await this.storePendingTOTPSecret(userId, secret);
    
    return {
      secret,
      qrCode,
      backupCodes: this.generateBackupCodes(),
      instructions: this.getTOTPInstructions()
    };
  }
  
  async verifyTOTP(userId: string, token: string): Promise<boolean> {
    const secret = await this.getTOTPSecret(userId);
    if (!secret) return false;
    
    // Allow for clock skew (±30 seconds)
    const currentWindow = Math.floor(Date.now() / 30000);
    
    for (let window = currentWindow - 1; window <= currentWindow + 1; window++) {
      const expectedToken = this.generateTOTPToken(secret, window);
      if (token === expectedToken) {
        // Prevent replay attacks
        await this.recordUsedToken(userId, token, window);
        return true;
      }
    }
    
    return false;
  }
}
```

### Attribute-Based Access Control (ABAC)

```typescript
export class AttributeBasedAccessControl {
  async evaluateAccess(request: AccessRequest): Promise<AccessDecision> {
    const context = await this.gatherContext(request);
    const policies = await this.getApplicablePolicies(request);
    
    for (const policy of policies) {
      const result = await this.evaluatePolicy(policy, context);
      
      if (result.effect === Effect.DENY) {
        return {
          allowed: false,
          reason: result.reason,
          policy: policy.id
        };
      }
      
      if (result.effect === Effect.ALLOW) {
        return {
          allowed: true,
          conditions: result.conditions,
          policy: policy.id
        };
      }
    }
    
    // Default deny
    return {
      allowed: false,
      reason: "No applicable allow policy found"
    };
  }
  
  private async gatherContext(request: AccessRequest): Promise<EvaluationContext> {
    const userAttributes = await this.getUserAttributes(request.principal);
    const resourceAttributes = await this.getResourceAttributes(request.resource);
    const environmentAttributes = this.getEnvironmentAttributes(request);
    
    return {
      user: userAttributes,
      resource: resourceAttributes,
      environment: environmentAttributes,
      action: request.action,
      timestamp: new Date()
    };
  }
  
  // Policy evaluation engine
  private async evaluatePolicy(
    policy: SecurityPolicy, 
    context: EvaluationContext
  ): Promise<PolicyResult> {
    try {
      // Evaluate target - does this policy apply?
      if (!await this.evaluateTarget(policy.target, context)) {
        return { effect: Effect.NOT_APPLICABLE };
      }
      
      // Evaluate condition - are the conditions met?
      if (policy.condition && !await this.evaluateCondition(policy.condition, context)) {
        return { effect: Effect.NOT_APPLICABLE };
      }
      
      // Policy applies and conditions are met
      return {
        effect: policy.effect,
        reason: policy.description,
        conditions: policy.obligations
      };
      
    } catch (error) {
      // Fail securely - errors result in deny
      return {
        effect: Effect.DENY,
        reason: `Policy evaluation error: ${error.message}`
      };
    }
  }
  
  // Example policies in code
  defineParasolSecurityPolicies(): SecurityPolicy[] {
    return [
      {
        id: "admin-full-access",
        description: "Administrators have full access from corporate network",
        target: {
          user: { roles: ["admin"] },
          environment: { network: "corporate" }
        },
        effect: Effect.ALLOW
      },
      
      {
        id: "user-own-data-access",
        description: "Users can access their own data",
        target: {
          action: ["read", "update"],
          resource: { type: "user-data" }
        },
        condition: "resource.owner == user.id",
        effect: Effect.ALLOW
      },
      
      {
        id: "sensitive-data-protection",
        description: "Sensitive data requires elevated privileges",
        target: {
          resource: { classification: "sensitive" },
          action: ["read", "download"]
        },
        condition: "user.clearanceLevel >= resource.requiredClearance",
        effect: Effect.ALLOW
      },
      
      {
        id: "time-based-access",
        description: "Administrative access only during business hours",
        target: {
          user: { roles: ["admin"] },
          action: ["admin"]
        },
        condition: "environment.time >= 09:00 && environment.time <= 17:00",
        effect: Effect.ALLOW
      },
      
      {
        id: "geographic-restriction",
        description: "Block access from restricted countries",
        target: {
          environment: { country: ["XX", "YY", "ZZ"] }
        },
        effect: Effect.DENY
      }
    ];
  }
}
```

## Input Validation and Security Controls

### Comprehensive Input Validation Framework

```typescript
export class InputValidationFramework {
  // SQL Injection Prevention
  createParameterizedQuery<T>(
    query: string,
    parameters: unknown[]
  ): ParameterizedQuery<T> {
    // Validate query doesn't contain dynamic SQL construction
    if (this.containsDynamicSQL(query)) {
      throw new SecurityError("Query contains dynamic SQL construction");
    }
    
    return {
      sql: query,
      parameters: this.sanitizeParameters(parameters),
      execute: async () => this.executeQuery<T>(query, parameters)
    };
  }
  
  // XSS Prevention with context-aware encoding
  encodeOutput(data: string, context: OutputContext): string {
    switch (context) {
      case OutputContext.HTML:
        return this.htmlEncode(data);
      case OutputContext.HTML_ATTRIBUTE:
        return this.htmlAttributeEncode(data);
      case OutputContext.JAVASCRIPT:
        return this.javascriptEncode(data);
      case OutputContext.CSS:
        return this.cssEncode(data);
      case OutputContext.URL:
        return encodeURIComponent(data);
      default:
        throw new Error(`Unsupported output context: ${context}`);
    }
  }
  
  // Input validation schemas
  createValidationSchema(): ValidationSchema {
    return {
      email: {
        pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
        maxLength: 254,
        sanitize: (email: string) => email.toLowerCase().trim()
      },
      
      password: {
        minLength: 12,
        pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
        validate: (password: string) => this.validatePasswordStrength(password)
      },
      
      fileName: {
        pattern: /^[a-zA-Z0-9._-]+$/,
        maxLength: 255,
        blacklist: ["con", "prn", "aux", "nul", "com1", "lpt1"],
        validate: (name: string) => !this.isExecutableExtension(name)
      },
      
      sqlIdentifier: {
        pattern: /^[a-zA-Z_][a-zA-Z0-9_]*$/,
        maxLength: 63,
        whitelist: this.getAllowedTableNames()
      }
    };
  }
  
  // File upload security
  async validateFileUpload(file: FileUpload): Promise<ValidationResult> {
    const validations = [
      await this.validateFileType(file),
      await this.validateFileSize(file),
      await this.validateFileName(file),
      await this.scanForMalware(file),
      await this.validateFileContent(file)
    ];
    
    const failed = validations.filter(v => !v.valid);
    
    return {
      valid: failed.length === 0,
      errors: failed.map(v => v.error),
      sanitizedFile: failed.length === 0 ? this.sanitizeFile(file) : null
    };
  }
  
  private async validateFileType(file: FileUpload): Promise<ValidationResult> {
    // Check MIME type
    const detectedMimeType = await this.detectMimeType(file.buffer);
    
    if (file.mimeType !== detectedMimeType) {
      return {
        valid: false,
        error: "File extension doesn't match content type"
      };
    }
    
    // Check against allowed types
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
    if (!allowedTypes.includes(file.mimeType)) {
      return {
        valid: false,
        error: `File type ${file.mimeType} not allowed`
      };
    }
    
    return { valid: true };
  }
  
  // Content Security Policy implementation
  generateCSP(): ContentSecurityPolicy {
    return {
      'default-src': ["'self'"],
      'script-src': [
        "'self'",
        "'nonce-" + this.generateNonce() + "'",
        'https://trusted-cdn.com'
      ],
      'style-src': ["'self'", "'unsafe-inline'"],
      'img-src': ["'self'", 'data:', 'https:'],
      'font-src': ["'self'", 'https://fonts.gstatic.com'],
      'connect-src': ["'self'", 'https://api.example.com'],
      'frame-ancestors': ["'none'"],
      'base-uri': ["'self'"],
      'form-action': ["'self'"]
    };
  }
}
```

## Encryption and Key Management

### Advanced Encryption Service

```typescript
export class EncryptionService {
  private keyManager: KeyManagementService;
  
  constructor(keyManager: KeyManagementService) {
    this.keyManager = keyManager;
  }
  
  // Encrypt data with authenticated encryption
  async encryptData(
    data: Buffer, 
    keyId: string,
    context?: EncryptionContext
  ): Promise<EncryptedData> {
    const key = await this.keyManager.getKey(keyId);
    const iv = crypto.randomBytes(12); // 96-bit IV for GCM
    const aad = this.createAAD(keyId, context);
    
    const cipher = crypto.createCipherGCM('aes-256-gcm');
    cipher.setAAD(aad);
    
    let encrypted = cipher.update(data);
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    const tag = cipher.getAuthTag();
    
    return {
      ciphertext: encrypted,
      iv,
      tag,
      keyId,
      algorithm: 'AES-256-GCM',
      context: context || {}
    };
  }
  
  async decryptData(encryptedData: EncryptedData): Promise<Buffer> {
    const key = await this.keyManager.getKey(encryptedData.keyId);
    const aad = this.createAAD(encryptedData.keyId, encryptedData.context);
    
    const decipher = crypto.createDecipherGCM('aes-256-gcm');
    decipher.setAAD(aad);
    decipher.setAuthTag(encryptedData.tag);
    
    let decrypted = decipher.update(encryptedData.ciphertext);
    decrypted = Buffer.concat([decrypted, decipher.final()]);
    
    return decrypted;
  }
  
  // Key derivation for password-based encryption
  async deriveKeyFromPassword(
    password: string,
    salt: Buffer,
    iterations: number = 600000
  ): Promise<Buffer> {
    return new Promise((resolve, reject) => {
      crypto.pbkdf2(password, salt, iterations, 32, 'sha256', (err, derivedKey) => {
        if (err) reject(err);
        else resolve(derivedKey);
      });
    });
  }
  
  // Digital signatures
  async signData(data: Buffer, privateKeyId: string): Promise<DigitalSignature> {
    const privateKey = await this.keyManager.getPrivateKey(privateKeyId);
    
    const signature = crypto.sign('sha256', data, {
      key: privateKey,
      padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
      saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST
    });
    
    return {
      signature,
      algorithm: 'RSA-PSS-SHA256',
      keyId: privateKeyId,
      timestamp: new Date()
    };
  }
  
  async verifySignature(
    data: Buffer, 
    signature: DigitalSignature
  ): Promise<boolean> {
    const publicKey = await this.keyManager.getPublicKey(signature.keyId);
    
    try {
      return crypto.verify('sha256', data, {
        key: publicKey,
        padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
        saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST
      }, signature.signature);
    } catch (error) {
      return false;
    }
  }
}

export class KeyManagementService {
  private hsm: HardwareSecurityModule;
  
  // Hierarchical key structure
  async createMasterKey(purpose: KeyPurpose): Promise<string> {
    const keySpec = {
      algorithm: 'AES',
      keyLength: 256,
      usage: ['encrypt', 'decrypt', 'derive'],
      extractable: false
    };
    
    const keyId = await this.hsm.generateKey(keySpec);
    
    await this.storeKeyMetadata(keyId, {
      purpose,
      level: 'master',
      created: new Date(),
      rotationSchedule: this.getRotationSchedule(purpose)
    });
    
    return keyId;
  }
  
  // Key rotation implementation
  async rotateKey(keyId: string): Promise<string> {
    const metadata = await this.getKeyMetadata(keyId);
    
    // Create new key with same specifications
    const newKeyId = await this.createMasterKey(metadata.purpose);
    
    // Re-encrypt data with new key
    await this.reencryptWithNewKey(keyId, newKeyId);
    
    // Schedule old key for deletion after grace period
    await this.scheduleKeyDeletion(keyId, new Date(Date.now() + 30 * 24 * 60 * 60 * 1000));
    
    return newKeyId;
  }
  
  // Key escrow for disaster recovery
  async createKeyEscrow(keyId: string, trustees: string[]): Promise<void> {
    const key = await this.exportKey(keyId);
    const shares = this.splitSecret(key, trustees.length, Math.ceil(trustees.length / 2));
    
    for (let i = 0; i < trustees.length; i++) {
      await this.securelyDeliverShare(trustees[i], shares[i]);
    }
    
    await this.recordEscrowCreation(keyId, trustees);
  }
}
```

## Security Monitoring and Incident Response

### Security Information and Event Management (SIEM)

```typescript
export class SIEMSystem {
  private ruleEngine: SecurityRuleEngine;
  private threatIntelligence: ThreatIntelligenceService;
  
  async processSecurityEvent(event: SecurityEvent): Promise<void> {
    // Normalize and enrich event
    const enrichedEvent = await this.enrichEvent(event);
    
    // Store for analysis
    await this.storeEvent(enrichedEvent);
    
    // Evaluate correlation rules
    const correlationResults = await this.evaluateCorrelationRules(enrichedEvent);
    
    // Check against threat intelligence
    const threatMatch = await this.checkThreatIntelligence(enrichedEvent);
    
    // Generate alerts if needed
    if (correlationResults.length > 0 || threatMatch.isMatch) {
      await this.generateSecurityAlert({
        event: enrichedEvent,
        correlations: correlationResults,
        threatMatch
      });
    }
  }
  
  private async enrichEvent(event: SecurityEvent): Promise<EnrichedSecurityEvent> {
    const enrichments = await Promise.all([
      this.geolocateIP(event.sourceIP),
      this.getUserContext(event.userId),
      this.getAssetContext(event.targetResource),
      this.getNetworkContext(event.sourceIP)
    ]);
    
    return {
      ...event,
      geolocation: enrichments[0],
      userContext: enrichments[1],
      assetContext: enrichments[2],
      networkContext: enrichments[3],
      enrichedAt: new Date()
    };
  }
  
  // Correlation rules for advanced threat detection
  defineCorrelationRules(): CorrelationRule[] {
    return [
      {
        name: "Brute Force Attack",
        description: "Multiple failed login attempts from same source",
        timeWindow: "5m",
        threshold: 10,
        conditions: [
          "event_type == 'authentication_failed'",
          "group_by: source_ip",
          "count >= 10"
        ],
        severity: "high"
      },
      
      {
        name: "Lateral Movement",
        description: "User accessing multiple systems rapidly",
        timeWindow: "15m",
        conditions: [
          "event_type == 'successful_login'",
          "group_by: user_id",
          "distinct_count(target_system) >= 5"
        ],
        severity: "medium"
      },
      
      {
        name: "Data Exfiltration",
        description: "Large amount of data accessed by single user",
        timeWindow: "1h",
        conditions: [
          "event_type == 'data_access'",
          "group_by: user_id",
          "sum(bytes_accessed) >= 1GB"
        ],
        severity: "high"
      },
      
      {
        name: "Privilege Escalation",
        description: "User accessing resources above their normal privileges",
        conditions: [
          "event_type == 'authorization_granted'",
          "required_privilege > user.normal_max_privilege"
        ],
        severity: "critical"
      },
      
      {
        name: "Off-Hours Activity",
        description: "Administrative activity during unusual hours",
        conditions: [
          "event_type == 'admin_action'",
          "(hour < 6 OR hour > 22)",
          "user.role == 'admin'"
        ],
        severity: "medium"
      }
    ];
  }
  
  // Automated incident response
  async executeResponsePlaybook(alert: SecurityAlert): Promise<void> {
    const playbook = this.getResponsePlaybook(alert.type);
    
    for (const action of playbook.actions) {
      try {
        await this.executeResponseAction(action, alert);
        
        await this.logResponseAction({
          action: action.name,
          alert: alert.id,
          timestamp: new Date(),
          status: 'success'
        });
        
      } catch (error) {
        await this.logResponseAction({
          action: action.name,
          alert: alert.id,
          timestamp: new Date(),
          status: 'failed',
          error: error.message
        });
        
        // Escalate if automated response fails
        if (action.critical) {
          await this.escalateToHuman(alert, error);
        }
      }
    }
  }
  
  private getResponsePlaybook(alertType: AlertType): ResponsePlaybook {
    const playbooks = {
      BRUTE_FORCE_ATTACK: {
        actions: [
          {
            name: "block_ip",
            critical: true,
            implementation: async (alert: SecurityAlert) => {
              await this.blockIPAddress(alert.sourceIP, '1h');
            }
          },
          {
            name: "notify_security_team",
            critical: false,
            implementation: async (alert: SecurityAlert) => {
              await this.sendSecurityNotification(alert);
            }
          }
        ]
      },
      
      DATA_EXFILTRATION: {
        actions: [
          {
            name: "suspend_user_account",
            critical: true,
            implementation: async (alert: SecurityAlert) => {
              await this.suspendUserAccount(alert.userId);
            }
          },
          {
            name: "start_investigation",
            critical: true,
            implementation: async (alert: SecurityAlert) => {
              await this.createIncident(alert, IncidentType.DATA_BREACH);
            }
          }
        ]
      }
    };
    
    return playbooks[alertType] || { actions: [] };
  }
}
```

## Vulnerability Management and Testing

### Security Testing Framework

```typescript
export class SecurityTestingFramework {
  // Static Application Security Testing (SAST)
  async runStaticAnalysis(codebase: string): Promise<SecurityIssue[]> {
    const scanners = [
      new SQLInjectionScanner(),
      new XSSScanner(),
      new HardcodedCredentialsScanner(),
      new CryptographyScanner(),
      new PathTraversalScanner()
    ];
    
    const issues: SecurityIssue[] = [];
    
    for (const scanner of scanners) {
      const scanResults = await scanner.scan(codebase);
      issues.push(...scanResults);
    }
    
    return this.prioritizeIssues(issues);
  }
  
  // Dynamic Application Security Testing (DAST)
  async runDynamicAnalysis(targetUrl: string): Promise<SecurityIssue[]> {
    const testSuite = new DynamicSecurityTestSuite(targetUrl);
    
    const tests = [
      testSuite.testAuthenticationBypass(),
      testSuite.testInputValidation(),
      testSuite.testSessionManagement(),
      testSuite.testAccessControls(),
      testSuite.testErrorHandling()
    ];
    
    const results = await Promise.all(tests);
    return results.flat();
  }
  
  // Interactive Application Security Testing (IAST)
  async runInteractiveAnalysis(application: Application): Promise<SecurityIssue[]> {
    const agent = new SecurityInstrumentationAgent();
    
    // Instrument application for runtime analysis
    await agent.instrument(application);
    
    // Run functional tests while monitoring for security issues
    const testResults = await this.runFunctionalTests(application);
    
    // Analyze runtime behavior
    const securityIssues = await agent.analyzeRuntimeBehavior();
    
    return securityIssues;
  }
  
  // Penetration testing automation
  async runPenetrationTests(target: Target): Promise<PenetrationTestReport> {
    const testPhases = [
      this.reconnaissance(target),
      this.scanning(target),
      this.enumeration(target),
      this.vulnerabilityAssessment(target),
      this.exploitation(target),
      this.postExploitation(target)
    ];
    
    const phaseResults = [];
    
    for (const phase of testPhases) {
      try {
        const result = await phase;
        phaseResults.push(result);
        
        // Stop if high-severity vulnerability found
        if (result.severity === 'critical') {
          break;
        }
        
      } catch (error) {
        phaseResults.push({
          phase: phase.name,
          status: 'failed',
          error: error.message
        });
      }
    }
    
    return this.generatePenetrationTestReport(phaseResults);
  }
}

// Specific security scanners
class SQLInjectionScanner {
  async scan(code: string): Promise<SecurityIssue[]> {
    const issues: SecurityIssue[] = [];
    
    // Pattern for SQL query construction
    const sqlPatterns = [
      /query\s*\(\s*["`'].*\$\{.*\}.*["`']/g,
      /execute\s*\(\s*["`'].*\+.*["`']/g,
      /"SELECT.*"\s*\+/g
    ];
    
    for (const pattern of sqlPatterns) {
      const matches = code.match(pattern);
      if (matches) {
        for (const match of matches) {
          issues.push({
            type: 'SQL_INJECTION',
            severity: 'high',
            description: 'Potential SQL injection vulnerability detected',
            evidence: match,
            recommendation: 'Use parameterized queries or prepared statements',
            cweId: 'CWE-89'
          });
        }
      }
    }
    
    return issues;
  }
}

class CryptographyScanner {
  async scan(code: string): Promise<SecurityIssue[]> {
    const issues: SecurityIssue[] = [];
    
    // Weak cryptographic algorithms
    const weakAlgorithms = ['md5', 'sha1', 'des', 'rc4'];
    
    for (const algorithm of weakAlgorithms) {
      const pattern = new RegExp(`\\b${algorithm}\\b`, 'gi');
      const matches = code.match(pattern);
      
      if (matches) {
        issues.push({
          type: 'WEAK_CRYPTOGRAPHY',
          severity: 'medium',
          description: `Weak cryptographic algorithm detected: ${algorithm}`,
          recommendation: 'Use strong cryptographic algorithms (AES-256, SHA-256)',
          cweId: 'CWE-327'
        });
      }
    }
    
    // Hardcoded cryptographic keys
    const keyPatterns = [
      /["\'][a-fA-F0-9]{32,}["\']/g, // Hex keys
      /["\'][A-Za-z0-9+/]{40,}={0,2}["\']/g // Base64 keys
    ];
    
    for (const pattern of keyPatterns) {
      const matches = code.match(pattern);
      if (matches) {
        for (const match of matches) {
          issues.push({
            type: 'HARDCODED_CRYPTOGRAPHIC_KEY',
            severity: 'critical',
            description: 'Hardcoded cryptographic key detected',
            evidence: match.substring(0, 20) + '...',
            recommendation: 'Store cryptographic keys securely using key management systems',
            cweId: 'CWE-798'
          });
        }
      }
    }
    
    return issues;
  }
}
```

## Compliance and Privacy Implementation

### GDPR Privacy Framework

```typescript
export class GDPRComplianceFramework {
  // Data processing legal basis tracking
  async recordProcessingBasis(
    dataSubjectId: string,
    processingPurpose: string,
    legalBasis: LegalBasis,
    consentDetails?: ConsentRecord
  ): Promise<void> {
    const record: ProcessingRecord = {
      id: this.generateId(),
      dataSubjectId,
      purpose: processingPurpose,
      legalBasis,
      consentDetails,
      timestamp: new Date(),
      status: 'active'
    };
    
    await this.dataProcessingRegistry.store(record);
    
    // Set up automatic review for consent-based processing
    if (legalBasis === LegalBasis.CONSENT && consentDetails) {
      await this.scheduleConsentReview(record, consentDetails.expiryDate);
    }
  }
  
  // Data subject rights implementation
  async handleAccessRequest(dataSubjectId: string): Promise<DataPortabilityPackage> {
    // Collect all personal data for the subject
    const personalData = await this.collectPersonalData(dataSubjectId);
    
    // Create structured export
    const dataPackage: DataPortabilityPackage = {
      dataSubject: {
        id: dataSubjectId,
        exportDate: new Date(),
        format: 'JSON'
      },
      
      personalData: {
        profile: personalData.profile,
        preferences: personalData.preferences,
        transactionHistory: personalData.transactions,
        communicationHistory: personalData.communications
      },
      
      processingActivities: await this.getProcessingActivities(dataSubjectId),
      
      metadata: {
        dataRetentionPolicies: await this.getRetentionPolicies(),
        thirdPartySharing: await this.getThirdPartySharing(dataSubjectId)
      }
    };
    
    // Log the access request for compliance audit
    await this.logDataSubjectRequest({
      type: 'access',
      dataSubjectId,
      timestamp: new Date(),
      status: 'fulfilled'
    });
    
    return dataPackage;
  }
  
  async handleErasureRequest(dataSubjectId: string): Promise<ErasureResult> {
    // Check if erasure is legally required or permitted
    const erasureAssessment = await this.assessErasureRequest(dataSubjectId);
    
    if (!erasureAssessment.permitted) {
      return {
        status: 'rejected',
        reason: erasureAssessment.reason,
        legalBasis: erasureAssessment.conflictingLegalBasis
      };
    }
    
    // Execute erasure across all systems
    const erasureResults = await Promise.all([
      this.eraseFromPrimaryDatabase(dataSubjectId),
      this.eraseFromBackups(dataSubjectId),
      this.eraseFromAnalytics(dataSubjectId),
      this.eraseFromThirdPartySystems(dataSubjectId)
    ]);
    
    // Verify erasure completion
    const verificationResult = await this.verifyErasureCompletion(dataSubjectId);
    
    return {
      status: verificationResult.complete ? 'completed' : 'partial',
      erasedSystems: erasureResults.filter(r => r.success).map(r => r.system),
      failedSystems: erasureResults.filter(r => !r.success).map(r => r.system),
      verificationDate: new Date()
    };
  }
  
  // Privacy by design implementation
  createPrivacyImpactAssessment(systemDesign: SystemDesign): PrivacyImpactAssessment {
    const assessment: PrivacyImpactAssessment = {
      systemOverview: systemDesign.description,
      dataTypes: this.identifyPersonalData(systemDesign),
      processingPurposes: this.identifyProcessingPurposes(systemDesign),
      legalBasis: this.determineLegalBasis(systemDesign),
      
      riskAnalysis: {
        privacyRisks: this.identifyPrivacyRisks(systemDesign),
        likelihood: this.assessLikelihood(systemDesign),
        impact: this.assessImpact(systemDesign),
        mitigationMeasures: this.recommendMitigations(systemDesign)
      },
      
      designRecommendations: {
        dataMinimization: this.recommendDataMinimization(systemDesign),
        purposeLimitation: this.recommendPurposeLimitation(systemDesign),
        storageMinimization: this.recommendStorageMinimization(systemDesign),
        technicalSafeguards: this.recommendTechnicalSafeguards(systemDesign)
      },
      
      complianceValidation: {
        gdprCompliance: this.validateGDPRCompliance(systemDesign),
        localRegulationCompliance: this.validateLocalCompliance(systemDesign),
        industryStandardCompliance: this.validateIndustryStandards(systemDesign)
      }
    };
    
    return assessment;
  }
  
  // Automated data retention management
  async enforceRetentionPolicies(): Promise<void> {
    const retentionPolicies = await this.getActiveRetentionPolicies();
    
    for (const policy of retentionPolicies) {
      const expiredData = await this.findExpiredData(policy);
      
      for (const dataRecord of expiredData) {
        try {
          if (policy.action === 'delete') {
            await this.deleteExpiredData(dataRecord);
          } else if (policy.action === 'anonymize') {
            await this.anonymizeExpiredData(dataRecord);
          } else if (policy.action === 'archive') {
            await this.archiveExpiredData(dataRecord);
          }
          
          await this.logRetentionAction({
            policy: policy.id,
            dataRecord: dataRecord.id,
            action: policy.action,
            timestamp: new Date()
          });
          
        } catch (error) {
          await this.logRetentionError({
            policy: policy.id,
            dataRecord: dataRecord.id,
            error: error.message,
            timestamp: new Date()
          });
        }
      }
    }
  }
}
```