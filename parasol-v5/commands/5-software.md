# /parasol:5-software - ソフトウェア設計

## コマンド: `/parasol:5-software`

アーキテクチャを詳細なソフトウェア設計に落とし込みます。ドメインモデル、L4ユースケース、データベース設計を行います。

## 実行時間
約2-3時間

## 前提条件
- Phase 4（アーキテクチャ設計）の完了
- マイクロサービス境界の確定
- API仕様の基本設計

## 実行内容

### Task 1: ドメインモデル設計

#### 中核ドメインモデル（MS-PROJECT）
```yaml
エンティティ:
  Project:
    属性:
      - id: ProjectId (値オブジェクト)
      - name: ProjectName (値オブジェクト)
      - description: string
      - stage: ValueStage (値オブジェクト)
      - status: ProjectStatus (列挙型)
      - owner: UserId (値オブジェクト)
      - createdAt: DateTime
      - updatedAt: DateTime

    ビジネスルール:
      - プロジェクト名は一意
      - ステージは順番に遷移
      - 削除は論理削除のみ

  ValueStage:
    属性:
      - stageId: StageId
      - name: string
      - order: int
      - requiredCapabilities: Capability[]

    不変条件:
      - VS0は常に利用可能
      - ステージは後戻りできない

値オブジェクト:
  ProjectId:
    - value: UUID
    - 生成規則: UUID v4

  ProjectName:
    - value: string
    - 制約: 3-100文字、特殊文字制限

  ProjectStatus:
    値: [DRAFT, ACTIVE, SUSPENDED, COMPLETED, ARCHIVED]

集約:
  ProjectAggregate:
    ルート: Project
    含む:
      - ProjectMetrics
      - ProjectTemplates
      - ProjectCapabilities

    境界:
      - 集約内での一貫性保証
      - 外部参照はIDのみ
```

#### ドメインサービス
```yaml
ProjectLifecycleService:
  責任: プロジェクトのライフサイクル管理

  メソッド:
    createProject(name, description, owner):
      - プロジェクト作成
      - 初期ステージ設定
      - 基盤ケーパビリティ付与

    transitionStage(projectId, newStage):
      - ステージ遷移検証
      - 必要ケーパビリティ確認
      - 遷移実行

    archiveProject(projectId):
      - アーカイブ可能性検証
      - 関連リソース処理
      - アーカイブ実行

StageTransitionPolicy:
  責任: ステージ遷移ルールの管理

  ルール:
    - VS1→VS2: 認知率80%以上
    - VS2→VS3: 教育完了率100%
    - VS3→VS4: 成功事例3件以上
```

### Task 2: L4ユースケース設計（CL3→L4展開）

#### CL3からL4への詳細化
```yaml
CL3-1: プロジェクト環境構築

  L4-1-1: 新規プロジェクト作成
    アクター: プロジェクトマネージャー
    前提条件: 認証済み、作成権限あり
    メインフロー:
      1. プロジェクト情報入力
      2. テンプレート選択
      3. 初期設定実行
      4. チームメンバー招待
    事後条件: プロジェクトが利用可能
    例外: 名前重複、権限不足

  L4-1-2: 開発環境セットアップ
    アクター: 開発者
    前提条件: プロジェクトメンバー
    メインフロー:
      1. 環境要件確認
      2. ツールインストール
      3. 認証情報設定
      4. 接続テスト
    事後条件: 開発可能状態

  L4-1-3: CI/CDパイプライン設定
    アクター: DevOpsエンジニア
    前提条件: インフラ権限あり
    メインフロー:
      1. リポジトリ連携
      2. ビルド設定
      3. デプロイ設定
      4. 通知設定
    事後条件: 自動化完了

CL3-2: テンプレート適用

  L4-2-1: テンプレート選択
    アクター: 開発者
    前提条件: プロジェクトメンバー
    メインフロー:
      1. テンプレート一覧表示
      2. フィルタ・検索
      3. プレビュー確認
      4. 選択決定
    事後条件: テンプレート選択完了

  L4-2-2: テンプレートカスタマイズ
    アクター: 開発者
    前提条件: テンプレート選択済み
    メインフロー:
      1. パラメータ設定
      2. 条件分岐設定
      3. プレビュー生成
      4. 確認・調整
    事後条件: カスタマイズ完了
```

