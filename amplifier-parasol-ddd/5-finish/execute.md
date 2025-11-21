# /ddd:5-finish - プラットフォーム設定と完了

## 概要

このフェーズでは、パラソルV4のPhase 6（プラットフォーム）として、デプロイメント、CI/CD、監視の設定を行い、プロジェクトを完了します。

## 実行コマンド

```bash
/ddd:5-finish
```

## 実行コンテキスト

### 前提条件
- `/ddd:4-code`が完了していること
- 実装コードがテスト済みであること
- Docker環境で動作確認済みであること

### 入力
- 実装コード（4-code/outputs/）
- インフラ要件
- 運用要件

### 出力
- Kubernetes マニフェスト
- CI/CDパイプライン
- 監視ダッシュボード
- 運用ドキュメント

---

## Task 1: Kubernetes デプロイメント設定

```yaml
# k8s/personalization-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: personalization-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: personalization-api
  template:
    metadata:
      labels:
        app: personalization-api
    spec:
      containers:
      - name: api
        image: your-registry/personalization-api:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: personalization-api
  namespace: production
spec:
  selector:
    app: personalization-api
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: personalization-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: personalization-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Task 2: CI/CDパイプライン設定

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd backend
          npm ci

      - name: Run tests
        run: |
          cd backend
          npm run test:unit
          npm run test:integration

      - name: Run E2E tests
        run: |
          docker-compose -f docker-compose.test.yml up -d
          npm run test:e2e
          docker-compose -f docker-compose.test.yml down

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ secrets.REGISTRY_URL }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build and push Docker images
        run: |
          docker build -t ${{ secrets.REGISTRY_URL }}/personalization-api:${{ github.sha }} ./backend
          docker build -t ${{ secrets.REGISTRY_URL }}/personalization-ui:${{ github.sha }} ./frontend
          docker push ${{ secrets.REGISTRY_URL }}/personalization-api:${{ github.sha }}
          docker push ${{ secrets.REGISTRY_URL }}/personalization-ui:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/personalization-api \
            api=${{ secrets.REGISTRY_URL }}/personalization-api:${{ github.sha }} \
            -n production
          kubectl rollout status deployment/personalization-api -n production
```

## Task 3: 監視とロギング設定

```yaml
# monitoring/prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    scrape_configs:
      - job_name: 'personalization-api'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - production
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: keep
            regex: personalization-api

    rule_files:
      - '/etc/prometheus/rules/*.yml'

---
# monitoring/grafana-dashboard.json
{
  "dashboard": {
    "title": "Personalization Service Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~'5..'}[5m])"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "rate(container_cpu_usage_seconds_total[5m])"
          }
        ]
      }
    ]
  }
}
```

## Task 4: アラート設定

```yaml
# monitoring/alerts.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alerting-rules
  namespace: monitoring
data:
  alerts.yml: |
    groups:
      - name: personalization-alerts
        interval: 30s
        rules:
          - alert: HighErrorRate
            expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "High error rate detected"
              description: "Error rate is {{ $value }} errors per second"

          - alert: HighResponseTime
            expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "High response time"
              description: "95th percentile response time is {{ $value }} seconds"

          - alert: PodMemoryUsage
            expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: "Pod memory usage critical"
              description: "Pod {{ $labels.pod }} memory usage is above 90%"
```

## Task 5: バックアップとディザスタリカバリ

```yaml
# backup/backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: production
spec:
  schedule: "0 2 * * *"  # 毎日午前2時
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: postgres-backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - |
              DATE=$(date +%Y%m%d_%H%M%S)
              pg_dump $DATABASE_URL > /backup/backup_$DATE.sql
              aws s3 cp /backup/backup_$DATE.sql s3://your-backup-bucket/
              # 30日以上前のバックアップを削除
              find /backup -name "*.sql" -mtime +30 -delete
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
            volumeMounts:
            - name: backup
              mountPath: /backup
          restartPolicy: OnFailure
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-pvc
```

## Task 6: プラットフォーム決定記録（PDR）

```yaml
PDR-001:
  タイトル: "Kubernetesプラットフォームの採用"
  ステータス: "承認済み"

  コンテキスト:
    マイクロサービスのオーケストレーションが必要

  決定:
    本番環境でKubernetesを採用

  理由:
    - 自動スケーリング
    - 自己修復機能
    - ローリングアップデート
    - 業界標準

PDR-002:
  タイトル: "Prometheus + Grafanaによる監視"
  ステータス: "承認済み"

  決定:
    監視スタックとしてPrometheus + Grafanaを採用

  理由:
    - Kubernetesネイティブ
    - 豊富なメトリクス
    - カスタマイズ可能なダッシュボード
```

## Task 7: 運用ドキュメント

```markdown
# 運用マニュアル

## デプロイ手順
1. mainブランチにマージ
2. CI/CDパイプラインが自動実行
3. Kubernetesへの自動デプロイ

## 監視
- Grafanaダッシュボード: https://grafana.your-domain.com
- アラート通知: Slack #alerts チャンネル

## トラブルシューティング
### Pod再起動
kubectl rollout restart deployment/personalization-api -n production

### ログ確認
kubectl logs -f deployment/personalization-api -n production

### バックアップリストア
kubectl exec -it postgres-pod -- psql -U admin -d personalization < backup.sql

## 連絡先
- オンコール: PagerDuty
- エスカレーション: Tech Lead
```

---

## 検証チェックリスト

- [ ] Kubernetesマニフェストが正しく設定されているか
- [ ] CI/CDパイプラインが動作するか
- [ ] 監視とアラートが機能しているか
- [ ] バックアップが定期実行されるか
- [ ] 運用ドキュメントが完全か

---

## プロジェクト完了

すべてのフェーズが完了しました！

### 成果物サマリー

1. **価値定義**: 価値宣言と価値分解構造
2. **ビジネス設計**: ケーパビリティマトリクスとビジネスオペレーション
3. **アーキテクチャ**: 境界コンテキストとAPI仕様
4. **ソフトウェア設計**: ドメインモデルとUIコンポーネント
5. **実装**: バックエンド・フロントエンドコード
6. **プラットフォーム**: デプロイメントと監視設定

### 価値指標の測定

```yaml
KPI:
  - デプロイ頻度: 週5回以上
  - リードタイム: <2時間
  - MTTR: <30分
  - 変更失敗率: <5%
  - システム可用性: 99.9%
```

---

## 成果物の保存先

```
amplifier-parasol-ddd/
└── 5-finish/
    └── outputs/
        ├── kubernetes/
        │   ├── deployments/
        │   ├── services/
        │   └── configmaps/
        ├── ci-cd/
        │   └── .github/workflows/
        ├── monitoring/
        │   ├── prometheus/
        │   └── grafana/
        ├── backup/
        └── docs/
            └── operations-manual.md
```

---

## 継続的改善

プロジェクトは完了しましたが、価値創造は続きます：

- フィードバックループの確立
- メトリクスの継続的監視
- 定期的な振り返り
- 次のバリューマイルストーンへの準備

---

*このドキュメントはAmplifierのDDDワークフローで直接実行できます*