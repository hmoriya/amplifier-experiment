# Parasol 実装ガイド

**作成日**: 2025-12-12  
**バージョン**: V5.1  
**基本哲学**: PHILOSOPHY.mdに基づく実装レベルの具体的指針

---

## 目的

このガイドは、Parasolの「保守性と変更容易性」の哲学を、日々のコーディングで実践するための具体的な指針を提供します。

---

## 1. コーディング原則

### 明示的な依存関係

```python
# ❌ 避けるべき: 暗黙的な依存
class OrderService:
    def create_order(self):
        # グローバルなイベントバスに依存
        EventBus.publish("order_created", {...})

# ✅ 推奨: 明示的な依存注入
class OrderService:
    def __init__(self, notification_api: NotificationAPI):
        self.notification_api = notification_api
    
    def create_order(self):
        # 明示的なAPI呼び出し
        result = self.notification_api.notify_order_created({...})
        if not result.success:
            # エラーハンドリングも明示的
            raise NotificationError(result.error)
```

### 同期的エラーハンドリング

```python
# ❌ 避けるべき: fire-and-forget
async def process_order():
    asyncio.create_task(send_notification())  # エラーが失われる

# ✅ 推奨: 明示的なエラー処理
async def process_order():
    try:
        notification_result = await send_notification()
        return ProcessResult(
            status="success",
            notification_sent=True
        )
    except NotificationError as e:
        # 部分的な成功として処理
        return ProcessResult(
            status="partial_success",
            notification_sent=False,
            error=str(e)
        )
```

---

## 2. モジュール設計指針

### ディレクトリ構造

```
services/
├── order/                      # サービス（デプロイ単位）
│   ├── api.py                 # 公開API定義（OpenAPI対応）
│   ├── models.py              # ドメインモデル
│   ├── service.py             # ビジネスロジック
│   ├── repository.py          # データアクセス層
│   └── tests/                 # ユニットテスト
│       ├── test_service.py
│       └── test_api.py
├── integration/                # 統合層
│   ├── inventory_client.py    # 外部サービスクライアント
│   └── order_hub.py          # Integration Hub実装
└── shared/                    # 共有コンポーネント
    ├── monitoring.py         # 監視・メトリクス
    └── diagnostics.py        # 診断ツール
```

### サービス間通信の標準化

```python
from typing import Optional, Protocol
from dataclasses import dataclass

# 標準レスポンス形式
@dataclass
class ApiResponse:
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    retry_after: Optional[int] = None  # 秒単位

# サービスクライアントの標準実装
class ServiceClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.circuit_breaker = CircuitBreaker()
    
    async def call(self, endpoint: str, method: str = "GET", **kwargs):
        if self.circuit_breaker.is_open:
            return ApiResponse(
                success=False,
                error="Service unavailable",
                error_code="CIRCUIT_OPEN"
            )
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=f"{self.base_url}{endpoint}",
                    **kwargs
                )
                
                if response.status_code >= 500:
                    self.circuit_breaker.record_failure()
                else:
                    self.circuit_breaker.record_success()
                
                return ApiResponse(
                    success=200 <= response.status_code < 300,
                    data=response.json() if response.status_code == 200 else None,
                    error=response.text if response.status_code >= 400 else None
                )
                
        except httpx.TimeoutException:
            self.circuit_breaker.record_failure()
            return ApiResponse(
                success=False,
                error="Request timeout",
                error_code="TIMEOUT",
                retry_after=5
            )
```

---

## 3. 運用可観測性の実装

### 構造化ログ

