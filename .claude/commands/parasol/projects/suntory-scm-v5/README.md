# サントリー SCMバリューストリーム

Parasol V5 プロジェクト

**対象**: サントリーホールディングス株式会社
**コンテキスト**: SCM（サプライチェーンマネジメント）
**作成日**: 2025-01-15

---

## プロジェクト概要

サントリーグループのサプライチェーンマネジメント領域におけるバリューストリームを構築するプロジェクトです。

### 分析スコープ

- **原材料調達**: 水資源、農産物、包装資材の調達
- **製造・生産**: 飲料製造プロセスの最適化
- **物流・配送**: 製品配送ネットワーク
- **在庫管理**: 適正在庫の維持
- **需要予測**: AIを活用した需要予測
- **サプライヤー管理**: サプライヤーとの協働

---

## クイックスタート

```bash
cd .claude/commands/parasol/projects/suntory-scm-v5

# Phase 1: コンテキスト分析
/parasol:1-context

# Phase 2: 価値定義・VStream設計
/parasol:2-value
```

---

## 進捗確認

```bash
/parasol:project info
/parasol:status
```

---

## プロジェクト構造

```
suntory-scm-v5/
├── parasol.yaml              # プロジェクト設定
├── README.md                 # このファイル
└── outputs/                  # 成果物ディレクトリ
    ├── 1-context/           # Phase 1 成果物
    ├── 2-value/             # Phase 2 成果物
    ├── 3-capabilities/      # Phase 3 成果物
    ├── 4-architecture/      # Phase 4 成果物
    ├── 5-software/          # Phase 5 成果物
    ├── 6-implementation/    # Phase 6 成果物
    └── 7-platform/          # Phase 7 成果物
```

---

## 参考情報

- [サントリーホールディングス](https://www.suntory.co.jp/)
- [サントリーグループ サステナビリティ](https://www.suntory.co.jp/company/csr/)
- [サントリー 水と生きる](https://www.suntory.co.jp/eco/teigen/)

---

**作成**: Parasol V5 プロジェクト
