# パラソル開発フレームワーク - 各フェーズの詳細ステップ

## Phase 1: 価値分析 (Value Analysis)

### Step 1.1: ステークホルダー分析

**入力**:
- プロジェクト概要
- ビジネス目標

**活動**:
1. ステークホルダーリストアップ
2. 影響度と関心度のマッピング
3. 各ステークホルダーの価値観分析
4. コミュニケーション戦略策定

**出力**:
```yaml
stakeholders:
  primary:
    - name: プロジェクトマネージャー
      interest: high
      influence: high
      values: [効率性, 透明性, 制御性]
  secondary:
    - name: 開発チーム
      interest: medium
      influence: medium
      values: [生産性, 学習機会, 自動化]
```

### Step 1.2: 価値提案の定義

**入力**:
- ステークホルダー分析結果
- 市場分析

**活動**:
1. 各ステークホルダーへの価値提案作成
2. 価値の優先順位付け
3. 価値間のトレードオフ分析
4. 統合価値提案の作成

**出力**:
```yaml
value_propositions:
  core:
    statement: "プロジェクト成功率を30%向上"
    metrics:
      - success_rate_improvement
      - time_to_market_reduction
  supporting:
    - efficiency_improvement
    - quality_enhancement
```

### Step 1.3: KPI設定

**入力**:
- 価値提案
- ビジネス目標

**活動**:
1. 測定可能な指標の識別
2. ベースラインの設定
3. 目標値の設定
4. 測定方法の定義

**出力**:
```yaml
kpis:
  - id: KPI-001
    name: プロジェクト完了率
    baseline: 65%
    target: 95%
    measurement: 完了プロジェクト数/全プロジェクト数
    frequency: monthly
```

## Phase 2: 能力設計 (Capability Design)

### Step 2.1: L1戦略的能力の識別

**入力**:
- 価値定義
- ビジネス戦略

**活動**:
1. トップレベル能力のブレインストーミング
2. 価値との関連付け
3. 能力の統合と整理
4. 戦略的重要度の評価

**出力**:
```yaml
L1_capabilities:
  - id: L1-001
    name: プロジェクト成功実現能力
    strategic_importance: critical
    value_contribution: high
```

### Step 2.2: L2戦術的能力への分解

**入力**:
- L1能力リスト

**活動**:
1. 各L1能力のWHAT-HOW分析
2. L2能力の識別
3. 能力間の関係定義
4. 実現可能性の評価

**出力**:
```yaml
L2_capabilities:
  parent: L1-001
  children:
    - id: L2-001
      name: タスク管理能力
      implementation_complexity: medium
    - id: L2-002
      name: リソース最適化能力
      implementation_complexity: high
```

### Step 2.3: L3運用能力の定義

**入力**:
- L2能力リスト
- 現場業務分析

**活動**:
1. 運用レベルの能力識別
2. 能力と操作の関係定義
3. 実装パターンの選択
4. リソース要件の定義

**出力**:
```yaml
L3_capabilities:
  - id: L3-001
    name: タスク作成・管理能力
    parent: L2-001
    operations:
      - create_task
      - update_task
      - assign_task
    pattern: CRUD_Workflow_hybrid
```

## Phase 3: ドメインモデリング (Domain Modeling)

### Step 3.1: 境界コンテキストの識別

**入力**:
- 能力マップ
- ドメイン知識

**活動**:
1. コンテキストマッピング
2. 境界の定義
3. コンテキスト間の関係分析
4. 統合パターンの選択

**出力**:
```yaml
bounded_contexts:
  - name: TaskManagement
    type: core
    capabilities: [L3-001, L3-002]
    integration_pattern: shared_kernel
```

### Step 3.2: エンティティの定義

**入力**:
- 境界コンテキスト
- ビジネスルール

**活動**:
1. エンティティの識別
2. 属性の定義
3. 振る舞いの定義
4. 不変条件の定義

**出力**:
```typescript
entity Task {
  id: TaskId
  title: string
  status: TaskStatus
  // 不変条件
  invariants: [
    "タイトルは空であってはならない",
    "ステータス遷移は定義されたフローに従う"
  ]
}
```

### Step 3.3: 集約の設計

**入力**:
- エンティティリスト
- トランザクション境界

**活動**:
1. 集約ルートの識別
2. 集約境界の定義
3. 一貫性境界の設計
4. リポジトリインターフェース定義

