# パラソルDDDフレームワーク - Amplifier統合シナリオ

## 概要

パラソル開発フレームワークをAmplifier上で実行するためのDDD（Domain-Driven Development）フレームワークです。中心の情報設計から、設計書、実装コード、テスト、ドキュメントが傘のように展開される開発手法を実現します。

## フレームワーク構成

```
amplifier/parasol/
├── __init__.py          # フレームワークエントリポイント
├── core.py              # ParasolEngine - メインオーケストレータ
├── phases.py            # 6つのフェーズ定義
├── patterns.py          # パターンライブラリとマッチング
├── knowledge.py         # ナレッジベースシステム
└── memory.py            # メモリと実行履歴管理
```

## 6つのフェーズ

### Phase 1: 価値分析 (Value Analysis)
- ステークホルダー分析
- 価値提案の定義
- KPI設定
- ROI計算

### Phase 2: 能力設計 (Capability Design)
- L1 戦略的能力
- L2 戦術的能力
- L3 運用能力
- 能力間の依存関係

### Phase 3: ドメインモデリング (Domain Modeling)
- 境界コンテキストの識別
- エンティティ定義
- 集約設計
- ドメインイベント
- ユビキタス言語

### Phase 4: オペレーション設計 (Operation Design)
- 操作の識別
- パターン分類（CRUD/Workflow/Analytics/Collaboration）
- API設計
- ビジネスルール定義

### Phase 5: 実装生成 (Implementation Generation)
- コード自動生成
- テスト生成
- ドキュメント生成
- デプロイメント設定

### Phase 6: 検証と最適化 (Validation & Optimization)
- ビジネスルール検証
- パフォーマンス最適化
- セキュリティ監査
- 価値メトリクス測定

## クイックスタート

### 1. 基本的な使い方

```python
from amplifier.parasol import (
    ParasolEngine,
    ValueAnalysisPhase,
    CapabilityDesignPhase,
    DomainModelingPhase,
    OperationDesignPhase,
    ImplementationGenerationPhase,
    ValidationOptimizationPhase
)

# エンジンの初期化
engine = ParasolEngine()

# フェーズの登録
engine.register_phase(ValueAnalysisPhase())
engine.register_phase(CapabilityDesignPhase())
engine.register_phase(DomainModelingPhase())
engine.register_phase(OperationDesignPhase())
engine.register_phase(ImplementationGenerationPhase())
engine.register_phase(ValidationOptimizationPhase())

# プロジェクトの初期化
value_definition = {
    'core_value': 'プロジェクト成功率の向上',
    'metrics': {
        'success_rate': '95%',
        'time_to_market': '30% reduction',
        'quality': '50% fewer defects'
    },
    'roi_target': '300%'
}

context = engine.initialize_project(
    project_name='consulting-dashboard',
    project_path='./projects/consulting-dashboard',
    value_definition=value_definition
)

# 実行
result = engine.execute()

# フィードバックからの学習
feedback = {
    'issues': ['Performance needs improvement'],
    'suggestions': ['Add more caching']
}
engine.learn_from_execution(feedback)
```

### 2. 特定のフェーズのみ実行

```python
# 価値分析とケーパビリティ設計のみ実行
result = engine.execute(phases=['Value Analysis', 'Capability Design'])
```

### 3. パターンライブラリの使用

```python
from amplifier.parasol import PatternLibrary, PatternMatcher

# パターンライブラリ
library = PatternLibrary()

# パターン検索
crud_patterns = library.get_patterns(category='operation', tags=['crud'])

# パターンマッチング
matcher = PatternMatcher(library)
applicable = matcher.find_applicable_patterns(context, 'Operation Design')
```

### 4. ナレッジベースの活用

```python
from amplifier.parasol import KnowledgeBase, KnowledgeCollector

# ナレッジベース
kb = KnowledgeBase()

# 知識の検索
insights = kb.search('task management', filters={'type': 'learning'})

# コンテキストに基づく推奨
recommendations = kb.get_insights_for_context(context)
```

## シナリオ例

### シナリオ1: コンサルティングダッシュボード開発

```python
# scenarios/parasol_ddd/consulting_dashboard.py

def run_consulting_dashboard_scenario():
    """コンサルティングダッシュボード開発シナリオ"""

    # 価値定義
    value_def = {
        'core_value': 'コンサルティングプロジェクトの可視化と最適化',
        'stakeholders': [
            {
                'name': 'プロジェクトマネージャー',
                'values': ['進捗可視化', 'リソース最適化', 'リスク管理']
            },
            {
                'name': 'コンサルタント',
                'values': ['タスク管理', '成果物管理', 'ナレッジ共有']
            }
        ],
        'metrics': {
            'project_visibility': '100%',
            'resource_utilization': '85%',
            'project_success_rate': '95%'
        }
    }

    # エンジン設定
    engine = create_parasol_engine()

    # プロジェクト初期化
    context = engine.initialize_project(
        project_name='consulting-dashboard',
        project_path='./generated/consulting-dashboard',
        value_definition=value_def
    )

    # 実行
    result = engine.execute()

    print(f"Generated artifacts: {context.generated_artifacts}")
    print(f"Patterns applied: {result['patterns_applied']}")
    print(f"Metrics achieved: {result['metrics']}")

    return result
```

