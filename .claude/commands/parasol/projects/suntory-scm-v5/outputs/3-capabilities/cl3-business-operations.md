# CL3 Business Operations Definition

**プロジェクト**: サントリーホールディングス / SCM
**Parasol Version**: V5
**作成日**: 2025-01-15
**前提**: CL2 Sub-capability Design 完了

---

## 概要

Phase 3-3として、14のCL2サブケイパビリティから39のCL3ビジネスオペレーションを定義します。
CL3は実際のビジネス操作（CRUD + ドメイン固有操作）を表し、BC（Bounded Context）の基礎となります。

### CL3サマリー

| 指標 | 値 |
|------|-----|
| CL3総数 | 39 |
| Core起源 | 22（56%） |
| VCI起源 | 9（23%） |
| Supporting起源 | 4（10%） |
| Generic起源 | 4（10%） |
| 平均CL3/CL2 | 2.79 |

### TVDC分布確認

| TVDC分類 | CL2数 | 目標CL3数 | 実際CL3数 | 達成状況 |
|---------|-------|----------|----------|---------|
| Core | 8 | 20-25 | 22 | ✅ |
| VCI | 3 | 7-10 | 9 | ✅ |
| Supporting | 2 | 2-4 | 4 | ✅ |
| Generic | 2 | 3-5 | 4 | ✅ |
| **合計** | **14** | **32-44** | **39** | ✅ |

---

## CL3一覧（全39オペレーション）

### 一覧表

| CL3 ID | ビジネスオペレーション名 | 親CL2 | TVDC | 主要アクター |
|--------|------------------------|-------|------|-------------|
| CL3-01-01-01 | sales-data-collection | demand-forecasting | Core | 営業本部 |
| CL3-01-01-02 | demand-forecast-execution | demand-forecasting | Core | 需給計画担当 |
| CL3-01-01-03 | forecast-accuracy-validation | demand-forecasting | Core | 需給計画担当 |
| CL3-01-02-01 | optimal-stock-calculation | inventory-optimization | Core | 在庫管理担当 |
| CL3-01-02-02 | inventory-allocation | inventory-optimization | Core | 在庫管理担当 |
| CL3-01-02-03 | stockout-risk-monitoring | inventory-optimization | Core | 在庫管理担当 |
| CL3-01-03-01 | production-schedule-creation | production-planning | Core | 生産本部 |
| CL3-01-03-02 | capacity-adjustment | production-planning | Core | 生産本部 |
| CL3-01-03-03 | contract-factory-coordination | production-planning | Core | 調達本部 |
| CL3-02-01-01 | delivery-schedule-creation | transport-planning | Core | 物流部 |
| CL3-02-01-02 | transport-resource-allocation | transport-planning | Core | 物流部 |
| CL3-02-01-03 | joint-transport-coordination | transport-planning | Core | 物流部 |
| CL3-02-02-01 | receipt-shipment-processing | warehouse-management | VCI | 倉庫事業者 |
| CL3-02-02-02 | warehouse-stock-control | warehouse-management | VCI | 倉庫事業者 |
| CL3-02-02-03 | warehouse-operation-optimization | warehouse-management | VCI | 物流部 |
| CL3-02-03-01 | route-calculation | route-optimization | Core | 物流部 |
| CL3-02-03-02 | real-time-route-optimization | route-optimization | Core | 物流部 |
| CL3-02-03-03 | relay-point-utilization | route-optimization | Core | 物流部 |
| CL3-02-04-01 | vehicle-tracking | fleet-management | Core | 物流部 |
| CL3-02-04-02 | driver-work-management | fleet-management | Core | 運送会社 |
| CL3-03-01-01 | haccp-management | food-safety-compliance | VCI | 品質保証部 |
| CL3-03-01-02 | temperature-control-recording | food-safety-compliance | VCI | 品質保証部 |
| CL3-03-01-03 | hygiene-inspection | food-safety-compliance | VCI | 品質保証部 |
| CL3-03-02-01 | lot-tracking | traceability-management | VCI | 品質保証部 |
| CL3-03-02-02 | material-history-management | traceability-management | VCI | 調達本部 |
| CL3-03-02-03 | recall-handling | traceability-management | VCI | 品質保証部 |
| CL3-04-01-01 | water-source-monitoring | water-source-management | Core | 環境部 |
| CL3-04-01-02 | forest-conservation-management | water-source-management | Core | 環境部 |
| CL3-04-01-03 | water-quality-testing | water-source-management | Core | 品質保証部 |
| CL3-04-02-01 | environmental-metrics-collection | environmental-reporting | Supporting | 環境部 |
| CL3-04-02-02 | regulatory-report-generation | environmental-reporting | Supporting | 環境部 |
| CL3-04-03-01 | co2-emission-calculation | carbon-footprint | Supporting | 環境部 |
| CL3-04-03-02 | reduction-target-tracking | carbon-footprint | Supporting | 環境部 |
| CL3-05-01-01 | order-registration | order-processing | Generic | 営業本部 |
| CL3-05-01-02 | order-confirmation | order-processing | Generic | 営業本部 |
| CL3-05-02-01 | edi-integration | partner-integration | Generic | IT部門 |
| CL3-05-02-02 | partner-data-synchronization | partner-integration | Generic | IT部門 |
| CL3-02-01-04 | 2024-compliance-monitoring | transport-planning | Core | 物流部 |
| CL3-02-02-04 | pallet-efficiency-management | warehouse-management | VCI | 物流部 |

---

## CL1-01: Demand Management（需要管理）起源

### CL2-01-01: demand-forecasting（需要予測）

#### CL3-01-01-01: sales-data-collection（販売実績収集）

| 項目 | 内容 |
|------|------|
| **日本語名** | 販売実績収集 |
| **目的** | 需要予測の入力となる販売実績データを収集・整理 |
| **主要アクター** | 営業本部、卸売業者、小売業者 |
| **入力** | POS売上データ、卸売出荷データ、EC販売データ |
| **出力** | 標準化された販売実績データセット |
| **頻度** | 日次（バッチ）+ リアルタイム（重要商品） |
| **VL2寄与** | 安定供給体制 → 需要把握による適正供給 |

