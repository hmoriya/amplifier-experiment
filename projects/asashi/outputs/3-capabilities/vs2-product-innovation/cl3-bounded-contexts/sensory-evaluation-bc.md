# Bounded Context: sensory-evaluation-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** sensory-evaluation（官能評価）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | sensory-evaluation-bc |
| **日本語名** | 官能評価 |
| **命名パターン** | `-evaluation`（アクション型） |
| **命名理由** | 「品質管理」ではなく「評価」を採用。判断・フィードバックという**能動的活動**を表現。Evaluation（評価）は品質の門番として製品の味・香り・外観を評価し、開発へフィードバックを提供する役割を明確化 |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**sensory-evaluation-bc**（官能評価バウンデッドコンテキスト）

#### 目的
全製品の官能評価（味・香り・外観等）を実施し、品質判定と製品改良のフィードバックを提供する。品質の門番役。

#### 責務
- 専門パネルによる官能評価の実施
- 一般消費者を対象とした消費者テストの実施
- 官能評価パネラーの育成・管理
- 製品別評価基準の設定・更新
- 評価結果の分析・フィードバック

#### チーム境界
- **担当組織**: R&D本部 官能評価センター
- **チーム構成**:
  - 官能評価チーム（評価専門家、パネルリーダー）
  - 消費者調査チーム（リサーチャー）
  - パネル管理チーム（トレーナー）
- **推定人員**: 10-20名（専門パネラー除く）

---

### 2. ビジネスオペレーション詳細

#### OP1: 官能評価実施

**業務フロー:**
```
1. 評価依頼受付
   └─ 開発BCからの評価依頼
   └─ 評価目的・項目の確認
   └─ スケジュール調整

2. 評価準備
   └─ サンプル準備・管理
   └─ 評価シートの準備
   └─ パネラーの選定・招集

3. 評価実施
   └─ ブラインドテスト実施
   └─ 記述式評価
   └─ スコアリング

4. 結果分析・報告
   └─ 統計解析
   └─ 評価コメントの整理
   └─ フィードバックレポート作成

5. 開発BCへの報告
   └─ 結果報告会
   └─ 改善提案
   └─ 追加評価の調整
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 評価はダブルブラインド方式で実施すること |
| BR-OP1-02 | 最低5名以上の訓練済みパネラーで評価すること |
| BR-OP1-03 | サンプル温度・提供順序は標準化すること |
| BR-OP1-04 | 評価結果は統計的有意性を確認すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 評価依頼 | 評価スコア |
| サンプル | フィードバックレポート |
| 評価基準 | 統計解析結果 |

**トリガー:**
- 開発段階ゲート
- 製品改良検証
- 品質問題調査

---

#### OP2: 消費者テスト

**業務フロー:**
```
1. テスト計画
   └─ テスト目的の明確化
   └─ ターゲット消費者の定義
   └─ サンプルサイズ設計

2. 参加者リクルート
   └─ 募集条件の設定
   └─ スクリーニング
   └─ 参加者確保

3. テスト実施
   └─ 中央会場テスト（CLT）
   └─ ホームユーステスト（HUT）
   └─ オンラインテスト

4. データ分析
   └─ 嗜好性データの集計
   └─ セグメント分析
   └─ 競合比較分析

5. 報告・提言
   └─ 消費者インサイト報告
   └─ 製品改良提言
   └─ マーケティング示唆
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | 定量調査はn≧100を基本とすること |
| BR-OP2-02 | ターゲット消費者の代表性を確保すること |
| BR-OP2-03 | 競合製品との比較を含めること |
| BR-OP2-04 | 個人情報保護法を遵守すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| テスト計画書 | 消費者評価データ |
| サンプル | 嗜好性分析レポート |
| 競合製品 | 消費者インサイト |

**トリガー:**
- 新製品発売前検証
- 製品リニューアル判断
- 市場動向調査

---

#### OP3: パネル管理

