# 付録：第36章　新興技術の統合の実装詳細

## AI/ML統合パターン

### AIコード生成システムの実装

```typescript
export class AICodeGenerator {
  private readonly model: LanguageModel;
  private readonly validator: CodeValidator;
  private readonly contextBuilder: ContextBuilder;
  
  async generateModule(
    specification: ModuleSpecification
  ): Promise<GeneratedModule> {
    // 1. コンテキストの構築
    const context = await this.buildContext(specification);
    
    // 2. プロンプトの生成
    const prompt = this.createPrompt(specification, context);
    
    // 3. AIモデルの呼び出し
    const generatedCode = await this.model.generate({
      prompt,
      maxTokens: 4000,
      temperature: 0.3,
      stopSequences: ['```', 'export class', 'export interface']
    });
    
    // 4. 生成されたコードの検証
    const validation = await this.validator.validate(generatedCode);
    
    // 5. 必要に応じて修正
    if (!validation.isValid) {
      return await this.refineCode(generatedCode, validation.errors);
    }
    
    // 6. テストとドキュメントの生成
    const tests = await this.generateTests(generatedCode);
    const documentation = await this.generateDocumentation(generatedCode);
    
    return {
      code: generatedCode,
      tests,
      documentation,
      metadata: {
        specification,
        generatedAt: new Date(),
        model: this.model.name,
        version: this.model.version
      }
    };
  }
  
  private async buildContext(
    specification: ModuleSpecification
  ): Promise<GenerationContext> {
    return {
      // 既存のインターフェース
      interfaces: await this.loadRelatedInterfaces(
        specification.dependencies
      ),
      
      // コーディング規約
      codingStandards: await this.loadCodingStandards(),
      
      // ドメイン知識
      domainKnowledge: await this.loadDomainKnowledge(
        specification.domain
      ),
      
      // アーキテクチャパターン
      patterns: await this.loadArchitecturePatterns(),
      
      // 類似モジュールの例
      examples: await this.findSimilarModules(specification)
    };
  }
  
  private createPrompt(
    spec: ModuleSpecification,
    context: GenerationContext
  ): string {
    return `
## Task: Generate TypeScript module

### Specification:
${JSON.stringify(spec, null, 2)}

### Context:
- Architecture: ${context.patterns.join(', ')}
- Domain: ${spec.domain}
- Dependencies: ${spec.dependencies.join(', ')}

### Requirements:
- Follow SOLID principles
- Include comprehensive error handling
- Add JSDoc comments
- Ensure type safety
- Follow project coding standards

### Related Interfaces:
${context.interfaces.map(i => i.definition).join('\n\n')}

### Generate the implementation:
`;
  }
}
```

### AIテスト生成システム

```typescript
export class AITestGenerator {
  async generateTests(
    module: ParsedModule,
    coverage: CoverageRequirements
  ): Promise<TestSuite> {
    const analysis = await this.analyzeModule(module);
    
    return {
      unit: await this.generateUnitTests(analysis),
      integration: await this.generateIntegrationTests(analysis),
      property: await this.generatePropertyTests(analysis),
      performance: await this.generatePerformanceTests(analysis)
    };
  }
  
  private async generateUnitTests(
    analysis: ModuleAnalysis
  ): Promise<UnitTest[]> {
    const tests: UnitTest[] = [];
    
    for (const method of analysis.methods) {
      // 正常系テスト
      tests.push(await this.generateHappyPathTest(method));
      
      // エッジケース
      tests.push(...await this.generateEdgeCaseTests(method));
      
      // エラーケース
      tests.push(...await this.generateErrorTests(method));
    }
    
    return tests;
  }
  
