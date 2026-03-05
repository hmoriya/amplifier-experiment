---
description: Value definition and enterprise activities (parasol5:value)
---

# Phase 2: Value Definition & Strategic Capabilities - 価値定義・戦略ケイパビリティ

企業の価値創造を定義し、**業種・セグメント特性に応じた**Value Stages (VS0-VS7) を確立します。さらに、**V4統合により戦略ケイパビリティ層（L1 Strategic Capabilities）**を構築し、価値実現の基盤を設計します。

**重要**:
- Value Stage は「組織の活動」ではなく「顧客の状態」を定義します
- **戦略ケイパビリティは価値ストリームを実現可能にする組織能力を定義します**

## 使用方法

```bash
# Phase 2.1: Value Definition（従来）
/value5:definition              # インタラクティブ選択（業種→セグメント→VS）
/value5:definition industry     # 業種・セグメント設定
/value5:definition VS0          # VS0を直接指定
/value5:definition VS2          # VS2を直接指定
/value5:definition all          # 全VS概要を生成
/value5:definition exploration  # 6軸探索モード（capability/business-unit/value/platform/fusion/multi-tier-vstr）
/value5:definition es-ps        # ES/PS VStr（従業員・パートナー向け）設計

# Phase 2.2: Strategic Capabilities（V4統合）
/parasol:2-strategic          # L1戦略ケイパビリティ設計
/parasol:2-strategic map      # VL1→L1→VS価値マッピング
/parasol:2-strategic maturity # 戦略ケイパビリティ成熟度評価
/parasol:2-strategic vms2      # VMS2マイルストーン設定

# Phase 2.3: Value Component Analysis（V5.6）
/parasol:2-vc                 # Value Component分析
/parasol:2-vc decompose       # 3軸価値分解（ステークホルダー/時間/性質）
/parasol:2-vc vs-matrix       # VS-VC優先度マトリクス生成
/parasol:2-vc portfolio       # Value Portfolio（投資配分）設計
```

## 目的

**Phase 2.1: Value Definition（従来）**
- **Phase 1からの入力を活用する** - コングロマリットスコア・アクターインベントリを基に軸パターンを自動推奨
- **業種・セグメントを特定する** - 適切なVSパターンの選択
- **Value Proposition（価値提案）を明確化する** - 誰に、何の価値を、どのように提供するか
- **バリューステージ (VS0-VS7) を定義する** - 顧客の状態遷移として価値創造の全体像を定義
- **多段VStr（ES/PS）の必要性を判定する** - 従業員・パートナー向けVStrの設計判断

**Phase 2.2: Strategic Capabilities（V4統合）**
- **価値ヒエラルキーを戦略ケイパビリティに変換する** - VL1→VL2→VL3からL1戦略能力を設計
- **価値ストリーム実現のための組織能力を定義する** - VS実現に必要な戦略的能力
- **価値成熟度評価システムを構築する** - 各戦略能力の現在・目標・ギャップを測定
- **VMS2マイルストーンを設定する** - 戦略能力構築の成功基準と測定指標
- **Phase 3 Capabilitiesへの価値トレーサビリティを確立する** - L1→CL1→CL2→CL3の価値追跡可能性

**Phase 2.3: Value Component Analysis（V5.6）**
- **VL3をValue Componentで分析する** - 各詳細価値の5VC構成（製品/サービス/体験/関係/情報）を定義
- **3軸価値分解を実行する** - ステークホルダー軸/時間軸/性質軸による多角的価値分析
- **VS-VC優先度マトリクスを作成する** - 各Value Stageで重要なVCを特定
- **Value Portfolioを設計する** - VC別・TVDC別の投資配分を決定
- **Phase 3への価値引継ぎを準備する** - VC-Capability対応の基盤情報

## 設計哲学の適用

### VL: 情報公理適用

