# /parasol:6-implementation - ソフトウェア実装

## コマンド: `/parasol:6-implementation`

設計に基づいて実際のコードを生成・実装します。バックエンド、フロントエンド、テストコードを作成します。

## 実行時間
約3-4時間

## 前提条件
- Phase 5（ソフトウェア設計）の完了
- ドメインモデルの確定
- 技術スタックの決定

## 実行内容

### Task 1: バックエンド実装（Spring Boot例）

#### ドメインエンティティ実装
```java
// Project.java
@Entity
@Table(name = "projects")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Project {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, unique = true, length = 100)
    private String name;

    @Column(columnDefinition = "TEXT")
    private String description;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "stage_id", nullable = false)
    private ValueStage stage;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private ProjectStatus status;

    @Column(name = "owner_id", nullable = false)
    private UUID ownerId;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;

    // ビジネスメソッド
    public void transitionTo(ValueStage newStage) {
        if (!canTransitionTo(newStage)) {
            throw new IllegalStateException(
                "Cannot transition from " + this.stage.getName() +
                " to " + newStage.getName()
            );
        }
        this.stage = newStage;
        this.updatedAt = LocalDateTime.now();
    }

    private boolean canTransitionTo(ValueStage newStage) {
        return newStage.getOrder() == this.stage.getOrder() + 1;
    }

    public void archive() {
        this.status = ProjectStatus.ARCHIVED;
        this.deletedAt = LocalDateTime.now();
    }
}
```

#### サービス層実装
```java
// ProjectService.java
@Service
@Transactional
@RequiredArgsConstructor
public class ProjectService {
    private final ProjectRepository projectRepository;
    private final AuthService authService;
    private final NotificationService notificationService;
    private final ProjectMapper projectMapper;

    public ProjectDto createProject(CreateProjectRequest request) {
        // 権限確認
        if (!authService.hasPermission(
            getCurrentUserId(),
            "project:create"
        )) {
            throw new AccessDeniedException("Project creation denied");
        }

        // プロジェクト作成
        Project project = Project.builder()
            .name(request.getName())
            .description(request.getDescription())
            .stage(getInitialStage())
            .status(ProjectStatus.ACTIVE)
            .ownerId(getCurrentUserId())
            .build();

        Project saved = projectRepository.save(project);

        // 通知送信
        notificationService.sendProjectCreated(saved);

        return projectMapper.toDto(saved);
    }

    public ProjectDto transitionStage(
        UUID projectId,
        String newStageId
    ) {
        Project project = projectRepository
            .findById(projectId)
            .orElseThrow(() -> new NotFoundException("Project not found"));

        ValueStage newStage = valueStageRepository
            .findById(newStageId)
            .orElseThrow(() -> new NotFoundException("Stage not found"));

        // ステージ遷移
        ValueStage oldStage = project.getStage();
        project.transitionTo(newStage);

        Project updated = projectRepository.save(project);

        // イベント発行
        eventPublisher.publish(
            new StageTransitionedEvent(
                projectId,
                oldStage.getId(),
                newStageId,
                getCurrentUserId()
            )
        );

        return projectMapper.toDto(updated);
    }
}
```

#### REST コントローラー実装
```java
// ProjectController.java
@RestController
@RequestMapping("/api/projects")
@RequiredArgsConstructor
@Tag(name = "Projects", description = "Project management API")
public class ProjectController {
    private final ProjectService projectService;

    @PostMapping
    @Operation(summary = "Create new project")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Created"),
        @ApiResponse(responseCode = "400", description = "Bad request"),
        @ApiResponse(responseCode = "403", description = "Forbidden")
    })
    public ResponseEntity<ProjectDto> createProject(
        @Valid @RequestBody CreateProjectRequest request
    ) {
        ProjectDto created = projectService.createProject(request);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(created);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get project by ID")
    public ResponseEntity<ProjectDto> getProject(
        @PathVariable UUID id
    ) {
        ProjectDto project = projectService.getProject(id);
        return ResponseEntity.ok(project);
    }

    @PutMapping("/{id}/stage")
    @Operation(summary = "Transition project stage")
    public ResponseEntity<ProjectDto> transitionStage(
        @PathVariable UUID id,
        @Valid @RequestBody TransitionStageRequest request
    ) {
        ProjectDto updated = projectService.transitionStage(
            id,
            request.getNewStageId()
        );
        return ResponseEntity.ok(updated);
    }
}
```

### Task 2: フロントエンド実装（Next.js例）

