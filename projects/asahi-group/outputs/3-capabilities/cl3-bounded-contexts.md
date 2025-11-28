# CL3 境界コンテキスト定義 - アサヒグループ（修正版）

## 設計原則

**Parasol原則**: 1つの境界コンテキスト = 1つのValue Stream内

各BCは必ず1つのVSに属し、VS境界をまたがない。

---

## 1. 境界コンテキスト一覧

| ID | コンテキスト名 | VS | ドメインタイプ | 所有チーム |
|----|---------------|-----|---------------|-----------|
| BC1 | Fermentation Platform | VS1 研究開発 | Core | コアテクノロジー研究所 |
| BC2 | Product Recipe | VS2 製品開発 | Core | 商品開発部 |
| BC3 | Brand Portfolio | VS3 ブランド | Core | マーケティング本部 |
| BC4 | Research Innovation | VS1 研究開発 | Supporting | R&D戦略室 |
| BC5 | Product Innovation | VS2 製品開発 | Supporting | 商品企画部 |
| BC6 | Functional Research | VS1 研究開発 | Supporting | 機能性研究グループ |
| BC7 | Functional Products | VS2 製品開発 | Supporting | 健康食品開発チーム |

### VS × BC マッピング

```
VS1 研究開発
├── BC1: Fermentation Platform (Core)
├── BC4: Research Innovation (Supporting)
└── BC6: Functional Research (Supporting)

VS2 製品開発
├── BC2: Product Recipe (Core)
├── BC5: Product Innovation (Supporting)
└── BC7: Functional Products (Supporting)

VS3 ブランド
└── BC3: Brand Portfolio (Core)
```

---

## 2. 各境界コンテキスト詳細

### BC1: Fermentation Platform（発酵プラットフォーム）

| 項目 | 内容 |
|------|------|
| **所属VS** | VS1 研究開発 |
| 責務 | 酵母・発酵技術の研究開発、酵母ライブラリ管理、発酵プロセス最適化 |
| 含むサブドメイン | VS1-C1-S1〜S4（酵母ライブラリ、育種、プロセス最適化、微生物学研究） |
| 所有チーム | コアテクノロジー研究所 発酵研究グループ |
| ドメインタイプ | **Core** |

#### 公開API

```yaml
YeastRecommendation:
  operation: recommendYeast
  input: targetFlavorProfile, fermentationConditions
  output: recommendedStrains, confidenceScore

FermentationOptimization:
  operation: optimizeConditions
  input: yeastStrain, targetAttributes, scaleType
  output: optimalConditions, expectedProfile
```

#### ユビキタス言語

| 用語 | 定義 |
|------|------|
| 酵母株 (Yeast Strain) | 特定の特性を持つ酵母の系統 |
| 発酵プロファイル | 発酵過程で生成される香味成分の特性 |
| スケールアップ | 実験室規模から工場規模への移行 |

---

### BC2: Product Recipe（製品処方）

| 項目 | 内容 |
|------|------|
| **所属VS** | VS2 製品開発 |
| 責務 | 製品処方の設計・管理、品質基準設定、官能評価 |
| 含むサブドメイン | VS2-C1-S1〜S3, VS2-C5-S1〜S3 |
| 所有チーム | アサヒビール商品開発部 |
| ドメインタイプ | **Core** |

#### 公開API

```yaml
RecipeDesign:
  operation: createRecipe
  input: productConcept, targetProfile, constraints
  output: recipe, qualitySpec

QualityAssessment:
  operation: evaluateProduct
  input: productSample, evaluationType
  output: evaluationResult, complianceStatus
```

#### ユビキタス言語

| 用語 | 定義 |
|------|------|
| 処方 (Recipe) | 原料配合・製造条件の仕様 |
| 辛口 (Karakuchi) | Super Dryの特徴（キレ・爽快感） |
| 官能パネル | 訓練された評価者グループ |

---

### BC3: Brand Portfolio（ブランドポートフォリオ）

| 項目 | 内容 |
|------|------|
| **所属VS** | VS3 ブランド・マーケティング |
| 責務 | グローバル・ローカルブランドの戦略策定、ブランドアイデンティティ管理 |
| 含むサブドメイン | VS3-C1-S1〜S3, VS3-C2-S1〜S3, VS3-C5-S1〜S3 |
| 所有チーム | マーケティング本部 ブランド戦略部 |
| ドメインタイプ | **Core** |

