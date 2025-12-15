# parasol:milestone - 価値マイルストーン管理コマンド

## 概要

Parasol V5の価値マイルストーン（VMS1-VMS5）を管理します。**VMSは「顧客が得ている価値状態」として定義**され、プロセス完了ではなく価値実現の段階を表します。VL（価値分解）からバックキャストで導出し、VS（バリューストリーム）へマッピングすることで、価値の所在と優先順位を明確にします。

## マイルストーン定義（価値実現型）

**重要**: VMSは「組織が何を完了したか」ではなく「顧客が何を得ているか」で定義します。

### VMS1: 顧客が最初の価値を体験できる状態（3ヶ月後）
- **顧客状態**: 顧客が最初の価値を体験できる状態
- **実現VL**: VL3の一部（最小実現）
- **成功基準**: 顧客が価値の存在を認識し、初回体験が可能

### VMS2: 顧客が価値を認識し選択できる状態（6ヶ月後）
- **顧客状態**: 顧客が価値を認識し選択できる状態
- **実現VL**: VL3の主要部分、VL2の一部
- **成功基準**: 顧客が継続利用の意思決定が可能

### VMS3: 顧客が主要価値を日常的に体験できる状態（9ヶ月後）
- **顧客状態**: 顧客が主要製品で価値を体験できる状態
- **実現VL**: VL2の主要部分
- **成功基準**: 顧客満足度の向上、継続利用の定着

### VMS4: 顧客が全面的に価値を実感している状態（12ヶ月後）
- **顧客状態**: 顧客が全製品ラインで価値を実感している状態
- **実現VL**: VL2完全、VL1の主要部分
- **成功基準**: 顧客ロイヤルティの確立、推奨行動の開始

### VMS5: 顧客が期待を超える価値を日常的に享受している状態（18ヶ月後）
- **顧客状態**: 顧客が期待を超える価値を日常的に享受している状態
- **実現VL**: VL1完全実現
- **成功基準**: 顧客の生活に価値が統合、共創関係の確立

## 価値マイルストーンの原則

### 1. バックキャスト導出
```
VMS5（理想状態）から逆算してVMS1を導出
VMS5 ← VMS4 ← VMS3 ← VMS2 ← VMS1
「VMS5に到達するにはVMS4で何が必要か？」の問いで各VMSを定義
```

### 2. 顧客視点の徹底
```
❌ 誤: 「システム開発完了」「機能リリース済」
✅ 正: 「顧客が24時間注文できる状態」「顧客が即座に回答を得られる状態」
```

### 3. VL分解との連携
```
VL1 → VL2 → VL3 （価値分解）
         ↓
VMS5 ← ... ← VMS1 （バックキャスト）
         ↓
VS0 → ... → VS7 （バリューストリーム）
         ↓
    VL×VSマッピング
```

## コマンド構文

```bash
amplifier parasol:milestone <サブコマンド> [オプション]
```

## サブコマンド

### status - 現在の状況確認

プロジェクトの現在のマイルストーン状況を表示します。

```bash
amplifier parasol:milestone status [--detailed] [--format <format>]
```

**出力例:**
```
プロジェクト: asahi-digital-transform
現在のマイルストーン: VMS2 (進行中)

マイルストーン進捗:
VMS1 [████████████████████] 100% ✓ 完了
VMS2 [████████████--------]  60% ⚡ 進行中
VMS3 [--------------------]   0% ⏸ 待機中
VMS4 [--------------------]   0% ⏸ 待機中
VMS5 [--------------------]   0% ⏸ 待機中

VMS2の残タスク:
- [ ] ケイパビリティマッピング (VS3, VS4)
- [ ] 優先順位マトリックスの作成
- [ ] ステークホルダーレビュー

次のアクション:
amplifier parasol:milestone advance --continue
```

### advance - マイルストーンの進行

次のマイルストーンへ進行、または現在のマイルストーンを完了させます。

```bash
amplifier parasol:milestone advance [--to <milestone>] [--force] [--validate]
```

