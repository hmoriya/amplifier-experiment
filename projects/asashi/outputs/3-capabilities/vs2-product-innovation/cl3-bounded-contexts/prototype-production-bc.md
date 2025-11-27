# Bounded Context: prototype-production-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** prototype-production（試作生産）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | prototype-production-bc |
| **日本語名** | 試作生産 |
| **命名パターン** | `-production`（アクション型） |
| **命名理由** | 「試作管理」ではなく「生産」を採用。開発から量産への橋渡しという**生産活動**を明示。Production（生産）はパイロットプラントでの実際の製造活動を強調し、単なる管理ではなく価値を生み出す生産行為であることを表現 |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**prototype-production-bc**（試作生産バウンデッドコンテキスト）

#### 目的
開発段階の試作品を製造し、開発から量産への橋渡しを行う。パイロットプラント運営と試作品供給。

#### 責務
- パイロットスケールでの試験醸造・製造
- 開発レシピに基づく試作品の製造
- 量産移行前のスケールアップ検証
- パイロットプラント設備の運営・保守
- 試作品の品質データ収集・分析

#### チーム境界
- **担当組織**: R&D本部 パイロットプラント
- **チーム構成**:
  - パイロット醸造チーム（醸造技師、オペレーター）
  - 試作製造チーム（食品技術者、オペレーター）
  - 設備管理チーム（設備エンジニア）
- **推定人員**: 20-30名

---

### 2. ビジネスオペレーション詳細

#### OP1: パイロット醸造

**業務フロー:**
```
1. 醸造依頼受付
   └─ 製品開発BCからの試作依頼
   └─ レシピ・条件の確認
   └─ スケジュール調整

2. 醸造準備
   └─ 原材料の手配・受入
   └─ 酵母の活性化（発酵研究BCから受領）
   └─ 設備の準備・清掃

3. 醸造実施
   └─ 仕込み（糖化、煮沸）
   └─ 発酵（主発酵、後発酵）
   └─ 熟成・貯酒
   └─ 経時データ収集

4. 仕上げ・パッケージング
   └─ 濾過・調合
   └─ 試験容器への充填
   └─ サンプリング

5. 品質検査・報告
   └─ 理化学分析
   └─ 官能評価依頼
   └─ 醸造報告書作成
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 醸造記録は全工程をリアルタイムで記録すること |
| BR-OP1-02 | レシピからの逸脱は事前承認を得ること |
| BR-OP1-03 | 原材料のトレーサビリティを確保すること |
| BR-OP1-04 | 試作品は必ず官能評価を実施すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 醸造レシピ | 試作ビール |
| 酵母株 | 醸造データ |
| 原材料 | 品質分析結果 |

**トリガー:**
- 新製品開発
- 製品改良検証
- 製造条件最適化

---

#### OP2: 試作品製造

**業務フロー:**
```
1. 製造依頼受付
   └─ 飲料開発等からの試作依頼
   └─ 配合・製造条件の確認
   └─ 必要数量・納期確認

2. 製造準備
   └─ 原材料の手配
   └─ 機能性成分の受領（functional-ingredientsから）
   └─ 設備の選定・準備

3. 製造実施
   └─ 配合・混合
   └─ 殺菌・充填
   └─ 製造データ記録

4. 品質検査
   └─ 理化学分析
   └─ 微生物検査
   └─ 賞味期限試験（加速試験）

5. 試作品納品
   └─ 試作品の保管・管理
   └─ 開発BCへの納品
   └─ 製造報告書作成
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | 食品衛生法・JAS法を遵守すること |
| BR-OP2-02 | 微生物検査に合格した製品のみ納品すること |
| BR-OP2-03 | アレルゲン管理を徹底すること |
| BR-OP2-04 | 製造ロット管理を行うこと |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品配合 | 試作飲料・食品 |
| 機能性成分 | 製造データ |
| 原材料 | 品質検査結果 |

**トリガー:**
- 新製品開発
- 配合変更検証
- 消費者テスト用サンプル

---

#### OP3: スケールアップ検証

