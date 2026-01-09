---
description: Validate project consistency (project:parasol)
---

# Parasol V5 - バリデーション

プロジェクト全体の一貫性と完全性を検証します。

## 使用方法

```bash
/parasol:validate              # 全体検証
/parasol:validate phase1       # Phase 1のみ検証
/parasol:validate phase2       # Phase 2のみ検証
/parasol:validate phase3       # Phase 3のみ検証
/parasol:validate capabilities # Phase 3の別名
/parasol:validate vs           # Value Streams一貫性
/parasol:validate architecture # Phase 4検証
/parasol:validate platform     # Phase 7検証
/parasol:validate full         # 完全検証（全フェーズ）
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
   → /parasol:project init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol:project list
```

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/parasol:1-context

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/parasol:1-context  # ❌
```

詳細は `.claude/commands/parasol/_project-detection.md` を参照。

## 検証項目

### パラメータなしの場合（標準検証）

以下の検証を実行し、レポートを生成：

**1. フェーズ完全性チェック**
```markdown
## Phase 完全性

Phase 1: Context
✅ organization-analysis.md 存在
✅ market-assessment.md 存在
✅ constraints.md 存在
✅ stakeholder-map.md 存在

Phase 2: Value Definition
✅ value-definition.md 存在
✅ value-streams-mapping.md 存在
⚠️ VS3が未定義です
✅ enterprise-activities.md 存在

Phase 3: Capabilities
✅ CL1: activity-area-classification.md 存在（傾向的分類）
✅ CL2: 3活動領域の全ケイパビリティ定義済み（正式分類）
⚠️ CL3: 8ケイパビリティ中6つの詳細能力+BO未定義
```

**2. 一貫性チェック**
```markdown
## Value Stream → Capability 整合性

VS0: ビジョン策定
→ Core Domain "Strategic Planning" に紐付き ✅
→ Subdomain "strategic-planning" 定義済み ✅
→ BC "strategic-planning-bc" 定義済み ✅

VS2: 製品開発
→ Core Domain "Product Management" に紐付き ✅
→ Subdomain "product-catalog" 定義済み ✅
→ BC "product-catalog-bc" 定義済み ✅
⚠️ Subdomain "pricing" のBC未定義

VS4: 販売活動
→ Supporting Domain "Sales Support" に紐付き ✅
⚠️ Subdomain未定義
```

**3. 命名一貫性チェック**
```markdown
## 命名規則

✅ 全サブドメイン名が kebab-case
✅ 全BC名が "{subdomain-name}-bc" パターン
⚠️ 以下のファイル名が規則に従っていません:
- outputs/3-capabilities/{vs}/cl2-subdomain-design.md 内のケイパビリティ名
→ kebab-case にリネーム推奨
```

**4. ドキュメント品質チェック**
```markdown
## ドキュメント品質

✅ 全ドキュメントにヘッダー存在
✅ 全BCに目的/責務セクション存在
⚠️ 以下のドキュメントにドメイン言語セクションが欠落:
- outputs/5-software/{service}/{bc}/domain-language.md（Phase 5で作成）

⚠️ 以下のドキュメントが空または不完全:
- outputs/2-value/enterprise-activities.md (142 bytes)
```

### phase1 指定時

Phase 1 の詳細検証：
- 必須ドキュメントの存在確認
- セクション完全性チェック
- SWOT分析の網羅性
- ステークホルダーの Power/Interest マトリックス妥当性

### phase2 / vs 指定時

Value Streams の詳細検証：
- VS0-VS7 全定義チェック
- Enterprise Activities とのマッピング
- Value Stream 間の依存関係
- KPI定義の有無

### phase3 / capabilities 指定時

Capability Hierarchy の詳細検証：
- CL1: 活動領域識別（傾向的分類の妥当性・全VS網羅性）
- CL2: ケイパビリティ設計（正式分類Core/Supporting/Generic・投資判断根拠）
- CL3: 詳細分解（≈BizOp）（各ケイパビリティの業務網羅性）
- VS → Activity Area → Capability → Operation → BC のトレーサビリティ

### architecture 指定時

Phase 4 の詳細検証：
- サービス境界とBC境界の整合性
- Context Map の完全性（全BC間の関係定義）
- 統合パターンの妥当性
- ADR（Architecture Decision Records）の存在

### platform 指定時

Phase 7 の詳細検証：
- インフラ設計の完全性
- CI/CDパイプライン定義
- 監視・可観測性設定
- デプロイメント戦略の明確性

### full 指定時

全フェーズの包括的検証：
- 上記すべての検証項目
- Phase間の整合性（Phase N → Phase N+1 のトレーサビリティ）
- エンドツーエンドのトレーサビリティ（VS0 → 実装）
- ドキュメント網羅率スコア

## 検証結果レポート

```markdown
# Parasol V5 - 検証レポート

