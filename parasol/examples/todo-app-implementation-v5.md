# TODOアプリ V5実装ガイド

前述のケイパビリティ分解に基づいた、実際の実装コードサンプルです。

## プロジェクト構造

```
todo-app/
├── backend/
│   ├── services/
│   │   ├── task-management/
│   │   │   ├── task.service.ts
│   │   │   ├── task.repository.ts
│   │   │   └── task.types.ts
│   │   ├── category/
│   │   │   └── category.service.ts
│   │   └── dashboard/
│   │       └── dashboard.service.ts
│   ├── api/
│   │   ├── graphql/
│   │   │   └── schema.graphql
│   │   └── rest/
│   │       └── routes.ts
│   └── infrastructure/
│       ├── database/
│       └── notifications/
├── frontend/
│   ├── orchestrators/
│   │   └── task.orchestrator.ts
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── Dashboard.tsx
│   └── state/
│       └── task.store.ts
└── shared/
    └── types/
```

## Backend実装（V5軽量スタイル）

### 1. タスク管理サービス（BC-001, BC-002）

```typescript
// backend/services/task-management/task.types.ts
export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: Priority;
  categoryId?: string;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date;
}

export type TaskStatus = 'todo' | 'in_progress' | 'done' | 'archived';
export type Priority = 'low' | 'medium' | 'high' | 'critical';

// V5: シンプルな通知タイプ（イベントソーシングなし）
export interface TaskNotification {
  type: 'task.created' | 'task.updated' | 'task.completed' | 'task.deleted';
  taskId: string;
  userId: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}
```

```typescript
// backend/services/task-management/task.service.ts
import { Injectable } from '@nestjs/common';
import { TaskRepository } from './task.repository';
import { NotificationService } from '../../infrastructure/notifications';
import { Task, TaskStatus, Priority } from './task.types';

@Injectable()
export class TaskManagementService {
  constructor(
    private repository: TaskRepository,
    private notifier: NotificationService
  ) {}

  // BC-001: タスク作成・編集
  async createTask(input: CreateTaskDto, userId: string): Promise<Task> {
    // シンプルなバリデーション
    if (!input.title || input.title.trim().length === 0) {
      throw new Error('タスクタイトルは必須です');
    }

    const task: Task = {
      id: this.generateId(),
      title: input.title.trim(),
      description: input.description,
      status: 'todo',
      priority: input.priority || 'medium',
      categoryId: input.categoryId,
      createdBy: userId,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    // V5: シンプルなCRUD操作
    await this.repository.save(task);

    // V5: 軽量な通知（非同期、失敗しても継続）
    this.notifyAsync({
      type: 'task.created',
      taskId: task.id,
      userId,
      timestamp: new Date(),
      metadata: { title: task.title, priority: task.priority }
    });

    return task;
  }

  // BC-002: タスク状態管理
  async updateTaskStatus(
    taskId: string, 
    newStatus: TaskStatus,
    userId: string
  ): Promise<Task> {
    const task = await this.repository.findById(taskId);
    if (!task) {
      throw new Error('タスクが見つかりません');
    }

    // 状態遷移のバリデーション
    if (!this.isValidStatusTransition(task.status, newStatus)) {
      throw new Error(`${task.status} から ${newStatus} への変更はできません`);
    }

    // 更新
    task.status = newStatus;
    task.updatedAt = new Date();
    
    if (newStatus === 'done') {
      task.completedAt = new Date();
    }

    await this.repository.update(task);

    // 完了時の通知
    if (newStatus === 'done') {
      this.notifyAsync({
        type: 'task.completed',
        taskId: task.id,
        userId,
        timestamp: new Date()
      });
    }

    return task;
  }

  // クイックタスク追加（BO-001）
  async quickAddTask(title: string, userId: string): Promise<Task> {
    // テンプレートベースの高速作成
    const template = await this.getQuickAddTemplate(userId);
    
    return this.createTask({
      title,
      priority: template.defaultPriority,
      categoryId: template.defaultCategoryId
    }, userId);
  }

  // 完了タスクの自動アーカイブ（BO-004）
  async archiveCompletedTasks(): Promise<number> {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    const tasksToArchive = await this.repository.findCompletedBefore(thirtyDaysAgo);
    
    for (const task of tasksToArchive) {
      task.status = 'archived';
      await this.repository.update(task);
    }

    return tasksToArchive.length;
  }

  // V5: 軽量な非同期通知
  private notifyAsync(notification: TaskNotification): void {
    // 非同期で通知（メイン処理をブロックしない）
    setImmediate(() => {
      this.notifier.send(notification).catch(err => {
        console.warn('通知送信失敗:', err);
        // 失敗してもメイン処理には影響なし
      });
    });
  }

  private isValidStatusTransition(from: TaskStatus, to: TaskStatus): boolean {
    const validTransitions = {
      'todo': ['in_progress', 'done'],
      'in_progress': ['todo', 'done'],
      'done': ['todo', 'archived'],
      'archived': [] // アーカイブからは変更不可
    };

    return validTransitions[from]?.includes(to) ?? false;
  }

  private generateId(): string {
    return `task_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
  }
}
```

### 2. カテゴリ管理サービス（BC-003）

```typescript
// backend/services/category/category.service.ts
import { Injectable } from '@nestjs/common';

