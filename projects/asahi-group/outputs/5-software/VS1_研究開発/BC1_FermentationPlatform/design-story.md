# BC1: Fermentation Platform - 設計ストーリー

## 概要

このドキュメントはBC1 Fermentation Platformの設計判断理由を記録します。
チーム全員が設計の背景を理解し、将来の変更時に意図を維持するための資料です。

---

## 1. Aggregate境界の設計判断

### YeastStrain Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. 独立したライフサイクル
   - 酵母株は独自に登録・管理され、他のエンティティとは独立して存在
   - 研究室で発見・育種された時点から、製品利用、アーカイブまでの
     完全なライフサイクルを持つ

2. 強い整合性境界
   - YeastCharacteristics、FlavorProfile、FermentationProfileは
     酵母株と不可分な特性情報
   - これらの属性は常に酵母株と一緒に更新される必要がある
   - 部分的な更新は酵母株の「アイデンティティ」を損なう

3. トランザクション境界の一致
   - 酵母株の特性更新は単一トランザクションで完結すべき
   - 発酵プロセスや実験との関係は参照（ID）で表現し、
     トランザクション境界を分離

4. ドメインエキスパートの言語との一致
   - 研究者は「酵母株」を独立した管理対象として認識
   - 「ASH-2024-0001の特性を更新する」という操作単位が自然
```

**代替案と却下理由：**

```
却下案1: YeastCharacteristicsを別Aggregateにする
  → 問題: 酵母株と特性の更新が分離され、不整合リスク増大
  → 酵母株の変更なしに特性だけ変更するユースケースがない

却下案2: FlavorProfileを共有カーネルにする
  → 問題: BC2 ProductRecipeでも使用するが、定義責任が曖昧になる
  → 決定: BC1が定義元、BC2はイベント経由で参照（VS間イベント連携）
```

### FermentationProcess Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. プロセス単位の整合性
   - 発酵条件、ステージ進行、測定データは一つのプロセスとして
     整合性を保つ必要がある
   - 温度調整と測定記録が同時に行われるケースあり

2. 時系列データの管理
   - ProcessMeasurementは時系列で蓄積される子エンティティ
   - プロセスと測定データの親子関係は明確
   - 個別の測定データを独立して管理する意味がない

3. StrainIdは参照のみ
   - 使用酵母株は変更されない（プロセス開始時に確定）
   - 酵母株の変更が発酵プロセスに自動伝播する必要はない
   - 弱参照（ID）で十分
```

**FermentationStageをEntityにした理由：**

```
決定理由:
- ステージは順序を持ち、プロセス内で識別される必要がある
- ステージの状態変更（進行・完了）を個別に追跡
- ただし、プロセスなしにステージ単体で意味をなさない
→ Aggregate内のEntityとして定義
```

### ResearchExperiment Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. 実験の独立性
   - 実験は複数の酵母株を使用するが、酵母株とは独立したライフサイクル
   - 実験完了後も結果・発見事項は永続的に参照される

2. 発見事項（ResearchFinding）の所属
   - 発見は実験から生まれるが、実験外でも参照される
   - VS間イベント（BreakthroughDiscovered）で他VSに通知
   → 実験の子エンティティとしつつ、イベントで拡散

3. strainIdsを参照リストにした理由
   - 実験は複数酵母株を比較することが多い
   - 酵母株の変更が実験に影響しない（実験時点のスナップショット的意味）
