# BC-001: R&D 水科学 [RD-WaterScience]

## 概要

| 項目 | 値 |
|------|-----|
| ID | bc-001-rd-water-science |
| 日本語名 | R&D 水科学 |
| 英語名 | RD-WaterScience |
| 定数名 | RD_WATER_SCIENCE |
| ドメイン分類 | Core（差別化の源泉） |
| 所属CL1 | R&D/品質 |
| ステータス | Draft |

---

## ビジネスコンテキスト

### サントリーと水

サントリーは「水と生きる」を企業理念に掲げ、水は全事業の根幹をなす。
水科学研究は、飲料・酒類製品の品質を決定づける最も重要な差別化要因である。

### ドメインの重要性

- **Core ドメイン**: 競合他社との差別化の源泉
- **全事業横断**: 飲料、酒類、健康食品すべてに影響
- **長期的視点**: 水源涵養活動は50年以上の歴史

---

## スコープ

### 含むもの

1. **水質分析・評価**
   - 水質検査の実施と記録
   - 品質基準の設定と管理
   - 検査結果の評価と判定

2. **水源管理**
   - 水源情報の登録と管理
   - 水源涵養活動の記録
   - 水源マップの可視化

3. **浄水技術**
   - 浄水プロセスの設計
   - 技術研究の管理
   - 製造部門への技術移転

### 含まないもの

- 製品製造プロセス（→ MFG-Beverage, MFG-Spirits）
- 製品品質検査（→ 各製造BC）
- 環境報告書作成（→ SUST-Environment）

---

## L3 Capabilities

| ID | 名称 | 責務 |
|----|------|------|
| cap-001 | 水質分析 [WaterQualityAnalysis] | 水質検査・評価・基準管理 |
| cap-002 | 水源管理 [WaterSourceManagement] | 水源情報・涵養活動管理 |
| cap-003 | 浄水技術 [PurificationTechnology] | 浄水プロセス・技術研究 |

---

## サービス構成

### 所属サービス

- **R&D Platform Service** (rd-platform-service)

### 外部連携

| 連携先BC | パターン | 説明 |
|----------|----------|------|
| MFG-Beverage | Customer-Supplier | 品質基準の提供 |
| MFG-Spirits | Customer-Supplier | 品質基準の提供 |
| SUST-Environment | Open Host Service | 水源データの公開 |

---

## ユーザー

### 主要アクター

| アクター | 役割 | 主な操作 |
|----------|------|----------|
| 水質分析担当者 | 水質検査の実施 | 検査登録、結果入力 |
| 品質管理責任者 | 基準設定・承認 | 基準CRUD、検査承認 |
| 水源管理担当者 | 水源情報管理 | 水源登録、涵養記録 |
| 技術研究者 | 浄水技術開発 | プロセス設計、技術移転 |
| 経営層 | ダッシュボード閲覧 | KPI確認 |

---

## 成功指標

| 指標 | 目標値 | 測定方法 |
|------|--------|----------|
| 水質検査合格率 | 99.5%以上 | 検査結果集計 |
| 検査リードタイム | 24時間以内 | サンプル受領〜結果確定 |
| 水源涵養面積 | 前年比+5% | 涵養活動記録 |
| 技術移転完了率 | 90%以上 | 移転プロセス追跡 |

---

## 技術スタック（推奨）

| レイヤー | 技術 | 理由 |
|----------|------|------|
| Frontend | Next.js + TypeScript | 社内標準 |
| API | GraphQL | 柔軟なデータ取得 |
| Backend | Python + FastAPI | データ分析連携 |
| Database | PostgreSQL | 構造化データ、ACID |
| Search | Elasticsearch | 水源・検査データ検索 |
| Event | Kafka | 他BCへのイベント発行 |

---

## ディレクトリ構造

```
bc-001-rd-water-science/
├── README.md                    # 本ファイル
├── l3-capabilities/
│   ├── cap-001-water-quality-analysis.md
│   ├── cap-002-water-source-management.md
│   └── cap-003-purification-technology.md
├── operations/
│   ├── op-001-analyze-water-quality.md
│   ├── op-002-set-quality-standard.md
│   ├── op-003-register-water-source.md
│   ├── op-004-record-conservation.md
│   ├── op-005-design-purification.md
│   └── op-006-transfer-technology.md
├── usecases/
│   ├── uc-001-water-quality-test.md
│   ├── uc-002-standard-setting.md
│   ├── uc-003-source-registration.md
│   ├── uc-004-conservation-record.md
│   ├── uc-005-process-design.md
│   ├── uc-006-tech-transfer.md
│   ├── uc-007-quality-dashboard.md
│   └── uc-008-source-map.md
├── pages/
│   ├── page-001-water-quality-test.md
│   ├── page-002-quality-standard.md
│   ├── page-003-water-source-registration.md
│   ├── page-004-conservation-record.md
│   ├── page-005-process-design.md
│   ├── page-006-tech-transfer.md
│   ├── page-007-quality-dashboard.md
│   └── page-008-source-map.md
└── domain-language/
    ├── entities.md
    ├── value-objects.md
    ├── aggregates.md
    ├── domain-services.md
    └── domain-events.md
```

---

## 関連ドキュメント

- [Phase 3 CL3定義](../../3-capabilities/cl3-bounded-contexts.md)
- [Phase 4 サービス境界](../../4-architecture/service-boundaries.md)
- [Phase 4 コンテキストマップ](../../4-architecture/context-map.md)
- [命名規則](../common/standards/naming-conventions.md)

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
**ステータス**: Draft