### Task 3: データベース設計

#### 物理データモデル（PostgreSQL）
```sql
-- プロジェクトテーブル
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    stage_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    owner_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,

    CONSTRAINT fk_stage FOREIGN KEY (stage_id)
        REFERENCES value_stages(id),
    CONSTRAINT fk_owner FOREIGN KEY (owner_id)
        REFERENCES users(id),
    INDEX idx_status (status),
    INDEX idx_stage (stage_id),
    INDEX idx_owner (owner_id)
);

-- バリューステージマスタ
CREATE TABLE value_stages (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    stage_order INT NOT NULL,
    description TEXT,
    success_criteria JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_stage_order (stage_order)
);

-- プロジェクトメトリクス
CREATE TABLE project_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    value DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20),
    measured_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_project FOREIGN KEY (project_id)
        REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_metric (project_id, metric_type),
    INDEX idx_measured_at (measured_at)
);

-- テンプレート
CREATE TABLE templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    stage_id VARCHAR(50),
    content JSONB NOT NULL,
    version VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_type_stage (type, stage_id),
    INDEX idx_active (is_active)
);
```

#### NoSQLデータモデル（MongoDB）
```javascript
// プロジェクトドキュメント
{
  "_id": ObjectId("..."),
  "projectId": "uuid",
  "name": "プロジェクト名",
  "stage": {
    "id": "VS3",
    "name": "初期実践",
    "enteredAt": ISODate("2024-01-01")
  },
  "capabilities": [
    {
      "cl1": "初期実践ケーパビリティ",
      "cl2": [
        {
          "id": "CL2-1",
          "name": "プロジェクト設定",
          "cl3": [
            {
              "id": "CL3-1",
              "name": "環境構築",
              "status": "completed",
              "completedAt": ISODate("2024-01-02")
            }
          ]
        }
      ]
    }
  ],
  "history": [
    {
      "event": "stage_transition",
      "from": "VS2",
      "to": "VS3",
      "timestamp": ISODate("2024-01-01"),
      "user": "user-id"
    }
  ]
}

// テンプレートドキュメント
{
  "_id": ObjectId("..."),
  "templateId": "uuid",
  "name": "Spring Boot マイクロサービス",
  "type": "backend",
  "tags": ["java", "spring", "microservice"],
  "structure": {
    "src/main/java": {
      "controller": ["UserController.java"],
      "service": ["UserService.java"],
      "repository": ["UserRepository.java"],
      "model": ["User.java"]
    }
  },
  "parameters": {
    "serviceName": {
      "type": "string",
      "required": true,
      "default": "my-service"
    },
    "port": {
      "type": "number",
      "required": false,
      "default": 8080
    }
  }
}
```

### Task 4: インターフェース契約

#### サービス間契約
```yaml
契約: ProjectService → AuthService
  目的: プロジェクト作成時の権限確認

  リクエスト:
    method: POST
    path: /internal/auth/validate
    body:
      userId: string
      permission: string
      resource: string

  レスポンス:
    200:
      hasPermission: boolean
      reason: string?

  SLA:
    応答時間: < 100ms
    可用性: 99.9%

契約: ProjectService → NotificationService
  目的: ステージ遷移通知

  イベント:
    topic: project.stage.changed
    payload:
      projectId: string
      fromStage: string
      toStage: string
      timestamp: datetime
      userId: string

  保証:
    配信: At least once
    順序: 保証なし
    遅延: < 1秒
```

## 成果物

以下のファイルが`outputs/5-software/`に生成されます：

1. **domain-model.md**
   - エンティティ定義
   - 値オブジェクト
   - ドメインサービス
   - ビジネスルール

