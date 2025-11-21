# 02. パラソルドメイン開発プロジェクト（Parasol Domain Development）

## 概要
パラソルV4フレームワークにおける「サービス・オペレーション・ページ」の3層構造を、Amplifierの自動生成機能で実装するプロジェクトです。ドメイン言語の確立から、実装コードの自動生成まで一貫したドメイン駆動開発を実現します。

## パラソルドメインの3層構造

```
Services（CL2: マイクロサービス）
    ↓ 提供
Operations（CL3: ビジネスオペレーション）
    ↓ 実装
Pages（L4: ユースケース/画面）
```

## ディレクトリ構造
```
02-parasol-domain/
├── services/               # マイクロサービス定義
│   ├── customer-service/       # 顧客サービス
│   ├── product-service/        # 商品サービス
│   ├── order-service/          # 注文サービス
│   └── notification-service/   # 通知サービス
├── operations/             # ビジネスオペレーション
│   ├── crud-operations/        # CRUD操作
│   ├── workflow-operations/    # ワークフロー
│   ├── analytics-operations/   # 分析操作
│   └── collaboration-ops/      # コラボレーション
├── pages/                  # ページ/ユースケース
│   ├── customer-pages/         # 顧客向けページ
│   ├── admin-pages/            # 管理者向けページ
│   └── mobile-pages/           # モバイルページ
└── domain-language/        # ドメイン言語
    ├── entities/               # エンティティ定義
    ├── value-objects/          # バリューオブジェクト
    ├── aggregates/             # 集約定義
    └── ubiquitous-language.md # ユビキタス言語
```

## サービス層（CL2）の設計

### マイクロサービス定義テンプレート
```yaml
# services/customer-service/service-definition.yaml
microservice:
  id: "ms-customer-service"
  name: "顧客サービス"
  capability_level: "CL2"

  bounded_context: "顧客管理"

  responsibilities:
    - 顧客情報の管理
    - 顧客プロファイルの維持
    - 顧客セグメンテーション
    - 顧客行動分析

  api_gateway:
    base_path: "/api/v1/customers"
    authentication: "Bearer Token"
    rate_limiting: "1000 req/min"

  data_store:
    primary: "PostgreSQL"
    cache: "Redis"
    search: "Elasticsearch"

  integrations:
    - service: "ms-notification-service"
      type: "async"
      protocol: "event-bus"
    - service: "ms-order-service"
      type: "sync"
      protocol: "REST"

  operations:
    - cl3-create-customer-profile
    - cl3-update-customer-information
    - cl3-segment-customers
    - cl3-analyze-customer-behavior
```

## オペレーション層（CL3）の設計

### ビジネスオペレーション定義
```yaml
# operations/crud-operations/create-customer-profile.yaml
operation:
  level: "CL3"
  id: "cl3-create-customer-profile"
  name: "顧客プロファイルを作成する"
  parent_service: "ms-customer-service"

  pattern: "CRUD"
  sub_pattern: "Create-with-validation"

  specification:
    trigger:
      type: "user_action"
      source: "registration_form"

    input:
      - name: "customer_data"
        type: "CustomerRegistration"
        required: true
        validation:
          - email_format
          - phone_number_format
          - age_range_check

    process:
      steps:
        1: "入力データの検証"
        2: "重複チェック"
        3: "プロファイル作成"
        4: "初期セグメント割り当て"
        5: "ウェルカムイベント発行"

    output:
      success:
        - type: "CustomerProfile"
        - status_code: 201
      error:
        - DUPLICATE_EMAIL: 409
        - VALIDATION_ERROR: 400

  business_rules:
    - BR-001: "同一メールアドレスの重複登録は不可"
    - BR-002: "年齢は18歳以上"
    - BR-003: "必須フィールドはすべて入力必要"

  pages:
    - l4-registration-page
    - l4-profile-confirmation-page
```

## ページ層（L4）の設計

### ページ/ユースケース定義
```yaml
# pages/customer-pages/registration-page.yaml
page:
  level: "L4"
  id: "l4-registration-page"
  name: "顧客登録ページ"
  parent_operation: "cl3-create-customer-profile"

  type: "form"
  platform: ["web", "mobile"]

  components:
    header:
      - Logo
      - Navigation

    main:
      - RegistrationForm:
          fields:
            - email: { type: "email", required: true }
            - password: { type: "password", min_length: 8 }
            - name: { type: "text", required: true }
            - phone: { type: "tel", format: "international" }
            - birthdate: { type: "date", max: "today-18years" }

          validation:
            - real_time: ["email", "password"]
            - on_submit: "all_fields"

      - ProgressIndicator:
          steps: ["基本情報", "詳細情報", "確認"]

    footer:
      - TermsAndConditions
      - PrivacyPolicy
      - ContactSupport

  api_calls:
    - endpoint: "POST /api/v1/customers"
      trigger: "form_submit"
      payload: "form_data"

    - endpoint: "GET /api/v1/customers/check-email"
      trigger: "email_blur"
      payload: { email: "input_value" }

  user_flow:
    entry_points:
      - homepage_signup_button
      - marketing_campaign_link

    success_path:
      - registration_page
      - confirmation_page
      - welcome_dashboard

    error_handling:
      - validation_error: "inline_message"
      - network_error: "retry_modal"
      - duplicate_email: "suggestion_modal"
```

