# 付録：第34章　トラブルシューティングの実装詳細

## トラブルシューティングフレームワーク

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
```

## 問題分類と優先順位付け

```typescript
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

## 情報収集ツール

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

## パフォーマンス問題の診断

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

## 接続性問題の診断

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

## 分散システムのデバッグ

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

## プロダクションデバッグ

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
}
```

## インシデント対応テンプレート

<div id="templates"></div>

### インシデントレポートテンプレート

```yaml
# インシデントレポートテンプレート
incident:
  id: INC-YYYY-MMDD-NNN
  title: <簡潔なタイトル>
  severity: critical | high | medium | low
  status: active | resolved | postmortem
  
timeline:
  - time: HH:MM
    event: <何が起きたか>
    actor: <誰が対応したか>
    
impact:
  users_affected: <影響を受けたユーザー数>
  duration: <影響時間>
  services: [<影響を受けたサービス>]
  
root_cause:
  summary: <根本原因の要約>
  details: <詳細な説明>
  
resolution:
  immediate: <応急処置>
  permanent: <恒久対策>
  
lessons_learned:
  what_went_well:
    - <うまくいったこと>
  what_went_wrong:
    - <問題だったこと>
  action_items:
    - owner: <担当者>
      action: <実施内容>
      due_date: YYYY-MM-DD
```

### ランブック例

```typescript
export const DatabaseConnectionErrorRunbook = {
  title: "データベース接続エラー対応",
  
  symptoms: [
    "API 500エラー増加",
    "Connection pool exhausted エラー",
    "Database timeout エラー"
  ],
  
  steps: [
    {
      id: "assess",
      title: "状況評価",
      actions: [
        "ダッシュボードで影響範囲確認",
        "現在の接続数を確認: SELECT count(*) FROM pg_stat_activity;",
        "最新のデプロイを確認"
      ],
      timeLimit: "5分"
    },
    {
      id: "mitigate",
      title: "影響緩和",
      actions: [
        "接続プールサイズを一時的に増加",
        "Read Replicaへの振り分け比率を上げる",
        "キャッシュTTLを延長"
      ],
      timeLimit: "10分"
    },
    {
      id: "investigate",
      title: "原因調査",
      actions: [
        "スロークエリの確認",
        "長時間実行中のトランザクション確認",
        "デッドロックの確認"
      ]
    },
    {
      id: "resolve",
      title: "問題解決",
      actions: [
        "問題のあるクエリをキル",
        "必要に応じてアプリケーション再起動",
        "接続プール設定を元に戻す"
      ]
    }
  ],
  
  escalation: {
    after_minutes: 30,
    contact: ["DBAチーム", "インフラチーム"]
  }
};
```

## 異常検知システムの実装

<div id="anomaly"></div>

```typescript
class AnomalyDetectionSystem {
  private models: Map<string, AnomalyModel> = new Map();
  
  async detectAnomalies(
    metrics: MetricData[]
  ): Promise<Anomaly[]> {
    const anomalies: Anomaly[] = [];
    
    for (const metric of metrics) {
      const model = this.getOrCreateModel(metric.name);
      const prediction = await model.predict(metric.value);
      
      if (prediction.isAnomaly) {
        anomalies.push({
          metric: metric.name,
          value: metric.value,
          expected: prediction.expected,
          deviation: prediction.deviation,
          confidence: prediction.confidence,
          timestamp: metric.timestamp
        });
      }
    }
    
    return anomalies;
  }
  
  private getOrCreateModel(metricName: string): AnomalyModel {
    if (!this.models.has(metricName)) {
      this.models.set(metricName, new AnomalyModel({
        algorithm: 'isolation-forest',
        windowSize: 1440, // 24時間
        updateFrequency: 300 // 5分
      }));
    }
    
    return this.models.get(metricName)!;
  }
}

// 自動修復システム
class AutoRemediationSystem {
  private remediations = new Map<string, RemediationAction>();
  
  constructor() {
    this.registerRemediations();
  }
  
  private registerRemediations() {
    this.remediations.set('high_memory_usage', {
      condition: (anomaly) => 
        anomaly.metric === 'memory_usage' && 
        anomaly.value > 0.9,
      actions: [
        () => this.restartWorkers(),
        () => this.triggerGarbageCollection(),
        () => this.scaleOut()
      ]
    });
    
    this.remediations.set('high_error_rate', {
      condition: (anomaly) => 
        anomaly.metric === 'error_rate' && 
        anomaly.value > 0.05,
      actions: [
        () => this.enableCircuitBreaker(),
        () => this.increaseTimeout(),
        () => this.rollbackDeployment()
      ]
    });
  }
  
  async remediate(anomaly: Anomaly): Promise<RemediationResult> {
    const remediation = this.findRemediation(anomaly);
    
    if (!remediation) {
      return { success: false, reason: 'No remediation found' };
    }
    
    for (const action of remediation.actions) {
      try {
        await action();
        
        // 効果を確認
        const improved = await this.verifyImprovement(anomaly);
        if (improved) {
          return {
            success: true,
            action: action.name,
            improvement: improved
          };
        }
      } catch (error) {
        console.error('Remediation failed:', error);
      }
    }
    
    return { success: false, reason: 'All remediations failed' };
  }
}
```