```python
import structlog
from datetime import datetime

# ロガー設定
logger = structlog.get_logger()

class ObservableService:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logger.bind(service=service_name)
    
    async def process_request(self, request_id: str, operation: str):
        # リクエストコンテキストの設定
        log = self.logger.bind(
            request_id=request_id,
            operation=operation,
            timestamp=datetime.utcnow().isoformat()
        )
        
        log.info("処理開始")
        start_time = datetime.utcnow()
        
        try:
            # ビジネスロジック
            result = await self._execute(operation)
            
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            log.info(
                "処理完了",
                duration_ms=duration_ms,
                result_size=len(result) if hasattr(result, '__len__') else None
            )
            
            return result
            
        except Exception as e:
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            log.error(
                "処理失敗",
                error_type=type(e).__name__,
                error_message=str(e),
                duration_ms=duration_ms,
                stack_trace=traceback.format_exc()
            )
            raise
```

### メトリクスの実装

```python
from prometheus_client import Counter, Histogram, Gauge
import functools

# メトリクス定義
request_count = Counter(
    'parasol_requests_total',
    'Total number of requests',
    ['service', 'operation', 'status']
)

request_duration = Histogram(
    'parasol_request_duration_seconds',
    'Request duration in seconds',
    ['service', 'operation']
)

active_requests = Gauge(
    'parasol_active_requests',
    'Number of active requests',
    ['service']
)

# デコレーターによる自動計測
def track_metrics(operation: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            # アクティブリクエスト数を増やす
            active_requests.labels(service=self.service_name).inc()
            
            # 実行時間の計測開始
            with request_duration.labels(
                service=self.service_name,
                operation=operation
            ).time():
                try:
                    result = await func(self, *args, **kwargs)
                    request_count.labels(
                        service=self.service_name,
                        operation=operation,
                        status="success"
                    ).inc()
                    return result
                    
                except Exception as e:
                    request_count.labels(
                        service=self.service_name,
                        operation=operation,
                        status="error"
                    ).inc()
                    raise
                    
                finally:
                    active_requests.labels(service=self.service_name).dec()
        
        return wrapper
    return decorator
```

---

## 4. テスト戦略

### ユニットテストの原則

```python
import pytest
from unittest.mock import Mock, AsyncMock

class TestOrderService:
    @pytest.fixture
    def mock_dependencies(self):
        return {
            'inventory_client': AsyncMock(spec=InventoryClient),
            'payment_client': AsyncMock(spec=PaymentClient),
            'notification_client': AsyncMock(spec=NotificationClient)
        }
    
    @pytest.mark.asyncio
    async def test_create_order_success(self, mock_dependencies):
        # Given
        mock_dependencies['inventory_client'].check_stock.return_value = ApiResponse(
            success=True,
            data={'available': True}
        )
        mock_dependencies['payment_client'].process_payment.return_value = ApiResponse(
            success=True,
            data={'transaction_id': 'TXN123'}
        )
        
        service = OrderService(**mock_dependencies)
        
        # When
        result = await service.create_order({
            'items': [{'id': 'ITEM1', 'quantity': 2}],
            'payment': {'amount': 1000}
        })
        
        # Then
        assert result.success
        assert result.data['order_id'] is not None
        mock_dependencies['inventory_client'].check_stock.assert_called_once()
        mock_dependencies['payment_client'].process_payment.assert_called_once()
```

### 統合テストの実装

```python
import docker
import pytest
import time
from typing import Generator

class IntegrationTestBase:
    @pytest.fixture(scope="session")
    def docker_services(self) -> Generator[dict, None, None]:
        """Docker Composeによるサービス起動"""
        client = docker.from_env()
        
        # docker-compose.test.ymlからサービスを起動
        services = {
            'postgres': {
                'image': 'postgres:15',
                'port': 5432,
                'env': {'POSTGRES_PASSWORD': 'test'}
            },
            'redis': {
                'image': 'redis:7',
                'port': 6379
            }
        }
        
        containers = {}
        try:
            for name, config in services.items():
                container = client.containers.run(
                    config['image'],
                    detach=True,
                    ports={f"{config['port']}/tcp": config['port']},
                    environment=config.get('env', {})
                )
                containers[name] = container
                
            # サービスの起動を待つ
            time.sleep(5)
            
            yield {
                'postgres_url': 'postgresql://localhost:5432/test',
                'redis_url': 'redis://localhost:6379'
            }
            
        finally:
            # クリーンアップ
            for container in containers.values():
                container.stop()
                container.remove()
```

