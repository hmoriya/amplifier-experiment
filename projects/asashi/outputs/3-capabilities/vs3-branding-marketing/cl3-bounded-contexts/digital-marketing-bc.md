# Bounded Context: digital-marketing-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** digital-marketing（デジタルマーケティング）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | digital-marketing-bc |
| **日本語名** | デジタルマーケティング |
| **命名パターン** | `-marketing`（業界標準用語） |
| **命名理由** | 業界で広く認知された用語を採用。SNS・SEO/SEM・インフルエンサー・EC施策の**継続的展開**と**デジタルチャネルでの顧客接点最大化**を表現。「デジタル広告管理」ではなく「マーケティング」で戦略的・統合的活動を強調 |
| **VS横断一意性** | 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

**BC名**: digital-marketing-bc（デジタルマーケティングバウンデッドコンテキスト）

**目的**:
SNS、SEO/SEM、インフルエンサー、EC連動施策を通じて、デジタルチャネルでのブランド接点を最大化し、Z世代を含む新規顧客層へのリーチを強化する。マルチブランド・マルチリージョンでのデジタル施策を統合管理し、責任ある飲酒に配慮したデジタルコミュニケーションを実現する。

**責務**:
- マルチブランドSNSアカウント運用（Instagram、X、TikTok、YouTube等）
- コンテンツマーケティング戦略の策定・実行
- SEO/SEMキーワード戦略・運用最適化
- EC/D2Cチャネル連動施策の企画・実行
- インフルエンサーパートナーシップの管理
- デジタル広告のプログラマティック運用
- デジタル施策のKPI管理・最適化

**チーム境界**:
- **担当組織**: マーケティング本部 デジタルマーケティング部
- **チーム構成**:
  - SNSマーケティングチーム（プラットフォーム別運用）
  - コンテンツ制作チーム（動画・記事・クリエイティブ）
  - パフォーマンスマーケティングチーム（SEO/SEM・広告運用）
  - インフルエンサーマーケティングチーム
  - EC連携チーム（D2C・ECモール連携）
- **推定人員**: 30-50名（地域横断）

---

### 2. ビジネスオペレーション詳細

#### OP1: SNSマーケティング（Instagram、X、TikTok等）

**業務フロー:**
```
1. SNS戦略策定
   └─ プラットフォーム別戦略（Instagram=ビジュアル訴求、TikTok=Z世代リーチ等）
   └─ ブランド別アカウント運用方針（Asahi Super Dry、Peroni等）
   └─ 地域別ローカライズ方針
   └─ 投稿カレンダー作成

2. コンテンツ制作・承認
   └─ クリエイティブ企画（brand-asset-governanceガイドライン準拠）
   └─ 責任ある飲酒表現の確認（年齢ゲート、警告表示）
   └─ 法規制確認（各国酒類広告規制）
   └─ 承認ワークフロー実行

3. 投稿・エンゲージメント管理
   └─ スケジュール投稿
   └─ リアルタイムエンゲージメント対応（コメント返信等）
   └─ UGC（ユーザー生成コンテンツ）キュレーション
   └─ クライシス対応（炎上リスク管理）

4. パフォーマンス分析
   └─ エンゲージメント率、リーチ、インプレッション測定
   └─ 競合ベンチマーク
   └─ 最適化施策立案
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 全SNS投稿は法定年齢確認（日本20歳/欧州18歳等）を実装したアカウントで配信 |
| BR-OP1-02 | アルコール製品投稿には責任ある飲酒メッセージを必須とする |
| BR-OP1-03 | 投稿前に各国酒類広告規制への準拠確認を必須とする |
| BR-OP1-04 | UGC利用時は著作権・肖像権の許諾確認を必須とする |
| BR-OP1-05 | クライシス発生時は2時間以内に初動対応を開始する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ブランド戦略（brand-strategy） | SNSコンテンツ |
| キャンペーン情報（campaign-communications） | エンゲージメントデータ |
| ブランド資産（brand-asset-governance） | フォロワー成長データ |

**トリガー:**
- コンテンツカレンダースケジュール
- キャンペーン開始
- リアルタイムイベント（スポーツ試合等）
- トレンド機会

---

#### OP2: コンテンツマーケティング

**業務フロー:**
```
1. コンテンツ戦略策定
   └─ オウンドメディア戦略（Webサイト、ブログ、メールマガジン）
   └─ コンテンツピラー設定（ブランドストーリー、製品知識、ライフスタイル等）
   └─ ターゲットオーディエンス定義（VS1消費者インサイト連携）
   └─ コンテンツカレンダー作成