**ドメイン操作**:
- `collectSalesData(channel, period)`: チャネル別販売データ収集
- `normalizeSalesData(rawData)`: 販売データの標準化
- `detectAnomalies(salesData)`: 異常値検出

**状態遷移**:
```
未収集 → 収集中 → 検証中 → 確定済み → 予測投入済み
```

**PDL候補用語**:
- 販売チャネル（SalesChannel）
- 販売実績（SalesRecord）
- 異常検出結果（AnomalyResult）

---

#### CL3-01-01-02: demand-forecast-execution（需要予測モデル実行）

| 項目 | 内容 |
|------|------|
| **日本語名** | 需要予測モデル実行 |
| **目的** | AI/統計モデルによる需要予測の実行 |
| **主要アクター** | 需給計画担当、データサイエンティスト |
| **入力** | 販売実績、季節性、プロモーション計画、外部要因 |
| **出力** | 品目別・拠点別の需要予測値 |
| **頻度** | 日次（ローリング予測）、週次（計画確定） |
| **VL2寄与** | 安定供給体制 → 精度高い予測による適正在庫 |

**ドメイン操作**:
- `executeForecast(model, parameters)`: 予測モデル実行
- `aggregateForecast(granularity)`: 予測値の集約（SKU→カテゴリ→事業部）
- `applyPromotionLift(forecast, promotionPlan)`: プロモーション補正

**状態遷移**:
```
予測準備中 → 実行中 → 結果生成 → レビュー中 → 承認済み
```

**PDL候補用語**:
- 需要予測（DemandForecast）
- 予測モデル（ForecastModel）
- プロモーションリフト（PromotionLift）

---

#### CL3-01-01-03: forecast-accuracy-validation（予測精度検証）

| 項目 | 内容 |
|------|------|
| **日本語名** | 予測精度検証 |
| **目的** | 需要予測の精度を検証し、モデル改善につなげる |
| **主要アクター** | 需給計画担当 |
| **入力** | 予測値、実績値 |
| **出力** | 精度指標（MAPE、バイアス）、改善提案 |
| **頻度** | 週次（振り返り）、月次（モデル評価） |
| **VL2寄与** | 安定供給体制 → 継続的な予測精度向上 |

**ドメイン操作**:
- `calculateAccuracy(forecast, actual)`: 精度指標計算
- `identifyBias(forecastHistory)`: バイアス傾向分析
- `recommendModelTuning(accuracyReport)`: モデル調整提案

**状態遷移**:
```
評価待ち → 評価実行中 → レポート生成 → 改善アクション中 → 完了
```

---

### CL2-01-02: inventory-optimization（在庫最適化）

#### CL3-01-02-01: optimal-stock-calculation（適正在庫計算）

| 項目 | 内容 |
|------|------|
| **日本語名** | 適正在庫計算 |
| **目的** | 需要予測に基づく適正在庫水準の算出 |
| **主要アクター** | 在庫管理担当 |
| **入力** | 需要予測、リードタイム、サービスレベル目標 |
| **出力** | 品目別・拠点別の適正在庫水準 |
| **頻度** | 日次（更新）、週次（見直し） |
| **VL2寄与** | 安定供給体制 → 欠品ゼロと過剰在庫回避の両立 |

**ドメイン操作**:
- `calculateSafetyStock(demand, variability, serviceLevel)`: 安全在庫計算
- `setReorderPoint(leadTime, demand)`: 発注点設定
- `optimizeStockLevel(constraints)`: 在庫水準最適化

**状態遷移**:
```
計算前 → 計算中 → 検証中 → 適用中 → モニタリング中
```

**PDL候補用語**:
- 適正在庫水準（OptimalStockLevel）
- 安全在庫（SafetyStock）
- 発注点（ReorderPoint）
- サービスレベル（ServiceLevel）

---

#### CL3-01-02-02: inventory-allocation（在庫配置最適化）

| 項目 | 内容 |
|------|------|
| **日本語名** | 在庫配置最適化 |
| **目的** | 全国約300倉庫への最適な在庫配置決定 |
| **主要アクター** | 在庫管理担当、物流部 |
| **入力** | 地域別需要、倉庫容量、輸送コスト |
| **出力** | 拠点別在庫配置計画 |
| **頻度** | 週次（計画策定）、月次（戦略見直し） |
| **VL2寄与** | 物流効率化 → 輸送距離短縮による配送効率向上 |

**ドメイン操作**:
- `allocateInventory(demand, warehouses)`: 在庫配置決定
- `balanceStock(sourceWarehouse, targetWarehouse)`: 拠点間在庫調整
- `evaluateAllocationCost(plan)`: 配置コスト評価

**状態遷移**:
```
需要分析 → 配置計算 → 計画作成 → 承認待ち → 実行中 → 完了
```

---

#### CL3-01-02-03: stockout-risk-monitoring（欠品リスク監視）

| 項目 | 内容 |
|------|------|
| **日本語名** | 欠品リスク監視 |
| **目的** | 欠品リスクの早期検知と対応アクション発動 |
| **主要アクター** | 在庫管理担当、営業本部 |
| **入力** | 在庫状況、需要予測、入荷予定 |
| **出力** | 欠品リスクアラート、対応推奨アクション |
| **頻度** | リアルタイム（監視）、日次（レポート） |
| **VL2寄与** | 安定供給体制 → 欠品発生前の予防措置 |

**ドメイン操作**:
- `monitorStockoutRisk(inventory, forecast)`: リスク監視
- `triggerAlert(riskLevel, item)`: アラート発行
- `recommendAction(riskType)`: 対応アクション提案

**状態遷移**:
```
正常 → 警告 → 危険 → 対応中 → 解消
```

---

### CL2-01-03: production-planning（生産計画）

#### CL3-01-03-01: production-schedule-creation（生産計画策定）

| 項目 | 内容 |
|------|------|
| **日本語名** | 生産計画策定 |
| **目的** | 需要予測に基づく工場別生産計画の策定 |
| **主要アクター** | 生産本部 |
| **入力** | 需要予測、在庫計画、製造能力、原材料在庫 |
| **出力** | 工場別・品目別の生産スケジュール |
| **頻度** | 週次（計画策定）、日次（微調整） |
| **VL2寄与** | 安定供給体制 → 需要に応じた適時生産 |