**業務フロー:**
```
1. パネラー募集・選抜
   └─ 募集告知
   └─ 感覚能力テスト
   └─ 適性評価

2. 基礎トレーニング
   └─ 味覚・嗅覚の基礎教育
   └─ 評価手法の習得
   └─ 評価語彙の統一

3. 専門トレーニング
   └─ 製品カテゴリ別訓練
   └─ 識別能力向上訓練
   └─ 記述能力向上訓練

4. 能力維持・管理
   └─ 定期的な能力評価
   └─ 継続トレーニング
   └─ パフォーマンスモニタリング

5. パネラー情報管理
   └─ 資格・能力記録
   └─ 参加履歴管理
   └─ 報酬管理
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | パネラーは年1回以上の能力再評価を受けること |
| BR-OP3-02 | 識別テスト正答率80%以上を維持すること |
| BR-OP3-03 | 評価バイアスを定期的にチェックすること |
| BR-OP3-04 | パネラープールは最低30名を維持すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 応募者情報 | 認定パネラー |
| トレーニング計画 | 能力評価記録 |
| 評価参加記録 | パネラープロファイル |

**トリガー:**
- パネラー不足
- 能力低下検出
- 新製品カテゴリ対応

---

#### OP4: 評価基準管理

**業務フロー:**
```
1. 基準設計
   └─ 製品カテゴリの特性把握
   └─ 評価項目の選定
   └─ 評価スケールの設計

2. 基準検証
   └─ パイロット評価
   └─ 再現性・識別力確認
   └─ パネラー間一致度確認

3. 基準承認・登録
   └─ 技術レビュー
   └─ 品質保証部門承認
   └─ 評価基準マスター登録

4. 基準維持・更新
   └─ 定期見直し
   └─ 製品変更への対応
   └─ 市場変化への対応
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | 評価基準は品質保証部門の承認を得ること |
| BR-OP4-02 | 基準は3年ごとに見直すこと |
| BR-OP4-03 | パネラー間一致度(ICC)≧0.7を確保すること |
| BR-OP4-04 | 製品仕様変更時は基準適合性を確認すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 製品仕様 | 評価基準書 |
| 品質方針 | 評価シート |
| 業界標準 | 基準マスターエントリ |

**トリガー:**
- 新製品カテゴリ追加
- 品質方針変更
- 定期見直し時期

---

### 3. ユビキタス言語（Ubiquitous Language）

#### ドメインオブジェクト（業務で扱うモノ・コト）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| SensoryPanel | 官能評価パネル | 訓練された評価者の集団 |
| Panelist | パネラー | 官能評価を行う訓練された評価者 |
| EvaluationCriteria | 評価基準 | 製品カテゴリ別の評価項目・基準 |
| SensoryProfile | 官能プロファイル | 製品の官能特性を数値化したもの |
| FlavorWheel | フレーバーホイール | 味・香りの分類体系 |
| ScoreSheet | 評価シート | 評価を記録するシート |
| ConsumerTest | 消費者テスト | 一般消費者による製品評価 |
| BlindTest | ブラインドテスト | 製品情報を隠した評価 |

#### ビジネスルール（業務上の制約・ルール）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| DoubleBlind | ダブルブラインド | 評価者・提供者双方が製品情報を知らない状態 |
| ICC | 級内相関係数 | パネラー間の評価一致度指標 |
| TriangleTest | 三点識別試験 | 3つのサンプルから異なる1つを識別するテスト |
| QDA | 定量的記述分析 | 官能特性を定量的に記述する手法 |

#### プロセス（業務フロー）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| SensoryEvaluation | 官能評価 | 専門パネルによる製品の感覚的評価 |
| ConsumerResearch | 消費者調査 | 一般消費者の嗜好・反応を調査するプロセス |
| PanelTraining | パネルトレーニング | パネラーの評価能力を向上させる訓練 |
| CriteriaValidation | 基準検証 | 評価基準の妥当性を確認するプロセス |

#### イベント（業務上の重要な出来事）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| EvaluationCompleted | 評価完了 | 官能評価が完了しレポートが作成された |
| ConsumerTestCompleted | 消費者テスト完了 | 消費者テストが完了した |
| PanelistCertified | パネラー認定 | パネラーが正式に認定された |
| CriteriaApproved | 基準承認 | 評価基準が承認された |
| QualityGatePassed | 品質ゲート通過 | 官能評価による品質ゲートを通過した |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: SensoryEvaluation（官能評価）

**責務**: 官能評価セッションの管理

