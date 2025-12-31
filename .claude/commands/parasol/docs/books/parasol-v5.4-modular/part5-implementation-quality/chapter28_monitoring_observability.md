# 第28章　監視とロギング ― システムの見える化

## はじめに：システムの体温計と聴診器

医師が患者の健康状態を診断する際、体温計で熱を測り、聴診器で心音を聞き、血圧計で循環状態を確認します。同様に、システムの健康状態を把握するには、適切な監視ツールとロギング機構が不可欠です。これらは問題の早期発見、迅速な診断、そして効果的な治療（修正）を可能にします。

本章では、Parasol V5.4における包括的な監視とロギングの実装について、オブザーバビリティの観点から解説します。

## オブザーバビリティの3つの柱

### メトリクス、ログ、トレース

```typescript
export interface ObservabilityPillars {
  metrics: {
    definition: "システムの状態を数値で表現";
    types: ["カウンター", "ゲージ", "ヒストグラム", "サマリー"];
    examples: ["CPU使用率", "メモリ使用量", "リクエスト数", "レスポンスタイム"];
    purpose: "トレンド分析、アラート、容量計画";
  };
  
  logs: {
    definition: "システムで発生したイベントの記録";
    levels: ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"];
    structured: true;
    purpose: "デバッグ、監査、フォレンジック分析";
  };
  
  traces: {
    definition: "リクエストの実行パスと時間の記録";
    components: ["スパン", "コンテキスト", "タグ", "ログ"];
    purpose: "パフォーマンス分析、ボトルネック特定、依存関係理解";
  };
}

export class ObservabilityFramework {
  // 統合オブザーバビリティ基盤
  initializeObservability(): ObservabilityStack {
    return {
      // メトリクス収集
      metrics: {
        collector: new PrometheusCollector({
          port: 9090,
          scrapeInterval: "15s",
          retention: "15d"
        }),
        
        exporters: [
          new DatadogExporter({ apiKey: process.env.DATADOG_API_KEY }),
          new CloudWatchExporter({ region: "ap-northeast-1" }),
          new GrafanaCloudExporter({ endpoint: process.env.GRAFANA_ENDPOINT })
        ]
      },
      
      // ログ収集
      logging: {
        aggregator: new FluentBit({
          inputs: [
            { type: "tail", path: "/var/log/app/*.log" },
            { type: "systemd", unit: "app.service" },
            { type: "docker", containers: ["app-*"] }
          ],
          
          filters: [
            { type: "parser", format: "json" },
            { type: "enrichment", add: { env: process.env.NODE_ENV } }
          ],
          
          outputs: [
            { type: "elasticsearch", host: "es.example.com" },
            { type: "s3", bucket: "logs-archive" }
          ]
        })
      },
      
      // 分散トレーシング
      tracing: {
        tracer: new JaegerTracer({
          serviceName: "parasol-api",
          sampler: {
            type: "adaptive",
            maxTracesPerSecond: 100
          },
          
          reporter: {
            endpoint: "http://jaeger-collector:14268/api/traces",
            batchSize: 100,
            flushInterval: 1000
          }
        })
      },
      
      // 相関分析
      correlation: {
        engine: new CorrelationEngine({
          sources: ["metrics", "logs", "traces"],
          rules: [
            {
              name: "Error Spike Detection",
              condition: "error_rate > 5% AND response_time > 1s",
              correlation: ["logs.level=ERROR", "traces.error=true"],
              action: "alert"
            }
          ]
        })
      }
    };
  }
}
```

### 構造化ロギング

