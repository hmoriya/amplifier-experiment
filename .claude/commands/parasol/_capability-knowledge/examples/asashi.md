# asashi プロジェクト - ケーパビリティ分解の学び

**プロジェクト:** asashi (Asahi Group Holdings)
**業界:** 飲料・食品
**実施期間:** 2025-11

---

## プロジェクト概要

アサヒグループホールディングスのDX推進プロジェクト。
VS2（製品開発・イノベーション）を対象にケーパビリティ分解を実施。

---

## 採用した分解戦略

### CL1: ドメイン分類

**採用パターン**: バリューチェーン分析型 + 研究開発分離型

**判断ポイント**:
- 100年以上の醸造技術 → 発酵研究をCoreに
- 素材へのこだわり → 素材研究をCoreに
- 多角化（酒類＋飲料） → 製品カテゴリ別に分離

### CL2: サブドメイン分解

**採用パターン**: 研究開発分離型

**分解結果**:
```
基盤研究（A1）: 4サブドメイン
├── fermentation-research (Core)
├── ingredient-research (Core)
├── functional-ingredients (Supporting)
└── process-engineering (Supporting)

製品開発（A3/A4）: 4サブドメイン
├── premium-beer-development (Core)
├── craft-innovation-development (Core)
├── spirits-development (Core)
└── beverage-development (Core)

横断支援: 2サブドメイン
├── sensory-evaluation (Supporting)
└── prototype-production (Supporting)
```

**合計**: 10サブドメイン（Core 6、Supporting 4）

---

## 命名で工夫した点

### 1. 「管理」を避けた命名

| 避けた表現 | 採用した表現 | 理由 |
|-----------|-------------|------|
| 酵母管理 | fermentation-research | 継続的な研究・進化を表現 |
| 素材管理 | ingredient-research | 探究姿勢を表現 |
| 品質管理 | quality-assurance | 保証という成果を表現 |
| 試作管理 | prototype-production | 生産活動を明示 |

### 2. 製品カテゴリの明示

- `premium-beer-development`: プレミアムビール（主力）
- `craft-innovation-development`: クラフト・革新（成長領域）
- `spirits-development`: スピリッツ（高付加価値）
- `beverage-development`: 飲料（多角化）

**理由**: アサヒグループの事業構造を反映し、投資判断の粒度と一致させた

### 3. 「innovation」の明示的使用

`craft-innovation-development`に「innovation」を含めた理由：
- 既存製品改良ではなく新規性を強調
- ノンアルコール、低糖質等の革新的製品を含む
- 市場創造型の取り組みを表現

---

## 分解の成功要因

### 1. 研究と開発の明確な分離

**成功**:
- 基盤研究（長期）と製品開発（中期）を分離
- 研究成果の「提供者」と「利用者」の関係を明確化

**効果**:
- 研究チームの独立性確保
- 技術知見の再利用促進
- 投資判断の明確化

### 2. 横断支援機能の抽出

**成功**:
- 官能評価と試作生産を横断Supportingとして抽出
- 全製品開発サブドメインから利用

**効果**:
- 重複投資の回避
- 評価基準の統一
- 設備の効率的利用

### 3. 規制の違いによる分離

**成功**:
- 酒類（酒税法）と非酒類で分離
- 機能性表示食品は別途管理

**効果**:
- コンプライアンス要件の明確化
- 規制対応チームの専門化

---

## 反省点・改善点

### 1. functional-ingredientsの位置づけ

**反省**:
- 当初Coreと迷ったがSupportingに
- 健康市場の成長を考えるとCore相当の投資が必要かも

**学び**:
- 市場成長率も分類判断に含めるべき
- 将来のCore昇格を想定した設計

### 2. サブドメイン数のバランス

**反省**:
- 研究系4、開発系4、支援系2
- 支援系が少なく感じる

**学び**:
- 品質保証（VS5）との境界を明確にする必要あり
- 横断機能は別VSとの調整が重要

### 3. 命名の日英対応

**反省**:
- 日本語チームには英語名が馴染みにくい
- `fermentation-research`より「発酵研究」が使われがち

**学び**:
- 日本語名を必ず併記
- ユビキタス言語として両方を定義

---

## 次回に活かしたいこと

### 1. 分解前のヒアリング強化

- 現場チームの言葉を先に収集
- 既存システム名との整合性確認
- 組織図との照合

### 2. 類似ケーパビリティの事前チェック

- registry.yamlを活用
- グローバルケーパビリティとの照合
- 業界パターンの参照

### 3. 投資配分との連動

- CL1の時点で投資比率を仮決め
- サブドメイン数と投資比率の整合性確認
- Coreへの集中投資を意識した分解

---

## 成果物一覧

| フェーズ | 成果物 | 状態 |
|---------|--------|------|
| CL1 | cl1-domain-classification.md | ✅完了 |
| CL2 | cl2-subdomain-design.md | ✅完了 |
| CL3 | fermentation-research-bc.md | ✅完了 |
| CL3 | ingredient-research-bc.md | ✅完了 |
| CL3 | premium-beer-development-bc.md | ✅完了 |
| CL3 | craft-innovation-development-bc.md | ✅完了 |
| CL3 | spirits-development-bc.md | ✅完了 |
| CL3 | beverage-development-bc.md | ✅完了 |

---

## 関連情報

- **Phase 4成果物**: `projects/asashi/outputs/4-architecture/`
- **サービス定義**: 7サービスに統合（研究2、開発3、支援2）
- **シンボリックリンク**: Phase 4からPhase 3のBCファイルへリンク

---

**記録者:** Claude (Parasol V4 Lite)
**記録日:** 2025-11-27
