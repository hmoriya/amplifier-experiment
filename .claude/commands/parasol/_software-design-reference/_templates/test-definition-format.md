# Parasol V5 テスト定義形式仕様

**解析エンジン対応・Mermaid非依存・パラソルドメイン言語連携**

---

## テスト階層と責務

### テストピラミッド

```
                    ▲  5%   E2E/シナリオテスト
                   /░\      ビジネスオペレーションテスト
                  /░░░\
                 /░░░░░\
                /───────\   15%  統合テスト（Actor UseCase）
               /░░░░░░░░░\       AUC基本/代替/例外フロー
              /░░░░░░░░░░░\
             /─────────────\  15%  UIテスト
            /░░░░░░░░░░░░░░░\      View/コンポーネント
           /░░░░░░░░░░░░░░░░░\
          /───────────────────\  15%  APIテスト
         /░░░░░░░░░░░░░░░░░░░░░\      契約/エンドポイント
        /░░░░░░░░░░░░░░░░░░░░░░░\
       /─────────────────────────\  50%  ユニットテスト
      /░░░░░░░░░░░░░░░░░░░░░░░░░░░\      ドメインモデル
     └───────────────────────────────┘
```

### 階層対応表

| パラソル設計層 | テスト種別 | 比率 | 実行頻度 |
|--------------|-----------|------|---------|
| パラソルドメイン言語 | ユニットテスト | 50% | 毎コミット |
| API仕様 | APIテスト | 15% | 毎コミット |
| View定義 | UIテスト | 15% | 毎コミット |
| Actor UseCase定義 | 統合テスト | 15% | 毎PR/日次 |
| ビジネスオペレーション | E2Eテスト | 5% | リリース前 |

---

## 1. ドメインモデルテスト（Unit Test）

### 1.1 Value Objectテスト

```yaml
# @parasol:test_value_object
test_value_object:
  target: ProductName
  source: "@parasol:value_objects/ProductName"

  validation_tests:
    - id: T-VO-001
      name: 正常値テスト
      category: positive
      inputs:
        - value: "有効な製品名"
          expected: valid
        - value: "A"
          expected: valid
          note: 最小長
        - value: "あ" * 200
          expected: valid
          note: 最大長

    - id: T-VO-002
      name: 異常値テスト
      category: negative
      inputs:
        - value: ""
          expected: invalid
          error: "製品名は必須です"
        - value: "   "
          expected: invalid
          error: "空白のみは不可"
        - value: "あ" * 201
          expected: invalid
          error: "200文字以内"
        - value: null
          expected: invalid
          error: "製品名は必須です"

    - id: T-VO-003
      name: 境界値テスト
      category: boundary
      inputs:
        - value: "A"
          expected: valid
          boundary: min_length
        - value: "A" * 200
          expected: valid
          boundary: max_length
        - value: "A" * 201
          expected: invalid
          boundary: max_length + 1

  equality_tests:
    - id: T-VO-004
      name: 等価性テスト
      cases:
        - a: "製品A"
          b: "製品A"
          expected: equal
        - a: "製品A"
          b: "製品B"
          expected: not_equal
```

### 1.2 Aggregateテスト

```yaml
# @parasol:test_aggregate
test_aggregate:
  target: Product
  source: "@parasol:aggregates/Product"

  invariant_tests:
    - id: T-AGG-001
      name: 不変条件-名前長制約
      source_invariant: "INV-001"
      cases:
        - setup:
            name: "A" * 201
          action: create
          expected: failure
          error: "名前は200文字以内"

    - id: T-AGG-002
      name: 不変条件-アクティブ時画像必須
      source_invariant: "INV-002"
      cases:
        - setup:
            status: Active
            images: []
          action: validate
          expected: failure
          error: "アクティブ製品は画像が必要"
        - setup:
            status: Active
            images: [image1]
          action: validate
          expected: success

  behavior_tests:
    - id: T-AGG-003
      name: 振る舞い-新規作成
      source_behavior: "create"
      cases:
        - inputs:
            name: "テスト製品"
            categoryId: "cat-001"
          expected:
            status: Draft
            createdAt: not_null
          events:
            - ProductCreated

    - id: T-AGG-004
      name: 振る舞い-アクティブ化
      source_behavior: "activate"
      precondition_tests:
        - case: 画像なし
          setup:
            images: []
          expected: failure
          error: "事前条件違反: has_image"
        - case: 画像あり
          setup:
            images: [image1]
          expected: success
          result:
            status: Active
          events:
            - ProductActivated
```

