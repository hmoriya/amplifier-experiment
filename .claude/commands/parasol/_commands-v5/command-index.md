# Parasol V5 コマンドインデックス

**全コマンドの詳細仕様と実装ガイド**

---

## 📑 目次

1. [価値管理コマンド群](#価値管理コマンド群)
2. [マイルストーン管理コマンド群](#マイルストーン管理コマンド群)
3. [統合実行コマンド群](#統合実行コマンド群)
4. [分析・レポートコマンド群](#分析レポートコマンド群)
5. [既存コマンド強化](#既存コマンド強化)

---

## 価値管理コマンド群

### `/parasol:value-trace`

**価値トレース記録・管理**

```bash
# 使用方法
/parasol:value-trace [action] [options]

# アクション
record    # 新規トレース記録
list      # トレース一覧表示
verify    # トレース検証
export    # トレースエクスポート
```

**実装仕様**:
```yaml
implementation:
  core_engine: "_value-traceability-system/core/value-tracer.yaml"
  data_format: "YAML with JSON-LD semantics"
  storage: "outputs/{project}/value-traces/"
  
features:
  - リアルタイム記録
  - 価値チェーン可視化
  - 自動検証機能
  - マルチフォーマットエクスポート
```

### `/parasol:necessity-check`

**構造的必然性検証**

```bash
# 使用方法
/parasol:necessity-check "設計判断の説明" [--evidence path/to/data]

# オプション
--evidence    # 根拠データファイル指定
--strict      # 厳格モード（4基準すべて必須）
--report      # 詳細レポート生成
```

**判定基準**:
```yaml
criteria:
  1_value_origin:
    question: "誰のどんな価値を実現するのか？"
    validation: "ステークホルダーと価値が明確"
    
  2_causality:
    question: "なぜその判断が価値を生むのか？"
    validation: "因果関係が論理的に説明可能"
    
  3_alternatives:
    question: "他の選択肢と比較したか？"
    validation: "代替案の検討記録あり"
    
  4_measurability:
    question: "効果を測定できるか？"
    validation: "KPIが定義されている"
```

### `/parasol:imagination-detect`

**想像の設計検出**

```bash
# 使用方法
/parasol:imagination-detect [target] [--fix]

# ターゲット
all           # 全フェーズスキャン
phase:N       # 特定フェーズ
file:path     # 特定ファイル
decision:id   # 特定の判断

# オプション
--fix         # 自動修正提案
--report      # 検出レポート生成
--block       # 検出時に実行ブロック
```

**検出パターン**:
```yaml
imagination_patterns:
  1_assumption_based:
    markers: ["思われる", "はず", "だろう", "かもしれない"]
    severity: HIGH
    
  2_authority_dependent:
    markers: ["エキスパートが", "コンサルが推奨", "業界標準"]
    severity: MEDIUM
    
  3_trend_following:
    markers: ["最新の", "トレンドの", "話題の"]
    severity: MEDIUM
    
  4_personal_preference:
    markers: ["個人的に", "好みとして", "センス的に"]
    severity: HIGH
    
  5_thought_stopping:
    markers: ["いつもの", "面倒なので", "とりあえず"]
    severity: CRITICAL
```

---

## マイルストーン管理コマンド群

### `/parasol:milestone`

**統合マイルストーン管理**

```bash
# 使用方法
/parasol:milestone [action] [VMS-ID]

# アクション
status        # 全VMS状況確認
check VMS1     # 特定VMS達成確認
plan          # VMS達成計画表示
report        # VMS進捗レポート
```

**マイルストーン定義**:
```yaml
milestones:
  VMS1:
    name: "コンテキスト確立"
    target: "1週間"
    criteria:
      - "ステークホルダー理解 >= 95%"
      - "価値定義明確性 >= 95%"
      - "VL1-VL3分解完了"

  VMS2:
    name: "戦略設計完了"
    target: "3週間"
    criteria:
      - "全VS価値検証完了"
      - "戦略ケイパビリティ定義"
      - "依存関係明確化"
```

### `/parasol:quality-gate`

**品質ゲート実行**

```bash
# 使用方法
/parasol:quality-gate [MS-ID] [--auto-fix]

# 実行例
/parasol:quality-gate VMS3 --auto-fix

# 出力例
🔍 VMS3品質ゲート実行中...

✅ ドメイン分解完全性: 98% [PASS]
✅ BC定義品質: 92% [PASS]
⚠️  価値継承確認: 85% [WARNING]
   → 自動修正実行中...
✅ 構造的必然性: 100% [PASS]

総合判定: PASS with fixes
```

### `/parasol:value-inheritance`

**価値継承チェック**

```bash
# 使用方法
/parasol:value-inheritance [from-phase] [to-phase]

# チェック内容
- 価値定義の一貫性
- 価値の具体化度合い
- 価値劣化の検出
- トレーサビリティ完全性
```

---

## 統合実行コマンド群

### `/parasol:quick-start`

**高速プロジェクト開始（VMS1達成）**

```bash
# 使用方法
/parasol:quick-start <company-url> [options]

# オプション
--industry    # 業界特化分析
--focus       # 重点領域指定
--team-size   # チーム規模

# 実行内容
1. 企業情報収集・分析
2. ステークホルダー自動特定
3. VL1-VL3価値分解実行
4. 構造的必然性検証
5. VMS1品質ゲート実行
6. 初期レポート生成
```

### `/parasol:full-design`

**完全設計実行（VMS1-VMS3）**

```bash
# 使用方法
/parasol:full-design [--parallel] [--strict]

# 実行フロー
Phase 1: Context → VMS1
  ├─ VL価値分解
  └─ 品質ゲート

Phase 2: Value → VMS2
  ├─ VS設計
  └─ 戦略ケイパビリティ

Phase 3: Capabilities → VMS3
  ├─ ドメイン分解
  └─ BC定義
```

### `/parasol:production-ready`

**本番環境準備完了（VMS1-VMS5）**

```bash
# 使用方法
/parasol:production-ready [--environment] [--validate-all]

# 統合実行内容
- VMS1: コンテキスト確立
- VMS2: 戦略設計
- VMS3: 戦術設計
- VMS4: 運用設計
- VMS5: プロダクション基盤

# 最終チェック
- 全価値トレース確認
- 構造的必然性総合評価
- 想像ゼロ確認
- SLA達成可能性検証
```

---

## 分析・レポートコマンド群

### `/parasol:value-report`

**価値実現総合レポート**

```bash
# 使用方法
/parasol:value-report [--format] [--audience]

# フォーマット
executive     # 経営層向け要約
technical     # 技術詳細
stakeholder   # ステークホルダー別

# レポート内容
- 価値実現マップ
- ステークホルダー別価値
- 価値チェーン分析
- ROI予測
```

### `/parasol:structural-analysis`

**構造的必然性分析**

```bash
# 使用方法
/parasol:structural-analysis [--depth] [--visualize]

# 分析内容
- 全判断の必然性スコア
- 根拠データ品質評価
- 弱点領域の特定
- 改善提案
```

### `/parasol:project-health`

**プロジェクト健全性診断**

```bash
# 使用方法
/parasol:project-health [--detailed]

# 診断項目
1. 価値トレーサビリティ完全性
2. 構造的必然性スコア  
3. 想像検出状況
4. MS達成状況
5. チーム理解度
6. リスク評価
```

---

## 既存コマンド強化

### Phase 1-7 コマンドの価値トレーサビリティ統合

**共通強化機能**:
```yaml
enhancements:
  auto_trace:
    - 全判断を自動記録
    - 価値起源を追跡
    - 継承関係を管理
    
  necessity_validation:
    - 4基準自動チェック
    - 不足時は入力要求
    - 根拠データ検証
    
  imagination_blocking:
    - リアルタイム検出
    - 実行前ブロック
    - 修正ガイダンス提供
```

**コマンド別統合ポイント**:

| コマンド | 統合機能 |
|----------|----------|
| `/parasol:1-context` | VL分解時の価値根拠記録 |
| `/parasol:2-value` | VS設計の必然性検証 |
| `/parasol:3-capabilities` | BC価値継承確認 |
| `/parasol:4-application` | サービス境界価値検証 |
| `/parasol:5-software` | 実装価値妥当性確認 |
| `/parasol:6-implementation` | 価値実現検証 |
| `/parasol:7-platform` | 価値保護確認 |

---

## 🔧 実装ガイドライン

### コマンド実装テンプレート

```python
# parasol_command_template.py

class ParasolCommand:
    def __init__(self):
        self.value_tracer = ValueTracer()
        self.necessity_judge = StructuralNecessityJudge()
        self.imagination_detector = ImaginationDetector()
        
    def execute(self, args):
        # 1. 価値トレース開始
        trace_id = self.value_tracer.start_trace(args)
        
        # 2. 想像チェック
        if self.imagination_detector.detect(args.decision):
            raise ImaginationDetectedError("想像の設計を検出")
            
        # 3. 構造的必然性確認
        necessity_score = self.necessity_judge.evaluate(args)
        if necessity_score < 3.0:
            raise LowNecessityError("構造的必然性が不足")
            
        # 4. 実処理
        result = self._execute_core(args)
        
        # 5. 価値記録
        self.value_tracer.record(trace_id, result)
        
        # 6. 品質ゲート
        self._check_quality_gate(result)
        
        return result
```

### 価値記録スキーマ

```yaml
# value_trace_schema.yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required:
  - trace_id
  - timestamp
  - phase
  - decision
  - value_origin
  - structural_necessity
  - imagination_check
  
properties:
  trace_id:
    type: string
    pattern: "^vt-\\d{4}-\\d{3}$"
    
  value_origin:
    type: object
    required:
      - stakeholder
      - need
      - evidence
```

---

## 📊 効果測定

### KPI定義

```yaml
kpis:
  quality:
    - imagination_detection_rate: "0%"  # 想像ゼロ
    - structural_necessity_avg: ">= 4.0"  # 高必然性
    - value_traceability: "100%"  # 完全追跡
    
  efficiency:
    - design_time_reduction: "50%"  # 時間短縮
    - rework_rate: "< 10%"  # 手戻り削減
    - automation_rate: ">= 80%"  # 自動化率
    
  business:
    - value_realization: ">= 95%"  # 価値実現率
    - roi_achievement: ">= 120%"  # ROI達成率
    - stakeholder_satisfaction: ">= 4.5"  # 満足度
```

---

**Parasol V5 統合コマンド体系** - 価値を確実に実現する革新的ツールセット