# 付録：第32章　実世界のケーススタディ実装詳細

## プロジェクト概要

```typescript
export interface ECReplatformingProject {
  context: {
    company: "日本大手EC企業";
    scale: {
      dailyActiveUsers: 5000000;
      peakTransactions: 100000; // per hour
      productCatalog: 10000000;
      annualGMV: "1兆円";
    };
    challenges: [
      "レガシーモノリスの技術的負債",
      "スケーラビリティの限界",
      "開発速度の低下",
      "運用コストの増大"
    ];
    objectives: [
      "マイクロサービス化による拡張性向上",
      "開発生産性の改善",
      "運用コストの30%削減",
      "レスポンスタイムの50%改善"
    ];
  };
}
```

## Strangler Figパターンの実装

```typescript
class StranglerFigImplementation {
  // レガシーシステムとの共存
  async routeRequest(req: Request): Promise<Response> {
    const path = req.url.pathname;
    
    // 新システムに移行済みのパス
    const migratedPaths = [
      /^\/api\/v2\/auth/,
      /^\/api\/v2\/products/,
      /^\/api\/v2\/inventory/
    ];
    
    // 移行済みパスは新システムへ
    if (migratedPaths.some(pattern => pattern.test(path))) {
      return this.routeToNewSystem(req);
    }
    
    // それ以外はレガシーシステムへ
    return this.routeToLegacySystem(req);
  }
  
  // 段階的なトラフィック移行
  async canaryDeployment(feature: string): Promise<void> {
    const stages = [
      { percentage: 5, duration: '1d', monitoring: 'enhanced' },
      { percentage: 25, duration: '3d', monitoring: 'normal' },
      { percentage: 50, duration: '1w', monitoring: 'normal' },
      { percentage: 100, duration: 'permanent', monitoring: 'normal' }
    ];
    
    for (const stage of stages) {
      await this.updateTrafficSplit(feature, stage.percentage);
      await this.monitorMetrics(stage.duration);
      
      if (await this.hasIssues()) {
        await this.rollback();
        throw new Error('Canary deployment failed');
      }
    }
  }
  
  private async routeToNewSystem(req: Request): Promise<Response> {
    const serviceMap = {
      '/api/v2/auth': 'http://auth-service:8080',
      '/api/v2/products': 'http://product-service:8080',
      '/api/v2/inventory': 'http://inventory-service:8080'
    };
    
    const targetService = Object.keys(serviceMap).find(path => 
      req.url.pathname.startsWith(path)
    );
    
    if (!targetService) {
      return new Response('Not Found', { status: 404 });
    }
    
    return fetch(serviceMap[targetService] + req.url.pathname, {
      method: req.method,
      headers: req.headers,
      body: req.body
    });
  }
}
```

## イベントソーシングの実装

<div id="event-sourcing"></div>

