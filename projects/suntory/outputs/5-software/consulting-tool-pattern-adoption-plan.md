# ConsultingToolパターン適用プラン

**作成日**: 2025-12-05
**プロジェクト**: サントリーグループ
**目的**: ConsultingToolのソフトウェアデザイン構成をサントリーのBounded Context以下の構成に適用

---

## 1. ConsultingTool構造サマリー

### 1.1 Parasol V3 MVP フレームワーク

ConsultingToolは**Parasol V3 MVP**フレームワークを採用しており、以下の7階層で設計されている：

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Parasol V3 設計階層                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Service (サービス)                                              │
│     └─ e.g., Task Management Service                               │
│                                                                     │
│  2. L3 Capability (L3ケーパビリティ)                                │
│     └─ e.g., cap-001-task-lifecycle                                │
│                                                                     │
│  3. Business Operation (ビジネスオペレーション)                      │
│     └─ e.g., op-001-create-task                                    │
│                                                                     │
│  4. Use Case (ユースケース)                                         │
│     └─ e.g., uc-001-task-creation                                  │
│                                                                     │
│  5. Robustness Diagram (BCE パターン)                               │
│     └─ Boundary, Control, Entity                                   │
│                                                                     │
│  6. Page Definition (ページ定義)                                    │
│     └─ e.g., page-001-task-creation                                │
│                                                                     │
│  7. Test Definition (テスト定義)                                    │
│     └─ Acceptance / Unit Tests                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 BC-001 Task Management の具体構造

```
bc-001-task-management/
├── README.md                          # BC概要・スコープ
├── l3-capabilities/                   # 3 L3ケーパビリティ
│   ├── cap-001-task-lifecycle.md
│   ├── cap-002-task-collaboration.md
│   └── cap-003-task-monitoring.md
├── operations/                        # 8 ビジネスオペレーション
│   ├── op-001-create-task.md
│   ├── op-002-assign-task.md
│   └── ...
├── usecases/                          # 12 ユースケース
│   ├── uc-001-task-creation.md
│   ├── uc-002-task-assignment.md
│   └── ...
├── pages/                             # 12 ページ定義
│   ├── page-001-task-creation.md
│   ├── page-002-task-list.md
│   └── ...
└── domain-language/                   # ドメイン言語
    ├── entities.md
    ├── value-objects.md
    ├── aggregates.md
    ├── domain-services.md
    └── domain-events.md
```

### 1.3 命名規則

| 要素 | 形式 | 例 |
|------|------|-----|
| BC | `bc-{number:03d}-{name}` | bc-001-task-management |
| Capability | `cap-{number:03d}-{name}` | cap-001-task-lifecycle |
| Operation | `op-{number:03d}-{name}` | op-001-create-task |
| UseCase | `uc-{number:03d}-{name}` | uc-001-task-creation |
| Page | `page-{number:03d}-{name}` | page-001-task-creation |

**3要素命名**: `[日本語名] [EnglishName] [SCREAMING_SNAKE_CASE]`

---

## 2. サントリーへの適用プラン

### 2.1 適用スコープ

Phase 4で定義した24 Bounded Contextsのうち、以下を優先対象とする：

| 優先度 | BC | 理由 |
|--------|-----|------|
| **Phase 1** | RD-WaterScience | Core、差別化の源泉 |
| | MKT-Beverage | Core、最大事業 |
| | CRM-CDP | Supporting、全事業の基盤 |
| **Phase 2** | MFG-Beverage | Core、製造DX |
| | BRAND-Corporate | Core、全社ブランド |
| **Phase 3** | 残りのBC | 順次展開 |

### 2.2 ディレクトリ構造（サントリー版）

