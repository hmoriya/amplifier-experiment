# 第34章　トラブルシューティング ― 問題解決の技法

## はじめに：探偵の推理

名探偵が事件を解決するとき、手がかりを集め、仮説を立て、証拠を検証し、真実に辿り着きます。システムのトラブルシューティングも同じプロセスです。症状から原因を推測し、データを収集し、仮説を検証し、問題の根本原因を突き止めます。

本章では、Parasol V5.4環境における効果的なトラブルシューティング技法を解説します。

## トラブルシューティングの基本原則

### 体系的アプローチ

```typescript
export interface TroubleshootingFramework {
  principles: {
    systematic: "体系的な問題解決アプローチ";
    datadriven: "データに基づく判断";
    reproducible: "問題の再現性確保";
    documented: "調査過程の文書化";
    collaborative: "チームでの協調作業";
  };
  
  process: {
    identify: "問題の特定と定義";
    gather: "情報収集と証拠集め";
    analyze: "データ分析と仮説立案";
    test: "仮説の検証";
    resolve: "解決策の実装";
    verify: "解決の確認";
    document: "教訓の文書化";
  };
  
  tools: {
    monitoring: "監視ツール";
    logging: "ログ分析ツール";
    debugging: "デバッグツール";
    profiling: "プロファイリングツール";
    tracing: "分散トレーシング";
  };
}

export class TroubleshootingMethodology {
  // 問題の分類と優先順位付け
  classifyProblem(incident: Incident): ProblemClassification {
    const classification = {
      severity: this.assessSeverity(incident),
      impact: this.assessImpact(incident),
      urgency: this.assessUrgency(incident),
      category: this.categorize(incident)
    };
    
    return {
      ...classification,
      priority: this.calculatePriority(classification),
      assignee: this.assignResponsible(classification),
      sla: this.determineSLA(classification)
    };
  }
  
  private assessSeverity(incident: Incident): Severity {
    if (incident.affectsProduction && incident.noWorkaround) {
      return 'critical';
    }
    if (incident.affectsMultipleUsers) {
      return 'high';
    }
    if (incident.hasWorkaround) {
      return 'medium';
    }
    return 'low';
  }
  
  // 5 Whys分析
  conductRootCauseAnalysis(problem: Problem): RootCauseAnalysis {
    const whys: Why[] = [];
    let currentWhy = problem.symptom;
    
    for (let i = 0; i < 5; i++) {
      const answer = this.askWhy(currentWhy);
      whys.push({
        question: `Why ${currentWhy}?`,
        answer: answer,
        evidence: this.gatherEvidence(answer)
      });
      
      if (this.isRootCause(answer)) {
        break;
      }
      
      currentWhy = answer;
    }
    
    return {
      whys,
      rootCause: whys[whys.length - 1].answer,
      actionItems: this.deriveActionItems(whys)
    };
  }
}
```

### 情報収集テクニック

