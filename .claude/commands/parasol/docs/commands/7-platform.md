---
description: Platform and deployment setup (project:parasol)
---

# Parasol V5 - Phase 7: Platform

プラットフォーム層の設計とインフラストラクチャ構成を定義します。

## 使用方法

```bash
/parasol:7-platform              # プラットフォーム全体設計
/parasol:7-platform infra        # インフラ設計のみ
/parasol:7-platform cicd         # CI/CDパイプライン設計
/parasol:7-platform monitoring   # 監視・可観測性設計
```

## 目的

Phase 6で実装されたサービス群のプラットフォーム層を設計し、**VMS5マイルストーン達成**を目指します：

- インフラストラクチャ設計
- CI/CDパイプライン構築
- 監視・可観測性システム
- デプロイメント戦略
- **VMS5達成状況評価**
- **プロダクションレディネス評価**

## VMS5 マイルストーン: 顧客が期待を超える価値を享受している状態

```yaml
VMS5_Production_Platform_Milestone:
  target_completion: "Phase 6完了から8週間"
  description: "プロダクション本番稼働に必要な基盤の完成"
  success_criteria:
    infrastructure_readiness: "本番環境インフラ100%準備完了"
    deployment_automation: "ゼロタッチデプロイメント達成"
    observability_coverage: "全サービス監視・アラート完備"
    security_compliance: "セキュリティ要件100%充足"
    disaster_recovery: "DR手順確立・テスト完了"
    performance_validation: "負荷テスト・SLA確認完了"
  
  key_deliverables:
    - "プロダクション環境（K8s/Cloud）"
    - "CI/CDパイプライン（GitOps）"
    - "監視基盤（メトリクス/ログ/トレース）"
    - "セキュリティ基盤（認証/認可/暗号化）"
    - "災害復旧計画（バックアップ/復旧手順）"
    - "運用手順書（デプロイ/監視/障害対応）"
  
  quality_gates:
    - "インフラコード化率: 100%"
    - "デプロイ自動化率: 100%"
    - "監視カバレッジ: 95%以上"
    - "セキュリティスキャン: 合格"
    - "DR演習: 成功"
  
  business_value:
    - "安定したサービス提供基盤の確立"
    - "迅速な機能リリースサイクルの実現"
    - "運用コストの最適化"
    - "セキュリティリスクの最小化"
    - "ビジネス継続性の保証"
```



## 🔧 プロジェクト検出

**重要**: このコマンドはParasolプロジェクト内で実行する必要があります。

### 自動検出

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：

1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)
3. **祖父ディレクトリ** (`../..`)

### 検出成功

```
✅ プロジェクト検出: {project-name}

プロジェクトディレクトリ: projects/{project-name}/
出力先: projects/{project-name}/outputs/
```

プロジェクト設定を読み込み、Phase進捗を自動記録します。

### 検出失敗

```
❌ Parasolプロジェクトが見つかりません

📋 次のアクションを選択してください:

1. 新しいプロジェクトを作成
   → /parasol:project init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol:project list
```

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/parasol:1-context

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/parasol:1-context  # ❌
```

詳細は `.claude/commands/parasol/_project-detection.md` を参照。

## 前提条件

Phase 6: Implementation が完了している必要があります：
- [ ] VMS4マイルストーン（顧客が全面的に価値を実感している状態）完了
- [ ] Implementation guide 完成
- [ ] コードスケルトン生成済み
- [ ] デプロイ要件明確化

## VMS5達成に向けた設計原則

### プロダクションレディネス
- **信頼性**: 99.9%以上のSLA達成
- **スケーラビリティ**: トラフィック10倍増に対応
- **セキュリティ**: ゼロトラスト原則の適用
- **保守性**: Infrastructure as Code による管理
- **可観測性**: 問題の迅速な検知・診断・解決

### 運用効率性
- **自動化**: 手作業を最小限に削減
- **再現性**: 環境構築の完全自動化
- **復旧性**: RPO/RTO目標の達成
- **コスト効率**: リソース使用量の最適化

### 🔬 AD原則適用

> 📚 [zigzag-foundations.md](../philosophy/zigzag-foundations.md#axiomatic-designの2つの公理)

**Phase 7チェック**:
- [ ] 各サービスが独立デプロイ可能
- [ ] 障害影響が局所化
- [ ] インフラ構成が必要最小限

## 実行

ユーザーからのパラメータを確認し、以下のいずれかを実行：

### パラメータなしの場合（プラットフォーム全体設計）

outputs/7-platform/ に以下の成果物を生成：

**1. infrastructure-design.md**
```markdown
# インフラストラクチャ設計