2. コンテンツ制作
   └─ 記事・ブログ制作
   └─ 動画コンテンツ制作（ブランドストーリー、製品紹介、How-to等）
   └─ インフォグラフィック・ビジュアル制作
   └─ ポッドキャスト・音声コンテンツ（必要に応じて）

3. コンテンツ配信
   └─ SEO最適化（OP3連携）
   └─ SNS配信（OP1連携）
   └─ メール配信
   └─ ペイドメディア活用（OP6連携）

4. パフォーマンス測定・最適化
   └─ PV、滞在時間、直帰率測定
   └─ コンテンツ別CVR分析
   └─ A/Bテスト実施
   └─ コンテンツ改善・リライト
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | 全コンテンツはブランドガイドライン準拠を必須とする |
| BR-OP2-02 | 製品関連コンテンツは責任ある飲酒メッセージを含める |
| BR-OP2-03 | エバーグリーンコンテンツは年1回以上のレビュー・更新を行う |
| BR-OP2-04 | 動画コンテンツは字幕・音声ガイド対応を推奨する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品情報・ストーリー（VS2） | 記事・ブログコンテンツ |
| ブランドストーリー（brand-strategy） | 動画コンテンツ |
| 消費者インサイト（VS1） | コンテンツライブラリ |

**トリガー:**
- コンテンツカレンダー
- 新製品発売
- 季節イベント
- トレンドトピック

---

#### OP3: SEO/SEM施策

**業務フロー:**
```
1. キーワード戦略策定
   └─ キーワードリサーチ（検索ボリューム、競合性分析）
   └─ ブランド別キーワードマップ作成
   └─ ロングテールキーワード戦略
   └─ ローカルSEO戦略（地域別最適化）

2. SEO施策実行
   └─ オンページSEO（タイトル、メタ、コンテンツ最適化）
   └─ テクニカルSEO（サイト速度、モバイル対応、構造化データ）
   └─ コンテンツSEO（OP2連携）
   └─ リンクビルディング

3. SEM（リスティング広告）運用
   └─ キャンペーン構造設計
   └─ 広告文・LP作成
   └─ 入札戦略設定
   └─ A/Bテスト実施

4. パフォーマンス分析・最適化
   └─ オーガニック順位トラッキング
   └─ CTR、CVR、CPA分析
   └─ 競合分析
   └─ 最適化施策実施
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | アルコール関連キーワードは各国規制に準拠したLP誘導とする |
| BR-OP3-02 | SEM広告はターゲティングで未成年除外を必須とする |
| BR-OP3-03 | ブランドキーワードの競合入札は事前承認を必須とする |
| BR-OP3-04 | キーワードランキングは週次でモニタリングする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ブランドキーワード要件 | キーワードランキングデータ |
| コンテンツ（OP2） | オーガニック流入データ |
| 予算配分 | SEM広告パフォーマンスデータ |

**トリガー:**
- 新製品・キャンペーン開始
- 検索トレンド変化
- 競合動向
- アルゴリズム更新

---

#### OP4: EC連動施策（D2C含む）

**業務フロー:**
```
1. EC戦略策定
   └─ D2Cサイト戦略（自社EC）
   └─ ECモール戦略（Amazon、楽天等）
   └─ クロスチャネル連携（オンラインtoオフライン）
   └─ サブスクリプション施策

