# Parasol5 Shared Context

Parasol V5 DDD・設計空間（Problem Space + Solution Space）の共有コンテキストです。

## Core Concepts

### ZIGZAGプロセス - Parasol5の位置づけ

```
Value Space (価値空間)     - Phase 0-2: value5/*
  VL1 → VL2 → VL3 → VS0-VS7

Problem Space (問題空間)   - Phase 3: parasol5/capability/*   <- THIS PACKAGE
  CL1 → CL2 → CL3 → BC

Solution Space (解決空間)  - Phase 4-5: parasol5/architecture/*  <- THIS PACKAGE
  Service → API → DB (設計まで。実装はGitHub spec-kit等を使用)
```

### Capability Level (CL) - ケイパビリティ階層

- **CL1**: Activity Area（活動領域 - 傾向的分類）
- **CL2**: Capability（ケイパビリティ - サービス境界）
- **CL3**: Business Operation（業務オペレーション - BC入力）

### VMS - Value Milestone State（顧客価値状態）

```
VMS1: 顧客が最初の価値を体験できる状態     (3ヶ月)
VMS2: 顧客が価値を認識し選択できる状態     (6ヶ月)
VMS3: 顧客が主要価値を日常的に体験できる状態 (9ヶ月)
VMS4: 顧客が全面的に価値を実感している状態   (12ヶ月)
VMS5: 顧客が期待を超える価値を享受している状態 (18ヶ月)
```

## Design Principles

### 構造的必然性 (Structural Necessity)

すべての設計判断は4基準で検証:
1. **価値起源**: 誰のどんな価値を実現するのか
2. **因果関係**: なぜその判断が価値を生むのか
3. **代替案検討**: 他の選択肢と比較したか
4. **測定可能性**: 効果を測定できるか

### 想像の設計の排除

根拠なき設計判断（「思われる」「はず」「業界標準だから」）を検出・排除する。

### 価値継承 (Value Inheritance)

上位フェーズで定義した価値が下位フェーズに正しく継承されているかを検証する。

## Command Mapping

| Category | Commands | Phase |
|----------|----------|-------|
| `capability/` | decompose | 3 |
| `architecture/` | application, software | 4-5 |
| _(implementation)_ | _(GitHub spec-kit等を使用)_ | _(6-7)_ |
| `milestone/` | status, quality-gate | Cross-cutting |
| `execution/` | quick-start, full-design, full-implementation | Integration |
| `utils/` | help, status, project, validate | Utility |

## Related: value5 (価値空間コマンド)

| Command | Phase |
|---------|-------|
| `/value5:init` | 0 |
| `/value5:context` | 1 |
| `/value5:definition` | 2 |
| `/value5:trace`, `/value5:necessity-check`, `/value5:imagination-detect`, `/value5:inheritance` | - |

## Output Structure

```
outputs/
├── 3-capabilities/        # Phase 3: ケイパビリティ
├── 4-architecture/        # Phase 4: アーキテクチャ
├── 5-software/            # Phase 5: ソフトウェア設計
├── 6-implementation/      # Phase 6: 実装 (GitHub spec-kit等)
└── 7-platform/            # Phase 7: プラットフォーム (GitHub spec-kit等)
```
