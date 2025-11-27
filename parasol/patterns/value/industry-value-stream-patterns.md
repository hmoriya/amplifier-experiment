# Industry Value Stream Patterns

業界別のValue Streamパターン集。**バックキャスティング方法論**に基づき、代表的企業を参考に設計。

---

## 方法論の適用

本ドキュメントは [_value-methodology.md](../../../.claude/commands/parasol/_value-methodology.md) の方法論を各業界に適用したパターン集です。

### 全体フロー

```
1. 価値宣言（VL1: 最上位価値）
      ↓
2. 価値分解（VL1→VL2→VL3）
      ↓
3. バックキャスティング（MS5→MS4→MS3→MS2→MS1）
      ↓
4. MS→VS変換（バリューステージ設計）
      ↓
5. プロジェクトマイルストーン = 価値MS × コアサブドメイン
```

---

## 汎用Value Streams（ベースライン）

| VS | 名称 | 最終価値提供者への価値ある状態 |
|----|------|-------------------------------|
| VS0 | Vision & Strategy | 明確な方向性と期待が共有された状態 |
| VS1 | Market Analysis | 市場機会を理解し選択できる状態 |
| VS2 | Customer Experience | 期待を超える体験を得られる状態 |
| VS3 | Operations Excellence | 安定的・効率的にサービスを受けられる状態 |
| VS4 | Innovation & Growth | 継続的に新しい価値を享受できる状態 |
| VS5 | Risk & Compliance | 安心・安全にサービスを利用できる状態 |
| VS6 | Partnership & Ecosystem | エコシステムの恩恵を受けられる状態 |
| VS7 | Sustainability & Impact | 社会的価値と共に成長できる状態 |

---

## 業界別パターン

---

## 1. 製造業・消費財（Manufacturing / Consumer Goods）

### 代表企業: アサヒグループホールディングス

**業界特性:**
- 物理的製品の設計・製造・流通
- R&Dと製品イノベーションが競争力の源泉
- サプライチェーン管理が重要
- 品質管理・規制対応が必須

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: 期待を超えるおいしさと楽しい生活文化を創造する

  提供価値:
    顧客への価値: 高品質で革新的な飲料・食品による豊かな生活体験
    社会への価値: 醸造技術を活かした持続可能な食文化の発展
    組織への価値: グローバルプレミアムブランドとしての成長

  価値の独自性:
    差別化要因: 100年以上の醸造技術と発酵研究の蓄積
    競争優位性: プレミアムビール市場でのブランド力
    価値の持続性: 継続的なR&D投資と技術革新
```

---

### 価値分解（VL1→VL2→VL3）

```yaml
VL1: 期待を超えるおいしさと楽しい生活文化の創造
  測定指標: 顧客満足度、ブランド価値、市場シェア

VL2: 価値グループ（4つ）

  VL2-1: 製品イノベーション価値
    定義: 革新的な製品開発による新しい味覚体験の提供
    VL1への貢献: おいしさの期待を超える

    VL3-1-1: 発酵技術による味の革新
      実現方法: 酵母研究、発酵条件最適化
      必要な活動: 発酵研究、官能評価

    VL3-1-2: 素材による差別化
      実現方法: 厳選素材、産地連携
      必要な活動: 素材研究、サプライヤー開発

    VL3-1-3: 健康価値の付加
      実現方法: 機能性成分研究、低糖質製品
      必要な活動: 機能性研究、製品開発

  VL2-2: 品質価値
    定義: 一貫した高品質による信頼の提供
    VL1への貢献: 期待通りの品質を保証

    VL3-2-1: 製造品質の一貫性
    VL3-2-2: 鮮度管理
    VL3-2-3: トレーサビリティ

  VL2-3: ブランド体験価値
    定義: ブランドを通じた特別な体験の提供
    VL1への貢献: 楽しい生活文化を創造

    VL3-3-1: プレミアム体験
    VL3-3-2: 地域・文化との結びつき
    VL3-3-3: 顧客コミュニティ

  VL2-4: 持続可能性価値
    定義: 環境・社会と調和した事業による長期的価値
    VL1への貢献: 持続可能な生活文化を支える

    VL3-4-1: 環境負荷低減
    VL3-4-2: 地域社会への貢献
    VL3-4-3: 責任ある飲酒推進