## ドメイン言語の定義

### エンティティとバリューオブジェクト
```yaml
# domain-language/entities/customer.yaml
entity:
  name: "Customer"
  id: "CustomerId"

  attributes:
    - customerId: CustomerId
    - profile: CustomerProfile
    - segments: CustomerSegment[]
    - lifecycle: CustomerLifecycle
    - preferences: CustomerPreferences

  invariants:
    - "顧客は少なくとも1つのセグメントに属する"
    - "ライフサイクルステージは順序に従って遷移する"

  behaviors:
    - updateProfile(data: ProfileUpdate): Result<CustomerProfile>
    - assignSegment(segment: CustomerSegment): Result<void>
    - progressLifecycle(): Result<CustomerLifecycle>

value_objects:
  CustomerId:
    type: "uuid"
    generation: "auto"

  CustomerProfile:
    attributes:
      - email: Email
      - name: PersonName
      - phone: PhoneNumber
      - birthdate: Date
      - registeredAt: DateTime

  CustomerSegment:
    type: "enum"
    values: ["新規", "アクティブ", "休眠", "VIP", "離脱リスク"]

  CustomerLifecycle:
    stages: ["認知", "検討", "購入", "利用", "推奨", "離脱"]
    transitions:
      - from: "認知", to: "検討", condition: "first_interaction"
      - from: "検討", to: "購入", condition: "first_purchase"
```

### ユビキタス言語辞書
```markdown
# domain-language/ubiquitous-language.md

## コアコンセプト

### 顧客（Customer）
**定義**: サービスを利用する個人または法人
**属性**:
- プロファイル: 基本的な個人情報
- セグメント: 行動や属性に基づく分類
- ライフサイクル: 顧客関係の成熟度

### オペレーション（Operation）
**定義**: ビジネス目的を達成するための一連の処理
**タイプ**:
- CRUD: データの作成・読取・更新・削除
- Workflow: 複数ステップの処理フロー
- Analytics: データ分析と洞察生成
- Collaboration: 複数アクターの協調作業

### ページ（Page）
**定義**: ユーザーインターフェースの単位
**要素**:
- コンポーネント: UI部品
- APIコール: バックエンド連携
- ユーザーフロー: 画面遷移
```

## Amplifierによる自動生成

### ドメインモデルからコード生成
```bash
# エンティティからTypeScriptクラス生成
amplifier generate-entity --input=domain-language/entities/ --output=src/domain/

# 生成例
class Customer {
  private readonly id: CustomerId;
  private profile: CustomerProfile;
  private segments: CustomerSegment[];

  updateProfile(data: ProfileUpdate): Result<CustomerProfile> {
    // Amplifierが生成したビジネスロジック
  }
}
```

### オペレーションからAPI生成
```bash
# オペレーション定義からRESTful API生成
amplifier generate-api --operations=operations/ --output=src/api/

# 生成例
@Controller('/api/v1/customers')
export class CustomerController {
  @Post('/')
  async createCustomerProfile(@Body() data: CustomerRegistration) {
    // Amplifierが生成した処理フロー
  }
}
```

### ページからReactコンポーネント生成
```bash
# ページ定義からReactコンポーネント生成
amplifier generate-pages --pages=pages/ --output=src/components/

# 生成例
export const RegistrationPage: React.FC = () => {
  const [formData, setFormData] = useState<CustomerRegistration>();

  const handleSubmit = async () => {
    // Amplifierが生成したAPI呼び出しロジック
  };

  return (
    <Form onSubmit={handleSubmit}>
      {/* Amplifierが生成したフォームフィールド */}
    </Form>
  );
};
```

## テストの自動生成

### ドメインテスト
```typescript
// 自動生成される不変条件テスト
describe('Customer Entity', () => {
  test('顧客は少なくとも1つのセグメントに属する', () => {
    // Amplifierが生成したテストケース
  });
});
```

### オペレーションテスト
```typescript
// ビジネスルールのテスト
describe('Create Customer Profile Operation', () => {
  test('同一メールアドレスの重複登録は不可', () => {
    // Amplifierが生成したテストケース
  });
});
```

## ベストプラクティス

1. **サービス境界の明確化**: マイクロサービスは単一の境界づけられたコンテキストを持つ
2. **オペレーションパターンの活用**: CRUD、Workflow、Analyticsなどのパターンを適切に選択
3. **ページの再利用性**: コンポーネント化により複数ページで再利用
4. **ドメイン言語の一貫性**: すべての層で同じ用語を使用
5. **段階的な詳細化**: CL2→CL3→L4の順序で詳細化

## Tips
- Amplifierの知識グラフでドメイン関係を可視化
- メタ認知レシピでオペレーションフローを標準化
- Git worktreeで複数サービスを並行開発
- AIエージェントによるドメイン分析支援