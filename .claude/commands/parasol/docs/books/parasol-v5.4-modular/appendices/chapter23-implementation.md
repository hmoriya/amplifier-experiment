# Appendix: Chapter 23 Implementation Examples

This appendix contains detailed code examples and implementation patterns referenced in Chapter 23: Testing Strategies.

## A. Testing Strategy Configuration

### Test Pyramid Implementation

```typescript
export interface TestPyramid {
  // Unit Tests (60%)
  unit: {
    purpose: "Verify individual component correctness";
    characteristics: ["Fast", "Independent", "Deterministic", "Numerous"];
    scope: "Classes, functions, modules";
  };
  
  // Integration Tests (30%)
  integration: {
    purpose: "Verify component collaboration";
    characteristics: ["Medium speed", "Partial dependencies", "Environment setup required"];
    scope: "API, database, external service integration";
  };
  
  // E2E Tests (10%)
  e2e: {
    purpose: "Verify complete system from user perspective";
    characteristics: ["Slow", "Environment dependent", "Fragile"];
    scope: "User stories, business scenarios";
  };
}

export class TestingStrategy {
  designStrategy(context: ProjectContext): TestStrategy {
    return {
      // Level-specific strategies
      levels: {
        unit: this.defineUnitTestStrategy(context),
        integration: this.defineIntegrationTestStrategy(context),
        e2e: this.defineE2ETestStrategy(context),
        contract: this.defineContractTestStrategy(context),
        performance: this.definePerformanceTestStrategy(context)
      },
      
      // Quality gates
      qualityGates: {
        coverage: {
          unit: 80,
          integration: 60,
          overall: 75
        },
        performance: {
          p95ResponseTime: 200,
          throughput: 1000
        },
        reliability: {
          successRate: 99.9
        }
      },
      
      // Automation strategy
      automation: {
        ci: this.defineCIStrategy(context),
        preCommitHooks: this.definePreCommitHooks(context),
        scheduledTests: this.defineScheduledTests(context)
      }
    };
  }
}
```

## B. Unit Testing Examples

### Domain Logic Testing

