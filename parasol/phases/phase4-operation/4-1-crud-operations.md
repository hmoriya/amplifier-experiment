# Phase 4-1: CRUD操作設計

## 実行コンテキスト

このドキュメントは、各ドメインモデルに対するCRUD（Create/Read/Update/Delete）操作を設計するための実行可能なMarkdownです。

### 前提条件
- Phase 3のドメインモデリングが完了していること
- エンティティと集約が定義されていること
- ドメインイベントが識別されていること

### 実行方法
```bash
/ddd:1-plan parasol/phases/phase4-operation/4-1-crud-operations.md
```

---

## 入力：ドメインモデルからの要求

### 主要集約
1. **CarbonFootprint**: CO2排出量管理
2. **ProductDevelopment**: 商品開発管理
3. **ConsumerHealth**: 消費者健康管理
4. **MarketEntry**: 市場参入管理

---

## タスク：CRUD操作の定義

### 実行ステップ

#### Step 1: CarbonFootprint CRUD操作

##### Create操作
```yaml
操作名: CreateCarbonFootprint
入力:
  command: RecordCarbonFootprintCommand
    - productId: string
    - scope1Emission: number
    - scope2Emission: number
    - scope3Emission: number
    - measurementDate: date
    - measurementMethod: string
検証:
  - productIdの存在確認
  - 排出量の妥当性チェック（前回比±50%以内）
  - 測定日の重複チェック
処理:
  1. 入力データの検証
  2. 総排出量の計算
  3. 削減目標との差分計算
  4. エンティティ生成
  5. データベース保存
  6. イベント発行: CarbonFootprintRecorded
出力:
  - footprintId: string
  - status: "created"
  - totalEmission: number
エラー:
  - InvalidProductId
  - DuplicateMeasurement
  - InvalidEmissionValue
```

##### Read操作
```yaml
操作名: GetCarbonFootprint
クエリパターン:
  1. 単一取得:
     - input: footprintId
     - output: CarbonFootprintDTO

  2. 製品別履歴:
     - input: productId, dateRange
     - output: List<CarbonFootprintDTO>

  3. 集計クエリ:
     - input: aggregationType, period
     - output: EmissionSummaryDTO

レスポンス形式:
  CarbonFootprintDTO:
    - footprintId: string
    - productId: string
    - totalEmission: number
    - trend: "increasing" | "stable" | "decreasing"
    - certificationStatus: object
    - lastUpdated: datetime

キャッシュ戦略:
  - 単一取得: 1時間
  - 履歴データ: 24時間
  - 集計データ: 6時間
```

##### Update操作
```yaml
操作名: UpdateCarbonFootprint
入力:
  command: UpdateFootprintCommand
    - footprintId: string
    - updates: {
        scope1Emission?: number
        scope2Emission?: number
        scope3Emission?: number
        certificationStatus?: object
      }
    - reason: string
検証:
  - footprintIdの存在確認
  - 更新権限の確認
  - 監査ログの必須化
処理:
  1. 現在のエンティティ取得
  2. 楽観的ロック確認
  3. 変更の適用
  4. 再計算（総排出量）
  5. データベース更新
  6. イベント発行: CarbonFootprintUpdated
  7. 監査ログ記録
出力:
  - status: "updated"
  - previousValues: object
  - newValues: object
```

##### Delete操作
```yaml
操作名: DeleteCarbonFootprint
入力:
  command: DeleteFootprintCommand
    - footprintId: string
    - reason: string
    - approvedBy: string
検証:
  - 削除権限の確認（管理者のみ）
  - 関連データの確認
  - 承認プロセスの完了確認
処理:
  1. ソフトデリート（論理削除）
  2. deletedAt, deletedBy記録
  3. アーカイブテーブルへ移動
  4. イベント発行: CarbonFootprintDeleted
出力:
  - status: "deleted"
  - archivedId: string
制約:
  - 物理削除は90日後に実行
  - 監査証跡は永続保持
```

#### Step 2: ProductDevelopment CRUD操作

##### Create操作
```yaml
操作名: CreateDevelopmentProject
入力:
  command: StartProjectCommand
    - projectName: string
    - category: string
    - healthClaims: array
    - targetLaunchDate: date
    - budget: number
ワークフロー:
  1. プロジェクト承認
  2. リソース割当
  3. 初期ステージ設定
  4. チーム編成
出力:
  - projectId: string
  - stage: "ideation"
  - assignedTeam: object
```

