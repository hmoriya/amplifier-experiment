# Parasol V5.6 開発計画

> **ステータス**: 計画策定完了
> **作成日**: 2026-01-13
> **バージョン**: 1.0

---

## 1. V5.6 ビジョン

**"5W1H-Driven Value Architecture"**

V5.6は、BIZBOKのビジネスアーキテクチャ概念とParasolの価値駆動設計を統合する包括的な5W1Hフレームワークを導入します。

### 主要イノベーション

1. **WHATの二面性**: 外向きWHAT（Value Component）と内向きWHAT（Capability）の明示的区別
2. **Value Componentフレームワーク**: 5つの価値構成要素カテゴリ
3. **多軸価値分解**: 3軸による価値分析（ステークホルダー/時間/性質）
4. **Operational Stage (OS)**: バリューストリーム内の運用段階の正式導入
5. **ステージ依存TVDC**: Value Stageに応じた動的TVDC分類

---

## 2. 新概念サマリーと優先度

### Priority 1: Critical（V5.6必須）

| 概念 | 英語 | 定義 | 影響Phase | 優先度 |
|------|------|------|-----------|--------|
| **Value Component (VC)** | Value Component | 外向きWHAT - 5つの顧客向け価値カテゴリ | Phase 2 | 10 |
| **Operational Stage (OS)** | Operational Stage | VStr内の組織活動段階 | Phase 3 | 9 |
| **VC-Capability対応** | VC-Cap Correspondence | 外向き・内向きWHATの明示的マッピング | Phase 2-3 | 9 |
| **ステージ依存TVDC** | Stage-Dependent TVDC | VSによって変わるTVDC分類 | Phase 3 | 8 |

### Priority 2: High（推奨）

| 概念 | 英語 | 定義 | 影響Phase | 優先度 |
|------|------|------|-----------|--------|
| **3軸価値分解** | Value Decomposition Directions | ステークホルダー/時間/性質軸 | Phase 2 | 7 |
| **Value Portfolio** | Value Portfolio | 価値軸別投資配分 | Phase 2 | 7 |
| **VS-VC優先度マトリクス** | VS-VC Matrix | VS別のVC重要度 | Phase 2-3 | 7 |

### Priority 3: Medium（追加検討）

| 概念 | 英語 | 定義 | 影響Phase | 優先度 |
|------|------|------|-----------|--------|
| **WHERE（チャネル）** | Channel/Touchpoint | チャネル横断的視点 | Phase 2 | 5 |
| **価値性質軸** | Value Nature | 機能的/情緒的/社会的分類 | Phase 2 | 5 |
| **ギャップ分析FW** | VC-Cap Gap Analysis | 体系的ギャップ識別 | Phase 3 | 5 |

---

## 3. Phase別影響分析

### Phase 1: コンテキスト（変更：小）

**現状**: プロジェクトコンテキスト確立
**V5.6変更**:
- 3軸分解に合わせたステークホルダー識別追加
- マルチステークホルダー価値分析の準備

### Phase 2: 価値定義（変更：大）

**現状**: VL1-VL3階層、VS0-VS7、VMS定義
**V5.6変更**:

| 追加ステップ | 内容 |
|-------------|------|
| **Step 2.2: VC分析** | 各VL3に対する5VC定義、重要度設定 |
| **Step 2.4: 3軸価値分解** | ステークホルダー/時間/性質軸の適用 |
| **Step 2.5: Value Portfolio** | 投資配分比率、優先ステークホルダー |

**テンプレート拡張**:
- `value-declaration.md` にVC分析セクション追加
- `vl3-definition.yaml` にVC構成を含める

### Phase 3: ケイパビリティ（変更：大）

**現状**: CL1-CL3階層、TVDC分類
**V5.6変更**:

| 追加概念 | 内容 |
|---------|------|
| **Operational Stage (OS)** | VStr内のOS正式定義、OS-Cap 1:1原則 |
| **ステージ依存TVDC** | `stage_overrides`による動的分類 |
| **VC-Cap対応** | 明示的マッピング、ギャップ分析 |

**テンプレート拡張**:
- CL2定義に`value_component`フィールド追加
- OS定義テンプレート新規作成
- ステージ依存TVDC仕様追加

### Phase 4: アプリケーション設計（変更：中）

**V5.6変更**:
- OS-BC整合: OSがBC境界の参考情報に
- TVDC基づく設計判断: ステージ依存TVDCがアーキテクチャ選択に影響

