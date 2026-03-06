---
description: Project status display (parasol5:utils)
---

# Parasol V5 - ステータス確認

プロジェクトの進捗状況と成果物の完成度を確認します。

## 使用方法

```bash
/parasol5:utils:status              # 全フェーズの進捗確認
/parasol5:utils:status phase1       # Phase 1の詳細確認
/parasol5:utils:status phase2       # Phase 2の詳細確認
/parasol5:utils:status phase3       # Phase 3の詳細確認
/parasol5:utils:status capabilities # Phase 3の別名
/parasol5:utils:status vs           # Value Streams状況
/parasol5:utils:status services     # サービス/BC状況
```



## 🔧 プロジェクト検出

**重要**: このコマンドはParasolプロジェクト内で実行する必要があります。

### 自動検出

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：

1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)
3. **祖父ディレクトリ** (`../..`)

### 検出成功

```
✅ プロジェクト検出: {project-name}

プロジェクトディレクトリ: projects/{project-name}/
出力先: projects/{project-name}/outputs/
```

プロジェクト設定を読み込み、Phase進捗を自動記録します。

### 検出失敗

```
❌ Parasolプロジェクトが見つかりません

📋 次のアクションを選択してください:

1. 新しいプロジェクトを作成
   → /parasol5:utils:project init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol5:utils:project list
```

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/value5:context

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/value5:context  # ❌
```

詳細は `.claude/commands/parasol/_project-detection.md` を参照。

## 実行

パラメータに応じて `outputs/` ディレクトリ構造をチェックし、適切なステータスレポートを生成します。

### パラメータなしの場合（全体ステータス）

```
📊 Parasol V5 - プロジェクトステータス

プロジェクト: {プロジェクト名}
最終更新: {日時}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: Context ✅ 完了
  ✅ 組織分析
  ✅ 市場評価
  ✅ 制約事項
  ✅ ステークホルダーマップ

Phase 2: Value Definition ✅ 完了
  ✅ 価値定義
  ✅ バリューストリームマッピング (VS0-VS7)
  ✅ エンタープライズ活動

Phase 3: Capabilities 🔄 進行中
  ✅ 3a. Activity Area Identification (CL1) - 傾向的分類
  ✅ 3b. Capability Design (CL2) - 正式分類 3/3 完了
  ⏸️ 3c. Operation Definition (CL3) - 2/8 ケイパビリティ完了

Phase 4: Application Design ⏸️ 未着手
Phase 5: Software Design ⏸️ 未着手
Phase 6: Implementation ⏸️ 未着手
Phase 7: Platform ⏸️ 未着手

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 全体進捗: 35% (3/7 フェーズ完了)

🎯 次のアクション:
1. Phase 3c の残り6サブドメインのCL3定義
   `/parasol5:capability:decompose cl3 {subdomain-name}`

2. Phase 4 アプリケーションデザイン開始
   `/parasol5:architecture:application-design`

💡 ヒント:
- 詳細確認: `/parasol5:utils:status phase3`
- 一貫性検証: `/parasol5:utils:validate`
```

**確認項目**:
1. Phase 1: Context (outputs/1-context/)
2. Phase 2: Value Definition (outputs/2-value/)
3. Phase 3: Capabilities (outputs/3-capabilities/{vs}/)
   - 3a: cl1-activity-identification.md（傾向的分類）
   - 3b: cl2-subdomain-design.md（ケイパビリティ設計）
   - 3c: cl3-business-operations/{capability}-operations.md
4. Phase 4: Application Design (outputs/4-architecture/)
5. Phase 5: Software (outputs/5-software/services/)
6. Phase 6: Implementation (outputs/6-implementation/)
7. Phase 7: Platform (outputs/7-platform/)

### phase1 指定時

Phase 1の詳細ステータスを表示：

```
📊 Phase 1: Context - 詳細ステータス

成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ organization-analysis.md
   作成日: 2025-01-15
   サイズ: 15.2 KB
   セクション: 組織概要、事業構造、グループガバナンス、戦略方向性

✅ market-assessment.md
   作成日: 2025-01-15
   サイズ: 12.8 KB
   セクション: 市場環境、競合分析、顧客セグメント

✅ constraints.md
   作成日: 2025-01-15
   サイズ: 8.5 KB
   セクション: 技術制約、組織制約、規制制約、時間制約

