# 第24章　コードレビュー ― 集合知の活用

## はじめに：職人の師弟制度

伝統工芸の世界では、師匠が弟子の作品を丁寧に見て、技術の向上を促します。単なる誤りの指摘ではなく、より良い技法の伝授、美意識の共有、そして職人としての心構えの伝承が行われます。ソフトウェア開発におけるコードレビューも、まさにこの師弟制度の現代版です。

本章では、Parasol V5.4の文脈で、効果的なコードレビューの実践方法と、チームの集合知を最大限に活用する仕組みを解説します。

## コードレビューの本質

### レビューの目的と価値

```typescript
export interface CodeReviewPurpose {
  primary: {
    knowledgeSharing: "チーム全体の知識レベル向上";
    qualityAssurance: "バグの早期発見と品質向上";
    standardsEnforcement: "コーディング規約の遵守";
    architectureAlignment: "アーキテクチャ原則の維持";
  };
  
  secondary: {
    mentoring: "経験の共有と技術指導";
    documentation: "コードの意図と設計の記録";
    teamBuilding: "チームの結束力向上";
    continuousImprovement: "プロセスの継続的改善";
  };
  
  metrics: {
    defectDetectionRate: number;  // 欠陥発見率
    knowledgeTransferScore: number; // 知識伝達スコア
    reviewTurnaroundTime: Duration; // レビュー所要時間
    implementationQuality: number;  // 実装品質スコア
  };
}
```

### レビュープロセスの設計

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
  
  private async executeStage(
    stage: ReviewStage,
    pr: PullRequest
  ): Promise<StageResult> {
    switch (stage.name) {
      case "自己レビュー":
        return await this.conductSelfReview(pr);
      
      case "自動レビュー":
        return await this.runAutomatedChecks(pr);
      
      case "ピアレビュー":
        return await this.conductPeerReview(pr);
      
      case "アーキテクトレビュー":
        return await this.conductArchitectReview(pr);
      
      default:
        throw new Error(`Unknown review stage: ${stage.name}`);
    }
  }
}
```

## 効果的なレビューの実践

### レビューチェックリスト

```typescript
export class ReviewChecklist {
  // 機能性のチェック
  functionality = {
    correctness: [
      "要求仕様を満たしているか",
      "エッジケースは考慮されているか",
      "エラーハンドリングは適切か",
      "並行性の問題はないか"
    ],
    
    completeness: [
      "必要な機能がすべて実装されているか",
      "テストケースは網羅的か",
      "ドキュメントは更新されているか",
      "設定ファイルは適切か"
    ]
  };
  
  // 設計のチェック
  design = {
    architecture: [
      "レイヤーアーキテクチャに従っているか",
      "依存関係は適切か",
      "責任の分離は明確か",
      "将来の拡張性は考慮されているか"
    ],
    
    patterns: [
      "適切なデザインパターンが使われているか",
      "アンチパターンは避けられているか",
      "DRY原則は守られているか",
      "SOLID原則に従っているか"
    ]
  };
  
  // 可読性のチェック
  readability = {
    naming: [
      "変数名・関数名は明確か",
      "命名規則は一貫しているか",
      "ドメイン言語が使われているか",
      "略語は適切に使われているか"
    ],
    
    structure: [
      "関数は適切な大きさか",
      "ネストは深すぎないか",
      "フローは理解しやすいか",
      "複雑な部分にはコメントがあるか"
    ]
  };
  
  // パフォーマンスのチェック
  performance = {
    efficiency: [
      "アルゴリズムの計算量は適切か",
      "不要なループや処理はないか",
      "キャッシュは適切に使われているか",
      "データベースアクセスは最適化されているか"
    ],
    
    scalability: [
      "大量データでも動作するか",
      "メモリリークはないか",
      "並列処理は効率的か",
      "ボトルネックは特定されているか"
    ]
  };
  
  // セキュリティのチェック
  security = {
    vulnerabilities: [
      "SQLインジェクション対策はあるか",
      "XSS対策はあるか",
      "認証・認可は適切か",
      "機密情報は適切に扱われているか"
    ],
    
    bestPractices: [
      "入力値検証は行われているか",
      "エラーメッセージは安全か",
      "ログに機密情報は含まれていないか",
      "依存関係のセキュリティは確認されているか"
    ]
  };
}
```

### レビューコメントの書き方

```typescript
export class ReviewCommentGuide {
  // 良いコメントの例
  goodExamples = {
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
    },
    
