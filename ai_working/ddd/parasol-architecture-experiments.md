# パラソル × Amplifier DDD ワークフロー統合プラン

## 概要

Amplifierの `/ddd` (Document-Driven Development) ワークフローを使用して、パラソル開発フレームワークの各アーキテクチャパターンを体系的に実験・比較します。

## 統合アプローチ

### 1. Amplifier DDDの5フェーズとパラソル6フェーズのマッピング

```yaml
mapping:
  amplifier_ddd:
    1_plan: # 設計フェーズ
      parasol_phases:
        - Phase 1: 価値分析
        - Phase 2: 能力設計

    2_docs: # ドキュメント更新
      parasol_phases:
        - Phase 3: ドメインモデリング
        - Phase 4: オペレーション設計

    3_code_plan: # コード計画
      parasol_phases:
        - Phase 5: 実装生成（計画部分）

    4_code: # 実装と検証
      parasol_phases:
        - Phase 5: 実装生成（実装部分）
        - Phase 6: 検証と最適化

    5_finish: # 完了とクリーンアップ
      parasol_phases:
        - ナレッジ蓄積
        - パターン登録
```

## アーキテクチャ実験ワークフロー

### 各アーキテクチャに対して実行

```bash
# 1. Monolithic Architecture
/ddd:1-plan Implement task management system using monolithic architecture

# 2. Microservices Architecture
/ddd:1-plan Implement task management system using microservices architecture

# 3. Event-Driven Architecture
/ddd:1-plan Implement task management system using event-driven architecture

# 4. Clean Architecture
/ddd:1-plan Implement task management system using clean architecture

# 5. Hexagonal Architecture
/ddd:1-plan Implement task management system using hexagonal architecture

# 6. Serverless Architecture
/ddd:1-plan Implement task management system using serverless architecture

# 7. Parasol V3-V4 Hybrid
/ddd:1-plan Implement task management system using Parasol V3-V4 hybrid architecture

# 8. CQRS + Event Sourcing
/ddd:1-plan Implement task management system using CQRS with event sourcing
```

## 実験プラン詳細

### Phase 1: Planning (/ddd:1-plan)

各アーキテクチャに対して：

```markdown
# Task Management System - [Architecture Name]

## Value Analysis (パラソル Phase 1)
- Core Value: チーム生産性の向上
- KPIs:
  - タスク完了率 > 90%
  - 平均サイクルタイム < 3日
  - チーム満足度 > 4.5/5

## Capability Design (パラソル Phase 2)
- L1: タスク管理戦略能力
- L2: タスク実行戦術能力
- L3: タスク操作運用能力

## Architecture-Specific Design
- Structure: [アーキテクチャ固有の構造]
- Patterns: [使用するパターン]
- Trade-offs: [トレードオフ]
```

### Phase 2: Documentation (/ddd:2-docs)

各アーキテクチャのドキュメントを作成：

```markdown
## Domain Modeling (パラソル Phase 3)
- Bounded Contexts
- Entities
- Aggregates
- Domain Events

## Operation Design (パラソル Phase 4)
- CRUD Operations
- Workflow Operations
- Analytics Operations
- Collaboration Operations
```

### Phase 3: Code Planning (/ddd:3-code-plan)

実装計画の作成：

```markdown
## Implementation Plan (パラソル Phase 5 - Planning)
- Technology Stack
- Directory Structure
- Dependencies
- Testing Strategy
```

### Phase 4: Implementation (/ddd:4-code)

実際の実装：

```markdown
## Implementation (パラソル Phase 5 - Execution)
- Core Implementation
- Tests
- Documentation

## Validation (パラソル Phase 6)
- Unit Tests
- Integration Tests
- Performance Tests
- Metrics Collection
```

### Phase 5: Finish (/ddd:5-finish)

完了とナレッジ蓄積：

```markdown
## Knowledge Collection
- Patterns Used
- Decisions Made
- Metrics Achieved
- Lessons Learned
```

## メトリクス収集フレームワーク

### 自動収集メトリクス