✅ stakeholder-map.md
   作成日: 2025-01-15
   サイズ: 10.2 KB
   セクション: ステークホルダー識別、影響マップ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ステータス: ✅ 完了
品質: 🟢 優良（全ドキュメント揃い）

次のステップ: Phase 2 Value Definition
→ `/value5:definition`
```

### phase3 または capabilities 指定時

Phase 3の段階的進捗を表示：

```
📊 Phase 3: Capabilities - 詳細ステータス

3a. Activity Area Identification (CL1) - 傾向的分類
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ activity-area-classification.md
   Core傾向: 3 活動領域
   Supporting傾向: 4 活動領域
   Generic傾向: 2 活動領域

3b. Capability Design (CL2) - 正式分類
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ core-capabilities.md (3 ケイパビリティ)
✅ supporting-capabilities.md (5 ケイパビリティ)
⏸️ generic-capabilities.md (未着手)

合計: 8 ケイパビリティ定義済み

3c. Sub-capability Definition (CL3) - 詳細能力+BO対応
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ product-catalog-operations.md (Core)
✅ order-management-operations.md (Core)
⏸️ inventory-management-bc.md (待機中)
⏸️ payment-processing-bc.md (待機中)
⏸️ customer-service-bc.md (待機中)
⏸️ analytics-bc.md (待機中)
⏸️ notification-bc.md (待機中)
⏸️ authentication-bc.md (待機中)

完了: 2/8 BC (25%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ステータス: 🔄 進行中
品質: 🟡 要継続（BC定義を完了させる必要あり）

次のアクション:
1. 残りBCの定義: `/parasol5:capability:decompose cl3 {subdomain-name}`
2. 全BC完了後: `/parasol5:architecture:application-design`

推奨順序:
  優先: inventory-management, payment-processing (Core周辺)
  次: customer-service, analytics (Supporting)
  最後: notification, authentication (Generic)
```

### vs 指定時

Value Streams別の進捗を表示：

```
📊 Value Streams - ステータス

VS0: ビジョン策定
  ステータス: ✅ 定義完了
  サブドメイン: 2 (strategic-planning, stakeholder-engagement)
  BC: 2 (両方定義済み)

VS1: 市場機会発見
  ステータス: ✅ 定義完了
  サブドメイン: 1 (market-analysis)
  BC: 1 (定義済み)

VS2: 製品開発
  ステータス: ✅ 定義完了
  サブドメイン: 3 (product-catalog, inventory, pricing)
  BC: 2/3 完了 (pricing待機中)

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

サマリー:
- 定義済みVS: 8/8 (100%)
- 紐付きサブドメイン: 8
- BC定義率: 2/8 (25%)

アクション: BCの残りを完了
→ `/parasol5:capability:decompose cl3`
```

### services 指定時

Phase 5のサービス/BC設計状況を表示：

```
📊 Services/Bounded Contexts - ステータス

Phase 5: Software Design の進捗

outputs/5-software/services/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏸️ ProductCatalog/ (サービス未着手)
  ⏸️ Core/ (BC)
  ⏸️ Inventory/ (BC)
  ⏸️ Pricing/ (BC)

⏸️ OrderManagement/ (サービス未着手)
  ⏸️ Orders/ (BC)
  ⏸️ Fulfillment/ (BC)

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ステータス: ⏸️ 未着手
前提条件: Phase 4 Application Design が完了している必要があります

次のステップ:
1. Phase 4を完了: `/parasol5:architecture:application-design`
2. サービス設計開始: `/parasol5:architecture:software-design {service} {bc}`
```

## エラーケース

**outputs/ ディレクトリが存在しない:**
```
⚠️ Parasolプロジェクトが初期化されていません

最初に Context を確立してください:
→ `/value5:context`
```

**無効なフェーズ指定:**
```
❌ 無効なフェーズ: phase9

有効なオプション:
- phase1, phase2, phase3, phase4, phase5, phase6, phase7
- capabilities (phase3の別名)
- vs (Value Streams状況)
- services (サービス/BC状況)
- パラメータなし (全体ステータス)
```

## バリデーション連携

ステータス確認後、一貫性の問題が検出された場合：

```
⚠️ 一貫性の問題を検出しました

詳細確認: `/parasol5:utils:validate`
```