### 1.3 Domain Serviceテスト

```yaml
# @parasol:test_domain_service
test_domain_service:
  target: ProductSearchService
  source: "@parasol:domain_services/ProductSearchService"

  method_tests:
    - id: T-SVC-001
      name: キーワード検索
      method: searchByKeyword
      cases:
        - inputs:
            keyword: "ビール"
            filters: { status: Active }
          expected:
            type: List<Product>
            constraints:
              - all_items_contain: "ビール"
              - all_items_status: Active

    - id: T-SVC-002
      name: 類似製品検索
      method: searchBySimilarity
      cases:
        - inputs:
            productId: "prod-001"
          expected:
            type: List<Product>
            constraints:
              - not_contains: "prod-001"
              - max_count: 10
```

---

## 2. APIテスト（Contract Test）

```yaml
# @parasol:test_api
test_api:
  target: ProductAPI
  base_path: /api/v1/products
  source: "@api-specification"

  endpoint_tests:
    - id: T-API-001
      name: 製品作成-正常系
      endpoint: POST /
      request:
        headers:
          Authorization: "Bearer {valid_token}"
          Content-Type: "application/json"
        body:
          title: "新製品"
          categoryId: "cat-001"
          priority: "HIGH"
      expected:
        status: 201
        body:
          id: matches("[a-f0-9-]{36}")
          title: "新製品"
          status: "Draft"
          createdAt: matches(ISO8601)
        headers:
          Location: matches("/api/v1/products/.*")

    - id: T-API-002
      name: 製品作成-バリデーションエラー
      endpoint: POST /
      request:
        body:
          title: ""
          categoryId: "cat-001"
      expected:
        status: 400
        body:
          success: false
          error:
            code: "VALIDATION_ERROR"
            details:
              - field: "title"
                message: contains("必須")

    - id: T-API-003
      name: 製品作成-認証エラー
      endpoint: POST /
      request:
        headers:
          Authorization: null
        body:
          title: "製品"
      expected:
        status: 401
        body:
          error:
            code: "UNAUTHORIZED"

    - id: T-API-004
      name: 製品作成-重複エラー
      endpoint: POST /
      precondition:
        existing_product:
          title: "既存製品"
      request:
        body:
          title: "既存製品"
      expected:
        status: 409
        body:
          error:
            code: "DUPLICATE_ERROR"

  schema_tests:
    - id: T-API-005
      name: レスポンススキーマ検証
      endpoint: GET /{id}
      expected:
        schema:
          type: object
          required: [id, title, status, createdAt]
          properties:
            id:
              type: string
              format: uuid
            title:
              type: string
            status:
              type: string
              enum: [Draft, Active, Discontinued]
```

---

## 3. UIテスト（Component Test）