```
projects/suntory/outputs/5-software/
├── README.md                              # ソフトウェア設計概要
├── bounded-contexts/
│   ├── bc-001-rd-water-science/
│   │   ├── README.md
│   │   ├── l3-capabilities/
│   │   │   ├── cap-001-water-quality-analysis.md
│   │   │   ├── cap-002-water-source-management.md
│   │   │   └── cap-003-purification-technology.md
│   │   ├── operations/
│   │   │   ├── op-001-analyze-water-quality.md
│   │   │   ├── op-002-register-water-source.md
│   │   │   └── ...
│   │   ├── usecases/
│   │   │   ├── uc-001-water-quality-test.md
│   │   │   ├── uc-002-water-source-registration.md
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── page-001-water-quality-dashboard.md
│   │   │   ├── page-002-water-source-list.md
│   │   │   └── ...
│   │   └── domain-language/
│   │       ├── entities.md
│   │       ├── value-objects.md
│   │       ├── aggregates.md
│   │       ├── domain-services.md
│   │       └── domain-events.md
│   ├── bc-002-mkt-beverage/
│   │   └── (同様の構造)
│   ├── bc-003-crm-cdp/
│   │   └── (同様の構造)
│   └── ...
├── services/
│   ├── README.md                          # サービス層概要
│   ├── rd-platform-service/
│   │   ├── api/
│   │   ├── db/
│   │   └── domain/
│   └── ...
└── common/
    ├── templates/                         # テンプレート
    │   ├── l3-capability-template.md
    │   ├── operation-template.md
    │   ├── usecase-template.md
    │   ├── page-template.md
    │   └── domain-language-template.md
    └── standards/                         # 標準・規約
        ├── naming-conventions.md
        ├── api-specification-standard.md
        └── database-design-standard.md
```

---

## 3. 実装プラン

### 3.1 Phase 1: 基盤整備（1週間）