```
SensoryEvaluation [Aggregate Root]
├── evaluationId: EvaluationId [Value Object]
├── requestingBC: BCId [Value Object]
├── productId: ProductId [Value Object]
├── evaluationType: EvaluationType [Value Object]
│   └── value: enum (DESCRIPTIVE, DISCRIMINATIVE, AFFECTIVE)
├── samples: Sample[] [Entity]
│   ├── sampleId: SampleId
│   ├── code: string (ブラインドコード)
│   ├── description: string
│   └── preparationConditions: PreparationConditions
├── criteria: EvaluationCriteria [Value Object]
│   └── criteriaId: CriteriaId
├── panel: EvaluationPanel [Entity]
│   ├── panelists: PanelistId[]
│   ├── minimumRequired: number
│   └── actualParticipants: number
├── sessions: EvaluationSession[] [Entity]
│   ├── sessionId: SessionId
│   ├── date: Date
│   ├── results: EvaluationResult[]
│   └── comments: Comment[]
├── analysis: StatisticalAnalysis [Entity]
│   ├── descriptiveStats: DescriptiveStats
│   ├── inferentialStats: InferentialStats
│   └── conclusion: Conclusion
├── status: EvaluationStatus [Value Object]
│   └── value: enum (REQUESTED, SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED)
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-SE-01 | COMPLETED statusには最低minimumRequired名のパネラー参加が必要 |
| INV-SE-02 | 全サンプルにブラインドコードが付与されていること |
| INV-SE-03 | 評価結果は統計的有意性を含むこと |
| INV-SE-04 | analysisはIN_PROGRESS以降でのみ更新可能 |

**主要メソッド:**
```
- requestEvaluation(requestingBC, productId, evaluationType): SensoryEvaluation
- scheduleSessions(dates, panelists): void
- recordResults(sessionId, results): void
- performAnalysis(): StatisticalAnalysis
- generateReport(): EvaluationReport
```

---

#### 集約2: Panelist（パネラー）

**責務**: パネラーの能力・資格管理

```
Panelist [Aggregate Root]
├── panelistId: PanelistId [Value Object]
├── personalInfo: PersonalInfo [Value Object]
│   ├── name: string
│   ├── employeeId: EmployeeId?
│   └── contactInfo: ContactInfo
├── qualifications: Qualification[] [Entity]
│   ├── qualificationId: QualificationId
│   ├── category: ProductCategory
│   ├── level: enum (TRAINEE, QUALIFIED, EXPERT)
│   ├── certifiedDate: Date
│   └── expiryDate: Date
├── capabilities: SensoryCapability [Value Object]
│   ├── tasteThreshold: ThresholdScores
│   ├── odorThreshold: ThresholdScores
│   ├── discriminationAbility: number
│   └── descriptiveAbility: number
├── trainingHistory: TrainingRecord[] [Entity]
│   ├── trainingId: TrainingId
│   ├── type: TrainingType
│   ├── completedDate: Date
│   └── result: TrainingResult
├── evaluationHistory: EvaluationParticipation[] [Entity]
│   ├── evaluationId: EvaluationId
│   ├── date: Date
│   └── performance: PerformanceScore
├── status: PanelistStatus [Value Object]
│   └── value: enum (ACTIVE, INACTIVE, SUSPENDED)
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-PL-01 | QUALIFIED以上にはdiscriminationAbility≧80%が必要 |
| INV-PL-02 | 資格は有効期限内であること |
| INV-PL-03 | ACTIVEには最低1つの有効な資格が必要 |
| INV-PL-04 | 年1回以上の能力評価記録があること |

**主要メソッド:**
```
- registerPanelist(personalInfo): Panelist
- addQualification(category, level): void
- updateCapabilities(newCapabilities): void
- recordTraining(training, result): void
- suspend(reason): void
- reactivate(): void
```

---

#### 集約3: EvaluationCriteria（評価基準）

**責務**: 製品カテゴリ別評価基準の管理