```typescript
// Test target: Order aggregate
describe('Order Aggregate', () => {
  describe('Order Creation', () => {
    it('should create a valid order with initial status', () => {
      // Arrange
      const customerId = CustomerId.generate();
      const shippingAddress = Address.create({
        street: '123 Main St',
        city: 'Tokyo',
        postalCode: '100-0001'
      });
      
      // Act
      const order = Order.create({
        customerId,
        shippingAddress
      });
      
      // Assert
      expect(order.getStatus()).toBe(OrderStatus.DRAFT);
      expect(order.getCustomerId()).toEqual(customerId);
      expect(order.getUncommittedEvents()).toHaveLength(1);
      expect(order.getUncommittedEvents()[0]).toBeInstanceOf(OrderCreatedEvent);
    });
    
    it('should fail when shipping address is invalid', () => {
      // Arrange
      const customerId = CustomerId.generate();
      
      // Act & Assert
      expect(() => {
        Order.create({
          customerId,
          shippingAddress: null as any
        });
      }).toThrow('Shipping address is required');
    });
  });
  
  describe('Adding Items', () => {
    let order: Order;
    
    beforeEach(() => {
      order = Order.create({
        customerId: CustomerId.generate(),
        shippingAddress: createValidAddress()
      });
    });
    
    it('should add item to draft order', () => {
      // Arrange
      const productId = ProductId.generate();
      const quantity = 2;
      const price = Money.create(1000, 'JPY');
      
      // Act
      order.addItem(productId, quantity, price);
      
      // Assert
      expect(order.getItems()).toHaveLength(1);
      expect(order.getItems()[0].getQuantity()).toBe(quantity);
      expect(order.getTotal()).toEqual(Money.create(2000, 'JPY'));
    });
    
    it('should not allow adding items to confirmed order', () => {
      // Arrange
      order.addItem(ProductId.generate(), 1, Money.create(1000, 'JPY'));
      order.confirm();
      
      // Act & Assert
      expect(() => {
        order.addItem(ProductId.generate(), 1, Money.create(500, 'JPY'));
      }).toThrow('Cannot modify confirmed order');
    });
    
    it('should update quantity when adding same product', () => {
      // Arrange
      const productId = ProductId.generate();
      const price = Money.create(1000, 'JPY');
      
      // Act
      order.addItem(productId, 2, price);
      order.addItem(productId, 3, price);
      
      // Assert
      expect(order.getItems()).toHaveLength(1);
      expect(order.getItems()[0].getQuantity()).toBe(5);
      expect(order.getTotal()).toEqual(Money.create(5000, 'JPY'));
    });
  });
  
  describe('Order Confirmation', () => {
    it('should confirm order with valid items', () => {
      // Arrange
      const order = createOrderWithItems();
      
      // Act
      order.confirm();
      
      // Assert
      expect(order.getStatus()).toBe(OrderStatus.CONFIRMED);
      const events = order.getUncommittedEvents();
      expect(events[events.length - 1]).toBeInstanceOf(OrderConfirmedEvent);
    });
    
    it('should not allow confirming empty order', () => {
      // Arrange
      const order = Order.create({
        customerId: CustomerId.generate(),
        shippingAddress: createValidAddress()
      });
      
      // Act & Assert
      expect(() => order.confirm()).toThrow('Cannot confirm empty order');
    });
  });
});

// Helper functions
function createValidAddress(): Address {
  return Address.create({
    street: '123 Main St',
    city: 'Tokyo',
    postalCode: '100-0001'
  });
}

function createOrderWithItems(): Order {
  const order = Order.create({
    customerId: CustomerId.generate(),
    shippingAddress: createValidAddress()
  });
  
  order.addItem(ProductId.generate(), 2, Money.create(1000, 'JPY'));
  order.addItem(ProductId.generate(), 1, Money.create(500, 'JPY'));
  
  return order;
}
```

### Value Object Testing

```typescript
describe('Money Value Object', () => {
  describe('Creation', () => {
    it('should create valid money instance', () => {
      const money = Money.create(1000, 'JPY');
      
      expect(money.getAmount()).toBe(1000);
      expect(money.getCurrency()).toBe('JPY');
    });
    
    it('should not allow negative amounts', () => {
      expect(() => Money.create(-100, 'JPY')).toThrow('Amount cannot be negative');
    });
    
    it('should not allow invalid currency', () => {
      expect(() => Money.create(100, 'XXX')).toThrow('Invalid currency: XXX');
    });
  });
  
  describe('Operations', () => {
    it('should add money with same currency', () => {
      const money1 = Money.create(1000, 'JPY');
      const money2 = Money.create(500, 'JPY');
      
      const result = money1.add(money2);
      
      expect(result.getAmount()).toBe(1500);
      expect(result.getCurrency()).toBe('JPY');
    });
    
    it('should not add money with different currencies', () => {
      const money1 = Money.create(1000, 'JPY');
      const money2 = Money.create(10, 'USD');
      
      expect(() => money1.add(money2)).toThrow('Cannot add money with different currencies');
    });
    
    it('should multiply by factor', () => {
      const money = Money.create(1000, 'JPY');
      
      const result = money.multiply(1.5);
      
      expect(result.getAmount()).toBe(1500);
    });
  });
  
  describe('Equality', () => {
    it('should be equal when amount and currency match', () => {
      const money1 = Money.create(1000, 'JPY');
      const money2 = Money.create(1000, 'JPY');
      
      expect(money1.equals(money2)).toBe(true);
    });
    
    it('should not be equal when amounts differ', () => {
      const money1 = Money.create(1000, 'JPY');
      const money2 = Money.create(2000, 'JPY');
      
      expect(money1.equals(money2)).toBe(false);
    });
  });
});
```