---

## 5. 段階的移行パターン

### Dual-Write実装

```python
from typing import Protocol
from dataclasses import dataclass
import logging

class StorageBackend(Protocol):
    async def write(self, data: dict) -> dict:
        ...
    
    async def read(self, key: str) -> dict:
        ...

@dataclass
class MigrationMetrics:
    total_writes: int = 0
    successful_matches: int = 0
    mismatches: int = 0
    new_system_failures: int = 0
    
    @property
    def match_rate(self) -> float:
        if self.total_writes == 0:
            return 0.0
        return self.successful_matches / self.total_writes

class DualWriteManager:
    def __init__(
        self,
        old_backend: StorageBackend,
        new_backend: StorageBackend,
        comparison_logger: logging.Logger
    ):
        self.old_backend = old_backend
        self.new_backend = new_backend
        self.comparison_logger = comparison_logger
        self.metrics = MigrationMetrics()
    
    async def write(self, data: dict) -> dict:
        # 旧システムへの書き込み（Primary）
        old_result = await self.old_backend.write(data)
        self.metrics.total_writes += 1
        
        # 新システムへの書き込み（Secondary）
        try:
            new_result = await self.new_backend.write(data)
            
            # 結果の比較
            if self._compare_results(old_result, new_result):
                self.metrics.successful_matches += 1
            else:
                self.metrics.mismatches += 1
                self.comparison_logger.warning(
                    "Result mismatch",
                    extra={
                        'data': data,
                        'old_result': old_result,
                        'new_result': new_result
                    }
                )
        
        except Exception as e:
            self.metrics.new_system_failures += 1
            self.comparison_logger.error(
                "New system write failed",
                extra={'data': data, 'error': str(e)}
            )
        
        # 常に旧システムの結果を返す
        return old_result
    
    def is_ready_for_migration(self) -> bool:
        """移行準備状況の判定"""
        return (
            self.metrics.match_rate > 0.99 and
            self.metrics.total_writes > 10000 and
            self.metrics.new_system_failures == 0
        )
```

### Feature Toggle実装

```python
from enum import Enum
from typing import Dict, Any

class FeatureState(Enum):
    OFF = "off"
    SHADOW = "shadow"  # 新機能を実行するが結果は使わない
    CANARY = "canary"  # 一部のユーザーのみ
    ON = "on"

class FeatureToggle:
    def __init__(self, config_source: str = "features.json"):
        self.config_source = config_source
        self.features: Dict[str, FeatureState] = {}
        self._load_config()
    
    def is_enabled(self, feature: str, context: Dict[str, Any] = None) -> bool:
        state = self.features.get(feature, FeatureState.OFF)
        
        if state == FeatureState.OFF:
            return False
        elif state == FeatureState.ON:
            return True
        elif state == FeatureState.CANARY:
            # カナリアロジック（例：ユーザーIDのハッシュで判定）
            if context and 'user_id' in context:
                return hash(context['user_id']) % 100 < 10  # 10%のユーザー
            return False
        elif state == FeatureState.SHADOW:
            # シャドウモードでは常にFalse（別途実行するが結果は使わない）
            return False
        
        return False
    
    def execute_with_toggle(
        self,
        feature: str,
        new_implementation,
        old_implementation,
        context: Dict[str, Any] = None
    ):
        """Feature Toggleによる実装の切り替え"""
        state = self.features.get(feature, FeatureState.OFF)
        
        if state == FeatureState.SHADOW:
            # 両方実行して比較
            old_result = old_implementation()
            try:
                new_result = new_implementation()
                self._compare_results(feature, old_result, new_result)
            except Exception as e:
                self._log_shadow_failure(feature, e)
            return old_result
        
        elif self.is_enabled(feature, context):
            return new_implementation()
        else:
            return old_implementation()
```