##### Read操作（パイプラインビュー）
```yaml
操作名: GetDevelopmentPipeline
クエリタイプ:
  1. ステージ別一覧:
     - input: stage
     - output: ProjectsByStageDTO

  2. ガントチャート用:
     - input: dateRange
     - output: ProjectTimelineDTO

  3. リソース配分:
     - input: teamId
     - output: ResourceAllocationDTO

特殊ビュー:
  ダッシュボード用集計:
    - 進行中プロジェクト数
    - ステージ別分布
    - 遅延プロジェクト
    - 今月のゲート審査
```

#### Step 3: API仕様の定義

##### RESTful API設計
```yaml
基本エンドポイント:
  CarbonFootprint:
    POST   /api/v1/carbon-footprints
    GET    /api/v1/carbon-footprints/{id}
    GET    /api/v1/carbon-footprints?productId={id}
    PUT    /api/v1/carbon-footprints/{id}
    DELETE /api/v1/carbon-footprints/{id}

  ProductDevelopment:
    POST   /api/v1/projects
    GET    /api/v1/projects/{id}
    GET    /api/v1/projects/pipeline
    PUT    /api/v1/projects/{id}/stage
    DELETE /api/v1/projects/{id}

レスポンス形式:
  成功:
    {
      "status": "success",
      "data": { ... },
      "metadata": {
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0"
      }
    }

  エラー:
    {
      "status": "error",
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "詳細メッセージ",
        "field": "scope1Emission"
      }
    }
```

#### Step 4: バッチ操作の設計

```yaml
一括インポート:
  操作名: BulkImportCarbonFootprints
  入力:
    - csvFile: file
    - validationMode: "strict" | "lenient"
  処理:
    1. ファイル解析
    2. バリデーション
    3. トランザクション処理
    4. 結果レポート生成
  出力:
    - imported: number
    - failed: number
    - errors: array

一括更新:
  操作名: BulkUpdateProjects
  入力:
    - filter: object
    - updates: object
  処理:
    1. 対象抽出
    2. プレビュー生成
    3. 承認待機
    4. 更新実行
  制限:
    - 最大1000件/バッチ
    - タイムアウト: 5分
```

#### Step 5: 監査とセキュリティ

```yaml
監査ログ:
  記録項目:
    - userId: 実行者
    - operation: CRUD種別
    - entityType: 対象エンティティ
    - entityId: 対象ID
    - timestamp: 実行日時
    - ipAddress: IPアドレス
    - changes: 変更内容
    - result: 成功/失敗

アクセス制御:
  ロールベース:
    Admin:
      - 全CRUD操作可能
      - 削除承認権限
    Manager:
      - CRU操作可能
      - 削除申請のみ
    Viewer:
      - R操作のみ

  データレベル:
    - 所属組織のデータのみ
    - 承認済みプロジェクトのみ
```

---

## 出力：CRUD操作定義書

### 生成する成果物
1. CRUD操作マトリクス（全エンティティ）
2. API仕様書（OpenAPI形式）
3. データフロー図
4. エラーハンドリングガイド
5. セキュリティポリシー

### 保存先
```
projects/asahi-parasol-development/
└── phase4-operation-design/
    ├── crud-operations.md
    ├── api-specification.yaml
    └── security-policy.md
```

---

## 検証項目

- [ ] すべての集約にCRUD操作が定義されているか
- [ ] 入力検証が十分か
- [ ] エラーハンドリングが網羅的か
- [ ] パフォーマンス要件を満たすか
- [ ] セキュリティ要件を満たすか

---

## 次のステップ

このCRUD操作定義が承認されたら：

```bash
# ワークフロー設計へ進む
/ddd:1-plan parasol/phases/phase4-operation/4-2-workflows.md
```

---

## 参考情報

- [ドメインモデル定義書](../phase3-domain/)
- [能力設計書](../../projects/asahi-parasol-development/phase2-capability-design/)
- [RESTful API設計ガイド](https://restfulapi.net/)

---

*このドキュメントは実行可能なMDとして、AmplifierのDDDワークフローで処理できます。*