### Phase 5-7: ソフトウェア設計・実装・プラットフォーム（変更：小）

- Phase 2-3の新メタデータを下流に継承
- Phase自体の構造変更なし

---

## 4. スプリント計画

### Sprint 1: 基盤構築（Week 1-2）

#### ドキュメント・仕様
- [ ] **T1.1**: `V56-SPECIFICATION.md` 作成 - 完全仕様書
- [ ] **T1.2**: `CHANGELOG-V5.6.md` 作成 - リリースノート
- [ ] **T1.3**: `overview-v5.md` 更新 - V5.6概念追加
- [ ] **T1.4**: `value-component-guide.md` 作成 - VCリファレンス

#### テンプレート開発
- [ ] **T1.5**: `value-declaration.md` 拡張 - VC分析セクション
- [ ] **T1.6**: `vl3-with-vc.yaml` 作成 - VL3+VCテンプレート
- [ ] **T1.7**: `operational-stage.yaml` 作成 - OSテンプレート

### Sprint 2: Phase 2統合（Week 3-4）

#### コマンド更新
- [ ] **T2.1**: `2-value.md` 更新 - VC分析ステップ追加
- [ ] **T2.2**: 3軸分解ワークフロー追加
- [ ] **T2.3**: Value Portfolio生成ロジック作成
- [ ] **T2.4**: VS-VC優先度マトリクス生成追加

#### バリデーションルール
- [ ] **T2.5**: VC完全性バリデータ作成
- [ ] **T2.6**: 3軸カバレッジチェッカー作成
- [ ] **T2.7**: Value Portfolioバランスチェッカー追加

### Sprint 3: Phase 3統合（Week 5-6）

#### Operational Stage実装
- [ ] **T3.1**: `3-capabilities.md` 更新 - OS定義追加
- [ ] **T3.2**: OS-Capマッピング検証実装
- [ ] **T3.3**: 「ケイパビリティはステージを跨がない」チェッカー追加

#### TVDC強化
- [ ] **T3.4**: CL2テンプレートにステージ依存TVDC追加
- [ ] **T3.5**: ステージオーバーライド設定スキーマ作成
- [ ] **T3.6**: VL3価値必然性からのTVDC継承実装

#### VC-Capマッピング
- [ ] **T3.7**: VC-Cap対応マトリクス生成器作成
- [ ] **T3.8**: ギャップ分析レポート実装
- [ ] **T3.9**: ギャップ可視化追加

### Sprint 4: Phase 4統合・テスト（Week 7-8）

#### Phase 4更新
- [ ] **T4.1**: `4-application-design.md` 更新 - OS-BC整合ガイダンス
- [ ] **T4.2**: TVDC基づくアーキテクチャ判断サポート追加

#### 統合テスト
- [ ] **T4.3**: V5.6統合テストスイート作成
- [ ] **T4.4**: 飲料メーカー例でテスト
- [ ] **T4.5**: 金融サービス例でテスト
- [ ] **T4.6**: V5.5からの移行ガイド作成

### Sprint 5: ドキュメント・リリース（Week 9-10）

#### ドキュメント完成
- [ ] **T5.1**: V5.6完全ガイド章更新
- [ ] **T5.2**: 全Phaseリファレンス更新
- [ ] **T5.3**: V5.6クイックスタートガイド作成
- [ ] **T5.4**: 用語集更新

#### リリース準備
- [ ] **T5.5**: 全テンプレート最終検証
- [ ] **T5.6**: V5.5→V5.6移行スクリプト作成
- [ ] **T5.7**: リリースアナウンス準備

---

## 5. 成果物一覧

### 仕様ドキュメント

| 成果物 | パス | 説明 |
|--------|------|------|
| V5.6仕様書 | `parasol/V56-SPECIFICATION.md` | 完全V5.6フレームワーク仕様 |
| V5.6変更履歴 | `parasol/CHANGELOG-V5.6.md` | リリースノート |
| VCガイド | `parasol/reference/value-component-guide.md` | VCフレームワークリファレンス |
| OSガイド | `parasol/reference/operational-stage-guide.md` | OSリファレンス |

### コマンドファイル更新

