# ケーパビリティ分解パターン集

**Parasol V4 Lite - 再利用可能な分解パターン**

---

## 概要

ケーパビリティ分解（CL1→CL2→CL3）で繰り返し適用可能なパターンを記録します。

---

## CL1: ドメイン分類パターン

### パターン1: バリューチェーン分析型

**適用条件**: 製造業、物流業など明確なバリューチェーンがある業界

```
原材料調達 → 研究開発 → 製造 → 販売 → アフターサービス
    ↓           ↓         ↓       ↓           ↓
Supporting    Core     Supporting  Core    Supporting
```

**判断基準**:
- 競合との差別化ポイント → Core
- 効率化が主目的 → Supporting
- 外部購入可能 → Generic

### パターン2: 顧客接点分析型

**適用条件**: 小売、サービス業など顧客接点が重要な業界

```
顧客獲得 → 顧客体験 → 顧客維持 → 顧客発展
    ↓         ↓          ↓          ↓
  Core      Core     Supporting   Core
```

**判断基準**:
- 顧客体験を直接創出 → Core
- 顧客体験を間接支援 → Supporting
- バックオフィス → Generic

### パターン3: プラットフォーム分析型

**適用条件**: テック企業、プラットフォームビジネス

```
プラットフォーム基盤 → エコシステム → マネタイズ
       ↓                  ↓            ↓
     Core              Core        Supporting
```

---

## CL2: サブドメイン分解パターン

### パターン1: 研究開発分離型

**適用条件**: R&Dが重要な業界（製薬、飲料、食品、化学）

```
基盤研究（長期）
├── 技術研究-A（専門領域1）  → Core
├── 技術研究-B（専門領域2）  → Core
└── 応用研究（製品化）       → Supporting

製品開発（中期）
├── カテゴリA開発           → Core
├── カテゴリB開発           → Core
└── 開発支援                → Supporting
```

**例（asashi）**:
```
基盤研究
├── fermentation-research（発酵研究）    → Core
├── ingredient-research（素材研究）      → Core
├── functional-ingredients（機能性研究）  → Supporting
└── process-engineering（プロセス技術）   → Supporting

製品開発
├── premium-beer-development             → Core
├── craft-innovation-development         → Core
├── spirits-development                  → Core
├── beverage-development                 → Core
├── sensory-evaluation（官能評価）        → Supporting
└── prototype-production（試作生産）      → Supporting
```

### パターン2: 顧客セグメント型

**適用条件**: 顧客セグメントごとに異なる価値提供が必要

```
顧客セグメントA対応
├── ニーズ分析-A       → Core
├── 提案・営業-A       → Core
└── デリバリー-A       → Supporting

顧客セグメントB対応
├── ニーズ分析-B       → Core
├── 提案・営業-B       → Core
└── デリバリー-B       → Supporting

共通基盤
├── 顧客データ基盤     → Supporting
└── 分析基盤          → Generic
```

### パターン3: プロダクトライン型

**適用条件**: 複数プロダクトラインを持つ企業

```
プロダクトラインA
├── A-企画開発        → Core
├── A-製造           → Supporting
└── A-販売           → Core

プロダクトラインB
├── B-企画開発        → Core
├── B-製造           → Supporting
└── B-販売           → Core

横断機能
├── 品質保証         → Supporting
├── サプライチェーン   → Supporting
└── IT基盤           → Generic
```

### パターン4: ライフサイクル型

**適用条件**: 製品/サービスのライフサイクル管理が重要

```
企画フェーズ
├── 市場調査         → Supporting
├── コンセプト設計    → Core
└── 事業計画         → Supporting

開発フェーズ
├── 製品開発         → Core
├── テスト・検証      → Supporting
└── 量産準備         → Supporting

運用フェーズ
├── 販売・マーケ      → Core
├── カスタマーサポート → Supporting
└── 改善・進化        → Core
```

---

## CL3: Bounded Context境界パターン

### パターン1: 集約ルート中心型

**適用条件**: 明確な中心エンティティが存在

```yaml
BC境界の決定:
  中心概念: Product（製品）
  含める:
    - ProductVariant（バリエーション）
    - ProductMedia（メディア）
    - ProductAttribute（属性）
  含めない:
    - Price（別BC: pricing）
    - Inventory（別BC: inventory）
    - Order（別BC: order）
```

### パターン2: ビジネスプロセス型

**適用条件**: 特定のビジネスプロセスを完結させる

```yaml
BC境界の決定:
  プロセス: 発酵研究プロセス
  含める:
    - 酵母株（YeastStrain）
    - 発酵実験（FermentationExperiment）
    - 発酵レシピ（FermentationRecipe）
  含めない:
    - 製品開発（別BC）
    - 品質検査（別BC）
```

### パターン3: チーム境界型

**適用条件**: 組織構造とBC境界を一致させたい

```yaml
BC境界の決定:
  チーム: 発酵研究チーム
  責任範囲:
    - 酵母の探索・育種・保存
    - 発酵条件の研究・最適化
    - 技術知見の体系化
  他チームへの提供:
    - 酵母株情報（API/イベント）
    - 発酵レシピ（API/イベント）
```

---

## 分解の判断基準

### サブドメイン数の目安

| ドメインタイプ | 推奨サブドメイン数 | 理由 |
|--------------|------------------|------|
| Core Domain | 4-6個 | 十分な詳細度で差別化を表現 |
| Supporting Domain | 2-4個 | 効率的な支援機能の提供 |
| Generic Domain | 1-3個 | 外部購入も視野に最小化 |

### 分離の判断チェックリスト

以下のいずれかに該当する場合、サブドメイン分離を検討：

- [ ] **変更頻度が異なる**: 一方は頻繁に変更、他方は安定
- [ ] **スケーリング要件が異なる**: 一方は高負荷、他方は低負荷
- [ ] **チーム境界が異なる**: 別チームが担当すべき
- [ ] **データ所有権が異なる**: 別のマスターデータを持つ
- [ ] **規制要件が異なる**: 異なるコンプライアンス要件
- [ ] **技術スタックが異なる**: 異なる技術が最適

---

## アンチパターン

### ❌ 過度な分解（Over-Decomposition）

**症状**: 1-2個のオペレーションしかないサブドメイン

**問題**:
- オーバーヘッドが増大
- チーム割り当てが困難
- 統合コストが高い

**対策**: 関連するオペレーションをまとめる

### ❌ 機能による分解（Functional Decomposition）

**症状**: 「入力」「処理」「出力」のような機能的分解

**問題**:
- ビジネス価値が見えない
- 変更時に複数BCに影響

**対策**: ビジネスケイパビリティで分解

### ❌ データモデル中心分解（Data-Centric Decomposition）

**症状**: テーブル単位でBCを分割

**問題**:
- トランザクション境界が不明確
- 分散トランザクションが必要に

**対策**: 集約ルートとビジネスルールで分解

### ❌ 技術レイヤー分解（Technical Layer Decomposition）

**症状**: 「UI」「API」「DB」のようなレイヤー分解

**問題**:
- 縦のチームが困難
- 変更が全レイヤーに波及

**対策**: 垂直スライス（機能単位）で分解

---

## 参考資料

- Eric Evans "Domain-Driven Design"
- Vaughn Vernon "Implementing Domain-Driven Design"
- Sam Newman "Building Microservices"
- Team Topologies

---

**更新履歴:**
- 2025-11-27: 初版作成（asashiプロジェクトの学びを反映）