2. EC販促施策企画
   └─ シーズナルプロモーション
   └─ 限定商品・先行販売
   └─ バンドル販売
   └─ ポイント・クーポン施策

3. EC連動デジタル施策
   └─ リターゲティング広告（OP6連携）
   └─ カート放棄メール
   └─ パーソナライズレコメンド
   └─ SNS直接販売（Instagram Shop等）

4. EC効果測定
   └─ EC売上・CVR分析
   └─ 顧客単価（AOV）分析
   └─ LTV分析
   └─ アトリビューション分析
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | EC販売は年齢確認プロセスを必須とする |
| BR-OP4-02 | 配送地域は各国酒類販売規制に準拠する |
| BR-OP4-03 | D2Cサイトと小売チャネルの価格整合性を維持する |
| BR-OP4-04 | 限定商品情報はエンバーゴ日まで非公開とする |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品情報（VS2） | EC売上データ |
| 販売計画（VS4） | 顧客購買データ |
| キャンペーン情報 | CVRデータ |

**トリガー:**
- 新製品発売
- 季節キャンペーン
- 在庫状況
- 競合プロモーション

---

#### OP5: インフルエンサーマーケティング

**業務フロー:**
```
1. インフルエンサー戦略策定
   └─ ターゲットオーディエンス定義
   └─ インフルエンサー層分類（メガ/マクロ/マイクロ/ナノ）
   └─ プラットフォーム選定
   └─ 予算配分

2. インフルエンサー発掘・選定
   └─ インフルエンサーリサーチ
   └─ オーディエンス分析（フォロワー属性、エンゲージメント率）
   └─ ブランド適合性評価
   └─ リスク評価（過去投稿、論争等）

3. パートナーシップ契約・実行
   └─ 契約交渉・締結
   └─ ブリーフィング（ブランドガイドライン、責任ある飲酒）
   └─ コンテンツレビュー・承認
   └─ 配信・モニタリング

4. 効果測定・関係管理
   └─ エンゲージメント、リーチ、CVR測定
   └─ ROI分析
   └─ 長期パートナーシップ評価
   └─ アンバサダープログラム運営
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP5-01 | インフルエンサーは法定飲酒年齢以上、かつフォロワーの70%以上が成人であることを確認 |
| BR-OP5-02 | 全投稿にPR表記（#PR、#タイアップ等）を必須とする |
| BR-OP5-03 | 責任ある飲酒メッセージの掲載を契約条項に含める |
| BR-OP5-04 | コンテンツは投稿前にブランド承認を必須とする |
| BR-OP5-05 | 過度な飲酒を助長する表現は禁止する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| キャンペーン方針 | インフルエンサーコンテンツ |
| ブランドガイドライン | インフルエンサーエンゲージメントデータ |
| 予算 | ROIレポート |

**トリガー:**
- キャンペーン開始
- 新製品発売
- イベント連動
- 長期パートナーシップ更新

---

#### OP6: デジタル広告運用

**業務フロー:**
```
1. メディアプランニング
   └─ 目標設定（認知、検討、購買）
   └─ チャネルミックス設計（ディスプレイ、動画、ソーシャル等）
   └─ オーディエンスセグメント設計
   └─ 予算配分

2. キャンペーン設定・実行
   └─ DSP/SSP連携設定
   └─ クリエイティブ入稿
   └─ ターゲティング設定（年齢制限必須）
   └─ フリークエンシーキャップ設定

3. リアルタイム最適化
   └─ 入札最適化
   └─ クリエイティブローテーション
   └─ A/Bテスト
   └─ ビューアビリティ管理

