# パラソルドメイン言語（Parasol Domain Language）ガイドライン

**重要**: これは「パラソルドメイン言語」です。DDD（ドメイン駆動設計）の「ドメイン言語」とは異なるコンセプトです。

## パラソル開発コンセプト

### 中心思想：Single Source of Truth

パラソルドメイン言語は、**AIによるソフトウェア開発の基盤**として機能します。すべての実装（UI、DB、API）はこの定義から自動生成・検証され、修正もこの言語定義を起点に行います。

```
パラソルドメイン言語
    ↓
┌─────┴─────┬─────────┬──────────┐
│    UI     │   API   │    DB    │
│ (自動生成) │(自動生成)│ (自動生成) │
└───────────┴─────────┴──────────┘
```

### AI駆動開発の3原則

1. **定義駆動開発（Definition-Driven Development）**
   - ドメイン定義が先、実装は後
   - 変更は定義から、実装へ自動伝播
   - 手動でのコード修正は原則禁止

2. **一貫性保証（Consistency Guarantee）**
   - 型定義の共有による型安全性
   - ビジネスルールの単一定義
   - VS間・BC間の整合性自動検証

3. **再生成可能性（Regeneratability）**
   - いつでも定義から実装を再生成可能
   - 部分的な再生成もサポート
   - 実装の詳細は破棄可能

### 実装非依存の原則（V4から継承）

パラソルドメイン言語は、特定の実装技術に依存しない抽象的な定義を重視します：

1. **共通型定義（Common Type Definition）**
   - **物理量型**: Temperature, Pressure, Duration等は単位と制約のみ定義
   - **識別子型**: Id型は概念レベルで定義、UUID等の実装詳細は含まない
   - **ドメイン型**: ビジネス概念を表す型は抽象度を保つ
   - **制約**: ビジネスルールは宣言的に記述、実装方法は規定しない

2. **技術中立性（Technology Neutrality）**
   - プログラミング言語固有の構文を使わない
   - データベース固有の型（VARCHAR、INT等）を前提としない
   - フレームワーク固有の概念（@Decorator等）を含まない
   - プラットフォーム依存の前提を置かない

3. **変換可能性（Transformability）**
   - 同じ定義から複数の技術スタックへの変換が可能
   - 技術変更時も定義は不変
   - 各実装言語の慣習に従った自然な変換

## パラソルドメイン言語の位置づけ

### DDD戦略的設計との関係

```
Phase 0: 初期化
    ↓
Phase 1: Context（ステークホルダー、制約）
    ↓
Phase 2: Value Streams（価値の流れ）
    ↓
Phase 3: Capabilities（ケーパビリティ）
    ├── CL1: 活動領域識別（傾向的分類・参考情報）
    ├── CL2: ケイパビリティ設計（正式分類・投資判断根拠）
    └── CL3: 業務オペレーション定義（分類なし・網羅性重視）
    ↓
Phase 4: Application Design（アプリケーション設計）
    ├── capability-bc-mapping.md（CL2-BC対応表）
    ├── context-map.md（BC間関係）
    └── Bounded Context確定
    ↓
Phase 5: Software Design（ソフトウェア設計）★
    └── BC単位でパラソルドメイン言語定義（domain-language.md）
    ↓
Phase 6-7: 実装・プラットフォーム
```

### 役割分担

| 成果物 | 役割 | 作成者 |
|--------|------|--------|
| CL3ビジネス定義 | What/Whyを定義 | 人間（ドメインエキスパート） |
| パラソルドメイン言語 | Howを定義 | 人間（設計者）→ AI（保守） |
| 実装コード | 動作する成果物 | AI（自動生成） |

## パラソルドメイン言語の6つのセクション

### 1. Aggregates（集約）

**目的**: ドメインの中核概念と振る舞いを定義