| タスク | 成果物 | 担当 |
|--------|--------|------|
| テンプレート作成 | common/templates/*.md | アーキテクト |
| 命名規則定義 | common/standards/naming-conventions.md | アーキテクト |
| BC-001 README作成 | bc-001-rd-water-science/README.md | ドメインエキスパート |

### 3.2 Phase 2: BC-001 RD-WaterScience 設計（2週間）

| 週 | タスク | 成果物 |
|----|--------|--------|
| 1週目 | L3 Capability定義 | 3 capabilities |
| | Business Operation定義 | 6-8 operations |
| 2週目 | UseCase定義 | 8-12 usecases |
| | Page Definition | 8-12 pages |
| | Domain Language | entities, VOs, aggregates |

### 3.3 Phase 3: BC-002, BC-003 設計（各2週間）

BC-001と同様のプロセスを並行実施。

### 3.4 Phase 4: 全BC展開（継続的）

残りの21 BCを順次設計。

---

## 4. BC-001 RD-WaterScience 設計案

### 4.1 L3 Capabilities

| ID | 名称 | 責務 |
|----|------|------|
| cap-001 | 水質分析 [WaterQualityAnalysis] | 水質検査・評価・基準管理 |
| cap-002 | 水源管理 [WaterSourceManagement] | 水源情報・涵養活動管理 |
| cap-003 | 浄水技術 [PurificationTechnology] | 浄水プロセス・技術研究 |

### 4.2 Business Operations

| ID | 名称 | Capability | 説明 |
|----|------|------------|------|
| op-001 | 水質検査実施 [AnalyzeWaterQuality] | cap-001 | 水サンプルの品質検査を実施 |
| op-002 | 水質基準設定 [SetQualityStandard] | cap-001 | 製品用水の品質基準を設定 |
| op-003 | 水源登録 [RegisterWaterSource] | cap-002 | 新規水源の登録 |
| op-004 | 涵養活動記録 [RecordConservation] | cap-002 | 水源涵養活動の記録 |
| op-005 | 浄水プロセス設計 [DesignPurification] | cap-003 | 浄水プロセスの設計 |
| op-006 | 技術移転 [TransferTechnology] | cap-003 | 製造部門への技術移転 |

### 4.3 Use Cases

| ID | 名称 | Operation | Page |
|----|------|-----------|------|
| uc-001 | 水質検査 [WaterQualityTest] | op-001 | page-001 |
| uc-002 | 基準設定 [StandardSetting] | op-002 | page-002 |
| uc-003 | 水源登録 [SourceRegistration] | op-003 | page-003 |
| uc-004 | 涵養記録 [ConservationRecord] | op-004 | page-004 |
| uc-005 | プロセス設計 [ProcessDesign] | op-005 | page-005 |
| uc-006 | 技術移転 [TechTransfer] | op-006 | page-006 |
| uc-007 | 品質ダッシュボード [QualityDashboard] | op-001/002 | page-007 |
| uc-008 | 水源マップ [SourceMap] | op-003/004 | page-008 |

### 4.4 Pages

| ID | 名称 | UseCase | 主要機能 |
|----|------|---------|----------|
| page-001 | 水質検査画面 | uc-001 | 検査入力、結果表示 |
| page-002 | 基準管理画面 | uc-002 | 基準CRUD、履歴 |
| page-003 | 水源登録画面 | uc-003 | 水源情報入力 |
| page-004 | 涵養活動記録 | uc-004 | 活動記録、写真 |
| page-005 | プロセス設計 | uc-005 | フロー図、パラメータ |
| page-006 | 技術移転管理 | uc-006 | 移転状況、承認 |
| page-007 | 品質ダッシュボード | uc-007 | KPI、トレンド |
| page-008 | 水源マップ | uc-008 | 地図、涵養状況 |

### 4.5 Domain Language

#### Entities

```yaml
WaterSource:
  日本語名: 水源
  説明: 水を採取する自然資源
  属性:
    - id: UUID
    - name: 水源名
    - location: 所在地
    - type: 種別（地下水/湧水/河川）
    - status: 状態
    - discoveredAt: 発見日

WaterQualityTest:
  日本語名: 水質検査
  説明: 水サンプルの品質検査記録
  属性:
    - id: UUID
    - sourceId: 水源ID
    - testedAt: 検査日時
    - results: 検査結果（JSON）
    - conclusion: 判定（合格/不合格/要再検査）

QualityStandard:
  日本語名: 品質基準
  説明: 製品用水の品質基準定義
  属性:
    - id: UUID
    - productCategory: 製品カテゴリ
    - parameters: 基準パラメータ（JSON）
    - effectiveFrom: 有効開始日
```

#### Value Objects

```yaml
MineralComposition:
  日本語名: ミネラル組成
  説明: 水中のミネラル成分構成
  属性:
    - calcium: カルシウム (mg/L)
    - magnesium: マグネシウム (mg/L)
    - sodium: ナトリウム (mg/L)
    - potassium: カリウム (mg/L)

WaterHardness:
  日本語名: 硬度
  説明: 水の硬度
  属性:
    - value: 数値 (mg/L)
    - category: 分類（軟水/中硬水/硬水）
```

#### Aggregates

```yaml
WaterSourceAggregate:
  ルート: WaterSource
  含むエンティティ:
    - WaterQualityTest[]
    - ConservationActivity[]
  含むVO:
    - Location
    - MineralComposition

QualityStandardAggregate:
  ルート: QualityStandard
  含むエンティティ:
    - StandardRevision[]
  含むVO:
    - ParameterRange[]
```

#### Domain Events

```yaml
WaterQualityTestCompleted:
  日本語名: 水質検査完了
  発行タイミング: 検査結果確定時
  ペイロード:
    - testId
    - sourceId
    - conclusion
    - testedAt

QualityStandardUpdated:
  日本語名: 品質基準更新
  発行タイミング: 基準変更時
  ペイロード:
    - standardId
    - productCategory
    - effectiveFrom
```

---

## 5. 次のアクション

### 5.1 即座に実行可能

1. **ディレクトリ構造作成**
   ```bash
   mkdir -p outputs/5-software/bounded-contexts/bc-001-rd-water-science/{l3-capabilities,operations,usecases,pages,domain-language}
   mkdir -p outputs/5-software/common/{templates,standards}
   ```

2. **テンプレート作成**
   - ConsultingToolのテンプレートをサントリー向けにカスタマイズ

3. **BC-001 README作成**
   - スコープ、責務、成功指標を定義

### 5.2 ユーザー確認事項

1. **優先BC**: RD-WaterScienceから開始で良いか？
2. **詳細度**: ConsultingToolと同レベルの詳細度で良いか？
3. **言語**: 日本語メインでEnglish併記で良いか？

---

## 6. ConsultingToolからの学び

### 6.1 成功パターン

| パターン | 説明 | サントリーへの適用 |
|----------|------|-------------------|
| 7階層設計 | Service→Capability→Operation→UseCase→Robustness→Page→Test | そのまま採用 |
| 3要素命名 | 日本語/英語/定数 | そのまま採用 |
| 1:1対応 | Operation→UseCase→Page | そのまま採用 |
| ドメイン言語 | Entity/VO/Aggregate/Event | そのまま採用 |

### 6.2 カスタマイズポイント

| 項目 | ConsultingTool | サントリー版 |
|------|---------------|-------------|
| 規模 | 1 BC、12 UC | 24 BC、100+ UC |
| 複雑性 | 単一事業 | 5事業×HD |
| 技術スタック | Next.js/SQLite | 未定（本フェーズで決定） |
| 連携 | 単一アプリ | マイクロサービス連携 |

---

**プラン作成完了**: 2025-12-05
**次ステップ**: ユーザー確認後、BC-001設計開始
