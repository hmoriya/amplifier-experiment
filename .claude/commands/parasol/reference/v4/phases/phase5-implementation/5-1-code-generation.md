# Phase 5-1: コード自動生成

## 実行コンテキスト

このドキュメントは、定義されたドメインモデルとオペレーションから実装コードを自動生成するための実行可能なMarkdownです。

### 前提条件
- Phase 4のオペレーション設計が完了していること
- API仕様が定義されていること
- 技術スタックが決定していること

### 実行方法
```bash
/ddd:1-plan parasol/phases/phase5-implementation/5-1-code-generation.md
```

---

## 入力：オペレーション設計からの要求

### 技術スタック
```yaml
バックエンド:
  言語: Python 3.11+
  フレームワーク: FastAPI
  ORM: SQLAlchemy
  データベース: PostgreSQL

フロントエンド:
  フレームワーク: Next.js 14
  言語: TypeScript
  状態管理: Zustand
  UIライブラリ: shadcn/ui

インフラ:
  コンテナ: Docker
  オーケストレーション: Kubernetes
  CI/CD: GitHub Actions
  クラウド: AWS
```

---

## タスク：実装コードの生成

### 実行ステップ

#### Step 1: ドメインモデルの生成

##### Pythonエンティティクラス
```python
# domain/sustainability/carbon_footprint.py
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

class CertificationStatus(Enum):
    PENDING = "pending"
    CERTIFIED = "certified"
    EXPIRED = "expired"

@dataclass
class CO2Amount:
    value: Decimal
    unit: str = "tCO2e"

    def __add__(self, other: 'CO2Amount') -> 'CO2Amount':
        return CO2Amount(self.value + other.value, self.unit)

class CarbonFootprint:
    def __init__(
        self,
        product_id: str,
        scope1_emission: CO2Amount,
        scope2_emission: CO2Amount,
        scope3_emission: CO2Amount,
        measurement_date: date,
        footprint_id: Optional[UUID] = None
    ):
        self.footprint_id = footprint_id or uuid4()
        self.product_id = product_id
        self.scope1_emission = scope1_emission
        self.scope2_emission = scope2_emission
        self.scope3_emission = scope3_emission
        self.measurement_date = measurement_date
        self.certification_status = CertificationStatus.PENDING
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def total_emission(self) -> CO2Amount:
        return self.scope1_emission + self.scope2_emission + self.scope3_emission

    def certify(self, certified_by: str, expiry_date: date):
        self.certification_status = CertificationStatus.CERTIFIED
        self.certified_by = certified_by
        self.certification_expiry = expiry_date
        self.updated_at = datetime.utcnow()
```

##### SQLAlchemyモデル
```python
# infrastructure/models/carbon_footprint_model.py
from sqlalchemy import Column, String, Numeric, Date, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class CarbonFootprintModel(Base):
    __tablename__ = "carbon_footprints"

    footprint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(String, nullable=False, index=True)
    scope1_emission = Column(Numeric(10, 3), nullable=False)
    scope2_emission = Column(Numeric(10, 3), nullable=False)
    scope3_emission = Column(Numeric(10, 3), nullable=False)
    total_emission = Column(Numeric(10, 3), nullable=False)
    measurement_date = Column(Date, nullable=False)
    certification_status = Column(Enum(CertificationStatus), nullable=False)
    certified_by = Column(String)
    certification_expiry = Column(Date)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
```

#### Step 2: APIエンドポイントの生成

##### FastAPIルーター
```python
# api/v1/carbon_footprint_router.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import date
from uuid import UUID

router = APIRouter(prefix="/api/v1/carbon-footprints", tags=["carbon-footprint"])

@router.post("/", response_model=CarbonFootprintResponse)
async def create_carbon_footprint(
    command: CreateCarbonFootprintCommand,
    service: CarbonFootprintService = Depends(get_service)
):
    """CO2排出量を記録"""
    try:
        result = await service.create_footprint(command)
        return CarbonFootprintResponse(
            status="success",
            data=result,
            metadata={"timestamp": datetime.utcnow()}
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{footprint_id}", response_model=CarbonFootprintResponse)
async def get_carbon_footprint(
    footprint_id: UUID,
    service: CarbonFootprintService = Depends(get_service)
):
    """CO2排出量を取得"""
    footprint = await service.get_footprint(footprint_id)
    if not footprint:
        raise HTTPException(status_code=404, detail="Footprint not found")
    return CarbonFootprintResponse(
        status="success",
        data=footprint
    )

@router.get("/", response_model=List[CarbonFootprintResponse])
async def list_carbon_footprints(
    product_id: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    service: CarbonFootprintService = Depends(get_service)
):
    """CO2排出量一覧を取得"""
    footprints = await service.list_footprints(
        product_id=product_id,
        date_range=(date_from, date_to)
    )
    return footprints
```

##### DTOとバリデーション
```python
# api/v1/dto/carbon_footprint_dto.py
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

class CreateCarbonFootprintCommand(BaseModel):
    product_id: str = Field(..., min_length=1)
    scope1_emission: Decimal = Field(..., ge=0)
    scope2_emission: Decimal = Field(..., ge=0)
    scope3_emission: Decimal = Field(..., ge=0)
    measurement_date: date
    measurement_method: str

    @validator('scope1_emission', 'scope2_emission', 'scope3_emission')
    def validate_emission(cls, v):
        if v > 10000:
            raise ValueError('Emission value seems too high')
        return v

class CarbonFootprintDTO(BaseModel):
    footprint_id: UUID
    product_id: str
    total_emission: Decimal
    trend: str
    certification_status: dict
    last_updated: datetime

class CarbonFootprintResponse(BaseModel):
    status: str
    data: CarbonFootprintDTO
    metadata: dict
```

