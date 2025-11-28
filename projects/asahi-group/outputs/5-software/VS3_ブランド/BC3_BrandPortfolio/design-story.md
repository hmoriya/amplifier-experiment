# BC3: Brand Portfolio - 設計ストーリー

## 概要

このドキュメントはBC3 Brand Portfolioの設計判断理由を記録します。
チーム全員が設計の背景を理解し、将来の変更時に意図を維持するための資料です。

---

## 1. アーキテクチャスタイルの設計判断

### なぜModular Monolithを採用したか

```
判断理由:
1. ドメインの特性
   - Brand、Campaign、MarketPresenceは密接に関連
   - リアルタイムの整合性が重要（キャンペーンはブランド情報を即時参照）
   - トランザクション境界が明確

2. チーム構成
   - BC3は単一チームで管理
   - マイクロサービス分割のオーバーヘッドが見合わない
   - 将来の分離可能性は維持

3. 性能要件
   - ブランド情報の頻繁な参照
   - キャンペーン一覧表示の高速化
   - モジュール内結合でレイテンシ最小化

4. 運用簡素化
   - デプロイ単位が1つで運用負荷軽減
   - 監視・ログ管理がシンプル
   - 開発環境構築が容易
```

**モジュール分割の設計：**

```
Global Brand Module:
  - グローバルブランドの管理
  - ブランドアイデンティティ、ガイドライン
  - ブランド階層（Master/Sub/Endorsed）

Local Brand Module:
  - ローカライズされたブランド情報
  - 市場別適応（言語、文化、規制）
  - MarketPresence管理

Campaign Planning Module:
  - キャンペーン企画・承認
  - 予算・KPI管理
  - クリエイティブ管理

モジュール間通信:
  - 内部イベントバス（同期）
  - 共有データベース（PostgreSQL）
  - Redisキャッシュで読み取り最適化
```

---

## 2. Aggregate境界の設計判断

### Brand Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. ブランドエクイティの中核
   - ブランドは企業の最重要資産
   - アイデンティティ、ガイドライン、アセットが一体
   - ブランド価値の毀損防止が最優先

2. 階層構造の管理
   - Master → Sub → Product の階層
   - parentBrandIdによる親子関係
   - 階層全体での整合性維持

3. 承認ワークフロー
   - ガイドライン変更は承認制
   - ブランド全体が承認単位
   - 部分的な変更も影響範囲を考慮

4. ドメインエキスパートの言語
   - マーケターは「ブランド」を統合的に管理
   - 「スーパードライのガイドラインを更新」が自然な操作
```

**BrandIdentityをEntityにした理由：**

```
判断:
- アイデンティティは複雑なネスト構造
  - mission, vision, values, personality, positioning, tagline
- 全体更新より部分更新が多い
- 変更履歴を詳細に追跡したい
→ Entity として配置し、更新を明示化

なぜValue Objectでないか:
- 頻繁な部分更新がある
- 変更のたびに全置換は非効率
- 各フィールドの変更履歴が必要
```

**BrandGuidelinesをEntityにした理由：**

```
判断:
- ガイドラインは独立した承認フローを持つ
- バージョン管理が必要
- VisualIdentity、VoiceTone、Messagingの個別更新
→ Entity として配置

ガイドライン公開フロー:
1. ドラフト作成
2. レビュー（デザインチーム）
3. 承認（ブランドマネージャー）
4. 公開（BrandGuidelinesPublishedイベント発行）
```

**BrandAssetをEntityにした理由：**

```
判断:
- アセット（ロゴ、画像、動画）は個別管理
- 追加・削除が頻繁
- 有効期限（expiresAt）による自動無効化
- assetIdで個別参照が必要

設計選択:
- assets: List<BrandAsset> として保持
- アセット数が増えた場合のパフォーマンス懸念
  → 別テーブルに格納、遅延ロード対応
