# ADR-004: Saga Choreography パターンの採用

## ステータス
承認済み（2025-01-15）

## コンテキスト

マイクロサービスアーキテクチャにおいて、複数サービスにまたがる長時間トランザクション（出荷処理など）の管理が必要。

### 要件

1. **出荷処理フロー**: 受注確定 → 在庫引当 → 配車割当 → 品質検査 → トレーサビリティ記録 → 出荷完了
2. **失敗時の補償**: 途中で失敗した場合、前のステップを巻き戻す
3. **可視性**: 各ステップの進捗を追跡可能
4. **疎結合**: サービス間の依存を最小化

### 分散トランザクションの課題

- 2PC（Two-Phase Commit）は可用性を犠牲にする
- 長時間ロックはスループットを低下させる
- 複数のマイクロサービス間でACIDトランザクションは現実的でない

## 決定

**Saga パターン（Choreography方式）を採用する。**

### Shipment_Saga の設計

```yaml
Shipment_Saga:
  Description: 出荷処理のサービス間協調
  Pattern: Choreography (Event-Driven)

  Steps:
    Step1:
      Service: Order Service
      Action: ShipmentOrderCreated（出荷指示作成）
      Trigger: OrderConfirmed + InventoryAllocated + DeliveryAssigned
      Compensation: CancelShipmentOrder（出荷指示取消）

    Step2:
      Service: Warehouse Service
      Action: InventoryAllocated（在庫引当完了）
      Trigger: ShipmentOrderCreated
      Compensation: ReleaseInventory（在庫引当解除）

    Step3:
      Service: Transport Planning Service
      Action: DeliveryAssigned（配車割当完了）
      Trigger: InventoryAllocated
      Compensation: ReleaseDeliverySlot（配車枠解放）

    Step4:
      Service: Food Safety Service
      Action: QualityApproved（品質承認完了）
      Trigger: InventoryAllocated
      Compensation: MarkAsNotShipped（未出荷マーク）

    Step5:
      Service: Traceability Service
      Action: LotTraceRecorded（ロット追跡記録完了）
      Trigger: QualityApproved
      Compensation: DeleteLotTrace（追跡記録削除）

    Step6:
      Service: Warehouse Service
      Action: ShipmentCompleted（出荷完了）
      Trigger: QualityApproved + LotTraceRecorded + DeliveryAssigned
      Compensation: ReverseShipment（出荷取消）
```

### イベントフロー図

```
┌─────────────┐    ShipmentOrderCreated    ┌─────────────────┐
│   Order     │ ─────────────────────────► │   Warehouse     │
│   Service   │                            │   Service       │
└─────────────┘                            └────────┬────────┘
                                                    │
                                           InventoryAllocated
                                                    │
                    ┌───────────────────────────────┼───────────────────────────────┐
                    ▼                               ▼                               ▼
          ┌─────────────────┐            ┌─────────────────┐              ┌─────────────────┐
          │   Transport     │            │   Food Safety   │              │   Traceability  │
          │   Planning      │            │   Service       │              │   Service       │
          └────────┬────────┘            └────────┬────────┘              └────────┬────────┘
                   │                              │                                │
           DeliveryAssigned               QualityApproved                  LotTraceRecorded
                   │                              │                                │
                   └──────────────────────────────┼────────────────────────────────┘
                                                  ▼
                                         ┌─────────────────┐
                                         │   Warehouse     │
                                         │   Service       │
                                         └────────┬────────┘
                                                  │
                                          ShipmentCompleted
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │   Order         │
                                         │   Service       │
                                         └─────────────────┘
```

### 補償トランザクションの実行

```yaml
Compensation_Flow:
  Trigger: Any step failure

  Example: QualityApproved fails (品質不合格)
    1. Food Safety publishes: QualityRejected
    2. Warehouse listens: ReleaseInventory (在庫引当解除)
    3. Transport listens: ReleaseDeliverySlot (配車枠解放)
    4. Order listens: CancelShipmentOrder (出荷指示取消)
    5. Order updates: OrderStatus = "Pending Re-inspection"
```

## 結果

### 良い影響

1. **疎結合**: 各サービスは自身のイベントを発行するだけ、他サービスの内部を知らない
2. **スケーラビリティ**: イベントベースで非同期処理、高スループット
3. **耐障害性**: 1サービスの障害が全体をブロックしない
4. **進化性**: 新しいステップ（サービス）の追加が容易
5. **可視性**: イベントログによりSaga全体の進捗を追跡可能

### トレードオフ

1. **複雑性**: イベントフローの理解・デバッグが困難
   - 軽減策: 分散トレーシング（Jaeger/Zipkin）の導入
2. **イベント順序**: イベントの到着順序が保証されない場合がある
   - 軽減策: パーティションキーによる順序保証、冪等性の確保
3. **グローバルビュー不在**: Sagaの全体状態を持つサービスがない
   - 軽減策: Saga状態追跡テーブル、イベントソーシング

### リスク

1. **循環依存**: イベントの循環による無限ループ
   - 軽減策: イベントの一方向性を設計で保証
2. **補償失敗**: 補償トランザクション自体が失敗
   - 軽減策: リトライ、手動介入アラート、Dead Letter Queue

## 代替案

### 代替案1: Saga Orchestration（オーケストレーション方式）
- **メリット**: 全体状態の一元管理、デバッグ容易
- **却下理由**: オーケストレーターが単一障害点、サービス間結合度が高い

### 代替案2: 2PC（Two-Phase Commit）
- **メリット**: 強整合性
- **却下理由**: 可用性の犠牲、長時間ロック、マイクロサービスに不適

### 代替案3: 手動補償（人間による介入）
- **メリット**: シンプル
- **却下理由**: スケーラビリティ不足、応答時間が遅い

## なぜ Choreography を選択したか

| 観点 | Orchestration | Choreography |
|------|---------------|--------------|
| 結合度 | 高（オーケストレーター依存） | 低（イベント駆動） |
| 単一障害点 | あり | なし |
| スケーラビリティ | 制限あり | 高い |
| 追加サービス | オーケストレーター変更必要 | イベント購読のみ |
| デバッグ | 容易 | 困難（分散トレーシング必要） |
| サントリーSCMへの適合 | △ | ◎（独立チーム、疎結合要件） |

**サントリーSCMでは**:
- 各部門（品質保証、物流、サステナビリティ）が独立して運用
- サービス追加（将来のM&A対応等）への柔軟性
- 高可用性要件（単一障害点を避ける）

これらの理由から**Choreography方式**を選択。

## 関連

- ADR-001: マイクロサービスアーキテクチャの採用
- ADR-002: イベントバスの選択
- ADR-003: Database per Service パターン
- 統合パターン: `outputs/4-architecture/integration-patterns.md`
- サービス定義: 各サービスの「Saga参加」セクション

---

**作成者**: Parasol V5 Phase 4
**レビュー者**: アーキテクチャチーム、各サービスオーナー