```typescript
export class StructuredLogging {
  // ロガーの設定
  createLogger(): Logger {
    return winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      
      defaultMeta: {
        service: 'parasol-api',
        environment: process.env.NODE_ENV,
        version: process.env.APP_VERSION,
        instance: process.env.INSTANCE_ID
      },
      
      transports: [
        // コンソール出力（開発環境）
        new winston.transports.Console({
          format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
          )
        }),
        
        // ファイル出力（本番環境）
        new winston.transports.DailyRotateFile({
          filename: 'logs/app-%DATE%.log',
          datePattern: 'YYYY-MM-DD',
          maxSize: '100m',
          maxFiles: '30d',
          zippedArchive: true
        })
      ],
      
      // エラーハンドリング
      exceptionHandlers: [
        new winston.transports.File({ filename: 'logs/exceptions.log' })
      ],
      
      rejectionHandlers: [
        new winston.transports.File({ filename: 'logs/rejections.log' })
      ]
    });
  }
  
  // コンテキスト付きロギング
  implementContextualLogging(): ContextualLogger {
    return {
      // リクエストコンテキスト
      middleware: (req: Request, res: Response, next: NextFunction) => {
        const requestId = uuid();
        const startTime = Date.now();
        
        // AsyncLocalStorageでコンテキスト管理
        AsyncLocalStorage.run({ requestId, userId: req.user?.id }, () => {
          // リクエストログ
          logger.info('Request received', {
            requestId,
            method: req.method,
            path: req.path,
            query: req.query,
            headers: this.sanitizeHeaders(req.headers),
            ip: req.ip
          });
          
          // レスポンスログ
          const originalSend = res.send;
          res.send = function(data) {
            const duration = Date.now() - startTime;
            
            logger.info('Response sent', {
              requestId,
              statusCode: res.statusCode,
              duration,
              size: Buffer.byteLength(data)
            });
            
            // メトリクスの記録
            metrics.recordResponseTime(req.path, res.statusCode, duration);
            
            return originalSend.call(this, data);
          };
          
          next();
        });
      },
      
      // 構造化エラーログ
      errorLogger: (error: Error, context?: any) => {
        const errorInfo = {
          message: error.message,
          stack: error.stack,
          type: error.constructor.name,
          ...context
        };
        
        if (error instanceof ValidationError) {
          logger.warn('Validation error', errorInfo);
        } else if (error instanceof BusinessError) {
          logger.error('Business error', errorInfo);
        } else {
          logger.error('Unexpected error', errorInfo);
        }
        
        // Sentryへの送信
        Sentry.captureException(error, {
          tags: { requestId: AsyncLocalStorage.getStore()?.requestId },
          extra: context
        });
      }
    };
  }
  
  // ログフォーマット標準
  defineLogFormat(): LogFormat {
    return {
      // 基本フィールド
      required: {
        timestamp: "ISO 8601形式",
        level: "ログレベル",
        message: "人間が読めるメッセージ",
        service: "サービス名"
      },
      
      // コンテキストフィールド
      contextual: {
        requestId: "リクエストID",
        userId: "ユーザーID",
        sessionId: "セッションID",
        traceId: "トレースID",
        spanId: "スパンID"
      },
      
      // メタデータ
      metadata: {
        environment: "環境名",
        version: "アプリケーションバージョン",
        hostname: "ホスト名",
        pid: "プロセスID"
      },
      
      // カスタムフィールド
      custom: {
        duration: "処理時間（ミリ秒）",
        statusCode: "HTTPステータスコード",
        method: "HTTPメソッド",
        path: "リクエストパス",
        userAgent: "User-Agent",
        ip: "クライアントIP"
      }
    };
  }
}
```

## メトリクス収集と可視化

### カスタムメトリクス