  private async generatePropertyTests(
    analysis: ModuleAnalysis
  ): Promise<PropertyTest[]> {
    return analysis.methods
      .filter(m => m.isPure)
      .map(method => ({
        name: `Property test for ${method.name}`,
        property: this.deriveProperty(method),
        generators: this.createGenerators(method.parameters),
        runs: 100,
        seed: Date.now()
      }));
  }
}
```

### 機械学習パイプライン

```typescript
export class MLPipeline {
  // モデルのトレーニングパイプライン
  async trainModel(
    dataset: Dataset,
    config: TrainingConfig
  ): Promise<TrainedModel> {
    // データの前処理
    const preprocessed = await this.preprocessData(dataset);
    
    // 特徴量エンジニアリング
    const features = await this.engineerFeatures(preprocessed);
    
    // データ分割
    const { train, validation, test } = this.splitData(features, {
      trainRatio: 0.7,
      validationRatio: 0.15,
      testRatio: 0.15
    });
    
    // モデルのトレーニング
    const model = await this.fitModel(train, validation, config);
    
    // 評価
    const metrics = await this.evaluateModel(model, test);
    
    // モデルの保存
    await this.saveModel(model, {
      metrics,
      metadata: {
        datasetId: dataset.id,
        trainedAt: new Date(),
        framework: config.framework,
        parameters: config.hyperparameters
      }
    });
    
    return model;
  }
  
  // モデルのデプロイメント
  async deployModel(
    model: TrainedModel,
    environment: Environment
  ): Promise<DeployedModel> {
    // モデルの最適化
    const optimized = await this.optimizeModel(model, {
      quantization: environment === 'edge',
      pruning: true,
      targetLatency: 100 // ms
    });
    
    // A/Bテストの設定
    const deployment = await this.setupABTest({
      model: optimized,
      trafficSplit: environment === 'production' ? 0.1 : 0.5,
      metrics: ['accuracy', 'latency', 'throughput'],
      duration: '7d'
    });
    
    // モニタリングの設定
    await this.setupMonitoring(deployment, {
      alerts: [
        {
          metric: 'accuracy',
          threshold: 0.9,
          comparison: 'less_than',
          action: 'rollback'
        },
        {
          metric: 'latency_p99',
          threshold: 150,
          comparison: 'greater_than',
          action: 'alert'
        }
      ]
    });
    
    return deployment;
  }
}
```

## クラウドネイティブ実装

<div id="cloud"></div>

### サーバーレス関数の実装

```typescript
import { APIGatewayProxyHandler } from 'aws-lambda';
import { DynamoDB } from 'aws-sdk';
import { SQS } from 'aws-sdk';

const dynamodb = new DynamoDB.DocumentClient();
const sqs = new SQS();

export const processOrder: APIGatewayProxyHandler = async (event) => {
  const order = JSON.parse(event.body!);
  
  try {
    // 1. 注文の検証
    await validateOrder(order);
    
    // 2. 在庫確認（並列実行）
    const inventoryChecks = order.items.map(item =>
      checkInventory(item.productId, item.quantity)
    );
    const inventoryResults = await Promise.all(inventoryChecks);
    
    // 3. 注文の保存
    await dynamodb.put({
      TableName: process.env.ORDERS_TABLE!,
      Item: {
        orderId: generateOrderId(),
        ...order,
        status: 'pending',
        createdAt: new Date().toISOString()
      }
    }).promise();
    
    // 4. 非同期処理のキューイング
    await sqs.sendMessage({
      QueueUrl: process.env.ORDER_QUEUE_URL!,
      MessageBody: JSON.stringify({
        orderId: order.orderId,
        type: 'process_payment'
      })
    }).promise();
    
    return {
      statusCode: 202,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        orderId: order.orderId,
        status: 'accepted',
        estimatedProcessingTime: '5-10 minutes'
      })
    };
  } catch (error) {
    console.error('Order processing failed:', error);
    
    return {
      statusCode: error.statusCode || 500,
      body: JSON.stringify({
        error: error.message || 'Internal server error'
      })
    };
  }
};
```

### Kubernetesオペレーター

```typescript
import { KubernetesObject } from '@kubernetes/client-node';

export class CustomResourceOperator {
  async reconcile(resource: CustomResource): Promise<void> {
    const desiredState = this.computeDesiredState(resource);
    const currentState = await this.getCurrentState(resource);
    
    // 差分を計算
    const diff = this.computeDiff(currentState, desiredState);
    
    // 必要なアクションを実行
    for (const action of diff.actions) {
      switch (action.type) {
        case 'create':
          await this.createResource(action.resource);
          break;
          
        case 'update':
          await this.updateResource(action.resource);
          break;
          
        case 'delete':
          await this.deleteResource(action.resourceName);
          break;
      }
    }
    
    // ステータスの更新
    await this.updateStatus(resource, {
      phase: 'Running',
      message: 'All resources reconciled',
      lastReconcileTime: new Date()
    });
  }
  
