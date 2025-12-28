# Appendix: Chapter 24 Implementation - Code Review Tools and Frameworks

## Review Process Implementation

### Multi-Stage Review Pipeline

```typescript
export class CodeReviewProcess {
  private readonly stages: ReviewStage[] = [
    {
      name: "自己レビュー",
      description: "作者自身による最初のチェック",
      checklist: [
        "テストはすべてパスしているか",
        "コーディング規約に準拠しているか",
        "不要なコメントやデバッグコードは削除したか",
        "変更の意図は明確か"
      ]
    },
    {
      name: "自動レビュー",
      description: "ツールによる機械的チェック",
      tools: ["ESLint", "Prettier", "SonarQube", "Security Scanner"]
    },
    {
      name: "ピアレビュー",
      description: "同僚による詳細レビュー",
      focus: ["ロジック", "可読性", "保守性", "パフォーマンス"]
    },
    {
      name: "アーキテクトレビュー",
      description: "設計の妥当性確認",
      criteria: ["設計原則", "将来の拡張性", "技術的負債"]
    }
  ];
  
  async conductReview(
    pullRequest: PullRequest
  ): Promise<ReviewResult> {
    const results: StageResult[] = [];
    
    for (const stage of this.stages) {
      const result = await this.executeStage(stage, pullRequest);
      results.push(result);
      
      if (result.status === ReviewStatus.BLOCKED) {
        return this.createBlockedResult(results);
      }
    }
    
    return this.createApprovedResult(results);
  }
}
```

### Automated Review Tools Configuration

```typescript
export class AutomatedReviewTools {
  // ESLint Configuration for Parasol V5.4
  eslintConfig = {
    extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
    rules: {
      "no-console": "error",
      "no-unused-vars": "error",
      "complexity": ["error", { max: 10 }],
      "max-lines-per-function": ["error", { max: 50 }],
      "parasol-naming-convention": "error"
    },
    
    customRules: {
      "parasol-naming-convention": {
        create(context) {
          return {
            ClassDeclaration(node) {
              if (!node.id.name.match(/^[A-Z][a-zA-Z]*$/)) {
                context.report({
                  node,
                  message: "Class names must be in PascalCase"
                });
              }
            },
            FunctionDeclaration(node) {
              if (!node.id.name.match(/^[a-z][a-zA-Z]*$/)) {
                context.report({
                  node,
                  message: "Function names must be in camelCase"
                });
              }
            }
          };
        }
      }
    }
  };
  
  // SonarQube Quality Gates
  sonarQubeConfig = {
    qualityGates: {
      coverage: 80,
      duplications: 3,
      maintainabilityRating: "A",
      reliabilityRating: "A",
      securityRating: "A",
      bugs: 0,
      vulnerabilities: 0,
      codeSmells: 10
    },
    
    exclusions: [
      "**/node_modules/**",
      "**/test/**/*.spec.ts",
      "**/dist/**",
      "**/*.generated.ts"
    ]
  };
}
```

## Review Comment Templates

### Constructive Feedback Templates

```typescript
export class ReviewCommentGuide {
  templates = {
    suggestion: (issue: string, solution: string, reason?: string) => `
      **問題**: ${issue}
      **提案**: ${solution}
      ${reason ? `**理由**: ${reason}` : ''}
    `,
    
    question: (context: string, question: string) => `
      **コンテキスト**: ${context}
      **質問**: ${question}
      意図を教えていただけますか？私の理解が間違っているかもしれません。
    `,
    
    nitpick: (issue: string) => `
      nit: ${issue}
      （必須ではありませんが、統一性のために修正を検討してください）
    `,
    
    praise: (what: string, why: string) => `
      👍 ${what}
      ${why}
    `,
    
    securityConcern: (vulnerability: string, impact: string, mitigation: string) => `
      🔒 **セキュリティ懸念**: ${vulnerability}
      **影響**: ${impact}
      **対策**: ${mitigation}
    `,
    
    performanceImpact: (issue: string, impact: string, alternative: string) => `
      ⚡ **パフォーマンス影響**: ${issue}
      **影響度**: ${impact}
      **代替案**: ${alternative}
    `
  };
  
  severityLevels = {
    MUST: "🚨 必須: マージ前に必ず修正が必要",
    SHOULD: "⚠️ 推奨: 修正を強く推奨",
    CONSIDER: "💭 検討: 改善の余地あり", 
    NITPICK: "💡 些細: 統一性のための提案"
  };
  
  // Good vs Bad Examples
  examples = {
    constructive: {
      bad: "この実装はダメです。",
      good: "この実装だとN+1問題が発生する可能性があります。バッチ取得を検討してはどうでしょうか？"
    },
    specific: {
      bad: "パフォーマンスが悪いです。",
      good: "このループは最悪計算量O(n²)になります。HashMapを使えばO(n)に改善できます。"
    },
    educational: {
      bad: "間違ってます。",
      good: "TypeScriptではnullとundefinedは異なります。この場合はundefinedチェックも必要です。参考: [リンク]"
    }
  };
}
```

