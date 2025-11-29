# Parasol V5 - 価値駆動ZIGZAGプロセス

## 概要

Parasol V5は、価値からソフトウェア実装まで、3層のネストしたWHAT→HOWパターン（ZIGZAGプロセス）で体系的に分解します。

```
価値（WHAT）→ 実現方法（HOW）→ 必要能力（WHAT）→ 実装（HOW）
```

---

## 3層ZIGZAGモデル

```
┌─────────────────────────────────────────────────────────────────────┐
│  Level 1: ビジネス層                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│    WHAT              →              HOW                             │
│    価値                          Value Stream                       │
│   「何を実現したいか」           「どう流れるか」                    │
│                                                                     │
│   Phase 2 前半                   Phase 2 後半                       │
└─────────────────────────────────────────────────────────────────────┘
                                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│  Level 2: サービス層                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│    WHAT              →              HOW                             │
│  Capability                      Service設計                        │
│  「何が必要か」                  「どう分割するか」                  │
│                                                                     │
│   Phase 3                        Phase 4                            │
└─────────────────────────────────────────────────────────────────────┘
                                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│  Level 3: 実装層                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│    WHAT              →              HOW                             │
│  Software設計                      実装                             │
│  「何を作るか」                  「どう作るか」                      │
│                                                                     │
│   Phase 5                        Phase 6                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phaseとの対応

| Phase | Level | WHAT/HOW | 内容 | 主要成果物 |
|-------|-------|----------|------|-----------|
| **1** | - | 前提 | Context（組織・市場・制約） | organization-analysis.md |
| **2a** | **L1** | **WHAT** | **価値定義** | value-definition.md |
| **2b** | **L1** | **HOW** | **Value Stream/Stage** | value-streams-mapping.md |
| **3** | **L2** | **WHAT** | **Capability（サービス候補）** | capabilities.md |
| **4** | **L2** | **HOW** | **Service設計（境界・Context Map）** | service-boundaries.md |
| **5** | **L3** | **WHAT** | **Software設計** | domain-model.md, api-specs/ |
| **6** | **L3** | **HOW** | **実装** | コード |
| **7** | - | 基盤 | Platform（インフラ・運用） | infrastructure.md |

---

## 各レベルの詳細

### Level 1: ビジネス層（Phase 2）

**目的**: ビジネス価値とその実現の流れを定義

#### WHAT: 価値定義（Phase 2前半）

- 企業が提供する価値は何か
- ステークホルダーにとっての価値
- 価値指標（KPI）

```
質問: 「このビジネスは何を実現するのか？」
出力: value-definition.md
```

#### HOW: Value Stream（Phase 2後半）

- 価値を実現する活動の流れ
- Value Stream → Value Stage への分解
- Stage間の依存関係

```
質問: 「価値はどのように流れるのか？」
出力: value-streams-mapping.md, vs{N}-detail.md
```

---

### Level 2: サービス層（Phase 3-4）

**目的**: Value Stageをスイムレーンとしてサービス境界を確定

#### WHAT: Capability（Phase 3）

- 各Value Stageに必要なケイパビリティ
- サービス候補の特定
- 重複のない唯一無二のサービス単位

```
質問: 「各Stageで何ができる必要があるか？」
出力: capabilities.md

┌──────────┐  ┌──────────┐  ┌──────────┐
│ Stage 1  │  │ Stage 2  │  │ Stage 3  │  ← スイムレーン
├──────────┤  ├──────────┤  ├──────────┤
│ Cap A    │  │ Cap D    │  │ Cap G    │  ← Capability
│ Cap B    │  │ Cap E    │  │ Cap H    │    （サービス候補）
│ Cap C    │  │ Cap F    │  │ Cap I    │
└──────────┘  └──────────┘  └──────────┘
```

#### HOW: Service設計（Phase 4）

- サービス境界の確定
- Context Map（サービス間関係）
- API契約の概要

```
質問: 「サービスをどう分割・連携させるか？」
出力: service-boundaries.md, context-map.md

