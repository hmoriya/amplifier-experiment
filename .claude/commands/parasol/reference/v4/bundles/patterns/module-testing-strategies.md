---
bundle:
  name: parasol-module-testing
  version: 1.0.0
  description: Testing strategies for modular BC architecture
  
includes:
  - bundle: ./bc-architecture-patterns.md
  
config:
  test_levels:
    - unit
    - integration
    - contract
    - e2e
    - performance
    - chaos
---

# Module Testing Strategies

モジュラーBCアーキテクチャのためのテスト戦略集です。

## テストピラミッドの再定義

```yaml
modular_test_pyramid:
  unit_tests: 40%
    scope: 単一モジュール内
    speed: <100ms
    isolation: complete
    
  module_tests: 30%
    scope: モジュール境界
    speed: <1s
    isolation: module_level
    
  contract_tests: 20%
    scope: モジュール間契約
    speed: <5s
    isolation: api_level
    
  e2e_tests: 10%
    scope: 全体フロー
    speed: <30s
    isolation: none
```

## 1. モジュール単体テスト

### ドメインロジックのテスト

```typescript
// modules/product/domain/__tests__/product.spec.ts
describe('Product Entity', () => {
  describe('changePrice', () => {
    it('価格変更時にイベントを生成する', () => {
      // Arrange
      const product = new Product(
        new ProductId('123'),
        new ProductName('テスト商品'),
        new Money(1000, 'JPY'),
        Category.ELECTRONICS
      );
      
      // Act
      const events = product.changePrice(new Money(1500, 'JPY'));
      
      // Assert
      expect(events).toHaveLength(1);
      expect(events[0]).toBeInstanceOf(ProductPriceChanged);
      expect(events[0].newPrice.amount).toBe(1500);
    });
    
    it('同じ価格への変更はイベントを生成しない', () => {
      const product = new Product(/* ... */);
      const events = product.changePrice(new Money(1000, 'JPY'));
      expect(events).toHaveLength(0);
    });
  });
});
```

### ユースケースのテスト

```typescript
// modules/product/application/__tests__/update-product-price.spec.ts
describe('UpdateProductPriceUseCase', () => {
  let useCase: UpdateProductPriceUseCase;
  let mockRepository: jest.Mocked<ProductRepository>;
  let mockEventBus: jest.Mocked<EventBus>;
  
  beforeEach(() => {
    mockRepository = createMockRepository();
    mockEventBus = createMockEventBus();
    useCase = new UpdateProductPriceUseCase(mockRepository, mockEventBus);
  });
  
  it('商品価格を更新し、イベントを発行する', async () => {
    // Arrange
    const product = createTestProduct({ price: 1000 });
    mockRepository.findById.mockResolvedValue(product);
    
    // Act
    await useCase.execute('123', 1500);
    
    // Assert
    expect(mockRepository.save).toHaveBeenCalledWith(
      expect.objectContaining({ price: new Money(1500, 'JPY') })
    );
    expect(mockEventBus.publishAll).toHaveBeenCalledWith([
      expect.objectContaining({ eventType: 'ProductPriceChanged' })
    ]);
  });
});
```

## 2. 契約テスト (Contract Testing)

### Consumer-Driven Contract Testing

```typescript
// modules/order/contracts/__tests__/product-service.contract.spec.ts
import { Pact } from '@pact-foundation/pact';

describe('Order Service → Product Service Contract', () => {
  const provider = new Pact({
    consumer: 'OrderService',
    provider: 'ProductService',
  });
  
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());
  
  describe('商品在庫確認', () => {
    it('在庫がある場合の応答', async () => {
      // 期待する相互作用を定義
      await provider.addInteraction({
        state: '商品ID:123の在庫が10個ある',
        uponReceiving: '在庫確認リクエスト',
        withRequest: {
          method: 'GET',
          path: '/products/123/availability',
        },
        willRespondWith: {
          status: 200,
          body: {
            productId: '123',
            available: true,
            quantity: 10,
          },
        },
      });
      
      // テスト実行
      await provider.executeTest(async (mockProvider) => {
        const client = new ProductServiceClient(mockProvider.url);
        const result = await client.checkAvailability('123');
        
        expect(result.available).toBe(true);
        expect(result.quantity).toBe(10);
      });
    });
  });
});
```