### Mocking and Stubbing

```typescript
describe('OrderService', () => {
  let orderService: OrderService;
  let orderRepository: jest.Mocked<OrderRepository>;
  let inventoryService: jest.Mocked<InventoryService>;
  let paymentService: jest.Mocked<PaymentService>;
  let eventBus: jest.Mocked<EventBus>;
  
  beforeEach(() => {
    // Create mocks
    orderRepository = createMock<OrderRepository>();
    inventoryService = createMock<InventoryService>();
    paymentService = createMock<PaymentService>();
    eventBus = createMock<EventBus>();
    
    orderService = new OrderService(
      orderRepository,
      inventoryService,
      paymentService,
      eventBus
    );
  });
  
  describe('placeOrder', () => {
    it('should place order successfully', async () => {
      // Arrange
      const customerId = CustomerId.generate();
      const items = [
        { productId: ProductId.generate(), quantity: 2 },
        { productId: ProductId.generate(), quantity: 1 }
      ];
      
      // Mock setup
      inventoryService.checkAvailability.mockResolvedValue({
        available: true,
        reservationId: 'RES-123'
      });
      
      paymentService.authorizePayment.mockResolvedValue({
        authorized: true,
        authorizationId: 'AUTH-456'
      });
      
      orderRepository.save.mockResolvedValue(undefined);
      eventBus.publish.mockResolvedValue(undefined);
      
      // Act
      const result = await orderService.placeOrder({
        customerId,
        items,
        shippingAddress: createValidAddress()
      });
      
      // Assert
      expect(result.isSuccess()).toBe(true);
      expect(inventoryService.checkAvailability).toHaveBeenCalledWith(items);
      expect(paymentService.authorizePayment).toHaveBeenCalled();
      expect(orderRepository.save).toHaveBeenCalled();
      expect(eventBus.publish).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'OrderPlaced'
        })
      );
    });
    
    it('should rollback when payment fails', async () => {
      // Arrange
      inventoryService.checkAvailability.mockResolvedValue({
        available: true,
        reservationId: 'RES-123'
      });
      
      paymentService.authorizePayment.mockResolvedValue({
        authorized: false,
        reason: 'Insufficient funds'
      });
      
      inventoryService.releaseReservation.mockResolvedValue(undefined);
      
      // Act
      const result = await orderService.placeOrder({
        customerId: CustomerId.generate(),
        items: [{ productId: ProductId.generate(), quantity: 1 }],
        shippingAddress: createValidAddress()
      });
      
      // Assert
      expect(result.isFailure()).toBe(true);
      expect(result.error).toBe('Payment authorization failed: Insufficient funds');
      expect(inventoryService.releaseReservation).toHaveBeenCalledWith('RES-123');
      expect(orderRepository.save).not.toHaveBeenCalled();
    });
  });
});

// Mock creation helper
function createMock<T>(): jest.Mocked<T> {
  return new Proxy({} as jest.Mocked<T>, {
    get: (target, prop) => {
      if (!(prop in target)) {
        target[prop as keyof T] = jest.fn();
      }
      return target[prop as keyof T];
    }
  });
}
```

## C. Integration Testing Examples

### Repository Integration Testing

