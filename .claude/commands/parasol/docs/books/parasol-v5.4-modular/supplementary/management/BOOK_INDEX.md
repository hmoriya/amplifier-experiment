# Parasol V5.4 モジュラー 完全索引

このファイルは、Parasol V5.4書籍の完全な索引を提供し、読者が必要な情報に素早くアクセスできるようにします。

## 主要概念索引

### A
- **Axiomatic Design** → Chapter 3, 4, 13
  - 独立性の公理 → Chapter 3 (p.XX), Chapter 4 (p.XX)
  - 情報の公理 → Chapter 3 (p.XX), Chapter 4 (p.XX)
  - Design Matrix → Chapter 4, 13, 14, 15, 16
- **API契約** → Chapter 31
  - バージョニング戦略 → Chapter 31 (p.XX)
  - 後方互換性 → Chapter 31 (p.XX)

### C
- **CI/CD** → Chapter 25
  - パイプライン設計 → Chapter 25 (p.XX)
  - 品質ゲート → Chapter 25 (p.XX)
  - カナリアデプロイ → Chapter 25 (p.XX)
- **CQRS** → Chapter 22
  - コマンドとクエリの分離 → Chapter 22 (p.XX)
  - イベントソーシング → Chapter 22 (p.XX)
- **Context Map** → Chapter 18
  - パターン一覧 → Chapter 18 (p.XX)

### D
- **DDD (Domain-Driven Design)** → Chapter 5, 20, 21
  - Parasolとの統合 → Chapter 5 (p.XX)
  - ユビキタス言語 → Chapter 20 (p.XX)
  - 境界づけられたコンテキスト → Chapter 18 (p.XX)
  - 集約 → Chapter 21 (p.XX)
- **Design Matrix** → Chapter 4, 13-16
  - FR-DPマッピング → Chapter 4 (p.XX)
  - 進化プロセス → Chapter 13 (p.XX)

### P
- **Parasol V5.4**
  - 概要 → Chapter 1 (p.XX)
  - 3つの空間 → Chapter 2 (p.XX)
  - 哲学 → Chapter 3 (p.XX)
  - 7つのフェーズ → Chapter 6-31
- **POMM (組織成熟度モデル)** → Chapter 6
  - 5段階評価 → Chapter 6 (p.XX)
  - Targetの失敗事例 → Chapter 6 (p.XX)
- **Phase 0-7** → Chapter 6-31
  - Phase 0: 組織アセスメント → Chapter 6
  - Phase 1: 組織コンテキスト → Chapter 7
  - Phase 2: 価値ストリーム → Chapter 9-12
  - Phase 3: ZIGZAG/ケイパビリティ → Chapter 13-16
  - Phase 4: アーキテクチャ → Chapter 17-19
  - Phase 5: ソフトウェア設計 → Chapter 20-22
  - Phase 6: 実装 → Chapter 23-28
  - Phase 7: プラットフォーム → Chapter 29-31

### V
- **価値ストリーム** → Chapter 9-12
  - VSM (Value Stream Mapping) → Chapter 9 (p.XX)
  - 価値ステージ → Chapter 10 (p.XX)
  - 価値階層 → Chapter 11 (p.XX)
  - メトリクス → Chapter 12 (p.XX)

### Z
- **ZIGZAG** → Chapter 13
  - プロセス詳細 → Chapter 13 (p.XX)
  - 探索・洗練・収束 → Chapter 13 (p.XX)
  - Design Matrix進化 → Chapter 13 (p.XX)

## 企業事例索引

### Amazon
- 配送システム → Chapter 9 (価値ストリーム)
- Kiva統合 → Chapter 29 (システム統合)

### Etsy
- アーキテクチャ選択 → Chapter 17
- モジュラーモノリス → Chapter 17

### Netflix
- マイクロサービス → Chapter 19, 33
- カオスエンジニアリング → Chapter 34

### Spotify
- 組織モデル → Chapter 8
- アジャイルスケーリング → Chapter 37

### Stack Overflow
- テスト文化 → Chapter 23
- CI/CDパイプライン → Chapter 25

### Target
- カナダ進出失敗 → Chapter 6
- POMM Level 3の限界 → Chapter 6

### Uber
- リアルタイムアーキテクチャ → Chapter 36
- スケーラビリティ → Chapter 33

### Zappos
- DDD実装 → Chapter 20
- 文化変革 → Chapter 37

## 技術トピック索引

### アーキテクチャパターン
- マイクロサービス → Chapter 17, 19
- モジュラーモノリス → Chapter 17
- イベント駆動 → Chapter 22, 36
- サーバーレス → Chapter 36

### テスト戦略
- 単体テスト → Chapter 23
- 統合テスト → Chapter 23
- E2Eテスト → Chapter 23, 25
- カオステスト → Chapter 34

### パフォーマンス
- 最適化手法 → Chapter 26, 33
- キャッシング → Chapter 33
- データベースチューニング → Chapter 33

### セキュリティ
- 設計原則 → Chapter 27
- 実装パターン → Chapter 27
- 監査とコンプライアンス → Chapter 27

### モニタリング
- 可観測性 → Chapter 28
- メトリクス設計 → Chapter 28
- ログ集約 → Chapter 28

## 図表索引

### PlantUML図
1. Parasol V5.4全体構造 → `parasol-v5-overview.puml`
2. Axiomatic Design原則 → `chapter03-axiomatic-design-principles.puml`
3. Design Matrix概念 → `chapter04-design-matrix.puml`
4. POMM成熟度モデル → `chapter06-pomm-maturity-model.puml`
5. 価値ストリームマッピング → `chapter09-value-stream-mapping.puml`
6. 価値階層 → `chapter11-value-hierarchy.puml`
7. ZIGZAGプロセス → `chapter13-zigzag-process.puml`
8. ケイパビリティ分解 → `chapter14-capability-decomposition.puml`
9. アーキテクチャ選択マトリクス → `chapter17-architecture-selection-matrix.puml`
10. Context Map → `chapter18-context-map.puml`
11. DDD統合 → `chapter20-ddd-integration.puml`
12. CI/CDパイプライン → `chapter25-cicd-pipeline.puml`

## 付録参照

- 付録A: 用語集
- 付録B: ツールカタログ
- 付録C: テンプレート集
- 付録D: チェックリスト
- 付録E: 参考文献

## クロスリファレンス

### Phase間の依存関係
- Phase 0 → Phase 1: 組織評価結果の活用
- Phase 1 → Phase 2: コンテキストから価値への展開
- Phase 2 → Phase 3: 価値からケイパビリティへ
- Phase 3 → Phase 4: ケイパビリティからアーキテクチャへ
- Phase 4 → Phase 5: アーキテクチャから設計へ
- Phase 5 → Phase 6: 設計から実装へ
- Phase 6 → Phase 7: 実装からプラットフォームへ

### 横断的テーマ
- **品質**: Chapter 23-28 (実装品質全般)
- **進化**: Chapter 36-38 (将来展望)
- **組織**: Chapter 6-8, 37 (組織変革)
- **価値**: Chapter 9-12 (価値中心設計)

---

最終更新：2025-12-29