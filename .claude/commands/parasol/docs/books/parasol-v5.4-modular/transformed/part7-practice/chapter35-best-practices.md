# 第35章　ベストプラクティス ― 千年続く技の継承

## はじめに：伊勢神宮の式年遷宮

伊勢神宮では20年に一度、社殿を建て替える「式年遷宮」が1300年以上続いています。

同じ材料、同じ技法、同じ手順で、寸分違わぬ社殿を建て直す。なぜでしょうか？

**技術の継承**です。

20年という期間は、若い職人が技を学び、熟練職人として次世代に教えるちょうどよい周期。設計図だけでなく、生きた技術が途切れることなく伝わります。

ソフトウェア開発も同じです。コードを書くだけでなく、その背後にある「技」を継承することが、長く続くシステムを作る秘訣なのです。

---

## 読者別ガイド

**エグゼクティブの方へ** 💼
- 技術継承の価値（5分）
- 品質文化の構築
- 長期的な競争優位

**アーキテクトの方へ** 🏗️
- 設計原則の体系化
- アーキテクチャ決定記録
- 技術的負債の管理

**開発者の方へ** 💻
- 実践的なコーディング規約
- テスト戦略の実装
- 日々の開発フロー

---

## 第1章：職人の心得 ― プロフェッショナリズム

### 守・破・離の精神

日本の伝統芸能や武道で重視される学びの段階：

**守（しゅ）** - 基本を忠実に守る
```typescript
// 基本に忠実なコード
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly logger: Logger
  ) {}
  
  async findById(id: string): Promise<User | null> {
    this.logger.debug('Finding user by id', { id });
    
    try {
      const user = await this.userRepository.findById(id);
      
      if (!user) {
        this.logger.warn('User not found', { id });
        return null;
      }
      
      this.logger.debug('User found', { id, userId: user.id });
      return user;
    } catch (error) {
      this.logger.error('Error finding user', { id, error });
      throw error;
    }
  }
}
```

**破（は）** - 基本を理解した上で応用する
```typescript
// キャッシングを追加した応用
export class CachedUserService extends UserService {
  constructor(
    userRepository: UserRepository,
    logger: Logger,
    private readonly cache: CacheService
  ) {
    super(userRepository, logger);
  }
  
  async findById(id: string): Promise<User | null> {
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return cached;
    
    const user = await super.findById(id);
    if (user) {
      await this.cache.set(`user:${id}`, user, 300); // 5分間キャッシュ
    }
    
    return user;
  }
}
```

**離（り）** - 独自の境地を開く
```typescript
// イベント駆動アーキテクチャへの進化
export class EventDrivenUserService {
  async findById(id: string): Promise<User | null> {
    // 読み取り専用モデルから取得（CQRSパターン）
    const user = await this.readModel.findUser(id);
    
    // アクセスイベントを非同期で発行
    this.eventBus.publish(
      new UserAccessedEvent(id, new Date())
    );
    
    return user;
  }
}
```

### 一期一会の精神

茶道の「一期一会」― 一生に一度の出会いを大切にする心。

コードも同じです。今書いているコードを読むのは、未来の自分か、見知らぬ誰か。その一度きりの出会いを大切に、読み手への思いやりを込めて書きましょう。

---

## 第2章：道具を磨く ― 開発環境とツール

### 職人の道具箱

優れた職人は道具を大切にします。毎日手入れし、最高の状態を保ちます。

**開発環境の整備**：
```json
// .vscode/settings.json - チーム共通の設定
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/dist": true
  }
}
```

**品質チェックツール**：
```json
// package.json - 品質維持のためのスクリプト
{
  "scripts": {
    "lint": "eslint . --fix",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "test": "jest --coverage",
    "quality": "npm run lint && npm run format && npm run type-check && npm run test",
    "pre-commit": "npm run quality"
  }
}
```

---

## 第3章：型を極める ― モジュール設計の型

### 組木細工のように ― 精密な組み合わせ

日本の組木細工は、釘を使わずに木材を組み合わせる技術。各部品が完璧にフィットし、全体として強固な構造を作ります。

**モジュールも同じ原理で設計します**：

```typescript
// 完璧にフィットする型定義
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

interface CacheService {
  get<T>(key: string): Promise<T | null>;
  set<T>(key: string, value: T, ttl?: number): Promise<void>;
}

interface EventBus {
  publish<T extends Event>(event: T): void;
  subscribe<T extends Event>(
    eventType: new (...args: any[]) => T,
    handler: (event: T) => void
  ): Unsubscribe;
}
```

### 単一責任の美学

日本刀は「切る」という単一の目的に特化して作られます。余計な装飾や機能はありません。

**モジュールも同じです**：
```typescript
// 責任を明確に分離したモジュール
export class UserValidator {
  // 検証のみに責任を持つ
  validate(user: UserInput): ValidationResult {
    const errors: ValidationError[] = [];
    
    if (!user.email || !this.isValidEmail(user.email)) {
      errors.push({ field: 'email', message: 'Invalid email' });
    }
    
    if (!user.name || user.name.length < 2) {
      errors.push({ field: 'name', message: 'Name too short' });
    }
    
    return { valid: errors.length === 0, errors };
  }
}

export class UserPersistence {
  // 永続化のみに責任を持つ
  async save(user: User): Promise<void> {
    await this.db.transaction(async tx => {
      await tx.users.upsert(user);
      await tx.auditLog.insert({
        action: 'USER_SAVED',
        userId: user.id,
        timestamp: new Date()
      });
    });
  }
}
```

---

