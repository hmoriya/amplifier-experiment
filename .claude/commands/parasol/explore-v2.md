---
description: Value decomposition exploration with flexible axis selection from 6 available axes (project:parasol)
---

# Parasol Explore V2 - 価値分解探索（6軸対応版）

業界特性に応じて6つの軸から最適な3軸を選択し、並行探索して比較・選択します。

## 使用方法

```bash
/parasol:explore init              # 探索開始: 業界判定 + 推奨軸提示
/parasol:explore select-axes       # 探索する3軸を選択（インタラクティブ）
/parasol:explore run [axis]        # 選択した軸で探索実行
/parasol:explore compare           # 選択した軸の比較表生成
/parasol:explore select [axis]     # 最終選択してmainにマージ
/parasol:explore cleanup           # worktree削除
/parasol:explore status            # 探索状況確認
```

## 6つの利用可能な軸

### 1. capability-axis（ケイパビリティ軸）
```
特徴: ビジネス能力中心の分解
適合: 機能横断的な価値創出を重視する企業
例: 人材サービス、プロフェッショナルサービス
```

### 2. business-unit-axis（事業部軸）
```
特徴: 組織構造に基づく分解
適合: 事業部制が明確で独立性の高い企業
例: 多角化企業、コングロマリット
```

### 3. value-axis（価値軸）
```
特徴: 純粋な価値種別での分解
適合: 統一的な価値体系を持つ企業
例: ブランド企業、理念駆動型企業
```

### 4. platform-axis（プラットフォーム軸）
```
特徴: 共通基盤 + 事業別サービスの2層構造
適合: プラットフォームビジネス、共通技術基盤を持つ企業
例: 飲料メーカー（共通：水・発酵 + 個別：各製品）
```

### 5. fusion-axis（融合軸）
```
特徴: 複数視点の戦略的統合
適合: 複雑な価値創造構造を持つ企業
例: 総合金融、ヘルスケア
```

### 6. multi-tier-vstr-axis（多層VST-R軸）
```
特徴: 階層的なValue Streamによる段階的価値実現
適合: サプライチェーンが長い、多段階の価値創造企業
例: 製造業、流通業
```

## 業界別推奨軸

```
┌─────────────────┬──────────────────────────────────────────┐
│ 業界            │ 推奨軸（優先順）                          │
├─────────────────┼──────────────────────────────────────────┤
│ 飲料・食品      │ 1. platform-axis                         │
│                │ 2. fusion-axis                           │
│                │ 3. multi-tier-vstr-axis                  │
├─────────────────┼──────────────────────────────────────────┤
│ 地域銀行        │ 1. value-axis                            │
│                │ 2. platform-axis                         │
│                │ 3. capability-axis                       │
├─────────────────┼──────────────────────────────────────────┤
│ 人材派遣        │ 1. capability-axis                       │
│                │ 2. platform-axis                         │
│                │ 3. business-unit-axis                    │
├─────────────────┼──────────────────────────────────────────┤
│ 製造業          │ 1. multi-tier-vstr-axis                  │
│                │ 2. platform-axis                         │
│                │ 3. capability-axis                       │
└─────────────────┴──────────────────────────────────────────┘
```

## 探索フロー

```
VL1（共通・mainブランチ）
        │
        │ /parasol:explore init
        ├─→ 業界判定
        ├─→ 推奨軸提示
        │
        │ /parasol:explore select-axes
        ├─→ 3軸を選択（推奨から選択 or カスタム）
        │
        ├──────────────┼──────────────┐
        ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ axis-1  │   │ axis-2  │   │ axis-3  │
   │worktree │   │worktree │   │worktree │
   └────┬────┘   └────┬────┘   └────┬────┘
        │              │              │
        │ run axis-1   │ run axis-2   │ run axis-3
        ▼              ▼              ▼
   VL2→VL3        VL2→VL3        VL2→VL3
   MS→VStr        MS→VStr        MS→VStr
   CL1            CL1            CL1
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                   compare
                       │
                       ▼
                select [axis]
                       │
                       ▼
                   cleanup
```

---

## サブコマンド詳細

### init - 探索初期化

**実行内容:**
1. プロジェクト検出（parasol.yaml）
2. 業界判定（settings.industry）
3. 業界別推奨軸の読み込み（_patterns/industries/{industry}/axis-selection-guide.md）
4. 推奨軸の提示

**出力例:**
```
✅ 探索環境を初期化しています

プロジェクト: asahi
業界: beverage-food（飲料・食品）

📊 業界別推奨軸:
1. platform-axis ★★★★★ 
   理由: 水資源・発酵技術の共通基盤 + 製品別展開
   
2. fusion-axis ★★★★☆
   理由: グローバル×ローカル、伝統×革新の融合
   
3. multi-tier-vstr-axis ★★★☆☆
   理由: 原料→製造→流通の多段階価値創造

次のステップ:
→ /parasol:explore select-axes  # 探索する3軸を選択
```

---

### select-axes - 軸選択

**実行内容:**
1. 推奨軸の再表示
2. インタラクティブな3軸選択
3. 選択した軸のworktree作成
4. 各worktreeへの基本ファイルコピー

**インタラクション例:**
```
📊 探索する軸を3つ選択してください

推奨軸:
[1] platform-axis ★★★★★
[2] fusion-axis ★★★★☆  
[3] multi-tier-vstr-axis ★★★☆☆

その他の軸:
[4] capability-axis
[5] business-unit-axis
[6] value-axis

選択（カンマ区切りで3つ）: 1,2,4

✅ 選択された軸:
1. platform-axis
2. fusion-axis
3. capability-axis

Worktrees作成中...
✅ 作成完了:
├── .worktrees/asahi-platform/
├── .worktrees/asahi-fusion/
├── .worktrees/asahi-capability/

次のステップ:
→ /parasol:explore run platform
→ /parasol:explore run fusion
→ /parasol:explore run capability
```