## Team Review Strategy Implementation

### Reviewer Assignment Algorithm

```typescript
export class TeamReviewStrategy {
  assignReviewers(pr: PullRequest): Reviewer[] {
    const reviewers: Reviewer[] = [];
    
    // Code owners based on CODEOWNERS file
    const codeOwners = this.findCodeOwners(pr.files);
    reviewers.push(...codeOwners);
    
    // Domain experts based on expertise matrix
    const domainExperts = this.findDomainExperts(pr.context);
    reviewers.push(...domainExperts);
    
    // Random reviewer for knowledge sharing
    const randomReviewer = this.selectRandomReviewer(
      pr.author,
      [...codeOwners, ...domainExperts]
    );
    reviewers.push(randomReviewer);
    
    return this.removeDuplicates(reviewers);
  }
  
  private findCodeOwners(files: string[]): Reviewer[] {
    const codeOwners: Reviewer[] = [];
    
    for (const file of files) {
      const owners = this.codeownersConfig.getOwnersForFile(file);
      codeOwners.push(...owners);
    }
    
    return codeOwners;
  }
  
  private findDomainExperts(context: PRContext): Reviewer[] {
    const experts: Reviewer[] = [];
    
    if (context.touches.includes("security")) {
      experts.push(...this.getSecurityExperts());
    }
    
    if (context.touches.includes("performance")) {
      experts.push(...this.getPerformanceExperts());
    }
    
    if (context.touches.includes("database")) {
      experts.push(...this.getDatabaseExperts());
    }
    
    return experts;
  }
  
  // Load balancing for review assignment
  implementRotation(): RotationSchedule {
    return {
      weekly: {
        primaryReviewer: this.rotatePrimary(),
        backupReviewer: this.rotateBackup()
      },
      
      loadBalancing: {
        maxReviewsPerWeek: 10,
        maxReviewsPerDay: 3,
        distributionStrategy: "round-robin"
      },
      
      expertise: {
        matchingStrategy: "best-fit",
        learningOpportunities: true,
        mentorshipPairs: this.createMentorshipPairs()
      }
    };
  }
}
```

## Pull Request Optimization

### PR Size and Structure Analysis

```typescript
export class PullRequestOptimization {
  optimizeSize(changes: FileChange[]): PullRequestStrategy {
    const stats = this.analyzeChanges(changes);
    
    if (stats.linesChanged > 500) {
      return {
        strategy: "分割",
        recommendation: "機能単位でPRを分割してください",
        suggestions: this.suggestSplitPoints(changes)
      };
    }
    
    if (stats.filesChanged > 20) {
      return {
        strategy: "段階的",
        recommendation: "リファクタリングと機能追加を分けてください",
        phases: this.suggestPhases(changes)
      };
    }
    
    return {
      strategy: "そのまま",
      recommendation: "適切なサイズです"
    };
  }
  
  // PR Template Generation
  generatePRTemplate(): PullRequestTemplate {
    return {
      title: {
        format: "[タイプ] 簡潔な説明",
        examples: [
          "[feat] ユーザー認証機能の追加",
          "[fix] ログイン時のセッションエラー修正", 
          "[refactor] 注文処理の最適化",
          "[docs] APIドキュメントの更新"
        ]
      },
      
      description: {
        sections: [
          {
            heading: "## 概要",
            content: "このPRで解決する問題や追加する機能の説明"
          },
          {
            heading: "## 変更内容", 
            content: "- 主な変更点のリスト\n- 技術的な詳細\n- 設計上の決定"
          },
          {
            heading: "## テスト",
            content: "- 追加したテスト\n- 手動テストの手順\n- 動作確認の結果"
          },
          {
            heading: "## レビューポイント",
            content: "- 特に見てほしい部分\n- 懸念事項\n- 代替案の検討"
          },
          {
            heading: "## 影響範囲",
            content: "- 影響を受けるシステム\n- 後方互換性\n- データマイグレーション"
          }
        ]
      }
    };
  }
  
  // Automated PR Preparation
  async automatePreparation(pr: PullRequest): Promise<void> {
    // Context gathering
    const context = await this.gatherContext(pr);
    
    // Related documentation
    const docs = await this.findRelatedDocumentation(pr);
    
    // Impact analysis
    const impact = await this.analyzeImpact(pr);
    
    // Test coverage analysis
    const coverage = await this.analyzeCoverage(pr);
    
    // Generate review summary
    const summary = this.generateReviewSummary({
      context,
      docs,
      impact,
      coverage,
      changes: pr.changes
    });
    
    await this.postComment(pr, summary);
  }
}
```

