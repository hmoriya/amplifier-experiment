# ケイパビリティ・BC・テスト構造の整合性定義

**Version**: V5.4 (2025-12-27) - Axiomatic Design統合、設計公理チェック機能追加

---

## 1. 概念階層の明確化

### 1.1 Phase別の階層関係

```
┌─────────────────────────────────────────────────────────────────────┐
│ Phase 2: Value Definition（価値定義）                                │
│ ─────────────────────────────────────────────────────────────────── │
│   Value Stream (VStr) = VS0→VS7 の価値フロー全体                     │
│   Value Stage (VS) = 各ステージ（顧客状態）                          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Phase 3: Capability Decomposition（ケイパビリティ分解）              │
│ ─────────────────────────────────────────────────────────────────── │
│                                                                      │
│   CL1: Activity Area（活動領域）                                     │
│   ├── 対象: 経営層                                                   │
│   ├── 分類: Core / Supporting / Generic                             │
│   └── 出力: cl1-domain-classification.md                            │
│              │                                                       │
│              │ 1:N                                                   │
│              ▼                                                       │
│   CL2: Capability（ケイパビリティ）                                   │
│   ├── 対象: 事業部長・PO                                             │
│   ├── 役割: サービス境界候補（≈ Subdomain）                         │
│   └── 出力: cl2-subdomain-design.md                                 │
│              │                                                       │
│              │ 1:N                                                   │
│              ▼                                                       │
│   CL3: Sub-capability + BO（詳細能力 + 業務オペレーション）           │
│   ├── 対象: 業務担当者                                               │
│   ├── 役割: 詳細能力（WHAT）+ 業務活動（HOW: 1日〜1週間単位）        │
│   └── 出力: cl3-business-operations/{capability}-operations.md      │
│                                                                      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                │ N:M（複数CL2から1BCへ統合可能）
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Phase 4: Application Design（アプリケーション設計）                  │
│ ─────────────────────────────────────────────────────────────────── │
│                                                                      │
│   Service（サービス）                                                │
│   ├── 対象: アーキテクト                                             │
│   ├── 役割: デプロイ・運用単位                                       │
│   └── 複数BCを含む可能性あり                                         │
│              │                                                       │
│              │ 1:N                                                   │
│              ▼                                                       │
│   Bounded Context (BC)                                              │
│   ├── 対象: 開発者                                                   │
│   ├── 役割: 技術実装境界                                             │
│   └── 出力: context-map.md, services/{service}/bounded-contexts.md  │
│                                                                      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Phase 5: Software Design（ソフトウェア設計）                         │
│ ─────────────────────────────────────────────────────────────────── │
│                                                                      │
│   BC単位で以下を定義:                                                │
│   ├── domain-language.md      # パラソルドメイン言語（SSOT）         │
│   ├── api-specification.md    # API仕様                             │
│   ├── database-design.md      # DB設計                              │
│   ├── operations/             # オペレーション群                     │
│   │   └── {operation}/                                              │
│   │       ├── operation.md                                          │
│   │       └── actor-usecases/                                       │
│   │           └── {auc}/                                            │
│   │               ├── actor-usecase.md                              │
│   │               ├── robustness.md                                 │
│   │               └── views/                                        │
│   └── tests/                  # テスト定義（設計側）                 │
│       ├── unit-spec.yaml                                            │
│       ├── api-spec.yaml                                             │
│       ├── ui-spec.yaml                                              │
│       └── integration-spec.yaml                                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Capability-BC対応ルール

| 関係パターン | 説明 | 例 |
|-------------|------|-----|
| **1:1対応** | 1つのCL2 Capabilityが1つのBCに対応 | 小規模・単純なケース |
| **N:1統合** | 複数のCL2 Capabilityを1つのBCに統合 | 関連性の高いCapability群 |
| **1:N分割** | 1つのCL2 Capabilityを複数BCに分割 | 複雑・大規模なCapability |

**決定タイミング**: Phase 4（Application Design）で明示的に定義

---

## 2. ディレクトリ構造（統一版）

### 2.1 プロジェクト出力構造

```
projects/{project}/outputs/
│
├── 1-context/                              # Phase 1
│   ├── organization-analysis.md
│   ├── market-assessment.md
│   └── stakeholder-map.md
│
├── 2-value/                                # Phase 2
│   ├── value-streams-mapping.md
│   └── vs{N}-detail.md
│
├── 3-capabilities/                         # Phase 3
│   └── {vs-slug}/
│       ├── cl1-domain-classification.md    # CL1: Core/Supporting/Generic
│       ├── cl2-subdomain-design.md         # CL2: サービス境界候補
│       └── cl3-business-operations/        # CL3: 詳細能力 + BO対応
│           └── {capability}-operations.md
│
├── 4-architecture/                         # Phase 4
│   ├── context-map.md                      # BC間関係
│   ├── capability-bc-mapping.md            # ★ CL2-BC対応表（必須）
│   └── services/
│       └── {service}/
│           └── bounded-contexts.md         # サービス内BC一覧
│
└── 5-software/                             # Phase 5
    └── {service}/
        └── {bc-name}/                      # ★ BCが設計単位
            │
            ├── domain-language.md          # パラソルドメイン言語（SSOT）
            ├── api-specification.md        # API仕様
            ├── database-design.md          # DB設計（生成物）
            │
            ├── operations/                 # オペレーション群
            │   └── {operation-name}/
            │       ├── operation.md        # オペレーション定義
            │       └── actor-usecases/     # Actor UseCase群
            │           └── {auc-name}/     # Actor UseCase
            │               ├── actor-usecase.md
            │               ├── robustness.md
            │               └── views/      # View群
            │                   └── {view}.md
            │
            └── tests/                      # ★ テスト定義（設計側）
                │
                ├── _bc-release-criteria.yaml   # BC全体のリリース基準
                │
                ├── shared/                     # BC共通テスト（ドメインモデル）
                │   └── unit-spec.yaml          # ← domain-language.mdから生成
                │
                └── {operation-name}/           # ★ オペレーション単位（イテレーション単位）
                    ├── _done-criteria.yaml     # オペレーション完了基準（DoD）
                    ├── unit-spec.yaml          # オペレーション固有のユニットテスト
                    ├── api-spec.yaml           # ← operation.mdから生成
                    ├── ui-spec.yaml            # ← pages/*.mdから生成
                    └── integration-spec.yaml   # ← usecases/*.mdから生成
