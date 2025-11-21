# /ddd:3-code-plan - ソフトウェア設計計画

## 概要

このフェーズでは、パラソルV4のPhase 4（ソフトウェア設計）として、詳細なドメインモデルとL4ユースケースを設計します。

## 実行コマンド

```bash
/ddd:3-code-plan
```

## 実行コンテキスト

### 前提条件
- `/ddd:2-docs`が完了していること
- 境界コンテキストが定義されていること
- API仕様が明確であること

### 入力
- 境界コンテキスト（2-docs/outputs/）
- ビジネスオペレーション（1-plan/outputs/）
- API仕様

### 出力
- 詳細ドメインモデル
- L4ユースケース
- データベース設計
- UIコンポーネント設計

---

## Task 1: L3→L4 ZIGZAG変換

CL3ビジネスオペレーションからL4ユースケースへ詳細化します。

```yaml
L4ユースケース導出:
  CL3-001_ユーザープロファイル管理:
    L4-001: "新規ユーザー登録"
      アクター: エンドユーザー
      前提条件: メールアドレス未登録
      基本フロー:
        1. ユーザーが登録フォームを開く
        2. 必要情報を入力
        3. システムが検証
        4. プロファイル作成
        5. 確認メール送信
      事後条件: ユーザーアカウント有効化

    L4-002: "プロファイル更新"
      アクター: 認証済みユーザー
      前提条件: ログイン済み
      基本フロー:
        1. プロファイル画面を開く
        2. 情報を編集
        3. 変更を保存
        4. 更新確認
      事後条件: プロファイル更新完了

    L4-003: "プロファイル削除"
      アクター: 認証済みユーザー
      前提条件: 削除権限あり
      基本フロー:
        1. 削除要求
        2. 確認ダイアログ
        3. 再認証
        4. 削除実行
        5. データアーカイブ
      事後条件: アカウント無効化
```

## Task 2: 詳細ドメインモデル設計

```yaml
ドメインモデル詳細:
  PersonalizationContext:
    集約_User:
      ルート: User

      エンティティ:
        User:
          属性:
            - userId: UserId
            - email: Email
            - profile: Profile
            - preferences: List<Preference>
            - createdAt: Timestamp
            - updatedAt: Timestamp

          ビジネスルール:
            - メールアドレスは一意
            - プロファイルは必須
            - 削除は論理削除

        Profile:
          属性:
            - profileId: ProfileId
            - firstName: Name
            - lastName: Name
            - birthDate: Date
            - location: Location
            - attributes: Map<String, Any>

      値オブジェクト:
        Email:
          検証: RFC5322準拠

        UserId:
          形式: UUID v4

        Location:
          属性:
            - country: CountryCode
            - city: String
            - timezone: TimeZone

    集約_Recommendation:
      ルート: Recommendation

      エンティティ:
        Recommendation:
          属性:
            - recommendationId: RecommendationId
            - userId: UserId
            - items: List<RecommendedItem>
            - score: Score
            - generatedAt: Timestamp
            - expiresAt: Timestamp
```

## Task 3: データベース設計

```yaml
データベース設計:
  PersonalizationDB:
    タイプ: PostgreSQL

    テーブル:
      users:
        columns:
          - user_id: UUID PRIMARY KEY
          - email: VARCHAR(255) UNIQUE NOT NULL
          - created_at: TIMESTAMP NOT NULL
          - updated_at: TIMESTAMP NOT NULL
          - deleted_at: TIMESTAMP

        indexes:
          - idx_email: (email)
          - idx_created_at: (created_at)

      profiles:
        columns:
          - profile_id: UUID PRIMARY KEY
          - user_id: UUID REFERENCES users(user_id)
          - first_name: VARCHAR(100)
          - last_name: VARCHAR(100)
          - birth_date: DATE
          - location: JSONB
          - attributes: JSONB
          - updated_at: TIMESTAMP

      preferences:
        columns:
          - preference_id: UUID PRIMARY KEY
          - user_id: UUID REFERENCES users(user_id)
          - category: VARCHAR(50)
          - value: JSONB
          - weight: DECIMAL(3,2)

  EventStoreDB:
    タイプ: EventStore/Kafka

    トピック:
      user-events:
        パーティション: 10
        レプリケーション: 3
        保持期間: 30日
```

## Task 4: UIコンポーネント設計

```yaml
UIコンポーネント:
  ProfileManagement:
    ProfileForm:
      タイプ: "フォームコンポーネント"

      props:
        - user: User
        - onSubmit: Function
        - onCancel: Function

      フィールド:
        - firstName: TextInput
        - lastName: TextInput
        - email: EmailInput
        - birthDate: DatePicker
        - location: LocationSelector

      バリデーション:
        - 必須フィールドチェック
        - Email形式検証
        - 年齢制限チェック

    ProfileView:
      タイプ: "表示コンポーネント"

      props:
        - profile: Profile
        - editable: boolean

      セクション:
        - 基本情報
        - 連絡先
        - 設定
        - アクティビティ

  RecommendationDisplay:
    RecommendationList:
      タイプ: "リストコンポーネント"

      props:
        - recommendations: List<Recommendation>
        - onItemClick: Function

      機能:
        - 無限スクロール
        - フィルタリング
        - ソート
```

## Task 5: 技術スタック決定

```yaml
技術スタック:
  バックエンド:
    言語: TypeScript/Node.js
    フレームワーク: NestJS
    ORM: TypeORM

  フロントエンド:
    フレームワーク: Next.js 14
    状態管理: Zustand
    UIライブラリ: Tailwind CSS + shadcn/ui

  インフラ:
    コンテナ: Docker
    オーケストレーション: Kubernetes
    クラウド: AWS

  開発ツール:
    パッケージマネージャ: pnpm
    ビルドツール: Vite
    テスト: Jest + Playwright
```

## Task 6: ソフトウェアアーキテクチャ決定記録（SADR）

```yaml
SADR-001:
  タイトル: "ヘキサゴナルアーキテクチャの採用"
  ステータス: "承認済み"

  コンテキスト:
    ドメインロジックの独立性を保つ必要がある

  決定:
    各マイクロサービスでヘキサゴナルアーキテクチャを採用

  理由:
    - ドメインロジックの保護
    - テスタビリティ
    - 外部依存の交換可能性

SADR-002:
  タイトル: "イベントソーシングの部分採用"
  ステータス: "承認済み"

  決定:
    重要なドメインイベントのみイベントソーシング

  理由:
    - 監査証跡の必要性
    - 履歴の再生可能性
    - パフォーマンスとのバランス
```

---

## 検証チェックリスト

- [ ] L4ユースケースが完全で実装可能か
- [ ] ドメインモデルがビジネス要件を満たすか
- [ ] データベース設計が正規化されているか
- [ ] UIコンポーネントがユーザビリティを考慮しているか
- [ ] 技術スタックが要件に適合しているか

---

## 次のステップ

ソフトウェア設計が完了したので、実装フェーズに進みます：

```bash
/ddd:4-code 4-code/execute.md
```

---

## 成果物の保存先

```
amplifier-parasol-ddd/
└── 3-code-plan/
    └── outputs/
        ├── l4-use-cases.yaml
        ├── domain-models.yaml
        ├── database-design.yaml
        ├── ui-components.yaml
        ├── tech-stack.yaml
        └── architecture-decisions/
            ├── SADR-001.md
            └── SADR-002.md
```

---

*このドキュメントはAmplifierのDDDワークフローで直接実行できます*