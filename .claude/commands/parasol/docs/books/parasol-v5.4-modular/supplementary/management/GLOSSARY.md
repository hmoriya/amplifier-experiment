# Parasol V5.4 用語集（Glossary）

このファイルは、Parasol V5.4で使用される重要な用語と概念を定義します。各用語には日本語・英語表記、定義、関連章、使用例を含みます。

## A

### Axiomatic Design（公理的設計）
- **定義**: Nam P. Suhによって開発された科学的設計方法論。2つの公理（独立性の公理と情報の公理）に基づく
- **関連章**: Chapter 3, 4, 13
- **使用例**: 「Axiomatic Designの原則に従い、各機能要求は独立した設計パラメータで実現する」

### Aggregate（集約）
- **定義**: DDDにおける一貫性の境界。関連するエンティティと値オブジェクトのクラスタ
- **関連章**: Chapter 21
- **日本語**: 集約
- **使用例**: 「注文集約は、注文エンティティと注文明細値オブジェクトから構成される」

## B

### Bounded Context（境界づけられたコンテキスト）
- **定義**: DDDにおける明確な境界を持つモデルの適用範囲
- **関連章**: Chapter 18, 20
- **使用例**: 「決済コンテキストと配送コンテキストは明確に分離される」

### Business Component (BC)
- **定義**: ビジネスロジックを実装する技術的コンポーネント
- **関連章**: Chapter 14, 16
- **使用例**: 「PaymentValidatorはpayment-authorizationケイパビリティを実現するBCである」

## C

### Capability（ケイパビリティ）
- **定義**: 組織が価値を提供するために必要な能力や機能
- **関連章**: Chapter 13, 14, 15
- **日本語**: ケイパビリティ、能力
- **使用例**: 「payment-authorizationケイパビリティは決済承認を行う能力」

### Context Map（コンテキストマップ）
- **定義**: 複数の境界づけられたコンテキスト間の関係を表す図
- **関連章**: Chapter 18
- **パターン**: Customer-Supplier、Partnership、Shared Kernel、Conformist、Anti-corruption Layer

### CQRS (Command Query Responsibility Segregation)
- **定義**: コマンド（更新）とクエリ（参照）の責任を分離するパターン
- **関連章**: Chapter 22
- **使用例**: 「書き込みモデルと読み込みモデルを分離してパフォーマンスを最適化」

## D

### Design Matrix（設計マトリクス）
- **定義**: Axiomatic Designにおける機能要求(FR)と設計パラメータ(DP)の関係を表す行列
- **関連章**: Chapter 4, 13, 14, 15, 16
- **種類**: 非結合(Uncoupled)、準結合(Decoupled)、結合(Coupled)

### Design Parameter (DP)
- **定義**: 機能要求を満たすための具体的な設計解
- **関連章**: Chapter 4, 13
- **日本語**: 設計パラメータ
- **使用例**: 「FR1:迅速な決済に対してDP1:バッチ処理を割り当てる」

### Domain-Driven Design (DDD)
- **定義**: Eric Evansによるドメイン中心のソフトウェア設計アプローチ
- **関連章**: Chapter 5, 20, 21
- **統合**: Parasol Phase 5で主に活用

## E

### Event Sourcing（イベントソーシング）
- **定義**: 状態変更をイベントの連続として保存するパターン
- **関連章**: Chapter 22
- **使用例**: 「注文の全履歴をイベントとして保存し、任意の時点の状態を再現可能」

## F

### Functional Requirement (FR)
- **定義**: システムが満たすべき機能的な要求
- **関連章**: Chapter 4, 13
- **日本語**: 機能要求
- **使用例**: 「FR1:2秒以内に決済を完了する」

## I

### Independence Axiom（独立性の公理）
- **定義**: Axiomatic Designの第1公理。機能要求の独立性を維持すべき
- **関連章**: Chapter 3, 4
- **実現方法**: Design Matrixの対角化

