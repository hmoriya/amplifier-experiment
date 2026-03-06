# 価値トレーサビリティシステム運用ガイド

**作成日**: 2025-12-13  
**バージョン**: V1.0  
**対象**: システム管理者、プロジェクトマネージャー、価値アーキテクト

---

## 目次

1. [システム概要](#システム概要)
2. [セットアップ・初期設定](#セットアップ初期設定)
3. [日常運用手順](#日常運用手順)
4. [ユーザーガイド](#ユーザーガイド)
5. [トラブルシューティング](#トラブルシューティング)
6. [システム保守](#システム保守)
7. [ベストプラクティス](#ベストプラクティス)

---

## システム概要

### システムの目的

価値トレーサビリティシステムは、Parasolプロジェクトにおいて：

- **構造的必然性**と**想像の設計**を自動判別
- VL1→VL2→VL3→実装まで完全な価値追跡を実現
- VMS1-VMS5マイルストーンでの品質保証ゲートを提供
- リアルタイムで設計判断を記録・検証

### 主要コンポーネント

```yaml
system_architecture:
  core_engines:
    value_tracer: "価値トレース記録エンジン"
    necessity_judge: "構造的必然性判定エンジン"
    assurance_gate: "価値保証ゲートエンジン"
    
  integrations:
    phase_hooks: "Parasolフェーズとの自動統合"
    trace_collector: "リアルタイムデータ収集"
    gate_validator: "ゲート検証システム"
    
  outputs:
    reports: "各種レポート生成"
    dashboards: "リアルタイムダッシュボード"
    alerts: "違反アラートシステム"
```

---

## セットアップ・初期設定

### 1. システム要件確認

#### 必要な環境

```yaml
system_requirements:
  infrastructure:
    - kubernetes_cluster: "v1.24以上"
    - redis_cache: "v6.0以上"
    - postgresql_db: "v13以上"
    - mongodb: "v5.0以上"
    - elasticsearch: "v7.0以上"
    
  integrations:
    - parasol_framework: "最新版"
    - yaml_processors: "PyYAML, ruamel.yaml"
    - ml_libraries: "scikit-learn, pandas"
    
  network:
    - internet_access: "外部API接続用"
    - internal_network: "システム間通信用"
```

### 2. 初期インストール手順

#### Step 1: 基盤システムのデプロイ

```bash
# 1. システムディレクトリの作成
mkdir -p /opt/parasol-value-trace
cd /opt/parasol-value-trace

# 2. 設定ファイルの配置
cp .claude/commands/parasol/_value-traceability-system/* ./

# 3. Kubernetesリソースのデプロイ
kubectl apply -f deployment/
kubectl apply -f services/
kubectl apply -f configmaps/

# 4. データベース初期化
kubectl exec -it postgres-pod -- psql -f /scripts/init-db.sql
kubectl exec -it mongodb-pod -- mongo /scripts/init-collections.js
```

#### Step 2: 統合設定

```bash
# 1. Parasolコマンドとの統合
cd .claude/commands/parasol/
for cmd in *.md; do
  # 各コマンドファイルにトレースフックを追加
  echo "# Value Traceability Integration" >> "$cmd"
  cat _value-traceability-system/integrations/phase-hooks.yaml >> "$cmd"
done

# 2. 環境変数の設定
export VALUE_TRACE_ENABLED=true
export NECESSITY_THRESHOLD=3.5
export ALERT_CHANNELS="slack,email"
```

#### Step 3: 初期データの投入

```yaml
# config/initial-setup.yaml
initial_configuration:
  projects:
    - name: "default-project"
      value_architect: "システム管理者"
      quality_thresholds:
        necessity_minimum: 3.5
        evidence_quality: 3.0
        
  alert_channels:
    - type: "slack"
      webhook: "${SLACK_WEBHOOK_URL}"
    - type: "email"
      smtp_server: "${SMTP_SERVER}"
      
  user_roles:
    - role: "value_architect"
      permissions: ["all"]
    - role: "project_manager"
      permissions: ["read", "report"]
    - role: "developer"
      permissions: ["read", "trace"]
```

### 3. システム検証

#### ヘルスチェック実行

```bash
# 1. システム状態確認
kubectl get pods -n parasol-trace
kubectl logs -f deployment/value-tracer

# 2. 接続テスト
curl http://trace-api:8080/health
curl http://dashboard:3000/api/status

# 3. 機能テスト
cd tests/
python run_integration_tests.py
```

---

## 日常運用手順

### 1. 朝の運用チェック

#### A. システム状態確認（毎朝9:00）

```bash
#!/bin/bash
# daily-health-check.sh

echo "=== 価値トレーサビリティシステム 日次ヘルスチェック ==="
echo "チェック時刻: $(date)"

# 1. システム稼働状況
echo "1. システム稼働状況"
kubectl get pods -n parasol-trace --no-headers | \
  awk '{print $1 ": " $3}' | \
  grep -v Running && echo "⚠️ 停止中のPodがあります" || echo "✅ 全Pod正常稼働中"

# 2. データ処理状況
echo "2. データ処理状況"
TRACES_TODAY=$(curl -s http://trace-api:8080/metrics/traces/today | jq '.count')
echo "本日のトレース記録数: $TRACES_TODAY"

# 3. アラート状況
echo "3. アラート状況"
ACTIVE_ALERTS=$(curl -s http://trace-api:8080/alerts/active | jq '.count')
echo "アクティブアラート数: $ACTIVE_ALERTS"
[ $ACTIVE_ALERTS -gt 0 ] && echo "⚠️ 要確認アラートがあります"

# 4. ダッシュボード動作確認
echo "4. ダッシュボード動作確認"
curl -s -o /dev/null -w "%{http_code}" http://dashboard:3000/ | \
  grep -q "200" && echo "✅ ダッシュボード正常" || echo "❌ ダッシュボード異常"

echo "=== チェック完了 ==="
```

#### B. 重要メトリクス確認

```yaml
daily_metrics_checklist:
  system_health:
    - cpu_usage: "< 80%"
    - memory_usage: "< 80%"
    - disk_space: "< 70%"
    - response_time: "< 2秒"
    
  business_metrics:
    - traces_recorded: "前日比較"
    - quality_scores: "平均 > 3.5"
    - alert_count: "< 10件/日"
    - user_activity: "正常範囲内"
    
  data_quality:
    - completeness: "> 98%"
    - freshness: "< 30分"
    - consistency: "> 99%"
```

### 2. 週次運用作業

#### A. 品質レビュー（毎週月曜日）

```bash
#!/bin/bash
# weekly-quality-review.sh

echo "=== 週次品質レビュー実行 ==="

# 1. 週次レポート生成
curl -X POST http://trace-api:8080/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "weekly_quality",
    "date_range": "last_7_days",
    "stakeholders": ["project_manager", "value_architect"]
  }'

# 2. 品質トレンド分析
python scripts/analyze_quality_trends.py --period=week --output=weekly_analysis.pdf

# 3. 改善提案の抽出
curl http://trace-api:8080/insights/improvement_suggestions | \
  jq '.suggestions' > weekly_improvements.json

echo "週次レビュー完了。レポートを確認してください。"
```

#### B. データクリーンアップ

```sql
-- weekly-cleanup.sql
-- 90日以上経過した詳細ログを削除
DELETE FROM trace_details WHERE created_at < NOW() - INTERVAL '90 days';

-- 集約データを更新
REFRESH MATERIALIZED VIEW weekly_quality_summary;
REFRESH MATERIALIZED VIEW monthly_trend_analysis;

-- インデックスの再構築
REINDEX INDEX idx_traces_date;
REINDEX INDEX idx_necessity_scores;
```

### 3. 月次運用作業

#### A. 包括的システム評価

```yaml
monthly_evaluation:
  performance_analysis:
    - response_time_trends
    - throughput_analysis
    - resource_utilization_review
    - scalability_assessment
    
  business_impact_review:
    - value_realization_progress
    - quality_improvement_metrics
    - user_satisfaction_scores
    - roi_calculation
    
  system_optimization:
    - configuration_tuning
    - capacity_planning
    - upgrade_planning
    - security_review
```

---

## ユーザーガイド

### 1. 価値アーキテクト向け操作

#### A. プロジェクト初期設定

```yaml
# project-setup-template.yaml
project_configuration:
  name: "新規プロジェクト名"
  value_hierarchy:
    vl1: "最上位価値定義"
    vl2_groups:
      - "価値グループ1"
      - "価値グループ2"
    vl3_details:
      - vl2_parent: "価値グループ1"
        vl3_items: ["詳細価値1-1", "詳細価値1-2"]
        
  quality_thresholds:
    necessity_minimum: 3.5
    evidence_tier1_ratio: 0.6
    traceability_completeness: 0.9
    
  stakeholders:
    - name: "プロジェクトマネージャー"
      role: "project_manager"
      alert_preferences: ["high", "critical"]
    - name: "技術リード"
      role: "technical_lead"
      alert_preferences: ["medium", "high", "critical"]
```

#### B. 品質基準のカスタマイズ

```bash
# 必然性判定基準の調整
curl -X PUT http://trace-api:8080/config/necessity-criteria \
  -H "Content-Type: application/json" \
  -d '{
    "criteria_weights": {
      "value_origin": 0.35,
      "causal_proof": 0.35,
      "alternatives": 0.15,
      "measurability": 0.15
    },
    "pass_threshold": 3.5,
    "warning_threshold": 3.0
  }'
```

#### C. ダッシュボード設定

```yaml
dashboard_configuration:
  layout: "executive"
  panels:
    - type: "value_realization_gauge"
      position: "top-left"
      size: "medium"
      
    - type: "quality_trend_chart"
      position: "top-right"
      size: "large"
      timeframe: "30_days"
      
    - type: "alert_summary"
      position: "bottom-left"
      size: "small"
      severity_filter: "high_and_above"
      
    - type: "traceability_network"
      position: "bottom-right"
      size: "large"
      depth_limit: 3
      
  refresh_interval: 30
  auto_export: true
```

### 2. プロジェクトマネージャー向け操作

#### A. 進捗モニタリング

```bash
# 日次進捗確認
curl http://trace-api:8080/progress/daily-summary | jq '
{
  "milestone_progress": .milestones,
  "quality_average": .quality.average,
  "alerts_today": .alerts.count,
  "next_actions": .recommendations
}'

# 週次レポート生成
curl -X POST http://trace-api:8080/reports/generate \
  -d '{"type": "project_progress", "period": "week", "format": "pdf"}'
```

#### B. リスク管理

```yaml
risk_monitoring:
  automated_alerts:
    milestone_delay:
      threshold: "5_days_behind"
      notification: "immediate"
      escalation: "auto_escalate_to_sponsor"
      
    quality_degradation:
      threshold: "below_3.0_for_3_consecutive"
      notification: "hourly_digest"
      escalation: "manual_review_required"
      
    traceability_break:
      threshold: "any_complete_break"
      notification: "immediate"
      escalation: "block_phase_progression"
```

### 3. 開発チーム向け操作

#### A. 設計判断の記録

```bash
# 設計決定を記録
cat > design_decision.yaml << EOF
decision:
  description: "データベースにPostgreSQLを選択"
  maker: "技術リード"
  context: "VL3: データ整合性確保"
  
value_link:
  vl1: "信頼性の高いシステム"
  vl2: "データ品質保証"
  vl3: "ACID準拠のトランザクション"
  
evidence:
  - type: "benchmark"
    source: "TPC-Cベンチマーク結果"
    data: "PostgreSQL: 1500 TPS, MySQL: 1200 TPS"
    reliability: 4.5
    
  - type: "case_study"
    source: "類似プロジェクトの実績"
    data: "99.9%可用性を達成"
    reliability: 4.0
EOF

curl -X POST http://trace-api:8080/traces/record \
  -H "Content-Type: application/yaml" \
  --data-binary @design_decision.yaml
```

#### B. 必然性セルフチェック

```bash
# 自己評価の実行
curl -X POST http://trace-api:8080/necessity/self-check \
  -d '{
    "decision_id": "db-selection-2025-001",
    "self_scores": {
      "value_origin": 4.0,
      "causal_proof": 4.5,
      "alternatives": 3.5,
      "measurability": 4.0
    }
  }' | jq '.feedback'
```

---

## トラブルシューティング

### 1. 一般的な問題と解決策

#### A. システム応答が遅い

**症状**: ダッシュボードの読み込みに5秒以上かかる

**診断手順**:
```bash
# 1. システムリソース確認
kubectl top pods -n parasol-trace

# 2. データベース状況確認
kubectl exec -it postgres-pod -- psql -c "SELECT * FROM pg_stat_activity;"

# 3. キャッシュ状況確認
kubectl exec -it redis-pod -- redis-cli info memory

# 4. ネットワーク遅延確認
kubectl exec -it trace-api-pod -- ping dashboard-service
```

**解決策**:
```bash
# リソース不足の場合
kubectl scale deployment trace-api --replicas=3
kubectl apply -f resource-limits-increased.yaml

# キャッシュクリアが必要な場合
kubectl exec -it redis-pod -- redis-cli flushall

# データベース最適化
kubectl exec -it postgres-pod -- psql -c "VACUUM ANALYZE;"
```

#### B. アラートが届かない

**症状**: 重要なアラートが通知されない

**診断手順**:
```bash
# 1. アラート設定確認
curl http://trace-api:8080/config/alerts | jq '.channels'

# 2. 通知履歴確認
curl http://trace-api:8080/alerts/history?hours=24

# 3. 外部サービス接続確認
curl -I https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**解決策**:
```yaml
# alert-config-fix.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alert-config
data:
  channels: |
    slack:
      webhook_url: "https://hooks.slack.com/services/..."
      retry_count: 3
      timeout: 30
    email:
      smtp_server: "smtp.company.com"
      port: 587
      use_tls: true
```

#### C. トレーサビリティチェーンが断絶

**症状**: VL3から実装への関連が見つからない

**診断手順**:
```sql
-- 断絶箇所の特定
SELECT 
  t1.vl3_value,
  t1.implementation,
  COUNT(t2.id) as connection_count
FROM traces t1
LEFT JOIN trace_links t2 ON t1.id = t2.source_id
WHERE t1.phase = 'implementation'
GROUP BY t1.vl3_value, t1.implementation
HAVING COUNT(t2.id) = 0;
```

**解決策**:
```bash
# 手動リンク追加
curl -X POST http://trace-api:8080/traces/add-link \
  -d '{
    "source_type": "vl3",
    "source_id": "vl3-data-integrity",
    "target_type": "implementation",
    "target_id": "postgresql-config",
    "link_type": "direct_implementation",
    "strength": 0.9
  }'

# 自動関連付け再実行
curl -X POST http://trace-api:8080/traces/rebuild-links
```

### 2. パフォーマンス最適化

#### A. データベースチューニング

```sql
-- postgresql-tuning.sql

-- インデックス最適化
CREATE INDEX CONCURRENTLY idx_traces_timestamp_phase 
  ON traces(timestamp DESC, phase) WHERE status = 'active';

CREATE INDEX CONCURRENTLY idx_necessity_scores_composite
  ON necessity_evaluations(project_id, phase, total_score DESC);

-- 統計情報更新
ANALYZE traces;
ANALYZE necessity_evaluations;
ANALYZE trace_links;

-- 不要データ削除
DELETE FROM trace_details WHERE created_at < NOW() - INTERVAL '180 days';
```

#### B. キャッシュ最適化

```bash
# Redis設定最適化
kubectl exec -it redis-pod -- redis-cli config set maxmemory-policy allkeys-lru
kubectl exec -it redis-pod -- redis-cli config set maxmemory 2gb

# アプリケーションキャッシュ設定
curl -X PUT http://trace-api:8080/config/cache \
  -d '{
    "ttl": {
      "dashboard_data": 300,
      "reports": 3600,
      "user_preferences": 86400
    },
    "strategy": "write_through"
  }'
```

---

## システム保守

### 1. 定期メンテナンス

#### A. バックアップ手順

```bash
#!/bin/bash
# backup-script.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/parasol-trace/$DATE"
mkdir -p $BACKUP_DIR

# 1. PostgreSQLダンプ
kubectl exec postgres-pod -- pg_dump parasol_trace > $BACKUP_DIR/postgres.sql

# 2. MongoDB エクスポート
kubectl exec mongodb-pod -- mongodump --db parasol_trace --out /tmp/mongodump
kubectl cp mongodb-pod:/tmp/mongodump $BACKUP_DIR/mongodb/

# 3. Redis データ保存
kubectl exec redis-pod -- redis-cli bgsave
kubectl cp redis-pod:/data/dump.rdb $BACKUP_DIR/redis.rdb

# 4. 設定ファイル
kubectl get configmaps -o yaml > $BACKUP_DIR/configmaps.yaml
kubectl get secrets -o yaml > $BACKUP_DIR/secrets.yaml

# 5. バックアップ完了通知
echo "バックアップ完了: $BACKUP_DIR" | \
  mail -s "Parasol Trace Backup Complete" admin@company.com

# 6. 古いバックアップ削除（30日以上）
find /opt/backups/parasol-trace -type d -mtime +30 -exec rm -rf {} \;
```

#### B. セキュリティパッチ適用

```bash
#!/bin/bash
# security-update.sh

echo "セキュリティパッチ適用開始"

# 1. システム一時停止
kubectl scale deployment --all --replicas=0 -n parasol-trace

# 2. イメージ更新
kubectl set image deployment/trace-api trace-api=parasol/trace-api:security-patch-v1.2.3
kubectl set image deployment/dashboard dashboard=parasol/dashboard:security-patch-v1.2.3

# 3. 設定更新
kubectl apply -f security-updates/

# 4. サービス再開
kubectl scale deployment trace-api --replicas=3 -n parasol-trace
kubectl scale deployment dashboard --replicas=2 -n parasol-trace

# 5. 動作確認
sleep 60
kubectl get pods -n parasol-trace
curl http://trace-api:8080/health

echo "セキュリティパッチ適用完了"
```

### 2. モニタリング・アラート

#### A. システムメトリクス監視

```yaml
# monitoring-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: monitoring-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    
    scrape_configs:
      - job_name: 'parasol-trace-api'
        static_configs:
          - targets: ['trace-api:8080']
        metrics_path: /metrics
        
      - job_name: 'parasol-dashboard'
        static_configs:
          - targets: ['dashboard:3000']
          
    rule_files:
      - "alert_rules.yml"
      
    alerting:
      alertmanagers:
        - static_configs:
            - targets: ['alertmanager:9093']

  alert_rules.yml: |
    groups:
      - name: parasol-trace-alerts
        rules:
          - alert: HighResponseTime
            expr: trace_api_response_time > 2
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "API応答時間が遅延しています"
              
          - alert: LowQualityScores
            expr: avg(necessity_quality_score) < 3.5
            for: 10m
            labels:
              severity: critical
            annotations:
              summary: "品質スコアが基準を下回っています"
```

#### B. ログ管理

```yaml
# logging-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: logging-config
data:
  fluentd.conf: |
    <source>
      @type tail
      path /var/log/parasol-trace/*.log
      pos_file /var/log/fluentd/parasol-trace.log.pos
      tag parasol.trace.*
      format json
      time_key timestamp
      time_format %Y-%m-%dT%H:%M:%S.%L%z
    </source>
    
    <filter parasol.trace.**>
      @type record_transformer
      <record>
        service ${tag_parts[2]}
        environment "production"
      </record>
    </filter>
    
    <match parasol.trace.**>
      @type elasticsearch
      host elasticsearch-service
      port 9200
      index_name parasol-trace-logs
      type_name _doc
    </match>
```

---

## ベストプラクティス

### 1. 運用のベストプラクティス

#### A. プロアクティブ監視

```yaml
proactive_monitoring:
  leading_indicators:
    - trace_record_frequency_decline
    - quality_score_trend_analysis
    - user_engagement_metrics
    - system_resource_utilization
    
  predictive_maintenance:
    - capacity_planning_quarterly
    - performance_trend_analysis
    - failure_pattern_recognition
    - upgrade_schedule_optimization
```

#### B. 効率的なインシデント対応

```yaml
incident_response:
  severity_levels:
    p1_critical:
      response_time: "15分以内"
      escalation: "自動でCTO/CTOに通知"
      resolution_target: "1時間以内"
      
    p2_high:
      response_time: "30分以内"
      escalation: "1時間後にマネージャーに通知"
      resolution_target: "4時間以内"
      
    p3_medium:
      response_time: "2時間以内"
      escalation: "24時間後に確認"
      resolution_target: "24時間以内"
      
  escalation_matrix:
    level_1: "システム管理者"
    level_2: "技術マネージャー"
    level_3: "CTO"
    level_4: "CEO"
```

### 2. 品質管理のベストプラクティス

#### A. 継続的品質向上

```yaml
quality_improvement_cycle:
  measurement:
    - weekly_quality_metrics_review
    - monthly_trend_analysis
    - quarterly_comprehensive_audit
    
  analysis:
    - root_cause_identification
    - pattern_recognition
    - improvement_opportunity_assessment
    
  improvement:
    - action_plan_development
    - implementation_tracking
    - results_measurement
    
  standardization:
    - best_practice_documentation
    - training_material_updates
    - process_refinement
```

#### B. データ品質管理

```yaml
data_quality_practices:
  validation:
    - input_data_validation
    - consistency_checking
    - completeness_verification
    - accuracy_assessment
    
  cleansing:
    - duplicate_removal
    - format_standardization
    - missing_value_handling
    - outlier_detection
    
  monitoring:
    - real_time_quality_metrics
    - quality_degradation_alerts
    - trend_analysis
    - stakeholder_reporting
```

### 3. セキュリティベストプラクティス

#### A. アクセス制御

```yaml
access_control:
  authentication:
    - multi_factor_authentication
    - sso_integration
    - session_timeout_30min
    
  authorization:
    - role_based_access_control
    - principle_of_least_privilege
    - regular_permission_review
    
  audit:
    - comprehensive_audit_logging
    - access_pattern_analysis
    - suspicious_activity_monitoring
```

#### B. データ保護

```yaml
data_protection:
  encryption:
    - at_rest: "AES-256"
    - in_transit: "TLS 1.3"
    - key_rotation: "quarterly"
    
  backup:
    - encrypted_backups
    - offsite_storage
    - recovery_testing_monthly
    
  privacy:
    - data_anonymization
    - retention_policy_compliance
    - gdpr_compliance
```

---

## まとめ

この運用ガイドに従うことで、価値トレーサビリティシステムを安全かつ効率的に運用できます。

### 重要な運用原則

1. **プロアクティブ監視**: 問題が発生する前に対処
2. **継続的改善**: 定期的な見直しと最適化
3. **品質第一**: 品質を犠牲にしないスピード重視
4. **セキュリティ最優先**: 常にセキュリティを最優先に考慮
5. **ステークホルダー第一**: 利用者の体験を最優先

### 緊急時連絡先

```yaml
emergency_contacts:
  system_admin: "admin@company.com / +81-XX-XXXX-XXXX"
  technical_lead: "tech-lead@company.com / +81-XX-XXXX-XXXX"
  vendor_support: "support@parasol-vendor.com / +1-XXX-XXX-XXXX"
```

**価値トレーサビリティシステムの成功は、適切な運用にかかっています。このガイドを定期的に見直し、継続的に改善していきましょう。**