**出力**:
```yaml
aggregates:
  - name: TaskAggregate
    root: Task
    entities: [Task, TaskAssignment, TaskComment]
    consistency_boundary: immediate
```

## Phase 4: オペレーション設計 (Operation Design)

### Step 4.1: 操作の識別

**入力**:
- L3能力
- ユースケース

**活動**:
1. 能力から操作を導出
2. 操作の粒度調整
3. 操作の分類
4. 優先順位付け

**出力**:
```yaml
operations:
  - id: OP-001
    name: create_task
    capability: L3-001
    priority: high
    category: CRUD
```

### Step 4.2: パターン適用

**入力**:
- 操作リスト
- パターンカタログ

**活動**:
1. 各操作へのパターンマッチング
2. パターンの選択
3. パターンのカスタマイズ
4. パターン適用の検証

**出力**:
```yaml
operation_patterns:
  OP-001:
    pattern: create_with_validation
    customizations:
      - async_processing
      - event_emission
```

### Step 4.3: API設計

**入力**:
- 操作定義
- 非機能要件

**活動**:
1. エンドポイント設計
2. リクエスト/レスポンス定義
3. エラーハンドリング設計
4. 認証・認可設計

**出力**:
```yaml
api:
  /tasks:
    post:
      operationId: createTask
      request:
        schema: CreateTaskRequest
      response:
        schema: TaskResponse
      security: [bearer_auth]
```

## Phase 5: 実装生成 (Implementation Generation)

### Step 5.1: テクノロジー選択

**入力**:
- 非機能要件
- 技術制約

**活動**:
1. 技術スタック評価
2. フレームワーク選択
3. ライブラリ選択
4. 開発環境構築

**出力**:
```yaml
technology_stack:
  backend:
    language: TypeScript
    framework: NestJS
    database: PostgreSQL
  frontend:
    framework: Next.js
    ui_library: shadcn/ui
```

### Step 5.2: コード生成

**入力**:
- 設計成果物
- テンプレート

**活動**:
1. テンプレート選択
2. パラメータ注入
3. コード生成実行
4. 生成結果の検証

**出力**:
- generated/src/
- generated/tests/
- generated/docs/

### Step 5.3: テスト生成

**入力**:
- 生成コード
- テストパターン

**活動**:
1. テストケース導出
2. テストコード生成
3. テストデータ生成
4. テスト実行

**出力**:
```typescript
describe('Task Creation', () => {
  it('should create task with valid data', async () => {
    // Generated test code
  });
});
```

## Phase 6: 検証と最適化 (Validation & Optimization)

### Step 6.1: ビジネスルール検証

**入力**:
- 実装コード
- ビジネスルール定義

**活動**:
1. ルール実装の確認
2. エッジケーステスト
3. 統合テスト実行
4. ビジネス承認

**出力**:
```yaml
validation_results:
  business_rules:
    total: 25
    passed: 25
    coverage: 100%
```

### Step 6.2: パフォーマンス最適化

**入力**:
- パフォーマンステスト結果
- 目標値

**活動**:
1. ボトルネック分析
2. 最適化実施
3. 再測定
4. 結果評価

**出力**:
```yaml
performance:
  api_response_time:
    p50: 45ms
    p95: 120ms
    p99: 250ms
  throughput: 1000req/s
```

### Step 6.3: フィードバック統合

**入力**:
- 検証結果
- ユーザーフィードバック

**活動**:
1. フィードバック分析
2. 改善点の識別
3. ナレッジベース更新
4. 次回への反映

**出力**:
```yaml
feedback_integration:
  patterns_updated: 5
  templates_improved: 3
  new_patterns_identified: 2
  knowledge_base_entries: 8
```

## チェックポイントとゲート条件

### Phase間の移行条件

```yaml
phase_gates:
  value_to_capability:
    required:
      - value_definition: approved
      - kpis: defined
      - stakeholders: identified

  capability_to_domain:
    required:
      - L3_capabilities: complete
      - dependencies: analyzed
      - feasibility: confirmed

  domain_to_operation:
    required:
      - bounded_contexts: defined
      - domain_model: validated
      - aggregates: designed

  operation_to_implementation:
    required:
      - operations: catalogued
      - patterns: selected
      - api: designed

  implementation_to_validation:
    required:
      - code: generated
      - tests: passing
      - documentation: complete
```

このフェーズごとの詳細ステップにより、体系的かつ再現可能な開発プロセスが実現されます。