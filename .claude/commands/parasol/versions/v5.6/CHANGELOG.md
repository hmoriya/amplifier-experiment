# Parasol V5.6 リリースノート

> **バージョン**: 5.6.0
> **リリース日**: TBD
> **コードネーム**: 5W1H-Driven Value Architecture

---

## ハイライト

Parasol V5.6は、BIZBOKのビジネスアーキテクチャ概念とParasolの価値駆動設計を統合する**5W1Hフレームワーク**を導入する重要なアップデートです。

### 主要な新機能

1. **WHATの二面性の明示化** - 外向きWHAT（Value Component）と内向きWHAT（Capability）を明確に区別
2. **Value Component（VC）フレームワーク** - 5つの価値構成要素による顧客視点の価値分析
3. **Operational Stage（OS）** - バリューストリーム内の運用段階の正式導入
4. **3軸価値分解** - ステークホルダー/時間/性質軸による多角的価値分析
5. **ステージ依存TVDC** - Value Stageに応じた動的TVDC分類

---

## 新概念

### Value Component（VC）

顧客に提供する価値を5つの構成要素で分析するフレームワークを導入。

| ID | 要素 | 顧客の問い |
|----|------|-----------|
| VC1 | 製品価値 | 「何を買うのか」 |
| VC2 | サービス価値 | 「どう手に入るか」 |
| VC3 | 体験価値 | 「どう感じるか」 |
| VC4 | 関係価値 | 「なぜ選び続けるか」 |
| VC5 | 情報価値 | 「何を知れるか」 |

**活用方法**:
- VL3（詳細価値）ごとにVC構成を分析
- VS-VCマトリクスで顧客状態別の重要VCを特定
- VC-Capability対応でギャップを分析

### Operational Stage（OS）

バリューストリーム内の運用段階を正式に導入。

```
Value Stage (VS) - 顧客状態
  └── Value Stream (VStr) - 価値の流れ
      └── Operational Stage (OS) - 運用段階
          └── Capability - 1:1対応
```

**設計原則**:
- 各OSで価値が蓄積される
- 1ケイパビリティは1OSに対応（ステージを跨がない）
- 判断ポイント・測定ポイントを明確化

### 3軸価値分解

WHY（価値）からWHAT（何を）への分解に3つの軸を適用。

| 軸 | 分解内容 |
|----|---------|
| ステークホルダー軸 | 顧客/株主/従業員/パートナー/社会 |
| 時間軸 | 現在価値/将来価値/持続価値 |
| 性質軸 | 機能的/情緒的/社会的 |

### ステージ依存TVDC

同一ケイパビリティでもValue Stageによって競争優位への貢献度が変化することを反映。

```yaml
capability:
  tvdc_default: "VCI"
  stage_overrides:
    VS1_VS2:
      tvdc: "Core"
      rationale: "選好形成において競争優位を生む"
```

---

## Phase別変更

### Phase 2: 価値定義

**追加ステップ**:
- Step 2.2: VC分析 - 各VL3のVC構成を分析
- Step 2.3: 3軸価値分解 - 多角的価値分析
- Step 2.5: VS-VC対応 - 顧客状態別VC重要度
- Step 2.6: Value Portfolio - 投資配分決定

**新規出力**:
- `vl3-with-vc.yaml` - VL3のVC構成定義
- `vs-vc-matrix.yaml` - VS-VC優先度マトリクス
- `value-portfolio.yaml` - 価値軸別投資配分

### Phase 3: ケイパビリティ分解

**追加ステップ**:
- Step 3.3: OS定義 - 運用段階の設計
- Step 3.4: ステージ依存TVDC設定
- Step 3.6: VC-Cap対応マッピング

**新規出力**:
- `operational-stage.yaml` - OS定義
- `vc-cap-matrix.yaml` - VC-Cap対応
- `gap-analysis.md` - ギャップ分析レポート

### Phase 4: アプリケーション設計

**追加ガイダンス**:
- OS-BC整合ガイダンス
- TVDC基づくアーキテクチャ判断サポート

---

## 新規テンプレート

| テンプレート | 用途 |
|------------|------|
| `vl3-with-vc.yaml` | VL3のVC構成定義 |
| `operational-stage.yaml` | OS定義 |
| `cl2-extended.yaml` | ステージ依存TVDC付きCL2 |
| `value-portfolio.yaml` | 投資配分 |
| `vc-cap-matrix.yaml` | VC-Cap対応マトリクス |

---

## 新規リファレンス

| ガイド | 内容 |
|--------|------|
| `value-component-guide.md` | VCフレームワーク完全ガイド |
| `operational-stage-guide.md` | OS設計ガイド |

---

## 互換性

### V5.5からの移行

V5.6はV5.5との**後方互換性を維持**しています。

| 項目 | 互換性 | 備考 |
|------|--------|------|
| VS0-VS7 | 完全互換 | 変更なし |
| VL1-VL3 | 完全互換 | メタデータ追加のみ |
| CL1-CL3 | 完全互換 | フィールド追加のみ |
| VMS | 完全互換 | 変更なし |
| TVDC | 拡張互換 | デフォルト値で動作 |

### 移行手順

1. 既存VL3へのVC分析追加
2. VS-VC対応の設定
3. OS（Operational Stage）の定義
4. ステージ依存TVDCの設定
5. VC-Cap対応の明示化
6. Value Portfolioの作成

詳細は `V56-SPECIFICATION.md` の移行ガイドを参照。

---

## 検討文書

V5.6の設計根拠となる検討文書：

| 文書 | 内容 |
|------|------|
| `V56-BIZBOK-5W1H-FRAMEWORK.md` | 5W1Hフレームワーク原案 |
| `V56-VALUE-DECOMPOSITION-DIRECTIONS.md` | 3軸価値分解 |
| `V56-STAGE-VS-MAPPING.md` | VS/OS概念整理 |
| `V56-CAPABILITY-TVDC-CLASSIFICATION.md` | TVDC分類例 |
| `V56-VALUE-COMPONENT-FRAMEWORK.md` | VCフレームワーク |

---

## 今後の予定

### V5.6.1（予定）
- バリデーションツールの追加
- 追加業種テンプレート
- 移行スクリプトの提供

### V5.7（検討中）
- WHEREチャネル軸の本格導入
- AI支援によるVC分析自動化
- ギャップ分析可視化ツール

---

## 謝辞

V5.6の設計にあたり、BIZBOKフレームワークおよび価値駆動設計の知見を参考にしました。

---

## 変更履歴

| 日付 | バージョン | 変更内容 |
|------|----------|---------|
| 2026-01-14 | Draft | 初版作成 |