**業務フロー:**
```
1. 検証計画策定
   └─ スケールアップ条件の確認（process-engineeringから）
   └─ 検証項目の定義
   └─ 成功基準の設定

2. 段階的スケールアップ
   └─ 小スケール（10L〜100L）
   └─ 中スケール（100L〜1000L）
   └─ パイロットスケール（1000L〜）

3. データ収集・分析
   └─ 各スケールでの製造データ
   └─ 品質比較データ
   └─ 工程パラメータの最適化

4. 検証報告
   └─ スケールアップ成否判定
   └─ 製造スケールへの推奨条件
   └─ 残課題の特定
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 各スケールで品質同等性を確認すること |
| BR-OP3-02 | スケールアップ因子を記録すること |
| BR-OP3-03 | 最低3バッチの再現性を確認すること |
| BR-OP3-04 | 製造スケール推奨には品質保証の承認を得ること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| スケールアップ条件 | スケールアップ検証報告 |
| ラボスケールレシピ | 推奨製造条件 |
| 品質基準 | 品質比較データ |

**トリガー:**
- 新製品の量産化決定
- 製造拠点変更
- 製造プロセス変更

---

#### OP4: パイロットプラント管理

**業務フロー:**
```
1. 設備管理
   └─ 定期点検・保守
   └─ キャリブレーション
   └─ 設備更新計画

2. 生産計画管理
   └─ 試作スケジュール管理
   └─ 設備稼働計画
   └─ リソース配分

3. 品質管理
   └─ 環境モニタリング
   └─ 洗浄バリデーション
   └─ 計測機器管理

4. 安全管理
   └─ 作業安全管理
   └─ 環境安全管理
   └─ 緊急時対応
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 設備は年次定期点検を実施すること |
| BR-OP4-02 | 計測機器は定期キャリブレーションを実施すること |
| BR-OP4-03 | 製品切替時は適切な洗浄を実施すること |
| BR-OP4-04 | 安全教育を全作業者に実施すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 保守計画 | 設備稼働記録 |
| 試作依頼 | 生産スケジュール |
| 品質基準 | 環境モニタリングデータ |

**トリガー:**
- 定期保守時期
- 試作依頼
- 設備故障

---

### 3. ユビキタス言語（Ubiquitous Language）

#### ドメインオブジェクト（業務で扱うモノ・コト）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| PilotPlant | パイロットプラント | 試作品製造のための小規模製造設備 |
| PilotBatch | パイロットバッチ | パイロットスケールで製造された1ロット |
| PrototypeSample | 試作サンプル | 開発段階で製造された試作品 |
| BrewingRecord | 醸造記録 | 醸造工程の詳細記録 |
| ManufacturingRecord | 製造記録 | 製造工程の詳細記録 |
| QualityData | 品質データ | 試作品の品質分析結果 |
| ScaleUpValidation | スケールアップ検証 | 量産移行のための検証データ |

#### ビジネスルール（業務上の制約・ルール）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| BatchTraceability | バッチトレーサビリティ | 原材料から試作品までの追跡可能性 |
| CIP | 定置洗浄 | 設備を分解せずに行う洗浄方式 |
| HACCP | 危害分析重要管理点 | 食品安全管理システム |
| GMP | 適正製造基準 | 製造品質管理の基準 |

#### プロセス（業務フロー）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| PilotBrewing | パイロット醸造 | パイロットスケールでの試験醸造 |
| PrototypeManufacturing | 試作製造 | 試作品の製造プロセス |
| ScaleUpTrial | スケールアップ試験 | 段階的なスケール拡大検証 |
| EquipmentMaintenance | 設備保守 | 製造設備の点検・保守 |

#### イベント（業務上の重要な出来事）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| PilotBatchCompleted | パイロットバッチ完了 | パイロット醸造/製造が完了した |
| PrototypeSampleDelivered | 試作品納品 | 試作品が開発BCに納品された |
| ScaleUpValidated | スケールアップ検証完了 | スケールアップ検証が成功した |
| QualityApproved | 品質承認 | 試作品の品質が承認された |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: PilotBatch（パイロットバッチ）

