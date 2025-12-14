# Bounded Context: vs2-skill-assessment-bc

プロジェクト: staff-v5-test
サブドメイン: vs2-skill-assessment
作成日: 2025-01-21

## 1. Bounded Context 概要

### 目的
個人の現在スキルレベルを多面的に評価し、市場要求との差分を明確化することで、戦略的なキャリア開発の基盤を提供する

### 責務
- スキルの客観的評価と可視化
- 市場要求スキルとのギャップ分析
- スキル履歴の管理と成長追跡
- 市場価値の算定と予測
- 評価データの信頼性確保

### チーム境界
**担当チーム**: Skill Assessment Team
- スキルアセスメント専門家: 2名
- バックエンドエンジニア: 3名
- データサイエンティスト: 1名
- フロントエンドエンジニア: 2名
- QAエンジニア: 1名

### ドメインタイプ
Core Domain（競争優位の源泉）

---

## 2. ビジネスオペレーション詳細

### スキル診断実施

**業務フロー**:
1. 評価対象者の選定・通知
2. 評価方法の選択（オンライン/実技/360度）
3. アセスメント環境の準備
4. 評価実施とデータ収集
5. 結果の自動採点・分析
6. レポート生成と通知

**業務ルール**:
- 評価は6ヶ月ごとに定期実施（最低年2回）
- 360度評価は3名以上の評価者が必要
- 実技テストは認定評価者による監督必須
- 不正防止のため同一IPからの複数回答は制限

**入力**:
- 評価対象者情報（ID、現在職種、経験年数）
- 評価種別とスケジュール
- 評価者リスト（360度評価の場合）

**出力**:
- スキル評価結果（スコア、レベル、詳細分析）
- 成長度レポート
- 推奨改善アクション

**トリガー**:
- 定期評価サイクル到達
- マネージャーからの評価リクエスト
- 本人からの自己評価申請

### スキルギャップ分析

**業務フロー**:
1. 現在スキルレベルの取得
2. 目標職種・レベルの設定
3. 市場要求スキルの参照
4. ギャップの計算と可視化
5. 優先順位付けとロードマップ作成

**業務ルール**:
- ギャップは5段階で評価（Critical/High/Medium/Low/None）
- 市場データは月次で更新
- Critical ギャップは即時通知

**入力**:
- 現在スキル評価結果
- 目標職種・ポジション
- 市場スキル要求データ

**出力**:
- ギャップ分析レポート
- 優先学習領域リスト
- 推定習得期間

### スキルポートフォリオ管理

**業務フロー**:
1. 評価結果の記録・蓄積
2. 外部資格・認定の登録
3. プロジェクト実績の紐付け
4. スキル証跡のアップロード
5. ポートフォリオの公開設定

**業務ルール**:
- 全評価履歴は永続保存（削除不可）
- 外部資格は検証後のみ登録可能
- 機密プロジェクトは非公開設定必須

### 市場価値算定

**業務フロー**:
1. スキルセットの総合評価
2. 市場給与データとの照合
3. 経験・実績の加味
4. 地域・業界補正の適用
5. 推定年収レンジの算出

**業務ルール**:
- 算定は四半期ごとに更新
- 3つ以上のデータソースから検証
- 個人情報保護のため匿名化処理必須

---

## 3. ユビキタス言語（Ubiquitous Language）

### 主要概念

**Skill（スキル）**
個人が保有する特定の能力や知識。技術スキル（ハードスキル）と対人スキル（ソフトスキル）に大別される。

**Skill Level（スキルレベル）**
スキルの習熟度を表す5段階評価。
- Level 1: Beginner（初心者）
- Level 2: Elementary（初級）
- Level 3: Intermediate（中級）
- Level 4: Advanced（上級）
- Level 5: Expert（エキスパート）

**Assessment（アセスメント）**
スキルレベルを測定する評価活動。オンラインテスト、実技評価、360度フィードバックなどの手法がある。

**Skill Gap（スキルギャップ）**
現在のスキルレベルと目標レベル（または市場要求レベル）との差分。

**Skill Portfolio（スキルポートフォリオ）**
個人の全スキル、評価履歴、資格、実績を統合した総合的なスキル資産。

**Market Value（市場価値）**
保有スキルセットに基づく労働市場での推定価値。通常は年収レンジで表現。

**Assessment Method（評価手法）**
- Online Assessment: システム上での自動評価
- Practical Test: 実技による評価
- 360-degree Feedback: 上司・同僚・部下からの多面評価
- Self Assessment: 自己評価