**オプション:**
- `--to <milestone>`: 特定のマイルストーンへジャンプ（VMS1-VMS5）
- `--force`: 検証をスキップして強制進行
- `--validate`: 進行前に包括的な検証を実施
- `--continue`: 現在のマイルストーンの作業を継続

**使用例:**
```bash
# 次のマイルストーンへ進行
amplifier parasol:milestone advance

# VMS3へ直接移行（VMS2完了が前提）
amplifier parasol:milestone advance --to VMS3 --validate

# 現在のマイルストーンを継続
amplifier parasol:milestone advance --continue
```

### rollback - マイルストーンの巻き戻し

問題が発生した場合に前のマイルストーンへ戻ります。

```bash
amplifier parasol:milestone rollback [--to <milestone>] [--preserve-work]
```

**オプション:**
- `--to <milestone>`: 特定のマイルストーンへ巻き戻し
- `--preserve-work`: 作業内容を保持したまま巻き戻し
- `--reason <text>`: 巻き戻しの理由を記録

**使用例:**
```bash
# 前のマイルストーンへ戻る
amplifier parasol:milestone rollback --reason "価値定義の見直しが必要"

# 作業を保持してVMS1へ戻る
amplifier parasol:milestone rollback --to VMS1 --preserve-work
```

### checkpoint - チェックポイント作成

現在の状態を保存し、後で復元できるようにします。

```bash
amplifier parasol:milestone checkpoint [--name <name>] [--description <desc>]
```

**使用例:**
```bash
# 名前付きチェックポイント作成
amplifier parasol:milestone checkpoint --name "before-major-refactor"

# 自動チェックポイント（タイムスタンプ付き）
amplifier parasol:milestone checkpoint
```

### validate - マイルストーン検証

現在のマイルストーンの成果物と品質を検証します。

```bash
amplifier parasol:milestone validate [--milestone <ms>] [--fix] [--report]
```

**検証内容:**

**VMS1検証:**
- 価値が明確に定義されているか
- ステークホルダーが特定されているか
- 価値の測定基準があるか

**VMS2検証:**
- すべての価値がケイパビリティに分解されているか
- 優先順位が明確か
- 依存関係が解決されているか

**VMS3検証:**
- ドメインモデルの一貫性
- バウンデッドコンテキストの境界明確性
- 技術選択の必然性

**出力例:**
```
VMS2 検証結果:

✓ 価値ストリーム定義: 完了 (8/8)
✓ ケイパビリティ分解: 完了 (24/24)
⚠ 優先順位付け: 不完全 (18/24)
✗ 依存関係解決: 未完了 (循環依存を検出)

総合評価: 75% (要改善)

修正提案:
1. 以下のケイパビリティの優先順位を設定:
   - inventory-management
   - customer-analytics
   
2. 循環依存の解決:
   order-service ←→ payment-service
   
自動修正: amplifier parasol:milestone validate --fix
```

### dependencies - 依存関係の確認

マイルストーン間の依存関係と前提条件を表示します。

```bash
amplifier parasol:milestone dependencies [--from <ms>] [--to <ms>] [--visualize]
```

**出力例:**
```mermaid
graph LR
    VMS1[価値発見] --> VMS2[価値設計]
    VMS2 --> VMS3[構造設計]
    VMS3 --> VMS4[実装設計]
    VMS4 --> VMS5[価値実現]

    VMS1 -.->|価値定義| VMS3
    VMS2 -.->|ケイパビリティ| VMS4
    VMS3 -.->|ドメインモデル| VMS5
```

### timeline - タイムライン表示

プロジェクトのマイルストーン進行履歴を表示します。

```bash
amplifier parasol:milestone timeline [--days <n>] [--format <format>]
```

**出力例:**
```
プロジェクトタイムライン:

2024-01-01 09:00 │ VMS1 開始
2024-01-02 14:30 │ ├─ 価値抽出完了
2024-01-03 11:00 │ ├─ ステークホルダー分析完了
2024-01-04 16:00 │ └─ VMS1 完了 ✓
2024-01-04 16:15 │ VMS2 開始
2024-01-08 10:00 │ ├─ 価値ストリーム設計完了
2024-01-10 15:30 │ ├─ ケイパビリティ分解 (進行中)
                 │
現在 ············→ ⚡
```