**ドメイン操作**:
- `createProductionPlan(demand, capacity)`: 生産計画作成
- `scheduleBatch(factory, items)`: バッチスケジューリング
- `adjustPlan(changeRequest)`: 計画変更対応

**状態遷移**:
```
計画立案中 → レビュー中 → 承認済み → 実行中 → 完了
```

**PDL候補用語**:
- 生産計画（ProductionPlan）
- 製造バッチ（ManufacturingBatch）
- 生産能力（ProductionCapacity）

---

#### CL3-01-03-02: capacity-adjustment（製造能力調整）

| 項目 | 内容 |
|------|------|
| **日本語名** | 製造能力調整 |
| **目的** | 需要変動に応じた製造能力の調整 |
| **主要アクター** | 生産本部 |
| **入力** | 需要予測、現在の稼働状況、設備能力 |
| **出力** | 能力調整計画（シフト変更、ライン変更） |
| **頻度** | 週次（計画）、随時（緊急対応） |
| **VL2寄与** | 安定供給体制 → 需要ピークへの柔軟な対応 |

**ドメイン操作**:
- `assessCapacity(factory, period)`: 能力評価
- `adjustShifts(factory, requirement)`: シフト調整
- `reallocateLines(products, lines)`: ライン再配置

---

#### CL3-01-03-03: contract-factory-coordination（委託工場連携）

| 項目 | 内容 |
|------|------|
| **日本語名** | 委託工場連携 |
| **目的** | 委託製造工場（OEM）との生産調整 |
| **主要アクター** | 調達本部、委託製造工場 |
| **入力** | 生産依頼、品質基準、納期要件 |
| **出力** | 委託生産オーダー、納品スケジュール |
| **頻度** | 週次（発注）、日次（進捗確認） |
| **VL2寄与** | 安定供給体制 → 自社能力を補完する外部生産活用 |

**ドメイン操作**:
- `placeContractOrder(factory, items, quantity)`: 委託発注
- `trackContractProgress(orderId)`: 進捗追跡
- `validateQuality(delivery)`: 品質検証

---

## CL1-02: Logistics Optimization（物流最適化）起源

### CL2-02-01: transport-planning（輸送計画）

#### CL3-02-01-01: delivery-schedule-creation（配送計画策定）

| 項目 | 内容 |
|------|------|
| **日本語名** | 配送計画策定 |
| **目的** | 出荷要件に基づく配送スケジュールの策定 |
| **主要アクター** | 物流部 |
| **入力** | 出荷依頼、配送先情報、納期要件 |
| **出力** | 配送スケジュール、車両割当 |
| **頻度** | 日次（翌日計画）、リアルタイム（当日調整） |
| **VL2寄与** | 物流効率化 → 計画的配送による効率向上 |

**ドメイン操作**:
- `createDeliverySchedule(shipments, constraints)`: 配送計画作成
- `assignVehicles(schedule, fleet)`: 車両割当
- `optimizeLoadSequence(vehicle, deliveries)`: 積載順序最適化

**状態遷移**:
```
計画作成中 → 車両割当中 → 確定 → 実行中 → 完了
```

**PDL候補用語**:
- 配送計画（DeliverySchedule）
- 車両割当（VehicleAssignment）
- 積載計画（LoadPlan）

---

#### CL3-02-01-02: transport-resource-allocation（輸送リソース配分）

| 項目 | 内容 |
|------|------|
| **日本語名** | 輸送リソース配分 |
| **目的** | 運送会社・車両の最適な配分決定 |
| **主要アクター** | 物流部、運送会社群 |
| **入力** | 輸送需要、運送会社キャパシティ、コスト条件 |
| **出力** | 運送会社別配分計画 |
| **頻度** | 週次（配分計画）、日次（調整） |
| **VL2寄与** | 物流効率化 → リソース最適化によるコスト削減 |

**ドメイン操作**:
- `allocateTransportResources(demand, carriers)`: リソース配分
- `negotiateCapacity(carrier, requirement)`: キャパシティ交渉
- `evaluateCarrierPerformance(carrier, period)`: パフォーマンス評価

---

#### CL3-02-01-03: joint-transport-coordination（共同輸送調整）

| 項目 | 内容 |
|------|------|
| **日本語名** | 共同輸送調整 |
| **目的** | 大王グループ等との異業種共同輸送の調整 |
| **主要アクター** | 物流部、大王グループ |
| **入力** | 自社輸送計画、パートナー輸送計画 |
| **出力** | 共同輸送計画、コスト按分 |
| **頻度** | 週次（計画調整）、日次（運行確認） |
| **VL2寄与** | 物流効率化 → 共同化による能力確保・コスト削減 |

**ドメイン操作**:
- `matchJointTransport(ownPlan, partnerPlan)`: 共同輸送マッチング
- `allocateSharedCapacity(jointRoute)`: 共同キャパシティ配分
- `splitCost(jointDelivery)`: コスト按分計算

**PDL候補用語**:
- 共同輸送（JointTransport）
- キャパシティ共有（SharedCapacity）
- コスト按分（CostAllocation）

---

#### CL3-02-01-04: 2024-compliance-monitoring（2024年問題対応監視）

| 項目 | 内容 |
|------|------|
| **日本語名** | 2024年問題対応監視 |
| **目的** | ドライバー労働時間規制（年960時間）の遵守監視 |
| **主要アクター** | 物流部、運送会社 |
| **入力** | ドライバー稼働実績、規制基準 |
| **出力** | コンプライアンス状況レポート、是正アラート |
| **頻度** | リアルタイム（監視）、週次（レポート） |
| **VL2寄与** | 物流効率化 → 規制対応による持続可能な物流 |

**ドメイン操作**:
- `trackOvertimeHours(driver, period)`: 時間外労働追跡
- `alertComplianceRisk(driver, threshold)`: コンプライアンスリスク警告
- `recommendWorkloadAdjustment(driver)`: 負荷調整提案

**状態遷移**:
```
正常 → 警告（80%） → 危険（90%） → 上限到達 → 代替対応中
```

**PDL候補用語**:
- 労働時間規制（OvertimeRegulation）
- コンプライアンス状態（ComplianceStatus）

---

### CL2-02-02: warehouse-management（倉庫管理）