#### APIクライアント
```typescript
// api/projectApi.ts
import { createApi } from '@/lib/api-client';

export interface Project {
  id: string;
  name: string;
  description: string;
  stage: ValueStage;
  status: ProjectStatus;
  createdAt: string;
  updatedAt: string;
}

export const projectApi = createApi({
  baseUrl: '/api/projects',

  endpoints: {
    create: async (data: CreateProjectInput): Promise<Project> => {
      return await this.post('/', data);
    },

    getById: async (id: string): Promise<Project> => {
      return await this.get(`/${id}`);
    },

    list: async (filter?: ProjectFilter): Promise<Project[]> => {
      return await this.get('/', { params: filter });
    },

    transitionStage: async (
      id: string,
      newStageId: string
    ): Promise<Project> => {
      return await this.put(`/${id}/stage`, { newStageId });
    },
  },
});
```

#### React コンポーネント
```tsx
// components/ProjectCard.tsx
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Project } from '@/api/projectApi';

interface ProjectCardProps {
  project: Project;
  onTransition?: (stageId: string) => void;
}

export function ProjectCard({ project, onTransition }: ProjectCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-xl font-semibold">{project.name}</h3>
            <p className="text-gray-600 mt-1">{project.description}</p>
          </div>
          <Badge variant={getStatusVariant(project.status)}>
            {project.status}
          </Badge>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">Stage:</span>
            <Badge variant="outline">{project.stage.name}</Badge>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">Created:</span>
            <span className="text-sm">
              {formatDate(project.createdAt)}
            </span>
          </div>

          {onTransition && canTransition(project) && (
            <Button
              onClick={() => onTransition(getNextStage(project))}
              className="w-full"
            >
              Move to Next Stage
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
```

#### 状態管理（Zustand）
```typescript
// stores/projectStore.ts
import { create } from 'zustand';
import { projectApi } from '@/api/projectApi';

interface ProjectStore {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  error: string | null;

  fetchProjects: () => Promise<void>;
  createProject: (data: CreateProjectInput) => Promise<void>;
  transitionStage: (projectId: string, stageId: string) => Promise<void>;
  setCurrentProject: (project: Project | null) => void;
}

export const useProjectStore = create<ProjectStore>((set, get) => ({
  projects: [],
  currentProject: null,
  isLoading: false,
  error: null,

  fetchProjects: async () => {
    set({ isLoading: true, error: null });
    try {
      const projects = await projectApi.list();
      set({ projects, isLoading: false });
    } catch (error) {
      set({
        error: error.message || 'Failed to fetch projects',
        isLoading: false
      });
    }
  },

  createProject: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const newProject = await projectApi.create(data);
      set(state => ({
        projects: [...state.projects, newProject],
        isLoading: false
      }));
    } catch (error) {
      set({
        error: error.message || 'Failed to create project',
        isLoading: false
      });
    }
  },

  transitionStage: async (projectId, stageId) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await projectApi.transitionStage(projectId, stageId);
      set(state => ({
        projects: state.projects.map(p =>
          p.id === projectId ? updated : p
        ),
        currentProject: state.currentProject?.id === projectId
          ? updated
          : state.currentProject,
        isLoading: false
      }));
    } catch (error) {
      set({
        error: error.message || 'Failed to transition stage',
        isLoading: false
      });
    }
  },

  setCurrentProject: (project) => {
    set({ currentProject: project });
  },
}));
```

### Task 3: テスト実装

#### ユニットテスト
```java
// ProjectServiceTest.java
@ExtendWith(MockitoExtension.class)
class ProjectServiceTest {
    @Mock
    private ProjectRepository projectRepository;

    @Mock
    private AuthService authService;

    @InjectMocks
    private ProjectService projectService;

    @Test
    void createProject_Success() {
        // Given
        CreateProjectRequest request = new CreateProjectRequest(
            "Test Project",
            "Description"
        );

        when(authService.hasPermission(any(), eq("project:create")))
            .thenReturn(true);
        when(projectRepository.save(any()))
            .thenReturn(createMockProject());

        // When
        ProjectDto result = projectService.createProject(request);

        // Then
        assertNotNull(result);
        assertEquals("Test Project", result.getName());
        verify(projectRepository).save(any(Project.class));
    }

    @Test
    void transitionStage_InvalidTransition_ThrowsException() {
        // Given
        Project project = createMockProject();
        project.setStage(createStage("VS3", 3));

        ValueStage invalidStage = createStage("VS5", 5); // Skip VS4

        when(projectRepository.findById(any()))
            .thenReturn(Optional.of(project));

        // When & Then
        assertThrows(
            IllegalStateException.class,
            () -> project.transitionTo(invalidStage)
        );
    }
}
```