```typescript
export class MetricsCollection {
  private registry = new promClient.Registry();
  
  // メトリクスの定義
  defineMetrics(): ApplicationMetrics {
    return {
      // HTTPメトリクス
      http: {
        requestsTotal: new promClient.Counter({
          name: 'http_requests_total',
          help: 'Total number of HTTP requests',
          labelNames: ['method', 'path', 'status'],
          registers: [this.registry]
        }),
        
        requestDuration: new promClient.Histogram({
          name: 'http_request_duration_seconds',
          help: 'HTTP request latency',
          labelNames: ['method', 'path', 'status'],
          buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
          registers: [this.registry]
        }),
        
        activeRequests: new promClient.Gauge({
          name: 'http_requests_active',
          help: 'Number of active HTTP requests',
          registers: [this.registry]
        })
      },
      
      // ビジネスメトリクス
      business: {
        ordersCreated: new promClient.Counter({
          name: 'orders_created_total',
          help: 'Total number of orders created',
          labelNames: ['payment_method', 'status'],
          registers: [this.registry]
        }),
        
        revenue: new promClient.Counter({
          name: 'revenue_total',
          help: 'Total revenue',
          labelNames: ['currency', 'product_category'],
          registers: [this.registry]
        }),
        
        cartAbandonment: new promClient.Gauge({
          name: 'cart_abandonment_rate',
          help: 'Shopping cart abandonment rate',
          registers: [this.registry]
        })
      },
      
      // システムメトリクス
      system: {
        cpuUsage: new promClient.Gauge({
          name: 'process_cpu_usage_percent',
          help: 'CPU usage percentage',
          registers: [this.registry],
          collect() {
            this.set(process.cpuUsage().user / 1000000);
          }
        }),
        
        memoryUsage: new promClient.Gauge({
          name: 'process_memory_usage_bytes',
          help: 'Memory usage in bytes',
          registers: [this.registry],
          collect() {
            const usage = process.memoryUsage();
            this.set({ type: 'rss' }, usage.rss);
            this.set({ type: 'heap_total' }, usage.heapTotal);
            this.set({ type: 'heap_used' }, usage.heapUsed);
            this.set({ type: 'external' }, usage.external);
          }
        })
      },
      
      // カスタムメトリクス実装
      custom: {
        recordBusinessEvent: (eventType: string, metadata: any) => {
          switch (eventType) {
            case 'order.created':
              this.business.ordersCreated.inc({
                payment_method: metadata.paymentMethod,
                status: metadata.status
              });
              this.business.revenue.inc({
                currency: metadata.currency,
                product_category: metadata.category
              }, metadata.amount);
              break;
            
            case 'cart.abandoned':
              this.business.cartAbandonment.set(metadata.rate);
              break;
          }
        }
      }
    };
  }
  
  // メトリクスエンドポイント
  exposeMetrics(): Router {
    const router = Router();
    
    router.get('/metrics', async (req, res) => {
      try {
        res.set('Content-Type', this.registry.contentType);
        res.end(await this.registry.metrics());
      } catch (error) {
        res.status(500).end(error);
      }
    });
    
    return router;
  }
}
```

### ダッシュボード設計

```typescript
export class DashboardDesign {
  // Grafanaダッシュボード定義
  createDashboard(): GrafanaDashboard {
    return {
      title: "Parasol V5.4 Overview",
      
      panels: [
        // ゴールデンシグナル
        {
          title: "Request Rate",
          type: "graph",
          targets: [{
            expr: 'rate(http_requests_total[5m])',
            legendFormat: '{{method}} {{path}}'
          }],
          gridPos: { x: 0, y: 0, w: 12, h: 8 }
        },
        
        {
          title: "Error Rate",
          type: "graph",
          targets: [{
            expr: 'rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])',
            legendFormat: 'Error Rate %'
          }],
          alert: {
            condition: "above",
            threshold: 0.05,
            duration: "5m"
          },
          gridPos: { x: 12, y: 0, w: 12, h: 8 }
        },
        
        {
          title: "Response Time (p95)",
          type: "graph",
          targets: [{
            expr: 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))',
            legendFormat: 'p95'
          }],
          gridPos: { x: 0, y: 8, w: 12, h: 8 }
        },
        
        {
          title: "Saturation",
          type: "graph",
          targets: [
            {
              expr: 'process_cpu_usage_percent',
              legendFormat: 'CPU %'
            },
            {
              expr: 'process_memory_usage_bytes{type="heap_used"} / process_memory_usage_bytes{type="heap_total"}',
              legendFormat: 'Memory %'
            }
          ],
          gridPos: { x: 12, y: 8, w: 12, h: 8 }
        },
        
        // ビジネスメトリクス
        {
          title: "Business Metrics",
          type: "row",
          collapsed: false,
          gridPos: { x: 0, y: 16, w: 24, h: 1 }
        },
        
        {
          title: "Order Creation Rate",
          type: "stat",
          targets: [{
            expr: 'rate(orders_created_total[1h])',
            format: "time_series"
          }],
          gridPos: { x: 0, y: 17, w: 6, h: 4 }
        },
        
        {
          title: "Revenue",
          type: "stat",
          targets: [{
            expr: 'increase(revenue_total[1h])',
            format: "time_series"
          }],
          gridPos: { x: 6, y: 17, w: 6, h: 4 }
        },
        
        {
          title: "Cart Abandonment Rate",
          type: "gauge",
          targets: [{
            expr: 'cart_abandonment_rate',
            format: "time_series"
          }],
          thresholds: {
            mode: "absolute",
            steps: [
              { color: "green", value: 0 },
              { color: "yellow", value: 0.3 },
              { color: "red", value: 0.5 }
            ]
          },
          gridPos: { x: 12, y: 17, w: 6, h: 4 }
        }
      ],
      
      // 変数定義
      templating: {
        list: [
          {
            name: "environment",
            type: "query",
            query: 'label_values(environment)',
            current: { text: "production", value: "production" }
          },
          {
            name: "instance",
            type: "query",
            query: 'label_values(instance)',
            multi: true,
            includeAll: true
          }
        ]
      },
      
      // アノテーション
      annotations: {
        list: [
          {
            name: "Deployments",
            datasource: "prometheus",
            expr: 'changes(app_info{version="$version"}[5m])',
            tagKeys: "version,environment"
          },
          {
            name: "Incidents",
            datasource: "elasticsearch",
            query: 'level:ERROR AND message:"incident"'
          }
        ]
      }
    };
  }
}
```

