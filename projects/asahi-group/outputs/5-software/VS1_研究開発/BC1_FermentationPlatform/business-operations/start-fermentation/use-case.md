# Use Case: 発酵プロセス開始 (Start Fermentation Process)

## 概要

| 項目 | 内容 |
|------|------|
| UC ID | BC1-UC-002 |
| 名称 | 発酵プロセス開始 |
| アクター | 醸造技術者、研究員 |
| トリガー | 新規発酵バッチの開始時 |
| 関連集約 | FermentationProcess, YeastStrain |

---

## ユースケース記述

### 事前条件 (Preconditions)

1. アクターは認証済みで、発酵プロセス開始権限を持つ
2. 使用する酵母株が登録済みかつ有効（Research/Validated/Production）
3. 発酵設備が利用可能
4. 初期条件（麦汁/原料）が準備済み

### 事後条件 (Postconditions)

1. 新規FermentationProcessエンティティが作成される
2. 一意のProcessCode（FP-YYYYMMDD-NNN形式）が発行される
3. ステータスは「InProgress」
4. FermentationProcessStartedイベントが発行される
5. 時系列データ記録が開始される

### 基本フロー (Main Flow)

1. **開始**: 技術者が「新規発酵プロセス開始」を選択
2. **酵母株選択**:
   - 有効な酵母株リストから選択
   - または株コードで直接検索
   - 選択株の特性・推奨条件を表示
3. **スケールタイプ選択**:
   - Laboratory（1-100L）
   - Pilot（100-1000L）
   - Production（1000L以上）
4. **発酵条件入力**:
   - 初期温度
   - 圧力
   - 溶存酸素濃度
   - 接種量（Pitch Rate）
   - 麦汁比重
5. **タイムライン設定**（任意）:
   - 発酵ステージの定義
   - 各ステージの目標条件と期間
6. **条件最適化提案**:
   - システムが過去データに基づく最適条件を提案
   - 提案の採用/却下を選択
7. **確認**: 入力内容の最終確認
8. **開始**: プロセスを開始
9. **完了**: ProcessCodeとダッシュボードリンクを表示

### 代替フロー (Alternative Flows)

**A1: 過去プロセスからの複製**
- ステップ2で「過去プロセスから複製」を選択
- 過去の成功プロセスを選択
- 条件を引き継ぎ、必要に応じて調整

**A2: 酵母推薦からの開始**
- BC1-UC-003「酵母推薦」の結果から遷移
- 推薦された酵母株と最適条件がプリセット

**A3: パイロットからプロダクションへのスケールアップ**
- ステップ3でProductionを選択
- 関連するPilotプロセスを選択
- スケールアップ係数を自動適用

### 例外フロー (Exception Flows)

**E1: 酵母株ステータス不正**
- Research株をProductionスケールで使用しようとした場合
- エラーメッセージ：「実験用酵母株は製造スケールで使用できません」
- Validated以上の株の選択を促す

**E2: 条件範囲逸脱**
- 酵母株の適温範囲を超える温度設定
- 警告を表示、継続/修正の選択

**E3: 設備キャパシティ超過**
- スケールタイプに対して不適切な容量設定
- エラーメッセージとスケール範囲を表示

---

## ビジネスルール

| BR ID | ルール | 検証タイミング |
|-------|--------|----------------|
| BR-010 | ProcessCodeは一意で自動発番 | 開始時 |
| BR-011 | Research株はLaboratoryスケールのみ | 開始時 |
| BR-012 | 温度は酵母株の適温範囲内を推奨 | 入力時（警告） |
| BR-013 | 接種量は酵母株の推奨範囲内 | 入力時（警告） |
| BR-014 | Productionスケールには承認済み条件が必要 | 開始時 |

---

## データ要件

### 入力データ

```yaml
StartFermentationInput:
  strainId: uuid (required)
  scaleType: enum [Laboratory, Pilot, Production] (required)
  conditions:
    temperature: decimal (required, °C)
    pressure: decimal (optional, kPa)
    dissolvedOxygen: decimal (optional, mg/L)
    pitchRate: decimal (required, cells/mL)
    wortGravity: decimal (required, SG)
  timeline: (optional)
    - name: string
      targetConditions: FermentationConditions
      durationHours: integer
  sourceProcessId: uuid (optional, for replication)
```

### 出力データ

```yaml
StartFermentationOutput:
  processId: uuid
  processCode: string (FP-YYYYMMDD-NNN)
  strainId: uuid
  strainName: string
  status: "InProgress"
  startedAt: datetime
  dashboardUrl: string
```

---

## 非機能要件

| 項目 | 要件 |
|------|------|
| 応答時間 | 開始処理: 3秒以内 |
| 並行性 | 同時に100プロセスまで稼働可能 |
| データ収集 | リアルタイム測定データ受信対応 |
| 監査ログ | 全開始操作・条件変更を記録 |

---

## 関連API

- POST `/fermentation-processes` - プロセス開始
- GET `/yeast-strains/{strainId}` - 酵母株情報取得
- POST `/recommendations/optimize-conditions` - 条件最適化
- GET `/fermentation-processes?status=completed` - 過去プロセス検索

---

## 関連ドメインイベント

| イベント | 発行タイミング | 購読者 |
|----------|----------------|--------|
| FermentationProcessStarted | プロセス開始成功時 | モニタリングシステム |
| FermentationConditionsSet | 条件設定完了時 | ログシステム |

---

**作成日**: 2025-11-28
**VS/BC**: VS1/BC1 Fermentation Platform