```

---

### バックキャスティングによる価値マイルストーン

```yaml
MS5: 製品イノベーションリーダー（18ヶ月後）
  状態: グローバルプレミアム市場でイノベーションリーダーとして認知
  成功基準:
    - 新製品売上比率 30%以上
    - プレミアムセグメントシェア1位
    - 顧客NPS +50以上
  価値指標: イノベーション指数、ブランド価値ランキング

MS4: イノベーション加速（12ヶ月後）
  状態: 研究開発パイプラインが充実し継続的な製品投入が可能
  成功基準:
    - 年間新製品10品以上
    - 開発リードタイム50%短縮
    - 研究成果の製品化率40%
  MS5への移行: 成功製品のグローバル展開

MS3: 研究基盤の成熟（9ヶ月後）
  状態: 発酵研究・素材研究の体系化と知見蓄積
  成功基準:
    - 酵母ライブラリ500株以上
    - 研究データベース構築完了
    - クロスファンクショナル連携確立
  MS4への移行: 研究成果の製品開発への展開

MS2: 研究開発プロセス展開（6ヶ月後）
  状態: 新しい研究開発プロセスが主要チームで稼働
  成功基準:
    - パイロットプロジェクト5件完了
    - 研究者の新プロセス習熟率80%
    - 初期成果物の品質評価完了
  MS3への移行: 全チームへの展開と知見の体系化

MS1: 研究開発基盤確立（3ヶ月後）
  状態: デジタル研究基盤と新プロセスの導入完了
  成功基準:
    - 研究データ管理システム稼働
    - 発酵研究チーム編成完了
    - パイロット対象製品選定完了
  MS2への移行: パイロットプロジェクトの実行開始
```

---

### MS→VS変換

| MS | VS | バリューステージ名 | 最終価値提供者（消費者）にとっての価値ある状態 |
|----|----|--------------------|---------------------------------------------|
| 基盤 | VS0 | Corporate Strategy | 企業の方向性を理解し共感できる状態 |
| MS1前半 | VS1 | Market & Consumer Insights | 自分のニーズが理解されていると感じる状態 |
| MS1後半-MS2前半 | VS2 | Product Development | 新しい製品の選択肢が増え始める状態 |
| MS2後半-MS3前半 | VS3 | Supply Chain & Manufacturing | 欲しい製品が安定的に入手できる状態 |
| MS3後半-MS4前半 | VS4 | R&D & Innovation | 期待を超える革新的製品を体験できる状態 |
| MS4後半 | VS5 | Quality & Regulatory | 品質への信頼が確立された状態 |
| MS5前半 | VS6 | Supplier & Distribution Network | あらゆるチャネルで入手できる状態 |
| MS5後半 | VS7 | Environmental & Social | 環境・社会配慮製品を選択できる状態 |

---

### 推奨VS構成

| VS | カスタマイズ名 | 重点度 | CL1候補ドメイン |
|----|---------------|--------|-----------------|
| VS0 | Corporate Strategy | Critical | strategic-planning (Supporting) |
| VS1 | Market & Consumer Insights | High | consumer-research (Core) |
| VS2 | **Product Development** | Critical | fermentation-research, ingredient-research, product-development (Core) |
| VS3 | **Supply Chain & Manufacturing** | Critical | manufacturing-operations, supply-chain (Supporting) |
| VS4 | R&D & Innovation | High | functional-ingredients, process-engineering (Core) |
| VS5 | Quality & Regulatory | High | quality-assurance, regulatory-compliance (Supporting) |
| VS6 | Supplier & Distribution Network | Medium | distribution-management (Supporting) |
| VS7 | Environmental & Social | Medium | sustainability (Generic) |

**適用例:** アサヒグループ、キリン、サントリー、コカ・コーラ、P&G、ユニリーバ

---

## 2. SaaS・ソフトウェア（SaaS / Software）

### 代表企業: Salesforce

**業界特性:**
- サブスクリプション収益モデル
- プロダクト主導の成長（PLG）
- 継続的なリリースとアップデート
- カスタマーサクセスが解約防止の鍵

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: すべての企業がAIで顧客とつながる世界を実現する

  提供価値:
    顧客への価値: 顧客関係を深め、売上を伸ばすためのプラットフォーム
    社会への価値: デジタルトランスフォーメーションの民主化
    組織への価値: 持続可能な成長と高い顧客生涯価値

  価値の独自性:
    差別化要因: 統合CRMプラットフォームとエコシステム
    競争優位性: クラウドネイティブアーキテクチャと拡張性
    価値の持続性: AIとデータ活用による継続的な価値創出
```

