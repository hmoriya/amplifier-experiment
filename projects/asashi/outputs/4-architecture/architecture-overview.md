# Phase 4: アーキテクチャ設計 概要

**プロジェクト:** asashi (Asahi Group Holdings)
**作成日:** 2025-11-27
**ステータス:** 初版

---

## ディレクトリ構成

```
outputs/4-architecture/
├── architecture-overview.md     # 本ファイル（Phase 4全体概要）
├── vs2-product-innovation/      # VS2: 製品開発・イノベーション
│   ├── overview.md              # VS2アーキテクチャ概要
│   ├── context-map.md           # サービス間関係（Context Map）
│   └── services/                # サービス定義（サービス毎）
│       ├── fermentation-research-service/
│       ├── ingredient-research-service/
│       ├── beer-development-service/
│       ├── spirits-development-service/
│       ├── beverage-development-service/
│       ├── rnd-support-service/
│       └── process-engineering-service/
└── cross-vs/                    # VS横断共通設計
    ├── integration-patterns.md  # 統合パターン定義
    └── decisions/               # Architecture Decision Records
        ├── adr-001-microservices-architecture.md
        ├── adr-002-kafka-event-bus.md
        ├── adr-003-api-gateway.md
        ├── adr-004-database-per-service.md
        └── adr-005-jwt-authentication.md
```

---

## 設計方針

### マイクロサービスアーキテクチャ

VS2（製品開発・イノベーション）を7つの独立したサービスに分割:

| # | サービス | タイプ | 主要責務 |
|---|----------|--------|----------|
| 1 | Fermentation Research | Core | 発酵技術研究、酵母管理 |
| 2 | Ingredient Research | Core | 素材研究、機能性研究 |
| 3 | Beer Development | Core | ビール製品開発 |
| 4 | Spirits Development | Core | スピリッツ製品開発 |
| 5 | Beverage Development | Core | 飲料製品開発 |
| 6 | R&D Support | Supporting | 官能評価、試作支援 |
| 7 | Process Engineering | Supporting | 技術移管、プロセス設計 |

### 統合パターン

| パターン | 用途 | 技術 |
|----------|------|------|
| REST API | 外部公開・同期クエリ | FastAPI + OpenAPI |
| gRPC | サービス間高速通信 | Protocol Buffers |
| Event-Driven | 疎結合統合 | Apache Kafka |
| CQRS | 読み書き分離 | PostgreSQL + Elasticsearch |

### Architecture Decision Records (ADRs)

| ADR | タイトル | ステータス |
|-----|----------|------------|
| ADR-001 | マイクロサービスアーキテクチャの採用 | 承認済み |
| ADR-002 | イベントバスとしてKafkaを選択 | 承認済み |
| ADR-003 | API Gatewayパターンの採用 | 承認済み |
| ADR-004 | Database per Serviceパターン | 承認済み |
| ADR-005 | JWT認証の選択 | 承認済み |

---

## Value Stream別成果物

### VS2: 製品開発・イノベーション

**詳細:** `vs2-product-innovation/overview.md`

- 7サービスの定義
- Context Map（サービス間関係）
- サービス毎の詳細定義

### 今後追加予定

- VS1: 市場インサイト
- VS3: ブランディング・マーケティング
- VS4: サプライチェーン・生産
- VS5: 品質保証
- VS6: データプラットフォーム

---

## 関連ドキュメント

### 前フェーズ

- Phase 3: `outputs/3-capabilities/` - Capability分解（CL1/CL2/CL3）

### 次フェーズ

- Phase 5: ソフトウェア設計（未着手）

---

**作成者:** Claude (Parasol V4 Lite)
**最終更新:** 2025-11-27
