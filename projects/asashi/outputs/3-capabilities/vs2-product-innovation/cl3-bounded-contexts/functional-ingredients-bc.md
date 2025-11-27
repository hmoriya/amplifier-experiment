# Bounded Context: functional-ingredients-bc

**プロジェクト:** asashi (アサヒグループホールディングス)
**サブドメイン:** functional-ingredients（機能性成分研究）
**作成日:** 2025-11-27
**ステータス:** CL3完了

---

## 命名理由（Naming Rationale）

| 項目 | 内容 |
|------|------|
| **BC名** | functional-ingredients-bc |
| **日本語名** | 機能性成分研究 |
| **命名パターン** | `functional-ingredients`（ドメイン特化型） |
| **命名理由** | 「機能性管理」ではなく具体的な研究対象を明示。健康効果のエビデンス構築という**発展**活動を表現。乳酸菌・枯草菌等の微生物研究を含む成長市場（健康・ウェルネス）への対応を担う |
| **VS横断一意性** | ✅ 確認済み（全VS間で一意） |

---

## 【ビジネス面】

### 1. コンテキスト概要

#### BC名
**functional-ingredients-bc**（機能性成分研究バウンデッドコンテキスト）

#### 目的
健康・機能性製品に必要な機能性成分の研究・開発を行い、乳酸菌・枯草菌等の微生物研究を含む。成長市場（健康・ウェルネス）への対応を支援する。

#### 責務
- 乳酸菌・枯草菌等の機能性微生物の研究・育種
- 機能性成分の健康効果に関する科学的検証
- 機能性表示食品の届出に必要なエビデンス作成
- 微生物バンクの構築・維持管理
- 機能性に関する規制対応研究

#### チーム境界
- **担当組織**: R&D本部 機能性研究所
- **チーム構成**:
  - 微生物研究チーム（微生物学者、遺伝学者）
  - 機能性評価チーム（栄養学者、薬理学者）
  - 規制対応チーム（薬事専門家）
- **推定人員**: 20-30名

---

### 2. ビジネスオペレーション詳細

#### OP1: 乳酸菌研究・育種

**業務フロー:**
```
1. 菌株探索・収集
   └─ 機能性に期待される菌株の探索
   └─ 自然環境・既存コレクションからの収集
   └─ 外部機関からの入手

2. 機能性スクリーニング
   └─ in vitro評価（細胞試験）
   └─ 候補菌株の絞り込み
   └─ 安全性の初期評価

3. 育種・改良
   └─ 機能性強化のための育種
   └─ 製造適性の改良
   └─ 安定性の向上

4. 登録・保存
   └─ 微生物バンクへの登録
   └─ 凍結保存・凍結乾燥
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP1-01 | 新規菌株は必ず遺伝学的同定を実施すること |
| BR-OP1-02 | 食品利用可能性（GRAS/食経験）を確認すること |
| BR-OP1-03 | 抗生物質耐性遺伝子の有無を確認すること |
| BR-OP1-04 | 全株に一意の株ID（FI-YYYY-NNNN形式）を付与すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 探索計画書 | 乳酸菌サンプル |
| 機能性要件 | スクリーニング結果 |
| 外部情報 | 微生物バンクエントリ |

**トリガー:**
- 製品開発からの機能性要求
- 健康トレンド・市場ニーズ
- 学術情報

---

#### OP2: 機能性評価試験

**業務フロー:**
```
1. 試験計画策定
   └─ 評価項目の定義（整腸、免疫、代謝等）
   └─ 試験デザインの設計
   └─ 倫理審査申請（ヒト試験の場合）

2. in vitro試験
   └─ 細胞試験による機能性評価
   └─ 作用機序の解析

3. 動物試験
   └─ 安全性試験
   └─ 有効性試験

4. ヒト臨床試験
   └─ 健常者対象の介入試験
   └─ 有効性・安全性の検証

5. 結果分析・報告
   └─ 統計解析
   └─ エビデンスレベルの判定
   └─ 論文・報告書作成
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP2-01 | ヒト試験は必ず倫理審査委員会の承認を得ること |
| BR-OP2-02 | 臨床試験はUMIN登録を行うこと |
| BR-OP2-03 | 二重盲検プラセボ対照試験を基本とすること |
| BR-OP2-04 | 有意水準はp<0.05を採用すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 候補菌株 | 機能性エビデンス |
| 試験計画書 | 試験報告書 |
| 倫理審査申請 | 論文・データ |