interface Category {
  id: string;
  name: string;
  parentId?: string;
  color?: string;
  userId: string;
}

@Injectable()
export class CategoryService {
  // カテゴリ作成（BO-005）
  async createCategory(name: string, parentId: string | null, userId: string): Promise<Category> {
    // V5: シンプルな階層構造
    const category: Category = {
      id: this.generateId(),
      name,
      parentId: parentId || undefined,
      userId
    };

    await this.repository.save(category);
    return category;
  }

  // カテゴリ別フィルタ（BO-006）
  async getTasksByCategory(categoryId: string): Promise<Task[]> {
    // V5: 高速レスポンス重視
    const startTime = Date.now();
    
    const tasks = await this.taskRepository.findByCategoryId(categoryId);
    
    const responseTime = Date.now() - startTime;
    if (responseTime > 100) {
      console.warn(`カテゴリフィルタが遅い: ${responseTime}ms`);
    }
    
    return tasks;
  }

  // 階層カテゴリの取得
  async getCategoryTree(userId: string): Promise<CategoryNode[]> {
    const categories = await this.repository.findByUserId(userId);
    return this.buildTree(categories);
  }

  private buildTree(categories: Category[]): CategoryNode[] {
    const map = new Map<string, CategoryNode>();
    const roots: CategoryNode[] = [];

    // ノード作成
    categories.forEach(cat => {
      map.set(cat.id, { ...cat, children: [] });
    });

    // 親子関係構築
    categories.forEach(cat => {
      const node = map.get(cat.id)!;
      if (cat.parentId && map.has(cat.parentId)) {
        map.get(cat.parentId)!.children.push(node);
      } else {
        roots.push(node);
      }
    });

    return roots;
  }
}
```

### 3. ダッシュボードサービス（BC-005, BC-006）

```typescript
// backend/services/dashboard/dashboard.service.ts
@Injectable()
export class DashboardService {
  // ダッシュボード表示（BC-005）
  async getDashboardData(userId: string): Promise<DashboardData> {
    // V5: 必要なデータを並列取得
    const [tasks, categories, stats] = await Promise.all([
      this.taskRepository.findByUserId(userId),
      this.categoryService.getCategoryTree(userId),
      this.calculateStats(userId)
    ]);

    return {
      summary: {
        total: tasks.length,
        todo: tasks.filter(t => t.status === 'todo').length,
        inProgress: tasks.filter(t => t.status === 'in_progress').length,
        done: tasks.filter(t => t.status === 'done').length
      },
      priorityBreakdown: this.groupByPriority(tasks),
      categoryBreakdown: this.groupByCategory(tasks),
      recentTasks: tasks.slice(0, 10),
      upcomingTasks: this.getUpcomingTasks(tasks)
    };
  }

  // 進捗レポート生成（BC-006）
  async generateWeeklyReport(userId: string): Promise<Report> {
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const tasks = await this.taskRepository.findByUserIdAndDateRange(
      userId, 
      oneWeekAgo, 
      new Date()
    );

    return {
      period: 'weekly',
      summary: {
        created: tasks.filter(t => t.createdAt >= oneWeekAgo).length,
        completed: tasks.filter(t => t.completedAt && t.completedAt >= oneWeekAgo).length,
        completionRate: this.calculateCompletionRate(tasks),
        averageCompletionTime: this.calculateAverageCompletionTime(tasks)
      },
      insights: this.generateInsights(tasks),
      recommendations: this.generateRecommendations(tasks)
    };
  }

