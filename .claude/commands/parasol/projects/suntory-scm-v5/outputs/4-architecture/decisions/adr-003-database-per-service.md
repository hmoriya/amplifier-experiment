# ADR-003: Database per Service パターンの採用

## ステータス
承認済み（2025-01-15）

## コンテキスト

マイクロサービスアーキテクチャにおいて、データストア戦略の決定が必要。以下の要件を考慮：

1. **データ所有権の明確化**: 各サービスが自身のデータを完全に所有
2. **独立したスキーマ進化**: サービスごとに独立してスキーマを変更可能
3. **異なるデータ特性**:
   - 受注データ: トランザクション指向、強整合性
   - 時系列データ: 水使用量、温度ログ
   - 分析データ: CO2計算、長期トレンド
   - グラフデータ: トレーサビリティの関係追跡

## 決定

**Database per Service パターンを採用し、各サービスが専用のデータストアを所有する。**

### データベース選定

| サービス | プライマリDB | 補助ストア | 選定理由 |
|---------|-------------|-----------|---------|
| Order Service | PostgreSQL | Redis (キャッシュ) | トランザクション、EDI連携 |
| Demand Planning Service | PostgreSQL | Redis (予測キャッシュ) | 分析クエリ、ML連携 |
| Transport Planning Service | PostgreSQL | Redis (ルートキャッシュ) | 地理空間クエリ |
| Warehouse Service | PostgreSQL | Redis (在庫キャッシュ) | 在庫トランザクション |
| Food Safety Service | PostgreSQL + TimescaleDB | S3 (監査アーカイブ) | 時系列温度データ |
| Traceability Service | PostgreSQL | Neo4j (オプション) | グラフ関係追跡 |
| Water Sustainability Service | PostgreSQL + TimescaleDB | BigQuery | 時系列水データ |
| Environmental Reporting Service | PostgreSQL | BigQuery/Redshift | 分析・レポート |

### スキーマ分離

```yaml
Schema Isolation:
  Strategy: Separate Database per Service

  # スキーマ命名規則
  Naming:
    order_service: orders_db
    warehouse_service: warehouse_db
    food_safety_service: food_safety_db
    ...

  # 接続情報
  Connection:
    # 各サービスは自身のDB接続情報のみを保持
    # 他サービスのDBへの直接アクセスは禁止
```

### データ共有パターン

```yaml
Data Sharing Patterns:

  # パターン1: API経由（同期）
  Synchronous:
    Use Case: リアルタイムの在庫照会
    Example: Order Service → Warehouse Service API

  # パターン2: イベント経由（非同期）
  Asynchronous:
    Use Case: 在庫更新の通知
    Example: InventoryUpdated event → Kafka → Order Service

  # パターン3: データレプリケーション（CQRS）
  Replication:
    Use Case: レポート用データ集約
    Example: 各サービス → BigQuery (分析用)
```

## 結果

### 良い影響

1. **独立したスキーマ進化**: サービスごとに独立してマイグレーション可能
2. **技術選択の自由度**: TimescaleDB（時系列）、Neo4j（グラフ）等、最適なDBを選択
3. **障害分離**: 1つのDBの障害が他サービスに波及しない
4. **スケーラビリティ**: サービスごとに独立してDBをスケール
5. **セキュリティ**: サービス単位でのアクセス制御が容易

### トレードオフ

1. **データ整合性**: 分散データの整合性管理が必要
   - 軽減策: 結果整合性の採用、Sagaパターン
2. **クエリの複雑化**: 複数サービスのデータを結合するクエリが困難
   - 軽減策: CQRS、データレイクへの集約
3. **運用コスト**: 複数DBの運用・監視が必要
   - 軽減策: マネージドDB（RDS/Cloud SQL）の活用
4. **データ重複**: 一部データの重複が発生
   - 軽減策: イベント駆動での同期、マスタデータ管理

### リスク

1. **分散トランザクション**: 複数DBにまたがるトランザクション管理
   - 軽減策: Saga Choreography パターンの採用（ADR-004）
2. **データ不整合**: イベント処理失敗時のデータ不整合
   - 軽減策: イベントソーシング、補償トランザクション

## 代替案

### 代替案1: 共有データベース
- **メリット**: JOIN可能、トランザクション容易
- **却下理由**: スキーマ結合、独立デプロイ困難、スケーラビリティ制限

### 代替案2: スキーマ分離（同一DB内）
- **メリット**: 運用シンプル、コスト低
- **却下理由**: 障害分離不十分、スケーラビリティ制限

### 代替案3: 全サービスでNoSQL
- **メリット**: スケーラビリティ、柔軟性
- **却下理由**: トランザクション要件、既存スキルセット

## データ整合性パターン

### 結果整合性の採用範囲

```yaml
Strong Consistency:
  - 在庫引当（Warehouse内部）
  - 受注登録（Order内部）
  - HACCP記録（Food Safety内部）

Eventual Consistency:
  - 受注 → 倉庫への出荷指示
  - 品質検査 → トレーサビリティ記録
  - 各サービス → 環境報告への集約
```

### マスタデータ管理

```yaml
Master Data:
  Customer Master:
    Owner: Order Service
    Sync: CustomerUpdated event → 他サービス

  Product Master:
    Owner: Demand Planning Service
    Sync: ProductUpdated event → 他サービス

  Location Master:
    Owner: Warehouse Service
    Sync: LocationUpdated event → 他サービス
```

## 関連

- ADR-001: マイクロサービスアーキテクチャの採用
- ADR-002: イベントバスの選択
- ADR-004: Saga Choreography パターン
- サービス定義: `outputs/4-architecture/services/`

---

**作成者**: Parasol V5 Phase 4
**レビュー者**: データベースチーム、アーキテクチャチーム