### Information Axiom（情報の公理）
- **定義**: Axiomatic Designの第2公理。設計情報量を最小化すべき
- **関連章**: Chapter 3, 4
- **意味**: シンプルで成功確率の高い設計

## O

### Organization Space（組織空間）
- **定義**: Parasolの3つの空間の1つ。組織の文化、構造、プロセスを扱う
- **関連章**: Chapter 2, 6, 7, 8
- **フェーズ**: Phase 0-1

## P

### Parasol V5.4
- **定義**: 価値駆動型のエンタープライズアーキテクチャ方法論の最新版
- **関連章**: Chapter 1, 5
- **特徴**: Axiomatic DesignとDDDの統合、7つのフェーズ

### Phase 0-7
- **定義**: Parasolの7つの実行フェーズ
- **詳細**:
  - Phase 0: 組織アセスメント
  - Phase 1: 組織コンテキスト
  - Phase 2: 価値ストリーム
  - Phase 3: ケイパビリティ（ZIGZAG）
  - Phase 4: アーキテクチャ
  - Phase 5: ソフトウェア設計
  - Phase 6: 実装
  - Phase 7: プラットフォーム

### POMM (Parasol Organization Maturity Model)
- **定義**: 組織のデジタル成熟度を5段階で評価するモデル
- **関連章**: Chapter 6
- **レベル**: Initial、Managed、Defined、Quantitatively Managed、Optimizing

### Problem Space（問題空間）
- **定義**: 何を解決すべきか（WHAT）を定義する空間
- **関連章**: Chapter 2, 13-16
- **フェーズ**: Phase 2-3

## S

### Solution Space（解決空間）
- **定義**: どのように解決するか（HOW）を定義する空間
- **関連章**: Chapter 2, 17-31
- **フェーズ**: Phase 4-7

## U

### Ubiquitous Language（ユビキタス言語）
- **定義**: ビジネスと開発で共通に使用される統一された語彙
- **関連章**: Chapter 20
- **使用例**: 「'配送'という言葉は全チームで同じ意味を持つ」

## V

### Value Stream（価値ストリーム）
- **定義**: 顧客に価値を提供するために必要な一連の活動
- **関連章**: Chapter 9, 10, 11, 12
- **記法**: VS-001, VS-002など

### Value Stream Mapping (VSM)
- **定義**: 価値の流れを可視化し、ムダを特定する手法
- **関連章**: Chapter 9
- **要素**: 付加価値活動、非付加価値活動、待機時間

## Z

### ZIGZAG Process（ジグザグプロセス）
- **定義**: 問題空間と解決空間を往復しながら設計を洗練する反復プロセス
- **関連章**: Chapter 13
- **フェーズ**: 探索(Exploration)、洗練(Refinement)、収束(Convergence)
- **表記**: 常に大文字で"ZIGZAG"

## 略語一覧

| 略語 | 完全形 | 日本語 |
|------|--------|--------|
| AD | Axiomatic Design | 公理的設計 |
| BC | Business Component | ビジネスコンポーネント |
| CA | Customer Attribute | 顧客属性 |
| CL1 | Capability Level 1 (Activity Area) | アクティビティエリア |
| CL2 | Capability Level 2 (Capability) | ケイパビリティ |
| CL3 | Capability Level 3 (Business Operation) | ビジネスオペレーション |
| DDD | Domain-Driven Design | ドメイン駆動設計 |
| DP | Design Parameter | 設計パラメータ |
| FR | Functional Requirement | 機能要求 |
| POMM | Parasol Organization Maturity Model | Parasol組織成熟度モデル |
| PV | Process Variable | プロセス変数 |
| VSM | Value Stream Mapping | 価値ストリームマッピング |

## 使用上の注意

1. **一貫性**: 書籍全体で同じ用語を使用
2. **初出時**: 初めて使用する際は定義を併記
3. **略語**: 初出時は完全形を示す
4. **日英併記**: 重要な概念は両言語で理解

---

最終更新：2025-12-29
参照：全38章で使用される用語を網羅