---

### 価値分解（VL1→VL2→VL3）

```yaml
VL1: すべての企業がAIで顧客とつながる
  測定指標: ARR成長率、顧客維持率、NPS

VL2: 価値グループ（4つ）

  VL2-1: 生産性向上価値
    定義: 営業・マーケティング・サービスの効率化
    VL1への貢献: 顧客とつながる時間を創出

    VL3-1-1: 営業プロセスの自動化
    VL3-1-2: マーケティングオートメーション
    VL3-1-3: サービスの効率化

  VL2-2: インサイト価値
    定義: データとAIによる顧客理解の深化
    VL1への貢献: AIで顧客を理解

    VL3-2-1: 顧客360度ビュー
    VL3-2-2: 予測分析
    VL3-2-3: AIレコメンデーション

  VL2-3: 拡張性価値
    定義: ビジネス成長に合わせたスケーラビリティ
    VL1への貢献: あらゆる規模の企業に対応

    VL3-3-1: マルチクラウド対応
    VL3-3-2: エンタープライズセキュリティ
    VL3-3-3: カスタマイズ性

  VL2-4: エコシステム価値
    定義: パートナー・アプリによる価値拡張
    VL1への貢献: つながりの可能性を拡大

    VL3-4-1: AppExchangeマーケットプレイス
    VL3-4-2: APIエコノミー
    VL3-4-3: 導入パートナー支援
```

---

### バックキャスティングによる価値マイルストーン

```yaml
MS5: AIファーストCRMの標準（18ヶ月後）
  状態: 顧客の業務にAI機能が完全に統合
  成功基準:
    - AI機能利用率 80%以上
    - 顧客のROI 300%以上
    - ネットリテンション率 120%以上

MS4: AI活用の最適化（12ヶ月後）
  状態: AI機能による具体的な成果が出ている
  成功基準:
    - AI予測精度 85%以上
    - 自動化タスク率 60%以上

MS3: AI機能の成熟（9ヶ月後）
  状態: AI機能が安定稼働し利用が拡大
  成功基準:
    - AI機能アクティブユーザー 50%以上
    - ユーザーフィードバックスコア 4.0以上

MS2: AI機能の展開（6ヶ月後）
  状態: AI機能が主要顧客に展開
  成功基準:
    - パイロット顧客100社完了
    - 機能採用率 30%以上

MS1: AI基盤確立（3ヶ月後）
  状態: AI機能の基盤インフラが整備
  成功基準:
    - AIプラットフォーム稼働
    - データパイプライン構築完了
```

---

### 推奨VS構成

| VS | カスタマイズ名 | 重点度 | CL1候補ドメイン |
|----|---------------|--------|-----------------|
| VS0 | Product Vision & Strategy | Critical | product-strategy (Core) |
| VS1 | Market & Competitive Analysis | High | market-intelligence (Supporting) |
| VS2 | **Customer Success & Experience** | Critical | customer-success, onboarding (Core) |
| VS3 | **Product Development & Delivery** | Critical | engineering, devops, platform (Core) |
| VS4 | Growth & Monetization | High | revenue-operations (Core) |
| VS5 | Security & Compliance | High | security, compliance (Core) |
| VS6 | Integration & Ecosystem | Medium | partnerships, integrations (Supporting) |
| VS7 | Accessibility & Inclusion | Low | accessibility (Generic) |

**適用例:** Salesforce、HubSpot、Slack、Notion、ServiceNow

---

## 3. 金融サービス（Financial Services）

### 代表企業: JPMorgan Chase

**業界特性:**
- 高度な規制環境
- 信頼とセキュリティが最優先
- レガシーシステムのモダナイゼーション
- デジタルトランスフォーメーション推進

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: 最も信頼される金融パートナーとして顧客の経済的成功を支援

  提供価値:
    顧客への価値: 安心・便利・成長を実現する金融サービス
    社会への価値: 健全な金融システムと経済発展への貢献
    組織への価値: 持続的な収益成長とリスク管理の両立

  価値の独自性:
    差別化要因: グローバルネットワークとテクノロジー投資
    競争優位性: 総合金融機関としてのワンストップサービス
    価値の持続性: 規制対応力と信頼性
