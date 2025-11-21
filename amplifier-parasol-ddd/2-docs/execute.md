# /ddd:2-docs - アーキテクチャドキュメント生成

## 概要

このフェーズでは、パラソルV4のPhase 3（アプリケーションアーキテクチャ）として、境界コンテキストとAPI仕様を生成します。

## 実行コマンド

```bash
/ddd:2-docs
```

## 実行コンテキスト

### 前提条件
- `/ddd:1-plan`が完了していること
- ケーパビリティマトリクスが定義されていること
- ビジネスオペレーションが明確であること

### 入力
- ケーパビリティマトリクス（1-plan/outputs/）
- ビジネスオペレーション定義
- パラソルドメイン言語

### 出力
- 境界コンテキスト定義
- コンテキストマップ
- API仕様書（OpenAPI）
- サービス契約書

---

## Task 1: 境界コンテキストの導出

CL2ケーパビリティから境界コンテキストを自然に導出します。

```yaml
境界コンテキスト:
  BC-001_PersonalizationContext:
    名称: "パーソナライゼーションコンテキスト"
    由来: CL2-001（パーソナライゼーション）
    責任:
      - ユーザープロファイル管理
      - 推薦ロジック
      - 嗜好学習

    ドメインモデル:
      エンティティ:
        - ユーザー [User] [USER]
        - プロファイル [Profile] [PROFILE]
        - 嗜好 [Preference] [PREFERENCE]

      値オブジェクト:
        - ユーザーID [UserId] [USER_ID]
        - 推薦スコア [RecommendationScore] [RECOMMENDATION_SCORE]

      ドメインイベント:
        - プロファイル作成済み [ProfileCreated] [PROFILE_CREATED]
        - 嗜好更新済み [PreferenceUpdated] [PREFERENCE_UPDATED]

  BC-002_RealtimeProcessingContext:
    名称: "リアルタイム処理コンテキスト"
    由来: CL2-002（リアルタイム処理）
    責任:
      - イベント受信
      - ストリーム処理
      - リアルタイム通知

    ドメインモデル:
      エンティティ:
        - イベント [Event] [EVENT]
        - ストリーム [Stream] [STREAM]

      値オブジェクト:
        - イベントID [EventId] [EVENT_ID]
        - タイムスタンプ [Timestamp] [TIMESTAMP]

  BC-003_AutomationContext:
    名称: "自動化コンテキスト"
    由来: CL2-003（自動化）
    責任:
      - ワークフロー管理
      - タスク自動実行
      - スケジューリング
```

## Task 2: コンテキストマップの作成

```yaml
コンテキストマップ:
  関係:
    PersonalizationContext → RealtimeProcessingContext:
      パターン: "Customer-Supplier"
      説明: "パーソナライゼーションがリアルタイムイベントを消費"
      統合方式: "イベント駆動"

    RealtimeProcessingContext → AutomationContext:
      パターン: "Published Language"
      説明: "イベントストリームを公開"
      統合方式: "イベントバス"

    AutomationContext → PersonalizationContext:
      パターン: "Anticorruption Layer"
      説明: "自動化結果をプロファイル更新に変換"
      統合方式: "API呼び出し"
```

## Task 3: API仕様の生成

```yaml
API仕様:
  PersonalizationAPI:
    basePath: "/api/v1/personalization"

    endpoints:
      POST /profiles:
        summary: "プロファイル作成"
        operationId: "createProfile"
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  userId: string
                  attributes: object
        responses:
          201:
            description: "作成成功"
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Profile"

      GET /profiles/{userId}:
        summary: "プロファイル取得"
        operationId: "getProfile"
        parameters:
          - name: userId
            in: path
            required: true
            schema:
              type: string
        responses:
          200:
            description: "取得成功"

      GET /recommendations/{userId}:
        summary: "推薦取得"
        operationId: "getRecommendations"
        parameters:
          - name: userId
            in: path
            required: true
          - name: limit
            in: query
            schema:
              type: integer
              default: 10
        responses:
          200:
            description: "推薦リスト"

  EventProcessingAPI:
    basePath: "/api/v1/events"

    endpoints:
      POST /events:
        summary: "イベント送信"
        operationId: "publishEvent"
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  eventType: string
                  payload: object
                  timestamp: string
        responses:
          202:
            description: "受信確認"

      WebSocket /streams:
        summary: "イベントストリーム購読"
        description: "WebSocketによるリアルタイムストリーム"
```

## Task 4: サービス契約の定義

```yaml
サービス契約:
  ProfileService:
    契約ID: "SC-001"
    提供者: "PersonalizationContext"
    消費者: ["ClientApplication", "AutomationContext"]

    契約内容:
      機能:
        - プロファイルCRUD操作
        - 推薦生成

      SLA:
        可用性: "99.9%"
        レスポンスタイム: "<500ms (p95)"
        スループット: "1000 req/sec"

      データ契約:
        入力検証: "必須"
        出力形式: "JSON"
        バージョニング: "セマンティック"

  EventService:
    契約ID: "SC-002"
    提供者: "RealtimeProcessingContext"
    消費者: ["PersonalizationContext", "AutomationContext"]

    契約内容:
      機能:
        - イベント配信
        - ストリーム処理

      SLA:
        遅延: "<100ms"
        順序保証: "パーティション内"
        配信保証: "At-least-once"
```

## Task 5: アーキテクチャ決定記録（AADR）

```yaml
AADR-001:
  タイトル: "マイクロサービス境界の決定"
  ステータス: "承認済み"

  コンテキスト:
    CL2ケーパビリティから境界コンテキストを導出

  決定:
    各境界コンテキストを独立したマイクロサービスとして実装

  理由:
    - 独立したデプロイメント
    - スケーラビリティ
    - チーム自律性

  結果:
    - 3つのマイクロサービス
    - API Gatewayによる統合
    - イベント駆動アーキテクチャ
```

---

## 検証チェックリスト

- [ ] 境界コンテキストがケーパビリティと整合しているか
- [ ] コンテキスト間の関係が明確か
- [ ] API仕様が完全で実装可能か
- [ ] サービス契約が現実的か
- [ ] パラソルドメイン言語が一貫して使用されているか

---

## 次のステップ

アーキテクチャドキュメントが生成されたので、ソフトウェア設計の計画に進みます：

```bash
/ddd:3-code-plan 3-code-plan/execute.md
```

---

## 成果物の保存先

```
amplifier-parasol-ddd/
└── 2-docs/
    └── outputs/
        ├── bounded-contexts.yaml
        ├── context-map.yaml
        ├── api-specification.yaml
        ├── service-contracts.yaml
        └── architecture-decisions/
            └── AADR-001.md
```

---

*このドキュメントはAmplifierのDDDワークフローで直接実行できます*