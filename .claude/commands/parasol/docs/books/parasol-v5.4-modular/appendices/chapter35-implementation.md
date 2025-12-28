# 付録：第35章　ベストプラクティスの実装詳細

## コーディング規約集

### 命名規約

```typescript
// ファイル名
user.service.ts         // サービスクラス
user.interface.ts       // インターフェース定義
user.service.spec.ts    // テストファイル

// クラス・インターフェース
export class UserService { }           // PascalCase
export interface UserRepository { }    // PascalCase

// 変数・関数
const userName = 'John';              // camelCase
function calculateTotal() { }         // camelCase

// 定数
const MAX_RETRY_COUNT = 3;           // UPPER_SNAKE_CASE
const DEFAULT_TIMEOUT = 5000;        // UPPER_SNAKE_CASE

// 型パラメータ
type Result<T, E = Error> = Success<T> | Failure<E>;  // 単一文字または意味のある名前
```

### コード構成

```typescript
// 推奨されるファイル構成
// 1. インポート
import { Injectable } from '@nestjs/common';
import { User } from './entities/user.entity';

// 2. インターフェース定義
interface UserCreateInput {
  email: string;
  name: string;
}

// 3. 定数定義
const DEFAULT_PAGE_SIZE = 20;

// 4. メインクラス/関数
@Injectable()
export class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly logger: Logger
  ) {}
  
  // パブリックメソッド
  async findAll(options?: FindOptions): Promise<User[]> {
    return this.repository.findAll(options);
  }
  
  // プライベートメソッド
  private validateEmail(email: string): boolean {
    return /^[^@]+@[^@]+\.[^@]+$/.test(email);
  }
}

// 5. ヘルパー関数
function formatUserName(firstName: string, lastName: string): string {
  return `${lastName} ${firstName}`;
}
```

### エラーハンドリング

```typescript
// カスタムエラークラス
export class BusinessError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 400
  ) {
    super(message);
    this.name = 'BusinessError';
  }
}

export class NotFoundError extends BusinessError {
  constructor(resource: string, id: string) {
    super(
      `${resource} with id ${id} not found`,
      'RESOURCE_NOT_FOUND',
      404
    );
  }
}

// エラーハンドリングパターン
export class UserService {
  async findById(id: string): Promise<User> {
    try {
      const user = await this.repository.findById(id);
      
      if (!user) {
        throw new NotFoundError('User', id);
      }
      
      return user;
    } catch (error) {
      // 既知のエラーは再スロー
      if (error instanceof BusinessError) {
        throw error;
      }
      
      // 未知のエラーはログして汎用エラーを投げる
      this.logger.error('Unexpected error finding user', { id, error });
      throw new Error('Failed to find user');
    }
  }
}
```

## モジュール構成パターン

### Clean Architecture構成

```
src/
├── domain/              # ビジネスロジック
│   ├── entities/       # エンティティ
│   ├── value-objects/  # 値オブジェクト
│   └── services/       # ドメインサービス
│
├── application/         # アプリケーションロジック
│   ├── use-cases/      # ユースケース
│   ├── dto/            # データ転送オブジェクト
│   └── interfaces/     # リポジトリインターフェース
│
├── infrastructure/      # 技術的詳細
│   ├── persistence/    # データベース実装
│   ├── messaging/      # メッセージング実装
│   └── web/           # Web API実装
│
└── shared/             # 共通コンポーネント
    ├── errors/         # エラー定義
    ├── utils/          # ユーティリティ
    └── types/          # 共通型定義
```

### Feature-based構成

```
src/
├── features/
│   ├── user/
│   │   ├── user.module.ts
│   │   ├── user.controller.ts
│   │   ├── user.service.ts
│   │   ├── user.repository.ts
│   │   ├── dto/
│   │   ├── entities/
│   │   └── tests/
│   │
│   ├── auth/
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   └── strategies/
│   │
│   └── order/
│       └── ... 同様の構成
│
├── shared/
│   ├── database/
│   ├── config/
│   └── middleware/
│
└── main.ts
```

## テストパターンカタログ

<div id="testing"></div>

### テストの構成 - AAA パターン

```typescript
describe('UserService', () => {
  let service: UserService;
  let repository: MockRepository<User>;
  
  beforeEach(() => {
    repository = createMockRepository();
    service = new UserService(repository);
  });
  
  describe('findById', () => {
    it('should return user when found', async () => {
      // Arrange（準備）
      const userId = 'user-123';
      const expectedUser = new User(userId, 'John Doe');
      repository.findById.mockResolvedValue(expectedUser);
      
      // Act（実行）
      const result = await service.findById(userId);
      
      // Assert（検証）
      expect(result).toEqual(expectedUser);
      expect(repository.findById).toHaveBeenCalledWith(userId);
    });
  });
});
```