#### CL3-02-02-01: receipt-shipment-processing（入出庫処理）

| 項目 | 内容 |
|------|------|
| **日本語名** | 入出庫処理 |
| **目的** | 倉庫での入庫・出庫業務の処理 |
| **主要アクター** | 倉庫事業者 |
| **入力** | 入庫予定、出荷指示 |
| **出力** | 入庫完了報告、出荷完了報告 |
| **頻度** | 随時（オペレーション発生都度） |
| **VL2寄与** | 物流効率化 → 正確な入出庫による在庫精度向上 |

**ドメイン操作**:
- `processReceipt(delivery, warehouse)`: 入庫処理
- `processShipment(order, warehouse)`: 出庫処理
- `updateInventory(transaction)`: 在庫更新

**状態遷移**:
```
【入庫】予定 → 到着 → 検品中 → 格納中 → 完了
【出庫】指示受付 → ピッキング中 → 検品中 → 出荷中 → 完了
```

---

#### CL3-02-02-02: warehouse-stock-control（倉庫内在庫管理）

| 項目 | 内容 |
|------|------|
| **日本語名** | 倉庫内在庫管理 |
| **目的** | 倉庫内の在庫状況把握と棚卸管理 |
| **主要アクター** | 倉庫事業者 |
| **入力** | 在庫データ、ロケーション情報 |
| **出力** | 在庫状況レポート、棚卸結果 |
| **頻度** | リアルタイム（在庫把握）、月次（棚卸） |
| **VL2寄与** | 物流効率化 → 正確な在庫把握による効率向上 |

**ドメイン操作**:
- `trackStock(warehouse, item)`: 在庫追跡
- `conductInventoryCount(warehouse)`: 棚卸実施
- `reconcileDiscrepancy(expected, actual)`: 差異調整

---

#### CL3-02-02-03: warehouse-operation-optimization（庫内作業効率化）

| 項目 | 内容 |
|------|------|
| **日本語名** | 庫内作業効率化 |
| **目的** | 倉庫内作業の効率化・自動化推進 |
| **主要アクター** | 物流部、倉庫事業者 |
| **入力** | 作業実績、レイアウト情報、作業者配置 |
| **出力** | 効率化提案、レイアウト改善案 |
| **頻度** | 月次（分析）、四半期（改善実施） |
| **VL2寄与** | 物流効率化 → 人手不足対応・コスト削減 |

**ドメイン操作**:
- `analyzeOperationEfficiency(warehouse)`: 効率分析
- `optimizeLayout(warehouse, flowPatterns)`: レイアウト最適化
- `introduceAutomation(warehouse, process)`: 自動化導入

---

#### CL3-02-02-04: pallet-efficiency-management（パレット効率管理）

| 項目 | 内容 |
|------|------|
| **日本語名** | パレット効率管理 |
| **目的** | パレット積載効率の向上（35→45ケース/パレット） |
| **主要アクター** | 物流部 |
| **入力** | パレットパターン、商品寸法、積載ルール |
| **出力** | 最適パレットパターン、効率指標 |
| **頻度** | 商品投入時、定期見直し（四半期） |
| **VL2寄与** | 物流効率化 → 29%効率向上による輸送能力確保 |

**ドメイン操作**:
- `calculatePalletPattern(item, palletSize)`: パレットパターン計算
- `optimizeStacking(items, constraints)`: 積載最適化
- `trackEfficiencyGain(baseline, current)`: 効率向上追跡

**PDL候補用語**:
- パレットパターン（PalletPattern）
- 積載効率（StackingEfficiency）

---

### CL2-02-03: route-optimization（ルート最適化）

#### CL3-02-03-01: route-calculation（配送ルート計算）

| 項目 | 内容 |
|------|------|
| **日本語名** | 配送ルート計算 |
| **目的** | 最適な配送ルートの計算 |
| **主要アクター** | 物流部 |
| **入力** | 配送先リスト、道路情報、時間制約 |
| **出力** | 最適配送ルート |
| **頻度** | 日次（計画時）、随時（追加対応時） |
| **VL2寄与** | 物流効率化 → ルート最適化による燃料・時間削減 |

**ドメイン操作**:
- `calculateOptimalRoute(destinations, constraints)`: 最適ルート計算
- `estimateArrivalTime(route)`: 到着時間予測
- `compareRouteAlternatives(routes)`: ルート比較

**PDL候補用語**:
- 配送ルート（DeliveryRoute）
- 到着予定時刻（EstimatedArrival）

---

#### CL3-02-03-02: real-time-route-optimization（リアルタイム経路最適化）

| 項目 | 内容 |
|------|------|
| **日本語名** | リアルタイム経路最適化 |
| **目的** | 交通状況に応じた動的なルート最適化（traevo連携） |
| **主要アクター** | 物流部、運送会社 |
| **入力** | 車両位置情報、交通情報、配送状況 |
| **出力** | 最適化されたルート指示 |
| **頻度** | リアルタイム |
| **VL2寄与** | 物流効率化 → DX活用による先進的物流 |

**ドメイン操作**:
- `adjustRouteRealtime(vehicle, trafficCondition)`: リアルタイム調整
- `rerouteOnIncident(vehicle, incident)`: 障害時再ルーティング
- `notifyDriverRouteChange(driver, newRoute)`: ドライバー通知

**traevo連携**:
- 車両位置のリアルタイム取得
- 交通情報の統合
- 最適ルートの自動提案

---

#### CL3-02-03-03: relay-point-utilization（中継拠点活用）

| 項目 | 内容 |
|------|------|
| **日本語名** | 中継拠点活用 |
| **目的** | 長距離輸送における中継拠点の活用（連続運転4時間制限対応） |
| **主要アクター** | 物流部 |
| **入力** | 輸送ルート、中継拠点情報、ドライバー制約 |
| **出力** | 中継計画、ドライバー引継ぎスケジュール |
| **頻度** | 日次（計画）、随時（調整） |
| **VL2寄与** | 物流効率化 → 2024年問題対応の効率的解決 |

**ドメイン操作**:
- `planRelayPoints(route, driverConstraints)`: 中継計画策定
- `scheduleDriverHandoff(relayPoint)`: ドライバー引継ぎ
- `trackRelayExecution(plan)`: 中継実行追跡