```typescript
export class InformationGathering {
  // ログ収集と分析
  async gatherLogs(timeRange: TimeRange): Promise<LogAnalysis> {
    const sources = [
      { type: 'application', path: '/var/log/app/*.log' },
      { type: 'system', path: '/var/log/syslog' },
      { type: 'container', command: 'docker logs' },
      { type: 'kubernetes', command: 'kubectl logs' }
    ];
    
    const logs: LogEntry[] = [];
    
    for (const source of sources) {
      const entries = await this.collectFromSource(source, timeRange);
      logs.push(...entries);
    }
    
    // ログの相関分析
    const correlated = this.correlateLogs(logs);
    
    // 異常パターンの検出
    const anomalies = this.detectAnomalies(correlated);
    
    // エラーの集約
    const errors = this.aggregateErrors(correlated);
    
    return {
      totalEntries: logs.length,
      timeRange,
      anomalies,
      errors,
      timeline: this.createTimeline(correlated),
      recommendations: this.generateRecommendations(anomalies, errors)
    };
  }
  
  // メトリクス収集
  async collectMetrics(
    incident: Incident
  ): Promise<MetricsSnapshot> {
    const timeWindow = this.determineTimeWindow(incident);
    
    const metrics = {
      system: await this.collectSystemMetrics(timeWindow),
      application: await this.collectApplicationMetrics(timeWindow),
      database: await this.collectDatabaseMetrics(timeWindow),
      network: await this.collectNetworkMetrics(timeWindow)
    };
    
    // ベースラインとの比較
    const baseline = await this.getBaseline(timeWindow);
    const deviations = this.compareWithBaseline(metrics, baseline);
    
    return {
      metrics,
      baseline,
      deviations,
      correlations: this.findCorrelations(metrics),
      insights: this.generateInsights(deviations)
    };
  }
  
  // 分散トレーシング
  async traceRequest(requestId: string): Promise<TraceAnalysis> {
    const trace = await this.distributedTracing.getTrace(requestId);
    
    if (!trace) {
      throw new Error(`Trace not found for request ${requestId}`);
    }
    
    const analysis = {
      totalDuration: trace.duration,
      spanCount: trace.spans.length,
      services: this.extractServices(trace),
      criticalPath: this.findCriticalPath(trace),
      bottlenecks: this.identifyBottlenecks(trace),
      errors: this.extractErrors(trace)
    };
    
    // ウォーターフォール図の生成
    analysis.waterfall = this.generateWaterfall(trace);
    
    // サービス依存関係の分析
    analysis.dependencies = this.analyzeDependencies(trace);
    
    return analysis;
  }
}
```

## 一般的な問題パターン

### パフォーマンス問題

```typescript
export class PerformanceIssues {
  // 遅延の診断
  async diagnoseLatency(
    symptoms: LatencySymptoms
  ): Promise<LatencyDiagnosis> {
    const checks = [
      this.checkDatabaseQueries(),
      this.checkNetworkLatency(),
      this.checkCPUUsage(),
      this.checkMemoryUsage(),
      this.checkDiskIO(),
      this.checkGarbageCollection(),
      this.checkConcurrency()
    ];
    
    const results = await Promise.all(checks);
    
    const issues = results
      .filter(r => r.hasIssue)
      .sort((a, b) => b.impact - a.impact);
    
    return {
      primaryCause: issues[0],
      contributingFactors: issues.slice(1),
      recommendations: this.generateOptimizations(issues),
      estimatedImprovement: this.estimateImprovement(issues)
    };
  }
  
  // メモリリークの検出
  async detectMemoryLeak(): Promise<MemoryLeakAnalysis> {
    // ヒープダンプの取得
    const dumps = await this.collectHeapDumps({
      count: 3,
      interval: 300000 // 5分間隔
    });
    
    // ヒープの成長分析
    const growth = this.analyzeHeapGrowth(dumps);
    
    // 保持されているオブジェクトの分析
    const retainers = this.analyzeRetainers(dumps[dumps.length - 1]);
    
    // 疑わしいパターンの検出
    const suspiciousPatterns = [
      this.checkGrowingCollections(dumps),
      this.checkEventListenerLeaks(dumps),
      this.checkCircularReferences(dumps),
      this.checkClosureLeaks(dumps)
    ];
    
    return {
      isLeaking: growth.rate > 0.1, // 10%以上の成長率
      growthRate: growth.rate,
      suspectedCauses: suspiciousPatterns.filter(p => p.likelihood > 0.7),
      largestRetainers: retainers.slice(0, 10),
      recommendations: this.generateMemoryOptimizations(suspiciousPatterns)
    };
  }
}
```

### 接続性問題

