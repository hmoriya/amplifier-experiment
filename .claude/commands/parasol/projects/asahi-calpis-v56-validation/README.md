# Parasol V5.6 検証プロジェクト: アサヒグループ → カルピス

**目的**: ホールディングカンパニーからブランドレベルへの価値分解でV5.6新機能を検証

## プロジェクト構造

```
アサヒグループホールディングス（持株会社）
    │
    ├── アサヒビール（事業会社）
    ├── アサヒ飲料（事業会社）← 今回のスコープ
    │       │
    │       ├── カルピス（ブランド）← 価値分解対象
    │       ├── 三ツ矢サイダー
    │       └── ワンダ
    │
    └── アサヒグループ食品
```

## V5.6 検証ポイント

| フェーズ | V5.5まで | V5.6新機能 |
|---------|---------|-----------|
| Phase 2 | VL1→VL2→VL3 | **VC分析**、3軸価値分解、VS-VCマトリクス |
| Phase 3 | CL1→CL2→CL3 | **OS定義**、VC-Cap対応、**ステージ依存TVDC** |

## 成果物

- `phase1-context.yaml` - 組織コンテキスト
- `phase2-value-definition.yaml` - 価値定義（VL1→VL3）
- `phase2-vc-analysis.yaml` - VC分析（V5.6新）
- `phase3-value-streams.yaml` - バリューストリーム設計
- `phase3-operational-stages.yaml` - OS定義（V5.6新）
- `phase3-stage-tvdc.yaml` - ステージ依存TVDC（V5.6新）
- `V56-VALIDATION-REPORT.md` - 検証レポート