---

## 6. エラーハンドリングパターン

### 統一エラー分類

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class ErrorCategory(Enum):
    VALIDATION = "validation"      # 400: 入力検証エラー
    BUSINESS = "business"          # 422: ビジネスルール違反
    NOT_FOUND = "not_found"        # 404: リソース不在
    CONFLICT = "conflict"          # 409: 競合状態
    EXTERNAL = "external"          # 503: 外部サービスエラー
    INTERNAL = "internal"          # 500: 内部エラー

@dataclass
class ServiceError(Exception):
    category: ErrorCategory
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    retry_after: Optional[int] = None  # 秒単位
    
    def to_response(self) -> dict:
        return {
            'error': {
                'category': self.category.value,
                'code': self.code,
                'message': self.message,
                'details': self.details,
                'retry_after': self.retry_after
            }
        }

# エラーハンドラーの実装
class ErrorHandler:
    @staticmethod
    def handle_external_error(e: Exception) -> ServiceError:
        if isinstance(e, httpx.TimeoutException):
            return ServiceError(
                category=ErrorCategory.EXTERNAL,
                code="EXTERNAL_TIMEOUT",
                message="外部サービスがタイムアウトしました",
                retry_after=5
            )
        elif isinstance(e, httpx.HTTPStatusError):
            return ServiceError(
                category=ErrorCategory.EXTERNAL,
                code="EXTERNAL_ERROR",
                message=f"外部サービスエラー: {e.response.status_code}",
                details={'status_code': e.response.status_code}
            )
        else:
            return ServiceError(
                category=ErrorCategory.INTERNAL,
                code="UNKNOWN_ERROR",
                message="予期しないエラーが発生しました"
            )
```

---

## 7. 診断ツールの実装

### ヘルスチェックエンドポイント

```python
from typing import Dict, Any
from datetime import datetime

class HealthChecker:
    def __init__(self):
        self.checks = {}
        self.startup_time = datetime.utcnow()
    
    def register_check(self, name: str, check_fn):
        """ヘルスチェック関数の登録"""
        self.checks[name] = check_fn
    
    async def check_health(self) -> Dict[str, Any]:
        """包括的なヘルスチェック"""
        results = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'uptime_seconds': (datetime.utcnow() - self.startup_time).total_seconds(),
            'checks': {}
        }
        
        for name, check_fn in self.checks.items():
            try:
                start = datetime.utcnow()
                result = await check_fn()
                duration_ms = (datetime.utcnow() - start).total_seconds() * 1000
                
                results['checks'][name] = {
                    'status': 'pass' if result else 'fail',
                    'duration_ms': duration_ms
                }
                
                if not result:
                    results['status'] = 'degraded'
                    
            except Exception as e:
                results['checks'][name] = {
                    'status': 'error',
                    'error': str(e)
                }
                results['status'] = 'unhealthy'
        
        return results

# 使用例
health_checker = HealthChecker()

# データベース接続チェック
async def check_database():
    try:
        await db.execute("SELECT 1")
        return True
    except:
        return False

health_checker.register_check('database', check_database)

# 外部API疎通チェック
async def check_external_api():
    try:
        response = await httpx.get("https://api.example.com/health", timeout=5)
        return response.status_code == 200
    except:
        return False

health_checker.register_check('external_api', check_external_api)
```

---

## まとめ

このガイドは、Parasolの哲学を実装レベルで実現するための具体的なパターンとコード例を提供しています。重要なのは：

1. **明示的であること** - 暗黙的な依存や副作用を避ける
2. **観測可能であること** - 何が起きているか常に把握できる
3. **段階的であること** - Big Bangではなく漸進的な変更
4. **回復可能であること** - 失敗を前提とした設計

これらの原則に従うことで、長期的に保守・変更しやすいシステムを構築できます。