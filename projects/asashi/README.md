# Asashi

Parasol V5 プロジェクト

作成日: 2025-11-24

## クイックスタート

```bash
cd projects/asashi

# オプション1: URLから自動初期化
/parasol:0-init https://company.example.com

# オプション2: 手動でPhase 1から開始
/parasol:1-context
```

## 進捗確認

```bash
/parasol:project info
/parasol:status
```

## プロジェクト構造

- `parasol.yaml`: プロジェクト設定
- `outputs/`: 全フェーズの成果物
- `docs/`: プロジェクト固有のドキュメント（任意）

## Phase概要

- **Phase 0**: Initialize from URL - 企業URLから自動で初期情報を収集
- **Phase 1**: Context - 組織分析、市場評価、制約条件
- **Phase 2**: Value Definition - 価値定義、バリューストリーム
- **Phase 3**: Capabilities - ドメイン分類、サブドメイン設計、境界づけられたコンテキスト
- **Phase 4**: Architecture - アプリケーションアーキテクチャ設計
- **Phase 5**: Software Design - ソフトウェア設計
- **Phase 6**: Implementation - 実装
- **Phase 7**: Platform - プラットフォーム・インフラ設計