### テストダブルの使い分け

```typescript
// スタブ - 固定値を返す
const userStub = {
  id: '123',
  name: 'Test User',
  email: 'test@example.com'
};

// モック - 呼び出しを検証
const mockLogger = {
  info: jest.fn(),
  error: jest.fn()
};

// スパイ - 実装を保持しつつ呼び出しを記録
const dateSpy = jest.spyOn(Date, 'now');

// フェイク - 簡易実装
class FakeUserRepository implements UserRepository {
  private users = new Map<string, User>();
  
  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }
  
  async save(user: User): Promise<void> {
    this.users.set(user.id, user);
  }
}
```

### 統合テストのパターン

```typescript
// データベース統合テスト
describe('UserRepository Integration', () => {
  let repository: UserRepository;
  let connection: Connection;
  
  beforeAll(async () => {
    connection = await createTestConnection();
    repository = new UserRepository(connection);
  });
  
  afterAll(async () => {
    await connection.close();
  });
  
  beforeEach(async () => {
    await connection.synchronize(true); // データベースをクリア
  });
  
  it('should persist and retrieve user', async () => {
    // 保存
    const user = new User('123', 'John Doe', 'john@example.com');
    await repository.save(user);
    
    // 取得
    const retrieved = await repository.findById(user.id);
    
    // 検証
    expect(retrieved).toEqual(user);
  });
});
```

### E2Eテストのパターン

```typescript
// API E2Eテスト
describe('User API E2E', () => {
  let app: INestApplication;
  
  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule]
    }).compile();
    
    app = moduleRef.createNestApplication();
    await app.init();
  });
  
  afterAll(async () => {
    await app.close();
  });
  
  describe('POST /users', () => {
    it('should create new user', async () => {
      const createDto = {
        name: 'John Doe',
        email: 'john@example.com'
      };
      
      const response = await request(app.getHttpServer())
        .post('/users')
        .send(createDto)
        .expect(201);
      
      expect(response.body).toMatchObject({
        id: expect.any(String),
        ...createDto
      });
    });
  });
});
```

## CI/CDテンプレート

<div id="cicd"></div>

### GitHub Actions設定

```yaml
# .github/workflows/main.yml
name: Main Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'
  
jobs:
  # 品質チェック
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Type check
        run: npm run type-check
      
      - name: Format check
        run: npm run format:check

  # テスト実行
  test:
    name: Test
    runs-on: ubuntu-latest
    needs: quality
    
    strategy:
      matrix:
        node: [16, 18, 20]
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:ci
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.node == 18

  # ビルド
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [quality, test]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  # デプロイ（本番環境）
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/
      
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # 実際のデプロイコマンドをここに記述
```

### Docker設定

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# 依存関係のインストール
COPY package*.json ./
RUN npm ci --only=production

# ソースコードのコピーとビルド
COPY . .
RUN npm run build

# 本番イメージ
FROM node:18-alpine

WORKDIR /app

# 必要なファイルのみコピー
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# セキュリティ設定
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD node healthcheck.js

EXPOSE 3000

CMD ["node", "dist/main.js"]
```

## 運用のベストプラクティス

### ロギング戦略

```typescript
// 構造化ログ
export class Logger {
  private context: Record<string, any> = {};
  
  withContext(context: Record<string, any>): Logger {
    const logger = new Logger();
    logger.context = { ...this.context, ...context };
    return logger;
  }
  
  info(message: string, meta?: Record<string, any>): void {
    this.log('INFO', message, meta);
  }
  
  error(message: string, error?: Error, meta?: Record<string, any>): void {
    this.log('ERROR', message, {
      ...meta,
      error: {
        message: error?.message,
        stack: error?.stack,
        name: error?.name
      }
    });
  }
  
  private log(level: string, message: string, meta?: Record<string, any>): void {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      level,
      message,
      ...this.context,
      ...meta
    }));
  }
}
```

### モニタリング設定

```typescript
// Prometheusメトリクス
import { Counter, Histogram, Registry } from 'prom-client';

export class MetricsService {
  private registry = new Registry();
  
  private httpRequestDuration = new Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status'],
    registers: [this.registry]
  });
  
  private httpRequestTotal = new Counter({
    name: 'http_request_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status'],
    registers: [this.registry]
  });
  
  recordHttpRequest(
    method: string,
    route: string,
    status: number,
    duration: number
  ): void {
    const labels = { method, route, status: status.toString() };
    this.httpRequestDuration.observe(labels, duration);
    this.httpRequestTotal.inc(labels);
  }
  
  getMetrics(): string {
    return this.registry.metrics();
  }
}
```