```typescript
// イベントソーシングによる注文管理
class OrderEventSourcing {
  async processOrder(command: CreateOrderCommand): Promise<Order> {
    const events: DomainEvent[] = [];
    
    // 在庫確認
    const inventoryReserved = await this.reserveInventory(
      command.items
    );
    events.push(new InventoryReservedEvent(inventoryReserved));
    
    // 価格計算
    const pricing = await this.calculatePricing(command);
    events.push(new PriceCalculatedEvent(pricing));
    
    // 決済処理
    const payment = await this.processPayment({
      amount: pricing.total,
      method: command.paymentMethod
    });
    events.push(new PaymentProcessedEvent(payment));
    
    // イベントストアに保存
    await this.eventStore.append(command.orderId, events);
    
    // Read Modelの更新
    await this.projectionsUpdater.update(events);
    
    return this.getOrder(command.orderId);
  }
  
  // 補償トランザクション
  async compensateOrder(orderId: string, reason: string): Promise<void> {
    const events = await this.eventStore.getEvents(orderId);
    const compensations: CompensationEvent[] = [];
    
    // 逆順で補償処理
    for (const event of events.reverse()) {
      switch (event.type) {
        case 'PaymentProcessed':
          compensations.push(
            await this.refundPayment(event.data)
          );
          break;
        
        case 'InventoryReserved':
          compensations.push(
            await this.releaseInventory(event.data)
          );
          break;
      }
    }
    
    await this.eventStore.append(orderId, compensations);
  }
  
  // イベントストアの実装
  private eventStore = {
    async append(aggregateId: string, events: DomainEvent[]): Promise<void> {
      const connection = await this.getConnection();
      const transaction = connection.startTransaction();
      
      try {
        for (const event of events) {
          await transaction.query(
            `INSERT INTO event_store 
             (aggregate_id, event_type, event_data, event_version, created_at)
             VALUES (?, ?, ?, ?, ?)`,
            [
              aggregateId,
              event.type,
              JSON.stringify(event.data),
              event.version,
              new Date()
            ]
          );
        }
        
        await transaction.commit();
      } catch (error) {
        await transaction.rollback();
        throw error;
      }
    },
    
    async getEvents(aggregateId: string): Promise<DomainEvent[]> {
      const results = await this.query(
        `SELECT * FROM event_store 
         WHERE aggregate_id = ? 
         ORDER BY event_version ASC`,
        [aggregateId]
      );
      
      return results.map(row => ({
        type: row.event_type,
        data: JSON.parse(row.event_data),
        version: row.event_version,
        createdAt: row.created_at
      }));
    }
  };
}

// Sagaパターンによるトランザクション管理
class OrderSaga {
  async execute(order: Order): Promise<SagaResult> {
    const compensations: CompensationAction[] = [];
    
    try {
      // 在庫予約
      const reservation = await this.inventoryService.reserve(
        order.items
      );
      compensations.push(() => 
        this.inventoryService.release(reservation.id)
      );
      
      // 支払い処理
      const payment = await this.paymentService.charge(
        order.payment
      );
      compensations.push(() => 
        this.paymentService.refund(payment.id)
      );
      
      // 配送手配
      const shipping = await this.shippingService.arrange(
        order.shipping
      );
      compensations.push(() => 
        this.shippingService.cancel(shipping.id)
      );
      
      return { success: true, order };
    } catch (error) {
      // 補償処理の実行
      await this.compensate(compensations);
      return { success: false, error };
    }
  }
  
  private async compensate(
    compensations: CompensationAction[]
  ): Promise<void> {
    // 逆順で実行
    for (const compensation of compensations.reverse()) {
      try {
        await compensation();
      } catch (error) {
        // 補償処理のエラーはログに記録して続行
        console.error('Compensation failed:', error);
      }
    }
  }
}
```

## 金融機関のハイブリッドアーキテクチャ

