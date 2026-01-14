# Parasol V5.6 バリデータ

V5.6で導入された検証ルールとテストスイートのドキュメント。

## バリデータ一覧

### Phase 2 バリデータ（既存）

| ファイル | 用途 | ルール数 |
|---------|------|---------|
| `vc-completeness.yaml` | VC（Value Component）の完全性検証 | - |
| `3axis-coverage.yaml` | 3軸カバレッジ検証 | - |
| `portfolio-balance.yaml` | ポートフォリオバランス検証 | - |

### Phase 3 バリデータ（V5.6新規）

| ファイル | 用途 | ルール数 |
|---------|------|---------|
| `os-capability-mapping.yaml` | OS-Capability 1:1マッピング検証 | 12 |
| `vc-capability-consistency.yaml` | VC-Capability整合性検証 | 10 |
| `stage-tvdc-consistency.yaml` | ステージ依存TVDC整合性検証 | 11 |

### Phase 4 バリデータ（V5.6新規）

| ファイル | 用途 | ルール数 |
|---------|------|---------|
| `os-bc-alignment.yaml` | OS-BC整合性検証 | 10 |
| `stage-architecture-consistency.yaml` | ステージ依存アーキテクチャ判断検証 | 11 |

### 統合テストスイート

| ファイル | 用途 |
|---------|------|
| `v56-integration-test-suite.yaml` | V5.6全機能の統合テスト |

## 使用方法

### 個別バリデータ実行

```bash
# Phase 3 バリデータ
/parasol:validate os-capability-mapping
/parasol:validate vc-capability-consistency
/parasol:validate stage-tvdc-consistency

# Phase 4 バリデータ
/parasol:validate os-bc-alignment
/parasol:validate stage-architecture-consistency
```

### 統合テスト実行

```bash
# 全V5.6機能の統合テスト
/parasol:validate v56-integration
```

## ルール重要度

各バリデータのルールは以下の重要度を持ちます:

| 重要度 | 説明 | 対応 |
|-------|------|------|
| `error` | 必須要件違反 | 修正必須 |
| `warning` | 推奨事項違反 | 修正推奨 |
| `info` | 情報提供 | 認識のみ |

## V5.6 主要検証ルール

### OS-Capability マッピング (os-capability-mapping.yaml)

- **OSCAP-001**: OS-Capability 1:1対応必須
- **OSCAP-002**: Value Stage範囲の有効性
- **OSCAP-003**: Capability存在確認
- **OSCAP-008**: OS責務の記載

### VC-Capability 整合性 (vc-capability-consistency.yaml)

- **VCCAP-001**: Primary VC必須
- **VCCAP-002**: VC ID有効性 (VC1-VC5)
- **VCCAP-006**: VL3のVCパターンとの整合

### ステージ依存TVDC (stage-tvdc-consistency.yaml)

- **STVDC-002**: デフォルトTVDC有効性 (Core/VCI/Supporting/Generic)
- **STVDC-004**: Value Stage形式有効性 (VS{N}_VS{M})
- **STVDC-009**: ステージ範囲重複チェック

### OS-BC 整合性 (os-bc-alignment.yaml)

- **OSBC-001**: 全OSにBC対応必須
- **OSBC-003**: alignmentステータス有効性 (aligned/partial/misaligned)
- **OSBC-004**: misaligned時の対応アクション必須

### ステージ依存アーキテクチャ (stage-architecture-consistency.yaml)

- **STARCH-003**: Build/Buy判断必須
- **STARCH-004**: Build/Buy値有効性 (Build/Buy/Buy+Customize/Partner/SaaS)
- **STARCH-005**: TVDC-Build/Buy整合性

## 検証フロー

```
Phase 3.4
    │
    ├─→ OS定義 ─→ os-capability-mapping検証
    │
    ├─→ VC-Capabilityマッピング ─→ vc-capability-consistency検証
    │
    └─→ ステージ依存TVDC ─→ stage-tvdc-consistency検証
            │
            ▼
Phase 4.1
    │
    ├─→ OS-BCマッピング ─→ os-bc-alignment検証
    │
    └─→ アーキテクチャ判断 ─→ stage-architecture-consistency検証
```

## 成功基準

統合テストの成功基準:

- 全`error`ルールがパス
- `warning`は5件以下
- カバレッジ:
  - OS-Capability対応: 100%
  - VC-Capability対応: 100%
  - TVDC定義: 100%
  - BC整合: 100%