```

---

## 2. Value Object選択の設計判断

### なぜValue Objectにしたか

| Value Object | 選択理由 |
|--------------|----------|
| StrainCode | 識別のためのコードだが、コード自体に意味がある（フォーマットルール: ASH-YYYY-NNNN）。等価性で比較。変更時は新しいコードを発行。 |
| Temperature | 単位（℃）と精度（0.1）を持つ不変の値。30.0℃と30.0℃は同一。演算（差分計算）が必要。 |
| SpecificGravity | 比重は測定値として不変。範囲制約（0.990-1.200）を値自体が保証。 |
| FlavorProfile | 複数の風味指標の集合体。全体として比較（このプロファイルとあのプロファイルは同じか）。 |
| YeastCharacteristics | 酵母の特性セット。部分更新ではなく全体置換で更新。 |

### StrainOriginをValue Objectにした理由

```
詳細理由:
- 由来情報は「Natural/Bred/Modified/Acquired」+ 採取地 + 日付 + 親株
- これらは酵母株登録時に確定し、変更されない
- source=Naturalで親株ありはビジネスルール違反（Value Object内で検証）
- 別の酵母株でも同じ由来情報なら等価（Natural, 北海道, 2024-01-01）
```

### FlavorLevelをEnumにした理由

```
判断:
- None/VeryLow/Low/Medium/High/VeryHighの6段階固定
- 数値ではなく官能評価の抽象化
- 研究者が使う言葉そのまま（「エステルはHighだ」）
- 順序比較が可能（High > Medium）
```

---

## 3. API設計の設計判断

### エンドポイント構造

```yaml
設計原則:
  RESTful: リソース指向でHTTPメソッドを適切に使用
  一貫性: 全BC共通の命名規則
  発見性: OpenAPI仕様で自己文書化
```

### /strains エンドポイント設計

```
GET /strains
  設計理由:
  - 検索パラメータで柔軟なフィルタリング
  - 風味プロファイル検索は複雑 → /strains/search/by-flavor を別途用意
  - ページネーション必須（数千の酵母株が想定される）

POST /strains
  設計理由:
  - 登録時に必要な最小限の情報のみ必須
  - characteristicsは後から更新可能にし、初期登録を簡素化

PUT /strains/{strainId}/characteristics
PUT /strains/{strainId}/flavor-profile
  設計理由:
  - 部分更新を明示的なエンドポイントで提供
  - 全体PUTではなく、意味のある単位で更新
  - 監査ログで「何を更新したか」が明確
```

### /fermentation-processes エンドポイント設計

```
POST /fermentation-processes/{processId}/measurements
  設計理由:
  - 測定データは頻繁に追加される（1日数回〜数十回）
  - プロセスの子リソースとして位置づけ
  - バルクAPIは提供しない（IoTセンサー連携は別途検討）

POST /fermentation-processes/{processId}/adjust-conditions
  設計理由:
  - 条件調整は「操作」であり、単なるPUT更新ではない
  - 理由（reason）の記録が必須
  - イベントソーシングで履歴追跡
```

### 酵母推薦API設計

```
POST /strains/recommend
  設計理由:
  - GETではなくPOST（検索条件が複雑でボディが必要）
  - 推薦結果にconfidenceScoreを含める
  - 推薦理由（reasoning）を返却し、透明性を確保

  レスポンス設計:
  - recommendations配列 + totalCount
  - 各推薦にmatchScore、matchingPoints、cautionsを含む
  - 研究者が判断に使える情報を提供
```

---

## 4. インデックス設計の設計判断

### YeastStrainインデックス

```sql
-- 主要検索パターンとインデックス
idx_strains_status          -- ステータス別一覧（研究中/検証済み/製造用）
idx_strains_code            -- コード検索（一意、ログ連携）
idx_strains_flavor_profile  -- GINインデックス（JSONB、風味検索）
idx_strains_characteristics -- GINインデックス（JSONB、特性検索）
```

**インデックス判断理由：**

```
風味プロファイル検索:
- 「フルーティさがHigh以上の酵母」などの検索が頻繁
- JSONBのGINインデックスで部分一致検索を高速化
- Btreeでは不可能なクエリパターン

特性検索:
- 「アルコール耐性10%以上」「凝集性がHigh」の組み合わせ検索
- 同様にGINインデックスを採用
```

### FermentationProcessインデックス

```sql
idx_processes_strain        -- 酵母株別プロセス一覧
idx_processes_status_date   -- 複合インデックス（ステータス + 開始日）
idx_measurements_process    -- プロセス別測定データ取得
idx_measurements_timestamp  -- 時系列クエリ最適化
```

**測定データインデックス判断：**

```
時系列分析の要件:
- 特定期間の温度推移グラフ描画
- 異常値検出のためのスキャン
→ timestampインデックス + パーティショニング検討
  （データ量が増えた場合に月別パーティション）