```typescript
class CoreBankingAdapter {
  // バッチ処理との統合
  async processDailyBatch(): Promise<BatchResult> {
    // 日次締め処理
    const cutoffTime = this.getCutoffTime();
    
    // オンライン取引の一時停止
    await this.suspendOnlineTransactions();
    
    // バッチファイルの生成
    const transactions = await this.extractTransactions(cutoffTime);
    const batchFile = await this.generateBatchFile(transactions);
    
    // メインフレームへの送信
    await this.sendToMainframe(batchFile);
    
    // 結果の待機と処理
    const result = await this.waitForBatchResult();
    await this.processBatchResult(result);
    
    // オンライン取引の再開
    await this.resumeOnlineTransactions();
    
    return result;
  }
  
  // リアルタイム照会
  async getAccountBalance(accountId: string): Promise<Balance> {
    // キャッシュチェック
    const cached = await this.cache.get(`balance:${accountId}`);
    if (cached && this.isFresh(cached)) {
      return cached;
    }
    
    // メインフレームへの照会
    const mfQuery = this.buildMainframeQuery(accountId);
    const response = await this.queryMainframe(mfQuery);
    
    // 結果の解析とキャッシュ
    const balance = this.parseBalance(response);
    await this.cache.set(
      `balance:${accountId}`,
      balance,
      { ttl: 300 } // 5分間キャッシュ
    );
    
    return balance;
  }
  
  private buildMainframeQuery(accountId: string): string {
    // COBOL形式のクエリを構築
    return `
      IDENTIFICATION DIVISION.
      PROGRAM-ID. BALANCE-INQUIRY.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
      01 WS-ACCOUNT-ID PIC X(10) VALUE '${accountId}'.
      01 WS-BALANCE PIC 9(15)V99.
      
      PROCEDURE DIVISION.
      MAIN-PROCEDURE.
          CALL 'GETBAL' USING WS-ACCOUNT-ID WS-BALANCE
          DISPLAY WS-BALANCE
          STOP RUN.
    `;
  }
}

// セキュリティフレームワーク
class SecurityFramework {
  // 多層防御の実装
  async validateTransaction(
    transaction: Transaction
  ): Promise<ValidationResult> {
    const checks = [
      this.checkDeviceFingerprint(transaction),
      this.checkGeoLocation(transaction),
      this.checkVelocity(transaction),
      this.checkPattern(transaction),
      this.runMLFraudDetection(transaction)
    ];
    
    const results = await Promise.all(checks);
    
    const riskScore = this.calculateRiskScore(results);
    
    if (riskScore > 0.8) {
      await this.requireAdditionalAuth(transaction);
    }
    
    return {
      approved: riskScore < 0.9,
      riskScore,
      checks: results
    };
  }
  
  private async checkDeviceFingerprint(
    transaction: Transaction
  ): Promise<CheckResult> {
    const knownDevice = await this.deviceRegistry.lookup(
      transaction.deviceId
    );
    
    if (!knownDevice) {
      return { passed: false, reason: 'Unknown device' };
    }
    
    const fingerprint = this.generateFingerprint(transaction.device);
    if (fingerprint !== knownDevice.fingerprint) {
      return { passed: false, reason: 'Device fingerprint mismatch' };
    }
    
    return { passed: true };
  }
  
  private calculateRiskScore(results: CheckResult[]): number {
    const weights = {
      deviceFingerprint: 0.3,
      geoLocation: 0.2,
      velocity: 0.2,
      pattern: 0.15,
      mlFraud: 0.15
    };
    
    let score = 0;
    results.forEach((result, index) => {
      if (!result.passed) {
        score += weights[Object.keys(weights)[index]];
      }
    });
    
    return score;
  }
}
```

## ヘルスケアプラットフォームのプライバシー保護

```typescript
class MedicalDataEncryption {
  // フィールドレベル暗号化
  async encryptPatientRecord(
    record: PatientRecord
  ): Promise<EncryptedRecord> {
    const encrypted: any = {
      id: record.id, // 識別子は平文
      metadata: record.metadata // メタデータも平文
    };
    
    // 個人情報の暗号化
    encrypted.personalInfo = await this.encryptField(
      record.personalInfo,
      'AES-256-GCM',
      this.keys.pii
    );
    
    // 医療情報の暗号化（より強い暗号化）
    encrypted.medicalInfo = await this.encryptField(
      record.medicalInfo,
      'AES-256-GCM',
      this.keys.medical
    );
    
    // 検索可能暗号化インデックスの生成
    encrypted.searchIndex = await this.generateSearchableIndex({
      name: record.personalInfo.name,
      birthDate: record.personalInfo.birthDate,
      patientId: record.personalInfo.patientId
    });
    
    return encrypted;
  }
  
  // 準同型暗号による統計処理
  async calculateStatistics(
    encryptedData: EncryptedRecord[]
  ): Promise<Statistics> {
    // 暗号化されたまま統計処理
    const encryptedSum = await this.homomorphicSum(
      encryptedData.map(d => d.medicalInfo.bloodPressure)
    );
    
    const encryptedAverage = await this.homomorphicDivide(
      encryptedSum,
      encryptedData.length
    );
    
    // 必要な場合のみ復号
    return {
      average: await this.decrypt(encryptedAverage)
    };
  }
  
  private async generateSearchableIndex(
    data: SearchableData
  ): Promise<EncryptedIndex> {
    // 決定性暗号化でインデックスを生成
    const index = {};
    
    for (const [key, value] of Object.entries(data)) {
      const hash = await this.deterministicHash(value);
      index[key] = hash;
    }
    
    return index;
  }
}

// HL7 FHIR統合
class HL7FHIRIntegration {
  // FHIR準拠のデータ交換
  async exchangePatientData(
    request: DataExchangeRequest
  ): Promise<Bundle> {
    // 同意確認
    const consent = await this.consentManager.checkAccess(
      request.requester,
      request.patient,
      'medical-records'
    );
    
    if (!consent.allowed) {
      throw new UnauthorizedError(consent.reason);
    }
    
    // FHIRリソースの生成
    const patient = await this.createPatientResource(
      request.patient
    );
    
    const observations = await this.createObservationResources(
      request.patient.observations
    );
    
    const medications = await this.createMedicationResources(
      request.patient.medications
    );
    
    // Bundleの作成
    return {
      resourceType: 'Bundle',
      type: 'document',
      timestamp: new Date().toISOString(),
      entry: [
        { resource: patient },
        ...observations.map(o => ({ resource: o })),
        ...medications.map(m => ({ resource: m }))
      ]
    };
  }
  
  private createPatientResource(patient: Patient): FHIRPatient {
    return {
      resourceType: 'Patient',
      id: patient.id,
      identifier: [{
        system: 'http://hospital.example.org/patients',
        value: patient.patientId
      }],
      name: [{
        family: patient.familyName,
        given: [patient.givenName]
      }],
      gender: patient.gender,
      birthDate: patient.birthDate.toISOString().split('T')[0]
    };
  }
}
```

