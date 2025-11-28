# ADR-004: Database per Serviceパターン

## ステータス

**承認済み** (2025-11-27)

## コンテキスト

マイクロサービス化に伴い、データストアの管理方針を決定する必要がある。

**選択肢:**
1. Shared Database: 全サービスが1つのデータベースを共有
2. Database per Service: 各サービスが専用のデータベースを所有

**要件:**
- データの所有権を明確化
- サービス間の疎結合
- 独立したスキーマ変更
- 適切なデータ分離（セキュリティ）

## 決定

**Database per Serviceパターンを採用する。**

各サービスは専用のデータベース（スキーマ）を所有し、他サービスのデータには直接アクセスしない。

構成:
- 各サービス: 専用PostgreSQLスキーマ
- 必要に応じて: MongoDB（ドキュメント）、Elasticsearch（検索）

```
fermentation-research-service → fermentation_research (PostgreSQL)
ingredient-research-service   → ingredient_research (PostgreSQL)
beer-development-service      → beer_development (PostgreSQL + Elasticsearch)
spirits-development-service   → spirits_development (PostgreSQL)
beverage-development-service  → beverage_development (PostgreSQL)
rnd-support-service           → rnd_support (PostgreSQL)
process-engineering-service   → process_engineering (PostgreSQL)
```

## 結果

### 良い影響

1. **疎結合**: サービス間のデータ依存がなく、独立して変更可能。
2. **所有権の明確化**: 各サービスが自身のデータに責任を持つ。
3. **独立したスキーマ変更**: 他サービスに影響なくスキーマ変更可能。
4. **技術選択の自由**: サービスごとに最適なデータストアを選択可能。
5. **スケーラビリティ**: 負荷の高いサービスのDBのみスケールアップ可能。

### 悪い影響/トレードオフ

1. **データ重複**: 同じデータが複数サービスに存在する可能性。
   - 対策: 明確なデータオーナーシップ、イベントによる同期
2. **結合クエリの困難**: 複数サービスのデータを結合するクエリが困難。
   - 対策: CQRS、読み取り専用ビューの構築
3. **分散トランザクション**: ACIDトランザクションが困難。
   - 対策: Sagaパターン、最終的整合性の受容
4. **運用コスト**: 複数データベースの管理が必要。

### リスク

1. **データ整合性**: サービス間のデータ不整合。
   - 対策: イベント駆動による同期、監視・アラート
2. **パフォーマンス**: サービス間データ取得のオーバーヘッド。
   - 対策: gRPC、キャッシング、データプリフェッチ

## 代替案

### 代替案1: Shared Database

**評価:**
- メリット: 結合クエリが容易、トランザクション管理が簡単
- デメリット: サービス間の結合度が高い、スキーマ変更の影響大
- 判断: マイクロサービスの利点を損なう

### 代替案2: Schema per Service（同一インスタンス）

**評価:**
- メリット: 運用コスト低減、リソース共有
- デメリット: リソース競合、障害影響範囲が広い
- 判断: 初期フェーズでは許容。将来的に分離を検討。

**採用:** 初期フェーズでは同一PostgreSQLインスタンス上に複数スキーマを作成。
負荷増加時に物理的に分離。

## データアクセスルール

```yaml
ルール:
  1. 自サービスのデータのみ直接アクセス可能
  2. 他サービスのデータはAPI経由でアクセス
  3. 読み取り専用のデータ複製は許可（イベント経由で同期）
  4. 共有データはShared Kernelとして明示的に管理

例外:
  - 分析・レポート用途: 読み取り専用レプリカへのアクセス許可
  - 監査ログ: 全サービスから集中ログDBへの書き込み
```

## 関連

- ADR-001: マイクロサービスアーキテクチャの採用
- ADR-002: イベントバスとしてKafkaを選択
- service-boundaries.md
- context-map.md (Shared Kernel定義)

---

**作成者:** Claude (Parasol V5)
**作成日:** 2025-11-27