```

---

### 価値分解（VL1→VL2→VL3）

```yaml
VL1: 顧客の経済的成功を支援する最も信頼されるパートナー
  測定指標: 顧客資産増加率、NPS、規制評価

VL2: 価値グループ（4つ）

  VL2-1: 安心価値（Trust）
    定義: 資産と情報の安全を保証
    VL3-1-1: 資産保護
    VL3-1-2: サイバーセキュリティ
    VL3-1-3: 不正検知

  VL2-2: 便利価値（Convenience）
    定義: いつでもどこでも利用可能な金融サービス
    VL3-2-1: デジタルバンキング
    VL3-2-2: オムニチャネル体験
    VL3-2-3: 迅速な処理

  VL2-3: 成長価値（Growth）
    定義: 顧客の経済的成長を支援
    VL3-3-1: 資産運用アドバイス
    VL3-3-2: 融資・ファイナンス
    VL3-3-3: 事業成長支援

  VL2-4: 持続価値（Sustainability）
    定義: 長期的な関係と社会的責任
    VL3-4-1: ライフステージ対応
    VL3-4-2: ESG投資
    VL3-4-3: 金融包摂
```

---

### 推奨VS構成

| VS | カスタマイズ名 | 重点度 | CL1候補ドメイン |
|----|---------------|--------|-----------------|
| VS0 | Corporate & Business Strategy | Critical | strategic-planning (Core) |
| VS1 | Market & Risk Intelligence | High | market-research, risk-analytics (Core) |
| VS2 | **Customer & Channel Experience** | Critical | digital-banking, wealth-management (Core) |
| VS3 | **Core Banking & Operations** | Critical | account-management, payments (Core) |
| VS4 | Product & Service Innovation | High | product-development (Core) |
| VS5 | **Regulatory & Compliance** | Critical | compliance, aml-kyc, audit (Core) |
| VS6 | FinTech & Partner Ecosystem | Medium | api-platform, partnerships (Supporting) |
| VS7 | Financial Inclusion & ESG | Medium | sustainability, inclusion (Supporting) |

**適用例:** JPMorgan、Goldman Sachs、三菱UFJ、Stripe、Revolut

---

## 4. 小売・Eコマース（Retail / E-commerce）

### 代表企業: Amazon

**業界特性:**
- オムニチャネル体験が必須
- 在庫・物流の最適化
- パーソナライゼーション
- 価格競争・マージン圧力

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: 地球上で最も顧客中心の企業

  提供価値:
    顧客への価値: 何でも見つかり、最高の価格で、最速で届く
    社会への価値: 中小企業の成長プラットフォーム
    組織への価値: 長期的な顧客価値とエコシステム効果

  価値の独自性:
    差別化要因: 物流ネットワークとテクノロジー基盤
    競争優位性: フライホイール効果（品揃え→顧客→出品者→品揃え）
    価値の持続性: 規模の経済とネットワーク効果
```

---

### 価値分解（VL1→VL2→VL3）

```yaml
VL1: 地球上で最も顧客中心の企業
  測定指標: 顧客満足度、リピート率、Prime会員数

VL2: 価値グループ（4つ）

  VL2-1: 選択価値（Selection）
    定義: 何でも見つかる品揃え
    VL3-1-1: 幅広いカテゴリ
    VL3-1-2: マーケットプレイス
    VL3-1-3: 検索・発見性

  VL2-2: 価格価値（Price）
    定義: 最高の価格
    VL3-2-1: 競争力のある価格
    VL3-2-2: 価格透明性
    VL3-2-3: 会員特典

  VL2-3: 利便性価値（Convenience）
    定義: 最速で届く
    VL3-3-1: 高速配送
    VL3-3-2: 簡単な返品
    VL3-3-3: ワンクリック購入

  VL2-4: 信頼価値（Trust）
    定義: 安心して購入できる
    VL3-4-1: レビュー・評価
    VL3-4-2: 購入保護
    VL3-4-3: プライバシー保護
```

---

### 推奨VS構成