```python
# amplifier/metrics/architecture_metrics.py

class ArchitectureMetrics:
    """Amplifier統合メトリクス収集"""

    def collect_ddd_metrics(self, phase: str):
        """DDDフェーズごとのメトリクス収集"""
        metrics = {
            'phase': phase,
            'timestamp': datetime.now(),
            'artifacts_created': self.count_artifacts(),
            'complexity': self.measure_complexity(),
            'test_coverage': self.measure_coverage()
        }
        return metrics

    def compare_architectures(self):
        """アーキテクチャ比較"""
        results = {}
        for arch in self.architectures:
            results[arch] = {
                'ddd_metrics': self.get_ddd_metrics(arch),
                'parasol_metrics': self.get_parasol_metrics(arch),
                'combined_score': self.calculate_score(arch)
            }
        return results
```

## Git Worktree統合

### Amplifier DDDでのWorktree管理

```bash
# 各アーキテクチャ用のworktreeで/dddを実行

# Monolithic
cd ../amplifier-monolithic
/ddd:1-plan Monolithic task management

# Microservices
cd ../amplifier-microservices
/ddd:1-plan Microservices task management

# 比較のために各worktreeのメトリクスを収集
python -c "
from amplifier.metrics import collect_all_worktrees
results = collect_all_worktrees()
print(results)
"
```

## パラソルパターンライブラリとの統合

### DDDフェーズでのパターン適用

```yaml
pattern_integration:
  ddd_1_plan:
    parasol_patterns:
      - VAL-001: Stakeholder Value Matrix
      - CAP-001: Hierarchical Capability Decomposition

  ddd_2_docs:
    parasol_patterns:
      - DOM-001: Aggregate Root
      - OPS-001: CRUD Operations
      - OPS-002: Workflow Pattern

  ddd_4_code:
    parasol_patterns:
      - IMP-001: Microservice Architecture
      - Architecture-specific patterns
```

## 実行例

### 1. Clean Architecture実験

```bash
# Step 1: Plan
/ddd:1-plan Implement task management using Clean Architecture with clear domain separation

# ai_working/ddd/plan.md が生成される

# Step 2: Documentation
/ddd:2-docs
# ドメイン層、アプリケーション層、インフラ層のドキュメントが更新される

# Step 3: Code Plan
/ddd:3-code-plan
# 実装計画が作成される

# Step 4: Implementation
/ddd:4-code
# 実際のClean Architectureコードが生成される

# Step 5: Finish
/ddd:5-finish
# メトリクスとナレッジが収集される
```

### 2. 比較レポート生成

```bash
# DDDワークフローの結果を比較
/ddd:status --compare-all

# Output:
# Architecture Comparison Report
# ==============================
# | Architecture | DDD Efficiency | Parasol Score | Overall |
# |--------------|----------------|---------------|---------|
# | Monolithic   | 85%           | 3.5/5         | Good    |
# | Microservices| 75%           | 4.5/5         | Excellent|
# | Clean        | 90%           | 4.0/5         | Excellent|
```

## カスタムDDDコマンド

### パラソル統合コマンドの作成

```bash
# .claude/commands/ddd/parasol-compare.md
---
description: Compare architectures using Parasol metrics
---

Compare all architecture implementations using both DDD and Parasol metrics.

This command will:
1. Collect DDD artifacts from all worktrees
2. Apply Parasol evaluation criteria
3. Generate comprehensive comparison report
4. Store results in knowledge base

Usage: /ddd:parasol-compare [--format=html|md|json]
```

## ベストプラクティス

### DDDワークフローでのパラソル原則

1. **価値駆動**: すべての`/ddd:1-plan`で価値定義から開始
2. **段階的詳細化**: DDDフェーズごとにパラソル階層を深化
3. **パターン適用**: 各フェーズで適切なパラソルパターンを使用
4. **ナレッジ蓄積**: `/ddd:5-finish`でパラソルナレッジベースに保存
5. **継続的改善**: メトリクスに基づいてパターンライブラリを更新

## まとめ

Amplifierの `/ddd` ワークフローは、パラソル開発フレームワークと完全に統合可能です：

- **Document-Driven**: パラソルの設計重視アプローチと一致
- **Phase-Based**: 段階的な開発プロセス
- **Artifact-Driven**: 成果物ベースの進行管理
- **Agent Orchestration**: 専門エージェントの活用
- **Knowledge Accumulation**: 実行ごとの学習

これにより、複数のアーキテクチャを体系的に実験・比較し、最適な選択ができます。