#### 公開API

```yaml
BrandGuideline:
  operation: getBrandGuidelines
  input: brandId, market
  output: guidelines, assets

CampaignPlanning:
  operation: createCampaignBrief
  input: brandId, objective, targetAudience
  output: campaignBrief
```

#### ユビキタス言語

| 用語 | 定義 |
|------|------|
| ブランドエクイティ | ブランドが持つ資産価値 |
| グローカル | グローバル×ローカルの融合戦略 |

---

### BC4: Research Innovation（研究イノベーション）

| 項目 | 内容 |
|------|------|
| **所属VS** | VS1 研究開発 |
| 責務 | 基礎研究のイノベーション管理、セレンディピティ収集、産学連携 |
| 含むサブドメイン | VS1-C4-S1〜S3（長期研究テーマ、産学連携、セレンディピティ） |
| 所有チーム | R&D戦略室 |
| ドメインタイプ | **Supporting** |

#### 公開API

```yaml
SerendipityHarvesting:
  operation: recordUnexpectedFinding
  input: experimentId, unexpectedResult, potentialApplications
  output: harvestId, evaluationStatus

ResearchPortfolio:
  operation: getResearchThemes
  input: timeHorizon, domain
  output: themes, priorityScores
```

#### ユビキタス言語

| 用語 | 定義 |
|------|------|
| セレンディピティ | 予期せぬ幸運な発見 |
| 研究ポートフォリオ | 短期・中期・長期研究の組み合わせ |

---

### BC5: Product Innovation（製品イノベーション）

| 項目 | 内容 |
|------|------|
| **所属VS** | VS2 製品開発 |
| 責務 | 実験的製品開発、限定品企画、新カテゴリ探索 |
| 含むサブドメイン | VS2-C2-S1〜S3（限定品開発、実験的製品、コラボ企画） |
| 所有チーム | 商品企画部 イノベーションチーム |
| ドメインタイプ | **Supporting** |

#### 公開API

```yaml
ExperimentalProduct:
  operation: createPilotProject
  input: concept, targetMarket, constraints
  output: projectId, timeline

LimitedEdition:
  operation: planLimitedRelease
  input: baseRecipeId, variation, quantity
  output: planId, schedule
```

#### ユビキタス言語

| 用語 | 定義 |
|------|------|
| パイロットバッチ | 試験的な少量製造ロット |
| 限定醸造 | 期間・数量限定で製造する特別製品 |

---

### BC6: Functional Research（機能性研究）

| 項目 | 内容 |
|------|------|
| **所属VS** | VS1 研究開発 |
| 責務 | 機能性素材研究、乳酸菌研究、健康効果の科学的実証 |
| 含むサブドメイン | VS1-C2-S1〜S3（乳酸菌研究、機能性成分解析、健康効果実証） |
| 所有チーム | 機能性研究グループ |
| ドメインタイプ | **Supporting** |

#### 公開API

```yaml
FunctionalIngredient:
  operation: searchIngredients
  input: healthBenefit, regulatoryRequirement
  output: ingredients, evidenceLevel

HealthEvidence:
  operation: getEvidence
  input: ingredientId, claimType
  output: clinicalStudies, regulatoryStatus
```

#### ユビキタス言語

| 用語 | 定義 |
|------|------|
| プロバイオティクス | 宿主に健康効果をもたらす生きた微生物 |
| β-グルカン | 酵母細胞壁由来の免疫活性化多糖類 |
| エビデンスレベル | 科学的根拠の強さの段階 |

---

### BC7: Functional Products（機能性製品開発）

| 項目 | 内容 |
|------|------|
| **所属VS** | VS2 製品開発 |
| 責務 | ノンアル製品開発、機能性飲料開発、健康志向製品の製品化 |
| 含むサブドメイン | VS2-C3-S1〜S3（ノンアルビール、機能性飲料、低アル製品） |
| 所有チーム | 健康食品開発チーム |
| ドメインタイプ | **Supporting** |

#### 公開API

```yaml
NonAlcoholProduct:
  operation: developNonAlcohol
  input: targetProfile, functionalClaims
  output: productSpec, regulatoryChecklist

FunctionalBeverage:
  operation: createFunctionalProduct
  input: baseIngredients, healthClaims, targetSegment
  output: productDesign, complianceStatus
```

#### ユビキタス言語