---

### CL2-02-04: fleet-management（車両管理）

#### CL3-02-04-01: vehicle-tracking（車両位置追跡）

| 項目 | 内容 |
|------|------|
| **日本語名** | 車両位置追跡 |
| **目的** | 配送車両のリアルタイム位置把握（traevo活用） |
| **主要アクター** | 物流部 |
| **入力** | GPS位置情報、車両ID |
| **出力** | 車両位置情報、配送進捗 |
| **頻度** | リアルタイム |
| **VL2寄与** | 物流効率化 → 可視化による待機時間削減 |

**ドメイン操作**:
- `trackVehiclePosition(vehicleId)`: 位置追跡
- `estimateArrivalAtDestination(vehicle)`: 到着予測
- `alertDelayRisk(vehicle, schedule)`: 遅延リスク警告

**traevo連携**:
- リアルタイム位置情報取得
- 遅延予測アルゴリズム
- 可視化ダッシュボード

---

#### CL3-02-04-02: driver-work-management（ドライバー稼働管理）

| 項目 | 内容 |
|------|------|
| **日本語名** | ドライバー稼働管理 |
| **目的** | ドライバーの稼働状況管理と労働時間管理 |
| **主要アクター** | 運送会社、物流部 |
| **入力** | ドライバー出勤情報、運転記録 |
| **出力** | 稼働状況レポート、労働時間実績 |
| **頻度** | リアルタイム（稼働把握）、日次（レポート） |
| **VL2寄与** | 物流効率化 → 2024年問題対応のドライバー管理 |

**ドメイン操作**:
- `recordDrivingHours(driver, session)`: 運転時間記録
- `calculateRestRequirement(driver)`: 休憩必要時間計算
- `assignDriverToRoute(driver, route)`: ドライバー割当

---

## CL1-03: Quality Assurance（品質保証）起源

### CL2-03-01: food-safety-compliance（食品安全コンプライアンス）

#### CL3-03-01-01: haccp-management（HACCP管理）

| 項目 | 内容 |
|------|------|
| **日本語名** | HACCP管理 |
| **目的** | HACCP（危害要因分析重要管理点）の実施・記録 |
| **主要アクター** | 品質保証部 |
| **入力** | 製造工程データ、管理基準 |
| **出力** | HACCP記録、逸脱報告 |
| **頻度** | 随時（製造工程に連動） |
| **VL2寄与** | 品質・安全 → 法令遵守と食品安全確保 |

**ドメイン操作**:
- `monitorCriticalControlPoint(ccp, measurement)`: CCP監視
- `recordHaccpData(ccp, value, timestamp)`: HACCP記録
- `handleDeviation(ccp, deviation)`: 逸脱対応

**状態遷移**:
```
監視中 → 正常 / 逸脱検出 → 是正措置中 → 是正完了 → 記録完了
```

**PDL候補用語**:
- 重要管理点（CriticalControlPoint）
- 逸脱（Deviation）
- 是正措置（CorrectiveAction）

---

#### CL3-03-01-02: temperature-control-recording（温度管理記録）

| 項目 | 内容 |
|------|------|
| **日本語名** | 温度管理記録 |
| **目的** | コールドチェーン全体の温度管理・記録 |
| **主要アクター** | 品質保証部、倉庫事業者、運送会社 |
| **入力** | 温度センサーデータ |
| **出力** | 温度記録、逸脱アラート |
| **頻度** | リアルタイム（監視）、日次（レポート） |
| **VL2寄与** | 品質・安全 → 温度逸脱による品質劣化防止 |

**ドメイン操作**:
- `recordTemperature(location, sensor, value)`: 温度記録
- `alertTemperatureExcursion(location, threshold)`: 温度逸脱警告
- `generateTemperatureReport(period)`: 温度レポート生成

---

#### CL3-03-01-03: hygiene-inspection（衛生検査実施）

| 項目 | 内容 |
|------|------|
| **日本語名** | 衛生検査実施 |
| **目的** | 製造施設・倉庫の衛生検査実施と記録 |
| **主要アクター** | 品質保証部 |
| **入力** | 検査計画、検査基準 |
| **出力** | 検査結果、是正要請 |
| **頻度** | 定期（日次〜月次）、随時（問題発生時） |
| **VL2寄与** | 品質・安全 → 衛生管理による品質確保 |

**ドメイン操作**:
- `scheduleInspection(facility, type)`: 検査スケジューリング
- `conductInspection(facility, checklist)`: 検査実施
- `issueCorrectiveRequest(facility, finding)`: 是正要請発行

---

### CL2-03-02: traceability-management（トレーサビリティ管理）

#### CL3-03-02-01: lot-tracking（ロット追跡）

| 項目 | 内容 |
|------|------|
| **日本語名** | ロット追跡 |
| **目的** | 製品ロットの製造〜出荷の追跡（日立協創連携） |
| **主要アクター** | 品質保証部 |
| **入力** | ロットID、製造記録、出荷記録 |
| **出力** | ロット履歴、追跡レポート |
| **頻度** | 随時（問い合わせ対応）、日次（バッチ更新） |
| **VL2寄与** | 品質・安全 → 問題発生時の迅速な追跡 |

**ドメイン操作**:
- `traceLot(lotId)`: ロット追跡
- `getLotHistory(lotId)`: ロット履歴取得
- `identifyAffectedLots(issue)`: 影響ロット特定

**日立協創連携**:
- ブロックチェーン基盤でのロット情報記録
- サプライチェーン全体での情報共有
- 改ざん防止機能

**PDL候補用語**:
- ロット（Lot）
- ロット履歴（LotHistory）
- トレースバック（Traceback）
- トレースフォワード（TraceForward）

---

#### CL3-03-02-02: material-history-management（原材料履歴管理）

| 項目 | 内容 |
|------|------|
| **日本語名** | 原材料履歴管理 |
| **目的** | 原材料の調達〜使用までの履歴管理 |
| **主要アクター** | 調達本部、品質保証部 |
| **入力** | 原材料入荷情報、サプライヤー情報、使用記録 |
| **出力** | 原材料履歴、サプライヤー評価 |
| **頻度** | 随時（入荷都度）、月次（サプライヤー評価） |
| **VL2寄与** | 品質・安全 → 原材料起因の問題追跡 |

