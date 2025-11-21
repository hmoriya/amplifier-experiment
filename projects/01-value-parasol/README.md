# 01. 価値パラソルプロジェクト（Value Parasol Project）

## 概要
パラソルフレームワークV4の中核となる「価値駆動型開発」を、Amplifierのメタ認知レシピと知識管理機能で実装するプロジェクトです。WHAT-HOW ZIGZAG構造により、ビジネス戦略から実装まで一貫した価値の実現を支援します。

## パラソルV4フレームワークの階層構造

```
CL1: 戦略ケーパビリティ（ビジネス価値）
  ↘️
    HOW → CL2: 戦術ケーパビリティ（機能要件）
            ↘️
              HOW → CL3: ビジネスオペレーション（業務フロー）
                      ↘️
                        HOW → L4: 詳細ユースケース（実装仕様）
```

## ディレクトリ構造
```
01-value-parasol/
├── value-streams/           # バリューストリーム定義
│   ├── vs-customer-lifecycle/    # 顧客ライフサイクル
│   │   ├── st0-foundation/      # 基盤ステージ
│   │   ├── st1-engagement/      # エンゲージメント
│   │   ├── st2-understanding/   # 理解ステージ
│   │   ├── st3-optimization/    # 最適化ステージ
│   │   ├── st4-realization/     # 実現ステージ
│   │   ├── st5-habituation/     # 習慣化ステージ
│   │   └── st6-co-creation/     # 共創ステージ
│   └── value-declaration.md     # 価値宣言
├── templates/               # パラソルテンプレート
│   ├── capability-template.yaml
│   ├── operation-template.yaml
│   └── domain-language-template.yaml
└── cross-cutting/          # 横断的関心事
    ├── security/
    ├── observability/
    └── compliance/
```

## 価値パラソルの実装フロー

### 1. バリューストリーム定義
```yaml
# value-streams/vs-customer-lifecycle/value-declaration.md
value_stream:
  name: 顧客ライフサイクル価値創出
  mission: 顧客の成功を支援し、共に成長する
  vision: すべての顧客が価値を実感し、ビジネス成果を達成

  stages:
    - st0-foundation: 基盤構築
    - st1-engagement: 初期エンゲージメント
    - st2-understanding: 顧客理解深化
    - st3-optimization: 価値最適化
    - st4-realization: 価値実現
    - st5-habituation: 価値習慣化
    - st6-co-creation: 価値共創
```

### 2. ケーパビリティレベル設計（CL1→CL2→CL3）

#### CL1: 戦略ケーパビリティ
```yaml
capability:
  level: "CL1"
  id: "cl1-digital-customer-touchpoint"
  name: "デジタル顧客タッチポイント"
  business_value:
    - 顧客エンゲージメント率30%向上
    - 顧客満足度スコア4.5以上
    - 顧客獲得コスト20%削減
```

#### CL2: 戦術ケーパビリティ（マイクロサービス）
```yaml
capability:
  level: "CL2"
  id: "cl2-ms-digital-customer-touchpoint"
  name: "デジタル顧客タッチポイントサービス"
  parent: "cl1-digital-customer-touchpoint"

  microservice_definition:
    bounded_context: "顧客エンゲージメント"
    technology_stack:
      - language: TypeScript
      - framework: Next.js
      - database: PostgreSQL
      - cache: Redis
```

#### CL3: ビジネスオペレーション
```yaml
operation:
  level: "CL3"
  id: "cl3-website-operation"
  name: "Webサイト運営"
  parent: "cl2-ms-digital-customer-touchpoint"

  pattern: "Workflow"
  specification:
    trigger:
      type: "user_action"
      description: "顧客がWebサイトにアクセス"

    process:
      steps:
        - コンテンツ配信
        - ユーザー行動追跡
        - パーソナライゼーション
        - エンゲージメント測定
```