```typescript
describe('OrderRepository Integration', () => {
  let repository: OrderRepository;
  let db: TestDatabase;
  
  beforeAll(async () => {
    // Test database setup
    db = await TestDatabase.create();
    await db.migrate();
  });
  
  beforeEach(async () => {
    // Clean data
    await db.clean();
    repository = new OrderRepository(db);
  });
  
  afterAll(async () => {
    await db.destroy();
  });
  
  describe('save and find', () => {
    it('should save and retrieve order', async () => {
      // Arrange
      const order = createOrderWithItems();
      
      // Act
      await repository.save(order);
      const retrieved = await repository.findById(order.getId());
      
      // Assert
      expect(retrieved).not.toBeNull();
      expect(retrieved!.getId()).toEqual(order.getId());
      expect(retrieved!.getStatus()).toBe(order.getStatus());
      expect(retrieved!.getItems()).toHaveLength(order.getItems().length);
    });
    
    it('should update existing order', async () => {
      // Arrange
      const order = createOrderWithItems();
      await repository.save(order);
      
      // Act
      order.confirm();
      await repository.save(order);
      
      const updated = await repository.findById(order.getId());
      
      // Assert
      expect(updated!.getStatus()).toBe(OrderStatus.CONFIRMED);
    });
    
    it('should return null for non-existent order', async () => {
      // Act
      const result = await repository.findById(OrderId.generate());
      
      // Assert
      expect(result).toBeNull();
    });
  });
  
  describe('findByCustomer', () => {
    it('should find orders by customer', async () => {
      // Arrange
      const customerId = CustomerId.generate();
      const order1 = createOrder(customerId);
      const order2 = createOrder(customerId);
      const order3 = createOrder(CustomerId.generate()); // Different customer
      
      await repository.save(order1);
      await repository.save(order2);
      await repository.save(order3);
      
      // Act
      const results = await repository.findByCustomer(customerId);
      
      // Assert
      expect(results).toHaveLength(2);
      expect(results.map(o => o.getId())).toContain(order1.getId());
      expect(results.map(o => o.getId())).toContain(order2.getId());
    });
  });
  
  describe('concurrent updates', () => {
    it('should handle optimistic locking', async () => {
      // Arrange
      const order = createOrderWithItems();
      await repository.save(order);
      
      // Get two instances simultaneously
      const order1 = await repository.findById(order.getId());
      const order2 = await repository.findById(order.getId());
      
      // Act
      order1!.addItem(ProductId.generate(), 1, Money.create(100, 'JPY'));
      await repository.save(order1!);
      
      order2!.addItem(ProductId.generate(), 2, Money.create(200, 'JPY'));
      
      // Assert
      await expect(repository.save(order2!)).rejects.toThrow('Optimistic lock error');
    });
  });
});
```

### API Endpoint Integration Testing