プロジェクト: {プロジェクト名}
検証日時: {日時}
検証スコープ: {スコープ}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 検証サマリー

✅ 合格: 45 項目
⚠️ 警告: 8 項目
❌ エラー: 2 項目

総合スコア: 82/100 🟡

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## エラー (要対応)

❌ Phase 3 - CL3: 詳細能力+BO未定義
影響: Phase 4 BC境界確定への入力が不完全
対応: `/parasol:3-capabilities cl3 {capability-name}` で詳細能力+BO定義

❌ Phase 2 - VS4: 販売活動の定義不完全
影響: VS4に紐付くドメイン/サブドメインが不明
対応: `/parasol:2-value VS4` で再定義

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 警告 (推奨対応)

⚠️ 命名規則: 3ファイルが規則違反
対応: ファイル名を kebab-case にリネーム

⚠️ ドキュメント品質: ユビキタス言語セクション欠落
対応: BC定義にユビキタス言語を追加

⚠️ CL1: Generic Domain比率が高い (30%)
推奨: Core Domain比率を高める (現在20% → 目標30%+)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 次のアクション

優先度順:
1. ❌ BC未定義の6サブドメインを完成 (Phase 3 CL3)
2. ❌ VS4の再定義 (Phase 2)
3. ⚠️ ファイル名リネーム
4. ⚠️ ユビキタス言語セクション追加

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## トレーサビリティマップ

VS0: ビジョン策定
→ Core: Strategic Planning
→ Subdomain: strategic-planning ✅
→ BC: strategic-planning-bc ✅
→ Service: StrategyService (Phase 5) ⏸️

VS2: 製品開発
→ Core: Product Management
→ Subdomain: product-catalog ✅
→ BC: product-catalog-bc ✅
→ Service: ProductCatalog (Phase 5) ⏸️
→ Subdomain: pricing ✅
→ BC: pricing-bc ⚠️ 未定義
→ Service: --- (ブロック中)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 推奨事項

1. **Core Domain集中**: 
現在の投資配分を見直し、Core Domainへのリソース集中を推奨

2. **BC境界明確化**:
未定義のBCを完成させ、サービス境界を明確化

3. **ドキュメント標準化**:
全BCドキュメントに同じセクション構成を適用

4. **継続的検証**:
各Phase完了時に `/parasol:validate {phase}` を実行

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

レポートを `outputs/validation-report.md` に保存

## 自動修正提案

検証で発見された問題に対し、可能な場合は修正コマンドを提案：

```bash
# 命名規則違反の修正
mv outputs/3-capabilities/subdomain-design/CoreDomain.md \
outputs/3-capabilities/subdomain-design/core-domain-subdomains.md

# BC未定義の完成
/parasol:3-capabilities cl3 pricing
/parasol:3-capabilities cl3 inventory-management
/parasol:3-capabilities cl3 payment-processing

# VS再定義
/parasol:2-value VS4
```

## 検証基準

### スコアリング

**100-90点 (🟢 優良)**
- 全フェーズ完了
- エラー 0件
- 警告 3件以下
- トレーサビリティ完全

**89-70点 (🟡 良好)**
- Phase 3まで完了
- エラー 2件以下
- 警告 10件以下
- 一部トレーサビリティ欠落

**69-50点 (🟠 要改善)**
- Phase 2まで完了
- エラー 5件以下
- 重大な一貫性問題なし

**49点以下 (🔴 不合格)**
- Phase 1未完了 または
- エラー 6件以上 または
- 重大な一貫性問題あり

### 一貫性ルール

**必須ルール（エラー）**:
1. 各Phaseの必須ドキュメント存在
2. VS → Domain → Subdomain → BC のトレーサビリティ
3. BC定義完全性（全サブドメインにBC必要）
4. Phase間の依存関係（Phase N完了 → Phase N+1開始可能）

**推奨ルール（警告）**:
1. 命名規則（kebab-case）
2. ドキュメント標準セクション
3. Core Domain比率（30%以上推奨）
4. ユビキタス言語の明示

## 価値トレーサビリティテンプレート

### 完全トレーサビリティマップ形式

各価値要素の追跡には以下のテンプレートを使用します：