> 参照: [zigzag-foundations.md](../philosophy/zigzag-foundations.md#axiomatic-designの2つの公理)

**なぜVLに情報公理か**:

価値構造（VL階層）が複雑だと、後続フェーズ全体が肥大化します。

```
VL階層が深い → CL3が爆発的に増加 → BC数も爆発 → 保守不能なシステム
```

**VLチェック（情報公理）**:
- [ ] VL階層 <= 3（VL1→VL2→VL3で十分）
- [ ] 重複VLなし（同じ価値を複数箇所で定義しない）

### VS: 認知負荷管理

> **注意**: VSは「設計パラメータ」ではなく「顧客状態の記述」です。
> 情報公理ではなく、認知科学の原則（Miller's Law: 7+/-2）を適用します。

**VSチェック（認知負荷管理）**:
- [ ] VS数 5-8（Miller's Law: 人間が一度に把握できる7+/-2の範囲）
- [ ] 各VSが明確な顧客状態変化を表現
- [ ] ステークホルダーが直感的に理解できる粒度

---

### 価値の実証要件 - 想像から観察へ

> **重要**: すべての価値主張は**測定可能な現実**に基づく必要があります

#### 必須の価値検証要件

**現在の状態（ベースライン）**:
- 現在の顧客行動パターンの観察データ
- 実際に測定されている指標とその値
- 顧客の声（実際のフィードバック・苦情・要望）
- 現在の収益構造と顧客ライフサイクル

**目標の状態（測定可能な改善）**:
- 具体的な数値目標（売上、満足度、効率性等）
- 成功の測定方法とタイミング
- 失敗の早期警告指標
- ROI/KPIの定義と測定計画

## 価値方法論リファレンス

**重要**: 本フェーズは**バックキャスティングアプローチ**を採用しています。

詳細な方法論は [_value-methodology.md](../../_value-methodology.md) を参照してください。

### 方法論の全体フロー（価値先行アプローチ）

**重要**: 価値マイルストーン（MS）は「プロセス完了」ではなく「**顧客が得ている価値状態**」として定義します。

```
STEP 1: 価値分解（VLだけを先に完成）
  VL1（最上位価値）→ VL2（価値グループ）→ VL3（詳細価値）

STEP 2: 価値マイルストーン導出（バックキャスト）
  VMS5 ← VMS4 ← VMS3 ← VMS2 ← VMS1
  ※主語は常に「顧客」、内容は「状態」

STEP 3: バリューストリーム設計（VS0-VS7）
  VS0 → VS1 → VS2 → VS3 → VS4 → VS5 → VS6 → VS7

STEP 4: VL x VS マッピング

STEP 5: 優先順位決定
```

### VMSの正しい定義

| 観点 | 誤（プロセス完了） | 正（顧客価値状態） |
|------|---------------------|---------------------|
| **主語** | 組織（我々が〜した） | **顧客**（顧客が〜を得ている） |
| **記述** | 活動の完了 | **状態の達成** |
| **例** | 「システム開発完了」 | 「顧客が24時間注文可能」 |
| **測定** | タスク完了率 | **顧客価値の実現度** |

### バリューストリームの設計原則

#### 最重要原則：1価値定義 = 1バリューストリーム

**バリューストリームは価値定義からバックキャスティングして作成する「1本の統合されたストリーム」です。**

#### アンチパターン（避けるべき設計）

| 誤った設計 | 正しい設計 |
|-------------|-------------|
| 機能別に複数VStr作成 | 1本のVStrにVS0-VS7として統合 |
| 製品別にVStr作成 | 事業部レベルで1本 |
| **シナジー駆動VStr統合** | 事業間シナジーはSupporting/Generic Layerで実現 |
| **コングロマリット単一VStr** | 事業部ごとに独立VStrを設計（事業部軸） |

### V5特有機能: 設計ストーリー出力

**重要**: Parasol V5では、価値分解・バックキャスティングの各段階で**設計ストーリー（なぜそう設計したか）**を出力します。

**参照**: 業種別の設計ストーリー例は `_patterns/industry-value-stream-patterns.md` を確認してください。

## プロジェクト検出

**重要**: このコマンドはParasolプロジェクト内で実行する必要があります。

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：
1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)
3. **祖父ディレクトリ** (`../..`)

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/value5:definition

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/value5:definition  # NG
```

## 成果物

以下のドキュメントを `outputs/2-value/` に作成します：

### Phase 2.1: Value Definition成果物

#### 業種・セグメント設定（初回必須）
- **industry-profile.md** - 業種特性・セグメント定義・VSパターン選択

#### 全体成果物
- **value-streams-overview.md** - VS0-VS7の概要マップ（パターンに応じた構成）

### Phase 2.2: Strategic Capabilities成果物

- **strategic-capabilities-map.md** - L1戦略ケイパビリティの完全定義
- **capability-maturity-assessment.md** - 各L1能力の現在・目標・ギャップ分析
- **investment-allocation-matrix.md** - 戦略投資配分と優先順位付け
- **value-traceability-report.md** - VL→L1→VS価値追跡レポート
- **vms2-completion-report.md** - VMS2マイルストーン達成状況

### Phase 2.3: Value Component Analysis成果物（V5.6）

- **vl3-vc-analysis.yaml** - 各VL3のVC構成分析
- **value-decomposition-3axis.yaml** - 3軸価値分解
- **vs-vc-priority-matrix.yaml** - VS別VC優先度マトリクス
- **value-portfolio.yaml** - VC別・TVDC別投資配分計画
- **phase3-vc-handoff.md** - Phase 3へのVC-Cap対応準備情報

## 関連コマンド

- `/value5:context` - Phase 1: Context（前提条件）
- `/value5:init` - Phase 0: URLからの自動初期化
- `/parasol5:capability:decompose` - Phase 3: Capabilities
- `/value5:trace` - 価値トレーサビリティ
- `/value5:necessity-check` - 構造的必然性検証
- `/value5:imagination-detect` - 想像の設計検出
- `/parasol5:milestone:status` - 進捗確認
