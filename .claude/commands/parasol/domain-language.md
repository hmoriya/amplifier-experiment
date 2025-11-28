# /parasol:domain-language - パラソルドメイン言語コマンド

## 概要

パラソルドメイン言語の定義を作成・更新・検証するコマンドです。Phase 3（CL3）で定義されたBounded Contextに対して、アーキテクチャ非依存のドメインモデル定義を作成します。

## 使用方法

```bash
# 基本的な使い方
/parasol:domain-language [action] [options]

# アクション
create   # 新規パラソルドメイン言語定義を作成
update   # 既存の定義を更新
validate # 定義の整合性を検証
generate # UI/API/DBコードを生成
```

## 前提条件

- Phase 3（CL3）のBounded Context定義が完了していること
- プロジェクトがParasolで初期化されていること

## コマンド詳細

### 1. create - 新規作成

```bash
/parasol:domain-language create [VS名] [BC名]
```

**例:**
```bash
/parasol:domain-language create vs2-product-innovation fermentation-research-bc
```

**生成されるファイル:**
```
outputs/3-capabilities/{vs-name}/cl3-bounded-contexts/
├── {bc-name}.md                    # 既存のCL3定義
└── {bc-name}-domain-language.md    # 新規作成
```

### 2. update - 更新

```bash
/parasol:domain-language update [VS名] [BC名]
```

既存のパラソルドメイン言語定義を更新します。

### 3. validate - 検証

```bash
/parasol:domain-language validate [VS名] [BC名]
```

**検証項目:**
- Aggregateの不変条件
- Value Objectsの型定義
- Domain Eventsの整合性
- Repositoriesのメソッド定義
- ユビキタス言語の一貫性

### 4. generate - コード生成

```bash
/parasol:domain-language generate [VS名] [BC名] [target]

# target options:
# - ui     # UI層のコード生成
# - api    # API層のコード生成
# - db     # DB層のコード生成
# - all    # 全層のコード生成（デフォルト）
```

**例:**
```bash
# 全層のコード生成
/parasol:domain-language generate vs2-product-innovation fermentation-research-bc

# API層のみ生成
/parasol:domain-language generate vs2-product-innovation fermentation-research-bc api
```

## パラソルドメイン言語の構造

### 1. Aggregates（集約）

```yaml
Root Entity: {EntityName}
Description: {説明}

Properties:
  - {propertyName}: {Type} ({説明})

Invariants:
  - {不変条件}

Behaviors:
  - {methodName}(): {説明}
```

### 2. Value Objects（値オブジェクト）

```yaml
{ValueObjectName}:
  Type: {型}
  Validation: {検証ルール}
  Format: {フォーマット}
```

### 3. Domain Events（ドメインイベント）

```yaml
{EventName}:
  Description: {説明}
  Properties:
    - {property}: {Type}
  Trigger: {発生条件}
  Subscribers: [{BC名}]
  VS間: Yes/No
```

### 4. Domain Services（ドメインサービス）

```yaml
Responsibility: {責務}
Methods:
  - {methodName}({params}):
      Input: {入力}
      Output: {出力}
      Logic: {ロジック概要}
```

### 5. Repositories（リポジトリ）

```yaml
Methods:
  - save({entity}: {Type}): void
  - findById(id: {IdType}): {EntityType}
  - {domainSpecificMethod}(): {ReturnType}
```

### 6. ユビキタス言語辞書

| 日本語 | 英語 | 定義 |
|--------|------|------|
| {用語} | {Term} | {定義} |

## 生成されるコードの例

### UI層（React/TypeScript）

```typescript
// 自動生成: YeastStrain Form Component
interface YeastStrainForm {
  strainCode: string; // Format: ASH-YYYY-NNNN
  name: string;       // 1-100文字
  
  validate(): ValidationResult {
    // Invariantsから生成されたバリデーション
  }
}
```

### API層（FastAPI/Python）

```python
# 自動生成: YeastStrain API
@router.post("/strains")
async def register_strain(dto: RegisterStrainDto):
    # Behaviorsから生成されたエンドポイント
    # Invariantsのビジネスルール適用
```

### DB層（PostgreSQL）

```sql
-- 自動生成: YeastStrain Table
CREATE TABLE yeast_strains (
  strain_id UUID PRIMARY KEY,
  strain_code VARCHAR(20) UNIQUE,
  -- Value Object制約の適用
  CONSTRAINT strain_code_format 
    CHECK (strain_code ~ '^ASH-\d{4}-\d{4}$')
);
```

## ワークフロー

1. **Phase 3でCL3定義を完了**
   ```bash
   /parasol:3-capabilities cl3 {vs-name} {subdomain-name}
   ```

2. **パラソルドメイン言語を作成**
   ```bash
   /parasol:domain-language create {vs-name} {bc-name}
   ```

3. **定義を編集・洗練**
   - 生成されたファイルを手動で編集
   - ビジネスルールを追加

4. **検証**
   ```bash
   /parasol:domain-language validate {vs-name} {bc-name}
   ```

5. **コード生成**
   ```bash
   /parasol:domain-language generate {vs-name} {bc-name}
   ```

## 注意事項

1. **名称の一貫性**: 必ず「パラソルドメイン言語」と呼称
2. **DDDとの区別**: DDDの「ドメイン言語」とは異なる概念
3. **再生成可能性**: 生成されたコードは直接編集せず、常に定義から再生成
4. **バージョン管理**: パラソルドメイン言語定義のみをGit管理

## 関連コマンド

- `/parasol:3-capabilities` - CL3定義の作成
- `/parasol:5-software` - ソフトウェア設計
- `/parasol:validate` - プロジェクト全体の検証

## トラブルシューティング

### エラー: "CL3定義が見つかりません"

Phase 3のCL3定義を先に完了してください:
```bash
/parasol:3-capabilities cl3 {vs-name} {subdomain-name}
```

### エラー: "型定義が不整合です"

Value Objectsの型定義を確認し、一貫性を保ってください。

---

**ステータス**: 実装準備中
**バージョン**: V5対応