## 分散トレーシング

### トレース実装

```typescript
export class DistributedTracing {
  // OpenTelemetry設定
  initializeTracing(): TracingSetup {
    const provider = new NodeTracerProvider({
      resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: 'parasol-api',
        [SemanticResourceAttributes.SERVICE_VERSION]: process.env.VERSION,
        [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV
      })
    });
    
    // エクスポーター設定
    const exporter = new JaegerExporter({
      endpoint: 'http://jaeger-collector:14268/api/traces'
    });
    
    // バッチプロセッサー
    provider.addSpanProcessor(
      new BatchSpanProcessor(exporter, {
        maxQueueSize: 1000,
        scheduledDelayMillis: 5000
      })
    );
    
    // サンプリング戦略
    const sampler = new TraceIdRatioBasedSampler(0.1); // 10%サンプリング
    
    provider.register();
    
    return {
      tracer: trace.getTracer('parasol-api'),
      
      // HTTPインストルメンテーション
      instrumentations: [
        new HttpInstrumentation({
          requestHook: (span, request) => {
            span.setAttributes({
              'http.request.body.size': request.headers['content-length'],
              'user.id': request.user?.id
            });
          }
        }),
        
        new ExpressInstrumentation({
          ignoreLayersType: ['middleware']
        }),
        
        new MongoDBInstrumentation(),
        new RedisInstrumentation(),
        new IORedisInstrumentation()
      ]
    };
  }
  
  // カスタムスパン
  implementCustomTracing(): TracingUtilities {
    return {
      // 手動スパン作成
      traceAsync: async <T>(
        operationName: string,
        fn: () => Promise<T>,
        attributes?: Attributes
      ): Promise<T> => {
        const span = trace.getActiveSpan() || trace.getTracer('parasol-api').startSpan(operationName);
        
        try {
          span.setAttributes(attributes || {});
          const result = await fn();
          span.setStatus({ code: SpanStatusCode.OK });
          return result;
        } catch (error) {
          span.recordException(error as Error);
          span.setStatus({
            code: SpanStatusCode.ERROR,
            message: (error as Error).message
          });
          throw error;
        } finally {
          span.end();
        }
      },
      
      // コンテキスト伝播
      propagateContext: (carrier: any): Context => {
        const propagator = new CompositePropagator({
          propagators: [
            new W3CTraceContextPropagator(),
            new W3CBaggagePropagator()
          ]
        });
        
        return propagator.extract(context.active(), carrier, defaultTextMapGetter);
      },
      
      // スパン装飾
      decorateSpan: (span: Span, metadata: SpanMetadata) => {
        // 基本属性
        span.setAttributes({
          'app.version': process.env.VERSION,
          'app.environment': process.env.NODE_ENV,
          'app.region': process.env.AWS_REGION
        });
        
        // カスタム属性
        if (metadata.userId) {
          span.setAttribute('user.id', metadata.userId);
        }
        
        if (metadata.tags) {
          Object.entries(metadata.tags).forEach(([key, value]) => {
            span.setAttribute(`custom.${key}`, value);
          });
        }
        
        // イベント記録
        if (metadata.events) {
          metadata.events.forEach(event => {
            span.addEvent(event.name, event.attributes);
          });
        }
      }
    };
  }
}
```

## アラートとインシデント管理

### インテリジェントアラート