**Skill Category（スキルカテゴリ）**
- Technical Skills: プログラミング、データ分析等
- Business Skills: プロジェクト管理、戦略立案等
- Soft Skills: コミュニケーション、リーダーシップ等
- Industry Skills: 業界特有の専門知識

**Verification Status（検証状態）**
- Verified: 第三者により検証済み
- Self-Reported: 自己申告（未検証）
- Expired: 有効期限切れ

---

## 4. 集約設計（Aggregates）

### Aggregate 1: SkillAssessment（スキル評価集約）

**集約ルート**: SkillAssessment
**エンティティ**: 
- AssessmentSession（評価セッション）
- AssessmentResult（評価結果）

**値オブジェクト**: 
- AssessmentId（評価ID）
- SkillId（スキルID）
- SkillLevel（1-5のレベル）
- Score（0-100の数値スコア）
- AssessmentMethod（評価手法）
- EvaluatorInfo（評価者情報）

**不変条件（Invariants）**:
- 評価は必ず完了または中断のいずれかの状態
- 360度評価は最低3名の評価者が必要
- スコアは0-100の範囲内
- 一度確定した評価結果は変更不可（新規評価として記録）

**主要操作**:
```typescript
class SkillAssessment {
  // コマンド
  create(personId, skillIds, method): SkillAssessment
  startSession(): AssessmentSession
  submitAnswer(questionId, answer): void
  complete360Feedback(evaluatorId, feedback): void
  finalizeAssessment(): AssessmentResult
  cancelAssessment(reason): void

  // クエリ
  getProgress(): AssessmentProgress
  getResults(): AssessmentResult[]
  canFinalize(): boolean
}
```

---

### Aggregate 2: SkillPortfolio（スキルポートフォリオ集約）

**集約ルート**: SkillPortfolio
**エンティティ**: 
- SkillRecord（スキル記録）
- ExternalCertification（外部資格）

**値オブジェクト**:
- PersonId（人材ID）
- SkillSnapshot（特定時点のスキル状態）
- VerificationStatus（検証状態）
- EvidenceDocument（証跡ドキュメント）
- PortfolioVisibility（公開設定）

**不変条件（Invariants）**:
- ポートフォリオは1人につき1つ
- 評価履歴は時系列で保存（削除不可）
- 外部資格は検証済みのみ表示可能
- 機密プロジェクト関連スキルは非公開必須

**主要操作**:
```typescript
class SkillPortfolio {
  // コマンド
  create(personId): SkillPortfolio
  addAssessmentResult(assessmentId, results): void
  registerCertification(certification, evidence): void
  verifyCertification(certificationId, verifier): void
  updateVisibility(skillId, visibility): void
  attachEvidence(skillId, document): void

  // クエリ
  getCurrentSkills(): SkillSnapshot
  getSkillHistory(skillId): SkillRecord[]
  getCertifications(onlyVerified?: boolean): ExternalCertification[]
  calculateGrowthRate(period): GrowthMetrics
}
```

---

### Aggregate 3: SkillGapAnalysis（スキルギャップ分析集約）

**集約ルート**: SkillGapAnalysis
**エンティティ**: 
- GapItem（ギャップ項目）
- LearningRecommendation（学習推奨）

**値オブジェクト**:
- TargetProfile（目標プロファイル）
- GapSeverity（Critical/High/Medium/Low/None）
- EstimatedEffort（推定習得期間）
- MarketDemand（市場需要度）

**不変条件（Invariants）**:
- ギャップ分析は現在スキルと目標の両方が必要
- Critical ギャップは最優先フラグ必須
- 推定習得期間は1日以上
- 分析結果は30日間有効

**主要操作**:
```typescript
class SkillGapAnalysis {
  // コマンド
  create(portfolioId, targetProfile): SkillGapAnalysis
  analyzeGaps(marketData): void
  prioritizeGaps(criteria): void
  generateLearningPath(): LearningRecommendation[]
  refreshAnalysis(newMarketData): void

  // クエリ
  getCriticalGaps(): GapItem[]
  getGapsByCategory(category): GapItem[]
  getEstimatedTimeToTarget(): Duration
  getLearningRecommendations(): LearningRecommendation[]
}
```

---

### Aggregate 4: MarketValueEstimation（市場価値推定集約）