**責務**: パイロットスケール製造のライフサイクル管理

```
PilotBatch [Aggregate Root]
├── batchId: BatchId [Value Object]
│   └── format: "PB-YYYY-NNNN"
├── requestId: RequestId [Value Object]
├── productType: ProductType [Value Object]
│   └── value: enum (BEER, SPIRITS, BEVERAGE, FOOD)
├── recipe: RecipeReference [Value Object]
│   ├── recipeId: RecipeId
│   ├── version: Version
│   └── sourceBC: BCId
├── scale: BatchScale [Value Object]
│   ├── targetVolume: number
│   ├── actualVolume: number
│   └── unit: VolumeUnit
├── ingredients: IngredientUsage[] [Entity]
│   ├── ingredientId: IngredientId
│   ├── lotNumber: string
│   ├── quantity: number
│   └── supplier: string
├── processRecords: ProcessRecord[] [Entity]
│   ├── recordId: RecordId
│   ├── step: ProcessStep
│   ├── startTime: DateTime
│   ├── endTime: DateTime
│   ├── parameters: Parameter[]
│   ├── measurements: Measurement[]
│   └── operator: OperatorId
├── qualityResults: QualityResult[] [Entity]
│   ├── testId: TestId
│   ├── testType: QualityTestType
│   ├── result: TestResult
│   └── testedAt: DateTime
├── samples: Sample[] [Entity]
│   ├── sampleId: SampleId
│   ├── quantity: number
│   ├── destination: string
│   └── deliveredAt: DateTime?
├── status: BatchStatus [Value Object]
│   └── value: enum (SCHEDULED, IN_PROGRESS, COMPLETED, APPROVED, REJECTED)
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-PB-01 | APPROVED statusには全必須qualityResultsがPASSであること |
| INV-PB-02 | 全ingredientsにlotNumberが記録されていること |
| INV-PB-03 | processRecordsは時系列順であること |
| INV-PB-04 | COMPLETED以降はprocessRecordsの追加不可 |

**主要メソッド:**
```
- createBatch(requestId, recipe, scale): PilotBatch
- recordIngredientUsage(ingredient, lot, quantity): void
- recordProcessStep(step, parameters, measurements): void
- addQualityResult(testType, result): void
- approveBatch(): void
- deliverSample(destination, quantity): Sample
```

---

#### 集約2: PilotPlantSchedule（パイロットプラントスケジュール）

**責務**: パイロットプラントの生産スケジュール管理

```
PilotPlantSchedule [Aggregate Root]
├── scheduleId: ScheduleId [Value Object]
├── period: SchedulePeriod [Value Object]
│   ├── startDate: Date
│   └── endDate: Date
├── allocations: ResourceAllocation[] [Entity]
│   ├── allocationId: AllocationId
│   ├── batchId: BatchId?
│   ├── equipmentId: EquipmentId
│   ├── timeSlot: TimeSlot
│   ├── purpose: enum (PRODUCTION, MAINTENANCE, CLEANING, IDLE)
│   └── status: enum (PLANNED, CONFIRMED, IN_PROGRESS, COMPLETED)
├── maintenanceWindows: MaintenanceWindow[] [Entity]
│   ├── windowId: WindowId
│   ├── equipmentId: EquipmentId
│   ├── type: MaintenanceType
│   ├── scheduledTime: TimeSlot
│   └── status: MaintenanceStatus
├── capacityUtilization: CapacityMetrics [Value Object]
│   ├── totalCapacity: number
│   ├── allocatedCapacity: number
│   └── utilizationRate: number
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-PS-01 | 同一equipmentに重複するallocationは不可 |
| INV-PS-02 | maintenanceWindowは製造allocationより優先 |
| INV-PS-03 | utilizationRateは0-100%の範囲 |