```typescript
export class AlertingSystem {
  // アラートルール定義
  defineAlertRules(): AlertRules {
    return {
      // SLOベースアラート
      sloAlerts: [
        {
          name: "API Availability SLO",
          expression: `
            (1 - (
              rate(http_requests_total{status=~"5.."}[5m]) /
              rate(http_requests_total[5m])
            )) < 0.999
          `,
          duration: "5m",
          severity: "critical",
          annotations: {
            summary: "API availability below 99.9%",
            description: "Current availability: {{ $value | humanizePercentage }}"
          }
        },
        {
          name: "Response Time SLO",
          expression: `
            histogram_quantile(0.95,
              rate(http_request_duration_seconds_bucket[5m])
            ) > 0.5
          `,
          duration: "10m",
          severity: "warning",
          annotations: {
            summary: "95th percentile response time > 500ms",
            description: "Current p95: {{ $value | humanizeDuration }}"
          }
        }
      ],
      
      // 異常検知アラート
      anomalyAlerts: [
        {
          name: "Unusual Error Rate",
          type: "statistical",
          metric: "http_requests_total{status=~'5..'}",
          method: "z-score",
          threshold: 3,
          lookback: "1h",
          severity: "warning"
        },
        {
          name: "Traffic Anomaly",
          type: "ml-based",
          model: "prophet",
          metric: "http_requests_total",
          confidence: 0.95,
          severity: "info"
        }
      ],
      
      // 複合条件アラート
      compositeAlerts: [
        {
          name: "System Degradation",
          conditions: [
            "error_rate > 0.05",
            "response_time_p95 > 1s",
            "cpu_usage > 80%"
          ],
          logic: "AND",
          duration: "3m",
          severity: "critical"
        }
      ]
    };
  }
  
  // アラート配信
  implementAlertRouting(): AlertRouting {
    return {
      // 重要度別ルーティング
      routes: [
        {
          match: { severity: "critical" },
          receivers: ["pagerduty", "slack-critical", "email-oncall"],
          groupBy: ["alertname", "cluster"],
          groupWait: "10s",
          groupInterval: "10s",
          repeatInterval: "1h"
        },
        {
          match: { severity: "warning" },
          receivers: ["slack-warnings", "email-team"],
          groupBy: ["alertname"],
          groupWait: "5m",
          groupInterval: "10m",
          repeatInterval: "4h"
        },
        {
          match: { severity: "info" },
          receivers: ["slack-info"],
          groupBy: ["alertname"],
          groupWait: "10m",
          groupInterval: "30m",
          repeatInterval: "12h"
        }
      ],
      
      // 受信者設定
      receivers: {
        pagerduty: {
          type: "pagerduty",
          config: {
            serviceKey: process.env.PAGERDUTY_SERVICE_KEY,
            details: {
              firing: "{{ range .Alerts.Firing }}{{ .Annotations.description }}{{ end }}",
              resolved: "{{ range .Alerts.Resolved }}{{ .Annotations.description }}{{ end }}",
              num_firing: "{{ .Alerts.Firing | len }}",
              num_resolved: "{{ .Alerts.Resolved | len }}"
            }
          }
        },
        
        slack: {
          type: "slack",
          config: {
            apiUrl: process.env.SLACK_WEBHOOK_URL,
            channel: "#alerts",
            title: "Alert: {{ .GroupLabels.alertname }}",
            text: "{{ .CommonAnnotations.summary }}",
            color: "{{ if eq .Status 'firing' }}danger{{ else }}good{{ end }}"
          }
        }
      },
      
      // 抑制ルール
      inhibitRules: [
        {
          sourceMatch: { severity: "critical" },
          targetMatch: { severity: "warning" },
          equal: ["alertname", "instance"]
        }
      ]
    };
  }
}
```

### インシデント対応自動化