#### 統合テスト
```typescript
// __tests__/projects.integration.test.ts
describe('Project API Integration', () => {
  let project: Project;

  beforeEach(async () => {
    await resetDatabase();
    await seedTestData();
  });

  test('Create and transition project', async () => {
    // Create project
    const createResponse = await request(app)
      .post('/api/projects')
      .send({
        name: 'Integration Test Project',
        description: 'Test description'
      })
      .expect(201);

    project = createResponse.body;
    expect(project.stage.id).toBe('VS1');

    // Transition to next stage
    const transitionResponse = await request(app)
      .put(`/api/projects/${project.id}/stage`)
      .send({ newStageId: 'VS2' })
      .expect(200);

    expect(transitionResponse.body.stage.id).toBe('VS2');
  });

  test('Invalid stage transition returns error', async () => {
    const response = await request(app)
      .put(`/api/projects/${project.id}/stage`)
      .send({ newStageId: 'VS5' }) // Invalid jump
      .expect(400);

    expect(response.body.error).toContain('Invalid transition');
  });
});
```

## 成果物

以下のファイルが`outputs/6-implementation/`に生成されます：

1. **backend/**
   - ソースコード（Java/Spring Boot）
   - 設定ファイル
   - Dockerファイル

2. **frontend/**
   - ソースコード（TypeScript/Next.js）
   - コンポーネント
   - 設定ファイル

3. **tests/**
   - ユニットテスト
   - 統合テスト
   - E2Eテスト

4. **docs/**
   - API ドキュメント
   - セットアップガイド
   - アーキテクチャ図

## チェックリスト

- [ ] ドメインロジックが正しく実装されているか
- [ ] APIが設計通りに動作するか
- [ ] フロントエンドが使いやすいか
- [ ] テストカバレッジが十分か（目標: 80%以上）
- [ ] エラーハンドリングが適切か

## 価値トレーサビリティ（Phase 6）

> **参照**: `_value-traceability-system/phase-integration-patterns.md` - Phase 6価値実現の検証

### 実装価値の直接検証

**価値実現コードの識別と検証**：
```yaml
価値実現機能コード:
  Project.transitionTo():
    価値実現: VS遷移による価値進化の確実な実装
    検証方法: ステージ遷移テストによる価値進化確認
    価値測定: 遷移成功率、価値実現時間、品質指標

  ProjectService.createProject():
    価値実現: VS1認知形成価値のスタート機能
    検証方法: プロジェクト作成フローテストによる価値開始確認
    価値測定: 作成成功率、初期設定完了率、ユーザー満足度
```

### テストによる価値検証

**価値実現テストの実装**：
```yaml
価値検証テストスイート:
  価値実現統合テスト:
    - create_and_transition_project_test:
        価値検証: VL1→MS1価値実現フローの完全実行
        期待結果: 価値進捗の段階的実現確認

  価値測定ユニットテスト:
    - project_metrics_collection_test:
        価値検証: 価値実現度の正確な測定機能
        期待結果: 定量的価値実現データの収集確認
```

### フロントエンド価値体験

**価値実現UIの検証**：
```yaml
価値体験実装:
  ProjectCard.tsx:
    価値表示: ユーザーが価値進捗を視覚的に確認可能
    価値操作: Next Stage移行による価値進化の直感的操作
    価値フィードバック: 価値実現状況のリアルタイム表示

  useProjectStore:
    価値状態管理: 価値実現状態の一貫した管理
    価値更新: 価値変化の即座な反映
    価値永続化: 価値実現履歴の確実な保存
```

### 価値実現の最終検証

**MS4-MS5価値実現確認**：
```yaml
最終価値検証:
  価値実現度測定:
    - VL1実現度: [定量的測定結果]
    - VL2実現度: [定量的測定結果]  
    - VL3実現度: [定量的測定結果]
    - 総合価値実現度: [統合評価結果]

  価値実現証明:
    - ユーザー価値: [実際のユーザーフィードバック]
    - 組織価値: [ビジネスメトリクス改善]
    - 社会価値: [外部インパクト測定]

  価値継続性確保:
    - 価値改善機能: 継続的な価値向上のための機能実装
    - 価値監視機能: 価値劣化の早期発見機能
    - 価値保護機能: 価値維持のためのセーフガード機能
```

### MS4-MS5品質ゲート

**Phase 6完了基準**：
```yaml
実装価値検証:
  - [ ] 全価値実現機能の実装完了
  - [ ] 価値実現テストの全合格
  - [ ] 価値測定機能の動作確認
  - [ ] 価値体験UIの品質確認

最終価値実現確認:
  - [ ] VL1-VL3の実装による実現確認
  - [ ] MS1-MS5価値マイルストーンの達成確認
  - [ ] 価値実現度の定量的測定完了
  - [ ] プラットフォーム価値保護準備完了
```

## 次のステップ

実装が完了したら、プラットフォーム設計フェーズへ：

```bash
# 価値実現最終検証
./value-trace verify-final-value-realization

# MS4-MS5品質ゲート実行
./value-trace quality-gate --milestone=MS4-MS5

# 次フェーズへの価値移転
./value-trace transfer --to=phase7

# Phase 7実行
/parasol:7-platform
```

---

*実装により価値が現実のものとなります。価値トレーサビリティにより、確実な価値実現が証明されます。*