| VS | カスタマイズ名 | 重点度 | CL1候補ドメイン |
|----|---------------|--------|-----------------|
| VS0 | Retail Strategy & Positioning | High | strategic-planning (Supporting) |
| VS1 | Consumer Insights & Trends | High | customer-analytics (Core) |
| VS2 | **Omnichannel Customer Experience** | Critical | customer-experience, personalization (Core) |
| VS3 | **Inventory & Fulfillment** | Critical | inventory-optimization, fulfillment, logistics (Core) |
| VS4 | Merchandising & Assortment | High | product-catalog, pricing (Core) |
| VS5 | Trust & Safety | Medium | fraud-prevention, compliance (Supporting) |
| VS6 | **Marketplace & Vendor Network** | High | marketplace-platform, seller-services (Core) |
| VS7 | Sustainable Retail | Medium | sustainability (Generic) |

**適用例:** Amazon、Walmart、楽天、ZARA、Shopify

---

## 5. 地方銀行（Regional Banking）

### 代表企業: 横浜銀行

**業界特性:**
- 地域密着型のリレーションシップバンキング
- **多面ステークホルダー構造**: 個人顧客・法人顧客・行員の3つの視点
- 地域経済・中小企業への貢献が使命
- デジタル化とリアル店舗の両立

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: 地域とともに発展し、お客さまの豊かな人生と企業の成長を支援する

  提供価値:
    個人顧客への価値: ライフステージに寄り添う金融パートナー
    法人顧客への価値: 地域経済を支える本業支援パートナー
    行員への価値: 地域貢献を実感できるやりがいある職場
    社会への価値: 地域経済の活性化と持続的発展

  価値の独自性:
    差別化要因: 地域への深い理解と長期的な関係性
    競争優位性: 地域ネットワークと信頼関係
    価値の持続性: 地域との共存共栄
```

---

### 価値分解（多面ステークホルダー型）

```yaml
VL1: 地域とともに発展し、豊かな人生と企業成長を支援
  測定指標: 地域シェア、顧客NPS、従業員エンゲージメント

VL2: 価値グループ（3面×3＝9グループ）

  # 個人顧客向け価値
  VL2-P1: 安心価値
    VL3-P1-1: 資産の安全管理
    VL3-P1-2: 将来への備え支援
    VL3-P1-3: 相談できる関係

  VL2-P2: 便利価値
    VL3-P2-1: デジタルチャネル
    VL3-P2-2: 店舗サービス
    VL3-P2-3: 手続き簡素化

  VL2-P3: 成長価値
    VL3-P3-1: 資産形成支援
    VL3-P3-2: ライフイベント対応
    VL3-P3-3: 金融リテラシー向上

  # 法人顧客向け価値
  VL2-C1: 資金価値
    VL3-C1-1: 成長資金の提供
    VL3-C1-2: 資金繰り支援
    VL3-C1-3: 柔軟な融資対応

  VL2-C2: 本業支援価値
    VL3-C2-1: 販路拡大支援
    VL3-C2-2: 人材紹介
    VL3-C2-3: 事業承継支援

  VL2-C3: 情報価値
    VL3-C3-1: 地域経済情報
    VL3-C3-2: 業界動向
    VL3-C3-3: 経営アドバイス

  # 行員向け価値
  VL2-E1: やりがい価値
    VL3-E1-1: 顧客貢献実感
    VL3-E1-2: 地域貢献実感
    VL3-E1-3: 成長実感

  VL2-E2: 働きやすさ価値
    VL3-E2-1: 業務効率化
    VL3-E2-2: 柔軟な働き方
    VL3-E2-3: 適正な評価

  VL2-E3: 成長価値
    VL3-E3-1: スキル向上
    VL3-E3-2: キャリア形成
    VL3-E3-3: 専門性獲得