```yaml
Root Entity: {EntityName}
Description: {説明}

Properties:
  - {propertyName}: {Type} ({説明})
  # → UI: フォームフィールド
  # → API: リクエスト/レスポンス
  # → DB: テーブルカラム

Invariants:
  - {不変条件}
  # → UI: バリデーション
  # → API: ビジネスルール
  # → DB: 制約

Behaviors:
  - {methodName}(): {説明}
  # → UI: アクション
  # → API: エンドポイント
  # → DB: トランザクション
```

### 2. Value Objects（値オブジェクト）

**目的**: 再利用可能な型定義

```yaml
# 基本形式
{ValueObjectName}:
  Type: {抽象型}
  Validation: {検証ルール}
  # → 全層で共通利用
  Format: {フォーマット}
  # → UI: 入力マスク
  # → API: パラメータ検証
  # → DB: CHECK制約

# 実装非依存の型定義例
Temperature:
  Type: Decimal
  Unit: Celsius
  Range: [-273.15, 1000.0]
  Precision: 0.1
  # 実装時に各言語の適切な型に変換
  # Python: float, TypeScript: number, Java: BigDecimal

Percentage:
  Type: Decimal
  Range: [0.0, 100.0]
  Precision: 0.01
  Unit: Percent

Duration:
  Type: Interval
  Unit: [Seconds, Minutes, Hours, Days]
  MinValue: 0
  # ISO 8601形式で表現可能

Money:
  Type: Decimal
  Currency: Currency
  Precision: 2
  # 通貨と金額を持つ複合型
```

### 3. Domain Events（ドメインイベント）

**目的**: システム間連携の定義

```yaml
{EventName}:
  Description: {説明}
  Properties:
    - {property}: {Type}
  # → イベント駆動アーキテクチャ
  # → 非同期処理
  # → 監査ログ
  VS間: Yes/No
  # → マイクロサービス間通信
```

### 4. Domain Services（ドメインサービス）

**目的**: 複雑なビジネスロジックの定義

```yaml
Responsibility: {責務}
Methods:
  - {methodName}({params}):
      Logic:
        - {処理概要}
  # → API: ビジネスロジック層
  # → UI: 複雑な画面ロジック
```

### 5. Repositories（リポジトリ）

**目的**: データアクセスパターンの定義

```yaml
Methods:
  - findBy{Criteria}(): {ReturnType}
  # → DB: クエリ生成
  # → API: データアクセス層
  # → UI: データ取得
```

### 6. ユビキタス言語辞書

**目的**: 用語の統一と理解の共有

| 日本語 | 英語 | 定義 |
|--------|------|------|
| {用語} | {Term} | {定義} |
# → 全層で一貫した命名

## AI生成パターン

### 1. UI生成

```typescript
// パラソルドメイン言語から自動生成
interface YeastStrainForm {
  strainCode: string; // StrainCode型から生成
  name: string;       // StrainName型から生成
  // Invariantsからバリデーション生成
  validate(): ValidationResult;
}
```

### 2. API生成

```typescript
// Behaviorsから自動生成
@Post('/strains')
async register(@Body() dto: RegisterStrainDto) {
  // Invariantsのビジネスルール適用
}
```

### 3. DB生成

```sql
-- Aggregateから自動生成
CREATE TABLE yeast_strains (
  strain_id UUID PRIMARY KEY,
  strain_code VARCHAR(20) UNIQUE,
  -- Value Object制約の適用
  CHECK (strain_code ~ 'ASH-[0-9]{4}-[0-9]{4}')
);
```

## 修正フロー

### 従来の開発
```
要件変更 → コード修正 → テスト → デプロイ
         ↑ 不整合の危険性
```

### パラソル開発
```
要件変更 → パラソルドメイン言語修正 → 自動生成 → デプロイ
                              ↑ 一貫性保証
```

## ディレクトリ構成