```

### 2.2 実装側ディレクトリ構造

```
services/{service}/
├── src/
│   └── {bc-name}/                          # BC単位のソースコード
│       ├── domain/                         # ドメイン層
│       │   ├── aggregates/
│       │   ├── value_objects/
│       │   ├── events/
│       │   └── services/
│       ├── application/                    # アプリケーション層
│       ├── infrastructure/                 # インフラ層
│       └── presentation/                   # プレゼンテーション層
│
└── tests/                                  # ★ テスト実装（実装側）
    └── {bc-name}/
        │
        ├── shared/                         # BC共通テスト（ドメインモデル）
        │   └── unit/                       # 50%
        │       ├── value_objects/
        │       ├── aggregates/
        │       └── services/
        │
        └── {operation-name}/               # ★ オペレーション単位
            ├── unit/                       # オペレーション固有
            ├── contract/                   # 15% - API契約テスト
            ├── component/                  # 15% - UIコンポーネント
            └── integration/                # 15% - ユースケース統合
```

---

## 3. テスト定義と実装の関係

### 3.1 二層構造の意図

```
┌─────────────────────────────────────────────────────────────────────┐
│ 設計側（outputs/5-software/{service}/{bc}/tests/）                   │
│                                                                      │
│ 役割: テスト仕様の定義（WHAT to test）                               │
│ 形式: YAML（@parasol:test_* マーカー）                               │
│ 担当: 設計者・PO                                                     │
│ 更新: Phase 5 で作成、ビジネス要件変更時に更新                       │
└───────────────────────────────────┬─────────────────────────────────┘
                                    │
                                    │ 生成・参照
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 実装側（services/{service}/tests/）                                  │
│                                                                      │
│ 役割: テストコードの実装（HOW to test）                              │
│ 形式: Python/TypeScript等                                           │
│ 担当: 開発者                                                         │
│ 更新: Phase 6 で生成、技術的詳細の追加時に更新                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 テスト定義の生成フロー（イテレーション対応）