### Provider Contract Verification

```typescript
// modules/product/contracts/__tests__/provider-verification.spec.ts
import { Verifier } from '@pact-foundation/pact';

describe('Product Service Provider Verification', () => {
  it('Order Serviceとの契約を満たす', async () => {
    const verifier = new Verifier({
      provider: 'ProductService',
      providerBaseUrl: 'http://localhost:3001',
      pactUrls: ['./pacts/orderservice-productservice.json'],
      stateHandlers: {
        '商品ID:123の在庫が10個ある': async () => {
          await seedDatabase({
            products: [{ id: '123', stock: 10 }]
          });
        },
      },
    });
    
    await verifier.verifyProvider();
  });
});
```

## 3. モジュール間統合テスト

### テストハーネスを使った統合テスト

```typescript
// tests/integration/order-placement.spec.ts
describe('注文配置フロー統合テスト', () => {
  let testHarness: ModularTestHarness;
  
  beforeEach(async () => {
    testHarness = await ModularTestHarness.create({
      modules: ['order', 'product', 'inventory', 'payment'],
      communication: 'in-memory',
      database: 'test-containers',
    });
  });
  
  afterEach(async () => {
    await testHarness.cleanup();
  });
  
  it('正常な注文フローを完了する', async () => {
    // Arrange
    await testHarness.seed({
      products: [{ id: '123', stock: 10, price: 1000 }],
      customers: [{ id: '456', credit: 5000 }],
    });
    
    // Act
    const result = await testHarness.execute(
      new PlaceOrderCommand({
        customerId: '456',
        items: [{ productId: '123', quantity: 2 }],
      })
    );
    
    // Assert
    expect(result.success).toBe(true);
    
    // 各モジュールの状態を確認
    await testHarness.eventually({
      inventory: async () => {
        const stock = await testHarness.query('inventory', { productId: '123' });
        expect(stock.quantity).toBe(8);
      },
      payment: async () => {
        const balance = await testHarness.query('payment', { customerId: '456' });
        expect(balance.credit).toBe(3000);
      },
    });
  });
});
```

## 4. E2Eテスト戦略

### フロントエンドを含むE2Eテスト

```typescript
// tests/e2e/shopping-flow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('ショッピングフロー', () => {
  test('商品購入の完全なフロー', async ({ page }) => {
    // 1. 商品一覧表示
    await page.goto('/products');
    await expect(page.locator('[data-testid="product-grid"]')).toBeVisible();
    
    // 2. 商品詳細確認
    await page.click('[data-testid="product-123"]');
    await expect(page.locator('[data-testid="product-detail"]')).toContainText('テスト商品');
    
    // 3. カートに追加
    await page.click('[data-testid="add-to-cart"]');
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');
    
    // 4. チェックアウト
    await page.goto('/checkout');
    await page.fill('[data-testid="credit-card"]', '4242424242424242');
    await page.click('[data-testid="place-order"]');
    
    // 5. 注文確認
    await expect(page).toHaveURL(/\/orders\/\d+/);
    await expect(page.locator('[data-testid="order-status"]')).toHaveText('注文完了');
  });
});
```

### APIレベルE2Eテスト

