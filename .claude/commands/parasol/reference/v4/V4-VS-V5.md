# Parasol V4 vs V5 比較

このドキュメントはParasol V4とV5の主要な違いを解説します。

---

## 概要比較

| 項目 | V4（アーカイブ） | V5（アクティブ） |
|------|-----------------|-----------------|
| **設計思想** | 重厚長大な本格的DDD | 実用的・軽量なアプローチ |
| **場所** | `reference/v4/` | `/.claude/commands/parasol/` |
| **実行方法** | `/ddd:1-plan` + MDファイル | `/parasol:X-xxx` スラッシュコマンド |
| **所要時間** | 複数日〜週単位 | 数時間〜数日 |
| **対象規模** | 大規模エンタープライズ | 中小〜大規模対応 |

---

## フェーズ構成の違い

### V4: 6フェーズ構成

```
Phase 1: 価値分析
    ↓
Phase 2: 能力設計（L1→L2→L3）
    ↓
Phase 3: ドメインモデリング
    ↓
Phase 4: オペレーション設計
    ↓
Phase 5: 実装生成
    ↓
Phase 6: 検証・最適化
```

### V5: 8フェーズ構成

```
Phase 0: プロジェクト初期化
    ↓
Phase 1: コンテキスト設定
    ↓
Phase 2: 価値定義（VS0-VS7）
    ↓
Phase 3: ケイパビリティ分解（CL1→CL2→CL3）
    ↓
Phase 4: アプリケーション設計
    ↓
Phase 5: ソフトウェア設計
    ↓
Phase 6: 実装
    ↓
Phase 7: プラットフォーム
```

---

## 能力階層の違い

### V4: L1-L2-L3モデル

| レベル | 名称 | 説明 |
|--------|------|------|
| **L1** | 戦略的能力 | Strategic Capabilities |
| **L2** | 戦術的能力 | Tactical Capabilities |
| **L3** | 運用的能力 | Operational Capabilities |

### V5: CL0-CL1-CL2-CL3モデル

| レベル | 名称 | 説明 |
|--------|------|------|
| **CL0** | 企業活動 | Enterprise Activities |
| **CL1** | 活動領域 | Activity Areas |
| **CL2** | ケイパビリティ | Capabilities |
| **CL3** | ビジネスオペレーション | Business Operations |

**主な違い**:
- V5はCL0（企業活動）を追加し、より上位からの分解を可能に
- V5はCL3からBC（Bounded Context）への明確なマッピングを提供

---

## 価値定義の違い

### V4: Business Nine Dimensions

9つの次元で価値を構造化：
1. Customer Value
2. Revenue Model
3. Market Position
4. Operations
5. Technology
6. Organization
7. Partners
8. Resources
9. Cost Structure

### V5: 価値ストリーム（VS0-VS7）

8つの価値ストリームで構造化：
- **VS0**: コア価値創造
- **VS1-VS7**: 支援価値ストリーム

**追加概念**:
- **VL（Value Level）**: 価値レベル階層
- **VMS（Value Milestone）**: 価値マイルストーン
- **VSTR（Value Stream Trace）**: 価値追跡

---

## 実行方法の違い

### V4: DDD統合実行

```bash
# コンテキストロード
/ddd:prime

# フェーズ別実行
/ddd:1-plan phase2-capability/2-1-strategic-capabilities.md
/ddd:2-docs
/ddd:3-code-plan
/ddd:4-code
/ddd:5-finish
```

### V5: スラッシュコマンド直接実行

```bash
# ヘルプ
/parasol:0-help

# フェーズ別実行
/parasol:0-project create [name]
/parasol:1-context
/parasol:2-value
/parasol:3-capabilities
/parasol:4-application-design
/parasol:5-software-design
/parasol:6-implementation
/parasol:7-platform
```

---

## 設計原則の違い

### V4の特徴

- **網羅的**: すべての可能性を事前に設計
- **ドキュメント重視**: 詳細な設計書を生成
- **トップダウン**: 戦略から運用へ順次分解
- **完全性追求**: 実装前に設計を完成させる

### V5の特徴

- **実用的**: 必要十分な設計に集中
- **イテレーティブ**: 段階的に詳細化
- **価値駆動**: 常に価値への貢献を確認
- **ZIGZAG**: FR→DP往復による設計プロセス
- **公理的設計統合**: 独立公理・情報公理による設計評価

---

## ツール・パターンの違い

### V4固有

- `bundles/`: 業界別・パターン別バンドル
- `contracts/`: フェーズ間コントラクト
- `knowledge/`: 学習・メトリクス蓄積

### V5固有

- `_commands-v5/`: 統合実行コマンド
- `_capability-knowledge/`: ケイパビリティ知識ベース
- `projects/`: プロジェクト別アーティファクト
- 公理的設計アドバイザー統合

---

## どちらを使うべきか

### V4が適している場合

- 大規模エンタープライズの全面刷新
- 複数チームによる長期プロジェクト
- 詳細な設計ドキュメントが必須
- レガシーシステムの完全移行

### V5が適している場合（推奨）

- 新規プロジェクト
- 中小規模のシステム開発
- アジャイル・イテレーティブな開発
- 迅速な価値検証が必要
- Claude Codeとの統合活用

---

## 移行ガイド

V4からV5への概念マッピング：

| V4 | V5 | 備考 |
|----|----|----|
| L1 戦略的能力 | CL1 活動領域 | より上位にCL0を追加 |
| L2 戦術的能力 | CL2 ケイパビリティ | ほぼ同等 |
| L3 運用的能力 | CL3 ビジネスオペレーション | BC境界確定を追加 |
| Nine Dimensions | VS0-VS7 | 価値ストリーム概念に進化 |
| Phase 1-6 | Phase 0-7 | 初期化・プラットフォーム追加 |

---

## 関連リンク

- [V5 概要](../overview-v5.md)
- [V5 フレームワーク](../../)
- [公理的設計アドバイザー](/.claude/agents/axiomatic-design-advisor.md)