4. 効果測定・レポーティング
   └─ インプレッション、クリック、CVR分析
   └─ ブランドリフト調査
   └─ アトリビューション分析
   └─ ROI計算・レポート作成
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP6-01 | 全デジタル広告は法定飲酒年齢以上のみをターゲティング |
| BR-OP6-02 | 広告配信面は酒類広告掲載可能なメディアのみとする |
| BR-OP6-03 | 子供向けコンテンツ・サイトへの配信を禁止する |
| BR-OP6-04 | ビューアビリティ基準（MRC基準）を満たす配信を優先する |
| BR-OP6-05 | ブランドセーフティリストを適用する |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| メディアプラン | 広告配信データ |
| クリエイティブ資産 | パフォーマンスデータ（Imp、Click、CV） |
| 予算 | ROIレポート |

**トリガー:**
- キャンペーン開始
- 予算消化状況
- パフォーマンス変動
- 競合出稿動向

---

### 3. ユビキタス言語（Ubiquitous Language）

#### デジタルマーケティング基本用語

| 用語 | 定義 |
|------|------|
| **Engagement（エンゲージメント）** | SNS投稿に対するユーザーのいいね、コメント、シェア等の反応 |
| **Impression（インプレッション）** | 広告またはコンテンツが表示された回数 |
| **Reach（リーチ）** | コンテンツを見たユニークユーザー数 |
| **CTR（クリック率）** | インプレッションに対するクリック数の割合 |
| **CVR（コンバージョン率）** | クリックまたは訪問に対するコンバージョン数の割合 |
| **CPA（獲得単価）** | 1コンバージョンあたりの広告費用 |
| **ROAS（広告費用対効果）** | 広告費用に対する売上の比率 |

#### SNS・コンテンツ用語

| 用語 | 定義 |
|------|------|
| **UGC（ユーザー生成コンテンツ）** | 消費者が自発的に作成したブランド関連コンテンツ |
| **Influencer（インフルエンサー）** | SNS上で影響力を持つ個人 |
| **Content Pillar（コンテンツピラー）** | コンテンツ戦略の柱となるテーマ領域 |
| **Evergreen Content（エバーグリーンコンテンツ）** | 時間が経っても価値が減少しにくいコンテンツ |
| **Age Gate（エイジゲート）** | 年齢確認を求めるアクセス制限機能 |

#### SEO/SEM用語

| 用語 | 定義 |
|------|------|
| **Organic Traffic（オーガニック流入）** | 検索エンジンからの自然検索流入 |
| **Paid Search（ペイドサーチ）** | 検索エンジン広告（リスティング広告） |
| **Keyword Ranking（キーワードランキング）** | 特定キーワードでの検索順位 |
| **Long-tail Keyword（ロングテールキーワード）** | 検索ボリュームは少ないが具体的なキーワード |
| **Quality Score（品質スコア）** | 広告の品質を示すGoogle指標 |

#### EC用語

| 用語 | 定義 |
|------|------|
| **D2C（Direct to Consumer）** | 自社ECでの直接販売モデル |
| **AOV（平均注文単価）** | 1注文あたりの平均購入金額 |
| **Cart Abandonment（カート放棄）** | カートに商品を入れたまま購入しない行動 |
| **LTV（顧客生涯価値）** | 顧客が生涯にわたってもたらす収益の予測値 |

#### 広告運用用語

| 用語 | 定義 |
|------|------|
| **Programmatic Advertising（プログラマティック広告）** | 自動入札による広告配信 |
| **DSP（Demand Side Platform）** | 広告主側の広告配信プラットフォーム |
| **Retargeting（リターゲティング）** | サイト訪問者への再広告配信 |
| **Brand Safety（ブランドセーフティ）** | 不適切なコンテンツ横への広告配信回避 |
| **Viewability（ビューアビリティ）** | 広告が実際に視認可能だった割合 |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: SocialMediaAccount（SNSアカウント）

**責務**: ブランド別SNSアカウントの管理