```

### Campaign Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. 独立したライフサイクル
   - キャンペーンはブランドとは別に作成・終了
   - Draft → Planning → Approved → InExecution → Completed
   - 各段階で異なるステークホルダーが関与

2. 予算管理の単位
   - キャンペーン単位で予算承認
   - チャネル配分はキャンペーン内で完結
   - 予算超過チェックはキャンペーン境界で実施

3. 承認ワークフロー
   - キャンペーン全体が承認対象
   - ブリーフ、予算、KPIが揃って承認
   - 部分承認はない

4. 効果測定の単位
   - キャンペーン単位でROI計算
   - KPI達成度評価
   - レポーティングの基本単位
```

**CampaignBriefをEntityにした理由：**

```
判断:
- ブリーフは企画の核心
- 背景、課題、機会、キーメッセージ、方向性
- ブリーフ単体での更新・レビューがある
→ Entity として独立管理

ブリーフ作成フロー:
1. プランナーがドラフト作成
2. ブランドマネージャーレビュー
3. クリエイティブチームへ共有
4. 必要に応じて修正サイクル
```

**CreativeをEntityにした理由：**

```
判断:
- クリエイティブは個別に制作・承認
- チャネルごとに異なるフォーマット
- 制作状況のステータス追跡
- creativeIdで個別参照が必要

Creative承認フロー:
1. 制作（Draft）
2. 内部レビュー（UnderReview）
3. 法務チェック（LegalReview）
4. 最終承認（Approved）
5. 配信（Deployed）
```

### MarketPresence Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. 市場単位の管理
   - 同一ブランドでも市場ごとに異なる展開
   - ローカライズ情報は市場固有
   - 実績データは市場単位で記録

2. 独立したライフサイクル
   - ブランドが存在しても特定市場に未展開
   - 市場参入・撤退はブランドとは別判断
   - 市場ごとの競合状況は独立して変化

3. パフォーマンスデータの帰属
   - 売上、シェア、認知度は市場単位
   - 市場間比較のための独立データ構造
```

**代替案と却下理由：**

```
却下案1: Brand Aggregate内にmarkets: List<MarketPresence>
  → 問題: ブランド更新のたびに全市場データがロード
  → 問題: 市場データの独立更新が複雑化
  → 決定: 別Aggregateとし、brandId + marketIdで参照

却下案2: 市場マスターを別BCとして独立
  → 問題: BC間通信のオーバーヘッド
  → 問題: 単純な参照のためにイベント連携は過剰
  → 決定: BC3内のAggregateとして配置
```

---

## 3. Value Object選択の設計判断

### なぜValue Objectにしたか

| Value Object | 選択理由 |
|--------------|----------|
| BrandCode | フォーマット（BRD-{Region}-{Type}-NNN）を値が保証。等価性比較。変更時は新コード発行。 |
| BrandPersonality | traits + archetypes + toneOfVoice の組み合わせ。全体として意味を持つ。パーソナリティ間の比較が必要。 |
| ColorSpec | hex/rgb/cmyk/pantone の変換可能な色仕様。不変で、同じ色は等価。 |
| Budget | totalAmount + allocation + contingency。予算全体として整合性検証。部分更新は全置換で。 |
| Money | amount + currency の組み合わせ。通貨演算（加算、比較）が必要。 |
| TargetAudience | demographics + psychographics + behaviors。ターゲット定義は全体で意味を持つ。 |

### BrandTypeをEnumにした理由

```yaml
Values: [Corporate, Master, Sub, Product, Endorsed]

判断:
- ブランドアーキテクチャの標準分類
- 各タイプで異なるビジネスルール適用
  - Corporate: 企業ブランド、最上位
  - Master: 製品カテゴリブランド
  - Sub: マスター配下のサブブランド
  - Product: 個別製品ブランド
  - Endorsed: 独立しつつ親の支持を受けるブランド
- 追加は稀（ブランド戦略変更時のみ）
```

### BrandScopeをEnumにした理由

```yaml
Values: [Global, Regional, Local]

