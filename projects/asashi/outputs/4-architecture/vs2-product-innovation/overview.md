# VS2: 製品開発・イノベーション アーキテクチャ概要

**プロジェクト:** asashi (Asahi Group Holdings)
**Value Stream:** VS2 製品開発・イノベーション
**作成日:** 2025-11-27
**ステータス:** 初版

---

## サービス一覧

### Core Services（コアドメイン）

事業競争力の源泉となる中核サービス群

| サービス | 日本語名 | 責務 | 含まれるBC |
|----------|----------|------|------------|
| [Fermentation Research](./services/fermentation-research-service/) | 発酵研究サービス | 酵母研究、発酵技術 | fermentation-research |
| [Ingredient Research](./services/ingredient-research-service/) | 素材研究サービス | 素材研究、機能性研究 | ingredient-research, functional-ingredients |
| [Beer Development](./services/beer-development-service/) | ビール開発サービス | ビール製品開発 | premium-beer-development, craft-innovation-development |
| [Spirits Development](./services/spirits-development-service/) | スピリッツ開発サービス | スピリッツ製品開発 | spirits-development |
| [Beverage Development](./services/beverage-development-service/) | 飲料開発サービス | 飲料製品開発 | beverage-development |

### Supporting Services（支援サービス）

コアサービスを支援する横断的サービス群

| サービス | 日本語名 | 責務 | 含まれるBC |
|----------|----------|------|------------|
| [R&D Support](./services/rnd-support-service/) | R&D支援サービス | 官能評価、試作生産 | sensory-evaluation, prototype-production |
| [Process Engineering](./services/process-engineering-service/) | プロセス技術サービス | 技術移管、製造プロセス | process-engineering |

---

## アーキテクチャ図

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          VS2 製品開発・イノベーション                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐       ┌─────────────────────┐                     │
│  │ Fermentation        │       │ Ingredient          │                     │
│  │ Research Service    │◄─────►│ Research Service    │                     │
│  │ [Core]              │  P    │ [Core]              │                     │
│  └──────────┬──────────┘       └──────────┬──────────┘                     │
│             │                             │                                 │
│             │ C-S                         │ C-S                             │
│             ▼                             ▼                                 │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │                    開発サービス群                            │           │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │           │
│  │  │ Beer        │  │ Spirits     │  │ Beverage    │         │           │
│  │  │ Development │  │ Development │  │ Development │         │           │
│  │  │ [Core]      │  │ [Core]      │  │ [Core]      │         │           │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │           │
│  └─────────┼────────────────┼────────────────┼─────────────────┘           │
│            │                │                │                              │
│            │ C-S            │ C-S            │ C-S                          │
│            ▼                ▼                ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │                    支援サービス群                            │           │
│  │  ┌─────────────────────┐       ┌─────────────────────┐     │           │
│  │  │ R&D Support         │◄─────►│ Process Engineering │     │           │
│  │  │ Service             │   P   │ Service             │     │           │
│  │  │ [Supporting]        │       │ [Supporting]        │     │           │
│  │  └─────────────────────┘       └─────────────────────┘     │           │
│  └─────────────────────────────────────────────────────────────┘           │
│                                                                             │
│  凡例: C-S = Customer-Supplier, P = Partnership                            │
│        ◄─────► = 双方向, ───────► = 単方向                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## データフロー

```
基盤研究（Upstream）
    │
    ├── Fermentation Research ──┐
    │                           ├──► 開発サービス群
    └── Ingredient Research ────┘
                                         │
                                         ├──► R&D Support（評価・試作）
                                         │
                                         └──► Process Engineering（技術移管）
                                                      │
                                                      ▼
                                               VS4 製造へ
```

---

## 主要イベント

### 研究 → 開発

| イベント | 発行元 | 購読先 |
|----------|--------|--------|
| YeastStrainRegistered | Fermentation Research | Beer Dev, Spirits Dev |
| FermentationRecipeCreated | Fermentation Research | Beer Dev |
| IngredientRegistered | Ingredient Research | Beer Dev, Beverage Dev |
| FunctionalEvidenceValidated | Ingredient Research | Beverage Dev |

### 開発 → 支援

| イベント | 発行元 | 購読先 |
|----------|--------|--------|
| ProductConceptApproved | 各開発サービス | R&D Support |
| ProductSpecificationFinalized | 各開発サービス | Process Engineering |

### 支援 → 開発

| イベント | 発行元 | 購読先 |
|----------|--------|--------|
| SensoryEvaluationCompleted | R&D Support | 各開発サービス |
| PrototypeBatchCompleted | R&D Support | 各開発サービス |
| TechnologyTransferValidated | Process Engineering | 各開発サービス |

---

## 関連ドキュメント

- [Context Map](./context-map.md) - サービス間関係の詳細
- [統合パターン](../cross-vs/integration-patterns.md) - 技術的な統合方式
- [ADRs](../cross-vs/decisions/) - アーキテクチャ決定記録

---

**作成者:** Claude (Parasol V5)
**最終更新:** 2025-11-27