**ドメイン操作**:
- `recordMaterialReceipt(material, supplier, lot)`: 入荷記録
- `trackMaterialUsage(material, productionBatch)`: 使用追跡
- `evaluateSupplierQuality(supplier, period)`: サプライヤー品質評価

---

#### CL3-03-02-03: recall-handling（リコール対応）

| 項目 | 内容 |
|------|------|
| **日本語名** | リコール対応 |
| **目的** | 品質問題発生時のリコール実行管理 |
| **主要アクター** | 品質保証部、営業本部 |
| **入力** | 問題ロット情報、出荷先情報 |
| **出力** | リコール計画、回収状況 |
| **頻度** | 随時（問題発生時） |
| **VL2寄与** | 品質・安全 → 迅速なリコールによる被害最小化 |

**ドメイン操作**:
- `initiateRecall(issue, affectedLots)`: リコール開始
- `trackRecallProgress(recallId)`: 回収進捗追跡
- `closeRecall(recallId, report)`: リコール完了

**状態遷移**:
```
問題検知 → リコール判断 → 計画策定 → 実行中 → 回収完了 → 報告完了
```

---

## CL1-04: Sustainability（サステナビリティ）起源

### CL2-04-01: water-source-management（水源管理）

#### CL3-04-01-01: water-source-monitoring（水源地モニタリング）

| 項目 | 内容 |
|------|------|
| **日本語名** | 水源地モニタリング |
| **目的** | 天然水の森（21,000ha）の水源状態監視 |
| **主要アクター** | 環境部 |
| **入力** | センサーデータ、気象データ、水文データ |
| **出力** | 水源状態レポート、アラート |
| **頻度** | リアルタイム（センサー）、日次（レポート） |
| **VL2寄与** | サステナビリティ → 水資源の持続的利用 |

**ドメイン操作**:
- `monitorWaterLevel(source)`: 水位監視
- `measureWaterQuality(source, parameters)`: 水質測定
- `alertWaterSourceAnomaly(source, anomaly)`: 異常アラート

**PDL候補用語**:
- 水源地（WaterSource）
- 天然水の森（NaturalWaterForest）
- 水源涵養（WaterRecharge）

---

#### CL3-04-01-02: forest-conservation-management（森林保全活動管理）

| 項目 | 内容 |
|------|------|
| **日本語名** | 森林保全活動管理 |
| **目的** | 天然水の森の保全活動計画・実行管理 |
| **主要アクター** | 環境部、地域パートナー |
| **入力** | 森林状態評価、保全計画 |
| **出力** | 活動実績、保全効果レポート |
| **頻度** | 月次（活動管理）、年次（効果評価） |
| **VL2寄与** | サステナビリティ → 水源涵養機能の維持・向上 |

**ドメイン操作**:
- `planConservationActivity(forest, period)`: 活動計画策定
- `recordConservationWork(activity, result)`: 活動記録
- `evaluateConservationEffect(forest, period)`: 効果評価

---

#### CL3-04-01-03: water-quality-testing（水質検査記録）

| 項目 | 内容 |
|------|------|
| **日本語名** | 水質検査記録 |
| **目的** | 水源地・製造用水の水質検査と記録 |
| **主要アクター** | 品質保証部、環境部 |
| **入力** | 水サンプル、検査基準 |
| **出力** | 水質検査結果、適合証明 |
| **頻度** | 定期（週次〜月次）、随時（問題発生時） |
| **VL2寄与** | サステナビリティ → 水質維持による製品品質確保 |

**ドメイン操作**:
- `sampleWater(source, location)`: 採水
- `testWaterQuality(sample, parameters)`: 水質検査
- `certifyWaterQuality(result, standard)`: 適合証明

---

### CL2-04-02: environmental-reporting（環境報告）

#### CL3-04-02-01: environmental-metrics-collection（環境指標収集）

| 項目 | 内容 |
|------|------|
| **日本語名** | 環境指標収集 |
| **目的** | ESG報告に必要な環境指標データの収集 |
| **主要アクター** | 環境部 |
| **入力** | エネルギー使用量、水使用量、廃棄物量 |
| **出力** | 環境指標データベース |
| **頻度** | 月次（データ収集）、四半期（集計） |
| **VL2寄与** | サステナビリティ → ESG情報開示の基盤 |

**ドメイン操作**:
- `collectEnergyData(facility, period)`: エネルギーデータ収集
- `collectWaterUsage(facility, period)`: 水使用量収集
- `collectWasteData(facility, period)`: 廃棄物データ収集

---

#### CL3-04-02-02: regulatory-report-generation（規制報告作成）

| 項目 | 内容 |
|------|------|
| **日本語名** | 規制報告作成 |
| **目的** | 環境規制当局への報告書作成 |
| **主要アクター** | 環境部 |
| **入力** | 環境指標データ、規制要件 |
| **出力** | 規制報告書 |
| **頻度** | 年次（定期報告）、随時（要請対応） |
| **VL2寄与** | サステナビリティ → 環境規制への適切な対応 |

**ドメイン操作**:
- `generateRegulatoryReport(type, period)`: 規制報告生成
- `validateReportData(report)`: データ検証
- `submitReport(report, authority)`: 報告提出

---

### CL2-04-03: carbon-footprint（カーボンフットプリント）

#### CL3-04-03-01: co2-emission-calculation（CO2排出量計算）

| 項目 | 内容 |
|------|------|
| **日本語名** | CO2排出量計算 |
| **目的** | サプライチェーン全体のCO2排出量算出 |
| **主要アクター** | 環境部 |
| **入力** | エネルギー使用量、輸送距離、排出係数 |
| **出力** | CO2排出量レポート |
| **頻度** | 月次（計算）、年次（総括） |
| **VL2寄与** | サステナビリティ → カーボンニュートラル進捗管理 |

**ドメイン操作**:
- `calculateScope1Emissions(facility)`: Scope1排出量計算
- `calculateScope2Emissions(facility)`: Scope2排出量計算
- `calculateScope3Emissions(activity)`: Scope3排出量計算

**PDL候補用語**:
- カーボンフットプリント（CarbonFootprint）
- 排出係数（EmissionFactor）
- Scope1/2/3排出量（ScopeEmission）