```typescript
describe('Order API Integration', () => {
  let app: TestApplication;
  let db: TestDatabase;
  let authToken: string;
  
  beforeAll(async () => {
    db = await TestDatabase.create();
    app = await TestApplication.create({ database: db });
    
    // Create test user and get token
    const user = await createTestUser(app);
    authToken = await getAuthToken(user);
  });
  
  afterAll(async () => {
    await app.close();
    await db.destroy();
  });
  
  beforeEach(async () => {
    await db.clean(['orders', 'order_items']);
  });
  
  describe('POST /api/orders', () => {
    it('should create order successfully', async () => {
      // Arrange
      const payload = {
        items: [
          { productId: 'PROD-001', quantity: 2 },
          { productId: 'PROD-002', quantity: 1 }
        ],
        shippingAddress: {
          street: '123 Main St',
          city: 'Tokyo',
          postalCode: '100-0001'
        }
      };
      
      // Act
      const response = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${authToken}`)
        .send(payload)
        .expect(201);
      
      // Assert
      expect(response.body).toMatchObject({
        orderId: expect.any(String),
        status: 'DRAFT',
        total: {
          amount: expect.any(Number),
          currency: 'JPY'
        }
      });
      
      // Database verification
      const order = await db.orders.findOne({
        where: { id: response.body.orderId }
      });
      expect(order).not.toBeNull();
    });
    
    it('should return 400 for invalid request', async () => {
      // Act
      const response = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          items: [], // Empty item list
          shippingAddress: null
        })
        .expect(400);
      
      // Assert
      expect(response.body).toMatchObject({
        error: 'Validation failed',
        details: expect.arrayContaining([
          expect.objectContaining({
            field: 'items',
            message: 'At least one item is required'
          }),
          expect.objectContaining({
            field: 'shippingAddress',
            message: 'Shipping address is required'
          })
        ])
      });
    });
    
    it('should return 401 for unauthorized request', async () => {
      await request(app)
        .post('/api/orders')
        .send({ items: [] })
        .expect(401);
    });
  });
});
```

## D. End-to-End Testing Examples

### Scenario-Based E2E Testing

```typescript
describe('Order Fulfillment E2E', () => {
  let browser: Browser;
  let page: Page;
  let testUser: TestUser;
  
  beforeAll(async () => {
    browser = await playwright.chromium.launch({
      headless: process.env.CI === 'true'
    });
    
    // Test user and data setup
    testUser = await setupE2ETestUser();
    await setupTestProducts();
  });
  
  afterAll(async () => {
    await cleanupE2EData();
    await browser.close();
  });
  
  beforeEach(async () => {
    page = await browser.newPage();
    await loginAsTestUser(page, testUser);
  });
  
  afterEach(async () => {
    await page.close();
  });
  
  it('should complete order from cart to delivery', async () => {
    // 1. Add products to cart
    await page.goto('/products');
    
    await page.click('[data-testid="product-PROD001"]');
    await page.fill('[data-testid="quantity-input"]', '2');
    await page.click('[data-testid="add-to-cart"]');
    
    await expect(page.locator('[data-testid="cart-notification"]'))
      .toContainText('Added to cart');
    
    // 2. Verify cart
    await page.click('[data-testid="cart-icon"]');
    
    await expect(page.locator('[data-testid="cart-items"]'))
      .toContainText('Test Product 1');
    await expect(page.locator('[data-testid="cart-total"]'))
      .toContainText('¥2,000');
    
    // 3. Checkout
    await page.click('[data-testid="checkout-button"]');
    
    // Enter shipping address
    await page.fill('[data-testid="shipping-street"]', '123 Test Street');
    await page.fill('[data-testid="shipping-city"]', 'Tokyo');
    await page.fill('[data-testid="shipping-postal"]', '100-0001');
    
    // 4. Enter payment information
    await page.click('[data-testid="continue-to-payment"]');
    
    await page.fill('[data-testid="card-number"]', '4242424242424242');
    await page.fill('[data-testid="card-expiry"]', '12/25');
    await page.fill('[data-testid="card-cvc"]', '123');
    
    // 5. Confirm order
    await page.click('[data-testid="place-order"]');
    
    // 6. Verify confirmation screen
    await page.waitForSelector('[data-testid="order-confirmation"]');
    
    const orderId = await page.textContent('[data-testid="order-id"]');
    expect(orderId).toMatch(/^ORD-\d+$/);
    
    await expect(page.locator('[data-testid="order-status"]'))
      .toContainText('Order Confirmed');
    
    // 7. Verify in order history
    await page.click('[data-testid="view-orders"]');
    
    await expect(page.locator(`[data-testid="order-${orderId}"]`))
      .toBeVisible();
    
    // 8. Verify shipping status updates (WebSocket real-time updates)
    await simulateShipmentUpdate(orderId);
    
    await expect(page.locator(`[data-testid="order-${orderId}-status"]`))
      .toContainText('Shipped');
  });
  
  it('should handle payment failure gracefully', async () => {
    // Add products to cart
    await addProductsToCart(page, [
      { id: 'PROD001', quantity: 1 }
    ]);
    
    // Proceed through checkout
    await page.goto('/checkout');
    await fillShippingAddress(page);
    await page.click('[data-testid="continue-to-payment"]');
    
    // Use failing card number
    await page.fill('[data-testid="card-number"]', '4000000000000002');
    await page.fill('[data-testid="card-expiry"]', '12/25');
    await page.fill('[data-testid="card-cvc"]', '123');
    
    await page.click('[data-testid="place-order"]');
    
    // Verify error message
    await expect(page.locator('[data-testid="payment-error"]'))
      .toContainText('Payment was declined');
    
    // Verify cart state is preserved
    await page.click('[data-testid="back-to-cart"]');
    await expect(page.locator('[data-testid="cart-items"]'))
      .toContainText('Test Product 1');
  });
});

