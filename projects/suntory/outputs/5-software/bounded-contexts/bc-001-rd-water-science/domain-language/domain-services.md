# Domain Services - BC-001 R&D 水科学

## 概要

本ドキュメントは、BC-001 R&D 水科学のドメインサービスを定義する。

---

## WaterQualityEvaluationService 水質評価サービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 水質評価サービス |
| 英語名 | WaterQualityEvaluationService |

### 責務

水質検査結果を品質基準と照合し、合否判定を行う。
複数の基準との照合や、トレンド分析も提供する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| evaluate | TestResult[], QualityStandard | EvaluationResult | 検査結果を基準と照合し判定 |
| findApplicableStandard | productCategory, Date | QualityStandard | 適用する基準を特定 |
| analyzeTrend | sourceId, DateRange | TrendAnalysis | 水質トレンドを分析 |
| detectAnomaly | TestResult[] | AnomalyReport | 異常値を検出 |

### ビジネスルール

- 1項目でも基準外ならFAIL
- 誤差範囲内はRETEST
- 連続3回不合格でアラートエスカレーション

---

## WaterSourceValidationService 水源検証サービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 水源検証サービス |
| 英語名 | WaterSourceValidationService |

### 責務

水源登録時の検証を行う。重複チェック、位置情報検証、
初回検査の合格確認を実施する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| validateLocation | Location | ValidationResult | 位置情報の妥当性を検証 |
| checkDuplicate | Location | DuplicateCheckResult | 近傍の重複水源をチェック |
| validateInitialTest | testId | ValidationResult | 初回検査の合格を確認 |
| validateRegistration | WaterSource | ValidationResult | 登録全体の妥当性を検証 |

### ビジネスルール

- 位置は日本国内であること
- 半径100m以内に既存水源がないこと
- 初回検査が合格していること

---

## ConservationAreaCalculationService 涵養面積計算サービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 涵養面積計算サービス |
| 英語名 | ConservationAreaCalculationService |

### 責務

水源ごと、および全体の涵養面積を計算する。
期間指定での集計や、年度別推移の算出も行う。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| calculateTotal | sourceId | Decimal | 水源の累計涵養面積を計算 |
| calculateByPeriod | sourceId, DateRange | Decimal | 期間内の涵養面積を計算 |
| calculateAllSources | DateRange | Map<sourceId, Decimal> | 全水源の涵養面積を計算 |
| calculateYearlyTrend | sourceId | YearlyTrendData | 年度別推移を算出 |

### ビジネスルール

- 面積は小数点以下1桁まで
- 活動種別による面積算入ルールを適用

---

## PurificationSimulationService 浄水シミュレーションサービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 浄水シミュレーションサービス |
| 英語名 | PurificationSimulationService |

### 責務

浄水プロセスのシミュレーションを実行する。
入力水質から各処理ステップの効果を予測し、
出力水質を算出する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| simulate | PurificationProcess, inputQuality | SimulationResult | シミュレーションを実行 |
| predictStepOutput | ProcessStep, inputQuality | QualityPrediction | 1ステップの出力を予測 |
| validateDesign | PurificationProcess, targetStandard | DesignValidation | 設計が目標を達成するか検証 |
| optimizeParameters | PurificationProcess, targetStandard | OptimizedParameters | パラメータを最適化 |

### ビジネスルール

- 各ステップのモデルは科学的根拠に基づく
- 目標品質への到達可能性を判定
- 最適化は制約条件内で実施

---

## TechnologyTransferCoordinationService 技術移転調整サービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 技術移転調整サービス |
| 英語名 | TechnologyTransferCoordinationService |

### 責務

技術移転プロセスの調整を行う。
フェーズ管理、関係者通知、検証テストの評価を実施する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| initiateTransfer | processId, targetFactory | TechnologyTransfer | 移転を開始 |
| advancePhase | transferId, phaseNumber | PhaseResult | フェーズを進める |
| evaluateVerification | transferId, testResults | VerificationResult | 検証テストを評価 |
| notifyStakeholders | transferId, event | NotificationResult | 関係者に通知 |
| cancelTransfer | transferId, reason | CancellationResult | 移転を中止 |

### ビジネスルール

- フェーズは順次完了が必要
- 検証テストは製造部門と共同で実施
- 完了後3ヶ月はフォローアップ期間

---

## QualityAlertService 品質アラートサービス

| 項目 | 値 |
|------|-----|
| 日本語名 | 品質アラートサービス |
| 英語名 | QualityAlertService |

### 責務

品質に関するアラートを生成・管理する。
検査不合格、トレンド異常、基準超過などを監視する。

### 操作

| 操作 | 入力 | 出力 | 説明 |
|------|------|------|------|
| raiseAlert | alertType, details | Alert | アラートを発行 |
| escalate | alertId | EscalationResult | アラートをエスカレーション |
| acknowledge | alertId, userId | AcknowledgeResult | アラートを確認 |
| resolve | alertId, resolution | ResolveResult | アラートを解決 |
| getActiveAlerts | filters | Alert[] | 未対応アラートを取得 |

### ビジネスルール

- 重要度（高/中/低）に応じた通知先
- エスカレーションルールに従った自動エスカレーション
- 対応期限の管理

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