## Architecture and Security Review Implementation

### Architecture Compliance Checking

```typescript
export class ArchitectureReview {
  checkDesignPrinciples(code: SourceCode): DesignViolations {
    const violations: Violation[] = [];
    
    // SOLID Principles Check
    violations.push(...this.checkSOLID(code));
    
    // DDD Principles Check
    violations.push(...this.checkDDD(code));
    
    // Parasol V5.4 Specific Principles
    violations.push(...this.checkParasolPrinciples(code));
    
    return this.categorizeViolations(violations);
  }
  
  private checkSOLID(code: SourceCode): Violation[] {
    const violations: Violation[] = [];
    
    // Single Responsibility Principle
    const classes = code.findClasses();
    for (const cls of classes) {
      const responsibilities = this.analyzeResponsibilities(cls);
      if (responsibilities.length > 1) {
        violations.push({
          principle: "SRP",
          location: cls.location,
          message: `クラス${cls.name}は複数の責任を持っています: ${responsibilities.join(", ")}`,
          severity: "warning",
          suggestion: "責任ごとにクラスを分割することを検討してください"
        });
      }
    }
    
    // Dependency Inversion Principle
    const dependencies = code.findDependencies();
    for (const dep of dependencies) {
      if (this.isConcreteImplementation(dep) && !this.hasAbstraction(dep)) {
        violations.push({
          principle: "DIP",
          location: dep.location,
          message: "具象クラスへの直接依存が検出されました",
          severity: "warning",
          suggestion: "インターフェースまたは抽象クラスを介した依存に変更してください"
        });
      }
    }
    
    return violations;
  }
  
  // Performance Review
  async performanceReview(code: SourceCode): Promise<PerformanceAnalysis> {
    const analysis: PerformanceAnalysis = {
      algorithms: [],
      database: [],
      memory: [],
      concurrency: []
    };
    
    // Algorithm complexity analysis
    const algorithms = this.analyzeAlgorithms(code);
    for (const algo of algorithms) {
      if (algo.complexity.time === "O(n^2)" || algo.complexity.time === "O(n^3)") {
        analysis.algorithms.push({
          location: algo.location,
          issue: `二次または三次の時間計算量: ${algo.complexity.time}`,
          impact: "大規模データで性能問題の可能性",
          suggestion: "より効率的なアルゴリズムを検討してください"
        });
      }
    }
    
    // Database access patterns
    const queries = this.findDatabaseQueries(code);
    for (const query of queries) {
      if (this.isNPlusOne(query)) {
        analysis.database.push({
          location: query.location,
          issue: "N+1クエリ問題",
          impact: "データベースへの過剰なアクセス",
          suggestion: "JOINまたはバッチ取得を使用してください"
        });
      }
    }
    
    return analysis;
  }
}
```

### Security Review Implementation

