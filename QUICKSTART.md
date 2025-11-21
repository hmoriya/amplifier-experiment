# クイックスタートガイド - Amplifier + パラソル統合プロジェクト

## 🎯 新しいプロジェクト構成の概要

Amplifierとパラソル開発フレームワークを統合した、実プロジェクトに即座に適用可能な構成です。

```
.
├── 📋 parasol/          # パラソル開発フレームワーク（コア）
├── 🚀 projects/         # 実際のプロジェクト
├── 🔧 amplifier/        # Amplifier AI支援機能
├── 📚 templates/        # プロジェクトテンプレート
├── 🛠️ tools/           # 開発ツール（CLI等）
├── ⚙️ config/          # グローバル設定
└── 📖 docs/            # ドキュメント
```

## 🚀 クイックスタート（3ステップ）

### Step 1: 新規プロジェクト作成

```bash
# パラソルCLIで新規プロジェクト作成
./tools/cli/parasol init my-awesome-project

# または手動で作成
mkdir -p projects/my-awesome-project
cd projects/my-awesome-project
```

### Step 2: DDDワークフロー開始

```bash
# プロジェクトディレクトリに移動
cd projects/my-awesome-project

# DDDワークフローを開始
# Phase 1: 計画
/ddd:1-plan "オンラインショッピングカートシステムの実装"

# Phase 2: ドキュメント
/ddd:2-docs

# Phase 3: コード計画
/ddd:3-code-plan

# Phase 4: 実装
/ddd:4-code

# Phase 5: 完了
/ddd:5-finish
```

### Step 3: パラソルパターン適用

```bash
# ドメインエンティティ生成
./tools/cli/parasol generate entity Product

# ユースケース生成
./tools/cli/parasol generate use-case AddToCart

# API生成
./tools/cli/parasol generate api cart
```

## 📊 プロジェクト構成例

### 実プロジェクトの標準構成

```
projects/my-awesome-project/
├── .ddd/                    # DDDワークフロー成果物
│   ├── plan.md             # 計画書
│   ├── docs_status.md      # ドキュメント状態
│   └── code_plan.md        # コード計画
│
├── parasol/                 # パラソル設定
│   ├── capabilities/       # 能力定義（L1→L2→L3）
│   └── operations/         # オペレーション定義
│
├── src/                    # ソースコード（Clean Architecture）
│   ├── domain/            # ドメイン層
│   ├── application/       # アプリケーション層
│   ├── infrastructure/    # インフラ層
│   └── presentation/      # プレゼンテーション層
│
├── tests/                  # テスト
└── docs/                   # ドキュメント
```

## 🎯 実際の使用例

### 例1: ECサイト開発

```bash
# プロジェクト作成
./tools/cli/parasol init ec-site --template=microservices

cd projects/ec-site

# DDDワークフローで設計
/ddd:1-plan "ECサイトのバックエンドAPI実装"

# パラソルフェーズ実行
# Phase 1: 価値分析
echo "売上向上30%、顧客満足度4.5以上" > parasol/value-proposition.md

# Phase 2: 能力設計
cat > parasol/capabilities/L1-strategic.yaml << EOF
capabilities:
  - id: L1-001
    name: "E-commerce Success"
    value: "オンライン売上の最大化"
EOF

# 実装生成
./tools/cli/parasol generate all
```

### 例2: タスク管理システム

```bash
# テンプレートから作成
./tools/cli/parasol init task-manager --template=clean-architecture

cd projects/task-manager

# DDDワークフロー実行（すべてのフェーズ）
/ddd:1-plan "タスク管理システムの実装"
/ddd:2-docs
/ddd:3-code-plan
/ddd:4-code
/ddd:5-finish
```

## 🔧 便利なコマンド

### プロジェクト管理

```bash
# プロジェクト一覧
ls -la projects/

# プロジェクト分析
./tools/cli/parasol analyze --project=my-awesome-project

# メトリクス確認
./tools/cli/parasol metrics --project=my-awesome-project
```

### コード生成

```bash
# エンティティ生成
./tools/cli/parasol generate entity User

# ユースケース生成
./tools/cli/parasol generate use-case RegisterUser

# 完全な CRUD 生成
./tools/cli/parasol generate crud User
```

### パターン適用

```bash
# 利用可能なパターン確認
ls parasol/patterns/

# パターン適用
./tools/cli/parasol apply-pattern aggregate-root Task

# パターン使用状況
./tools/cli/parasol patterns --usage
```

## 📈 メトリクスとレポート

### ダッシュボード確認

```bash
# プロジェクトメトリクス
cat projects/my-awesome-project/.ddd/metrics.json

# パラソル能力達成度
./tools/cli/parasol report capabilities

# 価値実現度
./tools/cli/parasol report value-metrics
```

## 🎓 学習リソース

### ドキュメント
- [Getting Started](docs/getting-started.md)
- [Parasol Guide](docs/parasol-guide.md)
- [Amplifier Integration](docs/amplifier-integration.md)

### サンプルプロジェクト
- `projects/consulting-dashboard/` - コンサルティングダッシュボード
- `examples/simple-crud/` - シンプルなCRUD
- `examples/enterprise-system/` - エンタープライズシステム

## ⚡ Tips & Tricks

### 1. 高速プロトタイピング

```bash
# テンプレートから即座に開始
./tools/cli/parasol init prototype --template=parasol-standard --fast
```

### 2. CI/CD統合

```yaml
# .github/workflows/parasol.yml
name: Parasol CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: ./tools/cli/parasol analyze
      - run: ./tools/cli/parasol test
```

### 3. VS Code統合

```json
// .vscode/settings.json
{
  "parasol.autoComplete": true,
  "parasol.validateOnSave": true,
  "parasol.ddd.enabled": true
}
```

## 🚨 トラブルシューティング

### DDDワークフローが動かない場合

```bash
# DDDステータス確認
ls -la ai_working/ddd/

# リセット
rm -rf ai_working/ddd/
/ddd:1-plan "新しい計画"
```

### パラソルCLIエラー

```bash
# 権限確認
chmod +x ./tools/cli/parasol

# パス確認
which parasol || echo "パスに追加: export PATH=$PATH:$(pwd)/tools/cli"
```

## 🎉 まとめ

この新しい構成により：

1. **即座に実プロジェクトで使用可能**
2. **Amplifier DDDワークフローと完全統合**
3. **パラソル6フェーズの体系的実行**
4. **ナレッジとパターンの自動蓄積**
5. **CI/CD対応の標準構成**

さあ、実プロジェクトを始めましょう！

```bash
# 今すぐ開始
./tools/cli/parasol init my-next-project
cd projects/my-next-project
/ddd:1-plan "素晴らしいプロジェクトの開始"
```

---

*Happy coding with Amplifier + Parasol! 🌂✨*