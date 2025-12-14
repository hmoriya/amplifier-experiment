# Parasol 価値トレーサビリティシステム設計書

**作成日**: 2025-12-13  
**バージョン**: V1.0

---

## システムアーキテクチャ

### 全体構成図

```
┌─────────────────────────────────────────────────────────────────┐
│                    Value Traceability System                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Value Tracer   │  │ Necessity Judge │  │ Assurance Gate  │ │
│  │   記録システム    │  │   判定エンジン    │  │  保証ゲート     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Phase Hooks   │  │ Trace Collector │  │ Gate Validator  │ │
│  │  Phase統合機能   │  │  データ収集     │  │   検証ロジック    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │    Validators   │  │    Templates    │  │    Reports      │ │
│  │   検証ルール     │  │   テンプレート   │  │   レポート生成   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      Parasol Phase Commands                     │
├─────────────────────────────────────────────────────────────────┤
│  Phase 0  │  Phase 1  │  Phase 2  │  Phase 3  │  Phase 4-7     │
│   init    │  context  │   value   │capabilities│ design/impl    │
└─────────────────────────────────────────────────────────────────┘
```

### データフロー

```
1. Phase Command 実行
    ↓
2. Phase Hook 発火
    ↓
3. Trace Collector がデータ収集
    ↓
4. Necessity Judge が構造的必然性判定
    ↓
5. Value Tracer が価値トレース記録
    ↓
6. Assurance Gate が価値保証チェック
    ↓
7. 結果をレポート生成
```

---

## コンポーネント設計

### 1. Value Tracer（価値トレース記録システム）

#### 責務
- 設計判断のリアルタイム記録
- 価値根拠の自動抽出と格納
- トレーサビリティチェーンの構築

#### データモデル
```yaml
value_trace:
  id: trace-{phase}-{timestamp}
  phase: "Phase 2"
  timestamp: "2025-12-13T10:30:00Z"
  decision:
    description: "発酵技術研究ケイパビリティの追加"
    maker: "システム分析者"
    context: "VL3価値「味の革新」実現のため"
  value_link:
    vl1: "期待を超えるおいしさ"
    vl2: "製品イノベーション価値" 
    vl3: "発酵技術による味の革新"
    ms: "MS2"
    vs: "VS2"
  evidence:
    - type: "market_analysis"
      source: "業界レポート2024"
      data: "発酵技術市場の成長率15%"
    - type: "competitive_analysis"
      source: "競合調査"
      data: "競合他社の発酵技術投資状況"
  necessity_check:
    score: 4.2  # 5点満点
    criteria:
      value_origin: 4.5
      causal_proof: 4.0
      alternatives: 4.0
      measurability: 4.2
```

### 2. Necessity Judge（構造的必然性判定エンジン）

#### 判定アルゴリズム
```yaml
structural_necessity_algorithm:
  input:
    - decision_context
    - value_hierarchy
    - evidence_data
    - alternative_options
    
  process:
    step1_value_origin:
      check: "VL3価値から直接導出されているか"
      weight: 0.3
      threshold: 3.0
      
    step2_causal_proof:
      check: "因果関係が証明されているか"
      weight: 0.3
      threshold: 3.0
      
    step3_alternatives:
      check: "代替案が適切に検討されているか"
      weight: 0.2
      threshold: 3.0
      
    step4_measurability:
      check: "効果測定が可能か"
      weight: 0.2
      threshold: 3.0
      
  output:
    overall_score: (各スコア × weight)の合計
    pass_threshold: 3.5
    status: "PASS" | "WARN" | "FAIL"
    recommendations: [改善提案リスト]
```

### 3. Assurance Gate（価値保証ゲートシステム）

#### ゲート種別
```yaml
gate_types:
  phase_entry_gate:
    trigger: "Phase開始時"
    checks:
      - 前Phase完了確認
      - 価値継承検証
      - 前提条件チェック
      
  phase_execution_gate:
    trigger: "Phase実行中"
    checks:
      - リアルタイム必然性判定
      - 想像パターン検出
      - 価値劣化監視
      
  phase_exit_gate:
    trigger: "Phase完了時"
    checks:
      - 成果物品質検証
      - 価値実現度測定
      - 次Phase準備確認
      
  milestone_gate:
    trigger: "MS1-MS5到達時"
    checks:
      - 価値マイルストーン達成確認
      - トレーサビリティチェーン検証
      - ROI実現度測定
```

---

## 統合アーキテクチャ

### Phase統合パターン

#### 1. Pre-Execution Hook
```yaml
pre_execution_hook:
  trigger: "Phaseコマンド実行前"
  actions:
    - プロジェクト検出確認
    - 前Phase完了ステータス確認
    - 価値トレース初期化
    - Entry Gate実行
```

#### 2. Execution Hook
```yaml
execution_hook:
  trigger: "Phase実行中"
  actions:
    - 入力データの価値根拠検証
    - リアルタイム必然性判定
    - 想像パターン検出
    - プログレス記録
```