```

---

### 2層構造VS設計

**Layer 1（分離型）**: セグメント固有の深掘り
**Layer 2（統合型）**: クロスステークホルダー施策

#### Layer 2: 統合型VS

| VS | 名称 | 個人価値 | 法人価値 | 行員価値 |
|----|------|---------|---------|---------|
| VS0 | Regional Strategy | 地域No.1の安心感 | 地域経済への貢献実感 | 地域貢献の誇り |
| VS1 | Market Intelligence | ニーズに合った提案 | 業界動向の情報提供 | 顧客理解の深化 |
| VS2 | **Customer Relationship** | 親身な相談対応 | 経営者との信頼関係 | やりがい・達成感 |
| VS3 | **Core Banking Operations** | 手続きの簡便さ | 融資審査の迅速化 | 業務効率化 |
| VS4 | Digital Transformation | いつでもどこでも取引 | オンライン手続き | デジタルスキル習得 |
| VS5 | **Regulatory & Risk** | 資産の安全性 | 健全な取引先 | コンプラ意識向上 |
| VS6 | Regional Partnership | 地域サービス紹介 | ビジネスマッチング | 地域貢献実感 |
| VS7 | Sustainability & Inclusion | 高齢者への配慮 | ESG経営支援 | 社会貢献の誇り |

**適用例:** 横浜銀行、福岡銀行、静岡銀行、千葉銀行

---

## 6. 人材派遣・人材サービス（Staffing / HR Services）

### 代表企業: リクルートスタッフィング

**業界特性:**
- **両面市場（Two-sided Market）**: 派遣スタッフとクライアント企業の両方が顧客
- マッチング精度が競争力の源泉
- 稼働率・定着率が収益に直結
- 労働法規制への厳格な対応

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: 一人ひとりが輝く「働く」をつくる

  提供価値:
    スタッフへの価値: 自分らしく活躍できる仕事との出会い
    クライアントへの価値: 事業成長を支える最適な人材の確保
    社会への価値: 多様な働き方の実現と労働市場の活性化

  価値の独自性:
    差別化要因: 豊富な求人と人材データベース
    競争優位性: マッチング技術と営業ネットワーク
    価値の持続性: 両面顧客の満足によるネットワーク効果
```

---

### 価値分解（両面市場型）

```yaml
VL1: 一人ひとりが輝く「働く」をつくる
  測定指標: マッチング成功率、両面NPS、稼働率

VL2: 価値グループ（両面×3＝6グループ）

  # スタッフ向け価値
  VL2-S1: 機会価値
    VL3-S1-1: 豊富な仕事情報
    VL3-S1-2: 希望条件に合う紹介
    VL3-S1-3: キャリアアップ機会

  VL2-S2: 安心価値
    VL3-S2-1: 労働者保護
    VL3-S2-2: 福利厚生
    VL3-S2-3: 担当者サポート

  VL2-S3: 成長価値
    VL3-S3-1: スキルアップ研修
    VL3-S3-2: 資格取得支援
    VL3-S3-3: キャリア相談

  # クライアント向け価値
  VL2-C1: 人材確保価値
    VL3-C1-1: 迅速な人材提案
    VL3-C1-2: 要件に合う人材
    VL3-C1-3: 豊富な人材プール

  VL2-C2: 品質価値
    VL3-C2-1: スキル評価の精度
    VL3-C2-2: 定着率の高さ
    VL3-C2-3: 即戦力人材

  VL2-C3: 安心価値
    VL3-C3-1: 法令遵守
    VL3-C3-2: 契約管理
    VL3-C3-3: トラブル対応
```

---

### 統合型VS設計

| VS | 名称 | スタッフ価値 | クライアント価値 |
|----|------|-------------|-----------------|
| VS0 | Strategy & Positioning | 信頼できるブランド | 安心して依頼できるパートナー |
| VS1 | Market & Talent Intelligence | 市場価値の把握 | 採用難易度・相場の把握 |
| VS2 | **Registration & Order Experience** | 簡単・迅速な登録 | 簡単・迅速な求人依頼 |
| VS3 | **Matching & Placement** | 希望に合う仕事紹介 | 要件に合う人材提案 |
| VS4 | Talent Development | スキルアップ機会 | 人材品質の向上 |
| VS5 | **Compliance & Worker Protection** | 労働者権利の保護 | コンプライアンスリスク回避 |
| VS6 | **Account & Relationship** | 担当者との信頼関係 | 専任担当による安定対応 |
| VS7 | Social Impact & Inclusion | 多様な働き方の選択肢 | 多様な人材活用 |

**ネットワーク効果:**
- スタッフ増加 → クライアント価値向上（人材プール拡大）
- クライアント増加 → スタッフ価値向上（仕事機会拡大）

**適用例:** リクルートスタッフィング、パソナ、テンプスタッフ、アデコ

---

## 7. プロフェッショナルサービス（Professional Services）

### 代表企業: マッキンゼー

**業界特性:**
- 人材・知識が主要資産
- プロジェクトベースの収益
- クライアントリレーション重視
- 専門性とブランドが競争力

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: 世界中の組織と人々が持続的で包括的な成長を達成することを支援する

  提供価値:
    顧客への価値: 経営課題の解決と持続的な成長の実現
    社会への価値: ビジネスリーダーの能力向上と組織変革
    組織への価値: 知的資産の蓄積と人材育成

  価値の独自性:
    差別化要因: グローバルな知見と最高の人材
    競争優位性: 実績と信頼に基づくブランド
    価値の持続性: 継続的な知識創造と人材投資
