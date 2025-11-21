# Phase 6-1: テストと検証

## 実行コンテキスト

このドキュメントは、実装されたシステムのテストと検証を実行するための実行可能なMarkdownです。

### 前提条件
- Phase 5の実装が完了していること
- テスト環境が構築されていること
- テストデータが準備されていること

### 実行方法
```bash
/ddd:1-plan parasol/phases/phase6-validation/6-1-testing-validation.md
```

---

## 入力：テスト要件

### テスト範囲
1. **単体テスト**: 個別コンポーネント
2. **統合テスト**: API・データベース連携
3. **E2Eテスト**: ユーザーシナリオ
4. **性能テスト**: 負荷・スケーラビリティ
5. **セキュリティテスト**: 脆弱性診断

### 品質基準
```yaml
カバレッジ:
  単体テスト: 80%以上
  統合テスト: 70%以上
  E2Eテスト: 主要シナリオ100%

パフォーマンス:
  レスポンス時間: 95%tile < 500ms
  同時接続数: 1000ユーザー
  可用性: 99.9%

セキュリティ:
  OWASP Top10: 全項目対応
  ペネトレーション: Critical/High なし
```

---

## タスク：テストの実行と検証

### 実行ステップ

#### Step 1: 単体テストの実行

##### ドメインロジックテスト
```python
# tests/unit/test_carbon_footprint_domain.py
import pytest
from decimal import Decimal
from datetime import date
from domain.sustainability.carbon_footprint import CarbonFootprint, CO2Amount

class TestCarbonFootprint:
    def test_total_emission_calculation(self):
        """総排出量が正しく計算されること"""
        footprint = CarbonFootprint(
            product_id="PROD001",
            scope1_emission=CO2Amount(Decimal("10.5")),
            scope2_emission=CO2Amount(Decimal("20.3")),
            scope3_emission=CO2Amount(Decimal("15.2")),
            measurement_date=date(2024, 1, 1)
        )

        assert footprint.total_emission.value == Decimal("46.0")

    def test_certification_status_update(self):
        """認証ステータスが更新されること"""
        footprint = CarbonFootprint(
            product_id="PROD001",
            scope1_emission=CO2Amount(Decimal("10.0")),
            scope2_emission=CO2Amount(Decimal("10.0")),
            scope3_emission=CO2Amount(Decimal("10.0")),
            measurement_date=date(2024, 1, 1)
        )

        footprint.certify("認証機関A", date(2025, 1, 1))

        assert footprint.certification_status == CertificationStatus.CERTIFIED
        assert footprint.certified_by == "認証機関A"

# 実行コマンド
# pytest tests/unit/ --cov=domain --cov-report=html
```

##### サービステスト
```python
# tests/unit/test_carbon_footprint_service.py
import pytest
from unittest.mock import Mock, AsyncMock
from application.services.carbon_footprint_service import CarbonFootprintService

@pytest.mark.asyncio
class TestCarbonFootprintService:
    async def test_create_with_validation(self):
        """バリデーション付きで作成できること"""
        # Arrange
        mock_repo = Mock()
        mock_repo.find_by_product_and_date = AsyncMock(return_value=None)
        mock_repo.save = AsyncMock()

        mock_event_bus = Mock()
        mock_event_bus.publish = AsyncMock()

        service = CarbonFootprintService(mock_repo, mock_event_bus)

        # Act
        result = await service.create_footprint(valid_command)

        # Assert
        assert result.footprint_id is not None
        mock_repo.save.assert_called_once()
        mock_event_bus.publish.assert_called_once()

    async def test_duplicate_detection(self):
        """重複を検出すること"""
        # Arrange
        mock_repo = Mock()
        mock_repo.find_by_product_and_date = AsyncMock(return_value=existing_footprint)

        service = CarbonFootprintService(mock_repo, Mock())

        # Act & Assert
        with pytest.raises(DuplicateMeasurementError):
            await service.create_footprint(duplicate_command)
```

#### Step 2: 統合テストの実行

##### API統合テスト
```python
# tests/integration/test_api_integration.py
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db():
    """テスト用データベース"""
    # Setup
    create_test_database()
    yield
    # Teardown
    drop_test_database()

class TestCarbonFootprintAPI:
    def test_create_and_retrieve(self, client, test_db):
        """作成と取得のフロー"""
        # Create
        create_response = client.post(
            "/api/v1/carbon-footprints",
            json={
                "product_id": "TEST001",
                "scope1_emission": 10.5,
                "scope2_emission": 20.3,
                "scope3_emission": 15.2,
                "measurement_date": "2024-01-01",
                "measurement_method": "LCA"
            }
        )
        assert create_response.status_code == 200
        footprint_id = create_response.json()["data"]["footprint_id"]

        # Retrieve
        get_response = client.get(f"/api/v1/carbon-footprints/{footprint_id}")
        assert get_response.status_code == 200
        assert get_response.json()["data"]["product_id"] == "TEST001"

    def test_list_with_filters(self, client, test_db):
        """フィルタリング付き一覧取得"""
        # Setup: 複数データ作成
        for i in range(10):
            client.post("/api/v1/carbon-footprints", json=test_data[i])

        # Test: 製品IDでフィルタ
        response = client.get("/api/v1/carbon-footprints?product_id=PROD001")
        assert len(response.json()) == 5
```

#### Step 3: E2Eテストの実行