```
SocialMediaAccount [Aggregate Root]
├── accountId: AccountId [Value Object]
├── platform: Platform [Value Object]
│   └── value: enum (INSTAGRAM, X, TIKTOK, YOUTUBE, FACEBOOK, LINKEDIN)
├── brandId: BrandId [Value Object]
├── region: Region [Value Object]
├── handle: Handle [Value Object]
├── accountType: AccountType [Value Object]
│   └── value: enum (BRAND_OFFICIAL, CAMPAIGN, PRODUCT_LINE)
├── ageGateEnabled: boolean
├── followers: FollowerMetrics [Value Object]
│   ├── count: number
│   ├── growthRate: Percentage
│   └── demographics: AudienceDemographics
├── engagementRate: EngagementRate [Value Object]
├── contentGuidelines: ContentGuideline[] [Entity]
├── approvers: Approver[] [Entity]
├── status: AccountStatus [Value Object]
│   └── value: enum (ACTIVE, PAUSED, ARCHIVED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-SMA-01 | アルコールブランドアカウントはageGateEnabled=trueを必須 |
| INV-SMA-02 | BRAND_OFFICIALアカウントは最低1名のapproverを必須 |
| INV-SMA-03 | 同一ブランド・同一プラットフォーム・同一リージョンで複数OFFICIALは不可 |

---

#### 集約2: SocialContent（SNSコンテンツ）

**責務**: SNS投稿コンテンツのライフサイクル管理

```
SocialContent [Aggregate Root]
├── contentId: ContentId [Value Object]
├── accountId: AccountId [Value Object]
├── contentType: ContentType [Value Object]
│   └── value: enum (POST, STORY, REEL, VIDEO, CAROUSEL)
├── caption: Caption [Value Object]
│   ├── text: string
│   ├── hashtags: Hashtag[]
│   └── mentions: Mention[]
├── media: MediaAsset[] [Entity]
│   ├── assetId: AssetId
│   ├── type: enum (IMAGE, VIDEO, GIF)
│   └── url: URL
├── responsibleDrinkingMessage: ResponsibleDrinkingMessage [Value Object]
├── scheduledAt: DateTime
├── publishedAt: DateTime?
├── performance: ContentPerformance [Entity]
│   ├── impressions: number
│   ├── reach: number
│   ├── engagements: number
│   ├── engagementRate: Percentage
│   └── clicks: number
├── approvalStatus: ContentApprovalStatus [Value Object]
│   ├── status: enum (DRAFT, PENDING_REVIEW, APPROVED, REJECTED, PUBLISHED)
│   ├── reviewedBy: UserId?
│   ├── reviewedAt: DateTime?
│   └── rejectionReason: string?
├── complianceCheck: ComplianceCheck [Entity]
│   ├── ageRestrictionCompliant: boolean
│   ├── responsibleDrinkingCompliant: boolean
│   ├── localRegulationCompliant: boolean
│   └── brandGuidelineCompliant: boolean
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-SC-01 | PUBLISHED状態への遷移には全complianceCheck項目がtrue |
| INV-SC-02 | アルコール製品コンテンツはresponsibleDrinkingMessageが必須 |
| INV-SC-03 | APPROVED状態のコンテンツは内容変更不可（新規作成が必要） |

---

#### 集約3: SEOKeyword（SEOキーワード）

**責務**: キーワード戦略とランキング管理