  private generateInsights(tasks: Task[]): string[] {
    const insights: string[] = [];

    // 高優先度タスクの完了率
    const highPriorityTasks = tasks.filter(t => t.priority === 'high' || t.priority === 'critical');
    const completedHighPriority = highPriorityTasks.filter(t => t.status === 'done');
    
    if (highPriorityTasks.length > 0) {
      const rate = (completedHighPriority.length / highPriorityTasks.length) * 100;
      insights.push(`高優先度タスクの完了率: ${rate.toFixed(1)}%`);
    }

    // 最も生産的な時間帯
    const completionsByHour = this.groupCompletionsByHour(tasks);
    const peakHour = this.findPeakProductivityHour(completionsByHour);
    if (peakHour) {
      insights.push(`最も生産的な時間帯: ${peakHour}時台`);
    }

    return insights;
  }
}
```

## Frontend実装（オーケストレーション）

### 1. タスクオーケストレーター

```typescript
// frontend/orchestrators/task.orchestrator.ts
export class TaskOrchestrator {
  constructor(
    private taskService: TaskService,
    private categoryService: CategoryService,
    private uiState: UIStateManager,
    private notificationManager: NotificationManager
  ) {}

  // フロントエンドでのタスク作成フロー
  async createTaskWithOptimisticUpdate(input: CreateTaskInput): Promise<void> {
    // 1. 楽観的UI更新
    const optimisticTask = {
      id: `temp_${Date.now()}`,
      ...input,
      status: 'todo' as const,
      createdAt: new Date(),
      loading: true
    };
    
    this.uiState.addTask(optimisticTask);

    try {
      // 2. カテゴリ確認（必要なら作成）
      let categoryId = input.categoryId;
      if (input.newCategory) {
        const category = await this.categoryService.createCategory(input.newCategory);
        categoryId = category.id;
      }

      // 3. バックエンドにタスク作成
      const actualTask = await this.taskService.create({
        ...input,
        categoryId
      });

      // 4. 楽観的更新を実際のデータで置換
      this.uiState.replaceTask(optimisticTask.id, actualTask);

      // 5. 成功通知
      this.notificationManager.success('タスクを作成しました');

    } catch (error) {
      // エラー時は楽観的更新をロールバック
      this.uiState.removeTask(optimisticTask.id);
      this.notificationManager.error('タスクの作成に失敗しました');
      throw error;
    }
  }

  // 複数タスクの一括操作
  async bulkUpdateStatus(taskIds: string[], newStatus: TaskStatus): Promise<void> {
    // 楽観的更新
    const originalStates = new Map<string, TaskStatus>();
    
    taskIds.forEach(id => {
      const task = this.uiState.getTask(id);
      if (task) {
        originalStates.set(id, task.status);
        this.uiState.updateTaskStatus(id, newStatus);
      }
    });

    try {
      // 並列実行
      await Promise.all(
        taskIds.map(id => this.taskService.updateStatus(id, newStatus))
      );

      // 完了タスクの場合、ダッシュボードを更新
      if (newStatus === 'done') {
        this.refreshDashboardStats();
      }

    } catch (error) {
      // ロールバック
      originalStates.forEach((originalStatus, id) => {
        this.uiState.updateTaskStatus(id, originalStatus);
      });
      throw error;
    }
  }

  // スマート優先度提案（将来の機能）
  async suggestPriority(task: Task): Promise<Priority> {
    // Phase 3で実装予定
    // 現在は単純なルールベース
    
    if (task.title.toLowerCase().includes('urgent') || 
        task.title.toLowerCase().includes('緊急')) {
      return 'high';
    }
    
    if (task.categoryId) {
      const category = await this.categoryService.getCategory(task.categoryId);
      if (category?.name.toLowerCase().includes('work')) {
        return 'high';
      }
    }
    
    return 'medium';
  }

  // リアルタイム同期
  subscribeToTaskUpdates(): void {
    const eventSource = new EventSource('/api/tasks/updates');
    
    eventSource.onmessage = (event) => {
      const notification = JSON.parse(event.data);
      
      switch (notification.type) {
        case 'task.created':
          if (notification.userId !== this.currentUserId) {
            // 他のユーザーが作成したタスクを追加
            this.taskService.getTask(notification.taskId).then(task => {
              this.uiState.addTask(task);
            });
          }
          break;
          
        case 'task.completed':
          this.uiState.updateTaskStatus(notification.taskId, 'done');
          this.refreshDashboardStats();
          break;
      }
    };
  }
}
```

### 2. React コンポーネント

```tsx
// frontend/components/TaskList.tsx
import React, { useEffect } from 'react';
import { useTaskStore } from '../state/task.store';
import { TaskOrchestrator } from '../orchestrators/task.orchestrator';

