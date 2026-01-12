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

## V5.5対応: トレーサビリティベースのテスト設計

### テスト導出の原則

V5.5では、**BO → activity_flow → Actor UseCase → api_operations/db_operations** の完全なトレーサビリティチェーンからテストを自動導出します。

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  テスト導出フロー                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BO (operation_pattern) ──────────────────┐                                │
│       │                                    │                                │
│       │ activity_flow                      │ テスト戦略決定                 │
│       ▼                                    ▼                                │
│  ┌─────────────────┐               ┌─────────────────┐                     │
│  │ Actor UseCase   │               │ パターン別       │                     │
│  │ (usecase_ref)   │               │ テスト戦略      │                     │
│  └────────┬────────┘               └─────────────────┘                     │
│           │                                                                 │
│     ┌─────┴─────┐                                                          │
│     ▼           ▼                                                          │
│  api_operations   db_operations                                            │
│     │               │                                                      │
│     ▼               ▼                                                      │
│  Contract Test   Transaction Test                                          │
│  Integration Test  Repository Test                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### operation_pattern別テスト戦略

| パターン | 単体テスト重点 | 統合テスト重点 | E2Eテスト重点 |
|----------|---------------|---------------|---------------|
| **CRUD** | バリデーション | API契約 | フォーム操作 |
| **Workflow** | 状態遷移ロジック | イベント発行 | 業務フロー完走 |
| **Batch** | チャンク処理 | 再開可能性 | 大量データ処理 |
| **Analytics** | 集計ロジック | クエリ性能 | ダッシュボード表示 |
| **Communication** | メッセージ形式 | 配信確認 | 通知受信 |
| **Administration** | 権限チェック | 監査ログ | 管理操作 |

#### CRUDパターン テスト設計テンプレート

**TypeScript (Jest/Vitest)**
```typescript
// operation_pattern: CRUD の場合
// Actor UseCase: 研究員が酵母株を登録する

describe('CRUDPattern - RegisterStrain', () => {
  // 1. バリデーションテスト（単体）
  it('必須フィールドのバリデーション', () => {
    const result = validateStrain({ name: '' });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('name is required');
  });

  it('形式バリデーション（メール、日付等）', () => {
    const result = validateStrain({ registrationDate: 'invalid' });
    expect(result.errors).toContain('invalid date format');
  });

  // 2. API契約テスト（統合）
  it('作成成功時に201を返す', async () => {
    const response = await request(app).post('/api/v1/strains').send(validStrain);
    expect(response.status).toBe(201);
  });

  it('不正入力時に400を返す', async () => {
    const response = await request(app).post('/api/v1/strains').send({});
    expect(response.status).toBe(400);
  });

  // 3. DB操作テスト（統合）
  it('INSERTでレコードが作成される', async () => {
    await strainRepository.save(strain);
    const found = await strainRepository.findById(strain.id);
    expect(found).not.toBeNull();
  });

  it('エラー時にトランザクションがロールバックされる', async () => {
    await expect(strainRepository.saveWithError(strain)).rejects.toThrow();
    const found = await strainRepository.findById(strain.id);
    expect(found).toBeNull();
  });
});
```

**C# (.NET xUnit)**
```csharp
// operation_pattern: CRUD の場合
public class CrudPatternTests
{
    // 1. バリデーションテスト（単体）
    [Fact]
    public void RequiredFieldsValidation()
    {
        var strain = new Strain { Name = "" };
        var result = _validator.Validate(strain);
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.PropertyName == "Name");
    }

    // 2. API契約テスト（統合）
    [Fact]
    public async Task CreateReturns201OnSuccess()
    {
        var response = await _client.PostAsJsonAsync("/api/v1/strains", validStrain);
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }

    // 3. DB操作テスト（統合）
    [Fact]
    public async Task InsertCreatesRecord()
    {
        await _repository.SaveAsync(strain);
        var found = await _repository.FindByIdAsync(strain.Id);
        Assert.NotNull(found);
    }

    [Fact]
    public async Task TransactionRollbackOnError()
    {
        await Assert.ThrowsAsync<DbUpdateException>(
            () => _repository.SaveWithErrorAsync(strain));
        var found = await _repository.FindByIdAsync(strain.Id);
        Assert.Null(found);
    }
}
```