##### Playwrightによる画面テスト
```typescript
// tests/e2e/carbon-footprint.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Carbon Footprint Management', () => {
  test('CO2排出量の記録フロー', async ({ page }) => {
    // ログイン
    await page.goto('/login');
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password');
    await page.click('button[type="submit"]');

    // ダッシュボードへ遷移
    await expect(page).toHaveURL('/dashboard');

    // CO2排出量記録ページへ
    await page.click('a[href="/carbon-footprint/new"]');

    // フォーム入力
    await page.fill('#productId', 'PROD001');
    await page.fill('#scope1Emission', '10.5');
    await page.fill('#scope2Emission', '20.3');
    await page.fill('#scope3Emission', '15.2');
    await page.fill('#measurementDate', '2024-01-01');

    // 送信
    await page.click('button[type="submit"]');

    // 成功メッセージ確認
    await expect(page.locator('.success-message')).toContainText('記録しました');

    // 一覧に表示されることを確認
    await page.goto('/carbon-footprint');
    await expect(page.locator('table tbody tr')).toContainText('PROD001');
  });
});

// 実行コマンド
// npx playwright test
```

#### Step 4: 性能テストの実行

##### Locustによる負荷テスト
```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between
import random
import json

class CarbonFootprintUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """認証"""
        response = self.client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "password"
        })
        self.token = response.json()["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def view_list(self):
        """一覧表示（高頻度）"""
        self.client.get(
            "/api/v1/carbon-footprints",
            headers=self.headers
        )

    @task(1)
    def create_footprint(self):
        """新規作成（低頻度）"""
        self.client.post(
            "/api/v1/carbon-footprints",
            headers=self.headers,
            json={
                "product_id": f"PROD{random.randint(1, 100)}",
                "scope1_emission": random.uniform(10, 50),
                "scope2_emission": random.uniform(10, 50),
                "scope3_emission": random.uniform(10, 50),
                "measurement_date": "2024-01-01",
                "measurement_method": "LCA"
            }
        )

    @task(2)
    def view_detail(self):
        """詳細表示（中頻度）"""
        footprint_id = "some-uuid"  # 事前に取得
        self.client.get(
            f"/api/v1/carbon-footprints/{footprint_id}",
            headers=self.headers
        )

# 実行コマンド
# locust -f locustfile.py --host=http://localhost:8000 --users=1000 --spawn-rate=10
```

##### 性能結果レポート
```yaml
負荷テスト結果:
  実施日: 2024-01-15
  同時ユーザー数: 1000

  レスポンス時間:
    平均: 145ms
    中央値: 120ms
    95%tile: 485ms
    99%tile: 890ms

  スループット:
    リクエスト/秒: 3,450
    成功率: 99.8%
    エラー率: 0.2%

  リソース使用率:
    CPU: 65%
    メモリ: 4.2GB
    データベース接続: 150/200

  ボトルネック:
    - データベースクエリ最適化が必要
    - キャッシュ層の追加推奨
```

#### Step 5: セキュリティテストの実行

##### OWASP ZAPによる脆弱性スキャン
```bash
# セキュリティスキャン実行スクリプト
#!/bin/bash

# ZAPデーモン起動
zap.sh -daemon -port 8090 -config api.key=test123

# スパイダースキャン
curl "http://localhost:8090/JSON/spider/action/scan/?apikey=test123&url=http://target-app.com"

# アクティブスキャン
curl "http://localhost:8090/JSON/ascan/action/scan/?apikey=test123&url=http://target-app.com"

# レポート生成
curl "http://localhost:8090/OTHER/core/other/htmlreport/?apikey=test123" > security-report.html
```

##### セキュリティテスト結果
```yaml
セキュリティ診断結果:
  実施日: 2024-01-15
  ツール: OWASP ZAP 2.14

  発見された脆弱性:
    Critical: 0
    High: 0
    Medium: 2
      - CSRFトークンの実装不備
      - セッションタイムアウト未設定
    Low: 5
      - X-Frame-Optionsヘッダー未設定
      - その他

  対応状況:
    - CSRFトークン: 修正済み
    - セッションタイムアウト: 30分に設定
    - セキュリティヘッダー: 全て追加
```

---

## 出力：テスト結果レポート

### 生成する成果物
1. テストカバレッジレポート
2. 性能テストレポート
3. セキュリティ診断レポート
4. 不具合一覧
5. 改善提案書

### 保存先
```
projects/asahi-parasol-development/
└── phase6-validation/
    ├── test-results/
    ├── performance-reports/
    ├── security-reports/
    └── improvement-proposals/
```

---

## 検証項目

- [ ] 全テストが成功しているか
- [ ] カバレッジ基準を満たしているか
- [ ] 性能要件を満たしているか
- [ ] セキュリティ要件を満たしているか
- [ ] 不具合が修正されているか

---

## 次のステップ

このテストと検証が完了したら：

```bash
# 最適化とデプロイへ進む
/ddd:1-plan parasol/phases/phase6-validation/6-2-optimization.md

# または本番デプロイ準備
/ddd:5-finish
```

---

## 参考情報

- [実装コード](../phase5-implementation/)
- [品質基準書](../../projects/asahi-parasol-development/quality-standards.md)
- [テスト戦略書](../../projects/asahi-parasol-development/test-strategy.md)

---

*このドキュメントは実行可能なMDとして、AmplifierのDDDワークフローで処理できます。*