export const TaskList: React.FC = () => {
  const { tasks, filter, loading } = useTaskStore();
  const orchestrator = useTaskOrchestrator();

  useEffect(() => {
    // リアルタイム更新を購読
    orchestrator.subscribeToTaskUpdates();
  }, []);

  const handleStatusChange = async (taskId: string, newStatus: TaskStatus) => {
    try {
      await orchestrator.updateTaskStatus(taskId, newStatus);
    } catch (error) {
      console.error('Status update failed:', error);
    }
  };

  const handleQuickAdd = async (title: string) => {
    await orchestrator.quickAddTask(title);
  };

  return (
    <div className="task-list">
      {/* クイック追加（BO-001） */}
      <QuickAddForm onSubmit={handleQuickAdd} />
      
      {/* フィルタ（BC-003） */}
      <CategoryFilter />
      <PriorityFilter />
      
      {/* タスク一覧 */}
      <div className="tasks">
        {tasks.map(task => (
          <TaskItem
            key={task.id}
            task={task}
            onStatusChange={(status) => handleStatusChange(task.id, status)}
          />
        ))}
      </div>
    </div>
  );
};

// frontend/components/Dashboard.tsx
export const Dashboard: React.FC = () => {
  const { stats, loading } = useDashboard();
  
  return (
    <div className="dashboard">
      {/* サマリー表示（BC-005） */}
      <div className="summary-cards">
        <SummaryCard title="未完了" value={stats.todo} color="yellow" />
        <SummaryCard title="進行中" value={stats.inProgress} color="blue" />
        <SummaryCard title="完了" value={stats.done} color="green" />
      </div>
      
      {/* 優先度別表示 */}
      <PriorityChart data={stats.priorityBreakdown} />
      
      {/* カテゴリ別表示 */}
      <CategoryChart data={stats.categoryBreakdown} />
      
      {/* 週次レポート（BC-006） */}
      <WeeklyReport />
    </div>
  );
};
```

## GraphQL スキーマ

```graphql
# backend/api/graphql/schema.graphql
type Task {
  id: ID!
  title: String!
  description: String
  status: TaskStatus!
  priority: Priority!
  category: Category
  createdBy: User!
  createdAt: DateTime!
  updatedAt: DateTime!
  completedAt: DateTime
}

enum TaskStatus {
  TODO
  IN_PROGRESS
  DONE
  ARCHIVED
}

enum Priority {
  LOW
  MEDIUM
  HIGH
  CRITICAL
}

type Query {
  # タスク取得
  tasks(filter: TaskFilter): [Task!]!
  task(id: ID!): Task
  
  # ダッシュボード
  dashboard: DashboardData!
  
  # レポート
  weeklyReport: Report!
}

type Mutation {
  # タスク操作
  createTask(input: CreateTaskInput!): Task!
  updateTask(id: ID!, input: UpdateTaskInput!): Task!
  updateTaskStatus(id: ID!, status: TaskStatus!): Task!
  deleteTask(id: ID!): Boolean!
  
  # 一括操作
  bulkUpdateStatus(ids: [ID!]!, status: TaskStatus!): [Task!]!
  archiveCompletedTasks: Int!
  
  # カテゴリ操作
  createCategory(name: String!, parentId: ID): Category!
}

type Subscription {
  # リアルタイム更新
  taskUpdates(userId: ID!): TaskNotification!
}
```

## データベース設計（PostgreSQL）

```sql
-- タスクテーブル
CREATE TABLE tasks (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'todo',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    category_id VARCHAR(50),
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    CONSTRAINT fk_category FOREIGN KEY (category_id) 
        REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_created_by_status (created_by, status),
    INDEX idx_completed_at (completed_at)
);

-- カテゴリテーブル（階層構造対応）
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    color VARCHAR(7),
    user_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_parent FOREIGN KEY (parent_id) 
        REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- 通知ログ（監査用）
CREATE TABLE notification_logs (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_type_created (type, created_at)
);
```

## まとめ

このTODOアプリの実装例では、Parasol V5の原則に従って：

1. **シンプルなCRUD + 軽量通知**: イベントソーシングを使わない
2. **フロントエンドオーケストレーション**: 複雑なフローはフロントで管理
3. **楽観的更新**: UIの即座の反応
4. **段階的成熟度向上**: 基本機能から高度な機能へ
5. **価値の追跡**: ビジネス価値から実装まで一貫性を保つ

これにより、保守しやすく拡張可能なアプリケーションが構築できます。