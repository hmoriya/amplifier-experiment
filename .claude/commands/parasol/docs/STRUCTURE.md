# Parasol V5 ドキュメント構造

**作成日**: 2025-12-14  
**バージョン**: V1.0

## ディレクトリ構造

```
docs/
├── STRUCTURE.md               # このファイル
├── commands/                  # コマンドリファレンス
│   ├── 0-init.md             # 初期化コマンド
│   ├── 1-context.md          # コンテキストコマンド
│   ├── 2-value.md            # 価値コマンド
│   └── ...                   # 各フェーズコマンド
├── guides/                    # ガイドドキュメント
│   ├── V5-COMPREHENSIVE-GUIDE.md  # 初心者向け総合ガイド
│   ├── GUIDE-SPECIFICATION.md     # ガイド仕様書
│   └── IMPLEMENTATION-GUIDE.md    # 実装ガイド
├── reference/                 # リファレンスドキュメント
│   ├── explore-v2.md         # 6軸探索システム
│   ├── VERSION-GUIDE.md      # バージョンガイド
│   └── PHILOSOPHY.md         # 哲学文書
├── philosophy/                # 哲学・原則文書
│   ├── zigzag-process.md     # ジグザグプロセス
│   ├── capability-naming.md  # ケイパビリティ命名ガイド
│   └── philosophy-checkpoints.md # 哲学チェックポイント
├── value-system/              # 価値トレーサビリティシステム
│   └── _value-traceability-system/  # トレーサビリティ文書
└── book/                      # 完全書籍版（350-400ページ）
    ├── README.md              # 書籍概要
    ├── part1-foundation/      # 第I部：基礎編（80-90ページ）
    │   ├── chapter1-why-parasol.md      # 第1章
    │   ├── chapter2-overview.md         # 第2章
    │   ├── chapter3-philosophy.md       # 第3章
    │   └── chapter4-ddd-relationship.md # 第4章
    ├── part2-understanding/   # 第II部：理解編（120-130ページ）
    │   ├── chapter5-phase0-1.md         # 第5章
    │   ├── chapter6-phase2.md           # 第6章
    │   ├── chapter7-phase3.md           # 第7章
    │   ├── chapter8-phase4-7.md         # 第8章
    │   └── chapter9-traceability.md     # 第9章
    ├── part3-practice/        # 第III部：実践編（100-110ページ）
    │   ├── chapter10-industry-patterns.md # 第10章
    │   ├── chapter11-claude-integration.md # 第11章
    │   ├── chapter12-team-scaling.md      # 第12章
    │   └── chapter13-troubleshooting.md   # 第13章
    ├── part4-advanced/        # 第IV部：発展編（80-90ページ）
    │   ├── chapter14-custom-patterns.md    # 第14章
    │   └── chapter15-future-evolution.md   # 第15章
    └── appendix/              # 付録（65ページ）
        ├── appendix-a-reference.md         # 付録A
        ├── appendix-b-patterns.md          # 付録B
        └── appendix-c-glossary.md          # 付録C
```

## 文書分類ガイド

### 1. commands/ - コマンドリファレンス
- 各フェーズの実行コマンド
- コマンドオプションと使用例
- 入出力仕様

### 2. guides/ - ガイドドキュメント
- 初心者向けチュートリアル
- 実装ガイド
- ベストプラクティス

### 3. reference/ - リファレンスドキュメント
- システム仕様
- APIリファレンス
- 技術詳細

### 4. philosophy/ - 哲学・原則文書
- Parasolの設計思想
- 原則と価値観
- 意思決定ガイドライン

### 5. value-system/ - 価値トレーサビリティシステム
- トレーサビリティ仕様
- 検証ルール
- 品質保証メカニズム

### 6. book/ - 完全書籍版
- 体系的な学習教材
- 段階的な理解を促進
- 実践から発展まで網羅

## 移行計画

### Phase 1: 基本構造の確立
- [x] ディレクトリ作成
- [ ] 既存ドキュメントの分類
- [ ] 基本的な移動作業

### Phase 2: 内容の整理
- [ ] 重複内容の統合
- [ ] 相互参照の更新
- [ ] インデックス作成

### Phase 3: 書籍版制作
- [ ] 第I部の執筆開始
- [ ] 各章の構成確定
- [ ] 実例とケーススタディの準備