```typescript
export class ConnectivityIssues {
  // ネットワーク診断
  async diagnoseNetworkIssue(
    target: NetworkTarget
  ): Promise<NetworkDiagnosis> {
    const diagnostics = {
      // 基本的な接続性テスト
      ping: await this.pingTest(target),
      
      // ルーティング分析
      traceroute: await this.traceroute(target),
      
      // DNS解決
      dns: await this.dnsLookup(target),
      
      // ポート接続性
      portCheck: await this.checkPort(target),
      
      // SSL/TLS検証
      ssl: await this.validateSSL(target),
      
      // 帯域幅テスト
      bandwidth: await this.measureBandwidth(target),
      
      // パケットロス分析
      packetLoss: await this.analyzePacketLoss(target)
    };
    
    // 問題の特定
    const issues = this.identifyNetworkIssues(diagnostics);
    
    return {
      diagnostics,
      issues,
      rootCause: this.determineNetworkRootCause(issues),
      resolution: this.suggestNetworkFixes(issues)
    };
  }
  
  // データベース接続問題
  async diagnoseDatabaseConnection(
    config: DatabaseConfig
  ): Promise<DbConnectionDiagnosis> {
    const checks = {
      // 接続プール状態
      poolStatus: await this.checkConnectionPool(),
      
      // アクティブな接続
      activeConnections: await this.getActiveConnections(),
      
      // ブロックされたクエリ
      blockedQueries: await this.findBlockedQueries(),
      
      // デッドロック検出
      deadlocks: await this.detectDeadlocks(),
      
      // 接続リーク
      leaks: await this.detectConnectionLeaks(),
      
      // 設定検証
      configuration: this.validateDbConfig(config)
    };
    
    return {
      checks,
      issues: this.analyzeDbConnectionIssues(checks),
      recommendations: this.generateDbRecommendations(checks)
    };
  }
}
```

## 高度なデバッグテクニック

### 分散システムのデバッグ

```typescript
export class DistributedDebugging {
  // 分散トランザクションの追跡
  async traceDistributedTransaction(
    transactionId: string
  ): Promise<DistributedTrace> {
    // 全サービスからログを収集
    const services = await this.discoverInvolvedServices(transactionId);
    const logs = await this.collectLogsFromServices(services, transactionId);
    
    // タイムライン構築
    const timeline = this.buildDistributedTimeline(logs);
    
    // サービス間の依存関係分析
    const dependencies = this.analyzeDependencies(timeline);
    
    // クリティカルパスの特定
    const criticalPath = this.findCriticalPath(timeline, dependencies);
    
    // エラーの伝播分析
    const errorPropagation = this.traceErrorPropagation(timeline);
    
    return {
      services: services.length,
      totalDuration: timeline.duration,
      criticalPath,
      bottlenecks: this.identifyBottlenecks(criticalPath),
      errors: errorPropagation,
      visualization: this.generateTraceVisualization(timeline)
    };
  }
  
  // カオスエンジニアリング
  async performChaosExperiment(
    hypothesis: ChaosHypothesis
  ): Promise<ChaosResult> {
    // 実験前のベースライン測定
    const baseline = await this.measureBaseline();
    
    // 障害注入
    const injection = await this.injectFailure(hypothesis.failure);
    
    try {
      // システムの振る舞い観察
      const observations = await this.observeSystem({
        duration: hypothesis.duration,
        metrics: hypothesis.metrics
      });
      
      // 仮説の検証
      const validation = this.validateHypothesis(
        hypothesis,
        observations
      );
      
      return {
        hypothesis,
        baseline,
        observations,
        validation,
        learnings: this.extractLearnings(observations),
        improvements: this.suggestImprovements(validation)
      };
    } finally {
      // 障害の除去
      await this.removeFailure(injection);
      
      // システムの回復確認
      await this.verifyRecovery(baseline);
    }
  }
}
```

### プロダクションデバッグ