```yaml
# @parasol:test_ui
test_ui:
  target: ProductCreationView
  source: "@parasol:views/product-creation"

  render_tests:
    - id: T-UI-001
      name: フォーム表示テスト
      assertions:
        - element: "input[name='title']"
          visible: true
          attributes:
            required: true
            maxLength: 200
        - element: "select[name='category']"
          visible: true
          options_count: ">= 1"
        - element: "button[type='submit']"
          visible: true
          text: "作成"

  validation_ui_tests:
    - id: T-UI-002
      name: クライアントバリデーション表示
      actions:
        - action: clear
          target: "input[name='title']"
        - action: blur
          target: "input[name='title']"
      assertions:
        - element: ".error-message[for='title']"
          visible: true
          text: contains("必須")

    - id: T-UI-003
      name: 文字数カウント表示
      actions:
        - action: type
          target: "input[name='title']"
          value: "テスト製品名"
      assertions:
        - element: ".char-count"
          text: "6/200"

  action_tests:
    - id: T-UI-004
      name: 送信アクション
      setup:
        mock_api:
          endpoint: POST /api/v1/products
          response:
            status: 201
            body: { id: "new-id" }
      actions:
        - action: fill
          target: "input[name='title']"
          value: "新製品"
        - action: select
          target: "select[name='category']"
          value: "cat-001"
        - action: click
          target: "button[type='submit']"
      assertions:
        - api_called:
            endpoint: POST /api/v1/products
            body:
              title: "新製品"
              categoryId: "cat-001"
        - navigate_to: "/products/new-id"

    - id: T-UI-005
      name: キャンセルアクション
      actions:
        - action: click
          target: "button.cancel"
      assertions:
        - navigate_to: "/products"
        - no_api_calls: true

  accessibility_tests:
    - id: T-UI-006
      name: WCAG 2.1 AA準拠
      checks:
        - rule: "color-contrast"
          level: "AA"
        - rule: "label"
          description: "全入力項目にラベルあり"
        - rule: "keyboard-navigation"
          description: "Tab順序が論理的"
```

---

## 4. Actor UseCaseテスト（Integration Test）

```yaml
# @parasol:test_actor_usecase
test_actor_usecase:
  target: AUC-001-ProductCreation
  source: "@parasol:actor-usecases/product-creation"

  basic_flow_test:
    - id: T-UC-001
      name: 基本フロー完走
      source_flow: "basic_flow"
      steps:
        - step: 1
          action: navigate
          to: "/products/new"
          verify:
            page: ProductCreationPage

        - step: 2
          action: fill_form
          data:
            title: "テスト製品"
            category: "cat-001"
            description: "説明文"

        - step: 3
          action: submit
          verify:
            api_call:
              method: POST
              endpoint: /api/v1/products

        - step: 4
          action: verify_result
          assertions:
            - success_message: visible
            - redirect_to: matches("/products/[a-f0-9-]+")
            - db_state:
                table: products
                where: { title: "テスト製品" }
                exists: true

  alternative_flow_tests:
    - id: T-UC-002
      name: 代替フロー-バリデーションエラー
      source_flow: "ALT-001"
      branch_from: 3
      steps:
        - step: "3a1"
          action: fill_form
          data:
            title: ""

        - step: "3a2"
          action: submit
          verify:
            error_displayed: true
            error_field: "title"

        - step: "3a3"
          action: fix_input
          data:
            title: "修正後の製品名"

        - step: "return"
          action: submit
          verify:
            success: true

    - id: T-UC-003
      name: 代替フロー-同名製品警告
      source_flow: "ALT-002"
      precondition:
        db_seed:
          - table: products
            data: { title: "既存製品" }
      steps:
        - step: "3b1"
          action: fill_form
          data:
            title: "既存製品"

        - step: "3b2"
          action: submit
          verify:
            warning_dialog: visible
            message: contains("同名の製品")

        - step: "3b3"
          action: click
          target: "button.confirm"
          verify:
            success: true

  exception_flow_tests:
    - id: T-UC-004
      name: 例外フロー-サーバーエラー
      source_flow: "EXC-001"
      setup:
        mock_api:
          endpoint: POST /api/v1/products
          response:
            status: 500
            body: { error: "Internal Server Error" }
      steps:
        - step: "trigger"
          action: submit_valid_form

        - step: "6e1"
          verify:
            error_page: visible
            message: contains("エラーが発生")

        - step: "6e2"
          action: click
          target: "button.retry"
          verify:
            api_retry: true
```

---

## 5. ビジネスオペレーションテスト（E2E Test）

