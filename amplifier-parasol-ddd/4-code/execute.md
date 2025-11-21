# /ddd:4-code - 実装コード生成

## 概要

このフェーズでは、パラソルV4のPhase 5（実装）として、設計から実際のコードを生成します。

## 実行コマンド

```bash
/ddd:4-code
```

## 実行コンテキスト

### 前提条件
- `/ddd:3-code-plan`が完了していること
- ドメインモデルが定義されていること
- 技術スタックが決定されていること

### 入力
- ドメインモデル（3-code-plan/outputs/）
- L4ユースケース
- UIコンポーネント設計
- データベース設計

### 出力
- バックエンドコード（NestJS）
- フロントエンドコード（Next.js）
- テストコード
- Docker構成

---

## Task 1: ドメインモデル実装

### エンティティ実装

```typescript
// src/domain/personalization/entities/user.entity.ts
export class UserId {
  constructor(private readonly value: string) {
    if (!value) {
      throw new Error('UserId cannot be empty');
    }
  }

  toString(): string {
    return this.value;
  }

  equals(other: UserId): boolean {
    return this.value === other.value;
  }
}

export class Email {
  private readonly value: string;

  constructor(value: string) {
    if (!this.isValid(value)) {
      throw new Error('Invalid email format');
    }
    this.value = value;
  }

  private isValid(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  toString(): string {
    return this.value;
  }
}

export class User {
  private constructor(
    private readonly userId: UserId,
    private email: Email,
    private profile: Profile,
    private preferences: Preference[],
    private readonly createdAt: Date,
    private updatedAt: Date,
    private deletedAt?: Date
  ) {}

  static create(email: string): User {
    return new User(
      new UserId(crypto.randomUUID()),
      new Email(email),
      Profile.createDefault(),
      [],
      new Date(),
      new Date()
    );
  }

  updateProfile(profile: Profile): void {
    this.profile = profile;
    this.updatedAt = new Date();
    this.emit(new ProfileUpdatedEvent(this.userId, profile));
  }

  delete(): void {
    if (this.deletedAt) {
      throw new Error('User already deleted');
    }
    this.deletedAt = new Date();
    this.emit(new UserDeletedEvent(this.userId));
  }

  // Domain Events
  private events: DomainEvent[] = [];

  private emit(event: DomainEvent): void {
    this.events.push(event);
  }

  getUncommittedEvents(): DomainEvent[] {
    return this.events;
  }

  markEventsAsCommitted(): void {
    this.events = [];
  }
}
```

## Task 2: アプリケーションサービス実装

```typescript
// src/application/services/user-profile.service.ts
import { Injectable } from '@nestjs/common';
import { CommandBus, QueryBus } from '@nestjs/cqrs';

@Injectable()
export class UserProfileService {
  constructor(
    private readonly commandBus: CommandBus,
    private readonly queryBus: QueryBus
  ) {}

  async createProfile(dto: CreateProfileDto): Promise<ProfileDto> {
    const command = new CreateProfileCommand(
      dto.email,
      dto.firstName,
      dto.lastName,
      dto.birthDate
    );

    const userId = await this.commandBus.execute(command);

    return this.queryBus.execute(new GetProfileQuery(userId));
  }

  async updateProfile(userId: string, dto: UpdateProfileDto): Promise<ProfileDto> {
    const command = new UpdateProfileCommand(
      userId,
      dto.firstName,
      dto.lastName,
      dto.attributes
    );

    await this.commandBus.execute(command);

    return this.queryBus.execute(new GetProfileQuery(userId));
  }

  async deleteProfile(userId: string): Promise<void> {
    await this.commandBus.execute(new DeleteProfileCommand(userId));
  }
}
```

## Task 3: APIコントローラー実装

```typescript
// src/infrastructure/controllers/profile.controller.ts
import { Controller, Get, Post, Put, Delete, Body, Param, HttpCode, HttpStatus } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { UserProfileService } from '@/application/services/user-profile.service';

@ApiTags('profiles')
@Controller('api/v1/personalization/profiles')
export class ProfileController {
  constructor(private readonly profileService: UserProfileService) {}

  @Post()
  @ApiOperation({ summary: 'Create user profile' })
  @ApiResponse({ status: 201, description: 'Profile created successfully' })
  async createProfile(@Body() dto: CreateProfileDto): Promise<ProfileDto> {
    return await this.profileService.createProfile(dto);
  }

  @Get(':userId')
  @ApiOperation({ summary: 'Get user profile' })
  @ApiResponse({ status: 200, description: 'Profile retrieved successfully' })
  async getProfile(@Param('userId') userId: string): Promise<ProfileDto> {
    return await this.profileService.getProfile(userId);
  }

  @Put(':userId')
  @ApiOperation({ summary: 'Update user profile' })
  @ApiResponse({ status: 200, description: 'Profile updated successfully' })
  async updateProfile(
    @Param('userId') userId: string,
    @Body() dto: UpdateProfileDto
  ): Promise<ProfileDto> {
    return await this.profileService.updateProfile(userId, dto);
  }

  @Delete(':userId')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Delete user profile' })
  @ApiResponse({ status: 204, description: 'Profile deleted successfully' })
  async deleteProfile(@Param('userId') userId: string): Promise<void> {
    await this.profileService.deleteProfile(userId);
  }
}
```