**主要メソッド:**
```
- createSchedule(period): PilotPlantSchedule
- allocateEquipment(batchId, equipmentId, timeSlot): ResourceAllocation
- schedulesMaintenance(equipmentId, type, time): MaintenanceWindow
- confirmAllocation(allocationId): void
- calculateUtilization(): CapacityMetrics
```

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **PilotBatchCompleted** | {batchId, productType, recipe, qualitySummary, completedAt} | パイロットバッチ製造完了時 | 依頼元BC, process-engineering |
| **PilotBatchApproved** | {batchId, productType, approvedAt} | 品質承認時 | 依頼元BC, 品質保証 |
| **SampleDelivered** | {sampleId, batchId, destination, quantity, deliveredAt} | 試作品納品時 | 依頼元BC, sensory-evaluation |
| **ScaleUpValidationCompleted** | {batchId, validationResult, recommendations, completedAt} | スケールアップ検証完了時 | process-engineering, A6生産技術 |
| **EquipmentMaintenanceRequired** | {equipmentId, maintenanceType, dueDate} | 保守時期到来時 | internal |

---

### 6. コンテキストマップ（Context Map）

```
┌─────────────────────────────────────────────────────────────────────┐
│                         技術提供BCs                                  │
│  ┌─────────────────┐              ┌─────────────────┐               │
│  │ fermentation-   │              │ process-        │               │
│  │ research-bc     │              │ engineering-bc  │               │
│  │ (酵母・レシピ)   │              │ (製造条件)       │               │
│  └────────┬────────┘              └────────┬────────┘               │
└───────────┼────────────────────────────────┼────────────────────────┘
            │                                │
            │    [Customer-Supplier]         │
            │                                │
            └────────────┬───────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │                     │
              │ prototype-          │
              │ production-bc       │
              │  (Supporting)       │
              │                     │
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ premium-beer-   │ │ craft-          │ │ beverage-       │
│ development-bc  │ │ innovation-     │ │ development-bc  │
│                 │ │ development-bc  │ │                 │
│ [Customer]      │ │ [Customer]      │ │ [Customer]      │
└─────────────────┘ └─────────────────┘ └─────────────────┘

              ┌─────────────────────┐
              │ sensory-            │
              │ evaluation-bc       │
              │                     │
              │ [Partnership]       │
              └─────────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| fermentation-research-bc | **Customer-Supplier** | 酵母株・発酵技術を受領 |
| process-engineering-bc | **Customer-Supplier** | 製造条件・スケールアップ条件を受領 |
| premium-beer-development-bc | **Customer** | 試作サービスを提供 |
| craft-innovation-development-bc | **Customer** | 試作サービスを提供 |
| beverage-development-bc | **Customer** | 試作サービスを提供 |
| sensory-evaluation-bc | **Partnership** | 試作品の官能評価を依頼 |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/batches` | POST | 新規パイロットバッチの作成 |
| `/batches/{id}/process-records` | POST | 製造工程記録の追加 |
| `/batches/{id}/quality-results` | POST | 品質検査結果の追加 |
| `/batches/{id}/approve` | POST | バッチの品質承認 |
| `/batches/{id}/samples` | POST | サンプル納品の記録 |
| `/schedules` | POST | 生産スケジュールの作成 |
| `/schedules/{id}/allocations` | POST | 設備割当の追加 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/batches` | GET | バッチ一覧取得 |
| `/batches/{id}` | GET | バッチ詳細取得 |
| `/batches/{id}/traceability` | GET | トレーサビリティ情報取得 |
| `/schedules` | GET | スケジュール取得 |
| `/schedules/availability` | GET | 設備空き状況取得 |
| `/equipment` | GET | 設備一覧取得 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| fermentation-research-bc | 酵母株・発酵レシピの参照 |
| process-engineering-bc | 製造条件・スケールアップ条件の参照 |
| sensory-evaluation-bc | 官能評価の依頼 |
| inventory-management-bc | 原材料在庫の確認・引当 |

---

## 次のステップ

### CL3完了後の推奨アクション

1. **VS2 CL3完了**
   - 全10サブドメインのBC定義完了

2. **Phase 4: Architecture への移行**
   - Context Map統合設計
   - イベント駆動アーキテクチャ設計
   - 技術スタック選定

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（prototype-production-bc定義）
**次のフェーズ:** Phase 4: Architecture