| 成果物 | パス | 変更内容 |
|--------|------|---------|
| Phase 2コマンド | `parasol/docs/commands/2-value.md` | VC分析、3軸分解 |
| Phase 3コマンド | `parasol/docs/commands/3-capabilities.md` | OS定義、ステージ依存TVDC |
| Phase 4コマンド | `parasol/docs/commands/4-application-design.md` | OS-BC整合 |

### 新規テンプレート

| 成果物 | パス | 用途 |
|--------|------|------|
| VL3+VC | `_templates/vl3-with-vc.yaml` | VC構成付きVL3定義 |
| Operational Stage | `_templates/operational-stage.yaml` | OS定義 |
| CL2拡張 | `_templates/cl2-extended.yaml` | ステージ依存TVDC付きCL2 |
| Value Portfolio | `_templates/value-portfolio.yaml` | 投資配分 |
| VC-Capマトリクス | `_templates/vc-cap-matrix.yaml` | 対応マトリクス |

### バリデーションツール

| 成果物 | パス | 機能 |
|--------|------|------|
| VCバリデータ | `_validators/vc-completeness.py` | VCカバレッジ確認 |
| OSバリデータ | `_validators/os-cap-alignment.py` | OS-Cap対応検証 |
| ステージTVDC検証 | `_validators/stage-tvdc.py` | ステージ依存TVDC検証 |
| ギャップ分析 | `_validators/vc-cap-gap.py` | VC-Capギャップ識別 |

---

## 6. マイルストーン

```
Week 1-2   Week 3-4   Week 5-6   Week 7-8   Week 9-10
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Sprint│  │Sprint│  │Sprint│  │Sprint│  │Sprint│
│  1   │  │  2   │  │  3   │  │  4   │  │  5   │
│基盤  │→ │Phase2│→ │Phase3│→ │統合  │→ │Release│
│構築  │  │統合  │  │統合  │  │Test  │  │準備  │
└──────┘  └──────┘  └──────┘  └──────┘  └──────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
 仕様書     VC分析     OS/TVDC    テスト     V5.6
 完成      ステップ   統合完了   完了       リリース
```

---

## 7. リスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| Phase 2-3間の整合性 | VC-Cap対応の不整合 | 早期に対応マトリクス設計、Sprint 2-3で同時レビュー |
| 既存プロジェクト互換性 | V5.5プロジェクトの移行困難 | 移行ガイド・スクリプト作成、段階的移行サポート |
| 概念の複雑化 | 学習コスト増加 | クイックスタートガイド充実、必須vs任意の明確化 |
| テンプレート膨張 | メンテナンス負荷 | モジュラー設計、共通部品の抽出 |

---

## 8. 成功基準

### 必須基準（Must）

- [ ] 5つのValue Component（VC1-VC5）が定義され、Phase 2で使用可能
- [ ] Operational Stage（OS）がPhase 3で正式に扱われる
- [ ] ステージ依存TVDCが実装され、動作する
- [ ] VC-Capマッピングが文書化される
- [ ] 飲料メーカー例で全機能が動作する

### 推奨基準（Should）

- [ ] 3軸価値分解が実装される
- [ ] Value Portfolioテンプレートが使用可能
- [ ] 金融サービス例での検証完了
- [ ] V5.5からの移行ガイドが作成される

### 追加基準（Could）

- [ ] ギャップ分析可視化ツール
- [ ] 自動バリデーションツール一式
- [ ] 他業種（製造、小売等）への適用例

---

## 9. 関連ドキュメント

### V5.6検討文書（作成済み）

| ファイル | 内容 |
|---------|------|
| `V56-BIZBOK-5W1H-FRAMEWORK.md` | 元文書 + V5適用分析 |
| `V56-VALUE-DECOMPOSITION-DIRECTIONS.md` | 価値分解3軸フレームワーク |
| `V56-STAGE-VS-MAPPING.md` | VS/OS概念整理 |
| `V56-CAPABILITY-TVDC-CLASSIFICATION.md` | TVDC分類例 |
| `V56-VALUE-COMPONENT-FRAMEWORK.md` | VCフレームワーク |

### 既存V5ドキュメント

| ファイル | 参照用途 |
|---------|---------|
| `reference/overview-v5.md` | V5概要（更新対象） |
| `reference/value-methodology.md` | 価値方法論（拡張対象） |
| `concepts/TVDC-FRAMEWORK.md` | TVDC定義（拡張対象） |

---

## 変更履歴

| 日付 | バージョン | 変更内容 |
|------|----------|---------|
| 2026-01-13 | 1.0 | 初版作成 |
