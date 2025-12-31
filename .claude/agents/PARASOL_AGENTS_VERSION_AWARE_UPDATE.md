# Parasolエージェントのバージョン認識アップデート

## 現在のParasolサブエージェント一覧と対応状況

### 1. parasol-book-architect ✅
**現状**: 書籍の執筆・変換を担当
**バージョン認識の追加方法**:
```markdown
## Version Awareness

When working on Parasol books, I understand:
- Current version from VERSION_CONFIG.yml
- Base version inheritance patterns
- Version-specific style guides and requirements
- Multi-version book structure under books/ directory

Before any operation:
1. Check VERSION_CONFIG.yml for version context
2. Adapt style and content to version requirements
3. Maintain consistency within the version
```

### 2. parasol-execution-documenter ✅
**現状**: プロジェクト実行のドキュメント化
**バージョン認識**: すでに書籍構造を認識するよう設計済み

### 3. parasol-phase0-assessment ❓
**現状**: Phase 0の組織評価
**必要な更新**: バージョン別の評価基準追加

### 4. parasol-phase1-context ✅
**現状**: Phase 1のコンテキスト確立
**バージョン認識**: PARASOL_AGENTS_BOOK_CONFIG.mdで設定済み

### 5. parasol-phase2-value ❓
**現状**: Phase 2の価値ストリーム
**必要な更新**: バージョン別の価値定義

### 6. parasol-phase3-capabilities ✅
**現状**: Phase 3のケイパビリティ定義
**バージョン認識**: 書籍参照が追加済み

### 7. parasol-phase4-architecture ❓
**現状**: Phase 4のアーキテクチャ設計
**必要な更新**: バージョン別のパターン認識

### 8. parasol-phase5-software ❓
**現状**: Phase 5のソフトウェア設計
**必要な更新**: バージョン別の設計原則

### 9. parasol-phase6-implementation ❓
**現状**: Phase 6の実装
**必要な更新**: バージョン別の実装標準

### 10. parasol-phase7-platform ❓
**現状**: Phase 7のプラットフォーム統合
**必要な更新**: バージョン別の統合パターン

### 11. parasol-version-manager ✅ (新規)
**現状**: バージョン管理専門
**バージョン認識**: 完全対応

## 統一的なバージョン認識の実装

### すべてのエージェントに追加する共通セクション

```markdown
## Version Context Recognition

This agent recognizes the Parasol book version structure:

1. **Version Detection**
   - Read VERSION_CONFIG.yml from current book directory
   - Identify version, variant, and base_version
   - Apply version-specific rules and constraints

2. **Multi-Version Support**
   - Understand parallel version existence
   - Reference correct version documentation
   - Maintain version isolation

3. **Version-Aware Operations**
   - Prefix outputs with version identifier when needed
   - Use version-appropriate terminology
   - Follow version-specific style guides
```

### エージェント間の連携プロトコル

```yaml
# Inter-agent version communication
agent_communication:
  version_handshake:
    sender: "Working on Parasol v5.5-modular"
    receiver: "Acknowledged, applying v5.5 context"
  
  cross_version_reference:
    format: "In v5.4: [reference], Updated in v5.5: [changes]"
```

## 実装計画

### Phase 1: 基本的なバージョン認識（必須）
1. すべてのエージェントにVERSION_CONFIG.yml読み込み機能
2. バージョン番号の出力への含有
3. バージョン固有の挙動の実装

### Phase 2: 高度なバージョン機能（推奨）
1. バージョン間の差分認識
2. 移行支援機能
3. 互換性チェック

### Phase 3: 統合機能（将来）
1. 自動バージョンアップ提案
2. クロスバージョン検索
3. バージョン別メトリクス

## 設定ファイルの統合

```yaml
# .claude/commands/parasol/PARASOL_AGENTS_VERSION_CONFIG.yml
agents_version_settings:
  global:
    version_awareness: enabled
    default_version: "5.4-modular"
    version_directory_pattern: "parasol-v{version}-{variant}"
  
  per_agent_overrides:
    parasol-book-architect:
      multi_version_edit: true
    parasol-version-manager:
      version_creation: true
```

## テスト方法

```bash
# エージェントのバージョン認識テスト
1. cd parasol-v5.4-modular/
2. エージェントを起動
3. "What version are you working with?" と質問
4. 正しいバージョンが返されることを確認
```

---

最終更新: 2025-12-29
目的: Parasolエージェントの統一的なバージョン認識実装