**集約ルート**: MarketValueEstimation
**エンティティ**: なし

**値オブジェクト**:
- SalaryRange（給与レンジ）
- MarketPosition（市場でのポジション）
- DemandLevel（需要レベル）
- LocationFactor（地域係数）
- IndustryFactor（業界係数）

**不変条件（Invariants）**:
- 推定値は最低給与 < 最高給与
- 市場データは3つ以上のソースから
- 更新は四半期ごと（90日）
- 匿名化処理済みデータのみ使用

**主要操作**:
```typescript
class MarketValueEstimation {
  // コマンド
  create(portfolioId, marketData): MarketValueEstimation
  calculate(location, industry): void
  applyExperienceFactor(years, projects): void
  updateMarketData(newData): void

  // クエリ
  getSalaryRange(): SalaryRange
  getMarketPosition(): MarketPosition
  getDemandLevel(): DemandLevel
  getConfidenceScore(): number
}
```

---

## 5. ドメインイベント（Domain Events）

### AssessmentCompleted
```typescript
{
  eventId: string
  occurredAt: timestamp
  assessmentId: string
  personId: string
  skillResults: {skillId: string, level: number, score: number}[]
  method: AssessmentMethod
  completedBy: string
}
```
**発生タイミング**: スキル評価が完了した時
**購読者**: 
- vs2-learning-management（学習推奨の更新）
- vs2-career-planning（キャリアプラン見直し）
- vs3-matching（マッチング条件の更新）

---

### CriticalGapIdentified
```typescript
{
  eventId: string
  occurredAt: timestamp
  personId: string
  gapAnalysisId: string
  criticalSkills: {skillId: string, currentLevel: number, requiredLevel: number}[]
  urgency: "immediate" | "high" | "medium"
}
```
**発生タイミング**: Critical レベルのスキルギャップが検出された時
**購読者**: 
- vs2-learning-management（緊急学習プログラムの作成）
- vs2-career-planning（キャリアパスの再検討）
- notification-service（本人・マネージャーへの通知）

---

### SkillPortfolioUpdated
```typescript
{
  eventId: string
  occurredAt: timestamp
  portfolioId: string
  personId: string
  updates: {type: "assessment" | "certification" | "evidence", details: any}[]
  newOverallLevel: number
}
```
**発生タイミング**: スキルポートフォリオが更新された時
**購読者**: 
- vs3-matching（検索インデックスの更新）
- vs2-market-intelligence（市場分析データへの反映）

---

### MarketValueCalculated
```typescript
{
  eventId: string
  occurredAt: timestamp
  personId: string
  estimationId: string
  salaryRange: {min: number, max: number, currency: string}
  marketPosition: "top10" | "top25" | "average" | "below"
  confidence: number
}
```
**発生タイミング**: 市場価値が算定された時
**購読者**: 
- vs2-career-planning（キャリア戦略への反映）
- vs1-engagement（エンゲージメント戦略）

---

### CertificationVerified
```typescript
{
  eventId: string
  occurredAt: timestamp
  portfolioId: string
  certificationId: string
  certificationName: string
  issuingOrganization: string
  verifiedBy: string
  expiryDate?: timestamp
}
```
**発生タイミング**: 外部資格が検証された時
**購読者**: 
- vs2-certification-management（デジタルバッジ発行）
- vs3-matching（資格フィルタの更新）

---

## 6. Context Map（他BCとの関係）

### Downstream BC（このBCがデータを提供）

**vs2-learning-management-bc** (Customer-Supplier)
- 関係: Skill Assessment が Upstream、Learning が Downstream
- 提供データ: スキルギャップ分析結果、評価結果
- パターン: Published Language（SkillGapDTO）
- イベント: AssessmentCompleted, CriticalGapIdentified

**vs2-career-planning-bc** (Customer-Supplier)
- 関係: Skill Assessment が Upstream、Career Planning が Downstream
- 提供データ: 現在スキルレベル、成長履歴、市場価値
- パターン: Published Language（SkillPortfolioDTO）
- イベント: SkillPortfolioUpdated, MarketValueCalculated

**vs3-matching-bc** (Customer-Supplier)
- 関係: Skill Assessment が Upstream、Matching が Downstream
- 提供データ: 検証済みスキルセット、スキルレベル
- パターン: Open Host Service（REST API）
- 同期API: GET /skills/{personId}/verified

### Upstream BC（このBCがデータを参照）