```typescript
export class ProductionDebugging {
  // 安全なプロダクションデバッグ
  async debugInProduction(
    issue: ProductionIssue
  ): Promise<DebugSession> {
    // カナリアユーザーの選択
    const canaryUsers = await this.selectCanaryUsers({
      percentage: 0.1,
      criteria: issue.affectedUserCriteria
    });
    
    // デバッグフラグの有効化
    await this.enableDebugFlags({
      users: canaryUsers,
      flags: ['verbose_logging', 'trace_enabled'],
      duration: 3600 // 1時間
    });
    
    // 詳細ログの収集
    const debugLogs = await this.collectDebugLogs(canaryUsers);
    
    // 動的計装
    const instrumentation = await this.addInstrumentation({
      methods: issue.suspectedMethods,
      metrics: ['execution_time', 'memory_usage', 'error_rate']
    });
    
    // データ収集と分析
    const analysis = await this.analyzeDebugData({
      logs: debugLogs,
      metrics: instrumentation.metrics
    });
    
    // クリーンアップ
    await this.cleanup({
      disableFlags: true,
      removeInstrumentation: true,
      archiveLogs: true
    });
    
    return {
      findings: analysis.findings,
      rootCause: analysis.rootCause,
      evidence: analysis.evidence,
      recommendations: analysis.recommendations
    };
  }
  
  // A/Bテストによる問題検証
  async verifyFixWithABTest(
    fix: ProposedFix
  ): Promise<ABTestResult> {
    // テストグループの設定
    const groups = {
      control: await this.createControlGroup(0.5),
      treatment: await this.createTreatmentGroup(0.5)
    };
    
    // 修正の適用
    await this.applyFix(groups.treatment, fix);
    
    // メトリクス収集
    const metrics = await this.collectABMetrics({
      groups,
      duration: fix.testDuration,
      indicators: fix.successIndicators
    });
    
    // 統計的有意性の検証
    const significance = this.calculateStatisticalSignificance(metrics);
    
    // 結果の分析
    return {
      improved: significance.pValue < 0.05 && metrics.treatment > metrics.control,
      metrics: {
        control: metrics.control,
        treatment: metrics.treatment,
        improvement: ((metrics.treatment - metrics.control) / metrics.control) * 100
      },
      significance,
      recommendation: this.makeRecommendation(significance, metrics)
    };
  }
}
```

## インシデント対応

### インシデント管理プロセス

```typescript
export class IncidentManagement {
  // インシデント対応フロー
  async handleIncident(alert: Alert): Promise<IncidentResolution> {
    // インシデントの作成
    const incident = await this.createIncident(alert);
    
    // 対応チームの招集
    const team = await this.assembleResponseTeam(incident);
    
    // 初期評価
    const assessment = await this.performInitialAssessment(incident);
    
    // コミュニケーションチャネルの確立
    const channels = await this.setupCommunication({
      internal: ['slack', 'zoom'],
      external: ['status-page', 'twitter']
    });
    
    // 問題の封じ込め
    const containment = await this.containIssue(incident, assessment);
    
    // 根本原因の調査
    const investigation = await this.investigateRootCause(incident);
    
    // 修正の実装
    const fix = await this.implementFix(investigation.rootCause);
    
    // 復旧の確認
    const recovery = await this.verifyRecovery(incident);
    
    // 事後分析
    const postmortem = await this.conductPostmortem(incident);
    
    return {
      incident,
      duration: this.calculateDuration(incident),
      impact: this.assessImpact(incident),
      resolution: fix,
      postmortem,
      actionItems: postmortem.actionItems
    };
  }
  
  // ランブック実行
  async executeRunbook(
    runbook: Runbook,
    incident: Incident
  ): Promise<RunbookExecution> {
    const execution = {
      runbook: runbook.id,
      incident: incident.id,
      steps: [],
      startTime: new Date()
    };
    
    for (const step of runbook.steps) {
      try {
        // ステップの実行
        const result = await this.executeStep(step, incident);
        
        execution.steps.push({
          step: step.id,
          status: 'completed',
          result,
          duration: result.duration
        });
        
        // 成功条件の確認
        if (!this.checkStepSuccess(step, result)) {
          throw new Error(`Step ${step.id} failed`);
        }
      } catch (error) {
        // エラーハンドリング
        execution.steps.push({
          step: step.id,
          status: 'failed',
          error: error.message
        });
        
        // フォールバック処理
        if (step.fallback) {
          await this.executeFallback(step.fallback, incident);
        }
        
        break;
      }
    }
    
    execution.endTime = new Date();
    execution.status = this.determineExecutionStatus(execution);
    
    return execution;
  }
}
```

## 予防的対策

### 問題の予測と防止