```typescript
export class IncidentAutomation {
  // インシデント対応ワークフロー
  async handleIncident(alert: Alert): Promise<IncidentResponse> {
    const incident = await this.createIncident(alert);
    
    // 1. 初期対応
    const initialResponse = await this.performInitialResponse(incident);
    
    // 2. 診断実行
    const diagnostics = await this.runDiagnostics(incident);
    
    // 3. 自動修復試行
    if (this.canAutoRemediate(incident, diagnostics)) {
      const remediation = await this.attemptAutoRemediation(incident);
      if (remediation.success) {
        return this.resolveIncident(incident, remediation);
      }
    }
    
    // 4. エスカレーション
    await this.escalateIncident(incident, diagnostics);
    
    // 5. 継続的監視
    this.monitorIncident(incident);
    
    return {
      incidentId: incident.id,
      status: incident.status,
      assignee: incident.assignee,
      timeline: incident.timeline
    };
  }
  
  // 自動診断
  private async runDiagnostics(incident: Incident): Promise<DiagnosticsResult> {
    const diagnostics: Diagnostic[] = [];
    
    // ログ分析
    diagnostics.push(await this.analyzeRecentLogs(incident));
    
    // メトリクス相関
    diagnostics.push(await this.correlateMetrics(incident));
    
    // トレース分析
    diagnostics.push(await this.analyzeTraces(incident));
    
    // 依存関係チェック
    diagnostics.push(await this.checkDependencies(incident));
    
    // 変更履歴確認
    diagnostics.push(await this.reviewRecentChanges(incident));
    
    return {
      diagnostics,
      rootCause: this.identifyRootCause(diagnostics),
      recommendations: this.generateRecommendations(diagnostics)
    };
  }
  
  // ランブック実行
  async executeRunbook(incident: Incident): Promise<RunbookExecution> {
    const runbook = await this.selectRunbook(incident);
    
    if (!runbook) {
      return { status: "no_runbook_available" };
    }
    
    const execution = new RunbookExecution(runbook);
    
    for (const step of runbook.steps) {
      try {
        const result = await this.executeStep(step, incident);
        execution.recordStep(step, result);
        
        if (step.breakOnFailure && !result.success) {
          break;
        }
      } catch (error) {
        execution.recordError(step, error);
        if (step.critical) {
          break;
        }
      }
    }
    
    return execution;
  }
}
```

## ログ分析と検索

### ログ検索エンジン

```typescript
export class LogAnalytics {
  // Elasticsearchインテグレーション
  implementLogSearch(): LogSearchEngine {
    const client = new ElasticsearchClient({
      nodes: ['http://elasticsearch:9200'],
      auth: {
        username: process.env.ES_USERNAME,
        password: process.env.ES_PASSWORD
      }
    });
    
    return {
      // インデックステンプレート
      indexTemplate: {
        name: "parasol-logs",
        index_patterns: ["logs-parasol-*"],
        template: {
          settings: {
            number_of_shards: 3,
            number_of_replicas: 1,
            "index.lifecycle.name": "parasol-logs-policy",
            "index.lifecycle.rollover_alias": "logs-parasol"
          },
          mappings: {
            properties: {
              "@timestamp": { type: "date" },
              level: { type: "keyword" },
              message: { type: "text", fields: { keyword: { type: "keyword" } } },
              service: { type: "keyword" },
              environment: { type: "keyword" },
              requestId: { type: "keyword" },
              userId: { type: "keyword" },
              traceId: { type: "keyword" },
              duration: { type: "long" },
              error: {
                properties: {
                  message: { type: "text" },
                  stack: { type: "text" },
                  type: { type: "keyword" }
                }
              }
            }
          }
        }
      },
      
      // 検索クエリビルダー
      searchBuilder: {
        byRequestId: (requestId: string) => ({
          query: {
            term: { requestId }
          },
          sort: [{ "@timestamp": "asc" }]
        }),
        
        byTimeRange: (from: Date, to: Date, filters?: any) => ({
          query: {
            bool: {
              must: [
                {
                  range: {
                    "@timestamp": {
                      gte: from.toISOString(),
                      lte: to.toISOString()
                    }
                  }
                },
                ...(filters || [])
              ]
            }
          }
        }),
        
        byError: (errorType?: string) => ({
          query: {
            bool: {
              must: [
                { term: { level: "ERROR" } },
                ...(errorType ? [{ term: { "error.type": errorType } }] : [])
              ]
            }
          },
          aggs: {
            error_types: {
              terms: { field: "error.type" }
            }
          }
        })
      },
      
      // 集約分析
      aggregations: {
        errorTrends: {
          date_histogram: {
            field: "@timestamp",
            calendar_interval: "1h"
          },
          aggs: {
            by_error_type: {
              terms: { field: "error.type" }
            }
          }
        },
        
        slowRequests: {
          range: {
            field: "duration",
            ranges: [
              { key: "fast", to: 100 },
              { key: "normal", from: 100, to: 1000 },
              { key: "slow", from: 1000, to: 5000 },
              { key: "very_slow", from: 5000 }
            ]
          }
        }
      }
    };
  }
  
  // ログ相関分析
  async correlateLogsWithIncident(
    incident: Incident
  ): Promise<CorrelatedLogs> {
    const timeWindow = {
      start: new Date(incident.startTime.getTime() - 30 * 60 * 1000), // 30分前
      end: new Date(incident.endTime?.getTime() || Date.now())
    };
    
    // 関連ログの収集
    const logs = await this.searchLogs({
      timeRange: timeWindow,
      filters: [
        { level: ["ERROR", "WARN"] },
        { service: incident.affectedServices }
      ]
    });
    
    // パターン分析
    const patterns = await this.analyzeLogPatterns(logs);
    
    // タイムライン構築
    const timeline = this.buildTimeline(logs, incident);
    
    return {
      logs,
      patterns,
      timeline,
      summary: this.generateLogSummary(patterns)
    };
  }
}
```