**トリガー:**
- 製品開発要件
- 機能性表示申請準備
- 研究計画

---

#### OP3: 規制対応研究

**業務フロー:**
```
1. 規制要件調査
   └─ 機能性表示食品制度の要件確認
   └─ 必要エビデンスの特定
   └─ 届出事例の調査

2. エビデンス構築
   └─ システマティックレビュー
   └─ メタアナリシス
   └─ 追加試験の実施

3. 届出資料作成
   └─ 機能性の科学的根拠資料
   └─ 安全性根拠資料
   └─ 表示内容の検討

4. 届出・審査対応
   └─ 消費者庁への届出
   └─ 照会対応
   └─ 受理・公表
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP3-01 | 機能性表示は科学的根拠に基づくこと |
| BR-OP3-02 | 届出前に法務・薬事部門のレビューを受けること |
| BR-OP3-03 | エビデンスは査読論文または同等の品質を確保すること |
| BR-OP3-04 | 安全性は既存情報および追加試験で担保すること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 機能性エビデンス | 届出資料 |
| 規制要件 | 機能性表示許可 |
| 安全性データ | 表示内容 |

**トリガー:**
- 新製品発売計画
- 規制変更
- 競合動向

---

#### OP4: 微生物バンク管理

**業務フロー:**
```
1. 保存処理
   └─ 凍結保存（-80℃）
   └─ 凍結乾燥保存
   └─ 作業株の維持培養

2. 在庫・品質管理
   └─ 生存率の定期確認
   └─ 特性の安定性確認
   └─ コンタミネーションチェック

3. 払出管理
   └─ 払出申請受付
   └─ 菌株の活性化・調製
   └─ トレーサビリティ記録

4. 情報管理
   └─ 株情報のデータベース管理
   └─ 機能性データとの紐付け
   └─ 知的財産管理