```typescript
export class ProactiveTroubleshooting {
  // 異常検知システム
  implementAnomalyDetection(): AnomalyDetectionSystem {
    return {
      // 機械学習モデル
      models: {
        timeseries: {
          algorithm: 'LSTM',
          features: ['cpu', 'memory', 'latency', 'error_rate'],
          training: 'continuous',
          threshold: 0.95
        },
        
        clustering: {
          algorithm: 'DBSCAN',
          features: ['request_pattern', 'user_behavior'],
          updateFrequency: 'hourly'
        },
        
        classification: {
          algorithm: 'RandomForest',
          features: ['log_patterns', 'metric_combinations'],
          labels: ['normal', 'degraded', 'critical']
        }
      },
      
      // アラート生成
      alerting: `
        class AnomalyAlerter {
          async processAnomaly(anomaly: Anomaly): Promise<void> {
            const severity = this.calculateSeverity(anomaly);
            const impact = await this.predictImpact(anomaly);
            
            if (severity === 'critical' || impact.users > 1000) {
              await this.createIncident({
                title: \`Anomaly detected: \${anomaly.type}\`,
                severity,
                impact,
                predictedDuration: impact.duration,
                recommendedActions: this.getRecommendedActions(anomaly)
              });
            } else {
              await this.notifyOncall({
                anomaly,
                severity,
                impact
              });
            }
          }
        }
      `,
      
      // 自動修復
      autoRemediation: `
        class AutoRemediator {
          async attemptRemediation(
            anomaly: Anomaly
          ): Promise<RemediationResult> {
            const actions = this.selectRemediationActions(anomaly);
            const results = [];
            
            for (const action of actions) {
              if (this.isSafeToExecute(action)) {
                const result = await this.executeAction(action);
                results.push(result);
                
                // 効果の検証
                const improved = await this.verifyImprovement(anomaly);
                if (improved) {
                  break;
                }
              }
            }
            
            return {
              anomaly,
              actions: results,
              success: results.some(r => r.success),
              metrics: await this.collectMetrics()
            };
          }
        }
      `
    };
  }
  
  // 健全性チェック
  async performHealthCheck(): Promise<HealthCheckResult> {
    const checks = [
      { name: 'API Endpoints', check: () => this.checkAPIEndpoints() },
      { name: 'Database Connections', check: () => this.checkDatabaseConnections() },
      { name: 'Cache Systems', check: () => this.checkCacheSystems() },
      { name: 'Message Queues', check: () => this.checkMessageQueues() },
      { name: 'External Dependencies', check: () => this.checkExternalDependencies() },
      { name: 'Disk Space', check: () => this.checkDiskSpace() },
      { name: 'Certificate Expiry', check: () => this.checkCertificates() }
    ];
    
    const results = await Promise.all(
      checks.map(async (check) => {
        try {
          const result = await check.check();
          return {
            name: check.name,
            status: result.healthy ? 'healthy' : 'unhealthy',
            details: result.details,
            metrics: result.metrics
          };
        } catch (error) {
          return {
            name: check.name,
            status: 'error',
            error: error.message
          };
        }
      })
    );
    
    return {
      overall: results.every(r => r.status === 'healthy') ? 'healthy' : 'unhealthy',
      checks: results,
      timestamp: new Date()
    };
  }
}
```

## まとめ

効果的なトラブルシューティングは、システムの安定性と信頼性を維持する鍵です。Parasol V5.4における成功の要因：

1. **体系的アプローチ** - 推測ではなくデータに基づく問題解決
2. **包括的な情報収集** - ログ、メトリクス、トレースの統合分析
3. **根本原因の追求** - 症状ではなく原因の解決
4. **予防的対策** - 問題の早期発見と自動修復
5. **知識の共有** - インシデントからの学習と改善

名探偵のように、観察力、分析力、そして経験を組み合わせることで、どんな複雑な問題も解決できます。

### 次章への架橋

トラブルシューティングの技法を習得しました。第35章では、これらの技術を総動員して、システム全体のベストプラクティスを探求します。

---

## 演習問題

1. 過去に遭遇した本番障害を選び、5 Whys分析を適用して根本原因を特定してください。また、再発防止策を提案してください。

2. 分散システムにおける遅延問題をトラブルシューティングするための調査計画を作成してください。必要なツール、収集すべきデータ、分析手法を含めてください。

3. インシデント対応のランブックを作成してください。具体的なシナリオ（例：データベース接続エラー）を選び、ステップバイステップの対応手順を記述してください。