# タスク管理ドメイン - V3.0×V4統合実装例

## 概要
コンサルティングツールのタスク管理ドメインを、V3.0の正しい理解とV4のWHAT-HOW構造を統合して実装

## 1. 価値定義（Why）

```yaml
value_definition:
  business_value: "プロジェクトタスクの効率的管理による生産性向上"

  metrics:
    productivity_improvement: 30%
    error_reduction: 50%
    cycle_time_reduction: 40%

  stakeholders:
    - project_managers: "タスクの可視化と制御"
    - team_members: "明確な責務と進捗共有"
    - clients: "透明性のある進捗報告"
```

## 2. 能力階層（What）

### L1 戦略的能力
```yaml
L1_capability:
  id: "L1-project-success"
  name: "プロジェクト成功実現能力"
  what: "プロジェクトを成功に導く包括的な能力"
```

### L2 戦術的能力
```yaml
L2_capabilities:
  - id: "L2-task-management"
    name: "タスク管理能力"
    what: "タスクの作成から完了まで一貫した管理"

  - id: "L2-resource-optimization"
    name: "リソース最適化能力"
    what: "人員と時間の効率的な配分"
```

## 3. 境界コンテキスト（BC）

```yaml
bounded_context:
  name: "タスク管理コンテキスト"

  why: "プロジェクトの生産性向上"

  what: # L3能力群
    - "タスク管理能力"
    - "進捗追跡能力"
    - "協働作業能力"

  how: # ドメイン設計
    entities:
      - Task
      - Assignment
      - Progress

    aggregates:
      - TaskAggregate

    services:
      - TaskManagementService
      - ProgressTrackingService
```

## 4. L3能力とOperations（親子関係）

### L3能力定義（What）
```yaml
L3_capability:
  id: "L3-task-management"
  name: "タスク管理能力"
  what: "タスクを効率的に管理する能力"

  # この能力を実現する操作群（How）
  operations:
    - create_task
    - update_task_status
    - assign_task_to_member
    - track_task_progress
    - collaborate_on_task
```

### Operations詳細（How）

#### CRUD操作パターン
```yaml
operation_create_task:
  id: "OP-create-task"
  name: "タスクを作成する"
  pattern: "CRUD"
  sub_pattern: "Create-with-validation"

  preconditions:
    - "プロジェクトが存在する"
    - "作成権限を持つ"

  postconditions:
    - "タスクがデータベースに保存される"
    - "タスクIDが生成される"
    - "作成通知が送信される"

  business_rules:
    - "必須項目の検証"
    - "期限の妥当性チェック"
    - "優先度の自動設定"
```

#### Workflow操作パターン
```yaml
operation_update_status:
  id: "OP-update-task-status"
  name: "タスクステータスを更新する"
  pattern: "Workflow"
  sub_pattern: "State-transition"

  state_flow:
    - from: "未着手"
      to: ["進行中", "保留"]
    - from: "進行中"
      to: ["レビュー待ち", "保留", "完了"]
    - from: "レビュー待ち"
      to: ["進行中", "完了"]

  triggers:
    - "ユーザーアクション"
    - "自動進捗更新"
    - "期限到達"
```

#### Analytics操作パターン
```yaml
operation_track_progress:
  id: "OP-track-progress"
  name: "進捗を追跡する"
  pattern: "Analytics"
  sub_pattern: "Aggregation"

  metrics:
    - completion_rate
    - average_cycle_time
    - bottleneck_detection

  calculations:
    - "完了タスク数 / 全タスク数"
    - "累積フロー分析"
    - "バーンダウンチャート"
```

#### Collaboration操作パターン
```yaml
operation_collaborate:
  id: "OP-collaborate-task"
  name: "タスクで協働する"
  pattern: "Collaboration"
  sub_pattern: "Asynchronous"

  features:
    - comment_thread
    - file_sharing
    - notification_system

  events:
    - "TaskCommented"
    - "FileAttached"
    - "MentionNotified"
```

## 5. ユースケース/ページ（Implementation）

### ページ構成
```yaml
pages:
  task_list_page:
    path: "/tasks"
    components:
      - TaskGrid
      - FilterPanel
      - ActionBar

    use_cases:
      - view_all_tasks
      - filter_tasks
      - bulk_actions

  task_detail_page:
    path: "/tasks/:id"
    components:
      - TaskForm
      - StatusTracker
      - CommentSection
      - AttachmentArea

    use_cases:
      - view_task_detail
      - update_task
      - add_comment
      - upload_file

  task_analytics_page:
    path: "/tasks/analytics"
    components:
      - ProgressChart
      - MetricsGrid
      - TeamPerformance

    use_cases:
      - view_progress
      - analyze_bottlenecks
      - generate_report
```

## 6. ドメインモデル実装

### エンティティ
```typescript
// V3.0の属性を保持しつつV4の価値要素を追加
export class Task {
  // V3.0から継承
  readonly id: TaskId;
  title: string;
  description: string;
  status: TaskStatus;
  priority: Priority;
  assigneeId: UserId;
  dueDate: Date;

  // V4で追加
  valueImpact: number;        // 価値への影響度
  capabilityLink: string;     // ケーパビリティとの関連
  metrics: TaskMetrics;       // 測定メトリクス

  // ビジネスルール
  canTransitionTo(newStatus: TaskStatus): boolean {
    // V3.0のステータス遷移ルール
    const validTransitions = this.getValidTransitions();
    return validTransitions.includes(newStatus);
  }

  calculateValueImpact(): number {
    // V4の価値影響度算出ルール
    return this.priority.weight * this.metrics.businessValue;
  }
}
```

### 集約
```typescript
export class TaskAggregate {
  private task: Task;
  private assignments: Assignment[];
  private progress: Progress[];

  // L3能力を実現するメソッド
  createTask(command: CreateTaskCommand): TaskCreatedEvent {
    // CRUD操作の実装
  }

  updateStatus(newStatus: TaskStatus): StatusUpdatedEvent {
    // Workflow操作の実装
  }

  trackProgress(): ProgressMetrics {
    // Analytics操作の実装
  }

  addCollaboration(comment: Comment): CollaborationEvent {
    // Collaboration操作の実装
  }
}
```

## 7. 価値測定とフィードバック

```yaml
value_metrics_tracking:
  productivity:
    measure: "タスク完了率"
    target: "> 90%"
    current: "tracking..."

  quality:
    measure: "初回完了率"
    target: "> 80%"
    current: "tracking..."

  efficiency:
    measure: "平均サイクルタイム"
    target: "< 3 days"
    current: "tracking..."
```

## まとめ

このタスク管理ドメインの実装例は：

1. **V3.0の正しい理解**を反映
   - L3 Capability（能力）とOperations（操作）の親子関係
   - What（何ができるか）とHow（どう実現するか）の明確な分離

2. **V4のWHAT-HOW構造**を適用
   - 各レベルでの段階的詳細化
   - 価値メトリクスの組み込み

3. **統合の利点**を実現
   - トップダウン（EA）とボトムアップ（DDD）の融合
   - ビジネス価値と技術実装の連携