判断:
- 展開範囲の3階層分類
- Global: 全世界共通ブランド（例: Asahi Super Dry）
- Regional: 地域限定（例: アジア限定）
- Local: 国別限定（例: 日本限定）
- 明確な分類で管理しやすさ優先
```

### CampaignStatusの状態遷移設計

```yaml
Draft → Planning (start planning)
Planning → Approved (approve)
Planning → Draft (reject)
Approved → InExecution (launch)
InExecution → Completed (complete)
InExecution → Cancelled (cancel)
Planning → Cancelled (cancel)
```

**設計判断：**

```
1. Planning状態の追加
   - 単なるDraftと企画中を区別
   - Planning中に予算・KPI・タイムライン設定
   - チーム作業の可視化

2. InExecution中のキャンセル許可
   - 市場環境変化への対応
   - 不測の事態（危機管理）
   - ただしキャンセル理由は必須記録

3. Completedへの直接遷移のみ
   - 完了後の再開はない
   - 継続が必要なら新規キャンペーン作成
```

---

## 4. API設計の設計判断

### エンドポイント構造

```yaml
設計原則:
  RESTful: リソース指向
  階層表現: ブランド→キャンペーン→クリエイティブ
  フィルタリング: クエリパラメータで柔軟に
```

### /brands エンドポイント設計

```
GET /brands
  設計理由:
  - 全ブランド一覧（ポートフォリオビュー）
  - フィルタ: type, scope, status, parentBrandId
  - ページネーション必須（大規模ポートフォリオ対応）

GET /brands/{brandId}
  設計理由:
  - ブランド詳細（identity, guidelines含む）
  - expand パラメータで関連データ制御
    - ?expand=assets,markets,children

POST /brands
  設計理由:
  - 最小限の必須項目（name, brandType, scope）
  - identity, guidelinesは後から設定
  - 親ブランド指定はオプション

PUT /brands/{brandId}/identity
PUT /brands/{brandId}/guidelines
  設計理由:
  - セクション単位の更新を明示化
  - 監査ログで「何を変更したか」が明確
  - ガイドライン更新は承認フロー連携
```

### /brands/{brandId}/campaigns エンドポイント設計

```
GET /brands/{brandId}/campaigns
  設計理由:
  - ブランド別キャンペーン一覧
  - 階層的なURL構造で所属関係を明示
  - フィルタ: status, dateRange

POST /brands/{brandId}/campaigns
  設計理由:
  - キャンペーン作成時にブランド紐付け必須
  - URLでブランドIDを指定し、ボディ簡素化
  - 作成後のブランド変更は不可
```

### キャンペーン承認API設計

```
POST /campaigns/{campaignId}/submit
POST /campaigns/{campaignId}/approve
POST /campaigns/{campaignId}/reject
  設計理由:
  - BC2と同様のパターン（一貫性）
  - 状態遷移をビジネスアクションとして明示
  - 各アクションで権限・バリデーション実行

POST /campaigns/{campaignId}/launch
POST /campaigns/{campaignId}/complete
  設計理由:
  - 実行開始・終了も明示的アクション
  - launch時にInExecution遷移 + 関連通知
  - complete時にCampaignCompletedイベント発行
```

### 市場プレゼンスAPI設計

```
GET /brands/{brandId}/markets
  設計理由:
  - ブランドの展開市場一覧
  - MarketPresence情報を含む

POST /brands/{brandId}/markets
  設計理由:
  - 新規市場展開
  - localBrandName, localizationを設定
  - BrandExpandedToMarketイベント発行

PUT /brands/{brandId}/markets/{marketId}
  設計理由:
  - 市場固有情報の更新
  - performance, competitorsの更新
```

---

## 5. インデックス設計の設計判断

### Brandインデックス

```sql
-- 主要検索パターンとインデックス
idx_brands_code             -- コード検索（一意）
idx_brands_type             -- タイプ別一覧（Corporate, Master等）
idx_brands_scope            -- 展開範囲別（Global, Regional, Local）
idx_brands_status           -- ステータス別（Active, Archived等）
idx_brands_parent           -- 子ブランド取得
idx_brands_name_fulltext    -- ブランド名検索（全文）
```

**ブランド階層検索の判断：**

```
検索パターン:
- 「スーパードライの子ブランド一覧」
- 「グローバルブランドとその配下一覧」