  private computeDesiredState(
    resource: CustomResource
  ): DesiredState {
    return {
      deployment: {
        apiVersion: 'apps/v1',
        kind: 'Deployment',
        metadata: {
          name: `${resource.metadata.name}-deployment`,
          namespace: resource.metadata.namespace
        },
        spec: {
          replicas: resource.spec.replicas,
          selector: {
            matchLabels: {
              app: resource.metadata.name
            }
          },
          template: {
            metadata: {
              labels: {
                app: resource.metadata.name
              }
            },
            spec: {
              containers: [{
                name: 'app',
                image: resource.spec.image,
                ports: [{
                  containerPort: resource.spec.port
                }],
                resources: resource.spec.resources
              }]
            }
          }
        }
      },
      
      service: {
        apiVersion: 'v1',
        kind: 'Service',
        metadata: {
          name: `${resource.metadata.name}-service`,
          namespace: resource.metadata.namespace
        },
        spec: {
          selector: {
            app: resource.metadata.name
          },
          ports: [{
            port: resource.spec.port,
            targetPort: resource.spec.port
          }]
        }
      },
      
      autoscaler: resource.spec.autoscaling ? {
        apiVersion: 'autoscaling/v2',
        kind: 'HorizontalPodAutoscaler',
        metadata: {
          name: `${resource.metadata.name}-hpa`,
          namespace: resource.metadata.namespace
        },
        spec: {
          scaleTargetRef: {
            apiVersion: 'apps/v1',
            kind: 'Deployment',
            name: `${resource.metadata.name}-deployment`
          },
          minReplicas: resource.spec.autoscaling.minReplicas,
          maxReplicas: resource.spec.autoscaling.maxReplicas,
          targetCPUUtilizationPercentage: 80
        }
      } : null
    };
  }
}
```

## IoT/ブロックチェーン統合

<div id="iot"></div>

### IoTデバイス管理

```typescript
export class IoTDeviceManager {
  private registry: DeviceRegistry;
  private mqttBroker: MQTTBroker;
  
  async provisionDevice(
    device: DeviceRegistration
  ): Promise<ProvisionedDevice> {
    // 1. デバイス証明書の生成
    const certificates = await this.generateCertificates({
      deviceId: device.id,
      publicKey: device.publicKey,
      validityPeriod: '365d'
    });
    
    // 2. デバイスの登録
    await this.registry.register({
      id: device.id,
      type: device.type,
      metadata: device.metadata,
      certificates: certificates.fingerprint
    });
    
    // 3. トピックの権限設定
    await this.mqttBroker.setPermissions(device.id, {
      publish: [
        `devices/${device.id}/telemetry`,
        `devices/${device.id}/state`
      ],
      subscribe: [
        `devices/${device.id}/commands`,
        `devices/${device.id}/config`
      ]
    });
    
    // 4. 初期設定の送信
    await this.sendInitialConfiguration(device.id, {
      telemetryInterval: 60000,
      commandTimeout: 5000,
      firmwareUpdateChannel: 'stable'
    });
    
    return {
      deviceId: device.id,
      certificates,
      endpoints: {
        mqtt: process.env.MQTT_ENDPOINT,
        http: process.env.HTTP_ENDPOINT
      },
      topics: {
        telemetry: `devices/${device.id}/telemetry`,
        commands: `devices/${device.id}/commands`
      }
    };
  }
  
  async handleTelemetry(
    deviceId: string,
    telemetry: DeviceTelemetry
  ): Promise<void> {
    // 1. データの検証
    this.validateTelemetry(telemetry);
    
    // 2. 時系列データベースへの保存
    await this.timeseries.write({
      measurement: 'device_telemetry',
      tags: {
        deviceId,
        deviceType: telemetry.deviceType,
        location: telemetry.location
      },
      fields: telemetry.data,
      timestamp: telemetry.timestamp
    });
    
    // 3. ルールエンジンの実行
    const rules = await this.getRulesForDevice(deviceId);
    for (const rule of rules) {
      if (rule.evaluate(telemetry)) {
        await this.executeAction(rule.action, {
          deviceId,
          telemetry,
          rule
        });
      }
    }
    
    // 4. デバイスツインの更新
    await this.updateDeviceTwin(deviceId, {
      reported: telemetry.data,
      metadata: {
        lastSeen: new Date(),
        firmwareVersion: telemetry.firmwareVersion
      }
    });
  }
}
```

### ブロックチェーン統合

```typescript
import Web3 from 'web3';
import { Contract } from 'web3-eth-contract';