```
EvaluationCriteria [Aggregate Root]
├── criteriaId: CriteriaId [Value Object]
├── productCategory: ProductCategory [Value Object]
├── version: Version [Value Object]
├── attributes: SensoryAttribute[] [Entity]
│   ├── attributeId: AttributeId
│   ├── name: string (例: "苦味", "ホップ香")
│   ├── definition: string
│   ├── scale: EvaluationScale
│   ├── anchors: ScaleAnchor[]
│   └── weight: number
├── referenceStandards: ReferenceStandard[] [Entity]
│   ├── standardId: StandardId
│   ├── attributeId: AttributeId
│   ├── description: string
│   └── intensity: number
├── acceptanceCriteria: AcceptanceCriteria [Value Object]
│   ├── minimumScores: Map<AttributeId, number>
│   └── overallMinimum: number
├── validationRecord: ValidationRecord [Entity]
│   ├── validatedDate: Date
│   ├── iccScore: number (級内相関係数)
│   └── discriminationPower: number
├── status: CriteriaStatus [Value Object]
│   └── value: enum (DRAFT, VALIDATED, APPROVED, DEPRECATED)
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-EC-01 | APPROVEDにはiccScore≧0.7が必要 |
| INV-EC-02 | 全attributesにはdefinitionとscaleが必要 |
| INV-EC-03 | acceptanceCriteriaは全必須attributeをカバーすること |
| INV-EC-04 | APPROVED後は変更不可（新版を作成） |

**主要メソッド:**
```
- createCriteria(productCategory): EvaluationCriteria
- addAttribute(name, definition, scale): void
- setReferenceStandard(attributeId, standard): void
- validate(): ValidationResult
- approve(approverId): void
```

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **EvaluationCompleted** | {evaluationId, productId, overallScore, recommendation, completedAt} | 官能評価完了時 | premium-beer-dev, craft-innovation-dev, beverage-dev |
| **QualityGatePassed** | {evaluationId, productId, gate, passedAt} | 品質ゲート通過時 | 依頼元BC, 品質保証 |
| **QualityGateFailed** | {evaluationId, productId, gate, failedAttributes, failedAt} | 品質ゲート不通過時 | 依頼元BC, 品質保証 |
| **ConsumerTestCompleted** | {testId, productId, overallPreference, insights, completedAt} | 消費者テスト完了時 | 依頼元BC, マーケティング |
| **CriteriaApproved** | {criteriaId, productCategory, version, approvedAt} | 評価基準承認時 | 全製品開発BC |

---

### 6. コンテキストマップ（Context Map）

```
┌─────────────────────────────────────────────────────────────────────┐
│                         製品開発BCs                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │premium-beer-│  │craft-       │  │spirits-     │  │beverage-    │ │
│  │development  │  │innovation   │  │development  │  │development  │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
└─────────┼────────────────┼────────────────┼────────────────┼────────┘
          │                │                │                │
          │   [Shared Service - Open Host Service]           │
          │                │                │                │
          └────────────────┴───────┬────────┴────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │                          │
                    │  sensory-evaluation-bc   │
                    │      (Supporting)        │
                    │                          │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │    A7 品質保証           │
                    │   （外部VS）             │
                    │                          │
                    │  [Conformist]            │
                    └──────────────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| premium-beer-development-bc | **Open Host Service** | 官能評価サービスを提供 |
| craft-innovation-development-bc | **Open Host Service** | 官能評価サービスを提供 |
| spirits-development-bc | **Open Host Service** | 官能評価サービスを提供 |
| beverage-development-bc | **Open Host Service** | 官能評価サービスを提供 |
| A7 品質保証 | **Conformist** | 品質基準・判定基準に従う |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/evaluations` | POST | 新規官能評価の依頼 |
| `/evaluations/{id}/sessions` | POST | 評価セッションのスケジュール |
| `/evaluations/{id}/results` | POST | 評価結果の記録 |
| `/consumer-tests` | POST | 消費者テストの依頼 |
| `/panelists` | POST | パネラーの登録 |
| `/criteria` | POST | 新規評価基準の作成 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/evaluations` | GET | 評価一覧取得 |
| `/evaluations/{id}` | GET | 評価詳細・結果取得 |
| `/evaluations/{id}/report` | GET | 評価レポート取得 |
| `/consumer-tests/{id}` | GET | 消費者テスト結果取得 |
| `/criteria` | GET | 評価基準一覧取得 |
| `/criteria/{id}` | GET | 評価基準詳細取得 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| A7 品質保証 | 品質判定基準の参照 |
| identity-management-bc | パネラー・社員認証 |
| scheduling-bc | 評価セッションのスケジューリング |

---

## 次のステップ

### CL3完了後の推奨アクション

1. **他のSupporting サブドメインのCL3定義**
   - prototype-production-bc

2. **Phase 4: Architecture への移行**
   - 全製品開発BCとの統合設計
   - 品質保証システムとの連携設計

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（sensory-evaluation-bc定義）
**次のフェーズ:** 他Supporting SDのCL3 または Phase 4: Architecture