## Task 4: フロントエンド実装

```tsx
// app/components/profile/ProfileForm.tsx
'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const profileSchema = z.object({
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),
  email: z.string().email('Invalid email address'),
  birthDate: z.string().refine((date) => {
    const age = new Date().getFullYear() - new Date(date).getFullYear();
    return age >= 18;
  }, 'Must be at least 18 years old'),
});

type ProfileFormData = z.infer<typeof profileSchema>;

export function ProfileForm({
  user,
  onSubmit,
  onCancel
}: {
  user?: User;
  onSubmit: (data: ProfileFormData) => Promise<void>;
  onCancel: () => void;
}) {
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: user || {},
  });

  const onFormSubmit = async (data: ProfileFormData) => {
    setIsLoading(true);
    try {
      await onSubmit(data);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="firstName" className="block text-sm font-medium">
            First Name
          </label>
          <input
            {...register('firstName')}
            type="text"
            className="mt-1 block w-full rounded-md border-gray-300"
            disabled={isLoading}
          />
          {errors.firstName && (
            <p className="mt-1 text-sm text-red-600">{errors.firstName.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="lastName" className="block text-sm font-medium">
            Last Name
          </label>
          <input
            {...register('lastName')}
            type="text"
            className="mt-1 block w-full rounded-md border-gray-300"
            disabled={isLoading}
          />
          {errors.lastName && (
            <p className="mt-1 text-sm text-red-600">{errors.lastName.message}</p>
          )}
        </div>
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          {...register('email')}
          type="email"
          className="mt-1 block w-full rounded-md border-gray-300"
          disabled={isLoading}
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <div className="flex justify-end space-x-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          disabled={isLoading}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : 'Save Profile'}
        </button>
      </div>
    </form>
  );
}
```

## Task 5: テストコード実装

```typescript
// src/domain/personalization/entities/__tests__/user.spec.ts
import { User, UserId, Email } from '../user.entity';

describe('User Entity', () => {
  describe('User creation', () => {
    it('should create a user with valid email', () => {
      const user = User.create('test@example.com');

      expect(user).toBeDefined();
      expect(user.getEmail().toString()).toBe('test@example.com');
    });

    it('should throw error for invalid email', () => {
      expect(() => User.create('invalid-email')).toThrow('Invalid email format');
    });
  });

  describe('Profile update', () => {
    it('should update profile and emit event', () => {
      const user = User.create('test@example.com');
      const newProfile = Profile.create('John', 'Doe');

      user.updateProfile(newProfile);

      const events = user.getUncommittedEvents();
      expect(events).toHaveLength(1);
      expect(events[0]).toBeInstanceOf(ProfileUpdatedEvent);
    });
  });

  describe('User deletion', () => {
    it('should mark user as deleted', () => {
      const user = User.create('test@example.com');

      user.delete();

      expect(user.isDeleted()).toBe(true);
    });

    it('should not allow deleting already deleted user', () => {
      const user = User.create('test@example.com');
      user.delete();

      expect(() => user.delete()).toThrow('User already deleted');
    });
  });
});
```

## Task 6: Docker構成

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: personalization
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres:5432/personalization
      REDIS_URL: redis://redis:6379
    ports:
      - "3000:3000"
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      NEXT_PUBLIC_API_URL: http://backend:3000
    ports:
      - "3001:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## 検証チェックリスト

- [ ] ドメインモデルが正しく実装されているか
- [ ] APIエンドポイントが仕様通りか
- [ ] フロントエンドコンポーネントが動作するか
- [ ] テストが網羅的でパスするか
- [ ] Docker環境で正常に動作するか

---

## 次のステップ

実装が完了したので、プラットフォーム設定とデプロイに進みます：

```bash
/ddd:5-finish 5-finish/execute.md
```

---

## 成果物の保存先

```
amplifier-parasol-ddd/
└── 4-code/
    └── outputs/
        ├── backend/
        │   ├── src/
        │   ├── package.json
        │   └── Dockerfile
        ├── frontend/
        │   ├── app/
        │   ├── package.json
        │   └── Dockerfile
        ├── tests/
        └── docker-compose.yml
```

---

*このドキュメントはAmplifierのDDDワークフローで直接実行できます*