## 運用ダッシュボードとレポート

### 運用ダッシュボード

```typescript
export class OperationalDashboard {
  // SREダッシュボード
  createSREDashboard(): DashboardConfig {
    return {
      name: "SRE Overview",
      
      sections: [
        // SLI/SLO
        {
          title: "Service Level Indicators",
          widgets: [
            {
              type: "slo-gauge",
              title: "Availability SLO",
              query: `
                sum(rate(http_requests_total{status!~"5.."}[5m])) /
                sum(rate(http_requests_total[5m]))
              `,
              target: 0.999,
              thresholds: {
                good: 0.999,
                warning: 0.995,
                bad: 0.99
              }
            },
            {
              type: "error-budget",
              title: "Error Budget Remaining",
              calculation: {
                slo: 0.999,
                window: "30d",
                consumed: "auto"
              }
            }
          ]
        },
        
        // 四つのゴールデンシグナル
        {
          title: "Golden Signals",
          widgets: [
            {
              type: "time-series",
              title: "Traffic",
              query: "sum(rate(http_requests_total[5m]))"
            },
            {
              type: "time-series",
              title: "Errors",
              query: `sum(rate(http_requests_total{status=~"5.."}[5m]))`
            },
            {
              type: "heatmap",
              title: "Latency",
              query: "http_request_duration_seconds_bucket"
            },
            {
              type: "gauge",
              title: "Saturation",
              queries: {
                cpu: "avg(cpu_usage_percent)",
                memory: "avg(memory_usage_percent)",
                disk: "avg(disk_usage_percent)"
              }
            }
          ]
        }
      ]
    };
  }
  
  // レポート生成
  async generateReport(period: ReportPeriod): Promise<Report> {
    const metrics = await this.collectMetrics(period);
    const incidents = await this.getIncidents(period);
    const changes = await this.getDeployments(period);
    
    return {
      executive_summary: {
        availability: this.calculateAvailability(metrics),
        incidents: {
          total: incidents.length,
          severity: this.groupBySeverity(incidents)
        },
        deployments: {
          total: changes.length,
          success_rate: this.calculateDeploymentSuccess(changes)
        }
      },
      
      detailed_analysis: {
        performance_trends: this.analyzePerformanceTrends(metrics),
        incident_analysis: this.analyzeIncidents(incidents),
        capacity_planning: this.projectCapacityNeeds(metrics)
      },
      
      recommendations: this.generateRecommendations({
        metrics,
        incidents,
        changes
      })
    };
  }
}
```

## まとめ

効果的な監視とロギングは、システムの健康状態を把握し、問題を迅速に解決するための基盤です。Parasol V5.4における成功の鍵：

1. **オブザーバビリティの3本柱** - メトリクス、ログ、トレースの統合
2. **構造化ロギング** - 検索と分析を容易にする一貫した形式
3. **プロアクティブな監視** - 問題が顕在化する前の検知
4. **自動化された対応** - インシデント対応の迅速化
5. **継続的な改善** - データに基づく最適化

適切に実装された監視システムは、システムの信頼性を高め、運用負荷を軽減します。

### 第V部のまとめ

第V部では、解決領域における実装の詳細を見てきました。アーキテクチャ設計、ソフトウェア設計、そして実装品質の3つの観点から、Parasol V5.4の具体的な実現方法を解説しました。

次の第VI部では、これらの要素をどのように統合し、実際のシステムとして動作させるかを見ていきます。

---

## 演習問題

1. あなたのシステムに対して、SLI/SLOを定義してください。四つのゴールデンシグナルそれぞれについて、具体的な目標値と測定方法を示してください。

2. 以下のシナリオに対して、適切なログ出力とメトリクス記録を実装してください：
   - ユーザーが商品をカートに追加
   - 注文処理中にエラーが発生
   - 外部APIの呼び出しがタイムアウト

3. インシデント発生時の自動診断フローを設計してください。収集すべき情報と、自動修復可能な条件を含めてください。