export class BlockchainIntegration {
  private web3: Web3;
  private contracts: Map<string, Contract> = new Map();
  
  async deploySmartContract(
    contractDefinition: ContractDefinition
  ): Promise<DeployedContract> {
    // 1. コンパイル
    const compiled = await this.compiler.compile({
      source: contractDefinition.source,
      version: '0.8.19',
      optimizer: {
        enabled: true,
        runs: 200
      }
    });
    
    // 2. ガス推定
    const gasEstimate = await this.web3.eth.estimateGas({
      data: compiled.bytecode
    });
    
    // 3. デプロイトランザクションの作成
    const contract = new this.web3.eth.Contract(compiled.abi);
    const deployment = contract.deploy({
      data: compiled.bytecode,
      arguments: contractDefinition.constructorArgs
    });
    
    // 4. トランザクションの送信
    const receipt = await deployment.send({
      from: this.account,
      gas: Math.ceil(gasEstimate * 1.2),
      gasPrice: await this.getOptimalGasPrice()
    });
    
    // 5. コントラクトの登録
    this.contracts.set(
      contractDefinition.name,
      new this.web3.eth.Contract(
        compiled.abi,
        receipt.contractAddress
      )
    );
    
    return {
      address: receipt.contractAddress,
      transactionHash: receipt.transactionHash,
      abi: compiled.abi,
      blockNumber: receipt.blockNumber
    };
  }
  
  async interactWithContract(
    contractName: string,
    method: string,
    params: any[]
  ): Promise<any> {
    const contract = this.contracts.get(contractName);
    if (!contract) {
      throw new Error(`Contract ${contractName} not found`);
    }
    
    // 読み取り専用メソッドの場合
    if (this.isViewMethod(contract, method)) {
      return await contract.methods[method](...params).call();
    }
    
    // 状態変更メソッドの場合
    const gasEstimate = await contract.methods[method](...params)
      .estimateGas({ from: this.account });
    
    const receipt = await contract.methods[method](...params)
      .send({
        from: this.account,
        gas: Math.ceil(gasEstimate * 1.1),
        gasPrice: await this.getOptimalGasPrice()
      });
    
    return {
      transactionHash: receipt.transactionHash,
      blockNumber: receipt.blockNumber,
      gasUsed: receipt.gasUsed,
      events: receipt.events
    };
  }
}
```

### エッジコンピューティング

```typescript
export class EdgeComputing {
  // エッジでの機械学習推論
  async runInference(
    data: SensorData,
    modelName: string
  ): Promise<InferenceResult> {
    // 1. モデルのロード（キャッシュから）
    const model = await this.loadModel(modelName);
    
    // 2. 前処理
    const preprocessed = this.preprocess(data, model.preprocessing);
    
    // 3. 推論の実行
    const startTime = performance.now();
    const prediction = await model.predict(preprocessed);
    const inferenceTime = performance.now() - startTime;
    
    // 4. 後処理
    const result = this.postprocess(prediction, model.postprocessing);
    
    // 5. 結果のフィルタリング（重要なものだけクラウドへ）
    if (result.confidence > 0.9 || result.anomaly) {
      await this.sendToCloud({
        deviceId: data.deviceId,
        timestamp: data.timestamp,
        result,
        inferenceTime
      });
    }
    
    return result;
  }
  
  // モデルの更新
  async updateModel(
    modelName: string,
    newVersion: string
  ): Promise<void> {
    // 1. 新しいモデルのダウンロード
    const newModel = await this.downloadModel(modelName, newVersion);
    
    // 2. 検証
    const validation = await this.validateModel(newModel);
    if (!validation.passed) {
      throw new Error(`Model validation failed: ${validation.errors}`);
    }
    
    // 3. A/Bテスト
    await this.runABTest({
      oldModel: this.currentModels.get(modelName),
      newModel,
      duration: '1h',
      trafficSplit: 0.1
    });
    
    // 4. 段階的な切り替え
    await this.gradualRollout(modelName, newModel, {
      stages: [0.1, 0.25, 0.5, 1.0],
      interval: '15m',
      rollbackOnError: true
    });
  }
}
```