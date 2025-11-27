# ケーパビリティ分解ナレッジベース

**Parasol V5 - 分解パターンと学習の蓄積**

---

## 目的

このナレッジベースは、ケーパビリティ分解（Phase 3）で得られた知見を蓄積し、将来のプロジェクトで活用するためのものです。

Amplifierの「継続的学習」の思想に基づき：
- **パターン**: 繰り返し適用可能な分解パターン
- **事例**: 実プロジェクトからの学習
- **アンチパターン**: 避けるべき設計判断

を体系的に記録します。

---

## ディレクトリ構成

```
_capability-knowledge/
├── README.md                    # 本ファイル（概要）
├── patterns/                    # パターン集
│   ├── naming-patterns.md       # 命名パターン
│   ├── decomposition-patterns.md # 分解パターン
│   └── anti-patterns.md         # アンチパターン
├── examples/                    # 事例集（プロジェクト別）
│   └── {project-name}.md        # 各プロジェクトからの学び
└── registry.yaml                # ケーパビリティ登録簿（一意性管理）
```

---

## 使い方

### パターンの参照

```bash
# 命名パターンを確認
cat .claude/commands/parasol/_capability-knowledge/patterns/naming-patterns.md

# 分解パターンを確認
cat .claude/commands/parasol/_capability-knowledge/patterns/decomposition-patterns.md
```

### 事例の追加

新しいプロジェクトでケーパビリティ分解を完了したら：

1. `examples/{project-name}.md` に学びを記録
2. 新しいパターンがあれば `patterns/` に追加
3. `registry.yaml` にケーパビリティを登録

### 一意性チェック

```bash
# registry.yaml を参照してVS横断での一意性を確認
grep "capability-name" .claude/commands/parasol/_capability-knowledge/registry.yaml
```

---

## ナレッジ蓄積のルール

### 1. パターン追加の基準

以下の場合に新しいパターンを追加：

- **3回以上**同様の分解判断を行った場合
- **業界特有**の分解パターンを発見した場合
- **アンチパターン**に気づいた場合

### 2. 事例記録の基準

各プロジェクト完了時に必ず記録：

- 採用した分解戦略とその理由
- 命名で工夫した点
- 次回に活かしたい学び
- 失敗・反省点

### 3. 登録簿（registry.yaml）の更新

CL2/CL3完了時に必ず更新：

- 新規ケーパビリティの登録
- VS横断での一意性確認
- 類似命名の関係性記録

---

## AI（Claude）への指示

ケーパビリティ分解時に以下を実行：

1. **開始時**: `registry.yaml` を読み込み、既存ケーパビリティを把握
2. **命名時**: `patterns/naming-patterns.md` を参照
3. **分解時**: `patterns/decomposition-patterns.md` を参照
4. **完了時**: `registry.yaml` に新規ケーパビリティを追加
5. **学習時**: `examples/{project-name}.md` に学びを記録

---

## 関連ドキュメント

- [命名ガイドライン](../_capability-naming-guide.md)
- [Phase 3コマンド](../3-capabilities.md)
- [検証コマンド](../0-validate.md)

---

**作成日:** 2025-11-27
**更新履歴:** 初版作成
