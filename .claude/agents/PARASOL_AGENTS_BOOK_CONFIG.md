# Parasol Agents Book Configuration

このファイルは、すべてのParasolフェーズエージェントが書籍構造を認識し、適切に参照するための共通設定です。

## エージェントと書籍章の対応表

### Phase 0: parasol-phase0-assessment（未実装）
- **Chapter 6**: Phase 0: 組織アセスメント
  - Targetの失敗事例（20億ドル損失）
  - POMM（Parasol組織成熟度モデル）
  - 組織評価ツール

### Phase 1: parasol-phase1-context
- **Chapter 7**: Phase 1: 組織コンテキスト確立 
  - 市場分析フレームワーク
  - ステークホルダー分析
  - 制約カタログ
- **関連章**: Chapter 6（前提）, Chapter 8（業界パターン）

### Phase 2: parasol-phase2-value
- **Chapter 9**: Phase 2: 価値ストリーム発見
  - Amazon配送の例
  - VSM（価値ストリームマッピング）
  - 価値の多面的定義
- **Chapter 10**: 価値ステージ設計
- **Chapter 11**: 価値レベル階層
- **Chapter 12**: 価値メトリクスと測定

### Phase 3: parasol-phase3-capabilities
- **Chapter 13**: Phase 3: ZIGZAGプロセス詳細
  - Christopher Alexanderの建築理論
  - Design Matrix進化プロセス
  - 探索・洗練・収束の3フェーズ
- **Chapter 14**: ケイパビリティ定義と管理
- **Chapter 15**: 制約の発見と管理
- **Chapter 16**: 問題から価値への翻訳

### Phase 4: parasol-phase4-architecture
- **Chapter 17**: Phase 4: アプリケーションアーキテクチャ
  - Etsyの事例
  - アーキテクチャ選択マトリクス
  - 3次元評価フレームワーク
- **Chapter 18**: 境界づけられたコンテキスト設計
- **Chapter 19**: マイクロサービス抽出戦略

### Phase 5: parasol-phase5-software
- **Chapter 20**: Phase 5: ドメイン言語とモデル
  - Zapposの変革事例
  - DDDとParasolの統合
- **Chapter 21**: 集約設計
- **Chapter 22**: ソフトウェアコンポーネント設計

### Phase 6: parasol-phase6-implementation
- **Chapter 23**: Phase 6: コード生成と標準
  - Stack Overflowのテスト文化
  - 実装品質基準
- **Chapter 24**: エラーハンドリングと復旧
- **Chapter 25**: CI/CDパイプライン
- **Chapter 26**: パフォーマンス最適化
- **Chapter 27**: セキュリティ実装
- **Chapter 28**: モニタリングと可観測性

### Phase 7: parasol-phase7-platform
- **Chapter 29**: Phase 7: プラットフォーム統合
  - Amazon/Kiva統合事例
  - プラットフォーム設計原則
- **Chapter 30**: 外部システム統合
- **Chapter 31**: API契約とバージョニング

### Support: parasol-book-architect
- **全38章**: 書籍執筆・変換支援
- **スタイルガイド**: STYLE_GUIDE.md準拠
- **品質基準**: 70:30（概念:コード）比率

## 共通参照ルール

### 1. フェーズ実行時の章参照

```markdown
このフェーズの詳細な理論的背景については、
Parasol V5.4書籍のChapter XX「タイトル」を参照してください。
```

### 2. Design Matrix活用（Phase 3以降）

```markdown
Design Matrixを更新します（Chapter 13の手法に従って）：
- FR（機能要求）の明確化
- DP（設計パラメータ）のマッピング
- 独立性（非結合）の検証
```

### 3. 実例の引用

```markdown
この概念の重要性は、Chapter XXで紹介された
[企業名]の[具体的な事例]でも示されています。
```

### 4. 付録への誘導

```markdown
実装の詳細については、
[付録XX.X: タイトル](../appendices/appendix-XX.X-filename.md)
を参照してください。
```

## 用語の統一

すべてのエージェントで以下の表記を統一：

- **ZIGZAG**（全て大文字）
- **Axiomatic Design**（頭文字大文字）
- **Design Matrix**（頭文字大文字）
- **Phase 0-7**（アラビア数字、スペースあり）
- **FR**（Functional Requirement）
- **DP**（Design Parameter）
- **ケイパビリティ**（カタカナ）
- **コンテキスト**（カタカナ）

## エージェント間連携での書籍活用

### 前フェーズ参照
```markdown
Phase Xの成果物（Chapter XXで定義）を基に、
本フェーズでは...
```

### 次フェーズへの橋渡し
```markdown
本フェーズの成果は、Phase Y（Chapter YY）で
具体的な[成果物]に変換されます。
```

---

最終更新：2025-12-29
用途：Parasolフェーズエージェントの書籍認識統一