**Java (JUnit 5)**
```java
// operation_pattern: CRUD の場合
@SpringBootTest
class CrudPatternTest {
    // 1. バリデーションテスト（単体）
    @Test
    void requiredFieldsValidation() {
        var strain = new Strain();
        strain.setName("");
        var violations = validator.validate(strain);
        assertFalse(violations.isEmpty());
    }

    // 2. API契約テスト（統合）
    @Test
    void createReturns201OnSuccess() throws Exception {
        mockMvc.perform(post("/api/v1/strains")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(validStrain)))
            .andExpect(status().isCreated());
    }

    // 3. DB操作テスト（統合）
    @Test
    @Transactional
    void insertCreatesRecord() {
        repository.save(strain);
        var found = repository.findById(strain.getId());
        assertTrue(found.isPresent());
    }

    @Test
    void transactionRollbackOnError() {
        assertThrows(DataIntegrityViolationException.class,
            () -> repository.saveWithError(strain));
        var found = repository.findById(strain.getId());
        assertTrue(found.isEmpty());
    }
}
```

#### Workflowパターン テスト設計テンプレート

**TypeScript (Jest/Vitest)**
```typescript
// operation_pattern: Workflow の場合
// BO: 酵母株スクリーニング（activity_flow定義あり）

describe('WorkflowPattern - YeastStrainScreening', () => {
  // 1. 状態遷移テスト（単体）
  it('有効な状態遷移が成功する', () => {
    const workflow = new ScreeningWorkflow('REGISTERED');
    workflow.transition('EVALUATE');
    expect(workflow.state).toBe('EVALUATING');
  });

  it('無効な状態遷移が拒否される', () => {
    const workflow = new ScreeningWorkflow('REGISTERED');
    expect(() => workflow.transition('COMPLETE')).toThrow(InvalidTransitionError);
  });

  // 2. activity_flow遷移テスト（統合）
  it('activity_flowの順序通りに実行される', async () => {
    // activity_flow.sequenceから自動生成
    await executeActivity('researcher.register_strain');
    await executeActivity('qa_manager.evaluate_strain');
    expect(workflowState).toBe('EVALUATED');
  });

  // 3. ドメインイベントテスト（統合）
  it('完了時にドメインイベントが発行される', async () => {
    const events: DomainEvent[] = [];
    eventBus.subscribe('ScreeningCompleted', e => events.push(e));
    await workflow.complete();
    expect(events).toHaveLength(1);
  });

  // 4. E2Eフローテスト
  it('ワークフロー全体が正常完了する', async () => {
    // BOのactivity_flow全体をテスト
    const result = await executeFullWorkflow(screeningWorkflowId);
    expect(result.status).toBe('COMPLETED');
  });
});
```

**C# (.NET xUnit)**
```csharp
// operation_pattern: Workflow の場合
public class WorkflowPatternTests
{
    [Fact]
    public void ValidStateTransitionSucceeds()
    {
        var workflow = new ScreeningWorkflow(WorkflowState.Registered);
        workflow.Transition(WorkflowAction.Evaluate);
        Assert.Equal(WorkflowState.Evaluating, workflow.State);
    }

    [Fact]
    public void InvalidStateTransitionIsRejected()
    {
        var workflow = new ScreeningWorkflow(WorkflowState.Registered);
        Assert.Throws<InvalidTransitionException>(
            () => workflow.Transition(WorkflowAction.Complete));
    }

    [Fact]
    public async Task DomainEventPublishedOnCompletion()
    {
        var events = new List<IDomainEvent>();
        _eventBus.Subscribe<ScreeningCompletedEvent>(e => events.Add(e));
        await _workflow.CompleteAsync();
        Assert.Single(events);
    }
}
```

#### Batchパターン テスト設計テンプレート

**TypeScript (Jest/Vitest)**
```typescript
// operation_pattern: Batch の場合
describe('BatchPattern', () => {
  // 1. チャンク処理テスト（単体）
  it('チャンクサイズが守られる', async () => {
    const processor = new BatchProcessor({ chunkSize: 100 });
    const chunks = await processor.process(items);
    chunks.forEach(chunk => expect(chunk.length).toBeLessThanOrEqual(100));
  });

  it('部分失敗時の処理', async () => {
    const result = await processor.processWithPartialFailure(items);
    expect(result.succeeded).toBeGreaterThan(0);
    expect(result.failed).toBeGreaterThan(0);
    expect(result.failedItems).toBeDefined();
  });

  // 2. 再開可能性テスト（統合）
  it('チェックポイントから再開可能', async () => {
    const checkpoint = await processor.getCheckpoint(jobId);
    const result = await processor.resumeFrom(checkpoint);
    expect(result.processedCount).toBe(totalItems - checkpoint.processedCount);
  });
});
```

**C# (.NET xUnit)**
```csharp
// operation_pattern: Batch の場合
public class BatchPatternTests
{
    [Fact]
    public async Task ChunkSizeRespected()
    {
        var processor = new BatchProcessor(chunkSize: 100);
        var chunks = await processor.ProcessAsync(items);
        Assert.All(chunks, chunk => Assert.True(chunk.Count <= 100));
    }

    [Fact]
    public async Task ResumeFromCheckpoint()
    {
        var checkpoint = await _processor.GetCheckpointAsync(jobId);
        var result = await _processor.ResumeFromAsync(checkpoint);
        Assert.Equal(totalItems - checkpoint.ProcessedCount, result.ProcessedCount);
    }
}
```