| 用語 | 定義 |
|------|------|
| スマートドリンキング | 適正飲酒・飲み方の多様化推進 |
| 機能性表示食品 | 科学的根拠に基づく健康機能表示が可能な食品 |

---

## 3. Context Map

### コンテキスト間関係図

```
VS1 研究開発                          VS2 製品開発                    VS3 ブランド
┌─────────────────────────┐    ┌─────────────────────────┐    ┌──────────────┐
│                         │    │                         │    │              │
│  ┌───────────────────┐  │    │  ┌───────────────────┐  │    │  ┌────────┐  │
│  │ BC1: Fermentation │  │    │  │ BC2: Product      │  │    │  │ BC3:   │  │
│  │     Platform      │──┼────┼─►│     Recipe        │──┼────┼─►│ Brand  │  │
│  │     [CORE]        │  │    │  │     [CORE]        │  │    │  │[CORE]  │  │
│  └───────────────────┘  │    │  └───────────────────┘  │    │  └────────┘  │
│           │             │    │           ▲             │    │              │
│           │             │    │           │             │    └──────────────┘
│  ┌────────▼──────────┐  │    │  ┌────────┴──────────┐  │
│  │ BC4: Research     │  │    │  │ BC5: Product      │  │
│  │    Innovation     │──┼────┼─►│    Innovation     │  │
│  │   [SUPPORTING]    │  │    │  │   [SUPPORTING]    │  │
│  └───────────────────┘  │    │  └───────────────────┘  │
│           │             │    │           ▲             │
│           │             │    │           │             │
│  ┌────────▼──────────┐  │    │  ┌────────┴──────────┐  │
│  │ BC6: Functional   │  │    │  │ BC7: Functional   │  │
│  │    Research       │──┼────┼─►│    Products       │  │
│  │   [SUPPORTING]    │  │    │  │   [SUPPORTING]    │  │
│  └───────────────────┘  │    │  └───────────────────┘  │
│                         │    │                         │
└─────────────────────────┘    └─────────────────────────┘
```

### 関係タイプ定義

| 上流 | 下流 | 関係タイプ | 説明 |
|------|------|-----------|------|
| BC1 (VS1) | BC2 (VS2) | Upstream/Downstream | 発酵技術→製品処方 |
| BC2 (VS2) | BC3 (VS3) | Customer/Supplier | 製品情報→ブランドストーリー |
| BC4 (VS1) | BC5 (VS2) | Upstream/Downstream | 研究シーズ→製品イノベーション |
| BC6 (VS1) | BC7 (VS2) | Upstream/Downstream | 機能性素材→機能性製品 |
| BC1 (VS1) | BC6 (VS1) | Shared Kernel | 微生物学基礎知識（同一VS内） |
| BC2 (VS2) | BC5 (VS2) | Partnership | 処方ノウハウ共有（同一VS内） |
| BC2 (VS2) | BC7 (VS2) | Partnership | 処方ノウハウ共有（同一VS内） |

### VS間連携のルール

```
【原則】
- BC間連携はイベント駆動（非同期）が基本
- 同一VS内のBC間はAPI連携も可
- VS境界を超える連携は必ずイベント経由

【VS1 → VS2 連携パターン】
BC1 publishes: YeastStrainOptimized
BC2 subscribes: 利用可能酵母リスト更新

BC6 publishes: FunctionalIngredientValidated
BC7 subscribes: 製品開発に利用可能な素材追加
```

---

## 4. 設計ストーリー

### 修正の理由

**問題**: 旧設計でBC4/BC5がVS1とVS2にまたがっていた

**原則違反**: Parasolでは1BC = 1VS内

**修正**:
- 旧BC4 → BC4（VS1内）+ BC5（VS2内）に分割
- 旧BC5 → BC6（VS1内）+ BC7（VS2内）に分割

### なぜVS境界を守るか

| 理由 | 説明 |
|------|------|
| チーム境界の明確化 | VS = チームの責任範囲。BCがまたがると責任が曖昧 |
| 独立デプロイ | VS単位でのリリースが可能 |
| 技術選択の自由 | VS1はPython中心、VS2はJava中心など |
| スケーラビリティ | VS単位でスケール可能 |

---

**作成日**: 2025-11-27（修正版）
**修正内容**: BC4/BC5をVS単位に分割し、7つのBCに再構成
**次フェーズ**: Phase 4 Architecture修正