// Helper functions
async function loginAsTestUser(page: Page, user: TestUser): Promise<void> {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', user.email);
  await page.fill('[data-testid="password"]', user.password);
  await page.click('[data-testid="login-button"]');
  await page.waitForSelector('[data-testid="user-menu"]');
}

async function addProductsToCart(
  page: Page, 
  products: Array<{ id: string; quantity: number }>
): Promise<void> {
  for (const product of products) {
    await page.goto(`/products/${product.id}`);
    await page.fill('[data-testid="quantity-input"]', product.quantity.toString());
    await page.click('[data-testid="add-to-cart"]');
    await page.waitForSelector('[data-testid="cart-notification"]');
  }
}
```

## E. Advanced Testing Strategies

### Property-Based Testing

```typescript
import * as fc from 'fast-check';

describe('Money Property-Based Tests', () => {
  it('should maintain associativity in addition', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 1000000 }),
        fc.integer({ min: 0, max: 1000000 }),
        fc.integer({ min: 0, max: 1000000 }),
        (a, b, c) => {
          const money1 = Money.create(a, 'JPY');
          const money2 = Money.create(b, 'JPY');
          const money3 = Money.create(c, 'JPY');
          
          // (a + b) + c = a + (b + c)
          const left = money1.add(money2).add(money3);
          const right = money1.add(money2.add(money3));
          
          return left.equals(right);
        }
      )
    );
  });
  
  it('should maintain identity in addition', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 1000000 }),
        (amount) => {
          const money = Money.create(amount, 'JPY');
          const zero = Money.create(0, 'JPY');
          
          // a + 0 = a
          return money.add(zero).equals(money);
        }
      )
    );
  });
  
  it('should handle currency conversion correctly', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 1000000 }),
        fc.float({ min: 0.01, max: 200 }),
        (amount, rate) => {
          const jpy = Money.create(amount, 'JPY');
          const usd = jpy.convertTo('USD', rate);
          const backToJpy = usd.convertTo('JPY', 1 / rate);
          
          // Round-trip conversion should be close to original (considering floating-point errors)
          return Math.abs(backToJpy.getAmount() - amount) < 2;
        }
      )
    );
  });
});

