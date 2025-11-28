# BC7: Functional Products - ドメイン言語定義

## 概要

機能性製品のドメイン。ノンアルコール製品、機能性飲料、低アルコール製品の開発・管理を担う。

**BCタイプ**: Supporting（VS2内でBC2を支援）
**技術スタック**: Java/Spring Boot（VS2統一）
**アーキテクチャ**: Hexagonal Architecture

---

## ユビキタス言語

### 集約（Aggregates）

#### 1. NonAlcoholicProduct（ノンアルコール製品）

アルコール0.00%のビールテイスト飲料等。

```
NonAlcoholicProduct {
  product_id: ProductId                     // 製品ID
  product_type: NAProductType               // 製品タイプ
  flavor_profile: FlavorProfile             // 風味プロファイル
  production_method: ProductionMethod       // 製法
  health_positioning: HealthPositioning     // 健康訴求
  target_occasions: list<Occasion>          // 飲用シーン
  nutritional_info: NutritionalInfo         // 栄養成分
  certifications: list<Certification>       // 認証
  status: ProductStatus
  created_at: timestamp
  updated_at: timestamp
}
```

**ビジネスルール**:
- アルコール分0.00%を厳格に保証
- カロリー・糖質表示は100ml当たり
- 「ビール」表記は製法による制限あり

#### 2. FunctionalBeverage（機能性飲料）

特定の健康機能を訴求する飲料製品。

```
FunctionalBeverage {
  product_id: ProductId                     // 製品ID
  functional_claim: FunctionalClaim         // 機能性表示
  active_ingredients: list<ActiveIngredient>// 機能性関与成分
  evidence_reference: EvidenceRef           // エビデンス参照
  dosage_guidance: DosageGuidance           // 摂取目安
  target_consumers: TargetConsumers         // ターゲット層
  regulatory_status: RegulatoryStatus       // 規制ステータス
  labeling: ProductLabeling                 // 表示内容
  status: ProductStatus
}
```

**ビジネスルール**:
- 機能性表示食品は消費者庁届出必須
- 1日摂取目安量を明記
- 医薬品的表現の禁止

#### 3. LowAlcoholProduct（低アルコール製品）

アルコール度数を抑えた製品。

```
LowAlcoholProduct {
  product_id: ProductId                     // 製品ID
  alcohol_content: AlcoholContent           // アルコール度数
  base_style: BeerStyle                     // ベーススタイル
  reduction_method: ReductionMethod         // 低アル化手法
  flavor_compensation: FlavorCompensation   // 風味補完
  positioning: MarketPositioning            // 市場ポジショニング
  consumption_guidance: ConsumptionGuidance // 飲用ガイダンス
  status: ProductStatus
}
```

**ビジネスルール**:
- 1%未満は「微アルコール」表記
- 運転・妊婦への注意喚起必須
- 酒税法上の分類を明確化

---

### 値オブジェクト（Value Objects）

```
NAProductType {
  category: string  // BEER_TASTE | WINE_TASTE | COCKTAIL_TASTE | RTD
  subcategory: string
  alcohol_declaration: string  // "0.00%" mandatory
}

FlavorProfile {
  primary_notes: list<string>
  secondary_notes: list<string>
  bitterness_ibu: int
  body: string  // LIGHT | MEDIUM | FULL
  carbonation: string  // LOW | MEDIUM | HIGH
  serving_temperature: TemperatureRange
}

ProductionMethod {
  method_type: string  // DEALCOHOLIZATION | ARRESTED_FERMENTATION | NON_FERMENTED
  process_details: string
  quality_controls: list<string>
}

HealthPositioning {
  primary_benefit: string
  calorie_claim: string  // ZERO | LOW | REDUCED
  sugar_claim: string
  additional_claims: list<string>
}

FunctionalClaim {
  claim_type: string  // FOSHU | FNFC | FOODS_WITH_NUTRIENT
  届出番号: string  // 届出番号（機能性表示食品）
  claim_text: string
  scientific_basis: string
  notification_date: date
}

ActiveIngredient {
  ingredient_name: string
  amount_per_serving: Quantity
  daily_intake: Quantity
  function: string
  evidence_level: string
}

DosageGuidance {
  recommended_serving: string
  frequency: string
  timing: string  // BEFORE_MEAL | AFTER_MEAL | ANYTIME
  warnings: list<string>
}

AlcoholContent {
  percentage: decimal  // e.g., 0.5, 2.5, 3.0
  category: string  // NON_ALCOHOLIC | MICRO | LOW | REDUCED
  declaration_format: string
}

ReductionMethod {
  technique: string  // VACUUM_DISTILLATION | MEMBRANE | DILUTION | HYBRID
  flavor_impact: string
  efficiency: decimal
}

NutritionalInfo {
  serving_size_ml: int
  energy_kcal: decimal
  protein_g: decimal
  fat_g: decimal
  carbohydrate_g: decimal
  sugar_g: decimal
  sodium_mg: decimal
  additional_nutrients: map<string, Quantity>
}
```

