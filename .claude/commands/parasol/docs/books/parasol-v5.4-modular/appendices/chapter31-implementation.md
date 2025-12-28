# 付録：第31章　APIコントラクトとバージョニングの実装詳細

## OpenAPI仕様の完全な例

```yaml
openapi: 3.1.0
info:
  title: Parasol V5.4 Order Management API
  version: 1.0.0
  description: |
    注文管理システムのREST API。
    このAPIは、ECサイトの注文処理に関するすべての操作を提供します。
  contact:
    name: API Support Team
    email: api-support@parasol.com
    url: https://developer.parasol.com/support
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html
  x-api-lifecycle:
    maturity: stable
    deprecation-policy: https://developer.parasol.com/deprecation-policy

servers:
  - url: https://api.parasol.com/v1
    description: Production server
  - url: https://api-staging.parasol.com/v1
    description: Staging server
  - url: https://api-sandbox.parasol.com/v1
    description: Sandbox for testing

tags:
  - name: Orders
    description: 注文管理に関する操作
  - name: Items
    description: 注文項目の操作
  - name: Customers
    description: 顧客情報の操作

paths:
  /orders:
    get:
      operationId: listOrders
      tags: [Orders]
      summary: 注文一覧の取得
      description: |
        指定された条件に基づいて注文の一覧を取得します。
        デフォルトでは最新20件の注文を返します。
      parameters:
        - $ref: '#/components/parameters/CustomerIdParam'
        - $ref: '#/components/parameters/StatusParam'
        - $ref: '#/components/parameters/DateFromParam'
        - $ref: '#/components/parameters/DateToParam'
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
        - $ref: '#/components/parameters/SortParam'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'
              examples:
                success:
                  $ref: '#/components/examples/OrderListExample'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '500':
          $ref: '#/components/responses/InternalServerError'
      security:
        - bearerAuth: []
        - apiKey: []
      x-rate-limit:
        requests: 100
        window: 1m
    
    post:
      operationId: createOrder
      tags: [Orders]
      summary: 新規注文の作成
      description: 新しい注文を作成し、注文処理を開始します。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              basic:
                $ref: '#/components/examples/CreateOrderExample'
      responses:
        '201':
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
          headers:
            Location:
              description: 作成された注文のURI
              schema:
                type: string
                example: /orders/550e8400-e29b-41d4-a716-446655440000
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'
      callbacks:
        statusUpdate:
          '{$request.body#/callbackUrl}':
            post:
              requestBody:
                required: true
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/OrderStatusUpdate'
              responses:
                '200':
                  description: 通知を受信しました

  /orders/{orderId}:
    parameters:
      - $ref: '#/components/parameters/OrderIdParam'
    
    get:
      operationId: getOrder
      tags: [Orders]
      summary: 注文詳細の取得
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '404':
          $ref: '#/components/responses/NotFound'
    
    patch:
      operationId: updateOrder
      tags: [Orders]
      summary: 注文の部分更新
      description: |
        注文の一部フィールドを更新します。
        JSON Patchフォーマットをサポートします。
      requestBody:
        required: true
        content:
          application/json-patch+json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/PatchOperation'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'
    
    delete:
      operationId: cancelOrder
      tags: [Orders]
      summary: 注文のキャンセル
      description: |
        注文をキャンセルします。
        キャンセル可能な状態でない場合はエラーを返します。
      responses:
        '204':
          description: キャンセル成功
        '400':
          description: キャンセル不可
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetail'

components:
  schemas:
    Order:
      type: object
      required: [id, customerId, items, total, status, createdAt]
      properties:
        id:
          type: string
          format: uuid
          description: 注文ID
          readOnly: true
          example: 550e8400-e29b-41d4-a716-446655440000
        customerId:
          type: string
          description: 顧客ID
          example: cust_123456
        items:
          type: array
          minItems: 1
          items:
            $ref: '#/components/schemas/OrderItem'
        subtotal:
          $ref: '#/components/schemas/Money'
        tax:
          $ref: '#/components/schemas/Money'
        shipping:
          $ref: '#/components/schemas/Money'
        total:
          $ref: '#/components/schemas/Money'
        status:
          $ref: '#/components/schemas/OrderStatus'
        shippingAddress:
          $ref: '#/components/schemas/Address'
        billingAddress:
          $ref: '#/components/schemas/Address'
        paymentMethod:
          $ref: '#/components/schemas/PaymentMethod'
        notes:
          type: string
          maxLength: 500
          description: 注文に関するメモ
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
        version:
          type: integer
          description: 楽観的ロック用のバージョン番号
          readOnly: true
      
    OrderItem:
      type: object
      required: [productId, productName, quantity, unitPrice]
      properties:
        productId:
          type: string
          description: 商品ID
        productName:
          type: string
          description: 商品名
        quantity:
          type: integer
          minimum: 1
          description: 数量
        unitPrice:
          $ref: '#/components/schemas/Money'
        discount:
          $ref: '#/components/schemas/Money'
        subtotal:
          $ref: '#/components/schemas/Money'
          readOnly: true
    
    Money:
      type: object
      required: [amount, currency]
      properties:
        amount:
          type: number
          format: double
          minimum: 0
          description: 金額
          example: 1234.56
        currency:
          type: string
          pattern: ^[A-Z]{3}$
          description: ISO 4217通貨コード
          example: JPY
    
    OrderStatus:
      type: string
      enum:
        - pending
        - confirmed
        - processing
        - shipped
        - delivered
        - cancelled
      x-enum-descriptions:
        pending: 注文確定待ち
        confirmed: 注文確定済み
        processing: 処理中
        shipped: 発送済み
        delivered: 配送済み
        cancelled: キャンセル済み
    
    Address:
      type: object
      required: [name, postalCode, prefecture, city, street]
      properties:
        name:
          type: string
          description: 宛名
        postalCode:
          type: string
          pattern: ^\d{3}-\d{4}$
          description: 郵便番号
        prefecture:
          type: string
          description: 都道府県
        city:
          type: string
          description: 市区町村
        street:
          type: string
          description: 番地
        building:
          type: string
          description: 建物名・部屋番号
        phone:
          type: string
          description: 電話番号
    
    ProblemDetail:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
          description: 問題タイプを識別するURI
        title:
          type: string
          description: 問題の短い要約
        status:
          type: integer
          description: HTTPステータスコード
        detail:
          type: string
          description: 問題の詳細な説明
        instance:
          type: string
          format: uri
          description: 問題の具体的なインスタンスを識別するURI
        errors:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
    
  responses:
    BadRequest:
      description: リクエストが不正です
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'
    
    Unauthorized:
      description: 認証が必要です
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'
    
    NotFound:
      description: リソースが見つかりません
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'
    
    InternalServerError:
      description: サーバー内部エラー
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'
  
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT形式のアクセストークン
    
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: APIキーによる認証
    
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.parasol.com/oauth/authorize
          tokenUrl: https://auth.parasol.com/oauth/token
          scopes:
            read:orders: 注文の読み取り
            write:orders: 注文の作成・更新
            delete:orders: 注文の削除

security:
  - bearerAuth: []
  - apiKey: []
  - oauth2: [read:orders]
```

