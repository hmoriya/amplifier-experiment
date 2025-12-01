# Parasol V5 概要

## Parasol V5とは

**Parasol V5**は、ビジネス価値からソフトウェア実装までを体系的に変換する**価値駆動型開発フレームワーク**です。Amplifier DDDの構造を基盤とし、**ZIGZAGプロセス**という独自の分解手法により、抽象的なビジネス要求を具体的な実装へと段階的に落とし込みます。

---

## 3つの核心コンセプト

### 1. ZIGZAG（視座転換による創発的分解）

```
┌─────────────────────────────────────────────────────────────────────┐
│ ZIGZAG = 視座転換による創発的分解                                    │
│                                                                     │
│ WHATの抽象語彙空間で行き詰まった時、                                 │
│ HOWの具体語彙空間への強制転換により、                                │
│ 元のWHATに暗黙に含まれていた未言語化概念が顕在化する。               │
│                                                                     │
│ これは「分解」ではなく「創発」である。                               │
└─────────────────────────────────────────────────────────────────────┘
```

**従来手法との違い**

| 手法 | 進行パターン | 限界 |
|------|-------------|------|
| トップダウン | WHAT→WHAT→WHAT | 抽象度の壁で停止 |
| ボトムアップ | HOW→HOW→HOW | 全体像を見失う |
| **ZIGZAG** | WHAT↔HOW交互 | 壁を迂回して進む |

### 2. 3層モデル

```
┌─────────────────────────────────────────────────────────────────────┐
│  Level 1: ビジネス層                                                │
│    WHAT: 価値        →        HOW: Value Stream                    │
│    Phase 2 前半               Phase 2 後半                         │
└─────────────────────────────────────────────────────────────────────┘
                                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  Level 2: サービス層                                                │
│    WHAT: Capability  →        HOW: Service設計                     │
│    Phase 3                    Phase 4 ※ここでサービス境界確定       │
└─────────────────────────────────────────────────────────────────────┘
                                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  Level 3: 実装層                                                    │
│    WHAT: Software設計 →       HOW: 実装                            │
│    Phase 5                    Phase 6                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 3. 4階層ケイパビリティ分解

```
WHAT       →      HOW        →      WHAT       →      HOW
何の領域?        どう組織?         何をする?         どう実装?
    │               │                │                │
   CL1            CL2              CL3              BC
 活動領域     ケイパビリティ     業務OP          実装設計
 ─────────   ────────────     ─────────       ─────────
  経営層        事業部長        業務担当         開発者
```

| レベル | 名称 | 対象者 | 内容 |
|--------|------|--------|------|
| **CL1** | 活動領域 | 経営層 | Core/Supporting/Generic分類、投資判断 |
| **CL2** | ケイパビリティ | 事業部長 | チーム境界、サービス候補 |
| **CL3** | 業務オペレーション | 業務担当 | トリガー→活動→成果物 |
| **BC** | 実装設計 | 開発者 | 集約、イベント、API契約 |

---

## 7つのフェーズ

| Phase | 名称 | ZIGZAG位置 | 主要成果物 |
|-------|------|-----------|-----------|
| **1** | Context | 基盤 | organization-analysis.md |
| **2** | Value | L1 WHAT→HOW | value-definition.md, value-streams-mapping.md |
| **3** | Capabilities | L2 WHAT | capabilities.md, cl1-cl3定義 |
| **4** | Architecture | L2 HOW | service-boundaries.md, context-map.md |
| **5** | Software | L3 WHAT | domain-model.md, api-specs/ |
| **6** | Implementation | L3 HOW | src/, tests/ |
| **7** | Platform | 運用基盤 | infrastructure.md, cicd-pipeline.md |

---

## 主要な特徴

### 1. 価値駆動（Value-Driven）

- ビジネス価値から出発し、逆算で設計
- バックキャスティング手法（理想状態MS5→現在MS1）
- 価値とソフトウェアの完全なトレーサビリティ

### 2. 段階的分解（Progressive Decomposition）

- 数字付きコマンドによる明確な実行順序
- 各フェーズで前フェーズの成果物を入力
- Phase 4でサービス境界を確定（以降の変更は高コスト）

### 3. DDD統合（DDD Integration）

| Parasol用語 | DDD用語 | 備考 |
|-------------|---------|------|
| Value Stage | Domain | 戦略的分類を含む |
| Capability | Subdomain | サービス候補 |
| Service境界 | Bounded Context | Phase 4で確定 |

### 4. 設計ストーリー（Design Story）

各フェーズで「なぜそう設計したか」を自動出力：

- **理解促進**: チーム全員が設計判断の背景を理解
- **意思決定記録**: 後から見直す際に根拠がわかる
- **学習資産**: プロジェクト固有の知見を蓄積

### 5. Amplifierサブエージェント連携

| フェーズ | サブエージェント | 用途 |
|----------|-----------------|------|
| Phase 1 | concept-extractor, content-researcher | 業界知識抽出 |
| Phase 2 | insight-synthesizer, knowledge-archaeologist | 価値洞察 |
| Phase 3 | zen-architect (ANALYZE/ARCHITECT) | ケイパビリティ設計 |
| Phase 4 | zen-architect, integration-specialist | サービス設計 |
| Phase 5 | api-contract-designer, database-architect | 技術設計 |
| Phase 6 | modular-builder, test-coverage, bug-hunter | 実装 |
| Phase 7 | security-guardian | インフラ設計 |

---

## コマンド体系

```bash
# ヘルプ・管理
/parasol:0-help [topic]      # ヘルプ
/parasol:0-status            # 進捗確認
/parasol:0-validate          # 検証