## エッジコンピューティングアーキテクチャ

<div id="edge-computing"></div>

```typescript
class EdgeNode {
  private readonly deviceManager = new DeviceManager();
  private readonly dataProcessor = new StreamProcessor();
  private readonly mlInference = new EdgeMLInference();
  
  async processDeviceData(
    deviceId: string,
    data: SensorData
  ): Promise<ProcessingResult> {
    // データ検証
    if (!this.validateData(data)) {
      return { status: 'invalid', reason: 'Data validation failed' };
    }
    
    // エッジでの前処理
    const processed = await this.preprocessData(data);
    
    // 異常検知（エッジML）
    const anomaly = await this.mlInference.detectAnomaly(processed);
    if (anomaly.score > 0.8) {
      // 即座にアラート
      await this.sendAlert({
        deviceId,
        anomaly,
        priority: 'high'
      });
    }
    
    // データ集約
    const aggregated = await this.aggregateData(processed);
    
    // クラウドへの送信判断
    if (this.shouldSendToCloud(aggregated)) {
      await this.sendToCloud(aggregated);
    }
    
    return { status: 'processed', data: aggregated };
  }
  
  // エッジでのML推論
  private async detectTrafficAnomaly(
    trafficData: TrafficData
  ): Promise<AnomalyResult> {
    // 軽量モデルでの推論
    const features = this.extractFeatures(trafficData);
    const prediction = await this.mlInference.predict(
      'traffic-anomaly-model',
      features
    );
    
    // 信頼度が高い場合は即座に信号制御
    if (prediction.confidence > 0.9) {
      await this.adjustTrafficSignals({
        intersection: trafficData.location,
        adjustment: prediction.recommendation
      });
    }
    
    return prediction;
  }
  
  private shouldSendToCloud(data: AggregatedData): boolean {
    // クラウド送信の判断基準
    if (data.anomalyScore > 0.5) return true;
    if (data.timestamp.getMinutes() % 5 === 0) return true; // 5分ごと
    if (data.significantChange) return true;
    
    return false;
  }
}

// ストリーム処理パイプライン
class StreamProcessingPipeline {
  // Apache Flinkによるストリーム処理
  async setupPipeline(): Promise<void> {
    const env = StreamExecutionEnvironment.getExecutionEnvironment();
    
    // Kafkaからのデータ取得
    const sensorStream = env.addSource(
      new FlinkKafkaConsumer(
        'sensor-data',
        new JSONDeserializationSchema(),
        this.kafkaProperties
      )
    );
    
    // ウィンドウ処理
    const aggregated = sensorStream
      .keyBy('sensorId')
      .window(TumblingEventTimeWindows.of(Time.minutes(5)))
      .aggregate(new SensorDataAggregator());
    
    // 複合イベント処理
    const patterns = aggregated
      .keyBy('area')
      .flatMap(new PatternDetector())
      .filter(pattern => pattern.significance > 0.7);
    
    // アラート生成
    patterns
      .filter(pattern => pattern.requiresAlert)
      .addSink(new AlertSink());
    
    // データレイクへの保存
    aggregated
      .addSink(new S3Sink({
        bucket: 'smart-city-data-lake',
        format: 'parquet'
      }));
    
    await env.execute('Smart City Stream Processing');
  }
}

// 市民サービスAPI
class CitizenServiceAPI {
  // 市民向けリアルタイムサービス
  async getTrafficConditions(
    location: GeoLocation,
    radius: number
  ): Promise<TrafficInfo> {
    // リアルタイムデータの取得
    const currentData = await this.cache.get(
      `traffic:${location.lat}:${location.lng}:${radius}`
    );
    
    if (currentData && this.isFresh(currentData, 30)) {
      return currentData;
    }
    
    // センサーデータの集約
    const sensorData = await this.getSensorData(location, radius);
    
    // AI予測モデルの適用
    const predictions = await this.predictTraffic({
      current: sensorData,
      historical: await this.getHistoricalData(location),
      events: await this.getPlannedEvents(location),
      weather: await this.getWeatherForecast()
    });
    
    const result = {
      current: this.analyzeCurrentTraffic(sensorData),
      predictions: predictions,
      alternatives: await this.suggestAlternativeRoutes(
        location,
        predictions
      ),
      lastUpdated: new Date()
    };
    
    // キャッシュ更新
    await this.cache.set(
      `traffic:${location.lat}:${location.lng}:${radius}`,
      result,
      { ttl: 30 }
    );
    
    return result;
  }
}
```