#### Analyticsパターン テスト設計テンプレート

**TypeScript (Jest/Vitest)**
```typescript
// operation_pattern: Analytics の場合
describe('AnalyticsPattern', () => {
  // 1. 集計ロジックテスト（単体）
  it('集計ロジックの正確性', () => {
    const result = aggregateStrainData(testData);
    expect(result.totalCount).toBe(100);
    expect(result.averageYield).toBeCloseTo(85.5, 2);
  });

  // 2. クエリ性能テスト（統合）
  it('負荷時のクエリ性能', async () => {
    const start = performance.now();
    await analyticsService.generateReport(largeDataset);
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(3000); // 3秒以内
  });

  // 3. 読み取り専用確認
  it('データが変更されないこと', async () => {
    const before = await getRecordCount();
    await analyticsService.generateReport(dataset);
    const after = await getRecordCount();
    expect(after).toBe(before);
  });
});
```

**C# (.NET xUnit)**
```csharp
// operation_pattern: Analytics の場合
public class AnalyticsPatternTests
{
    [Fact]
    public void AggregationLogicAccuracy()
    {
        var result = _aggregator.Aggregate(testData);
        Assert.Equal(100, result.TotalCount);
        Assert.Equal(85.5m, result.AverageYield, 2);
    }

    [Fact]
    public async Task NoDataModification()
    {
        var before = await _repository.CountAsync();
        await _analyticsService.GenerateReportAsync(dataset);
        var after = await _repository.CountAsync();
        Assert.Equal(before, after);
    }
}
```

### activity_flowからの統合テスト導出

```yaml
# BO定義からの自動テスト生成
operation:
  name: "酵母株スクリーニング"
  operation_pattern: Workflow
  activity_flow:
    sequence:
      - activity: "酵母株を登録"
        usecase_ref: "researcher.register_strain"
        next: "株を評価"
      - activity: "株を評価"
        usecase_ref: "qa_manager.evaluate_strain"
        next: "レポート出力 | 再評価依頼"
        condition: "評価完了時 | 不合格時"
```

↓ 自動生成されるテストケース

**TypeScript (Jest/Vitest)**
```typescript
describe('YeastStrainScreeningFlow', () => {
  // activity_flowから導出された統合テスト

  it('登録→評価への遷移', async () => {
    // usecase_ref: researcher.register_strain 実行
    const strain = await executeUseCase('researcher.register_strain', strainData);
    // 次のusecase_ref: qa_manager.evaluate_strain へ遷移確認
    const evaluation = await executeUseCase('qa_manager.evaluate_strain', { strainId: strain.id });
    expect(evaluation.status).toBe('EVALUATED');
  });

  it('評価合格→レポート出力への分岐', async () => {
    // condition: "評価完了時"
    const evaluation = await completeEvaluation(strainId, { result: 'PASS' });
    expect(evaluation.nextActivity).toBe('admin.export_report');
  });

  it('評価不合格→再評価依頼への分岐', async () => {
    // condition: "不合格時"
    const evaluation = await completeEvaluation(strainId, { result: 'FAIL' });
    expect(evaluation.nextActivity).toBe('qa_manager.request_reevaluation');
  });

  it('正常系の完全フロー', async () => {
    // activity_flow.sequence全体の実行
    const result = await executeFullWorkflow('yeast_strain_screening', initialData);
    expect(result.status).toBe('COMPLETED');
    expect(result.activities).toHaveLength(4);
  });
});
```

**C# (.NET xUnit)**
```csharp
public class YeastStrainScreeningFlowTests
{
    [Fact]
    public async Task FlowStep1_RegisterToEvaluate()
    {
        var strain = await ExecuteUseCaseAsync("researcher.register_strain", strainData);
        var evaluation = await ExecuteUseCaseAsync("qa_manager.evaluate_strain",
            new { StrainId = strain.Id });
        Assert.Equal("EVALUATED", evaluation.Status);
    }

    [Fact]
    public async Task FlowBranch_PassToReport()
    {
        var evaluation = await CompleteEvaluationAsync(strainId, EvaluationResult.Pass);
        Assert.Equal("admin.export_report", evaluation.NextActivity);
    }

    [Fact]
    public async Task CompleteHappyPath()
    {
        var result = await ExecuteFullWorkflowAsync("yeast_strain_screening", initialData);
        Assert.Equal("COMPLETED", result.Status);
        Assert.Equal(4, result.Activities.Count);
    }
}
```

