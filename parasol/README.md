# Parasol V4 Framework

> **注意**: このディレクトリはParasol V4（アーカイブ版）です。
> **現在は実行されません。リファレンスとしてのみ保持されています。**
>
> 実際に使用するには **Parasol V5** を参照してください:
> `/.claude/commands/parasol/`

---

## 概要

Parasol V4は「重厚長大な本格的DDDプロセス」として設計された、エンタープライズ規模のシステム刷新に対応する網羅的なアプローチです。

**ステータス**: アーカイブ（参照専用）

---

## V4 vs V5 比較

| 項目 | V4（本ディレクトリ） | V5（推奨） |
|------|---------------------|------------|
| **場所** | `/parasol/` | `/.claude/commands/parasol/` |
| **ステータス** | アーカイブ | アクティブ |
| **実行方法** | `/ddd:1-plan` + MDファイル | `/parasol:X-xxx` スラッシュコマンド |
| **フェーズ数** | 6フェーズ（Phase 1-6） | 8フェーズ（Phase 0-7） |
| **能力階層** | L1→L2→L3（戦略→戦術→運用） | CL1→CL2→CL3 + BC境界確定 |

---

## ディレクトリ構造

```
parasol/                    # V4ルート（アーカイブ）
├── README.md               # このファイル
├── phases/                 # フェーズ定義
│   ├── README.md
│   ├── phase1-value-analysis/
│   ├── phase2-capability/
│   ├── phase3-domain/
│   ├── phase4-operation/
│   ├── phase5-implementation/
│   └── phase6-validation/
├── bundles/                # 業界別・パターン別バンドル
│   ├── base/
│   ├── industry/
│   └── patterns/
├── commands/               # V4コマンド定義
├── contracts/              # コントラクト定義
├── examples/               # 実装例
├── knowledge/              # 知識ベース
│   ├── database/
│   ├── learnings/
│   └── metrics/
├── patterns/               # 設計パターン
│   ├── capability/
│   ├── domain/
│   ├── implementation/
│   ├── operation/
│   └── value/
└── value-definition/       # 価値定義
```

---

## フェーズ構成

### Phase 1: 価値分析
- Business Nine Dimensionsフレームワーク
- 価値構造の明確化

### Phase 2: 能力設計
- L1 戦略的能力（Strategic Capabilities）
- L2 戦術的能力（Tactical Capabilities）
- L3 運用的能力（Operational Capabilities）

### Phase 3: ドメインモデリング
- 境界コンテキスト（Bounded Contexts）
- エンティティとアグリゲート

### Phase 4: オペレーション設計
- CRUD操作定義
- ワークフロー設計

### Phase 5: 実装生成
- コード自動生成
- テストコード生成

### Phase 6: 検証と最適化
- パフォーマンステスト
- ビジネス価値検証

---

## V5への移行

V4の概念はV5に継承されています：

| V4概念 | V5対応 |
|--------|--------|
| L1-L3能力階層 | CL1-CL3ケイパビリティ |
| Business Nine Dimensions | 価値ストリーム（VS0-VS7） |
| フェーズMD実行 | スラッシュコマンド |

V5を使用するには：
```
/parasol:0-help
```

---

## 関連リンク

- [V5 フレームワーク](/.claude/commands/parasol/)
- [V5 概要](/.claude/commands/parasol/reference/overview-v5.md)
- [V4 リファレンス](/.claude/commands/parasol/reference/v4/)