```
SEOKeyword [Aggregate Root]
├── keywordId: KeywordId [Value Object]
├── keyword: Keyword [Value Object]
│   ├── term: string
│   ├── language: Language
│   └── region: Region
├── category: KeywordCategory [Value Object]
│   └── value: enum (BRAND, PRODUCT, CATEGORY, LONG_TAIL, COMPETITOR)
├── searchVolume: SearchVolume [Value Object]
│   ├── monthly: number
│   └── trend: enum (RISING, STABLE, DECLINING)
├── competition: CompetitionLevel [Value Object]
│   └── value: enum (LOW, MEDIUM, HIGH)
├── targetBrands: BrandId[] [Value Object]
├── rankings: KeywordRanking[] [Entity]
│   ├── date: Date
│   ├── position: number
│   ├── url: URL
│   └── searchEngine: SearchEngine
├── targetPosition: number
├── semBid: SEMBid [Entity]
│   ├── maxCPC: Money
│   ├── qualityScore: number
│   └── estimatedCTR: Percentage
├── status: KeywordStatus [Value Object]
│   └── value: enum (ACTIVE, PAUSED, MONITORING_ONLY)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-SEO-01 | COMPETITORカテゴリキーワードのSEM入札は要承認フラグを設定 |
| INV-SEO-02 | targetPositionは1-100の範囲内 |
| INV-SEO-03 | rankingsは最新365日分を保持 |

---

#### 集約4: Influencer（インフルエンサー）

**責務**: インフルエンサーパートナー情報管理

```
Influencer [Aggregate Root]
├── influencerId: InfluencerId [Value Object]
├── name: InfluencerName [Value Object]
├── platforms: InfluencerPlatform[] [Entity]
│   ├── platform: Platform
│   ├── handle: Handle
│   ├── followerCount: number
│   ├── engagementRate: Percentage
│   └── audienceDemographics: AudienceDemographics
├── categories: ContentCategory[] [Value Object]
├── tier: InfluencerTier [Value Object]
│   └── value: enum (MEGA, MACRO, MICRO, NANO)
├── ageVerified: AgeVerification [Value Object]
│   ├── verified: boolean
│   ├── birthDate: Date?
│   └── verifiedAt: DateTime?
├── audienceAgeCompliance: AudienceAgeCompliance [Value Object]
│   ├── adultPercentage: Percentage
│   ├── verifiedAt: DateTime
│   └── compliant: boolean (>70% adult)
├── riskAssessment: RiskAssessment [Entity]
│   ├── score: RiskScore (1-10)
│   ├── factors: RiskFactor[]
│   └── assessedAt: DateTime
├── partnershipHistory: Partnership[] [Entity]
│   ├── campaignId: CampaignId
│   ├── contractValue: Money
│   ├── deliverables: Deliverable[]
│   ├── performance: PartnershipPerformance
│   └── status: PartnershipStatus
├── status: InfluencerStatus [Value Object]
│   └── value: enum (PROSPECT, APPROVED, ACTIVE, PAUSED, BLOCKED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-INF-01 | ACTIVE状態にはageVerified=trueを必須 |
| INV-INF-02 | アルコールブランド施策にはaudienceAgeCompliance.compliant=trueを必須 |
| INV-INF-03 | riskScore > 7のインフルエンサーはACTIVE不可 |
| INV-INF-04 | BLOCKEDからの復帰は新規審査が必要 |

---

#### 集約5: DigitalAdCampaign（デジタル広告キャンペーン）

**責務**: プログラマティック広告キャンペーン管理

```
DigitalAdCampaign [Aggregate Root]
├── campaignId: CampaignId [Value Object]
├── name: CampaignName [Value Object]
├── brandId: BrandId [Value Object]
├── objective: CampaignObjective [Value Object]
│   └── value: enum (AWARENESS, CONSIDERATION, CONVERSION)
├── budget: Budget [Entity]
│   ├── totalBudget: Money
│   ├── dailyBudget: Money
│   ├── spent: Money
│   └── remaining: Money
├── schedule: CampaignSchedule [Value Object]
│   ├── startDate: DateTime
│   ├── endDate: DateTime
│   └── dayParting: DayPartingRule[]
├── targeting: AdTargeting [Entity]
│   ├── ageRange: AgeRange (minAge=法定年齢以上)
│   ├── geoTargets: GeoTarget[]
│   ├── interests: Interest[]
│   ├── exclusions: Exclusion[]
│   └── retargetingAudiences: Audience[]
├── creatives: AdCreative[] [Entity]
│   ├── creativeId: CreativeId
│   ├── format: AdFormat
│   ├── assets: MediaAsset[]
│   ├── responsibleDrinkingMessage: ResponsibleDrinkingMessage
│   └── approvalStatus: CreativeApprovalStatus
├── placements: Placement[] [Entity]
│   ├── channel: AdChannel
│   ├── placementType: PlacementType
│   └── brandSafetySettings: BrandSafetySettings
├── performance: CampaignPerformance [Entity]
│   ├── impressions: number
│   ├── clicks: number
│   ├── conversions: number
│   ├── ctr: Percentage
│   ├── cvr: Percentage
│   ├── cpa: Money
│   └── roas: Percentage
├── complianceCheck: AdComplianceCheck [Entity]
│   ├── ageTargetingCompliant: boolean
│   ├── placementCompliant: boolean
│   ├── creativeCompliant: boolean
│   └── brandSafetyCompliant: boolean
├── status: CampaignStatus [Value Object]
│   └── value: enum (DRAFT, PENDING_APPROVAL, ACTIVE, PAUSED, COMPLETED)
└── audit: AuditTrail [Value Object]
```

**不変条件:**
| 不変条件 | 説明 |
|----------|------|
| INV-DAC-01 | ACTIVE状態には全complianceCheck項目がtrue |
| INV-DAC-02 | targeting.ageRange.minAgeは法定飲酒年齢以上 |
| INV-DAC-03 | budget.spentはbudget.totalBudgetを超過不可 |
| INV-DAC-04 | 全creativesにresponsibleDrinkingMessageが必須 |
| INV-DAC-05 | brandSafetySettingsは必須 |

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **SocialContentPublished** | {contentId, accountId, platform, publishedAt} | SNSコンテンツ公開時 | marketing-analytics, consumer-engagement |
| **ContentEngagementUpdated** | {contentId, impressions, reach, engagements, updatedAt} | エンゲージメント更新時 | marketing-analytics |
| **InfluencerPartnershipStarted** | {influencerId, campaignId, startDate, contractValue} | インフルエンサー施策開始時 | marketing-analytics, campaign-communications |
| **InfluencerContentApproved** | {influencerId, contentId, approvedAt} | インフルエンサーコンテンツ承認時 | brand-asset-governance |
| **AdCampaignLaunched** | {campaignId, brandId, objective, budget, startDate} | 広告キャンペーン開始時 | marketing-analytics |
| **AdCampaignCompleted** | {campaignId, performance, endDate} | 広告キャンペーン終了時 | marketing-analytics, brand-strategy |
| **KeywordRankingChanged** | {keywordId, previousPosition, newPosition, date} | キーワード順位変動時 | marketing-analytics |
| **ECConversionRecorded** | {campaignId, orderId, revenue, attributionSource} | EC売上計上時 | marketing-analytics, VS4 |
| **ComplianceViolationDetected** | {entityType, entityId, violationType, severity, detectedAt} | コンプライアンス違反検出時 | brand-asset-governance, リスク管理 |

---

### 6. コンテキストマップ（Context Map）

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    │   brand-strategy-bc                  │
                    │        (Upstream)                    │
                    │   グローバルブランド戦略提供          │
                    └──────────────┬───────────────────────┘
                                   │ ブランドメッセージ・方針
                                   ▼
┌─────────────────┐    ┌──────────────────────────────────┐    ┌─────────────────┐
│ campaign-       │    │                                  │    │ marketing-      │
│ communications- │◄──►│  digital-marketing-bc            │───►│ analytics-bc    │
│ bc              │    │                                  │    │ (Downstream)    │
│ (Partnership)   │    │                                  │    │                 │
│ キャンペーン連携 │    └──────────────┬───────────────────┘    │ KPIデータ提供   │
└─────────────────┘                   │                        └─────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ brand-asset-    │    │ consumer-       │    │ VS4:            │
│ governance-bc   │    │ engagement-bc   │    │ sales-          │
│ (Upstream)      │    │ (Downstream)    │    │ distribution    │
│                 │    │                 │    │ (Partnership)   │
│ ブランド資産提供 │    │ 接点データ受領   │    │ EC連動          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                      │
                                      │
                                      ▼
                       ┌─────────────────┐
                       │ VS2:            │
                       │ product-        │
                       │ innovation      │
                       │ (Upstream)      │
                       │ 製品情報受領    │
                       └─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| brand-strategy-bc | **Customer-Supplier** | ブランドメッセージ・方針の供給を受ける |
| campaign-communications-bc | **Partnership** | キャンペーン連携で対等に協力 |
| brand-asset-governance-bc | **Customer-Supplier** | ブランド資産・ガイドラインの供給を受ける |
| consumer-engagement-bc | **Customer-Supplier** | デジタル接点データを提供する |
| marketing-analytics-bc | **Customer-Supplier** | デジタルKPIデータを提供する |
| VS4 sales-distribution | **Partnership** | EC連動施策で対等に協力 |
| VS2 product-innovation | **Customer-Supplier** | 製品情報・ストーリーの供給を受ける |

#### 外部システム連携

| 外部システム | 連携タイプ | 説明 |
|-------------|-----------|------|
| SNSプラットフォームAPI | ACL (Anti-Corruption Layer) | Instagram Graph API, X API, TikTok API等 |
| Google Ads / Meta Ads | ACL | 広告配信・レポーティング |
| Google Analytics / Adobe Analytics | ACL | Web分析データ |
| DSP/SSP | ACL | プログラマティック広告配信 |
| ECプラットフォーム | ACL | 楽天、Amazon等のAPI連携 |
| インフルエンサープラットフォーム | ACL | HYSTA、Klear等 |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/social-accounts` | POST | SNSアカウント登録 |
| `/social-contents` | POST | SNSコンテンツ作成 |
| `/social-contents/{id}/submit-review` | POST | コンテンツレビュー提出 |
| `/social-contents/{id}/approve` | POST | コンテンツ承認 |
| `/social-contents/{id}/publish` | POST | コンテンツ公開 |
| `/seo-keywords` | POST | キーワード登録 |
| `/seo-keywords/{id}/update-ranking` | POST | ランキング更新 |
| `/influencers` | POST | インフルエンサー登録 |
| `/influencers/{id}/approve` | POST | インフルエンサー承認 |
| `/influencer-partnerships` | POST | パートナーシップ作成 |
| `/ad-campaigns` | POST | 広告キャンペーン作成 |
| `/ad-campaigns/{id}/launch` | POST | キャンペーン開始 |
| `/ad-campaigns/{id}/pause` | POST | キャンペーン一時停止 |
| `/ad-campaigns/{id}/update-performance` | POST | パフォーマンス更新 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/social-accounts` | GET | SNSアカウント一覧 |
| `/social-accounts/{id}` | GET | SNSアカウント詳細 |
| `/social-contents` | GET | コンテンツ一覧（フィルタ可） |
| `/social-contents/{id}` | GET | コンテンツ詳細 |
| `/social-contents/{id}/performance` | GET | コンテンツパフォーマンス |
| `/seo-keywords` | GET | キーワード一覧 |
| `/seo-keywords/{id}/rankings` | GET | ランキング履歴 |
| `/influencers` | GET | インフルエンサー一覧 |
| `/influencers/{id}` | GET | インフルエンサー詳細 |
| `/ad-campaigns` | GET | キャンペーン一覧 |
| `/ad-campaigns/{id}` | GET | キャンペーン詳細 |
| `/ad-campaigns/{id}/performance` | GET | キャンペーンパフォーマンス |
| `/digital-kpi/summary` | GET | デジタルKPIサマリー |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| brand-strategy-bc | ブランドメッセージ・方針取得 |
| brand-asset-governance-bc | ブランド資産・ガイドライン取得 |
| campaign-communications-bc | キャンペーン情報取得 |
| VS2 product-innovation | 製品情報取得 |
| VS4 sales-distribution | EC在庫・販売情報取得 |

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（digital-marketing-bc定義）