```yaml
# @parasol:test_business_operation
test_business_operation:
  target: OP-001-CustomerOnboarding
  source: "@parasol:operations/customer-onboarding"

  scenario_test:
    - id: T-BO-001
      name: 顧客オンボーディング完走
      actors:
        - id: customer
          role: 新規顧客
        - id: cs_staff
          role: CSスタッフ
        - id: compliance
          role: コンプライアンス担当

      steps:
        - phase: "UC-001実行"
          actor: customer
          usecase: AccountCreation
          actions:
            - navigate: "/signup"
            - fill_form:
                email: "test@example.com"
                password: "SecurePass123!"
            - submit: true
          verify:
            - account_created: true
            - email_sent: "verification"

        - phase: "メール認証"
          actor: customer
          actions:
            - click_email_link: "verification"
          verify:
            - account_verified: true

        - phase: "UC-002実行"
          actor: customer
          usecase: IdentityVerification
          actions:
            - upload_document: "id_card.jpg"
            - submit: true
          verify:
            - status: "pending_review"

        - phase: "本人確認審査"
          actor: compliance
          actions:
            - navigate: "/admin/verifications"
            - select_case: "test@example.com"
            - approve: true
          verify:
            - status: "verified"
            - notification_sent: customer

        - phase: "UC-003実行"
          actor: customer
          usecase: InitialSetup
          actions:
            - complete_wizard: true
          verify:
            - onboarding_complete: true
            - can_access_service: true

      kpi_assertions:
        - metric: completion_rate
          expected: ">= 95%"
        - metric: avg_duration
          expected: "<= 48h"

  failure_scenario_tests:
    - id: T-BO-002
      name: 本人確認却下シナリオ
      steps:
        # ... 却下フローのステップ
```

---

## 6. テスト生成マッピング

### パラソルドメイン言語 → テスト生成対応表

| ソース定義 | 生成テスト | 自動生成可能性 |
|-----------|----------|---------------|
| `@parasol:value_objects` | `@parasol:test_value_object` | **高** - constraints/validation |
| `@parasol:aggregates.invariants` | `@parasol:test_aggregate.invariant_tests` | **高** |
| `@parasol:aggregates.behaviors` | `@parasol:test_aggregate.behavior_tests` | **高** |
| `@parasol:domain_services` | `@parasol:test_domain_service` | **中** |
| `@parasol:repositories` | `@parasol:test_repository` | **中** |
| API仕様 | `@parasol:test_api` | **高** |
| View定義 | `@parasol:test_ui` | **中** |
| `@parasol:actor_usecase_flow` | `@parasol:test_actor_usecase` | **中** |
| ビジネスオペレーション | `@parasol:test_business_operation` | **低** |

### 生成ルール

```yaml
# @parasol:test_generation_rules
generation_rules:
  value_object:
    from: "@parasol:value_objects"
    generate:
      - type: boundary_test
        source: constraints.min/max
        pattern: "[min, min-1, max, max+1]"
      - type: pattern_test
        source: constraints.pattern
        pattern: "[valid_match, invalid_match]"
      - type: enum_test
        source: values
        pattern: "[all_values, invalid_value]"

  aggregate:
    from: "@parasol:aggregates"
    generate:
      - type: invariant_test
        source: invariants
        pattern: "violation_cases"
      - type: behavior_test
        source: behaviors
        pattern: "precondition + action + postcondition"
      - type: event_test
        source: behaviors
        pattern: "verify_event_published"

  actor_usecase:
    from: "@parasol:actor_usecase_flow"
    generate:
      - type: happy_path_test
        source: basic_flow
        pattern: "step_by_step_execution"
      - type: alternative_test
        source: alternative_flows
        pattern: "branch_execution"
      - type: exception_test
        source: exception_flows
        pattern: "error_handling_verification"
```

---

## 7. テスト実行単位と品質ゲート

### 実行単位

