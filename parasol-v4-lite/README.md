# Parasol V4 Lite Framework

## 概要

Parasol V4 Liteは、Amplifier DDDフレームワークの構造を参考にした、軽量版のParasol開発フレームワークです。数字付きコマンド体系により、実行順序が明確で、段階的な開発プロセスを提供します。

## コマンド体系

Parasol V4 LiteはAmplifier DDDと同様の`/parasol:*`コマンド形式を採用：

```bash
# 基本コマンド
/parasol:0-help        # ヘルプとガイド
/parasol:status        # 現在のステータス確認

# 実行コマンド（順序通りに実行）
/parasol:1-context     # Phase 0: プロジェクトコンテキスト
/parasol:2-value       # Phase 1: 価値定義と企業活動設計
/parasol:3-business    # Phase 2: バリューステージ設計
/parasol:4-architecture # Phase 3: アプリケーションアーキテクチャ
/parasol:5-software    # Phase 4: ソフトウェア設計
/parasol:6-implementation # Phase 5: ソフトウェア実装
/parasol:7-platform    # Phase 6: プラットフォーム設計
```

## ディレクトリ構造

```
parasol-v4-lite/
├── README.md                    # このファイル
├── QUICK-START.md              # クイックスタートガイド
│
├── commands/                    # 実行可能なコマンド
│   ├── 0-help.md               # ヘルプとガイド
│   ├── status.md               # ステータス確認
│   ├── 1-context.md            # プロジェクトコンテキスト
│   ├── 2-value.md              # 価値定義
│   ├── 3-business.md           # ビジネス設計
│   ├── 4-architecture.md       # アーキテクチャ設計
│   ├── 5-software.md           # ソフトウェア設計
│   ├── 6-implementation.md     # 実装
│   └── 7-platform.md           # プラットフォーム
│
├── outputs/                     # 各フェーズの成果物
│   ├── 1-context/              # コンテキスト成果物
│   ├── 2-value/                # 価値定義成果物
│   ├── 3-business/             # ビジネス設計成果物
│   ├── 4-architecture/         # アーキテクチャ成果物
│   ├── 5-software/             # ソフトウェア設計成果物
│   ├── 6-implementation/       # 実装成果物
│   └── 7-platform/             # プラットフォーム成果物
│
└── templates/                   # テンプレート（オプション）
    ├── decisions/              # 決定記録テンプレート
    └── outputs/                # 成果物テンプレート
```

## 実行フロー

### 1. 初期化とヘルプ

```bash
# ヘルプを表示
/parasol:0-help

# 現在のステータス確認
/parasol:status
```

### 2. 順次実行

```bash
# Step 1: プロジェクトコンテキストの確立
/parasol:1-context

# Step 2: 価値定義と企業活動設計
/parasol:2-value

# Step 3: バリューステージ設計
/parasol:3-business

# Step 4: アプリケーションアーキテクチャ設計
/parasol:4-architecture

# Step 5: ソフトウェア設計
/parasol:5-software

# Step 6: ソフトウェア実装
/parasol:6-implementation

# Step 7: プラットフォーム設計
/parasol:7-platform
```

## 特徴

### 1. 数字付きコマンド
- 実行順序が一目瞭然
- 段階的な進行が明確
- スキップや選択実行も可能

### 2. Amplifier DDDとの互換性
- 同様のコマンド体系
- 既存のAmplifierツールと組み合わせ可能
- 学習曲線が緩やか

### 3. 軽量版の利点
- 迅速なプロトタイピング
- 概念実証に最適
- 必要に応じて詳細化可能

## V4フレームワークの核心概念

### バリューストリーム
価値提供状態の連続的な流れ

### バリューステージ（VS）
- VS0: 汎用・横断的基盤
- VS1-VS7: 価値実現ステージ

### ケーパビリティ階層
- CL1: 戦略的（境界コンテキスト）
- CL2: 戦術的（マイクロサービス）
- CL3: オペレーショナル
- L4: 詳細ユースケース

### 決定記録
- VDR: 価値決定
- BDR: ビジネス決定
- AADR: アーキテクチャ決定
- SADR: ソフトウェア決定
- PDR: プラットフォーム決定

## クイックスタート

```bash
# 1. ヘルプを確認
/parasol:0-help

# 2. プロジェクトコンテキストから開始
/parasol:1-context

# 3. 各成果物はoutputs/に自動保存
ls outputs/1-context/
```

## デモ実行

```bash
# デモモードで全フェーズを連続実行
/parasol:demo

# 特定フェーズのデモ
/parasol:demo --phase=3-business
```

## カスタマイズ

各`commands/*.md`ファイルを編集することで、プロジェクト固有の要件に合わせてカスタマイズ可能です。

## サポート

- ドキュメント: `commands/0-help.md`
- ステータス確認: `/parasol:status`
- V4完全版への拡張: 必要に応じて各コマンドを詳細化

---

*Parasol V4 Lite - Amplifier DDD構造を採用した軽量版Parasolフレームワーク*