    appreciative: {
      bad: "// 無言で承認",
      good: "このエラーハンドリングの実装、とても分かりやすくて良いですね！他の箇所でも参考にさせてもらいます。"
    }
  };
  
  // コメントのテンプレート
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
    `
  };
  
  // 重要度レベル
  severity = {
    MUST: "🚨 必須: マージ前に必ず修正が必要",
    SHOULD: "⚠️ 推奨: 修正を強く推奨",
    CONSIDER: "💭 検討: 改善の余地あり",
    NITPICK: "💡 些細: 統一性のための提案"
  };
}
```

### 自動レビューツールの活用

```typescript
export class AutomatedReviewTools {
  // 静的解析ツール
  staticAnalysis = {
    linting: {
      tool: "ESLint",
      config: {
        extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
        rules: {
          "no-console": "error",
          "no-unused-vars": "error",
          "complexity": ["error", { max: 10 }],
          "max-lines-per-function": ["error", { max: 50 }]
        }
      },
      
      customRules: [
        {
          name: "parasol-naming-convention",
          description: "Parasol V5.4の命名規約チェック",
          implementation: `
            export const parasolNamingRule: Rule.RuleModule = {
              create(context) {
                return {
                  ClassDeclaration(node) {
                    if (!node.id.name.match(/^[A-Z][a-zA-Z]*$/)) {
                      context.report({
                        node,
                        message: "Class names must be in PascalCase"
                      });
                    }
                  }
                };
              }
            };
          `
        }
      ]
    },
    
    codeQuality: {
      tool: "SonarQube",
      qualityGates: {
        coverage: 80,
        duplications: 3,
        maintainabilityRating: "A",
        reliabilityRating: "A",
        securityRating: "A"
      }
    },
    
    security: {
      tool: "Snyk",
      checks: [
        "依存関係の脆弱性",
        "コードの脆弱性",
        "Dockerfileのセキュリティ",
        "IaCのセキュリティ"
      ]
    }
  };
  
  // 自動修正ツール
  autoFixers = {
    formatting: {
      tool: "Prettier",
      config: {
        semi: true,
        trailingComma: "all",
        singleQuote: false,
        printWidth: 100,
        tabWidth: 2
      }
    },
    
    imports: {
      tool: "import-sort",
      style: "module-first",
      groups: [
        ["^\\u0000"],  // side effects
        ["^@?\\w"],    // external
        ["^"],         // internal
        ["^\\."]       // relative
      ]
    }
  };
  
  // CI/CDパイプラインでの実行
  async runInPipeline(pr: PullRequest): Promise<AutoReviewResult> {
    const results: CheckResult[] = [];
    
    // リンティング
    const lintResult = await this.runESLint(pr.files);
    results.push(lintResult);
    
    // フォーマッティングチェック
    const formatResult = await this.checkFormatting(pr.files);
    results.push(formatResult);
    
    // セキュリティスキャン
    const securityResult = await this.runSecurityScan(pr.files);
    results.push(securityResult);
    
    // カバレッジチェック
    const coverageResult = await this.checkTestCoverage(pr.files);
    results.push(coverageResult);
    
    // 複雑度チェック
    const complexityResult = await this.analyzeComplexity(pr.files);
    results.push(complexityResult);
    
    return this.aggregateResults(results);
  }
}
```

## レビュー文化の構築

### チームレビュー戦略

```typescript
export class TeamReviewStrategy {
  // レビュアーの割り当て
  assignReviewers(pr: PullRequest): Reviewer[] {
    const reviewers: Reviewer[] = [];
    
    // コードオーナー
    const codeOwners = this.findCodeOwners(pr.files);
    reviewers.push(...codeOwners);
    
    // ドメインエキスパート
    const domainExperts = this.findDomainExperts(pr.context);
    reviewers.push(...domainExperts);
    
    // ランダムレビュアー（知識の拡散）
    const randomReviewer = this.selectRandomReviewer(
      pr.author,
      [...codeOwners, ...domainExperts]
    );
    reviewers.push(randomReviewer);
    
    return this.removeDuplicates(reviewers);
  }
  
  // レビューローテーション
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
  
  // レビューメトリクス
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
}
```

### 建設的なフィードバック文化