```

---

### 推奨VS構成

| VS | カスタマイズ名 | 重点度 | CL1候補ドメイン |
|----|---------------|--------|-----------------|
| VS0 | Firm Strategy & Positioning | High | firm-strategy (Core) |
| VS1 | Market & Client Intelligence | High | market-research (Supporting) |
| VS2 | **Client Experience & Delivery** | Critical | client-engagement, delivery-excellence (Core) |
| VS3 | **Resource & Project Management** | Critical | resource-planning, project-management (Core) |
| VS4 | Knowledge & IP Development | Medium | knowledge-management (Core) |
| VS5 | Professional Standards & Ethics | High | compliance, ethics (Supporting) |
| VS6 | Alliance & Referral Network | Medium | partnerships (Supporting) |
| VS7 | Pro Bono & Social Impact | Low | social-impact (Generic) |

**適用例:** マッキンゼー、BCG、デロイト、アクセンチュア、法律事務所

---

## 8. ヘルスケア・医療（Healthcare）

### 代表企業: メイヨークリニック

**業界特性:**
- 患者中心のケア
- 厳格な規制（HIPAA等）
- データプライバシーが極めて重要
- 多職種連携が必須

---

### 価値宣言（VL1）

```yaml
価値宣言:
  ビジョン: すべての患者に希望と最高のケアを提供する

  提供価値:
    患者への価値: 最高水準の医療と安心できるケア体験
    社会への価値: 医療の質向上と健康社会の実現
    組織への価値: 医療イノベーションと持続可能な経営

  価値の独自性:
    差別化要因: 統合医療モデルとチーム医療
    競争優位性: 臨床研究と教育の一体化
    価値の持続性: 継続的な医療技術革新
```

---

### 推奨VS構成

| VS | カスタマイズ名 | 重点度 | CL1候補ドメイン |
|----|---------------|--------|-----------------|
| VS0 | Healthcare Strategy & Planning | High | strategic-planning (Supporting) |
| VS1 | Population Health Analytics | High | health-analytics (Core) |
| VS2 | **Patient Experience & Care** | Critical | patient-engagement, care-coordination (Core) |
| VS3 | **Clinical Operations** | Critical | clinical-workflow, medical-records (Core) |
| VS4 | Medical Innovation & Research | High | clinical-research (Core) |
| VS5 | **Compliance & Patient Safety** | Critical | hipaa-compliance, patient-safety (Core) |
| VS6 | Care Network & Referrals | Medium | referral-network (Supporting) |
| VS7 | Health Equity & Access | Medium | health-equity (Supporting) |

**適用例:** メイヨークリニック、カイザー、国立病院機構、医療法人

---

## プロジェクトマイルストーン作成テンプレート

各業界パターンを適用後、以下のテンプレートでプロジェクトマイルストーンを作成：

```yaml
プロジェクトマイルストーン:
  業種: [業種名]
  代表企業参照: [企業名]

  PM1: [3ヶ月後の名称]
    対応MS: MS1
    コアサブドメイン別目標:
      {subdomain-1}:
        達成目標: [具体的目標]
        成果物: [成果物]
      {subdomain-2}:
        達成目標: [具体的目標]
        成果物: [成果物]

  PM2: [6ヶ月後の名称]
    対応MS: MS2
    # ...同様に記載

  PM3-PM5: # ...同様に記載
```

---

## 参照

- [価値方法論リファレンス](../../../.claude/commands/parasol/_value-methodology.md)
- [Phase 2コマンド](../../../.claude/commands/parasol/2-value.md)
- [ケーパビリティ命名ガイド](../../../.claude/commands/parasol/_capability-naming-guide.md)
- [バージョンガイド](../../VERSION-GUIDE.md)

---

**更新履歴:**
- 2025-11-27: バックキャスティング方法論を適用した全面改訂
- 2025-11-27: 代表企業（アサヒ、Salesforce、JPMorgan、Amazon等）を基に価値分解を具体化
- 2025-11-27: VL1→VL2→VL3の価値分解を各業種に追加
- 2025-11-27: MS→VS変換マッピングを追加