```typescript
// tests/e2e/api-flow.spec.ts
describe('API E2E Flow', () => {
  it('GraphQL経由の注文フロー', async () => {
    const client = createTestClient();
    
    // 1. 商品検索
    const { data: products } = await client.query({
      query: GET_PRODUCTS,
      variables: { category: 'ELECTRONICS' }
    });
    
    // 2. カート作成
    const { data: cart } = await client.mutate({
      mutation: CREATE_CART,
      variables: {
        items: [{ productId: products[0].id, quantity: 2 }]
      }
    });
    
    // 3. 注文作成
    const { data: order } = await client.mutate({
      mutation: PLACE_ORDER,
      variables: {
        cartId: cart.id,
        payment: { method: 'CREDIT_CARD', token: 'test-token' }
      }
    });
    
    // 4. 注文状態確認（ポーリング）
    await waitFor(async () => {
      const { data } = await client.query({
        query: GET_ORDER_STATUS,
        variables: { orderId: order.id }
      });
      expect(data.order.status).toBe('CONFIRMED');
    });
  });
});
```

## 5. パフォーマンステスト

### 負荷テスト

```typescript
// tests/performance/load-test.ts
import { check } from 'k6';
import http from 'k6/http';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // ランプアップ
    { duration: '5m', target: 100 }, // 維持
    { duration: '2m', target: 0 },   // ランプダウン
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95%が500ms以内
    http_req_failed: ['rate<0.1'],    // エラー率10%未満
  },
};

export default function() {
  // 商品一覧取得
  const productsRes = http.get('http://api/products');
  check(productsRes, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  
  // 注文作成
  const orderRes = http.post('http://api/orders', JSON.stringify({
    items: [{ productId: '123', quantity: 1 }]
  }), {
    headers: { 'Content-Type': 'application/json' }
  });
  check(orderRes, {
    'order created': (r) => r.status === 201,
  });
}
```

## 6. カオステスト

### Chaos Engineering

```yaml
# chaos/experiments/network-latency.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: product-service-latency
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - default
    labelSelectors:
      app: product-service
  delay:
    latency: "300ms"
    correlation: "25"
    jitter: "50ms"
  duration: "5m"
```

### カオステストの実装

```typescript
// tests/chaos/resilience.spec.ts
describe('システムレジリエンステスト', () => {
  it('ProductServiceダウン時も注文を受け付ける', async () => {
    // ProductServiceを停止
    await chaosMonkey.kill('product-service');
    
    // 注文は受け付けられるべき（後で処理）
    const result = await orderService.placeOrder({
      customerId: '123',
      items: [{ productId: '456', quantity: 1 }]
    });
    
    expect(result.status).toBe('PENDING_VALIDATION');
    
    // ProductService復旧後に処理される
    await chaosMonkey.restore('product-service');
    await eventually(() => {
      const order = await orderService.getOrder(result.orderId);
      expect(order.status).toBe('CONFIRMED');
    });
  });
});
```

## テスト自動化パイプライン

```yaml
# .github/workflows/modular-testing.yml
name: Modular Testing Pipeline

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        module: [product, order, inventory, payment]
    steps:
      - uses: actions/checkout@v3
      - name: Run Unit Tests
        run: |
          cd modules/${{ matrix.module }}
          npm test
          
  contract-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      - name: Run Contract Tests
        run: npm run test:contracts
      - name: Publish Pacts
        run: npm run pact:publish
        
  integration-tests:
    needs: contract-tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
      redis:
        image: redis:7
    steps:
      - name: Run Integration Tests
        run: npm run test:integration
        
  e2e-tests:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Test Environment
        run: |
          docker-compose up -d
          npm run wait-for-services
      - name: Run E2E Tests
        run: npm run test:e2e
```

## CLI統合

```bash
# モジュール単体テスト実行
parasol bc test ProductManagement \
  --module product \
  --level unit

# 契約テスト生成と実行
parasol bc generate-contract-tests ProductManagement \
  --consumer order \
  --provider product

# 統合テストハーネス実行
parasol bc test-integration ProductManagement \
  --modules product,order,inventory \
  --scenario order-placement

# カオステスト実行
parasol bc chaos-test ProductManagement \
  --experiment kill-random-module \
  --duration 5m \
  --assert system-remains-operational
```