### api_operations/db_operationsからのテスト導出

```yaml
# Actor UseCase定義
actor_usecase:
  id: "researcher.register_strain"

  api_operations:
    - method: POST
      endpoint: /api/v1/strains
      operationId: createStrain
      request_schema: CreateStrainRequest
      response_schema: Strain

  db_operations:
    type: CRUD
    tables:
      - yeast_strains (INSERT)
      - strain_origins (INSERT)
    transaction: REQUIRED
```

↓ 自動生成されるテストケース

**TypeScript (Jest/Vitest)**
```typescript
// api_operationsから導出
describe('RegisterStrainAPI', () => {
  it('POST /api/v1/strains が成功する', async () => {
    const response = await request(app)
      .post('/api/v1/strains')
      .send(validRequest);
    expect(response.status).toBe(201);
    expect(response.body).toMatchSchema(StrainSchema);
  });

  it('CreateStrainRequestスキーマでバリデーション', async () => {
    const response = await request(app)
      .post('/api/v1/strains')
      .send({ invalid: 'data' });
    expect(response.status).toBe(400);
    expect(response.body.errors).toBeDefined();
  });
});

// db_operationsから導出
describe('RegisterStrainDB', () => {
  it('yeast_strainsテーブルにINSERT', async () => {
    await strainRepository.save(strain);
    const result = await db.query('SELECT * FROM yeast_strains WHERE id = $1', [strain.id]);
    expect(result.rows).toHaveLength(1);
  });

  it('strain_originsテーブルにINSERT', async () => {
    await strainRepository.save(strainWithOrigin);
    const result = await db.query('SELECT * FROM strain_origins WHERE strain_id = $1', [strain.id]);
    expect(result.rows).toHaveLength(1);
  });

  it('トランザクションの原子性（全INSERT or 全ロールバック）', async () => {
    await expect(strainRepository.saveWithError(strain)).rejects.toThrow();
    const strains = await db.query('SELECT * FROM yeast_strains WHERE id = $1', [strain.id]);
    const origins = await db.query('SELECT * FROM strain_origins WHERE strain_id = $1', [strain.id]);
    expect(strains.rows).toHaveLength(0);
    expect(origins.rows).toHaveLength(0);
  });
});
```

**C# (.NET xUnit)**
```csharp
// api_operationsから導出
public class RegisterStrainApiTests
{
    [Fact]
    public async Task PostStrains_ReturnsCreated()
    {
        var response = await _client.PostAsJsonAsync("/api/v1/strains", validRequest);
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        var strain = await response.Content.ReadFromJsonAsync<Strain>();
        Assert.NotNull(strain);
    }

    [Fact]
    public async Task PostStrains_ValidatesRequest()
    {
        var response = await _client.PostAsJsonAsync("/api/v1/strains", new { Invalid = "data" });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
}

// db_operationsから導出
public class RegisterStrainDbTests
{
    [Fact]
    public async Task InsertsToYeastStrains()
    {
        await _repository.SaveAsync(strain);
        var result = await _context.YeastStrains.FindAsync(strain.Id);
        Assert.NotNull(result);
    }

    [Fact]
    public async Task TransactionAtomicity()
    {
        await Assert.ThrowsAsync<DbUpdateException>(
            () => _repository.SaveWithErrorAsync(strain));
        var strains = await _context.YeastStrains.FindAsync(strain.Id);
        var origins = await _context.StrainOrigins
            .Where(o => o.StrainId == strain.Id).ToListAsync();
        Assert.Null(strains);
        Assert.Empty(origins);
    }
}
```

**Java (JUnit 5)**
```java
// api_operationsから導出
@SpringBootTest
@AutoConfigureMockMvc
class RegisterStrainApiTest {
    @Test
    void postStrains_returnsCreated() throws Exception {
        mockMvc.perform(post("/api/v1/strains")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(validRequest)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists());
    }
}

// db_operationsから導出
@DataJpaTest
class RegisterStrainDbTest {
    @Test
    void insertsToYeastStrains() {
        repository.save(strain);
        var found = entityManager.find(YeastStrain.class, strain.getId());
        assertNotNull(found);
    }

    @Test
    void transactionAtomicity() {
        assertThrows(DataIntegrityViolationException.class,
            () -> repository.saveWithError(strain));
        var strains = entityManager.find(YeastStrain.class, strain.getId());
        assertNull(strains);
    }
}
```

---

## 入力：テスト要件

### テスト範囲
1. **単体テスト**: 個別コンポーネント
2. **統合テスト**: API・データベース連携
3. **E2Eテスト**: ユーザーシナリオ（activity_flowベース）
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