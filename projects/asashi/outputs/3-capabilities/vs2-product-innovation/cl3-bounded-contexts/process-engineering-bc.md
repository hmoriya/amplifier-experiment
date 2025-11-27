# Bounded Context: process-engineering-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** process-engineering（プロセス技術）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | process-engineering-bc |
| **日本語名** | プロセス技術 |
| **命名パターン** | `-engineering`（アクション型） |
| **命名理由** | 「プロセス管理」ではなく「技術」を採用。研究から生産への橋渡しという技術的**構築**を表現。Engineering（技術）は設計・実装・最適化という能動的なエンジニアリング活動を強調 |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**process-engineering-bc**（プロセス技術バウンデッドコンテキスト）

#### 目的
研究成果を製造プロセスに実装するための技術開発を行い、スケールアップ・量産化を支援する。研究と生産の橋渡し役。

#### 責務
- ラボスケールから製造スケールへのスケールアップ研究
- 新製品の製造プロセス設計
- 既存工程の効率・品質最適化
- 研究成果の生産部門への技術移転支援
- 製造仕様書・技術文書の作成

#### チーム境界
- **担当組織**: R&D本部 生産技術研究所
- **チーム構成**:
  - スケールアップ研究チーム（化学工学エンジニア）
  - プロセス設計チーム（製造技術者）
  - 技術移転チーム（プロジェクトマネージャー）
- **推定人員**: 15-25名

---

### 2. ビジネスオペレーション詳細

#### OP1: スケールアップ研究

**業務フロー:**
```
1. スケールアップ要件定義
   └─ 対象レシピ・プロセスの特定
   └─ 目標製造規模の設定
   └─ 品質要件の確認

2. スケールアップ因子分析
   └─ 物質移動・熱移動の解析
   └─ スケール依存パラメータの特定
   └─ シミュレーションモデル構築

3. パイロットスケール検証
   └─ 段階的スケールアップ試験
   └─ パラメータ調整・最適化
   └─ 品質検証

4. 製造スケール条件決定
   └─ 最終製造条件の確定
   └─ 製造仕様書への反映
   └─ バリデーション計画策定
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | スケールアップは段階的（10x→100x→製造規模）に実施すること |
| BR-OP1-02 | 各スケールで品質同等性を確認すること |
| BR-OP1-03 | スケールアップ因子は定量的に記録すること |
| BR-OP1-04 | 製造条件は3ロット以上の再現性を確認すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| ラボスケールレシピ | スケールアップ条件 |
| 品質要件 | 製造スケール仕様 |
| 設備仕様 | スケールアップ報告書 |

**トリガー:**
- 新製品の量産化決定
- 製品改良の製造移行
- 製造拠点の変更

---

#### OP2: 製造プロセス設計

**業務フロー:**
```
1. 製品仕様の確認
   └─ 製品特性・品質基準の把握
   └─ 製造数量・頻度の確認
   └─ 使用設備の選定

2. プロセスフロー設計
   └─ 工程フローの設計
   └─ 各工程の条件設定
   └─ 制御パラメータの定義

3. 製造仕様書作成
   └─ 詳細製造手順の文書化
   └─ 品質管理ポイントの設定
   └─ 逸脱時対応の定義

4. 検証・承認
   └─ 技術レビュー
   └─ 生産部門との調整
   └─ 最終承認
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | 製造仕様書はGMP要件を満たすこと |
| BR-OP2-02 | 工程能力指数Cpk≧1.33を目標とすること |
| BR-OP2-03 | クリティカル工程は特定・管理すること |
| BR-OP2-04 | 変更管理プロセスに従うこと |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品仕様書 | 製造仕様書 |
| 品質基準 | プロセスフロー図 |
| 設備情報 | 工程管理基準 |

**トリガー:**
- 新製品の製造準備
- 製造拠点の新設・変更
- 設備更新

---

#### OP3: 工程最適化

**業務フロー:**
```
1. 現状分析
   └─ 製造データの収集・分析
   └─ ボトルネック工程の特定
   └─ 改善機会の洗い出し

2. 改善策立案
   └─ 条件変更による改善検討
   └─ 設備改良の検討
   └─ 費用対効果分析

3. 実証試験
   └─ パイロットスケールでの検証
   └─ 製造スケールでの確認
   └─ 品質への影響確認

4. 標準化・展開
   └─ 改善内容の標準化
   └─ 製造仕様書の更新
   └─ 他拠点への水平展開
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 改善前後のデータを定量的に比較すること |
| BR-OP3-02 | 品質への悪影響がないことを確認すること |
| BR-OP3-03 | コスト削減効果を算出すること |
| BR-OP3-04 | 改善記録を保管すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製造データ | 最適化パラメータ |
| 改善要件 | 改善報告書 |
| コスト目標 | 更新された製造仕様書 |

**トリガー:**
- コスト削減目標
- 品質改善要求
- 生産性向上要求

---

#### OP4: 技術移転支援

**業務フロー:**
```
1. 技術移転計画
   └─ 移転範囲の定義
   └─ スケジュール策定
   └─ 体制構築