2. **use-cases.md**
   - L4ユースケース詳細
   - アクター定義
   - フロー図
   - 例外処理

3. **database-design.sql**
   - DDL定義
   - インデックス設計
   - 制約定義

4. **interface-contracts.yaml**
   - サービス間契約
   - イベント定義
   - SLA定義

## 決定記録

**SADR-001: ドメイン駆動設計採用**
```yaml
決定: DDDの戦術的設計パターン採用
理由: ビジネスロジックの複雑性管理
代替案: トランザクションスクリプト、テーブルモジュール
影響: 学習コスト増、保守性向上
```

**SADR-002: CQRSパターン部分採用**
```yaml
決定: 読み取り専用モデルの分離
理由: パフォーマンス最適化
代替案: 単一モデル
影響: 複雑性増加、スケーラビリティ向上
```

## チェックリスト

- [ ] ドメインモデルがビジネス要求を表現しているか
- [ ] L4ユースケースが網羅的か
- [ ] データベース設計が正規化されているか
- [ ] インターフェース契約が明確か
- [ ] パフォーマンス要件を満たす設計か

## 価値トレーサビリティ（Phase 5）

> **参照**: `_value-traceability-system/phase-integration-patterns.md` - Phase 5実装価値の確認

### ドメインモデルの価値表現

**ビジネスルールの価値根拠**：
```yaml
価値実現ビジネスルール:
  Project.transitionTo():
    価値ルール: ステージ遷移による価値進化の保証
    実装根拠: VS価値フローの論理的制約をコードで実現
    価値保護: 不正な遷移により価値実現が阻害されることを防止

  ValueStage.requiredCapabilities:
    価値ルール: ステージ価値実現に必要なケーパビリティの保証
    実装根拠: CL分解で特定した必要条件のコード化
    価値測定: ケーパビリティ充足度による価値実現可能性評価
```

### L4ユースケースの価値実現

**価値実現オペレーションのトレーサビリティ**：
```yaml
ユースケース価値マッピング:
  L4-1-1（新規プロジェクト作成）:
    価値実現: VS1認知形成価値の具体的スタート
    価値測定: プロジェクト作成成功率、初期設定完了時間
    価値保証: テンプレート適用による価値再現性確保

  L4-2-1（テンプレート選択）:
    価値実現: VS3実践価値の効率的実現支援
    価値測定: 適用成功率、カスタマイズ精度、実装時間短縮
    価値保証: テンプレート品質による価値実現確率向上
```

### データベース設計の価値整合性

**価値データの永続化戦略**：
```yaml
価値データ設計:
  projects.stage_id:
    価値トレーサビリティ: VSによる価値進捗の完全記録
    価値測定支援: ステージ別価値実現統計の収集基盤

  project_metrics:
    価値測定実装: VL実現度の定量的記録
    価値改善支援: メトリクス分析による価値向上機会発見
    価値証明: 価値実現の客観的証拠収集
```

### MS4品質ゲート

**Phase 5完了基準**：
```yaml
設計価値整合性:
  - [ ] ドメインモデルが価値概念を正確に表現
  - [ ] ビジネスルールが価値実現を保証
  - [ ] L4ユースケースが価値オペレーションを実装
  - [ ] データ設計が価値測定を支援

価値実現設計の妥当性:
  - [ ] 全設計要素が価値まで追跡可能
  - [ ] 価値測定機能の設計完了
  - [ ] 価値保護機能の設計完了
  - [ ] 次フェーズ実装準備完了
```

## 次のステップ

ソフトウェア設計が完了したら、実装フェーズへ：

```bash
# 設計価値整合性検証
./value-trace verify-design-value-alignment

# MS4品質ゲート実行
./value-trace quality-gate --milestone=MS4

# 次フェーズへの価値移転
./value-trace transfer --to=phase6

# Phase 6実行
/parasol:6-implementation
```

---

*詳細設計が価値実現の確実な設計図となります。価値トレーサビリティにより、実装すべき価値機能が明確になります。*