## コンテナオーケストレーション
- Kubernetes クラスタ構成
- Namespace 設計
- Resource Quotas/Limits
- Network Policies

## クラウドサービス
- Managed Services 選定
- RDS/Cloud SQL (Database)
- ElastiCache/Memorystore (Cache)
- S3/Cloud Storage (Object Storage)
- SQS/Pub/Sub (Message Queue)

## ネットワーク設計
- VPC/Subnet 構成
- Load Balancer 配置
- Service Mesh (Istio/Linkerd)
- Ingress Controller

## セキュリティ
- IAM/RBAC 設計
- Secrets Management (Vault/AWS Secrets Manager)
- Network Security (Firewall Rules)
- TLS/mTLS 構成

## スケーラビリティ
- Horizontal Pod Autoscaling (HPA)
- Cluster Autoscaling
- Database Scaling 戦略
```

**2. cicd-pipeline.md**
```markdown
# CI/CD パイプライン設計

## ビルドパイプライン
```yaml
stages:
- lint_and_test
- build
- security_scan
- deploy_staging
- integration_test
- deploy_production

lint_and_test:
- ESLint/Prettier チェック
- Unit Tests (Jest)
- Integration Tests
- Code Coverage (>80%)

build:
- Docker Image Build
- Multi-stage Build 最適化
- Image Tagging (commit SHA, semver)

security_scan:
- Container Image Scan (Trivy/Snyk)
- Dependency Vulnerability Check
- SAST (Static Application Security Testing)

deploy_staging:
- Kubernetes Manifest Apply
- Database Migration (Flyway/Liquibase)
- Smoke Tests

integration_test:
- End-to-End Tests (Playwright)
- Performance Tests (k6)
- Security Tests (OWASP ZAP)

deploy_production:
- Manual Approval Gate
- Blue-Green Deployment
- Canary Deployment
- Rollback Strategy
```

## GitOps
- ArgoCD/FluxCD 設定
- Git Repository 構成
- Application Code
- Kubernetes Manifests
- Helm Charts/Kustomize
- Environment Promotion (dev → staging → prod)

## デプロイメント戦略
- Rolling Update (デフォルト)
- Blue-Green Deployment (重要サービス)
- Canary Deployment (リスク高い変更)
```

**3. monitoring-observability.md**
```markdown
# 監視と可観測性

## メトリクス収集
- Prometheus + Grafana
- Golden Signals (Latency, Traffic, Errors, Saturation)
- Business Metrics (Custom metrics)
- Infrastructure Metrics (Node/Pod)

## ログ集約
- ELK Stack / Loki + Grafana
- Centralized Logging
- Structured Logging (JSON format)
- Log Retention Policy

## 分散トレーシング
- Jaeger / Zipkin
- End-to-End Request Tracing
- Service Dependency Map
- Performance Bottleneck 特定

## アラート設定
```yaml
alerts:
- name: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
severity: critical

- name: HighLatency
expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
severity: warning

- name: PodRestartingTooFrequently
expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
severity: warning
```

## ダッシュボード
- Service Overview Dashboard
- Resource Utilization Dashboard
- Business Metrics Dashboard
- SLI/SLO Tracking Dashboard
```

**4. deployment-strategy.md**
```markdown
# デプロイメント戦略

## 環境構成
- Development (開発環境)
- Staging (ステージング環境)
- Production (本番環境)

## デプロイメントパターン

### Rolling Update
- デフォルト戦略
- 段階的にPodを置き換え
- ゼロダウンタイム
- 適用: 低リスクの変更

### Blue-Green Deployment
- 新環境(Green)を完全に構築
- トラフィックを一気に切り替え
- 即座にロールバック可能
- 適用: データベーススキーマ変更を伴う場合