設計:
- parentBrandIdにインデックス
- 再帰クエリ（WITH RECURSIVE）で階層取得
- 深さ制限（通常3階層まで）
→ 初期は再帰クエリ、データ増加でネストセットモデル検討
```

### Campaignインデックス

```sql
idx_campaigns_code          -- コード検索
idx_campaigns_brand         -- ブランド別キャンペーン
idx_campaigns_status        -- ステータス別
idx_campaigns_date          -- 期間検索（launchDate, endDate）
idx_campaigns_brand_status  -- 複合（ブランド + ステータス）
```

**日付範囲検索の判断：**

```
検索パターン:
- 「今月実行中のキャンペーン」
- 「来月開始予定のキャンペーン」
- 「過去1年のキャンペーン実績」

設計:
- launchDate, endDateにBtreeインデックス
- 範囲検索の最適化
- 複合インデックス（status + launchDate）で
  「実行中かつ特定期間」を高速化
```

### MarketPresenceインデックス

```sql
idx_presence_brand          -- ブランド別市場一覧
idx_presence_market         -- 市場別ブランド一覧
idx_presence_brand_market   -- 複合（一意制約）
idx_presence_performance    -- GIN（JSONBの実績データ検索）
```

**市場実績検索の判断：**

```
検索パターン:
- 「日本市場でシェア10%以上のブランド」
- 「認知度が前年比上昇したブランド」

設計:
- performance（JSONB）にGINインデックス
- 数値範囲検索に対応
- 集計クエリはマテリアライズドビュー検討
```

---

## 6. ドメインサービス設計判断

### BrandManagementServiceの配置

```
判断:
- ポートフォリオ全体の分析
- 複数ブランドの比較・評価
- 単一Aggregateに属さない横断機能
→ ドメインサービスとして配置

提供機能:
1. ポートフォリオ概要（getPortfolioOverview）
   - グローバル/リージョナル/ローカル別集計
   - ポートフォリオ健全性スコア

2. ブランド階層分析（analyzeBrandHierarchy）
   - 親子関係の可視化
   - シナジー機会の特定

3. ブランドヘルス評価（evaluateBrandHealth）
   - 認知度、選好度、ロイヤルティの総合評価
   - 改善提案の生成
```

### CampaignPlanningServiceの配置

```
判断:
- キャンペーン企画支援は複数情報源を参照
  - ブランドガイドライン
  - 過去のキャンペーン実績
  - 市場データ
- 予測・最適化ロジックを集約
→ ドメインサービス

提供機能:
1. ブリーフ生成支援（generateCampaignBrief）
   - ブランド情報からテンプレート生成
   - 過去の成功ブリーフパターン参照

2. チャネルミックス最適化（optimizeChannelMix）
   - 予算とターゲットから配分提案
   - ROI予測モデル適用

3. パフォーマンス予測（forecastCampaignPerformance）
   - 過去データからKPI予測
   - リスク要因の特定
```

### BrandGuidelineServiceの配置

```
判断:
- ガイドライン取得は市場別ローカライズ対応
- アセットコンプライアンスチェック
- スタイルガイド生成
→ ドメインサービス

提供機能:
1. ガイドライン取得（getBrandGuidelines）
   - 市場指定でローカライズ版取得
   - アセット一覧を含む

2. コンプライアンス検証（validateAssetCompliance）
   - 制作物がガイドライン準拠か検証
   - 違反箇所と修正提案

3. スタイルガイド生成（generateStyleGuide）
   - PDF/HTML形式でガイドブック出力
   - 外部パートナー向け配布用