## バージョニング戦略の実装

<div id="versioning"></div>

```typescript
export class APIVersioningImplementation {
  // セマンティックバージョニングの実装
  implementSemanticVersioning(): VersioningSystem {
    return {
      // バージョン管理クラス
      versionManager: `
        class SemanticVersion {
          constructor(
            public readonly major: number,
            public readonly minor: number,
            public readonly patch: number,
            public readonly preRelease?: string,
            public readonly metadata?: string
          ) {}
          
          static parse(version: string): SemanticVersion {
            const pattern = /^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$/;
            const match = version.match(pattern);
            
            if (!match) {
              throw new Error(\`Invalid version format: \${version}\`);
            }
            
            return new SemanticVersion(
              parseInt(match[1]),
              parseInt(match[2]),
              parseInt(match[3]),
              match[4],
              match[5]
            );
          }
          
          toString(): string {
            let version = \`\${this.major}.\${this.minor}.\${this.patch}\`;
            if (this.preRelease) version += \`-\${this.preRelease}\`;
            if (this.metadata) version += \`+\${this.metadata}\`;
            return version;
          }
          
          isCompatibleWith(other: SemanticVersion): boolean {
            // 同じメジャーバージョンなら互換性あり
            if (this.major !== other.major) return false;
            
            // マイナーバージョンが上位なら互換性あり
            if (this.minor < other.minor) return false;
            
            // パッチバージョンは常に互換性あり
            return true;
          }
          
          compareTo(other: SemanticVersion): number {
            if (this.major !== other.major) {
              return this.major - other.major;
            }
            if (this.minor !== other.minor) {
              return this.minor - other.minor;
            }
            if (this.patch !== other.patch) {
              return this.patch - other.patch;
            }
            
            // プレリリース版の比較
            if (this.preRelease && !other.preRelease) return -1;
            if (!this.preRelease && other.preRelease) return 1;
            if (this.preRelease && other.preRelease) {
              return this.preRelease.localeCompare(other.preRelease);
            }
            
            return 0;
          }
        }
      `,
      
      // バージョンネゴシエーション
      negotiation: `
        class VersionNegotiator {
          private supportedVersions: Map<string, VersionHandler>;
          
          constructor() {
            this.supportedVersions = new Map([
              ['1.0', new V1Handler()],
              ['1.1', new V1_1Handler()],
              ['2.0', new V2Handler()]
            ]);
          }
          
          negotiateVersion(request: Request): VersionHandler {
            const requestedVersion = this.extractVersion(request);
            
            // 完全一致を試みる
            if (this.supportedVersions.has(requestedVersion)) {
              return this.supportedVersions.get(requestedVersion)!;
            }
            
            // セマンティックバージョニングによる互換性チェック
            const requested = SemanticVersion.parse(requestedVersion);
            const compatible = this.findCompatibleVersion(requested);
            
            if (compatible) {
              return compatible;
            }
            
            // デフォルトバージョンを返す
            return this.getDefaultVersion();
          }
          
          private extractVersion(request: Request): string {
            // 1. URLパスから抽出
            const pathMatch = request.path.match(/^\/api\/v(\d+(?:\.\d+)?)/);
            if (pathMatch) {
              return pathMatch[1];
            }
            
            // 2. Acceptヘッダーから抽出
            const accept = request.headers['accept'];
            if (accept) {
              const versionMatch = accept.match(/application\/vnd\.parasol\.v(\d+(?:\.\d+)?)\+json/);
              if (versionMatch) {
                return versionMatch[1];
              }
            }
            
            // 3. カスタムヘッダーから抽出
            const apiVersion = request.headers['x-api-version'];
            if (apiVersion) {
              return apiVersion;
            }
            
            // 4. クエリパラメータから抽出
            const queryVersion = request.query['api-version'];
            if (queryVersion) {
              return queryVersion;
            }
            
            // デフォルトバージョンを返す
            return this.config.defaultVersion;
          }
          
          private findCompatibleVersion(
            requested: SemanticVersion
          ): VersionHandler | null {
            let bestMatch: { version: SemanticVersion; handler: VersionHandler } | null = null;
            
            for (const [versionStr, handler] of this.supportedVersions) {
              const version = SemanticVersion.parse(versionStr);
              
              if (version.isCompatibleWith(requested)) {
                if (!bestMatch || version.compareTo(bestMatch.version) > 0) {
                  bestMatch = { version, handler };
                }
              }
            }
            
            return bestMatch?.handler || null;
          }
        }
      `,
      
      // バージョン別ハンドラー
      handlers: `
        abstract class VersionHandler {
          abstract getVersion(): string;
          abstract handleRequest(req: Request, res: Response): Promise<void>;
          
          // 共通の処理
          protected async processOrder(orderId: string): Promise<Order> {
            const order = await this.orderRepository.findById(orderId);
            if (!order) {
              throw new NotFoundError('Order not found');
            }
            return order;
          }
          
          // バージョン固有の変換
          protected abstract transformResponse(data: any): any;
        }
        
        class V1Handler extends VersionHandler {
          getVersion(): string {
            return '1.0';
          }
          
          async handleRequest(req: Request, res: Response): Promise<void> {
            const order = await this.processOrder(req.params.orderId);
            const response = this.transformResponse(order);
            res.json(response);
          }
          
          protected transformResponse(order: Order): any {
            return {
              id: order.id,
              customerId: order.customerId,
              items: order.items.map(item => ({
                productId: item.productId,
                quantity: item.quantity,
                price: item.price
              })),
              total: order.total,
              status: order.status,
              createdAt: order.createdAt.toISOString()
            };
          }
        }
        
        class V2Handler extends VersionHandler {
          getVersion(): string {
            return '2.0';
          }
          
          protected transformResponse(order: Order): any {
            // V2では追加フィールドを含む
            return {
              id: order.id,
              customerId: order.customerId,
              customerName: order.customer?.name, // 新規追加
              items: order.items.map(item => ({
                productId: item.productId,
                productName: item.product?.name, // 新規追加
                quantity: item.quantity,
                unitPrice: item.price, // 名称変更
                subtotal: item.quantity * item.price // 新規追加
              })),
              subtotal: order.subtotal, // 新規追加
              tax: order.tax, // 新規追加
              shipping: order.shipping, // 新規追加
              total: order.total,
              status: order.status,
              statusHistory: order.statusHistory, // 新規追加
              shippingAddress: order.shippingAddress, // 新規追加
              billingAddress: order.billingAddress, // 新規追加
              createdAt: order.createdAt.toISOString(),
              updatedAt: order.updatedAt.toISOString() // 新規追加
            };
          }
        }
      `,
      
      // 互換性維持レイヤー
      compatibility: `
        class CompatibilityLayer {
          // レスポンス変換
          transformResponseForVersion(
            data: any,
            fromVersion: string,
            toVersion: string
          ): any {
            const transformer = this.getTransformer(fromVersion, toVersion);
            return transformer ? transformer(data) : data;
          }
          
          // リクエスト変換
          transformRequestForVersion(
            data: any,
            fromVersion: string,
            toVersion: string
          ): any {
            // 古いバージョンのリクエストを新しいバージョンに変換
            if (fromVersion === '1.0' && toVersion === '2.0') {
              return {
                ...data,
                // デフォルト値を追加
                shippingAddress: data.address || null,
                billingAddress: data.address || null,
                paymentMethod: data.paymentMethod || 'credit_card'
              };
            }
            
            return data;
          }
          
          // 廃止予定フィールドの処理
          handleDeprecatedFields(
            data: any,
            version: string
          ): any {
            const deprecations = this.getDeprecations(version);
            const result = { ...data };
            
            for (const dep of deprecations) {
              if (dep.removeInVersion && version >= dep.removeInVersion) {
                delete result[dep.field];
              } else if (result[dep.field] !== undefined) {
                // 警告を追加
                result._warnings = result._warnings || [];
                result._warnings.push({
                  field: dep.field,
                  message: dep.message,
                  deprecatedSince: dep.since,
                  removeIn: dep.removeInVersion
                });
              }
            }
            
            return result;
          }
        }
      `
    };
  }
}
```

## 移行支援ツールの実装

<div id="migration"></div>

```typescript
export class MigrationToolsImplementation {
  // クライアント移行ツール
  implementMigrationTools(): MigrationToolkit {
    return {
      // コード分析ツール
      codeAnalyzer: `
        class APIUsageAnalyzer {
          async analyzeCodebase(
            directory: string,
            options: AnalysisOptions
          ): Promise<AnalysisReport> {
            const files = await this.findSourceFiles(directory, options);
            const usages: APIUsage[] = [];
            
            for (const file of files) {
              const content = await fs.readFile(file, 'utf-8');
              const fileUsages = this.analyzeFile(file, content);
              usages.push(...fileUsages);
            }
            
            return {
              totalFiles: files.length,
              apiUsages: usages,
              summary: this.generateSummary(usages),
              recommendations: this.generateRecommendations(usages)
            };
          }
          
          private analyzeFile(filePath: string, content: string): APIUsage[] {
            const usages: APIUsage[] = [];
            
            // APIエンドポイントの検出
            const endpointPattern = /['"]\/api\/v\d+\/[^'"]+['"]/g;
            let match;
            
            while ((match = endpointPattern.exec(content)) !== null) {
              const endpoint = match[0].slice(1, -1);
              const line = content.substring(0, match.index).split('\n').length;
              
              usages.push({
                file: filePath,
                line,
                type: 'endpoint',
                value: endpoint,
                version: this.extractVersionFromEndpoint(endpoint)
              });
            }
            
            // HTTPメソッドの検出
            const methodPattern = /\.(get|post|put|patch|delete)\s*\(/g;
            while ((match = methodPattern.exec(content)) !== null) {
              const method = match[1];
              const line = content.substring(0, match.index).split('\n').length;
              
              usages.push({
                file: filePath,
                line,
                type: 'method',
                value: method.toUpperCase()
              });
            }
            
            // レスポンス処理の検出
            const responsePattern = /\.then\s*\(\s*(?:response|res|r)\s*=>/g;
            while ((match = responsePattern.exec(content)) !== null) {
              const line = content.substring(0, match.index).split('\n').length;
              
              // レスポンス内のフィールドアクセスを検出
              const responseBlock = this.extractCodeBlock(content, match.index);
              const fieldAccesses = this.analyzeFieldAccesses(responseBlock);
              
              for (const field of fieldAccesses) {
                usages.push({
                  file: filePath,
                  line,
                  type: 'field',
                  value: field
                });
              }
            }
            
            return usages;
          }
          
          private generateRecommendations(usages: APIUsage[]): Recommendation[] {
            const recommendations: Recommendation[] = [];
            
            // 古いバージョンの使用を検出
            const oldVersionUsages = usages.filter(u => 
              u.version && this.isOldVersion(u.version)
            );
            
            if (oldVersionUsages.length > 0) {
              recommendations.push({
                severity: 'high',
                title: '古いAPIバージョンの使用',
                description: \`\${oldVersionUsages.length}箇所で古いAPIバージョンを使用しています\`,
                files: [...new Set(oldVersionUsages.map(u => u.file))],
                action: 'バージョン移行ツールを実行してください'
              });
            }
            
            // 廃止予定フィールドの使用を検出
            const deprecatedFields = usages.filter(u => 
              u.type === 'field' && this.isDeprecatedField(u.value)
            );
            
            if (deprecatedFields.length > 0) {
              recommendations.push({
                severity: 'medium',
                title: '廃止予定フィールドの使用',
                description: \`\${deprecatedFields.length}箇所で廃止予定のフィールドを使用しています\`,
                fields: [...new Set(deprecatedFields.map(u => u.value))],
                action: '代替フィールドへの移行を検討してください'
              });
            }
            
            return recommendations;
          }
        }
      `,
      
      // 自動マイグレーション
      migrationScript: `
        class AutoMigration {
          async migrateCodebase(
            directory: string,
            fromVersion: string,
            toVersion: string,
            options: MigrationOptions = {}
          ): Promise<MigrationResult> {
            // 1. コードベースを分析
            const analysis = await this.analyzer.analyzeCodebase(directory, {
              fileTypes: options.fileTypes || ['js', 'ts', 'jsx', 'tsx']
            });
            
            // 2. 移行ルールを取得
            const rules = this.getMigrationRules(fromVersion, toVersion);
            
            // 3. 各ファイルに対して移行を実行
            const results: FileModification[] = [];
            
            for (const usage of analysis.apiUsages) {
              const rule = rules.find(r => r.matches(usage));
              if (rule) {
                const modification = await this.applyRule(usage, rule);
                if (modification) {
                  results.push(modification);
                }
              }
            }
            
            // 4. ドライランモードの場合は変更を適用しない
            if (!options.dryRun) {
              await this.applyModifications(results);
            }
            
            return {
              analysisReport: analysis,
              modifications: results,
              summary: this.generateMigrationSummary(results)
            };
          }
          
          private getMigrationRules(
            fromVersion: string,
            toVersion: string
          ): MigrationRule[] {
            const rules: MigrationRule[] = [];
            
            if (fromVersion === '1.0' && toVersion === '2.0') {
              rules.push(
                // エンドポイントの変更
                {
                  name: 'Update endpoint paths',
                  matches: (usage) => 
                    usage.type === 'endpoint' && 
                    usage.value.includes('/customer/'),
                  transform: (code) => 
                    code.replace(/\/customer\/(\w+)\/orders/g, '/orders?customerId=$1')
                },
                
                // フィールド名の変更
                {
                  name: 'Rename price to unitPrice',
                  matches: (usage) => 
                    usage.type === 'field' && 
                    usage.value === 'price',
                  transform: (code) => 
                    code.replace(/\.price\b/g, '.unitPrice')
                },
                
                // 新しい必須フィールドの追加
                {
                  name: 'Add required fields',
                  matches: (usage) => 
                    usage.type === 'method' && 
                    usage.value === 'POST' &&
                    usage.endpoint?.includes('/orders'),
                  transform: (code) => {
                    // リクエストボディに必須フィールドを追加
                    return code.replace(
                      /const\s+orderData\s*=\s*{([^}]+)}/,
                      (match, body) => {
                        if (!body.includes('paymentMethod')) {
                          body += ",\n  paymentMethod: 'credit_card'";
                        }
                        return \`const orderData = {\${body}}\`;
                      }
                    );
                  }
                }
              );
            }
            
            return rules;
          }
          
          private async applyModifications(
            modifications: FileModification[]
          ): Promise<void> {
            // ファイルごとにグループ化
            const fileGroups = this.groupByFile(modifications);
            
            for (const [filePath, mods] of fileGroups) {
              // バックアップを作成
              await this.createBackup(filePath);
              
              // ファイルの内容を読み込む
              let content = await fs.readFile(filePath, 'utf-8');
              
              // すべての変更を適用
              for (const mod of mods) {
                content = mod.transform(content);
              }
              
              // ファイルに書き戻す
              await fs.writeFile(filePath, content);
              
              // 変更をログに記録
              this.logger.info(\`Modified: \${filePath} (\${mods.length} changes)\`);
            }
          }
        }
      `,
      
      // 移行バリデーション
      validation: `
        class MigrationValidator {
          async validateMigration(
            directory: string,
            targetVersion: string
          ): Promise<ValidationResult> {
            const errors: ValidationError[] = [];
            const warnings: ValidationWarning[] = [];
            
            // 1. 静的解析
            const staticErrors = await this.performStaticAnalysis(
              directory,
              targetVersion
            );
            errors.push(...staticErrors);
            
            // 2. 型チェック
            if (this.isTypeScriptProject(directory)) {
              const typeErrors = await this.runTypeCheck(directory);
              errors.push(...typeErrors);
            }
            
            // 3. テストの実行
            const testResults = await this.runTests(directory);
            if (!testResults.success) {
              errors.push({
                type: 'test_failure',
                message: \`\${testResults.failed} tests failed\`,
                details: testResults.failures
              });
            }
            
            // 4. APIコントラクトの検証
            const contractViolations = await this.validateContracts(
              directory,
              targetVersion
            );
            errors.push(...contractViolations);
            
            // 5. 廃止予定機能の使用チェック
            const deprecations = await this.checkDeprecations(
              directory,
              targetVersion
            );
            warnings.push(...deprecations.map(d => ({
              type: 'deprecation',
              message: \`Using deprecated feature: \${d.feature}\`,
              location: d.location,
              suggestion: d.alternative
            })));
            
            return {
              valid: errors.length === 0,
              errors,
              warnings,
              summary: {
                totalErrors: errors.length,
                totalWarnings: warnings.length,
                readyForMigration: errors.length === 0
              }
            };
          }
          
          private async validateContracts(
            directory: string,
            version: string
          ): Promise<ValidationError[]> {
            const errors: ValidationError[] = [];
            const contracts = await this.loadContracts(version);
            
            // リクエストの検証
            const requests = await this.findAPIRequests(directory);
            for (const req of requests) {
              const contract = contracts.find(c => c.matches(req));
              if (contract) {
                const validation = contract.validateRequest(req.payload);
                if (!validation.valid) {
                  errors.push({
                    type: 'contract_violation',
                    message: \`Invalid request for \${req.endpoint}\`,
                    details: validation.errors
                  });
                }
              }
            }
            
            return errors;
          }
        }
      `,
      
      // 移行ガイド生成
      documentationGenerator: `
        class MigrationGuideGenerator {
          async generateGuide(
            fromVersion: string,
            toVersion: string,
            analysis: AnalysisReport
          ): Promise<string> {
            const guide = [];
            
            guide.push(\`# API Migration Guide: v\${fromVersion} → v\${toVersion}\`);
            guide.push('');
            guide.push('## Overview');
            guide.push(\`This guide helps you migrate from API v\${fromVersion} to v\${toVersion}.\`);
            guide.push('');
            
            // 変更サマリー
            guide.push('## Change Summary');
            const changes = this.getVersionChanges(fromVersion, toVersion);
            for (const change of changes) {
              guide.push(\`- \${change.type}: \${change.description}\`);
            }
            guide.push('');
            
            // 影響を受けるコード
            guide.push('## Affected Code');
            guide.push(\`Total files affected: \${analysis.affectedFiles.length}\`);
            guide.push(\`Total changes required: \${analysis.totalChanges}\`);
            guide.push('');
            
            // 詳細な移行手順
            guide.push('## Migration Steps');
            guide.push('');
            
            const steps = this.getMigrationSteps(fromVersion, toVersion);
            steps.forEach((step, index) => {
              guide.push(\`### Step \${index + 1}: \${step.title}\`);
              guide.push('');
              guide.push(step.description);
              guide.push('');
              
              if (step.before && step.after) {
                guide.push('**Before:**');
                guide.push('\`\`\`javascript');
                guide.push(step.before);
                guide.push('\`\`\`');
                guide.push('');
                guide.push('**After:**');
                guide.push('\`\`\`javascript');
                guide.push(step.after);
                guide.push('\`\`\`');
                guide.push('');
              }
              
              if (step.automated) {
                guide.push('✅ This change can be automated using the migration tool.');
              } else {
                guide.push('⚠️ This change requires manual intervention.');
              }
              guide.push('');
            });
            
            // テストガイド
            guide.push('## Testing Your Migration');
            guide.push('');
            guide.push('1. Run the validation tool:');
            guide.push('   \`\`\`bash');
            guide.push('   npm run validate-migration -- --version=2.0');
            guide.push('   \`\`\`');
            guide.push('');
            guide.push('2. Run your test suite:');
            guide.push('   \`\`\`bash');
            guide.push('   npm test');
            guide.push('   \`\`\`');
            guide.push('');
            guide.push('3. Test critical user flows manually');
            guide.push('');
            
            // トラブルシューティング
            guide.push('## Troubleshooting');
            guide.push('');
            
            const issues = this.getCommonIssues(fromVersion, toVersion);
            for (const issue of issues) {
              guide.push(\`### \${issue.title}\`);
              guide.push('');
              guide.push('**Problem:**');
              guide.push(issue.problem);
              guide.push('');
              guide.push('**Solution:**');
              guide.push(issue.solution);
              guide.push('');
            }
            
            return guide.join('\n');
          }
        }
      `
    };
  }
}
```