## 共通パターンの実装

```typescript
// マルチレイヤーキャッシュ
class MultiLayerCache {
  // L1: プロセス内キャッシュ
  private readonly l1Cache = new LRUCache({ max: 1000 });
  
  // L2: Redis分散キャッシュ
  private readonly l2Cache = new RedisCache();
  
  // L3: CDN/エッジキャッシュ
  private readonly l3Cache = new CDNCache();
  
  async get(key: string): Promise<any> {
    // L1チェック
    let value = this.l1Cache.get(key);
    if (value) return value;
    
    // L2チェック
    value = await this.l2Cache.get(key);
    if (value) {
      this.l1Cache.set(key, value);
      return value;
    }
    
    // L3チェック
    value = await this.l3Cache.get(key);
    if (value) {
      await this.propagateToLowerLayers(key, value);
      return value;
    }
    
    return null;
  }
  
  private async propagateToLowerLayers(
    key: string,
    value: any
  ): Promise<void> {
    // 下位レイヤーに伝播
    await this.l2Cache.set(key, value, { ttl: 3600 });
    this.l1Cache.set(key, value);
  }
}

// CQRSによる読み取り最適化
class ReadOptimizedArchitecture {
  async setupReadModel(): Promise<void> {
    // イベントストリームからの投影
    this.eventStream
      .subscribe('order-events')
      .map(event => this.projectEvent(event))
      .groupBy(projection => projection.viewType)
      .forEach(async (group) => {
        const viewUpdater = this.getViewUpdater(group.key);
        await viewUpdater.update(group.values);
      });
  }
  
  // 複数のReadモデル
  private setupViews(): ViewDefinitions {
    return {
      orderList: {
        storage: 'elasticsearch',
        optimizedFor: 'search and filter',
        updateStrategy: 'eventual'
      },
      orderDetail: {
        storage: 'mongodb',
        optimizedFor: 'document retrieval',
        updateStrategy: 'immediate'
      },
      analytics: {
        storage: 'clickhouse',
        optimizedFor: 'aggregation',
        updateStrategy: 'batch'
      }
    };
  }
}
```