2. 技術文書準備
   └─ 製造仕様書の最終化
   └─ トレーニング資料作成
   └─ トラブルシューティングガイド作成

3. 技術トレーニング
   └─ 生産部門への技術教育
   └─ OJT実施
   └─ 理解度確認

4. 量産立ち上げ支援
   └─ 初回製造の立会い
   └─ 問題解決支援
   └─ 安定稼働確認

5. 移転完了・引継ぎ
   └─ 量産移行判定
   └─ 残課題の引継ぎ
   └─ サポート体制移行
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 技術移転は文書化された手順に従うこと |
| BR-OP4-02 | 量産移行前に3ロット以上の安定生産を確認すること |
| BR-OP4-03 | 移転完了は品質保証部門の承認を得ること |
| BR-OP4-04 | 技術課題は完全に解決または引継ぎを完了すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 開発完了レシピ | 技術移転文書 |
| 製造仕様書 | トレーニング記録 |
| 生産計画 | 量産移行判定書 |

**トリガー:**
- 新製品の量産開始
- 生産拠点の追加
- 製造委託開始

---

### 3. ユビキタス言語（Ubiquitous Language）

#### ドメインオブジェクト（業務で扱うモノ・コト）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| ManufacturingSpecification | 製造仕様書 | 製品製造の詳細手順・条件を記載した文書 |
| ProcessFlow | プロセスフロー | 製造工程の流れを示した図 |
| ScaleUpFactor | スケールアップ因子 | スケール変更時に調整が必要なパラメータ |
| CriticalProcessParameter | 重要工程パラメータ | 品質に大きく影響する製造パラメータ |
| ProcessCapability | 工程能力 | 工程が規格内の製品を安定して作れる能力 |
| TechnologyTransferPackage | 技術移転パッケージ | 技術移転に必要な文書・データ一式 |

#### ビジネスルール（業務上の制約・ルール）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| GMP | 適正製造基準 | 医薬品・食品の製造品質管理基準 |
| Cpk | 工程能力指数 | 工程の安定性を示す統計指標 |
| ChangeControl | 変更管理 | 製造条件変更を管理するプロセス |
| Validation | バリデーション | プロセスが一貫して要求品質を満たすことの検証 |

#### プロセス（業務フロー）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| ScaleUp | スケールアップ | ラボスケールから製造スケールへの移行 |
| ProcessDesign | プロセス設計 | 製造工程の設計・条件設定 |
| Optimization | 最適化 | 製造条件の改善・効率化 |
| TechTransfer | 技術移転 | 研究部門から生産部門への技術引継ぎ |
| ProcessValidation | プロセスバリデーション | 製造プロセスの検証 |

#### イベント（業務上の重要な出来事）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| ScaleUpCompleted | スケールアップ完了 | 製造スケール条件が確定した |
| SpecificationApproved | 仕様承認 | 製造仕様書が承認された |
| ProcessOptimized | 工程最適化完了 | 製造工程の改善が完了した |
| TechTransferCompleted | 技術移転完了 | 生産部門への技術移転が完了した |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: ManufacturingProcess（製造プロセス）

**責務**: 製造プロセスの設計・管理