## 品質ゲート統合

### 価値実現型品質チェック

各マイルストーンの品質ゲートは**顧客価値の実現度**で判定します：

```yaml
quality_gates:
  VMS1:
    - 顧客が最小限の価値を体験できるか
    - 価値の測定基準が定義されているか
    - 顧客フィードバックの収集体制があるか

  VMS2:
    - 顧客が価値を選択・比較できるか
    - 継続利用の障壁が除去されているか
    - 顧客満足度が目標値を達成しているか

  VMS3:
    - 顧客が主要価値を日常的に利用しているか
    - 顧客の課題が解決されているか
    - NPS/顧客満足度が基準を満たすか

  VMS4:
    - 顧客が全製品ラインで価値を実感しているか
    - 顧客ロイヤルティ指標が目標を達成しているか
    - 推奨行動（口コミ等）が発生しているか

  VMS5:
    - 顧客の生活に価値が統合されているか
    - 顧客との共創関係が確立されているか
    - 長期的な価値提供基盤が整備されているか
```

### カスタム品質ルール

```yaml
# .parasol/milestone-rules.yaml
custom_gates:
  VMS2:
    - id: capability-size
      rule: "各ケイパビリティは3-7の機能を含む"
      severity: warning

    - id: value-trace
      rule: "すべてのケイパビリティが価値にトレース可能"
      severity: error
```

## 自動化機能

### マイルストーン自動進行

```bash
# 条件を満たしたら自動的に次へ
amplifier parasol:milestone auto-advance --enable

# 進行条件の設定
amplifier parasol:milestone set-conditions --file conditions.yaml
```

### 進捗レポート自動生成

```bash
# 日次進捗レポート
amplifier parasol:milestone report --schedule daily

# マイルストーン完了時の成果物レポート
amplifier parasol:milestone report --on-complete
```

## CI/CD統合

### GitHub Actions

```yaml
- name: Milestone Validation
  run: |
    amplifier parasol:milestone validate
    amplifier parasol:milestone advance --validate
```

### 自動通知

```bash
# Slack通知設定
amplifier parasol:milestone notify --slack-webhook $SLACK_WEBHOOK

# メール通知
amplifier parasol:milestone notify --email team@example.com
```

## トラブルシューティング

### マイルストーンがブロックされた場合

```bash
# ブロック理由の詳細表示
amplifier parasol:milestone diagnose

# 強制進行（管理者権限）
amplifier parasol:milestone advance --force --admin

# 部分的な進行
amplifier parasol:milestone advance --partial
```

### データ不整合の修復

```bash
# 整合性チェック
amplifier parasol:milestone integrity-check

# 自動修復
amplifier parasol:milestone repair --auto

# 手動修復ガイド
amplifier parasol:milestone repair --guide
```

## ベストプラクティス

### 1. 段階的進行

```bash
# 各マイルストーンを確実に完了
amplifier parasol:milestone validate --strict
amplifier parasol:milestone advance

# スキップは避ける
# ✗ amplifier parasol:milestone advance --to VMS5 --force
```

### 2. 定期的なチェックポイント

```bash
# 重要な決定前後でチェックポイント作成
amplifier parasol:milestone checkpoint --name "before-architecture-decision"

# 週次でのチェックポイント
amplifier parasol:milestone checkpoint --schedule weekly
```

### 3. チームコラボレーション

```bash
# 進捗の共有
amplifier parasol:milestone share --format pdf

# レビュー会の準備
amplifier parasol:milestone prepare-review --milestone VMS3
```

## 次のステップ

現在のマイルストーンを完了したら：

```bash
# 品質ゲートの実行
amplifier parasol:quality-gate check

# 次のマイルストーンへ
amplifier parasol:milestone advance
```