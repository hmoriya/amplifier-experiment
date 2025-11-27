# アークウェイプロジェクト

## 概要

アークウェイ株式会社のビジネスドメインとケイパビリティを、Parasol V4 Liteフレームワークを使用してDDD（ドメイン駆動設計）の観点から分析するプロジェクトです。

## 対象企業

**アークウェイ株式会社**
- URL: https://www.archway.co.jp/
- 業界: ITサービス業
- 主要サービス: システム開発、ITコンサルティング、クラウドソリューション

## プロジェクト構造

```
archway/
├── parasol.yaml        # プロジェクト設定ファイル
├── README.md          # このファイル
└── outputs/           # 各フェーズの成果物
    ├── 0-init/        # Phase 0: 企業情報の初期分析
    ├── 1-context/     # Phase 1: コンテキスト分析
    ├── 2-value/       # Phase 2: バリューストリーム定義
    ├── 3-capabilities/# Phase 3: ケイパビリティ分析
    ├── 4-implementation/# Phase 4: 実装パターン
    ├── 5-assembly/    # Phase 5: 統合戦略
    ├── 6-deployment/  # Phase 6: 展開戦略
    └── 7-platform/    # Phase 7: プラットフォーム設計
```

## フェーズ概要

### Phase 0: Init (初期化)
- 企業の公開情報を収集し、初期分析を実施
- 戦略的な観点からの企業理解を構築

### Phase 1: Context (コンテキスト)
- ステークホルダーマッピング
- ビジネス制約の特定
- 組織構造の分析
- 市場環境の評価

### Phase 2: Value (バリュー)
- 価値定義
- バリューストリームマッピング
- エンタープライズ活動の分析

### Phase 3: Capabilities (ケイパビリティ)
- ドメイン分類（コア/サポート/汎用）
- サブドメイン設計
- 境界付けられたコンテキストの定義

### Phase 4: Implementation (実装)
- 実装パターンの定義
- アーキテクチャ決定

### Phase 5: Assembly (アセンブリ)
- 統合パターン
- アセンブリ戦略

### Phase 6: Deployment (デプロイメント)
- 展開戦略
- ロールアウト計画

### Phase 7: Platform (プラットフォーム)
- プラットフォームアーキテクチャ
- インフラストラクチャ設計

## 使用方法

各フェーズのコマンドを実行してプロジェクトを進めます：

```bash
# Phase 0: 初期分析の実行
make parasol/0-init url=https://www.archway.co.jp/

# Phase 1: コンテキスト分析
make parasol/1-context

# Phase 2: バリューストリーム定義
make parasol/2-value

# Phase 3: ケイパビリティ分析
make parasol/3-capabilities

# 以降のフェーズも同様に実行
```

## 進捗状況

| フェーズ | ステータス | 最終更新日 |
|---------|-----------|------------|
| Phase 0 | pending   | -          |
| Phase 1 | pending   | -          |
| Phase 2 | pending   | -          |
| Phase 3 | pending   | -          |
| Phase 4 | pending   | -          |
| Phase 5 | pending   | -          |
| Phase 6 | pending   | -          |
| Phase 7 | pending   | -          |

## 関連ドキュメント

- [Parasol V4 Lite Framework](../../parasol-v4-lite/)
- [DDD戦略的設計ガイド](../../docs/ddd-strategic-design.md)