```

**業務ルール:**
| ルール | 説明 |
|--------|------|
| BR-OP4-01 | マスターストック・ワーキングストックの2層管理を維持 |
| BR-OP4-02 | 生存率80%以上を維持すること |
| BR-OP4-03 | 年1回以上の特性再確認を実施すること |
| BR-OP4-04 | 外部提供は知財確認・MTA締結後に限ること |

**入力/出力:**
| 入力 | 出力 |
|------|------|
| 新規登録株 | 保存済み菌株 |
| 払出申請 | 活性化済み菌株 |
| 品質検査計画 | 品質記録 |

**トリガー:**
- 新株登録
- 払出申請
- 定期品質管理

---

### 3. ユビキタス言語（Ubiquitous Language）

#### ドメインオブジェクト（業務で扱うモノ・コト）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| FunctionalStrain | 機能性菌株 | 特定の健康効果が期待される微生物株 |
| Probiotic | プロバイオティクス | 適切な量を摂取した際に宿主に有益な効果をもたらす生きた微生物 |
| Lactobacillus | 乳酸菌 | 乳酸を産生する細菌の総称 |
| BacillusSubtilis | 枯草菌 | 納豆菌等を含むバチルス属の細菌 |
| FunctionalEvidence | 機能性エビデンス | 健康効果を裏付ける科学的根拠 |
| ClinicalTrial | 臨床試験 | ヒトを対象とした有効性・安全性試験 |
| FoodsWithFunctionClaims | 機能性表示食品 | 科学的根拠に基づき機能性を表示した食品 |
| MicrobialBank | 微生物バンク | 菌株を体系的に保存・管理する施設 |

#### ビジネスルール（業務上の制約・ルール）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| GRAS | 一般に安全と認められる | 米国FDAによる安全性認定 |
| EthicsApproval | 倫理審査承認 | ヒト試験実施に必要な審査承認 |
| SystematicReview | システマティックレビュー | 文献の系統的レビュー手法 |
| MetaAnalysis | メタアナリシス | 複数研究の統合解析 |

#### プロセス（業務フロー）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| Screening | スクリーニング | 候補菌株から目的特性を持つ株を選抜するプロセス |
| InVitroTest | in vitro試験 | 試験管・培養細胞レベルの試験 |
| AnimalStudy | 動物試験 | 動物を用いた有効性・安全性試験 |
| HumanTrial | ヒト試験 | 健常者を対象とした介入試験 |
| Filing | 届出 | 機能性表示食品の届出プロセス |

#### イベント（業務上の重要な出来事）

| 用語 | 日本語 | 定義 |
|------|--------|------|
| StrainDiscovered | 菌株発見 | 有望な機能性菌株が発見された |
| EvidenceEstablished | エビデンス確立 | 機能性の科学的根拠が確立された |
| FilingAccepted | 届出受理 | 機能性表示食品の届出が受理された |
| StrainTransferred | 菌株移転 | 製品開発BCへ菌株が移転された |

---

## 【技術面】

### 4. 集約設計（Aggregates）

#### 集約1: FunctionalStrain（機能性菌株）

**責務**: 機能性微生物株のライフサイクル管理

```
FunctionalStrain [Aggregate Root]
├── strainId: StrainId [Value Object]
│   └── format: "FI-YYYY-NNNN"
├── taxonomy: Taxonomy [Value Object]
│   ├── genus: string (例: "Lactobacillus")
│   ├── species: string (例: "gasseri")
│   └── strain: string (例: "CP2305")
├── origin: StrainOrigin [Value Object]
│   ├── source: enum (ISOLATED, ACQUIRED, BRED)
│   ├── location: string
│   └── collectionDate: Date
├── functionalProperties: FunctionalProperty[] [Entity]
│   ├── propertyId: PropertyId
│   ├── category: enum (INTESTINAL, IMMUNE, METABOLIC, SKIN)
│   ├── effect: string
│   └── evidenceLevel: enum (IN_VITRO, ANIMAL, HUMAN)
├── safetyProfile: SafetyProfile [Value Object]
│   ├── grasStatus: boolean
│   ├── foodHistory: boolean
│   ├── antibioticResistance: boolean
│   └── toxicityTest: TestResult
├── stocks: Stock[] [Entity]
│   ├── stockId: StockId
│   ├── type: enum (MASTER, WORKING)
│   ├── preservationMethod: enum (FROZEN, LYOPHILIZED)
│   ├── viability: number
│   └── lastChecked: Date
├── status: StrainStatus [Value Object]
│   └── value: enum (RESEARCH, VALIDATED, PRODUCTION)
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-FS-01 | strainIdは一意でFI-YYYY-NNNN形式であること |
| INV-FS-02 | PRODUCTION statusには最低1つのHUMANレベルエビデンスが必要 |
| INV-FS-03 | 食品利用にはgrasStatusまたはfoodHistoryがtrueであること |
| INV-FS-04 | viabilityは0-100%の範囲であること |

**主要メソッド:**
```
- registerStrain(taxonomy, origin): FunctionalStrain
- addFunctionalProperty(category, effect, evidenceLevel): void
- validateForProduction(): ValidationResult
- transferToBeverageDevelopment(targetBC): TransferRecord
```

---

#### 集約2: FunctionalEvidence（機能性エビデンス）

**責務**: 機能性の科学的根拠の管理

```
FunctionalEvidence [Aggregate Root]
├── evidenceId: EvidenceId [Value Object]
├── strainId: StrainId [Value Object]
├── targetFunction: FunctionCategory [Value Object]
│   └── value: enum (INTESTINAL_HEALTH, IMMUNE_MODULATION, FAT_METABOLISM, SKIN_HEALTH)
├── studies: Study[] [Entity]
│   ├── studyId: StudyId
│   ├── type: enum (IN_VITRO, ANIMAL, HUMAN_RCT, META_ANALYSIS)
│   ├── design: StudyDesign
│   ├── results: StudyResult
│   ├── publication: Publication?
│   └── qualityScore: number
├── overallEvidenceLevel: EvidenceLevel [Value Object]
│   └── value: enum (INSUFFICIENT, PRELIMINARY, MODERATE, STRONG)
├── regulatoryStatus: RegulatoryStatus [Entity]
│   ├── filingId: FilingId?
│   ├── status: enum (NOT_FILED, UNDER_REVIEW, ACCEPTED, REJECTED)
│   └── approvedClaim: string?
└── audit: AuditTrail [Value Object]
```