# プロジェクト管理
/parasol:0-project init {name}  # 新規作成
/parasol:0-project list         # 一覧
/parasol:0-init {url}           # URL起動

# 実行コマンド（順序通り）
/parasol:1-context           # Phase 1: コンテキスト
/parasol:2-value [VS番号]    # Phase 2: 価値定義
/parasol:3-capabilities [mode] [target]  # Phase 3: ケイパビリティ
/parasol:4-architecture      # Phase 4: アーキテクチャ
/parasol:5-software [service] [bc]       # Phase 5: ソフトウェア設計
/parasol:6-implementation [service] [bc] # Phase 6: 実装
/parasol:7-platform          # Phase 7: プラットフォーム
```

---

## Value Stage Swimlaneパターン

Value StreamのStageをスイムレーンとしてCapabilityを分解し、重複のないサービス境界を導出：

```
Value Stream: 調達 → 製造 → 販売

┌──────────┐  ┌──────────┐  ┌──────────┐
│ Stage:   │  │ Stage:   │  │ Stage:   │  ← スイムレーン
│ 調達     │  │ 製造     │  │ 販売     │
├──────────┤  ├──────────┤  ├──────────┤
│原料調達  │  │製品開発  │  │受注管理  │  ← Capability
│品質検査  │  │生産管理  │  │出荷管理  │    （サービス候補）
│在庫管理  │  │品質保証  │  │顧客管理  │
└──────────┘  └──────────┘  └──────────┘
```

---

## ZIGZAG実践ガイド

### 「詰まり」の検知シグナル

1. **同じ単語が3回以上繰り返される**
2. **「つまり」で言い換えても新情報がない**
3. **抽象度が変わらない**（上にも下にも行けない）

### 突破方法

```
詰まり検知
  ↓
「これをどう実装/実現するか？」と強制的に問う
  ↓
具体的な手段・技術・活動を列挙
  ↓
各HOWから見えてくる新しいWHATを言語化
  ↓
新しいWHAT（WHAT'）を記録して次へ
```

---

## 重要な原則

### 1. Phase 4でサービス枠をフリーズ

```
Phase 1-4: 設計フェーズ（変更容易）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           ↓ Phase 4完了 = サービス枠確定
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 5-7: 実装フェーズ（枠内で作業）
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

## クイックスタート

```bash
# 1. ヘルプを確認
/parasol:0-help

# 2. プロジェクト作成
/parasol:0-project init my-project

# 3. コンテキストから開始
/parasol:1-context

# 4. 価値定義
/parasol:2-value

# 5. 以降、順次実行
/parasol:3-capabilities cl1
/parasol:3-capabilities cl2 VS1
...
```

---

## ライセンス

MIT License - Copyright (c) Microsoft Corporation

商用利用可能。LICENSEファイルを保持すること。

---

## 参照

- 詳細設計: `.claude/commands/parasol/_zigzag-process.md`
- ヘルプ: `/parasol:0-help`
- 価値方法論: `.claude/commands/parasol/_value-methodology.md`