---

#### CL3-04-03-02: reduction-target-tracking（削減目標進捗管理）

| 項目 | 内容 |
|------|------|
| **日本語名** | 削減目標進捗管理 |
| **目的** | CO2削減目標に対する進捗追跡 |
| **主要アクター** | 環境部 |
| **入力** | 削減目標、実績排出量 |
| **出力** | 進捗レポート、ギャップ分析 |
| **頻度** | 月次（進捗確認）、四半期（詳細分析） |
| **VL2寄与** | サステナビリティ → 目標達成に向けたPDCA |

**ドメイン操作**:
- `trackReductionProgress(target, actual)`: 進捗追跡
- `analyzeGap(target, actual)`: ギャップ分析
- `recommendReductionActions(gap)`: 削減アクション提案

---

## CL1-05: Order Management（受注管理）起源

### CL2-05-01: order-processing（受注処理）

#### CL3-05-01-01: order-registration（受注登録）

| 項目 | 内容 |
|------|------|
| **日本語名** | 受注登録 |
| **目的** | 顧客からの受注情報の登録 |
| **主要アクター** | 営業本部 |
| **入力** | 受注情報（品目、数量、納期、配送先） |
| **出力** | 受注データ、在庫引当結果 |
| **頻度** | 随時（受注発生都度） |
| **VL2寄与** | 安定供給体制 → 受注の確実な処理 |

**ドメイン操作**:
- `registerOrder(customer, items, deliveryDate)`: 受注登録
- `allocateInventory(order)`: 在庫引当
- `validateOrderFeasibility(order)`: 納期検証

**状態遷移**:
```
受付 → 引当中 → 引当完了 → 出荷指示済み → 出荷完了 → 完了
```

**PDL候補用語**:
- 受注（Order）
- 在庫引当（InventoryAllocation）
- 納期（DeliveryDate）

---

#### CL3-05-01-02: order-confirmation（受注確認通知）

| 項目 | 内容 |
|------|------|
| **日本語名** | 受注確認通知 |
| **目的** | 受注確認と納期回答の通知 |
| **主要アクター** | 営業本部 |
| **入力** | 受注登録結果、在庫引当結果 |
| **出力** | 受注確認通知、納期回答 |
| **頻度** | 随時（受注処理完了後） |
| **VL2寄与** | 安定供給体制 → 顧客への迅速な情報提供 |

**ドメイン操作**:
- `confirmOrder(order)`: 受注確認
- `notifyCustomer(order, confirmation)`: 顧客通知
- `updateDeliveryDate(order, newDate)`: 納期更新

---

### CL2-05-02: partner-integration（パートナー連携）

#### CL3-05-02-01: edi-integration（EDI連携）

| 項目 | 内容 |
|------|------|
| **日本語名** | EDI連携 |
| **目的** | 卸売・小売とのEDI（電子データ交換）連携 |
| **主要アクター** | IT部門、卸売業者、小売業者 |
| **入力** | EDIメッセージ（発注、出荷、請求） |
| **出力** | 処理済みEDIデータ |
| **頻度** | リアルタイム〜日次（メッセージ種別による） |
| **VL2寄与** | 安定供給体制 → パートナーとの効率的な情報連携 |

**ドメイン操作**:
- `receiveEdiMessage(message)`: EDIメッセージ受信
- `processEdiOrder(ediOrder)`: EDI発注処理
- `sendEdiResponse(response)`: EDI応答送信

**PDL候補用語**:
- EDIメッセージ（EdiMessage）
- 取引先コード（TradingPartnerCode）

---

#### CL3-05-02-02: partner-data-synchronization（パートナーデータ同期）

| 項目 | 内容 |
|------|------|
| **日本語名** | パートナーデータ同期 |
| **目的** | 取引先マスタ・商品マスタの同期 |
| **主要アクター** | IT部門 |
| **入力** | マスタ更新情報 |
| **出力** | 同期済みマスタデータ |
| **頻度** | 日次（定期同期）、随時（緊急更新） |
| **VL2寄与** | 安定供給体制 → 正確なデータによる取引精度向上 |

**ドメイン操作**:
- `syncPartnerMaster(partner)`: 取引先マスタ同期
- `syncProductMaster(partner)`: 商品マスタ同期
- `resolveDataConflict(conflict)`: データ競合解消

---

## PDL（Parasol Domain Language）候補一覧

### Core Domain 用語

| 用語（英語） | 用語（日本語） | 定義 | 関連CL3 |
|------------|--------------|------|--------|
| DemandForecast | 需要予測 | 将来の需要量の予測値とその信頼度 | CL3-01-01-02 |
| OptimalStockLevel | 適正在庫水準 | 欠品リスクと在庫コストを最適化した在庫量 | CL3-01-02-01 |
| SafetyStock | 安全在庫 | 需要変動に対するバッファ在庫量 | CL3-01-02-01 |
| DeliverySchedule | 配送計画 | 配送先・配送時間・車両の割当計画 | CL3-02-01-01 |
| JointTransport | 共同輸送 | 異業種間での輸送キャパシティ共有 | CL3-02-01-03 |
| DeliveryRoute | 配送ルート | 最適化された配送経路 | CL3-02-03-01 |
| WaterSource | 水源地 | 天然水の採水地点 | CL3-04-01-01 |
| NaturalWaterForest | 天然水の森 | 水源涵養のための保全林（21,000ha） | CL3-04-01-02 |

### VCI Domain 用語

| 用語（英語） | 用語（日本語） | 定義 | 関連CL3 |
|------------|--------------|------|--------|
| CriticalControlPoint | 重要管理点 | HACCP における監視必須ポイント | CL3-03-01-01 |
| CorrectiveAction | 是正措置 | 逸脱発生時の対応アクション | CL3-03-01-01 |
| Lot | ロット | 製造単位を識別する管理番号 | CL3-03-02-01 |
| Traceback | トレースバック | 製品から原材料への遡及追跡 | CL3-03-02-01 |
| TraceForward | トレースフォワード | 原材料から製品・出荷先への追跡 | CL3-03-02-01 |
| PalletPattern | パレットパターン | 商品のパレット積載パターン | CL3-02-02-04 |

### Supporting Domain 用語

