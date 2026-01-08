# BizBOK公式見解：ケイパビリティマップの位置づけ

**バージョン**: 1.0
**最終更新**: 2025-01-08
**出典**: BIZBOK™ Guide, The Real Tie that Binds (William Ulrich & Jim Rhyne)

---

## 核心的問い

> **「ケイパビリティマップは、ビジネスアーキテクチャ図として成立するか？」**

---

## BizBOKの公式見解：単体では不十分

### 公式引用①：BIZBOK™ Section 2.8

> **「ビジネスケイパビリティだけでは、ビジネスが短期的および長期的な問題や課題に完全に対処できるようにするには不十分です。**
>
> **ステークホルダーのエンゲージメントの明確なビューや、ステークホルダー価値がどのように達成されるかのビジョンがない場合、ビジネスケイパビリティの展開は困難になる可能性があります。」**

### 公式引用②：The Real Tie that Binds

> **「ケイパビリティ単体はネットワークを表しません。**
>
> **ネットワークは、ケイパビリティが互いに、組織に、そしてバリューストリームにどのように関連するかを示す必要があります。」**
>
> — William Ulrich & Jim Rhyne（Business Architecture Guild創設者）

### 公式引用③：BIZBOK™ Metamodel Guide

> **「最も重要なクロスマッピングブループリントの1つは、バリューストリーム/ケイパビリティ クロスマッピングです。このブループリントは、バリューストリームの各ステージで価値提供を可能にする特定のケイパビリティを特定します。」**

---

## BizBOKが定義する「ビジネスアーキテクチャ」

### 4コアドメインの統合

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ビジネスアーキテクチャ = 4コアドメインの統合                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌───────────────┐    ┌──────────────┐    ┌───────────────┐              │
│   │ Value Stream  │◄──▶│  Capability  │◄──▶│  Information  │              │
│   └───────────────┘    └──────┬───────┘    └───────────────┘              │
│                               │                                             │
│                               ▼                                             │
│                        ┌──────────────┐                                     │
│                        │ Organization │                                     │
│                        └──────────────┘                                     │
│                                                                              │
│   ★ 4つが揃って初めて「ビジネスアーキテクチャ」                            │
│   ★ Capability Map単体は「ビジネスケイパビリティアーキテクチャ（BCA）」    │
│      → BizBOKはBCAを「不完全」と明言                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 各ドメインの役割

| ドメイン | 役割 | 答える問い |
|----------|------|-----------|
| **Value Stream** | ステークホルダー価値提供のエンド・ツー・エンド視点 | 「どう価値を届けるか？」 |
| **Capability** | ビジネスが行うこと - 基本的な構成要素 | 「何ができるか？」 |
| **Information** | ビジネス用語とセマンティクスの表現 | 「何を扱うか？」 |
| **Organization** | 組織構造とビジネスユニット | 「誰がやるか？」 |

---

## ケイパビリティマップ単体の評価

### BizBOKによる評価

| 評価観点 | BizBOKの見解 |
|----------|--------------|
| **ビジネスアーキテクチャか？** | ❌ **不完全**（4ドメイン中1つのみ） |
| **有用な成果物か？** | ✅ 有用だが単体では不十分 |
| **必要な追加要素** | Value Stream Map + Cross-Mapping |
| **最低限の組み合わせ** | Capability Map + Value Stream Map + Cross-Mapping |

### ケイパビリティマップ単体の限界

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Capability Map単体で分かること / 分からないこと                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  【分かること】                                                              │
│  ✅ 組織が持つ能力の一覧                                                    │
│  ✅ 能力の階層構造（L1/L2/L3）                                              │
│  ✅ 能力間の構造的関係                                                      │
│                                                                              │
│  【分からないこと】                                                          │
│  ❌ その能力がどう価値を生むか                                              │
│  ❌ どのステークホルダーに価値を届けるか                                    │
│  ❌ どの文脈（バリューストリーム）で使われるか                              │
│  ❌ どの能力が価値提供のボトルネックか                                      │
│  ❌ 投資の優先順位をどう決めるか                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 最重要ブループリント：Cross-Mapping

### Value Stream / Capability Cross-Mapping Blueprint

BizBOKが「最も重要なブループリントの1つ」と位置づける成果物：

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        Acquire Loan Value Stream                                  │
├────────────────┬────────────────┬────────────────┬────────────────┬──────────────┤
│    Validate    │    Approve     │   Issue Loan   │ Issue Second   │   Onboard    │
│   Application  │      Loan      │                │   Approval     │  Applicant   │
├────────────────┼────────────────┼────────────────┼────────────────┼──────────────┤
│Account Pipeline│Customer Info   │Account         │Account Info    │Account Info  │
│  Management    │  Management    │ Structuring    │  Management    │   Update     │
├────────────────┼────────────────┼────────────────┼────────────────┼──────────────┤
│Account Payments│Account Info    │Account Info    │Work Queue,Case │Work Queue,   │
│  Management    │  Management    │  Management    │File, Routing   │Case File,    │
│                │                │                │  Management    │Routing Mgmt  │
├────────────────┼────────────────┼────────────────┼────────────────┼──────────────┤
│                │Work Queue,Case │Work Queue,Case │Acceptance      │Acceptance    │
│                │File, Routing   │File, Routing   │ Notification   │ Notification │
│                │  Management    │  Management    │                │              │
└────────────────┴────────────────┴────────────────┴────────────────┴──────────────┘