```typescript
export class SecurityReview {
  async detectVulnerabilities(code: SourceCode): Promise<SecurityIssue[]> {
    const issues: SecurityIssue[] = [];
    
    // OWASP Top 10 checks
    issues.push(...await this.checkOWASPTop10(code));
    
    // Sensitive data exposure
    issues.push(...this.checkSensitiveDataExposure(code));
    
    // Authentication and authorization
    issues.push(...this.checkAuthenticationAuthorization(code));
    
    return issues;
  }
  
  private checkOWASPTop10(code: SourceCode): SecurityIssue[] {
    const issues: SecurityIssue[] = [];
    
    // A1: Injection
    const sqlQueries = code.findPattern(/query\(|execute\(/g);
    for (const query of sqlQueries) {
      if (this.hasStringConcatenation(query)) {
        issues.push({
          type: "SQL Injection",
          severity: "critical",
          location: query.location,
          description: "SQLクエリで文字列結合を使用しています",
          fix: "パラメータ化クエリを使用してください",
          example: `
            // Bad
            db.query(\`SELECT * FROM users WHERE id = \${userId}\`);
            
            // Good  
            db.query('SELECT * FROM users WHERE id = ?', [userId]);
          `
        });
      }
    }
    
    // A3: Sensitive Data Exposure
    const sensitivePatterns = [
      /password\s*=\s*["'](.+)["']/gi,
      /api_key\s*=\s*["'](.+)["']/gi,
      /secret\s*=\s*["'](.+)["']/gi
    ];
    
    for (const pattern of sensitivePatterns) {
      const matches = code.findPattern(pattern);
      for (const match of matches) {
        issues.push({
          type: "Hardcoded Credentials",
          severity: "high",
          location: match.location,
          description: "機密情報がハードコードされています",
          fix: "環境変数または安全な設定管理システムを使用してください"
        });
      }
    }
    
    return issues;
  }
}
```

## Metrics and Analytics

### Review Metrics Collection

```typescript
export class ReviewMetrics {
  trackMetrics(): ReviewMetrics {
    return {
      efficiency: {
        averageReviewTime: this.calculateAverageReviewTime(),
        firstResponseTime: this.calculateFirstResponseTime(), 
        totalTurnaroundTime: this.calculateTurnaroundTime()
      },
      
      quality: {
        defectsFound: this.countDefectsFound(),
        defectEscapeRate: this.calculateEscapeRate(),
        reworkRate: this.calculateReworkRate()
      },
      
      participation: {
        reviewerDistribution: this.analyzeReviewerDistribution(),
        authorResponseRate: this.calculateResponseRate(),
        discussionDepth: this.measureDiscussionDepth()
      },
      
      learning: {
        knowledgeTransfer: this.measureKnowledgeTransfer(),
        improvementTrends: this.analyzeImprovementTrends(),
        bestPracticesAdoption: this.trackBestPracticesAdoption()
      }
    };
  }
  
  generateReviewReport(period: DateRange): ReviewReport {
    const metrics = this.collectMetricsForPeriod(period);
    
    return {
      summary: {
        totalReviews: metrics.totalReviews,
        averageSize: metrics.averageSize,
        participationRate: metrics.participationRate
      },
      
      quality_trends: {
        defectReduction: this.calculateDefectReduction(metrics),
        reviewThoroughness: this.calculateThoroughness(metrics),
        codeQualityImprovement: this.measureQualityImprovement(metrics)
      },
      
      team_insights: {
        topReviewers: this.identifyTopReviewers(metrics),
        knowledgeSharingEffectiveness: this.measureKnowledgeSharing(metrics),
        bottlenecks: this.identifyBottlenecks(metrics)
      },
      
      recommendations: this.generateRecommendations(metrics)
    };
  }
}
```

## Integration with Development Tools

### GitHub/GitLab Integration

```typescript
export class ReviewToolIntegration {
  integrateWithGitHub(): GitHubIntegration {
    return {
      prTemplate: ".github/pull_request_template.md",
      
      requiredChecks: [
        "continuous-integration/github-actions",
        "security/snyk",
        "quality/sonarcloud",
        "coverage/codecov"
      ],
      
      branchProtection: {
        requireReviews: true,
        requiredReviewers: 2,
        dismissStaleReviews: true,
        includeAdmins: false,
        strictStatusChecks: true
      },
      
      automation: {
        autoAssignReviewers: {
          enabled: true,
          algorithm: "load-balanced",
          excludeAuthors: true
        },
        
        autoLabel: {
          enabled: true,
          labels: {
            "size/S": "1-10 files changed",
            "size/M": "11-30 files changed", 
            "size/L": "31+ files changed",
            "security": "touches security-critical files",
            "performance": "touches performance-critical files"
          }
        },
        
        autoMerge: {
          enabled: true,
          conditions: [
            "all-checks-passed",
            "approved-by-required-reviewers",
            "no-merge-conflicts",
            "up-to-date-with-base"
          ]
        }
      },
      
      webhooks: {
        reviewSubmitted: this.handleReviewSubmitted,
        prOpened: this.handlePROpened,
        prUpdated: this.handlePRUpdated
      }
    };
  }
  
  // Custom Review Bot Implementation
  createParasolReviewBot(): ReviewBot {
    return {
      name: "Parasol Review Assistant",
      
      triggers: [
        "pr.opened",
        "pr.synchronize", 
        "review.submitted"
      ],
      
      actions: [
        {
          name: "Architecture Compliance Check",
          trigger: "pr.opened",
          implementation: async (pr: PullRequest) => {
            const violations = await this.checkArchitectureCompliance(pr);
            if (violations.length > 0) {
              await this.postArchitectureReview(pr, violations);
            }
          }
        },
        
        {
          name: "Performance Impact Analysis",
          trigger: "pr.opened",
          implementation: async (pr: PullRequest) => {
            const impact = await this.analyzePerformanceImpact(pr);
            if (impact.significance > 0.1) {
              await this.postPerformanceWarning(pr, impact);
            }
          }
        },
        
        {
          name: "Documentation Coverage",
          trigger: "pr.synchronize", 
          implementation: async (pr: PullRequest) => {
            const coverage = await this.checkDocumentationCoverage(pr);
            if (coverage < 0.8) {
              await this.requestDocumentationUpdate(pr, coverage);
            }
          }
        }
      ]
    };
  }
}
```