| 用語（英語） | 用語（日本語） | 定義 | 関連CL3 |
|------------|--------------|------|--------|
| CarbonFootprint | カーボンフットプリント | 製品・活動のCO2排出量 | CL3-04-03-01 |
| EmissionFactor | 排出係数 | 活動量あたりのCO2排出量 | CL3-04-03-01 |
| ScopeEmission | Scope排出量 | GHGプロトコルのScope1/2/3分類 | CL3-04-03-01 |

### Generic Domain 用語

| 用語（英語） | 用語（日本語） | 定義 | 関連CL3 |
|------------|--------------|------|--------|
| Order | 受注 | 顧客からの注文情報 | CL3-05-01-01 |
| InventoryAllocation | 在庫引当 | 受注に対する在庫の確保 | CL3-05-01-01 |
| EdiMessage | EDIメッセージ | 電子データ交換の標準メッセージ | CL3-05-02-01 |

---

## BC（Bounded Context）マッピング候補

### BC候補一覧

| BC候補名 | 含まれるCL3 | TVDC | 優先度 |
|---------|-----------|------|--------|
| **DemandPlanningContext** | CL3-01-01-*, CL3-01-02-*, CL3-01-03-* | Core | 高 |
| **TransportPlanningContext** | CL3-02-01-*, CL3-02-03-*, CL3-02-04-* | Core | 高 |
| **WarehouseContext** | CL3-02-02-* | VCI | 高 |
| **FoodSafetyContext** | CL3-03-01-* | VCI | 高 |
| **TraceabilityContext** | CL3-03-02-* | VCI | 高 |
| **WaterSustainabilityContext** | CL3-04-01-* | Core | 高 |
| **EnvironmentalReportingContext** | CL3-04-02-*, CL3-04-03-* | Supporting | 中 |
| **OrderContext** | CL3-05-01-*, CL3-05-02-* | Generic | 中 |

### Context Map 関係候補

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Suntory SCM Context Map                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐          ┌──────────────────┐                     │
│  │ DemandPlanning   │ ───U───▶ │ TransportPlanning│                     │
│  │ Context [Core]   │          │ Context [Core]   │                     │
│  └────────┬─────────┘          └────────┬─────────┘                     │
│           │                             │                                │
│           │ D                           │ U                              │
│           ▼                             ▼                                │
│  ┌──────────────────┐          ┌──────────────────┐                     │
│  │ Warehouse        │ ◀───U─── │ Fleet/Route      │                     │
│  │ Context [VCI]    │          │ (traevo連携)     │                     │
│  └────────┬─────────┘          └──────────────────┘                     │
│           │                                                              │
│           │ D                                                            │
│           ▼                                                              │
│  ┌──────────────────┐          ┌──────────────────┐                     │
│  │ FoodSafety       │ ◀───P───▶│ Traceability     │                     │
│  │ Context [VCI]    │          │ Context [VCI]    │                     │
│  └──────────────────┘          │ (日立協創連携)   │                     │
│                                 └──────────────────┘                     │
│                                                                          │
│  ┌──────────────────┐          ┌──────────────────┐                     │
│  │ WaterSustain     │ ───CF───▶│ Environmental    │                     │
│  │ Context [Core]   │          │ Reporting [Supp] │                     │
│  └──────────────────┘          └──────────────────┘                     │
│                                                                          │
│  ┌──────────────────┐                                                   │
│  │ Order Context    │ ← 外部システム（EDI）                             │
│  │ [Generic]        │                                                   │
│  └──────────────────┘                                                   │
│                                                                          │
│  凡例: U=Upstream, D=Downstream, P=Partnership, CF=Conformist           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 価値トレーサビリティ確認

### VL2 → CL3 マッピング

| VL2（価値グループ） | 関連CL3（主要） | カバレッジ |
|-------------------|----------------|-----------|
| 安定供給体制 | CL3-01-01-*, CL3-01-02-*, CL3-01-03-*, CL3-05-01-* | 完全 ✅ |
| 物流効率化 | CL3-02-01-*, CL3-02-02-*, CL3-02-03-*, CL3-02-04-* | 完全 ✅ |
| 品質・安全 | CL3-03-01-*, CL3-03-02-* | 完全 ✅ |
| サステナビリティ | CL3-04-01-*, CL3-04-02-*, CL3-04-03-* | 完全 ✅ |

### 差別化要素の反映確認

| 差別化要素 | 反映CL3 | 状態 |
|-----------|--------|------|
| スマートロジスティクス | CL3-02-03-02（traevo連携） | ✅ |
| 2024年問題対応 | CL3-02-01-04, CL3-02-04-02 | ✅ |
| 天然水の森 | CL3-04-01-01, CL3-04-01-02 | ✅ |
| 日立協創トレーサビリティ | CL3-03-02-01 | ✅ |
| 異業種共同輸送（大王グループ） | CL3-02-01-03 | ✅ |
| パレット効率化（29%向上） | CL3-02-02-04 | ✅ |

---

## Phase 4への入力サマリー

### BC設計の入力

1. **8つのBC候補**が定義済み
2. **Context Map関係**の候補が整理済み
3. **TVDC分類**による優先度付けが完了

### API設計の入力

1. **39のCL3オペレーション**がドメイン操作として定義済み
2. **状態遷移**が主要オペレーションで定義済み
3. **PDL候補用語**が抽出済み

### 外部システム連携

| 連携先 | 連携CL3 | 連携方式 |
|-------|--------|---------|
| traevo（車両追跡） | CL3-02-03-02, CL3-02-04-01 | API連携 |
| 日立協創トレーサビリティ | CL3-03-02-01 | ブロックチェーン連携 |
| EDI（卸売・小売） | CL3-05-02-01 | EDI標準 |
| 大王グループ（共同輸送） | CL3-02-01-03 | パートナー連携 |

---

## 次のステップ

**Phase 4: Application Design（アーキテクチャ設計）**へ進む

```
→ /parasol:4-architecture
```

Phase 4では以下を実施:
1. BC境界の確定
2. Context Mapの詳細設計
3. サービス分割戦略
4. 統合パターンの選定

---

**作成**: Parasol V5 Phase 3-3
**価値トレーサビリティ**: VL2 → CL1 → CL2 → CL3 完全追跡可能