## 第4章：品質の作り込み ― テスト戦略

### 漆塗りの技法

漆器は何十回も漆を重ね塗りして作られます。各層が完璧でなければ、最終的な美しさは生まれません。

**テストも層を重ねて品質を作り込みます**：

```typescript
// ユニットテスト - 基礎の層
describe('UserValidator', () => {
  const validator = new UserValidator();
  
  test('有効なユーザー入力を検証', () => {
    const result = validator.validate({
      email: 'user@example.com',
      name: 'Taro Yamada'
    });
    
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });
  
  test('無効なメールアドレスを検出', () => {
    const result = validator.validate({
      email: 'invalid-email',
      name: 'Taro Yamada'
    });
    
    expect(result.valid).toBe(false);
    expect(result.errors).toContainEqual({
      field: 'email',
      message: 'Invalid email'
    });
  });
});
```

**統合テスト - 中間の層**：
```typescript
describe('UserService Integration', () => {
  let service: UserService;
  let db: TestDatabase;
  
  beforeEach(async () => {
    db = await TestDatabase.create();
    service = new UserService(db, new Logger());
  });
  
  test('ユーザーの作成から取得まで', async () => {
    // 作成
    const created = await service.create({
      email: 'test@example.com',
      name: 'Test User'
    });
    
    // 取得
    const found = await service.findById(created.id);
    
    expect(found).toEqual(created);
  });
});
```

### 守りのテスト、攻めのテスト

**守りのテスト** - リグレッションを防ぐ：
```typescript
// スナップショットテストで既存の動作を守る
test('APIレスポンスの形式が変わっていないこと', () => {
  const response = formatUserResponse(user);
  expect(response).toMatchSnapshot();
});
```

**攻めのテスト** - 新機能の品質を保証：
```typescript
// プロパティベーステストで未知のケースも検証
import fc from 'fast-check';

test('どんな入力でもクラッシュしない', () => {
  fc.assert(
    fc.property(
      fc.record({
        email: fc.string(),
        name: fc.string()
      }),
      (input) => {
        // クラッシュしないことを確認
        expect(() => validator.validate(input)).not.toThrow();
      }
    )
  );
});
```

---

## 第5章：流れを整える ― 開発フローの最適化

### 茶道の所作

茶道では、一つ一つの動作に意味があり、無駄がありません。全ての所作が流れるように繋がっています。

**開発フローも同じように設計します**：

```yaml
# .github/workflows/ci.yml - 自動化された品質チェック
name: Continuous Integration

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Type Check
        run: npm run type-check
      
      - name: Test
        run: npm run test:coverage
      
      - name: Build
        run: npm run build
```

### 断捨離の精神

不要なものを持たない、シンプルさの美学。

**コードベースの断捨離**：
```typescript
// 使われていない依存関係の検出
// package.json
{
  "scripts": {
    "deps:check": "depcheck",
    "deps:update": "npm-check-updates -u",
    "clean": "rm -rf dist node_modules coverage"
  }
}
```

---

## 第6章：伝承の仕組み ― ドキュメントと知識共有

### 口伝と文書

伝統技術は「口伝」と「文書」の両方で伝承されます。

**コードコメント - 口伝の代わり**：
```typescript
/**
 * ユーザー認証サービス
 * 
 * このサービスはJWT方式で認証を行います。
 * トークンの有効期限は30分で、リフレッシュトークンで更新可能です。
 * 
 * @example
 * const auth = new AuthService(config);
 * const token = await auth.login('user@example.com', 'password');
 * const user = await auth.verify(token);
 */
export class AuthService {
  // 実装...
}
```

**アーキテクチャ決定記録（ADR）- 文書**：
```markdown
# ADR-001: JWT認証の採用

## ステータス
承認済み

## コンテキスト
APIの認証方式を決定する必要がある。

## 決定
JWT（JSON Web Token）を採用する。

## 理由
- ステートレスでスケーラブル
- マイクロサービス間で共有しやすい
- 標準規格で多くのライブラリがある

## 結果
- 各リクエストでトークン検証が必要
- トークン無効化には別途仕組みが必要
```

---

## 伝統は革新の連続

式年遷宮は同じことの繰り返しに見えて、実は毎回、材料の調達方法や道具、技術に少しずつ改良が加えられています。伝統とは、革新の連続なのです。

ソフトウェア開発のベストプラクティスも同じ。基本を大切にしながら、常に改善を続ける。それが、千年続く技術を作る秘訣です。

**これまでの旅を振り返って**：
1. **守** - 基本に忠実に（Part 1-3の基礎）
2. **破** - 応用と実践（Part 4-6の設計と実装）
3. **離** - 独自の境地へ（Part 7-8の実践と未来）

あなたも今日から、千年続くコードを書く職人の一人です。

---

## 演習問題：職人への道

1. **道具の手入れ**：あなたのプロジェクトの開発環境を見直してください。改善できる点を3つ挙げ、実際に設定を追加してください。

2. **型の設計**：既存のモジュールを1つ選び、単一責任の原則に従ってリファクタリングしてください。Before/Afterを比較し、改善点を説明してください。

3. **伝承の準備**：重要な設計決定を1つ選び、ADR（アーキテクチャ決定記録）として文書化してください。

---

**💡 実装の詳細は付録をご覧ください**
- [付録35-A: コーディング規約集](../appendices/chapter35-implementation.md)
- [付録35-B: テストパターンカタログ](../appendices/chapter35-implementation.md#testing)
- [付録35-C: CI/CDテンプレート](../appendices/chapter35-implementation.md#cicd)