```yaml
# @parasol:test_execution
test_execution:
  units:
    - name: unit_tests
      scope: ドメインモデル
      files: "tests/unit/**/*.py"
      trigger: every_commit
      timeout: 5min
      parallelism: high

    - name: api_tests
      scope: API契約
      files: "tests/contract/**/*.py"
      trigger: every_commit
      timeout: 10min
      parallelism: medium
      dependencies: [unit_tests]

    - name: ui_tests
      scope: UIコンポーネント
      files: "tests/component/**/*.spec.ts"
      trigger: every_commit
      timeout: 15min
      parallelism: medium
      dependencies: [unit_tests]

    - name: integration_tests
      scope: Actor UseCase統合
      files: "tests/integration/**/*.py"
      trigger: every_pr
      timeout: 30min
      parallelism: low
      dependencies: [unit_tests, api_tests, ui_tests]
      environment: test_db

    - name: e2e_tests
      scope: ビジネスオペレーション
      files: "tests/e2e/**/*.spec.ts"
      trigger: pre_release
      timeout: 60min
      parallelism: none
      dependencies: [integration_tests]
      environment: staging
```

### 品質ゲート

```yaml
# @parasol:quality_gates
quality_gates:
  unit_tests:
    coverage: ">= 80%"
    pass_rate: "100%"
    mutation_score: ">= 70%"

  api_tests:
    endpoint_coverage: "100%"
    pass_rate: "100%"
    response_time: "p95 < 500ms"

  ui_tests:
    view_coverage: "100%"
    accessibility: "WCAG 2.1 AA"
    pass_rate: ">= 95%"

  integration_tests:
    flow_coverage:
      basic: "100%"
      alternative: ">= 90%"
      exception: ">= 80%"
    pass_rate: ">= 95%"

  e2e_tests:
    scenario_coverage: "100%"
    pass_rate: "100%"
    response_time: "p95 < 3s"
```

---

## 8. ディレクトリ構造

```
tests/
├── unit/                               # 50% - ユニットテスト
│   ├── domain/
│   │   ├── value_objects/
│   │   │   └── test_{vo_name}.py       # @parasol:test_value_object
│   │   ├── aggregates/
│   │   │   └── test_{agg_name}.py      # @parasol:test_aggregate
│   │   └── services/
│   │       └── test_{svc_name}.py      # @parasol:test_domain_service
│   └── application/
│       └── test_{app_service}.py
│
├── contract/                           # 15% - API契約テスト
│   └── api/
│       └── test_{endpoint}_contract.py # @parasol:test_api
│
├── component/                          # 15% - UIコンポーネントテスト
│   └── views/
│       └── {view_name}.spec.ts         # @parasol:test_ui
│
├── integration/                        # 15% - 統合テスト
│   └── actor-usecases/
│       └── test_{auc_id}.py            # @parasol:test_actor_usecase
│
├── e2e/                               # 5% - E2Eテスト
│   └── scenarios/
│       └── {operation_id}.spec.ts      # @parasol:test_business_operation
│
└── fixtures/                          # テストデータ
    ├── seeds/                         # DBシード
    └── mocks/                         # モックレスポンス
```

---

## 9. パーサー実装ガイド

### テスト定義抽出

```python
# テストYAMLブロック抽出
import re
import yaml

TEST_MARKER_PATTERN = r"```yaml\n# @parasol:(test_\w+)\n(.*?)```"

def extract_test_definitions(md_content: str) -> dict:
    """Markdown内のテスト定義を抽出"""
    tests = {}
    for match in re.finditer(TEST_MARKER_PATTERN, md_content, re.DOTALL):
        test_type = match.group(1)
        yaml_content = match.group(2)
        tests[test_type] = yaml.safe_load(yaml_content)
    return tests
```

### テストコード生成スケルトン

```python
def generate_test_skeleton(test_def: dict, test_type: str) -> str:
    """テスト定義からテストコードスケルトン生成"""
    if test_type == "test_value_object":
        return generate_vo_test(test_def)
    elif test_type == "test_aggregate":
        return generate_aggregate_test(test_def)
    elif test_type == "test_api":
        return generate_api_test(test_def)
    # ...
```

---

## 10. Consulting Toolsからの移行

| Consulting Tools形式 | Parasol V5形式 |
|---------------------|----------------|
| テスト仕様書（Word/Excel） | `@parasol:test_*` YAML |
| テストケース表 | `@parasol:test_*.cases` |
| E2Eシナリオ手順書 | `@parasol:test_business_operation` |