パーティショニング見送り理由:
- 初期フェーズではデータ量が限定的
- 複雑さを避け、必要時に追加
```

### ResearchExperimentインデックス

```sql
idx_experiments_researcher  -- 研究者別実験一覧
idx_experiments_strains     -- 酵母株使用実験（GIN、配列）
idx_findings_significance   -- 重要発見のフィルタリング
idx_findings_fulltext       -- 発見内容の全文検索
```

**全文検索判断：**

```
発見事項の検索要件:
- 「エステル生成」に関連する発見を探す
- 過去の類似研究を参照

採用技術:
- PostgreSQL ts_vector（日本語対応にはpg_bigm追加）
- 初期はLIKE検索、データ増加で全文検索移行
```

---

## 5. ドメインサービス設計判断

### YeastRecommendationServiceの配置

```
判断:
- 推薦ロジックは複数の酵母株を横断的に比較
- 単一のYeastStrain Aggregateに属さない
→ ドメインサービスとして配置

アルゴリズム設計:
1. 風味プロファイルマッチング（類似度計算）
2. 発酵条件適合性チェック
3. 過去の成功実績重み付け
4. 総合スコアでランキング

将来拡張:
- 機械学習モデルの導入（現在は決定論的アルゴリズム）
- モデルは別サービスとし、このサービスがオーケストレーション
```

### FermentationOptimizationServiceの配置

```
判断:
- 条件最適化は酵母株情報 + 過去の発酵データを使用
- 複数Aggregateを参照するが、どれも変更しない
→ 読み取り専用ドメインサービス

予測モデル:
- 現在: 過去データの統計分析（平均、標準偏差）
- 将来: 時系列予測モデル（Prophet等）
- インターフェースを抽象化し、実装差し替え可能に
```

---

## 6. VS間イベント連携の設計判断

### VS1 → VS2 イベント

| イベント | 目的 | 設計判断 |
|----------|------|----------|
| YeastStrainOptimized | 製品レシピでの利用可能通知 | 酵母特性改善時、レシピ側で再評価の機会 |
| YeastStrainValidated | 製造用酵母として承認通知 | 新規酵母がレシピ開発で使用可能になった |
| BreakthroughDiscovered | 画期的発見の共有 | 新しい可能性をイノベーションチームに通知 |

**イベント設計判断：**

```
なぜイベント駆動か:
1. VS間の疎結合維持
   - VS1はVS2の内部を知らない
   - 「通知」のみで、後続処理はVS2の責任

2. 最終整合性の許容
   - 酵母検証完了 → レシピへの反映は数分遅れてOK
   - 厳密な同期は不要、業務的にも許容範囲

3. 監査証跡
   - イベントログで「いつ、何が通知されたか」が追跡可能
   - トラブル時の調査に有用
```

---

## 7. 設計上の妥協と将来課題

### 現在の妥協

```
1. 測定データの格納
   - 現在: PostgreSQL JSONB
   - 理想: 時系列DB（InfluxDB等）
   - 理由: 初期はPostgreSQL統一で運用簡素化

2. 推薦アルゴリズム
   - 現在: ルールベース
   - 理想: 機械学習
   - 理由: データ蓄積後に導入予定

3. 検索機能
   - 現在: PostgreSQL LIKE + GIN
   - 理想: Elasticsearch
   - 理由: 検索量が増えてから検討
```

### 将来の拡張ポイント

```
1. IoTセンサー連携
   - 測定データの自動取得
   - リアルタイムモニタリング
   - → APIはバルク対応を追加予定

2. 機械学習統合
   - 推薦精度向上
   - 異常検知
   - → MLサービスとの連携インターフェース準備

3. 系統解析
   - 酵母株の系統樹可視化
   - 遺伝子情報との連携
   - → StrainOrigin.parentStrainIdsの拡張
```

---

**作成日**: 2025-11-28
**VS**: VS1 研究開発
**BC**: BC1 Fermentation Platform
**参照**: domain-language.md, api-specification.md, database-design.md