---

### run [axis] - 探索実行

**引数:** 選択した軸名（platform, fusion, capability など）

**実行内容:**
1. 対応する軸定義ファイルの読み込み（_patterns/_axes/{axis}.md）
2. 軸固有のテンプレートに基づく分解
3. VL2→VL3→MS→VStr→CL1の一連の成果物生成

**軸別の特殊処理:**

#### platform-axis の場合
```
outputs/2-value/exploration/platform/
├── vl2-vl3-decomposition.md    # 共通基盤 + 事業別の2層構造
├── platform-architecture.md     # プラットフォーム設計
├── service-layer-design.md      # サービス層設計
└── cl1-classification.md        # 2層での分類
```

#### multi-tier-vstr-axis の場合
```
outputs/2-value/exploration/multi-tier/
├── vl2-vl3-decomposition.md    # 階層的分解
├── tier-definitions.md          # 各階層の定義
├── value-flow-cascade.md        # 階層間の価値フロー
└── cl1-classification.md        # 階層別分類
```

---

### compare - 比較表生成

**実行内容:**
1. 選択した3軸の成果物を読み込み
2. 多面的な比較表を生成
3. 各軸の特性に応じた評価

**比較表テンプレート（拡張版）:**
```markdown
# 価値分解探索 比較表

## 探索サマリー

| 項目 | {axis-1} | {axis-2} | {axis-3} |
|------|----------|----------|----------|
| 軸タイプ | {説明} | {説明} | {説明} |
| VL2構造 | {特徴} | {特徴} | {特徴} |
| VStr数 | N個 | N個 | N個 |
| 特殊要素 | {軸固有} | {軸固有} | {軸固有} |
| CL1 Core数 | N個 | N個 | N個 |
| CL1 Core投資比率 | XX% | XX% | XX% |

## 軸別特性評価

### 構造的特性
| 評価項目 | {axis-1} | {axis-2} | {axis-3} |
|----------|----------|----------|----------|
| シンプルさ | ★☆☆☆☆ | ★★★☆☆ | ★★★★☆ |
| 柔軟性 | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |
| 拡張性 | ★★★★★ | ★★★☆☆ | ★★☆☆☆ |

### ビジネス適合性
| 評価項目 | {axis-1} | {axis-2} | {axis-3} |
|----------|----------|----------|----------|
| 経営戦略との整合 | ○/△/× | ○/△/× | ○/△/× |
| 組織構造との整合 | ○/△/× | ○/△/× | ○/△/× |
| 投資判断の明確性 | ○/△/× | ○/△/× | ○/△/× |

## 推奨判定

### 総合スコア
- {axis-1}: XX点
- {axis-2}: XX点  
- {axis-3}: XX点

### 推奨軸: {recommended-axis}

**推奨理由:**
{詳細な推奨理由}

### 条件付き推奨
「もし{条件}なら、{alternative-axis}も検討価値あり」
```

---

### select [axis] - 選択・確定

**実行内容:**
- 選択した軸の成果物を正式採用
- Phase 2の完了マーク
- 選択理由の記録

---

### cleanup - 環境クリーンアップ

**実行内容:**
- worktree削除
- 探索ブランチの削除
- 一時ファイルのクリーンアップ

---

### status - 探索状況確認

**拡張版ステータス表示:**
```
📋 Parasol Explore V2 Status

プロジェクト: asahi
業界: beverage-food
選択軸: platform, fusion, capability

┌─────────────────────────────────────────────────────────────┐
│ 探索状況                                                    │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│ 軸       │ VL2-VL3  │ VStr     │ CL1      │ 状態           │
├──────────┼──────────┼──────────┼──────────┼────────────────┤
│ platform │ ✅       │ ✅       │ ✅       │ 完了           │
│ fusion   │ ✅       │ ⏳       │ -        │ VStr作成中     │
│ capability│ ⏳       │ -        │ -        │ VL2-VL3作成中  │
└──────────┴──────────┴──────────┴──────────┴────────────────┘

軸別の特記事項:
- platform: プラットフォーム層の設計完了
- fusion: 融合ポイントの特定中
- capability: ケイパビリティマップ作成中
```

---

## 軸選択のベストプラクティス

### 1. 業界特性を重視
- 推奨軸には業界知見が反映されている
- まずは推奨軸から2つ以上選択することを推奨

### 2. 組み合わせの相性
良い組み合わせ例:
- platform + capability: 基盤とサービスの明確な分離
- value + business-unit: 理念と組織の整合性確認
- multi-tier + platform: 階層構造の多面的理解

### 3. 探索の目的に応じた選択
- DX推進: capability-axis を含める
- M&A/組織再編: business-unit-axis を含める  
- ブランド戦略: value-axis を含める

---

## 移行ガイド（旧explore.mdからの移行）

### 旧3軸との対応
- 旧「価値軸」→ 新「value-axis」
- 旧「事業部軸」→ 新「business-unit-axis」
- 旧「ハイブリッド」→ 新「fusion-axis」または「platform-axis」

### 主な変更点
1. 固定3軸から柔軟な6軸選択へ
2. 業界別推奨の追加
3. 軸固有のテンプレートと評価項目

---

## 関連ファイル

- `_patterns/_axes/*.md` - 各軸の詳細定義
- `_patterns/industries/*/axis-selection-guide.md` - 業界別ガイド
- `/parasol:2-value` - 通常の価値定義プロセス
- `/parasol:3-capabilities` - ケイパビリティ分解