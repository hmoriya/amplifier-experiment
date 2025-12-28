# Parasol V5.4 完全ガイド（モジュラー版）

**バージョン**: V5.4  
**総ページ数**: 500ページ  
**最終更新**: 2025-12-27

## 本書の特徴

### モジュラー構成の利点
- **8部38章の体系的構成** - 価値領域・問題領域・解決領域を明確に分離
- **段階的学習** - 初心者から上級者まで、レベルに応じた学習パスを提供
- **実践重視** - 各章に具体例とケーススタディを収録
- **V5.4新機能完全対応** - Axiomatic Design、Design Matrix、ZIGZAG思想を統合

## 全体構成

### [第I部：基礎編「Parasol V5への招待」](./part1-foundation/README.md)（50ページ）
フレームワークの全体像と基本思想を理解します。

- [第1章：なぜParasol V5なのか](./part1-foundation/chapter1-why-parasol-v5.md)
- [第2章：3つのスペース - WHY・WHAT・HOW](./part1-foundation/chapter2-three-spaces.md)
- [第3章：Parasol哲学とマインドセット](./part1-foundation/chapter3-philosophy.md)
- [第4章：Axiomatic Designと設計公理](./part1-foundation/chapter4-axiomatic-design.md)
- [第5章：V5とDDDの融合](./part1-foundation/chapter5-v5-and-ddd.md)

### [第II部：組織理解編「プロジェクトの土台」](./part2-organization/README.md)（30ページ）
プロジェクトを始める前の準備と理解を深めます。

- [第6章：Phase 0 - 組織とドメインの理解](./part2-organization/chapter6-phase0-organization.md)
- [第7章：Phase 1 - プロジェクト基盤構築](./part2-organization/chapter7-phase1-foundation.md)
- [第8章：産業パターンの選択と適用](./part2-organization/chapter8-industry-patterns.md)

### [第III部：価値領域編「WHY - なぜ作るのか」](./part3-value-space/README.md)（60ページ）
ビジネス価値の発見と定義を学びます。

- [第9章：Phase 2 - 価値ストリームの発見](./part3-value-space/chapter9-value-stream-discovery.md)
- [第10章：価値ステージ（VS）設計](./part3-value-space/chapter10-value-stage-design.md)
- [第11章：価値レベル（VL）の階層化](./part3-value-space/chapter11-value-level-hierarchy.md)
- [第12章：価値指標とマイルストーン設定](./part3-value-space/chapter12-value-metrics.md)

### [第IV部：問題領域編「WHAT - 何を作るのか」](./part4-problem-space/README.md)（60ページ）
ビジネス能力の定義とモデリングを習得します。

- [第13章：Phase 3 - ケイパビリティの発見](./part4-problem-space/chapter13-capability-discovery.md)
- [第14章：CL階層とビジネス能力の構造化](./part4-problem-space/chapter14-cl-hierarchy.md)
- [第15章：ZIGZAGプロセスによる変換](./part4-problem-space/chapter15-zigzag-process.md)
- [第16章：Design Matrixによる設計評価](./part4-problem-space/chapter16-design-matrix.md)

### [第V部：解決領域編「HOW - どう作るのか」](./part5-solution-space/README.md)（160ページ）
技術的な実装方法を詳細に解説します。

#### セクション1：アーキテクチャ（Phase 4）
- [第17章：アーキテクチャパターンの選択](./part5-solution-space/section1-architecture/chapter17-architecture-patterns.md)
- [第18章：BCへのマッピングと境界設計](./part5-solution-space/section1-architecture/chapter18-bc-mapping.md)
- [第19章：技術スタックの決定](./part5-solution-space/section1-architecture/chapter19-tech-stack.md)

#### セクション2：ソフトウェア設計（Phase 5）
- [第20章：ドメインモデルの詳細設計](./part5-solution-space/section2-software-design/chapter20-domain-model.md)
- [第21章：APIとインターフェース設計](./part5-solution-space/section2-software-design/chapter21-api-interface.md)
- [第22章：データベースとイベント設計](./part5-solution-space/section2-software-design/chapter22-database-event.md)

#### セクション3：実装（Phase 6）
- [第23章：実装パターンとベストプラクティス](./part5-solution-space/section3-implementation/chapter23-implementation-patterns.md)
- [第24章：テスト戦略と品質保証](./part5-solution-space/section3-implementation/chapter24-test-strategy.md)
- [第25章：コードレビューと改善](./part5-solution-space/section3-implementation/chapter25-code-review.md)