**不変条件（Invariants）:**
| 不変条件 | 説明 |
|----------|------|
| INV-FE-01 | STRONG evidenceLevelには最低1つのHUMAN_RCTが必要 |
| INV-FE-02 | ACCEPTED regulatoryStatusには最低MODERATEのevidenceLevelが必要 |
| INV-FE-03 | studyのqualityScoreは0-100の範囲であること |

**主要メソッド:**
```
- createEvidence(strainId, targetFunction): FunctionalEvidence
- addStudy(type, design, results): Study
- calculateOverallLevel(): EvidenceLevel
- prepareFilingDocuments(): FilingDocuments
```

---

### 5. ドメインイベント（Domain Events）

| イベント名 | ペイロード | 発生タイミング | 購読者 |
|-----------|-----------|---------------|--------|
| **FunctionalStrainRegistered** | {strainId, taxonomy, functionalProperties, registeredAt} | 新規機能性菌株の登録完了時 | beverage-development |
| **EvidenceEstablished** | {evidenceId, strainId, targetFunction, evidenceLevel, establishedAt} | エビデンスレベルがMODERATE以上に達した時 | beverage-development |
| **FilingAccepted** | {evidenceId, strainId, approvedClaim, acceptedAt} | 機能性表示届出が受理された時 | beverage-development, VS3ブランディング |
| **StrainTransferredToProduction** | {strainId, targetBC, quantity, transferredAt} | 菌株が製品開発BCに移転された時 | beverage-development |

---

### 6. コンテキストマップ（Context Map）

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    │   functional-ingredients-bc          │
                    │        (Supporting)                  │
                    │                                      │
                    └──────────────┬───────────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              │              ▼
         ┌─────────────────┐      │   ┌─────────────────┐
         │ ingredient-     │      │   │ beverage-       │
         │ research-bc     │      │   │ development-bc  │
         │                 │      │   │                 │
         │ [Partnership]   │      │   │ [Customer-      │
         └─────────────────┘      │   │  Supplier]      │
                                  │   └─────────────────┘
                                  │
                                  ▼
                       ┌─────────────────┐
                       │ 規制当局         │
                       │ （外部システム）  │
                       │                 │
                       │ [ACL]           │
                       └─────────────────┘
```

#### 関係パターン詳細

| 関連BC | パターン | 説明 |
|--------|---------|------|
| ingredient-research-bc | **Partnership** | 素材と機能性成分の組み合わせ研究で対等に協力 |
| beverage-development-bc | **Customer-Supplier** | 機能性成分・乳酸菌を供給。製品開発のニーズを受領 |
| 規制当局システム | **ACL** | 機能性表示届出のための外部連携。防腐壁で分離 |

---

### 7. API契約概要

#### 提供API（Commands）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/strains` | POST | 新規機能性菌株の登録 |
| `/strains/{id}/properties` | POST | 機能性特性の追加 |
| `/strains/{id}/transfer` | POST | 製品開発BCへの菌株移転 |
| `/evidence` | POST | 新規エビデンスの作成 |
| `/evidence/{id}/studies` | POST | 試験結果の追加 |
| `/evidence/{id}/filing` | POST | 届出申請の開始 |

#### 提供API（Queries）

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/strains` | GET | 機能性菌株一覧取得 |
| `/strains/{id}` | GET | 菌株詳細取得 |
| `/strains/search` | GET | 機能性による菌株検索 |
| `/evidence/{id}` | GET | エビデンス詳細取得 |
| `/evidence/for-function/{function}` | GET | 機能別エビデンス検索 |

#### 依存API（他BCへの依存）

| BC | 依存内容 |
|----|---------|
| identity-management-bc | 研究者認証・権限管理 |
| audit-logging-bc | 監査ログの記録 |

---

## 次のステップ

### CL3完了後の推奨アクション

1. **他のSupporting サブドメインのCL3定義**
   - process-engineering-bc
   - sensory-evaluation-bc
   - prototype-production-bc

2. **Phase 4: Architecture への移行**
   - Context Map統合設計
   - イベント駆動アーキテクチャ設計

---

**作成完了:** 2025-11-27
**ステータス:** CL3完了（functional-ingredients-bc定義）
**次のフェーズ:** 他Supporting SDのCL3 または Phase 4: Architecture