**vs2-market-intelligence-bc** (Customer-Supplier)
- 関係: Market Intelligence が Upstream、Skill Assessment が Downstream
- 依存データ: スキル需要データ、市場給与データ
- パターン: Published Language（MarketDataDTO）
- 同期API: GET /market/skills/demand, GET /market/salary/ranges

**vs1-person-management-bc** (Conformist)
- 関係: Person Management が Upstream、Skill Assessment が Downstream
- 依存データ: 人材基本情報、組織情報
- パターン: Conformist（人材マスタに従う）
- 同期API: GET /persons/{personId}

### Partnership（相互依存）

**vs2-certification-management-bc** (Partnership)
- 関係: 双方向の緊密な連携
- Skill Assessment → 資格情報の評価への反映
- Certification → 検証済み資格の登録
- パターン: Partnership（共同でスキル証明を実現）

---

## 7. API契約概要

### 提供API（Open Host Service）

**スキル評価開始**
```
POST /api/v1/assessments
Request: {
  personId: string
  skillIds: string[]
  method: "online" | "practical" | "360degree"
  scheduledAt?: timestamp
}
Response: AssessmentDTO
```

**評価結果取得**
```
GET /api/v1/assessments/{assessmentId}/results
Response: AssessmentResultDTO
```

**スキルポートフォリオ取得**
```
GET /api/v1/portfolios/{personId}
Query: ?includeHistory=true&verified=true
Response: SkillPortfolioDTO
```

**スキルギャップ分析実行**
```
POST /api/v1/gap-analysis
Request: {
  personId: string
  targetRole?: string
  targetSkills?: {skillId: string, level: number}[]
}
Response: GapAnalysisDTO
```

**市場価値推定**
```
GET /api/v1/market-value/{personId}
Query: ?location={code}&industry={code}
Response: MarketValueDTO
```

### 依存API（他BCへの依存）

**市場データ取得**
```
GET /api/v1/market/skills/{skillId}/demand
→ vs2-market-intelligence-bc
```

**人材情報取得**
```
GET /api/v1/persons/{personId}
→ vs1-person-management-bc
```

**資格情報検証**
```
POST /api/v1/certifications/verify
→ external-certification-apis
```

---

## 8. 技術スタック推奨

### バックエンド
- **言語**: TypeScript / Node.js（高速な評価処理）
- **フレームワーク**: NestJS（DDD/CQRSサポート）
- **データベース**: 
  - PostgreSQL（トランザクショナルデータ）
  - MongoDB（スキルポートフォリオ、柔軟なスキーマ）
- **キャッシュ**: Redis（評価セッション管理）
- **イベントバス**: Apache Kafka（高スループット）

### AI/ML基盤
- **スキル推定**: Python / scikit-learn
- **市場価値予測**: TensorFlow / PyTorch
- **自然言語処理**: spaCy（スキル記述の解析）

### API
- **スタイル**: RESTful API + GraphQL（柔軟なクエリ）
- **仕様**: OpenAPI 3.0
- **認証**: OAuth 2.0 + JWT
- **レート制限**: あり（評価は1人1日10回まで）

### セキュリティ
- **評価データ暗号化**: AES-256
- **監査ログ**: 全評価活動を記録
- **不正検知**: 異常な評価パターンの自動検出

### 監視・可観測性
- **ログ**: ELK Stack
- **メトリクス**: Prometheus + Grafana
- **トレーシング**: Jaeger
- **アラート**: PagerDuty連携

---

## 9. 次のステップ

### 即座の次のアクション

1. **他のVS2サブドメインのBC定義**
```bash
/parasol:3-capabilities cl3 vs2-learning-management
/parasol:3-capabilities cl3 vs2-career-planning
/parasol:3-capabilities cl3 vs2-certification-management
/parasol:3-capabilities cl3 vs2-market-intelligence
```

### VS2の全BC定義完了後

2. **他のCore Domain VSのサブドメイン設計**
```bash
/parasol:3-capabilities cl2 VS1    # 人材獲得
/parasol:3-capabilities cl2 VS3    # マッチング
/parasol:3-capabilities cl2 VS5    # 企業サービス
```

### 全BC定義完了後

3. **Phase 4: Architecture - Context Map統合**
```bash
/parasol:4-architecture
```

Phase 4では：
- 全BCの関係を統合したContext Mapを作成
- マイクロサービス境界を確定
- APIゲートウェイ設計
- イベント駆動アーキテクチャの詳細設計