```

---

## 7. VS間イベント連携の設計判断

### VS2 → VS3 イベント受信

| イベント | 処理内容 | 設計判断 |
|----------|----------|----------|
| ProductApproved | 製品情報の取り込み | 新製品のマーケティング準備開始 |

**イベント処理方針：**

```
ProductApproved受信時:
1. 製品情報をローカルキャッシュに保存
2. 関連ブランドを特定（brandIdまたはマッチング）
3. マーケティングポイントを取り込み
4. キャンペーン企画の参考情報として蓄積

設計判断:
- 自動的なキャンペーン作成はしない
- 人間（プランナー）の判断を待つ
- 通知で「新製品承認」を知らせる
```

### BC3内部イベント

```yaml
BrandExpandedToMarket:
  目的: 市場展開情報の共有
  購読者:
    - LocalBrandModule: ローカライズ準備
    - CampaignPlanningModule: 市場別キャンペーン検討

CampaignApproved:
  目的: 承認完了の通知
  購読者:
    - クリエイティブチーム: 制作開始
    - メディアチーム: 出稿準備
    - ブランドマネージャー: 進捗確認

CampaignCompleted:
  目的: キャンペーン終了と結果共有
  購読者:
    - 分析チーム: 効果測定
    - 次回企画チーム: 学習・改善
```

---

## 8. キャッシュ戦略の設計判断

### なぜRedisキャッシュを採用したか

```
判断理由:
1. ブランド情報の読み取り頻度
   - キャンペーン企画時に毎回参照
   - ガイドライン取得は高頻度
   - DBアクセス削減が効果的

2. ガイドラインの安定性
   - 更新頻度は低い（月に数回）
   - キャッシュTTLを長く設定可能
   - 更新時にキャッシュ無効化

3. アセットURLのキャッシュ
   - CDN URLは変更されない
   - メタデータをキャッシュ
   - 実ファイルはCDN経由
```

**キャッシュ設計：**

```yaml
brand:{brandId}:
  TTL: 1時間
  内容: Brand Aggregate全体
  無効化: Brand更新時

brand:{brandId}:guidelines:
  TTL: 24時間
  内容: BrandGuidelines
  無効化: ガイドライン更新時

brand:{brandId}:assets:
  TTL: 6時間
  内容: アセット一覧（メタデータ）
  無効化: アセット追加/削除時

campaign:{campaignId}:
  TTL: 30分
  内容: Campaign Aggregate
  無効化: Campaign更新時
```

---

## 9. 設計上の妥協と将来課題

### 現在の妥協

```
1. ブランドアセット管理
   - 現在: BC3内でシンプル管理
   - 理想: DAM（Digital Asset Management）連携
   - 理由: 初期はシンプルに、運用しながら要件明確化

2. キャンペーン効果測定
   - 現在: 手動でKPI実績入力
   - 理想: 広告プラットフォームAPI連携（自動取得）
   - 理由: 連携先が多数、段階的に対応

3. ブランドヘルス評価
   - 現在: 基本指標（認知度、選好度）
   - 理想: 高度な分析（因子分析、クラスター分析）
   - 理由: データ蓄積後に分析機能拡充
```

### 将来の拡張ポイント

```
1. DAM連携
   - Adobe Experience Manager等との連携
   - アセット承認ワークフロー統合
   - → BrandAssetの参照先を外部DAMに変更

2. マーケティングオートメーション
   - キャンペーン実行の自動化
   - ターゲティング・パーソナライゼーション
   - → Campaign Aggregateの拡張

3. AI活用
   - ブリーフ自動生成
   - クリエイティブ提案
   - パフォーマンス予測精度向上
   - → ドメインサービスへのML統合

4. マイクロサービス分割
   - 将来的にCampaignを独立サービス化
   - GlobalBrand / LocalBrandの分離
   - → モジュール境界を維持しておく重要性
```

---

**作成日**: 2025-11-28
**VS**: VS3 ブランド・マーケティング
**BC**: BC3 Brand Portfolio
**参照**: domain-language.md, api-specification.md, database-design.md