#### セクション4：プラットフォーム（Phase 7）
- [第26章：デプロイメントアーキテクチャ](./part5-solution-space/section4-platform/chapter26-deployment.md)
- [第27章：CI/CDパイプライン構築](./part5-solution-space/section4-platform/chapter27-cicd.md)
- [第28章：監視とオブザーバビリティ](./part5-solution-space/section4-platform/chapter28-monitoring.md)

### [第VI部：統合編「価値の実現」](./part6-integration/README.md)（40ページ）
全体を通じた価値の追跡と実現方法を学びます。

- [第29章：価値トレーサビリティシステム](./part6-integration/chapter29-value-traceability.md)
- [第30章：Golden Threadによる一貫性確保](./part6-integration/chapter30-golden-thread.md)
- [第31章：価値指標の測定と改善](./part6-integration/chapter31-value-measurement.md)

### [第VII部：実践編「チームでの適用」](./part7-practice/README.md)（60ページ）
実際のプロジェクトでの活用方法を詳説します。

- [第32章：Claude Code統合実践](./part7-practice/chapter32-claude-code.md)
- [第33章：チーム編成とスケーリング](./part7-practice/chapter33-team-scaling.md)
- [第34章：よくあるトラブルと解決法](./part7-practice/chapter34-troubleshooting.md)
- [第35章：カスタムパターンの開発](./part7-practice/chapter35-custom-patterns.md)

### [第VIII部：発展編「未来への道」](./part8-evolution/README.md)（30ページ）
継続的な改善と発展の方向性を示します。

- [第36章：V5の進化と最新動向](./part8-evolution/chapter36-v5-evolution.md)
- [第37章：コミュニティへの参加と貢献](./part8-evolution/chapter37-community.md)
- [第38章：次世代への展望](./part8-evolution/chapter38-future-vision.md)

### [付録](./appendices/README.md)（40ページ）
- [付録A：コマンドリファレンス](./appendices/appendix-a-commands.md)
- [付録B：チェックリストとテンプレート](./appendices/appendix-b-checklists.md)
- [付録C：用語集](./appendices/appendix-c-glossary.md)
- [付録D：参考文献とリソース](./appendices/appendix-d-references.md)

## 読者別推奨学習パス

### 初心者向け（基礎理解）
1. 第I部（第1-5章）- 基本概念の理解
2. 第II部（第6-7章）- プロジェクトの始め方
3. 第III部（第9章）- 価値ストリームの基礎
4. 第VII部（第32章）- Claude Code実践

### 実践者向け（体系的習得）
1. 第I部（第2、4章）- 3スペースとAxiomatic Design
2. 第III-V部（全章）- 価値から実装までの完全な流れ
3. 第VI部（全章）- 価値の追跡と実現

### 上級者向け（深化と拡張）
1. 第IV部（第15-16章）- ZIGZAG、Design Matrix
2. 第V部（セクション3-4）- 実装とプラットフォーム
3. 第VII部（第35章）- カスタムパターン開発
4. 第VIII部（全章）- 最新動向と将来

### マネージャー向け（戦略的理解）
1. 第I部（第1-2章）- 全体像の把握
2. 第III部（全章）- 価値管理の方法
3. 第VI部（第29-30章）- 価値追跡システム
4. 第VII部（第33章）- チーム運営

## 本書の活用方法

### 学習のポイント
1. **理論と実践のバランス** - 各章の概念を理解したら、必ず実践例を試す
2. **段階的な理解** - 無理に全章を読まず、自分のレベルに合わせて進める
3. **反復学習** - 実プロジェクトで適用しながら、該当章を読み返す
4. **コミュニティ活用** - 不明点は積極的にコミュニティで質問する

### 演習問題の取り組み方
- 各章末の演習は、理解度を確認する重要な要素
- まず自力で解いてから、解答例を参照
- 実際のプロジェクトに置き換えて考える

## V5.4の新機能

本書では、V5.4で追加された以下の機能を重点的に解説しています：

1. **Axiomatic Design統合** - 設計公理による品質保証
2. **Design Matrix評価** - 結合度の可視化と改善
3. **ZIGZAG思想** - 問題と解決の往復による洗練
4. **ビジネス時間的凝集** - 顧客体験に基づく新しい凝集概念

## フィードバック

本書の改善のため、以下の方法でフィードバックをお寄せください：

- GitHub Issues: [parasol-framework/books](https://github.com/parasol-framework/books)
- コミュニティフォーラム: [community.parasol.dev](https://community.parasol.dev)
- メール: feedback@parasol.dev

---

**継続的な更新**: 本書は四半期ごとに更新され、新しいパターンや実践例が追加されます。