```
Phase 5: Software Design
    │
    ├── domain-language.md ─────────→ tests/shared/unit-spec.yaml（BC共通）
    │
    └── operations/{operation}/
        ├── operation.md ───────────→ tests/{operation}/api-spec.yaml
        ├── actor-usecases/*.md ───→ tests/{operation}/integration-spec.yaml
        └── views/*.md ─────────────→ tests/{operation}/ui-spec.yaml

Phase 6: Implementation（イテレーション単位で実行）
    │
    ├── tests/shared/unit-spec.yaml ─────→ services/tests/{bc}/shared/unit/*.py
    │
    └── tests/{operation}/ ──────────────→ services/tests/{bc}/{operation}/
        ├── api-spec.yaml ───────────────→ contract/*.py
        ├── ui-spec.yaml ────────────────→ component/*.spec.ts
        └── integration-spec.yaml ───────→ integration/*.py
```

### 3.3 イテレーションとリリースの関係

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ BC: product-catalog                                                         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ イテレーション1: create-product                                      │   │
│  │                                                                      │   │
│  │  Phase 5: 設計                    Phase 6: 実装                      │   │
│  │  ┌────────────────────┐          ┌────────────────────┐             │   │
│  │  │ operation.md       │    →     │ src/application/   │             │   │
│  │  │ actor-usecases/*.md│          │ src/presentation/  │             │   │
│  │  │ views/*.md         │          └────────────────────┘             │   │
│  │  └────────────────────┘                   ↓                          │   │
│  │           ↓                      ┌────────────────────┐             │   │
│  │  ┌────────────────────┐          │ tests実装          │             │   │
│  │  │ tests/create-product/│   →    │ ├─ contract/       │             │   │
│  │  │ ├─ api-spec.yaml   │          │ ├─ component/      │             │   │
│  │  │ ├─ ui-spec.yaml    │          │ └─ integration/    │             │   │
│  │  │ └─ integration-spec│          └────────────────────┘             │   │
│  │  └────────────────────┘                   ↓                          │   │
│  │                                  ┌────────────────────┐             │   │
│  │                                  │ _done-criteria.yaml│             │   │
│  │                                  │ ✅ 全テストPass    │             │   │
│  │                                  └────────────────────┘             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                          ↓                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ イテレーション2: search-products  （同様の流れ）                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                          ↓                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ BCリリース判定: _bc-release-criteria.yaml                            │   │
│  │                                                                      │   │
│  │  operations:                                                         │   │
│  │    - create-product:  ✅ done                                        │   │
│  │    - search-products: ✅ done                                        │   │
│  │    - manage-categories: ✅ done                                      │   │
│  │  shared-tests: ✅ pass                                               │   │
│  │  e2e-scenarios: ✅ pass                                              │   │
│  │                                                                      │   │
│  │  → BC READY FOR RELEASE                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.4 完了基準ファイル形式

#### オペレーション完了基準（_done-criteria.yaml）

```yaml
# tests/{operation}/_done-criteria.yaml
operation: create-product
version: "1.0"

criteria:
  unit_tests:
    required: true
    coverage_min: 80%
  api_tests:
    required: true
    endpoints_covered: all
  ui_tests:
    required: true
    pages_covered: all
  integration_tests:
    required: true
    scenarios_covered: all

status: pending  # pending | in_progress | done
completed_at: null
```

#### BCリリース基準（_bc-release-criteria.yaml）

```yaml
# tests/_bc-release-criteria.yaml
bc: product-catalog
version: "1.0"

operations:
  - name: create-product
    status: done
    completed_at: "2025-12-10"
  - name: search-products
    status: done
    completed_at: "2025-12-11"
  - name: manage-categories
    status: in_progress
    completed_at: null

shared_tests:
  domain_model: pass

release_criteria:
  all_operations_done: false
  shared_tests_pass: true
  e2e_scenarios_pass: false

release_ready: false
```

---

## 4. パラソルドメイン言語の配置ルール

### 4.1 配置場所（統一）

**正**: `outputs/5-software/{service}/{bc-name}/domain-language.md`

**誤**: ~~`outputs/3-capabilities/{vs}/cl3-bounded-contexts/{bc}-domain-language.md`~~

### 4.2 理由

1. **Single Source of Truth**: Phase 5 が技術設計の中心
2. **BC単位の管理**: ドメイン言語はBC内で完結
3. **生成物との近接**: 同一ディレクトリからDB設計・テスト定義を生成

### 4.3 Phase 3 との関係

```
Phase 3: CL3 Business Operations
    │
    │ ビジネス要件の収集
    │ （業務担当者の言葉で記述）
    │
    ▼
Phase 5: パラソルドメイン言語
    │
    │ 技術用語への変換
    │ （開発者が実装可能な精度で記述）
    │
    ▼
自動生成: ドメインモデル、ER図、状態遷移図
```

---

## 5. 命名規則

### 5.1 ディレクトリ・ファイル命名

| 対象 | 規則 | 例 |
|------|------|-----|
| VS番号 | `vs{N}` (N=0-7) | `vs2`, `vs5` |
| VS slug | kebab-case | `product-development`, `customer-service` |
| Capability | kebab-case | `fermentation-research`, `quality-control` |
| BC名 | kebab-case | `product-catalog`, `order-management` |
| Service名 | kebab-case | `brewing-service`, `sales-service` |
| Operation | kebab-case | `create-product`, `approve-order` |
| Actor UseCase | kebab-case | `auc-create-product`, `auc-search-products` |

### 5.2 BC命名の一本化

**正**: `{bc-name}` (例: `product-catalog`)

**誤**: ~~`{capability-name}-bc`~~ (例: ~~`product-management-bc`~~)

---

## 6. Phase間の成果物トレーサビリティ

```
Phase 2: VS定義
    │
    │ vs2-detail.md
    │   └── VS2: 製品開発（選好形成）
    │
    ▼
Phase 3: Capability分解
    │
    │ cl2-subdomain-design.md
    │   └── Capability: fermentation-research（発酵研究）
    │
    │ cl3-business-operations/fermentation-research-operations.md
    │   └── Operations: 菌株培養、発酵モニタリング、品質検査
    │
    ▼
Phase 4: BC確定
    │
    │ capability-bc-mapping.md
    │   └── fermentation-research → fermentation-bc
    │
    │ context-map.md
    │   └── fermentation-bc ←[U/D]→ quality-bc
    │
    ▼
Phase 5: ソフトウェア設計
    │
    │ fermentation-bc/domain-language.md
    │   └── Aggregates: Strain, FermentationBatch, QualityResult
    │
    │ fermentation-bc/tests/unit-spec.yaml
    │   └── test_strain.yaml, test_fermentation_batch.yaml
    │
    ▼
Phase 6: 実装
    │
    │ services/brewing-service/tests/unit/fermentation-bc/
    │   └── test_strain.py, test_fermentation_batch.py
```

---

## 7. 移行ガイド

### 7.1 既存プロジェクトの移行

1. **Phase 3 配置のドメイン言語を Phase 5 に移動**
   ```bash
   mv outputs/3-capabilities/*/cl3-bounded-contexts/*-domain-language.md \
      outputs/5-software/{service}/{bc}/domain-language.md
   ```

2. **テスト定義を BC 直下に集約**
   ```bash
   mkdir -p outputs/5-software/{service}/{bc}/tests/
   # 既存のテスト定義を移動
   ```

3. **capability-bc-mapping.md を作成**
   ```bash
   touch outputs/4-architecture/capability-bc-mapping.md
   # CL2 → BC の対応関係を記述
   ```

### 7.2 新規プロジェクトの推奨手順

1. Phase 3 で CL1/CL2/CL3 を定義（業務観点）
2. Phase 4 で capability-bc-mapping.md を作成（技術観点）
3. Phase 5 で BC 単位にディレクトリを作成
4. Phase 5 で domain-language.md を作成
5. Phase 5 で tests/ ディレクトリにテスト定義を生成
6. Phase 6 で実装側 tests/ にテストコードを生成

---

## 関連ドキュメント

- [business-operations.md](./business-operations.md) - 階層構造の詳細
- [structured-md-format.md](./_templates/structured-md-format.md) - パラソルドメイン言語形式
- [test-definition-format.md](./_templates/test-definition-format.md) - テスト定義形式
