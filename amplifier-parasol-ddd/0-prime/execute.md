# /ddd:prime - プロジェクトコンテキスト設定

## 概要

このフェーズでは、プロジェクト全体のコンテキストを設定し、価値駆動開発の基盤を確立します。

## 実行コマンド

```bash
/ddd:prime
```

## 実行コンテキスト

### 前提条件
- プロジェクトの目的が明確であること
- ステークホルダーが特定されていること
- ビジネスゴールが定義されていること

### 入力
- ビジネスビジョン
- 市場環境分析
- 既存システムの評価

### 出力
- 価値コンテキスト定義
- ドメインコンテキスト定義
- プロジェクト設定ファイル

---

## タスク

### Task 1: 価値視座の選択

```yaml
価値視座の評価:
  顧客視座:
    重要度: 高
    理由: エンドユーザー体験の向上が最優先

  企業視座:
    重要度: 中
    理由: 収益性と効率性の改善

  社会視座:
    重要度: 高
    理由: サステナビリティへの貢献

選択された主要視座: 顧客・社会
```

### Task 2: 価値宣言の定義

```yaml
価値宣言:
  北極星: "持続可能な価値創造を通じて、顧客と社会に貢献する"

  測定指標:
    - 顧客満足度スコア（NPS）
    - サステナビリティインデックス
    - 事業成長率
```

### Task 3: ドメインコンテキストの確立

```yaml
ドメイン識別:
  コアドメイン:
    - 価値創造
    - 顧客体験

  サポーティングドメイン:
    - オペレーション
    - データ管理

  ジェネリックドメイン:
    - 認証・認可
    - 通知
```

### Task 4: パラソルドメイン言語の初期化

```yaml
基本用語定義:
  - 顧客 [Customer] [CUSTOMER]
  - 価値 [Value] [VALUE]
  - サービス [Service] [SERVICE]
  - 製品 [Product] [PRODUCT]
  - 注文 [Order] [ORDER]
```

### Task 5: プロジェクト設定

```yaml
project:
  name: "価値駆動型システム開発"
  version: "1.0.0"
  framework: "amplifier-parasol-ddd"

  team:
    - role: Product Owner
    - role: Architect
    - role: Developer
    - role: Designer

  timeline:
    phase1: 2週間
    phase2: 3週間
    phase3: 2週間
    phase4: 3週間
    phase5: 4週間
    phase6: 2週間
```

---

## 検証チェックリスト

- [ ] 価値宣言が明確で測定可能か
- [ ] ドメインコンテキストが適切に分類されているか
- [ ] パラソルドメイン言語が統一されているか
- [ ] プロジェクト設定が完全か
- [ ] ステークホルダーの合意が得られているか

---

## 次のステップ

価値コンテキストが確立されたので、次は価値とビジネスの詳細計画に進みます：

```bash
/ddd:1-plan 1-plan/execute.md
```

---

## 成果物の保存先

```
amplifier-parasol-ddd/
└── 0-prime/
    ├── outputs/
    │   ├── value-context.yaml
    │   ├── domain-context.yaml
    │   └── project-config.yaml
    └── decisions/
        └── VDR-001-value-perspective.md
```

---

*このドキュメントはAmplifierのDDDワークフローで直接実行できます*