```
projects/{project-name}/outputs/
│
├── 3-capabilities/                             # Phase 3: ビジネス観点
│   └── {vs-slug}/
│       ├── cl1-domain-classification.md        # CL1: Core/Supporting/Generic分類
│       ├── cl2-subdomain-design.md             # CL2: サービス境界候補
│       └── cl3-business-operations/            # CL3: 業務オペレーション
│           └── {capability}-operations.md
│
├── 4-architecture/                             # Phase 4: 技術設計
│   ├── capability-bc-mapping.md                # ★ CL2-BC対応表（必須）
│   ├── context-map.md                          # BC間関係
│   └── services/
│       └── {service}/
│           └── bounded-contexts.md             # サービス内BC一覧
│
└── 5-software/                                 # Phase 5: ソフトウェア設計
    └── {service}/
        └── {bc-name}/                          # ★ BCが設計単位
            ├── domain-language.md              # パラソルドメイン言語（SSOT）
            ├── api-specification.md            # API仕様
            ├── database-design.md              # DB設計（生成物）
            ├── operations/                     # オペレーション群
            │   └── {operation}/actor-usecases/
            └── tests/                          # テスト定義
                ├── unit-spec.yaml
                ├── api-spec.yaml
                ├── ui-spec.yaml
                └── integration-spec.yaml
```

**重要**: パラソルドメイン言語は **Phase 5** の `domain-language.md` に配置します。
Phase 3 はビジネス観点の定義であり、技術実装の詳細は Phase 5 で定義します。

## 実装例：酵母株管理

### パラソルドメイン言語定義（抜粋）

```yaml
# Aggregates
YeastStrain:
  Properties:
    - strainCode: StrainCode
    - name: StrainName
  Invariants:
    - strainCodeは一意で必須
  Behaviors:
    - register(): 新規酵母株登録

# Value Objects
StrainCode:
  Type: String
  Format: "ASH-YYYY-NNNN"
  Validation: 正規表現パターンマッチ
```

### 自動生成される実装

**UI（React）**
```tsx
const YeastStrainForm: FC = () => {
  const [strainCode, setStrainCode] = useState('');
  
  // Format from Value Object
  const pattern = /^ASH-\d{4}-\d{4}$/;
  
  // Invariant validation
  const validate = () => {
    if (!strainCode) return "strainCodeは必須です";
    if (!pattern.test(strainCode)) return "形式が正しくありません";
  };
```

**API（FastAPI）**
```python
class StrainCodeValidator:
    @validator('strain_code')
    def validate_format(cls, v):
        if not re.match(r'^ASH-\d{4}-\d{4}$', v):
            raise ValueError('Invalid strain code format')
```

**DB（PostgreSQL）**
```sql
CREATE DOMAIN strain_code AS VARCHAR(20)
  CHECK (VALUE ~ '^ASH-\d{4}-\d{4}$');
```

## 利点

1. **一貫性**: すべての層で同じルールが適用される
2. **保守性**: 定義を変更すれば全層に反映
3. **品質**: 人間のミスを排除
4. **速度**: 実装の自動生成により開発速度向上
5. **理解**: ビジネスロジックが一箇所に集約

## 注意事項

1. **名称の統一**: 必ず「パラソルドメイン言語」と呼称
2. **定義優先**: 実装の前に必ず定義を作成
3. **手動修正禁止**: 生成されたコードは直接編集しない
4. **バージョン管理**: パラソルドメイン言語のみをGit管理

## 今後の展開

1. **AI生成エンジン**: 各言語/フレームワーク向けジェネレータ
2. **整合性検証**: BC間・VS間の自動検証
3. **影響分析**: 変更の影響範囲を自動特定
4. **テスト生成**: 定義からテストケースも自動生成

---

**作成日**: 2025-11-28
**更新日**: 2025-12-10
**バージョン**: V5.3（Actor UseCase / View 用語統一）
**ステータス**: 確定

## 関連ドキュメント

- [capability-bc-test-structure.md](./_software-design-reference/capability-bc-test-structure.md) - 階層構造の詳細定義
- [structured-md-format.md](./_software-design-reference/_templates/structured-md-format.md) - パラソルドメイン言語形式