#### 3. Post-Execution Hook
```yaml
post_execution_hook:
  trigger: "Phase実行完了後"
  actions:
    - 成果物トレース記録
    - Exit Gate実行
    - 価値実現度測定
    - 次Phase準備確認
```

### データ永続化

#### ディレクトリ構成
```
projects/{project-name}/
├── parasol.yaml                    # プロジェクト設定
├── value-traces/                   # 価値トレース記録
│   ├── phase0-traces.json
│   ├── phase1-traces.json
│   └── ...
├── necessity-checks/               # 構造的必然性判定結果
│   ├── phase0-necessity.json
│   ├── phase1-necessity.json
│   └── ...
├── gate-reports/                   # ゲート実行結果
│   ├── ms1-gate-report.json
│   ├── ms2-gate-report.json
│   └── ...
└── violation-alerts/               # 違反アラート
    ├── imagination-alerts.json
    └── value-degradation-alerts.json
```

---

## 検証・監視

### 想像の設計パターン検出

#### パターン定義
```yaml
imagination_patterns:
  pattern_1_assumption_based:
    name: "仮定ベース設計"
    signals:
      - "〜と思われる"
      - "〜のはず"
      - "一般的に〜"
    action: "BLOCK"
    
  pattern_2_trend_following:
    name: "トレンド追従"
    signals:
      - "最新だから"
      - "他社もやっているから"
      - "業界標準だから"
    action: "WARN"
    
  pattern_3_personal_preference:
    name: "個人的嗜好"
    signals:
      - "使いやすいから"
      - "きれいだから"
      - "好みに合うから"
    action: "BLOCK"
    
  pattern_4_authority_based:
    name: "権威ベース"
    signals:
      - "エキスパートが言った"
      - "コンサルが推奨"
      - "有名企業の事例"
    action: "WARN"
```

### 価値劣化検出

#### 劣化シナリオ
```yaml
value_degradation_scenarios:
  scenario_1_scope_creep:
    name: "スコープクリープ"
    detection:
      - 元のVL3から乖離した要求
      - 価値根拠のない機能追加
    threshold: "追加要求 > 20%"
    
  scenario_2_technical_drift:
    name: "技術的漂流"
    detection:
      - 技術的制約による価値妥協
      - アーキテクチャ都合の設計変更
    threshold: "価値実現度 < 80%"
    
  scenario_3_political_pressure:
    name: "政治的圧力"
    detection:
      - ステークホルダー要求による方向転換
      - ROIを無視した機能要求
    threshold: "ROI影響度 > 15%"
```

---

## パフォーマンス設計

### 応答性能要件
- Phase実行時の遅延: < 5秒
- 必然性判定: < 2秒
- レポート生成: < 10秒
- アラート発信: < 1秒

### スケーラビリティ
- 同時プロジェクト数: 100
- トレース記録保持期間: 5年
- 検索性能: < 1秒（過去1年分）

### 可用性
- システム稼働率: 99.9%
- データ整合性: 100%
- バックアップ頻度: 1日1回

---

## セキュリティ

### アクセス制御
```yaml
access_control:
  roles:
    value_architect:
      permissions:
        - value_trace_read
        - value_trace_write
        - necessity_override
        
    project_member:
      permissions:
        - value_trace_read
        - necessity_view
        
    stakeholder:
      permissions:
        - report_read
        - dashboard_view
        
  data_classification:
    value_traces: "confidential"
    necessity_checks: "internal"
    reports: "internal"
    alerts: "internal"
```

### 監査ログ
- すべての操作を監査ログに記録
- 改ざん検知機能
- 変更履歴の完全保持

---

## 運用・保守

### モニタリング指標
```yaml
monitoring_metrics:
  system_metrics:
    - トレース記録成功率
    - 判定エンジン応答時間
    - ゲート通過率
    
  business_metrics:
    - 想像設計検出数
    - 価値実現度
    - プロジェクト成功率
    
  quality_metrics:
    - 構造的必然性平均スコア
    - 価値劣化発生率
    - アラート精度
```

### 保守手順
1. **日次**: システムヘルスチェック
2. **週次**: パフォーマンス監視
3. **月次**: 検証ルール調整
4. **四半期**: システム改善

---

## 実装フェーズ

### Phase 1: コアエンジン実装（2週間）
- Value Tracer基本機能
- Necessity Judge基本判定
- 基本的なPhase統合

### Phase 2: 統合・検証機能（2週間）
- Assurance Gate実装
- 全Phase統合
- 想像パターン検出

### Phase 3: レポート・運用機能（1週間）
- ダッシュボード機能
- アラート機能
- 運用ツール

### Phase 4: テスト・文書化（1週間）
- 統合テスト
- 運用マニュアル
- トレーニング資料

---

このシステム設計により、Parasolは「想像の設計を技術的に不可能にする」フレームワークとして進化し、価値の純度を保証する強力な基盤を提供します。