```typescript
export class ConstructiveFeedbackCulture {
  // フィードバックの原則
  principles = {
    beSpecific: "具体的な例とともにフィードバック",
    beKind: "思いやりを持って伝える",
    beHelpful: "改善方法を提案する",
    beTimely: "適切なタイミングで行う",
    beBalanced: "良い点も悪い点も伝える"
  };
  
  // レビュー会議の運営
  conductReviewMeeting(pr: PullRequest): MeetingAgenda {
    return {
      opening: {
        duration: "5分",
        activities: [
          "PRの背景説明",
          "主な変更点の概要",
          "レビューの焦点"
        ]
      },
      
      walkthrough: {
        duration: "20分",
        approach: "作者主導",
        focus: [
          "設計判断の説明",
          "実装の難しかった点",
          "代替案の検討"
        ]
      },
      
      discussion: {
        duration: "20分",
        format: "オープンディスカッション",
        topics: [
          "アーキテクチャの適合性",
          "潜在的な問題",
          "改善提案"
        ]
      },
      
      actionItems: {
        duration: "5分",
        outputs: [
          "必須修正項目",
          "推奨改善項目",
          "将来の検討事項"
        ]
      }
    };
  }
  
  // 学習の促進
  promoteLearning(): LearningInitiatives {
    return {
      codeReadingClub: {
        frequency: "週1回",
        format: "優れたコードを皆で読む",
        benefits: ["良い設計の学習", "議論スキル向上", "共通理解構築"]
      },
      
      reviewWorkshop: {
        topics: [
          "効果的なレビューコメントの書き方",
          "レビューツールの活用法",
          "建設的なフィードバックの与え方"
        ]
      },
      
      mentorshipProgram: {
        pairing: "経験者と初心者のペア",
        activities: [
          "ペアレビュー",
          "レビューの振り返り",
          "ベストプラクティスの共有"
        ]
      },
      
      knowledgeBase: {
        contents: [
          "レビューでよく指摘される問題",
          "設計パターンの例",
          "パフォーマンス改善のヒント",
          "セキュリティチェックリスト"
        ]
      }
    };
  }
}
```

### Pull Requestの最適化

```typescript
export class PullRequestOptimization {
  // PRサイズの管理
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
  
  // PRの構造化
  structurePR(): PullRequestTemplate {
    return {
      title: {
        format: "[タイプ] 簡潔な説明",
        examples: [
          "[feat] ユーザー認証機能の追加",
          "[fix] ログイン時のセッションエラー修正",
          "[refactor] 注文処理の最適化"
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
          }
        ]
      },
      
      metadata: {
        labels: ["レビュー待ち", "バグ修正", "機能追加"],
        assignees: ["@reviewer1", "@reviewer2"],
        milestone: "v1.0.0",
        relatedIssues: ["#123", "#456"]
      }
    };
  }
  
  // レビューの効率化
  async automatePreparation(pr: PullRequest): Promise<void> {
    // 自動的にコンテキストを準備
    const context = await this.gatherContext(pr);
    
    // 関連するドキュメントをリンク
    const docs = await this.findRelatedDocumentation(pr);
    
    // 影響分析を実行
    const impact = await this.analyzeImpact(pr);
    
    // レビュー用サマリーを生成
    const summary = this.generateReviewSummary({
      context,
      docs,
      impact,
      changes: pr.changes
    });
    
    // PRにコメントとして追加
    await this.postComment(pr, summary);
  }
}
```

## 高度なレビューテクニック

### アーキテクチャレビュー

```typescript
export class ArchitectureReview {
  // 設計原則のチェック
  checkDesignPrinciples(code: SourceCode): DesignViolations {
    const violations: Violation[] = [];
    
    // SOLID原則
    const solidViolations = this.checkSOLID(code);
    violations.push(...solidViolations);
    
    // DDD原則
    const dddViolations = this.checkDDD(code);
    violations.push(...dddViolations);
    
    // Parasol V5.4固有の原則
    const parasolViolations = this.checkParasolPrinciples(code);
    violations.push(...parasolViolations);
    
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
    
    // Open/Closed Principle
    const modifications = this.detectModifications(code);
    for (const mod of modifications) {
      if (mod.type === "existing-class-modification") {
        violations.push({
          principle: "OCP",
          location: mod.location,
          message: "既存クラスの修正より拡張を検討してください",
          severity: "info"
        });
      }
    }
    
    // その他の原則チェック...
    
    return violations;
  }
  
  // パフォーマンスレビュー
  async performanceReview(code: SourceCode): Promise<PerformanceAnalysis> {
    const analysis: PerformanceAnalysis = {
      algorithms: [],
      database: [],
      memory: [],
      concurrency: []
    };
    
    // アルゴリズム分析
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
    
    // データベースアクセス分析
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

### セキュリティレビュー

```typescript
export class SecurityReview {
  // 脆弱性の検出
  async detectVulnerabilities(code: SourceCode): Promise<SecurityIssue[]> {
    const issues: SecurityIssue[] = [];
    
    // OWASP Top 10のチェック
    issues.push(...await this.checkOWASPTop10(code));
    
    // 機密情報の露出
    issues.push(...this.checkSensitiveDataExposure(code));
    
    // 認証・認可の問題
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
    
    // A2: Broken Authentication
    const authCode = code.findPattern(/password|auth|login/g);
    for (const auth of authCode) {
      if (this.hasWeakAuthentication(auth)) {
        issues.push({
          type: "Weak Authentication",
          severity: "high",
          location: auth.location,
          description: "弱い認証メカニズム",
          fix: "強力な認証方式を実装してください"
        });
      }
    }
    
    return issues;
  }
  