※ここで「サービス枠」をフリーズ
※以降の変更は高コスト
```

---

### Level 3: 実装層（Phase 5-6）

**目的**: 確定したサービス枠内で設計・実装

#### WHAT: Software設計（Phase 5）

- ドメインモデル
- API仕様
- データベース設計
- ユースケース詳細

```
質問: 「各サービスで何を作るか？」
出力: domain-model.md, api-specs/, database-design.md
```

#### HOW: 実装（Phase 6）

- コード生成
- テスト
- リファクタリング

```
質問: 「どう作るか？」
出力: src/, tests/
```

---

## Value Stage Swimlane パターン

### なぜスイムレーンか

| 観点 | スイムレーン方式 | ボトムアップ方式 |
|------|-----------------|-----------------|
| **サービス境界** | Value Stageで事前確定 | 後から決めるため曖昧に |
| **重複リスク** | 低い（境界が明確） | 高い（ユーザー視点で重複） |
| **修正コスト** | 低い（事前設計） | 高い（結合後の分離困難） |

### スイムレーンの作り方

```
Step 1: Value Streamを特定
        「調達 → 製造 → 販売」

Step 2: 各Stageをスイムレーンとして配置
        ┌────────┐ ┌────────┐ ┌────────┐
        │ 調達   │ │ 製造   │ │ 販売   │
        └────────┘ └────────┘ └────────┘

Step 3: 各スイムレーン内でCapabilityを列挙
        ┌────────┐ ┌────────┐ ┌────────┐
        │原料調達│ │製品開発│ │受注管理│
        │品質検査│ │生産管理│ │出荷管理│
        │在庫管理│ │品質保証│ │顧客管理│
        └────────┘ └────────┘ └────────┘

Step 4: 各Capabilityがサービス候補
        → Phase 4で境界を確定
```

---

## ハイレベルユースケースの位置づけ

### どこで使うか

ハイレベルユースケースは**Level 2（サービス層）のCapability内部**で活用：

```
Capability（サービス候補）
    │
    ├── ハイレベルUC 1: 「顧客が見積もりを依頼する」
    ├── ハイレベルUC 2: 「営業が見積もりを作成する」
    └── ハイレベルUC 3: 「顧客が見積もりを承認する」
```

### なぜこの位置か

- **境界は既に確定**: Value Stageスイムレーンで重複なし
- **中身の充填に最適**: 具体的なシナリオで業務理解を深める
- **ビジネスユーザーが語りやすい**: 抽象的なCapabilityより具体的

---

## DDD用語との対応（技術者向け参照）

| Parasol用語 | DDD用語 | 備考 |
|-------------|---------|------|
| Value Stage | Domain | 戦略的分類を含む |
| Capability | Subdomain | サービス候補 |
| ハイレベルUC | Use Case | 業務オペレーション |
| Service境界 | Bounded Context | Phase 4で確定 |

---

## コマンド体系

```bash
# Level 1: ビジネス層
/parasol:2-value                    # WHAT: 価値定義
/parasol:2-value VS1                # HOW: Value Stream詳細

# Level 2: サービス層
/parasol:3-capabilities             # WHAT: Capability一覧
/parasol:3-capabilities VS1         # 特定VSのCapability
/parasol:4-architecture             # HOW: Service設計

# Level 3: 実装層
/parasol:5-software [service]       # WHAT: Software設計
/parasol:6-implementation [service] # HOW: 実装
```

---

## 重要な原則

### 1. Phase 4でサービス枠をフリーズ

```
Phase 1-4: 設計フェーズ（変更容易）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           ↓ Phase 4完了 = サービス枠確定
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 5-6: 実装フェーズ（枠内で作業）
```

### 2. 各レベルでWHAT→HOWを完了してから次へ

```
✓ L1: 価値が明確 → Value Streamが定義できる
✓ L2: Capabilityが明確 → Service境界が決まる
✓ L3: 設計が明確 → 実装できる
```

### 3. 上位レベルの決定は下位に影響

```
価値変更 → 全レベルに影響（大）
Capability変更 → L2-L3に影響（中）
設計変更 → L3のみ影響（小）
```

---

## 参照

- `/parasol:0-help concepts` - 主要概念の説明
- `/parasol:0-help workflow` - 実行ワークフロー
- `parasol-v5/FRAMEWORK-DESIGN.md` - 詳細設計ドキュメント