#### Step 3: ビジネスロジックサービス

```python
# application/services/carbon_footprint_service.py
from typing import List, Optional, Tuple
from datetime import date
from uuid import UUID

class CarbonFootprintService:
    def __init__(
        self,
        repository: CarbonFootprintRepository,
        event_bus: EventBus
    ):
        self.repository = repository
        self.event_bus = event_bus

    async def create_footprint(
        self,
        command: CreateCarbonFootprintCommand
    ) -> CarbonFootprintDTO:
        # 製品の存在確認
        if not await self._validate_product(command.product_id):
            raise ValidationError(f"Product {command.product_id} not found")

        # 重複チェック
        existing = await self.repository.find_by_product_and_date(
            command.product_id,
            command.measurement_date
        )
        if existing:
            raise DuplicateMeasurementError()

        # エンティティ作成
        footprint = CarbonFootprint(
            product_id=command.product_id,
            scope1_emission=CO2Amount(command.scope1_emission),
            scope2_emission=CO2Amount(command.scope2_emission),
            scope3_emission=CO2Amount(command.scope3_emission),
            measurement_date=command.measurement_date
        )

        # 保存
        await self.repository.save(footprint)

        # イベント発行
        await self.event_bus.publish(
            CarbonFootprintRecorded(
                footprint_id=footprint.footprint_id,
                product_id=footprint.product_id,
                total_emission=footprint.total_emission.value
            )
        )

        return self._to_dto(footprint)
```

#### Step 4: フロントエンドコンポーネント

##### React/TypeScriptコンポーネント
```typescript
// components/carbon-footprint/CarbonFootprintForm.tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const footprintSchema = z.object({
  productId: z.string().min(1),
  scope1Emission: z.number().min(0),
  scope2Emission: z.number().min(0),
  scope3Emission: z.number().min(0),
  measurementDate: z.date(),
  measurementMethod: z.string()
});

type FootprintFormData = z.infer<typeof footprintSchema>;

export const CarbonFootprintForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<FootprintFormData>({
    resolver: zodResolver(footprintSchema)
  });

  const onSubmit = async (data: FootprintFormData) => {
    try {
      const response = await fetch('/api/v1/carbon-footprints', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (!response.ok) throw new Error('Failed to create footprint');

      const result = await response.json();
      console.log('Created:', result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="productId">製品ID</label>
        <input {...register('productId')} className="input" />
        {errors.productId && <span className="error">{errors.productId.message}</span>}
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <label>Scope 1 排出量</label>
          <input {...register('scope1Emission', { valueAsNumber: true })} type="number" />
        </div>
        <div>
          <label>Scope 2 排出量</label>
          <input {...register('scope2Emission', { valueAsNumber: true })} type="number" />
        </div>
        <div>
          <label>Scope 3 排出量</label>
          <input {...register('scope3Emission', { valueAsNumber: true })} type="number" />
        </div>
      </div>

      <button type="submit" className="btn btn-primary">記録</button>
    </form>
  );
};
```

#### Step 5: テストコード生成

```python
# tests/test_carbon_footprint_service.py
import pytest
from datetime import date
from decimal import Decimal

@pytest.mark.asyncio
async def test_create_carbon_footprint():
    # Arrange
    service = CarbonFootprintService(
        repository=MockRepository(),
        event_bus=MockEventBus()
    )
    command = CreateCarbonFootprintCommand(
        product_id="PROD001",
        scope1_emission=Decimal("10.5"),
        scope2_emission=Decimal("20.3"),
        scope3_emission=Decimal("15.2"),
        measurement_date=date(2024, 1, 1),
        measurement_method="LCA"
    )

    # Act
    result = await service.create_footprint(command)

    # Assert
    assert result.product_id == "PROD001"
    assert result.total_emission == Decimal("46.0")
    assert result.footprint_id is not None
```

---

## 出力：生成コード成果物

### 生成する成果物
1. バックエンドコード（Python/FastAPI）
2. フロントエンドコード（TypeScript/Next.js）
3. データベーススキーマ（SQL）
4. APIドキュメント（OpenAPI）
5. テストコード（pytest/Jest）

### 保存先
```
projects/asahi-parasol-development/
└── phase5-implementation/
    ├── backend/
    ├── frontend/
    ├── database/
    ├── api-docs/
    └── tests/
```

---

## 検証項目

- [ ] 生成コードがコンパイル可能か
- [ ] テストが実行可能か
- [ ] APIが仕様通りか
- [ ] セキュリティ要件を満たすか
- [ ] パフォーマンス要件を満たすか

---

## 次のステップ

このコード生成が完了したら：

```bash
# デプロイメント設定へ進む
/ddd:1-plan parasol/phases/phase5-implementation/5-2-deployment.md
```

---

## 参考情報

- [オペレーション設計書](../phase4-operation/)
- [技術スタック選定書](../../projects/asahi-parasol-development/)
- [コーディング規約](../../standards/coding-standards.md)

---

*このドキュメントは実行可能なMDとして、AmplifierのDDDワークフローで処理できます。*