★ 同一ケイパビリティが複数ステージに出現（例：Account Info Management）
★ これにより「能力がどう価値を生むか」が可視化される
```

### Cross-Mappingで得られる洞察

| 洞察 | 説明 |
|------|------|
| **価値貢献度** | どのケイパビリティがどれだけの価値ステージに貢献しているか |
| **ボトルネック** | 多くのステージに関わるケイパビリティの品質が低い場合、全体に影響 |
| **投資優先度** | 価値貢献度の高いケイパビリティへの投資を優先できる |
| **改善インパクト** | どのケイパビリティを改善すれば最大の効果があるか |

---

## BizBOKの核心メッセージ

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  「これらのシナリオ（Value Stream）がない場合、                             │
│   ケイパビリティをどのように改善、展開、または活用するかの決定は欠如し、    │
│   ステークホルダー価値提供に投資を集中する能力も失われます。」              │
│                                                                              │
│                        — The Real Tie that Binds                             │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  【要約】                                                                    │
│  ケイパビリティは「何ができるか」を示すが、                                 │
│  「どう価値を提供するか」はバリューストリームなしには分からない             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 実務上の指針

### ビジネスアーキテクチャ成果物の成熟度

| レベル | 成果物 | BizBOKによる評価 |
|--------|--------|------------------|
| **Level 1** | Capability Map単体 | ❌ 不完全（BCA） |
| **Level 2** | Capability Map + Value Stream Map | △ 最低限 |
| **Level 3** | Level 2 + Cross-Mapping | ✅ 基本的なBA |
| **Level 4** | Level 3 + Information Map | ✅✅ 標準的なBA |
| **Level 5** | Level 4 + Organization Map | ✅✅✅ 完全なBA |

### 推奨される構築順序

```
1. Value Stream Map（価値の流れを先に定義）
     ↓
2. Capability Map（能力を定義）
     ↓
3. Cross-Mapping（VSとCapの関係を定義）★最重要
     ↓
4. Information Map（情報の流れを定義）
     ↓
5. Organization Map（組織との対応を定義）
```

---

## Parasol V5への適用

### V5の設計はBizBOKの見解と整合

| BizBOKの主張 | Parasol V5での実現 |
|--------------|-------------------|
| 「Capability単体では不十分」 | VS起点の設計（Phase 2 → Phase 3） |
| 「Cross-Mappingが最重要」 | VSスイムレーン方式（VS内でCL分解） |
| 「4コアドメインの統合」 | Phase 1-7で全ドメインをカバー |

### V5とBizBOKの相違点

| 観点 | BizBOK | Parasol V5 |
|------|--------|------------|
| **Cross-Mapping方式** | 多対多（同一Capが複数VSに） | スイムレーン（VS内でCL分解） |
| **設計思想** | 組織横断のCap再利用 | DX/サービス設計への直結 |

---

## まとめ

### BizBOKの公式回答

| 質問 | BizBOKの回答 |
|------|-------------|
| **Capability Mapはビジネスアーキテクチャ図か？** | **❌ 単体ではNo** |
| **何が足りないか？** | Value Stream視点（価値がどう提供されるか） |
| **最小構成は？** | Capability Map + Value Stream Map + Cross-Mapping |
| **理想構成は？** | 4コアドメイン（Cap + VS + Info + Org）全て |

### 核心

> **ケイパビリティマップは「ビジネスアーキテクチャの重要な構成要素」であるが、単体では「ビジネスアーキテクチャ」として成立しない。バリューストリームとのクロスマッピングが不可欠。**

---

## 参考文献

- **BIZBOK™ Guide** - Business Architecture Guild®
  - Section 2.4: Value Streams
  - Section 2.8: Capability単体の限界に関する記述
- **The Real Tie that Binds** - William Ulrich & Jim Rhyne
  - [PDF](https://cdn.ymaws.com/www.businessarchitectureguild.org/resource/resmgr/public_resources/TiethatBinds.pdf)
- **Business Architecture Metamodel Guide V3.0** - Business Architecture Guild®

---

## 関連ドキュメント

- [BIZBOK-TIE-THAT-BINDS-JA.md](./BIZBOK-TIE-THAT-BINDS-JA.md) - The Real Tie that Binds 全訳
- [BIZBOK-METAMODEL-GUIDE-JA.md](./BIZBOK-METAMODEL-GUIDE-JA.md) - メタモデルガイド
- [V5-BIZBOK-COMPARISON.md](./V5-BIZBOK-COMPARISON.md) - V5とBizBOKの詳細比較
- [TOGAF-BIZBOK-COMPARISON.md](./TOGAF-BIZBOK-COMPARISON.md) - TOGAF/BizBOK比較

---

**Parasol V5 - BizBOK理論基盤に基づく価値駆動設計フレームワーク**