### Canary Deployment
- 小規模なユーザーに先行リリース
- メトリクスを監視しながら段階的に拡大
- 問題検知でロールバック
- 適用: リスクの高い機能変更

## データベースマイグレーション
- Backward Compatible な変更
- Blue-Green Deployment での実行
- Rollback スクリプト準備
- Production での事前検証 (Staging)

## ロールバック計画
- 自動ロールバック条件
- Error Rate > 5%
- Latency > 2x baseline
- Health Check 失敗
- 手動ロールバック手順
- データ整合性の考慮
```

**5. disaster-recovery.md**
```markdown
# 災害復旧計画

## バックアップ戦略
- Database: 毎日フルバックアップ + 継続的WALアーカイブ
- Object Storage: Cross-Region Replication
- Configuration: GitOps Repository (自動バックアップ)
- Secrets: Encrypted Backup

## RTO/RPO 目標
- RTO (Recovery Time Objective): 4時間
- RPO (Recovery Point Objective): 1時間

## 復旧手順
1. 影響範囲の特定
2. バックアップからのリストア
3. データ整合性チェック
4. サービス再起動
5. 正常性確認
6. 事後分析 (Post-mortem)
```

### infra パラメータ指定時

infrastructure-design.md のみを詳細に生成

### cicd パラメータ指定時

cicd-pipeline.md のみを詳細に生成

### monitoring パラメータ指定時

monitoring-observability.md のみを詳細に生成

## 成果物一覧

```
outputs/7-platform/
├── infrastructure-design.md      # インフラ設計
├── cicd-pipeline.md              # CI/CDパイプライン
├── monitoring-observability.md   # 監視・可観測性
├── deployment-strategy.md        # デプロイメント戦略
├── disaster-recovery.md          # 災害復旧計画
└── kubernetes/                   # Kubernetesマニフェスト
├── base/                     # 共通設定
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── ingress.yaml
├── overlays/
│   ├── dev/
│   ├── staging/
│   └── production/
└── helm/                     # Helm Charts
└── {service-name}/
├── Chart.yaml
├── values.yaml
└── templates/
```

## エラーケース

**Phase 6 が完了していない:**
```
⚠️ Phase 6: Implementation が完了していません

先に実装ガイドを完成させてください:
→ `/parasol:6-implementation`
```

**outputs/ ディレクトリが存在しない:**
```
⚠️ Parasolプロジェクトが初期化されていません

最初に Context を確立してください:
→ `/parasol:1-context`
```

## VMS5達成評価

Phase 7完了時に以下の評価を実施し、VMS5マイルストーン達成を確認します：

### インフラストラクチャ評価
- [ ] プロダクション環境の完全構築
- [ ] オートスケーリング機能の動作確認
- [ ] ネットワークセキュリティの実装確認
- [ ] 災害復旧手順の動作確認

### デプロイメント評価
- [ ] ゼロタッチデプロイメントの実現
- [ ] ロールバック機能の動作確認
- [ ] Blue-Green/Canaryデプロイメントの実装
- [ ] セキュリティスキャンの自動化

### 運用準備度評価
- [ ] 監視ダッシュボードの完備
- [ ] アラート設定の妥当性確認
- [ ] 運用手順書の整備完了
- [ ] オンコール体制の確立

### VMS5完了報告書
以下の成果物でVMS5達成を証明：
- プロダクション環境構築完了報告書
- 負荷テスト結果報告書
- セキュリティ監査完了報告書
- 災害復旧テスト完了報告書
- SLA達成可能性評価書

## 次のステップ

**VMS5達成後の実運用移行**:
1. Kubernetes マニフェストの適用
2. CI/CD パイプラインの構築
3. 監視ダッシュボードのセットアップ
4. Staging 環境でのエンドツーエンドテスト
5. Production デプロイメント
6. **VMS5マイルストーン達成宣言**

## バリデーション連携

Platform 設計後、全体検証を実施:
```
/parasol:validate platform
/parasol:status vms5  # VMS5達成状況確認
```

## 関連コマンド

- `/parasol:6-implementation` - Phase 6: 実装ガイド
- `/parasol:status` - 進捗確認
- `/parasol:validate` - 全体検証