```
ManufacturingProcess [Aggregate Root]
├── processId: ProcessId [Value Object]
├── productId: ProductId [Value Object]
├── version: Version [Value Object]
├── processFlow: ProcessFlow [Entity]
│   ├── steps: ProcessStep[]
│   │   ├── stepId: StepId
│   │   ├── name: string
│   │   ├── sequence: number
│   │   ├── parameters: ProcessParameter[]
│   │   ├── criticalParameters: CriticalParameter[]
│   │   └── controlPoints: ControlPoint[]
│   └── totalDuration: Duration
├── specification: ManufacturingSpecification [Entity]
│   ├── documentId: DocumentId
│   ├── content: string (markdown)
│   ├── revision: number
│   ├── approvedBy: UserId
│   └── approvedAt: Date
├── scaleUpData: ScaleUpData [Entity]
│   ├── labScale: ScaleConditions
│   ├── pilotScale: ScaleConditions
│   ├── productionScale: ScaleConditions
│   └── scalingFactors: ScalingFactor[]
├── validationStatus: ValidationStatus [Value Object]
│   └── value: enum (NOT_VALIDATED, IN_PROGRESS, VALIDATED)
├── status: ProcessStatus [Value Object]
│   └── value: enum (DRAFT, APPROVED, PRODUCTION, DEPRECATED)
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-MP-01 | PRODUCTION statusにはVALIDATED validationStatusが必要 |
| INV-MP-02 | processFlowのstepsは連続したsequenceを持つこと |
| INV-MP-03 | criticalParametersには許容範囲が定義されていること |
| INV-MP-04 | specificationはAPPROVED status以降は変更不可（新版作成） |

**主要メソッド:**
```
- createProcess(productId, processFlow): ManufacturingProcess
- addScaleUpData(scale, conditions): void
- submitForApproval(): void
- approve(approverId): void
- startValidation(): void
- completeValidation(results): void
```

---

#### 集約2: TechnologyTransfer（技術移転）

**責務**: 技術移転プロジェクトの管理

```
TechnologyTransfer [Aggregate Root]
├── transferId: TransferId [Value Object]
├── processId: ProcessId [Value Object]
├── sourceOrg: OrganizationId [Value Object]
├── targetOrg: OrganizationId [Value Object]
├── transferPackage: TransferPackage [Entity]
│   ├── specifications: DocumentReference[]
│   ├── trainingMaterials: DocumentReference[]
│   ├── troubleshootingGuide: DocumentReference
│   └── supplementaryData: DocumentReference[]
├── trainingRecords: TrainingRecord[] [Entity]
│   ├── recordId: RecordId
│   ├── trainee: UserId
│   ├── topic: string
│   ├── completedAt: Date
│   └── assessmentResult: AssessmentResult
├── productionTrials: ProductionTrial[] [Entity]
│   ├── trialId: TrialId
│   ├── date: Date
│   ├── result: TrialResult
│   └── issues: Issue[]
├── status: TransferStatus [Value Object]
│   └── value: enum (PLANNING, DOCUMENTATION, TRAINING, TRIAL, COMPLETED)
├── milestones: Milestone[] [Entity]
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-TT-01 | COMPLETEDには最低3回の成功したproductionTrialsが必要 |
| INV-TT-02 | TRAININGフェーズ前にtransferPackageが完成していること |
| INV-TT-03 | 全対象者のtrainingRecordsがPASS以上であること |

**主要メソッド:**
```
- createTransfer(processId, sourceOrg, targetOrg): TechnologyTransfer
- prepareDocuments(): void
- recordTraining(trainee, topic, result): void
- conductTrial(): ProductionTrial
- completeTransfer(): void
```

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **ScaleUpCompleted** | {processId, productId, productionConditions, completedAt} | スケールアップ条件確定時 | prototype-production |
| **ManufacturingSpecApproved** | {processId, specificationId, version, approvedAt} | 製造仕様書承認時 | prototype-production, A6生産技術 |
| **ProcessValidated** | {processId, validationResults, validatedAt} | プロセスバリデーション完了時 | A6生産技術, 品質保証 |
| **TechTransferCompleted** | {transferId, processId, targetOrg, completedAt} | 技術移転完了時 | A6生産技術 |

---

### 6. コンテキストマップ（Context Map）

```
┌─────────────────────────────────────────────────────────────┐
│                fermentation-research-bc                      │
│                      (Upstream)                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │                     │
               │ process-engineering-│
               │ bc (Supporting)     │
               │                     │
               └──────────┬──────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ prototype-      │ │ premium-beer-   │ │ A6 生産技術     │
│ production-bc   │ │ development-bc  │ │ （外部VS）       │
│                 │ │                 │ │                 │
│ [Customer-      │ │ [Partnership]   │ │ [Conformist]    │
│  Supplier]      │ │                 │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| fermentation-research-bc | **Conformist** | 発酵研究の知見・レシピに従う |
| prototype-production-bc | **Customer-Supplier** | 製造条件を試作生産に提供 |
| premium-beer-development-bc | **Partnership** | 製品開発と協力して製造プロセスを設計 |
| A6生産技術 | **Conformist** | 量産技術・設備情報を受領 |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/processes` | POST | 新規製造プロセスの作成 |
| `/processes/{id}/scaleup` | POST | スケールアップデータの追加 |
| `/processes/{id}/approve` | POST | 製造仕様書の承認 |
| `/processes/{id}/validate` | POST | バリデーションの実施 |
| `/transfers` | POST | 技術移転プロジェクトの開始 |
| `/transfers/{id}/complete` | POST | 技術移転の完了 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/processes` | GET | 製造プロセス一覧取得 |
| `/processes/{id}` | GET | プロセス詳細取得 |
| `/processes/{id}/specification` | GET | 製造仕様書取得 |
| `/transfers/{id}` | GET | 技術移転状況取得 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| fermentation-research-bc | 発酵レシピ・技術知見の参照 |
| identity-management-bc | 技術者認証・権限管理 |
| document-management-bc | 技術文書の管理 |

---

## 次のステップ

### CL3完了後の推奨アクション

1. **他のSupporting サブドメインのCL3定義**
   - sensory-evaluation-bc
   - prototype-production-bc

2. **Phase 4: Architecture への移行**
   - A6生産技術との統合設計
   - 製造実行システム（MES）との連携設計

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（process-engineering-bc定義）
**次のフェーズ:** 他Supporting SDのCL3 または Phase 4: Architecture