---

### ドメインイベント（Domain Events）

```
# ノンアルコール製品イベント
NAProductDeveloped               // NA製品開発完了
FlavorProfileApproved            // 風味承認
ZeroAlcoholVerified              // 0.00%検証完了
NAProductLaunched                // NA製品発売

# 機能性飲料イベント
FunctionalClaimDrafted           // 機能性表示案作成
EvidencePackageLinked            // エビデンス紐付け
RegulatoryNotificationFiled      // 届出申請
FunctionalClaimAccepted          // 届出受理
FunctionalProductLaunched        // 機能性製品発売

# 低アルコール製品イベント
LowAlcoholFormulated             // 低アル処方決定
ReductionProcessValidated        // 低アル化プロセス検証
FlavorCompensationApplied        // 風味補完適用
LowAlcoholProductLaunched        // 低アル製品発売
```

---

### VS間連携イベント（Kafka）

#### 発行イベント

```json
{
  "event_type": "functional_products.product_launched",
  "payload": {
    "product_id": "string",
    "product_category": "NON_ALCOHOLIC | FUNCTIONAL | LOW_ALCOHOL",
    "product_name": "string",
    "functional_claims": ["string"],
    "target_market": "string",
    "launched_at": "timestamp"
  }
}
```

#### 購読イベント

```json
// BC6からの成分検証通知
{
  "event_type": "functional_research.ingredient_validated",
  "payload": {
    "ingredient_id": "string",
    "validated_claims": ["string"]
  }
}

// BC2からのレシピ承認
{
  "event_type": "product_recipe.recipe_approved",
  "payload": {
    "recipe_id": "string",
    "product_category": "string"
  }
}
```

---

## ドメインサービス

### NonAlcoholicProductService

```java
public interface NonAlcoholicProductService {
    NonAlcoholicProduct developProduct(NAProductType type, FlavorProfile targetProfile);
    void verifyZeroAlcohol(ProductId productId);
    void approveFlavorProfile(ProductId productId, FlavorProfile profile);
    void prepareForLaunch(ProductId productId, LaunchPlan plan);
}
```

### FunctionalBeverageService

```java
public interface FunctionalBeverageService {
    FunctionalBeverage createProduct(FunctionalClaim claim, List<ActiveIngredient> ingredients);
    void linkEvidencePackage(ProductId productId, EvidenceRef evidence);
    RegulatoryNotification fileNotification(ProductId productId);
    void updateClaimStatus(ProductId productId, RegulatoryStatus status);
}
```

### LowAlcoholService

```java
public interface LowAlcoholService {
    LowAlcoholProduct formulateProduct(BeerStyle baseStyle, AlcoholContent targetContent);
    void validateReductionProcess(ProductId productId, ReductionMethod method);
    void applyFlavorCompensation(ProductId productId, FlavorCompensation compensation);
    ComplianceCheck checkRegulatory(ProductId productId);
}
```

---

## 用語集

| 日本語 | 英語 | 定義 |
|--------|------|------|
| ノンアルコール | Non-Alcoholic | アルコール0.00%の飲料 |
| 機能性表示食品 | Foods with Function Claims (FNFC) | 消費者庁届出の機能性食品 |
| 機能性関与成分 | Active Ingredient | 機能性を発揮する成分 |
| 低アルコール | Low Alcohol | アルコール度数を抑えた製品 |
| 脱アルコール | Dealcoholization | アルコールを除去する製法 |
| 届出番号 | Notification Number | 機能性表示食品の登録番号 |