### 3. L4詳細ユースケース生成
```yaml
usecase:
  level: "L4"
  id: "l4-view-product-catalog"
  name: "商品カタログ閲覧"
  parent_operation: "cl3-website-operation"

  pages:
    - page_id: "product-list"
      components:
        - ProductGrid
        - FilterPanel
        - SearchBar

    - page_id: "product-detail"
      components:
        - ProductGallery
        - ProductInfo
        - ReviewSection

  api_endpoints:
    - GET /api/products
    - GET /api/products/{id}
    - GET /api/products/{id}/reviews
```

## Amplifierを活用した価値実現

### 知識グラフによる価値トレーサビリティ
```bash
# 価値の関係性を可視化
make knowledge-graph-build --source=value-streams/
make knowledge-graph-viz --type=value-traceability

# 価値実現パスの探索
make knowledge-graph-path FROM="business_value" TO="implementation"
```

### メタ認知レシピによる自動生成
```markdown
# recipes/generate-parasol-structure.md
## Purpose
バリューストリームからパラソル構造を自動生成

## Steps
1. **価値分析**: ビジネス価値を特定し測定可能な指標に変換
2. **ケーパビリティ分解**: CL1→CL2→CL3の階層的分解
3. **オペレーション設計**: ビジネスオペレーションの詳細化
4. **ユースケース生成**: L4レベルの実装仕様生成
5. **ページ/サービス設計**: UIとAPIの設計

## Output
- ケーパビリティ定義書
- オペレーション仕様書
- ユースケース設計書
- ドメイン言語辞書
```

### AIエージェントによる価値検証
```bash
# 価値メトリクスの収集と分析
amplifier analyze-value-metrics --stage=all

# 価値ギャップの特定
amplifier identify-value-gaps --target=customer_satisfaction

# 改善提案の生成
amplifier suggest-improvements --focus=engagement
```

## パラソルドメイン言語

### エンティティ定義
```yaml
parasol_domain:
  entities:
    Customer:
      attributes:
        - id: CustomerId
        - profile: CustomerProfile
        - lifecycle_stage: LifecycleStage

    ValueStream:
      attributes:
        - stages: Stage[]
        - milestones: Milestone[]
        - metrics: ValueMetric[]

  value_objects:
    CustomerId: uuid
    LifecycleStage: enum[Foundation|Engagement|Understanding|...]
    ValueMetric:
      - name: string
      - current: number
      - target: number
      - unit: string
```

### ビジネスルール
```yaml
business_rules:
  - id: BR-001
    name: "ライフサイクル進行条件"
    rule: "顧客は前のステージの完了条件を満たさない限り次のステージに進めない"

  - id: BR-002
    name: "価値測定頻度"
    rule: "価値メトリクスは最低週次で測定される"
```

## 成功指標（KPI）

### ビジネスKPI
- 顧客ライフタイムバリュー（LTV）: 200%向上
- 顧客満足度（CSAT）: 4.5/5.0以上
- ネットプロモータースコア（NPS）: +50以上

### 技術KPI
- ページロード時間: 1秒以内
- API応答時間: 100ms以内（p95）
- システム可用性: 99.99%

### プロセスKPI
- 価値実現までのリードタイム: 2週間以内
- デプロイ頻度: 日次
- 変更失敗率: 5%以下

## ベストプラクティス

1. **価値ファースト思考**: すべての決定を価値メトリクスに基づいて行う
2. **段階的詳細化**: WHAT-HOW ZIGZAG構造に従って段階的に詳細化
3. **継続的検証**: 各ステージで価値の実現を検証
4. **クロスファンクショナル**: 横断的関心事を早期に統合
5. **データ駆動**: メトリクスに基づく継続的改善

## Tips
- Amplifierの知識グラフで価値の流れを可視化
- Git worktreeで複数のバリューストリームを並行開発
- AIエージェントによる価値分析の自動化
- メタ認知レシピでパラソル構造を自動生成