describe('Order Invariants Property-Based Tests', () => {
  it('should never have negative total', () => {
    fc.assert(
      fc.property(
        fc.array(
          fc.record({
            quantity: fc.integer({ min: 1, max: 100 }),
            price: fc.integer({ min: 1, max: 100000 })
          }),
          { minLength: 1, maxLength: 10 }
        ),
        (items) => {
          const order = Order.create({
            customerId: CustomerId.generate(),
            shippingAddress: createValidAddress()
          });
          
          items.forEach(item => {
            order.addItem(
              ProductId.generate(),
              item.quantity,
              Money.create(item.price, 'JPY')
            );
          });
          
          return order.getTotal().getAmount() > 0;
        }
      )
    );
  });
  
  it('should maintain item count consistency', () => {
    fc.assert(
      fc.property(
        fc.array(fc.string({ minLength: 1 }), { minLength: 1, maxLength: 20 }),
        (productIds) => {
          const order = Order.create({
            customerId: CustomerId.generate(),
            shippingAddress: createValidAddress()
          });
          
          const uniqueProducts = [...new Set(productIds)];
          
          productIds.forEach(id => {
            order.addItem(
              ProductId.fromString(id),
              1,
              Money.create(1000, 'JPY')
            );
          });
          
          // Same products should be consolidated into single items
          return order.getItems().length === uniqueProducts.length;
        }
      )
    );
  });
});
```

### Contract Testing

```typescript
// Provider side (Inventory Service)
describe('Inventory Service Contract', () => {
  let pact: Pact;
  let inventoryService: InventoryService;
  
  beforeAll(async () => {
    pact = new Pact({
      consumer: 'OrderService',
      provider: 'InventoryService',
      port: 8080
    });
    
    await pact.setup();
    inventoryService = new InventoryService();
  });
  
  afterAll(async () => {
    await pact.finalize();
  });
  
  it('should check product availability', async () => {
    // Define expected interaction
    await pact.addInteraction({
      state: 'Product PROD001 has 10 items in stock',
      uponReceiving: 'a request to check availability',
      withRequest: {
        method: 'POST',
        path: '/api/inventory/check-availability',
        headers: {
          'Content-Type': 'application/json'
        },
        body: {
          productId: 'PROD001',
          quantity: 5
        }
      },
      willRespondWith: {
        status: 200,
        headers: {
          'Content-Type': 'application/json'
        },
        body: {
          available: true,
          currentStock: 10,
          reservationId: like('RES-123456')
        }
      }
    });
    
    // Actual test
    const response = await inventoryService.checkAvailability('PROD001', 5);
    
    expect(response).toMatchObject({
      available: true,
      currentStock: 10,
      reservationId: expect.stringMatching(/^RES-\d+$/)
    });
  });
  
  it('should handle insufficient stock', async () => {
    await pact.addInteraction({
      state: 'Product PROD002 has 2 items in stock',
      uponReceiving: 'a request for more items than available',
      withRequest: {
        method: 'POST',
        path: '/api/inventory/check-availability',
        body: {
          productId: 'PROD002',
          quantity: 5
        }
      },
      willRespondWith: {
        status: 200,
        body: {
          available: false,
          currentStock: 2,
          message: 'Insufficient stock'
        }
      }
    });
    
    const response = await inventoryService.checkAvailability('PROD002', 5);
    
    expect(response.available).toBe(false);
    expect(response.message).toBe('Insufficient stock');
  });
});

// Consumer side (Order Service)
describe('Order Service as Consumer', () => {
  it('should verify contract with Inventory Service', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:8080',
      provider: 'InventoryService',
      providerVersion: '1.0.0',
      pactUrls: ['./pacts/orderservice-inventoryservice.json']
    });
    
    await verifier.verifyProvider();
  });
});
```

## F. Test Quality Measurement

### Coverage Analysis

```typescript
// Coverage configuration
export const coverageConfig = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/**/*.stories.tsx'
  ],
  coverageThreshold: {
    global: {
      branches: 75,
      functions: 80,
      lines: 80,
      statements: 80
    },
    './src/domain/': {
      branches: 90,
      functions: 95,
      lines: 95,
      statements: 95
    },
    './src/infrastructure/': {
      branches: 70,
      functions: 75,
      lines: 75,
      statements: 75
    }
  }
};

// Coverage report analysis
export class CoverageAnalyzer {
  analyzeReport(report: CoverageReport): CoverageInsights {
    return {
      uncoveredCriticalPaths: this.findUncoveredCriticalPaths(report),
      lowCoverageModules: this.findLowCoverageModules(report),
      recommendations: this.generateRecommendations(report)
    };
  }
  
  private findUncoveredCriticalPaths(report: CoverageReport): Path[] {
    // Identify business-critical paths that are uncovered
    const criticalPaths = [
      'src/domain/order/Order.ts',
      'src/domain/payment/PaymentService.ts',
      'src/application/OrderService.ts'
    ];
    
    return report.files
      .filter(file => 
        criticalPaths.includes(file.path) && 
        file.lineCoverage < 90
      )
      .map(file => ({
        path: file.path,
        uncoveredLines: file.uncoveredLines,
        risk: 'HIGH'
      }));
  }
}
```

This appendix provides the complete implementation examples that support the testing strategies discussed in Chapter 23. These patterns can be adapted to specific project needs while maintaining the core principles of effective testing.