```markdown
## 価値トレーサビリティレコード

### 基本情報
| 項目 | 値 |
|------|-----|
| トレースID | VT-{VSN}-{CL2ID}-{N} |
| 作成日 | YYYY-MM-DD |
| 最終更新 | YYYY-MM-DD |

### Phase 2: 価値定義層
| レベル | ID | 名称 | 説明 |
|--------|-----|------|------|
| VL1 | VL1-{N} | [ビジョン要素] | [企業価値への貢献] |
| VL2 | VL2-{N}-{M} | [戦略要素] | [戦略的位置づけ] |
| VL3 | VL3-{N}-{M}-{L} | [戦術要素] | [具体的価値活動] |
| VS | VS{N} | [Value Stream] | [顧客価値ストリーム] |

### Phase 2→3: 価値必然性継承
| VL3-ID | 価値必然性 | 差別化可能性 | TVDC継承 |
|--------|-----------|-------------|----------|
| VL3-{ID} | ★★★/★★/★ | ★★★/★★/★ | Core/VCI/Supporting/Generic |

### Phase 3: ケーパビリティ層
| レベル | ID | 名称 | 役割 |
|--------|-----|------|------|
| L1 | L1-{N} | [戦略ケーパビリティ] | [戦略的能力] |
| CL1 | CL1-{N} | [活動領域] | [傾向的分類] |
| CL2 | CL2-{N}-{M} | [ケーパビリティ] | [正式TVDC分類] |
| CL3 | CL3-{N}-{M}-{L} | [詳細能力] | [WHAT: 具体的能力] |
| BO | BO-{N}-{M}-{L}-{K} | [業務オペレーション] | [CL3のHOW対応] |

### Phase 4: 実装層
| レベル | ID | 名称 | 役割 |
|--------|-----|------|------|
| BC | BC-{slug} | [Bounded Context] | [ドメイン境界] |
| Service | SVC-{slug} | [サービス名] | [実装サービス] |

### トレーサビリティチェーン図
```
VL1 → VL2 → VL3 → VS
           ↓
      L1 → CL1 → CL2 → CL3 → BO
                         ↓
                    BC → Service
```

### 検証チェックリスト
- [ ] VL3→CL2: TVDC分類が価値必然性と整合
- [ ] CL3→BO: 詳細能力に対応する業務オペレーション定義済み
- [ ] BO→BC: 業務オペレーションがBC境界内に配置
- [ ] 価値根拠: 全技術設計に価値根拠が明示
```

### 簡易トレーサビリティ記法

ドキュメント内での参照用簡易形式：

```
[VT] VS2 → VL3-2-1 → CL2-brewing → CL3-fermentation → BO-ferment-process → BC-brewing
```

### 価値断絶検出ルール

以下の場合は「価値断絶」としてエラー：

| 断絶パターン | 説明 | 対処 |
|-------------|------|------|
| VL3なしCL2 | CL2に対応するVL3が未定義 | Phase 2で価値要素を追加 |
| CL3なしBO | BOに対応するCL3が未定義 | Phase 3でCL3を定義 |
| BOなしBC | BCに対応するBOが未定義 | Phase 3でBO対応を明示 |
| 価値根拠なし | 技術設計に価値根拠がない | 想像の設計を削除 |

## エラーケース

**outputs/ ディレクトリが存在しない:**
```
⚠️ Parasolプロジェクトが初期化されていません

最初に Context を確立してください:
→ `/parasol:1-context`
```

**検証スコープ不明:**
```
❌ 無効な検証スコープ: xyz

有効なオプション:
- phase1, phase2, phase3, capabilities
- architecture, platform
- vs (Value Streams)
- full (完全検証)
- パラメータなし (標準検証)
```

## 継続的検証

**推奨実行タイミング**:
- 各Phase完了後: `/parasol:validate {phase}`
- 大きな変更後: `/parasol:validate`
- Phase 4開始前: `/parasol:validate phase3`（BC完全性必須）
- 最終確認: `/parasol:validate full`

**CI統合**:
```yaml
# .github/workflows/parasol-validate.yml
name: Parasol Validation

on:
pull_request:
paths:
- 'outputs/**'

jobs:
validate:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v3
- name: Validate Parasol
run: |
# Claude Code CLI で検証実行
/parasol:validate full
```

## 関連コマンド

- `/parasol:status` - 進捗確認（簡易版）
- `/parasol:0-help` - ヘルプシステム
- すべての Phase コマンド - 問題修正用