### シナリオ2: タスク管理システム構築

```python
# scenarios/parasol_ddd/task_management.py

def run_task_management_scenario():
    """タスク管理システム構築シナリオ"""

    # V3.0のL3 Capability ⊃ Operations構造を適用
    value_def = {
        'core_value': 'チームの生産性向上',
        'metrics': {
            'task_completion_rate': '> 90%',
            'cycle_time': '< 3 days',
            'team_satisfaction': '> 4.5/5'
        }
    }

    engine = create_parasol_engine()

    # カスタムパターンの登録
    engine.pattern_library.add_pattern(
        Pattern(
            id='TASK-001',
            name='Task Management Capability',
            category='capability',
            type='structural',
            problem='Need comprehensive task management',
            solution='L3 capability with CRUD, Workflow, Analytics operations',
            context={'phase': 'capability_design'},
            consequences={'benefits': ['Complete coverage']},
            tags=['task', 'management']
        )
    )

    context = engine.initialize_project(
        project_name='task-management',
        project_path='./generated/task-management',
        value_definition=value_def
    )

    result = engine.execute()

    return result
```

## パターンカタログ

### 組み込みパターン

- **VAL-001**: Stakeholder Value Matrix
- **CAP-001**: Hierarchical Capability Decomposition
- **DOM-001**: Aggregate Root
- **OPS-001**: CRUD Operations
- **OPS-002**: Workflow Pattern
- **IMP-001**: Microservice Architecture

### カスタムパターンの追加

```python
from amplifier.parasol import Pattern

custom_pattern = Pattern(
    id='CUSTOM-001',
    name='My Custom Pattern',
    category='domain',
    type='structural',
    problem='Specific problem description',
    solution='Pattern solution',
    context={'applicability': 'specific_context'},
    consequences={'benefits': [], 'liabilities': []},
    tags=['custom', 'domain']
)

engine.pattern_library.add_pattern(custom_pattern)
```

## Amplifierとの統合

### メタ認知レシピとして実行

```bash
# Amplifierのレシピとして実行
amplifier run scenarios/parasol_ddd/recipe.md \
  --project-name="my-project" \
  --output="./generated"
```

### CLIコマンド

```bash
# パラソルエンジンの直接実行
python -m amplifier.parasol \
  --project consulting-dashboard \
  --value-definition value.yaml \
  --phases all \
  --output ./generated
```

## ナレッジの蓄積と活用

### 実行履歴の分析

```python
# メモリシステムから学習
memory = engine.memory
history = memory.get_execution_history('consulting-dashboard')

# パターン効果の分析
analysis = memory.analyze_execution_patterns()
print(f"Most effective patterns: {analysis['most_effective_patterns']}")
```

### ナレッジのエクスポート/インポート

```python
# エクスポート
engine.knowledge_base.export_knowledge(Path('knowledge_export.json'))

# インポート（別プロジェクトで再利用）
new_kb = KnowledgeBase()
new_kb.import_knowledge(Path('knowledge_export.json'))
```

## ベストプラクティス

1. **価値定義を明確に**: すべての開発は価値から始まる
2. **フェーズを段階的に実行**: 必要に応じて特定フェーズのみ実行
3. **パターンを活用**: 実証済みのパターンを積極的に適用
4. **ナレッジを蓄積**: 実行結果から継続的に学習
5. **フィードバックループ**: 結果を次回に活かす

## トラブルシューティング

### よくある問題

**Q: フェーズのゲート条件を満たせない**
```python
# ゲート条件を確認
phase = ValueAnalysisPhase()
if not phase.check_gate_conditions(context):
    print("Missing requirements:", context.value_definition)
```

**Q: パターンが適用されない**
```python
# パターンの適用条件を確認
matcher = PatternMatcher(library)
patterns = matcher.find_applicable_patterns(context, 'current_phase')
for pattern in patterns:
    print(f"Pattern {pattern.id}: {pattern.context['applicability']}")
```

## 今後の展開

- AIによるパターン推奨の強化
- 実行結果からの自動学習
- より多くの組み込みパターン
- GUIツールの開発
- クラウドベースのナレッジ共有

## リンク

- [Amplifier Documentation](../README.md)
- [Parasol Framework Design](../../framework/parasol-development-framework.md)
- [Pattern Library](../../framework/patterns/)
- [Knowledge Base](../../framework/knowledge-base/)