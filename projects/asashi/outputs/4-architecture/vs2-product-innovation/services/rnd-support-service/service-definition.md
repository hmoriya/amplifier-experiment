# R&D Support Service（R&D支援サービス）

**プロジェクト:** asashi (Asahi Group Holdings)
**Value Stream:** VS2 製品開発・イノベーション
**作成日:** 2025-11-27
**ステータス:** 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | R&D Support Service |
| **日本語名** | R&D支援サービス |
| **ドメインタイプ** | Supporting |
| **所有チーム** | R&D支援部 |
| **リポジトリ** | `asahi-rnd/rnd-support-service` |

---

## 含まれるBounded Contexts

- **sensory-evaluation BC** - 官能評価
- **prototype-production BC** - 試作生産

**統合理由:**
- 両BCとも全開発サービスを横断的に支援
- 同一チームが運用
- 試作と官能評価は密接に連携

---

## 責務

### ミッション

全製品開発サービスに対して、官能評価と試作生産の共通サービスを提供し、開発効率と品質を向上させる。

### 主要責務

1. 官能評価パネルの運営
2. 官能評価試験の実施・分析
3. 試作品の製造
4. 小規模生産設備の管理

---

## ドメインモデル

### Aggregates

```yaml
SensoryEvaluation:
  説明: 官能評価
  Root Entity: SensoryEvaluation
  Entities:
    - EvaluationSession
    - PanelResponse
    - StatisticalAnalysis
  Value Objects:
    - EvaluationId
    - SampleId
    - ScoreProfile

SensoryPanel:
  説明: 官能評価パネル
  Root Entity: SensoryPanel
  Entities:
    - Panelist
    - TrainingRecord
  Value Objects:
    - PanelId
    - PanelType

PrototypeRequest:
  説明: 試作依頼
  Root Entity: PrototypeRequest
  Entities:
    - ProductionSpec
    - MaterialRequirements
  Value Objects:
    - RequestId
    - Quantity
    - DueDate

PrototypeBatch:
  説明: 試作バッチ
  Root Entity: PrototypeBatch
  Entities:
    - ProductionRecord
    - QualityCheck
  Value Objects:
    - BatchId
    - BatchSize
```

---

## API仕様

### REST API

```yaml
Base URL: /api/v1/rnd-support

Endpoints:
  # 官能評価
  POST /sensory-evaluations: 評価依頼作成
  GET /sensory-evaluations: 評価一覧
  GET /sensory-evaluations/{id}: 評価詳細
  GET /sensory-evaluations/{id}/results: 評価結果取得
  POST /sensory-evaluations/{id}/responses: パネル回答登録

  # パネル管理
  GET /panels: パネル一覧
  GET /panels/{id}: パネル詳細
  GET /panels/{id}/panelists: パネリスト一覧

  # 試作生産
  POST /prototype-requests: 試作依頼作成
  GET /prototype-requests: 試作依頼一覧
  GET /prototype-requests/{id}: 依頼詳細
  GET /prototype-requests/{id}/status: ステータス確認

  # 試作バッチ
  GET /prototype-batches: バッチ一覧
  GET /prototype-batches/{id}: バッチ詳細
  POST /prototype-batches/{id}/quality-check: 品質チェック登録
```

---

## イベント

### Published Events

```yaml
SensoryEvaluationCompleted: 官能評価完了
SensoryReportGenerated: 評価レポート生成
PrototypeRequestReceived: 試作依頼受付
PrototypeBatchCompleted: 試作バッチ完了
```

### Subscribed Events

```yaml
ProductConceptApproved: (from Beer/Spirits/Beverage Development)
  → 評価準備のトリガー
```

---

## データストア

```yaml
Primary Database:
  Type: PostgreSQL
  Schema: rnd_support
```

---

## 依存関係

### 提供先（このサービスを利用するサービス）

| サービス | 提供内容 |
|----------|----------|
| Beer Development Service | 官能評価、試作 |
| Spirits Development Service | 官能評価、試作 |
| Beverage Development Service | 官能評価、試作 |

### 連携先（Partnership）

| サービス | 連携内容 |
|----------|----------|
| Process Engineering Service | 試作→製造スケールアップ連携 |

---

## 非機能要件

```yaml
Scaling:
  Requirement: 低〜中
  Replicas: 2

SLA: 99.5%

特記事項:
  - 官能評価データは統計分析に使用
  - 試作スケジュールの管理が重要
```

---

**作成者:** Claude (Parasol V4 Lite)
**最終更新:** 2025-11-27