  // セキュアコーディングのチェック
  checkSecureCoding(code: SourceCode): SecureCodingReport {
    return {
      inputValidation: this.checkInputValidation(code),
      outputEncoding: this.checkOutputEncoding(code),
      cryptography: this.checkCryptography(code),
      sessionManagement: this.checkSessionManagement(code),
      errorHandling: this.checkSecureErrorHandling(code),
      logging: this.checkSecureLogging(code)
    };
  }
}
```

## レビューツールとプラクティス

### コードレビューツールの統合

```typescript
export class ReviewToolIntegration {
  // GitHub/GitLab統合
  integrateWithVCS(): VCSIntegration {
    return {
      github: {
        prTemplate: ".github/pull_request_template.md",
        
        requiredChecks: [
          "continuous-integration/travis-ci",
          "security/snyk",
          "coverage/coveralls"
        ],
        
        branchProtection: {
          requireReviews: true,
          dismissStaleReviews: true,
          requiredReviewers: 2,
          includeAdmins: true
        },
        
        automation: {
          autoAssignReviewers: true,
          autoLabel: true,
          autoMerge: {
            enabled: true,
            conditions: ["all-checks-passed", "approved", "no-conflicts"]
          }
        }
      },
      
      customIntegrations: [
        {
          name: "Parasol Review Bot",
          triggers: ["pr_opened", "pr_updated"],
          actions: [
            "アーキテクチャチェック",
            "パフォーマンス分析",
            "セキュリティスキャン",
            "ドキュメント生成"
          ]
        }
      ]
    };
  }
  
  // レビューダッシュボード
  createDashboard(): ReviewDashboard {
    return {
      metrics: {
        pending: this.getPendingReviews(),
        averageTime: this.getAverageReviewTime(),
        throughput: this.getReviewThroughput(),
        quality: this.getQualityMetrics()
      },
      
      insights: {
        bottlenecks: this.identifyBottlenecks(),
        trends: this.analyzeTrends(),
        recommendations: this.generateRecommendations()
      },
      
      visualizations: [
        {
          type: "heatmap",
          data: "レビュー活動の時間分布",
          purpose: "最適なレビュー時間の特定"
        },
        {
          type: "flow",
          data: "PRのライフサイクル",
          purpose: "プロセスの最適化ポイント発見"
        },
        {
          type: "network",
          data: "レビュアーの相互作用",
          purpose: "知識の流れの可視化"
        }
      ]
    };
  }
}
```

## まとめ

効果的なコードレビューは、単なる品質保証の仕組みではありません。チームの集合知を活用し、継続的な学習と改善を促進する重要なプラクティスです。Parasol V5.4における成功の鍵：

1. **目的の明確化** - バグ発見だけでなく知識共有を重視
2. **プロセスの体系化** - 段階的で包括的なレビュープロセス
3. **建設的な文化** - 思いやりと成長を促すフィードバック
4. **ツールの活用** - 機械的なチェックは自動化
5. **継続的な改善** - メトリクスに基づくプロセス改善

優れたレビュー文化は、チーム全体の技術力向上と製品品質の向上をもたらします。

### 次章への架橋

コードレビューを通じて高品質なコードベースを維持する方法を学びました。第25章では、継続的インテグレーション/デリバリー（CI/CD）を通じて、品質を保ちながら迅速にソフトウェアをリリースする仕組みについて解説します。

---

## 演習問題

1. あなたのチームのコードレビュープロセスを分析し、改善点を3つ挙げてください。それぞれに対する具体的な改善策を提案してください。

2. 以下のコードに対してレビューコメントを書いてください。建設的で具体的なフィードバックを心がけてください。
   ```typescript
   function processOrder(order) {
     const total = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
     if (total > 10000) {
       // 高額注文の処理
       console.log("High value order: " + order.id);
       sendEmail(order.customer.email, "Your order is being processed");
     }
     updateDatabase("UPDATE orders SET status = 'processed' WHERE id = " + order.id);
     return true;
   }
   ```

3. 自動レビューツールの設定ファイルを作成し、あなたのプロジェクトに適したルールセットを定義してください。