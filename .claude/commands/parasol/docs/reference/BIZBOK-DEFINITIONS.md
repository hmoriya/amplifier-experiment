# BizBOK 定義・概念 参照資料

**バリューストリーム、ケイパビリティ、マッピングに関する公開資料からの抽出**

**最終更新**: 2025-01-08
**出典**: Business Architecture Guild 公開資料

---

## 1. Value Stream（バリューストリーム）

### 定義

| 出典 | 定義（原文） | 日本語訳 |
|------|-------------|----------|
| **BizBOK** | "An end-to-end collection of activities that creates a result for a customer" | 顧客に結果を生み出す、エンド・ツー・エンドの活動の集まり |
| **Capstera** | "An end-to-end flow of activities depicted from a stakeholder perspective" | ステークホルダー視点で描かれた、エンド・ツー・エンドの活動の流れ |

### 特徴

- ステークホルダー（内部または外部）によってトリガーされる
- ステークホルダーの満足が達成された時点で終了する
- 各ステージで価値が蓄積される
- 左から右へ進行するステージの連続として表現される

> "A value stream is initiated by an internal or external stakeholder and ends when stakeholder gratification is achieved. Value is accrued at each stage."
> — BizBOK

---

## 2. Value Stream Stage（バリューストリームステージ）

### 定義

| 出典 | 定義 |
|------|------|
| **BizBOK Metamodel** | Value Stream内の子コンポーネント。価値提供プロセスの離散的なステップを表す |

### 構成要素（BizBOK Metamodel / Ardoq実装より）

| 要素 | 説明 |
|------|------|
| **Entrance Criteria** | ステージをトリガーする開始条件 |
| **Exit Criteria** | 完了を示す終了条件 |
| **Quality Metrics** | 5次元の品質指標 |

### 品質指標（5次元）

1. **Quality and Correctness** - 品質と正確性
2. **Efficiency and Timeliness** - 効率性と適時性
3. **Consistency and Standardization** - 一貫性と標準化
4. **Availability to Stakeholder Community** - ステークホルダーへの可用性
5. **Performance against Expectations** - 期待に対するパフォーマンス

---

## 3. Capability（ケイパビリティ）

### 定義

| 出典 | 定義（原文） | 日本語訳 |
|------|-------------|----------|
| **BizBOK** | Organizational ability to perform business functions | ビジネス機能を実行する組織的能力 |

### 評価軸（BizBOK Metamodel / Ardoq実装より）

| 評価軸 | スケール | 説明 |
|--------|----------|------|
| **Criticality** | 1-5 | 重要度・影響度 |
| **Quality** | 0-5 | 現在の成熟度 |

### 特徴

- 組織が「何をするか（What）」を表す
- 比較的安定している（他のビジネス側面と比較して）
- 階層的に分解可能

---

## 4. マッピング関係

### BizBOK Metamodelにおける関係

```
┌─────────────┐
│ Stakeholder │
└──────┬──────┘
       │ triggers
       ▼
┌─────────────┐     consists of    ┌───────────────────┐
│Value Stream │────────────────────►│ Value Stream Stage│
└─────────────┘                    └─────────┬─────────┘
                                             │
                                             │ enables
                                             │
┌─────────────┐     achieve        ┌────────▼────────┐
│   Outcome   │◄───────────────────│   Capability    │
└─────────────┘                    └────────┬────────┘
                                            │
                                            │ use / modify
                                            ▼
                                   ┌─────────────────┐
                                   │   Information   │
                                   └─────────────────┘
```

### 関係の定義

| 関係 | 動詞 | 説明 |
|------|------|------|
| **Capability → Value Stream Stage** | **enables** | ケイパビリティがステージを有効化する |
| **Capability → Outcome** | **achieves** | ケイパビリティが成果を達成する |
| **Capability → Information** | **uses / modifies** | ケイパビリティが情報を使用/変更する |
| **Stakeholder → Value Stream** | **triggers** | ステークホルダーがVSをトリガーする |

---

## 5. ケイパビリティの重複許容（重要）

### BizBOKの明示的記述

> "Capabilities enable stages within various value streams and require certain information."
> — BizBOK

> "Value streams enable a wide range of capabilities and capabilities can be mapped to each stage of the value stream. **Many capabilities map to multiple value streams.**"
> — BizBOK

> "A capability can be reused many times **within** and **across** value streams."
> — BizBOK Section 2.4（Biz Arch Mastery解説より）

### 解釈

| 表現 | 意味 |
|------|------|
| **within** value streams | 同一バリューストリーム内で複数ステージに出現可能 |
| **across** value streams | 異なるバリューストリーム間で再利用可能 |
| **Many capabilities map to multiple** | 多対多のマッピング関係 |

---

## 6. 4つのコアドメイン

BizBOKでは、以下の4つをビジネスアーキテクチャの基盤（Core Domains）として定義:

```
┌─────────────────────────────────────────────────────────┐
│                    Core Domains                         │
├─────────────┬─────────────┬─────────────┬──────────────┤
│ Capability  │Value Stream │ Information │ Organization │
│  (What)     │   (How)     │   (With)    │    (Who)     │
└─────────────┴─────────────┴─────────────┴──────────────┘
```

> "Organization, capability, value streams, and information comprise the foundation of the business architecture. These four 'core' domains are considered foundational because they are **relatively stable** compared to other aspects of the business."
> — BizBOK

---

## 7. クロスマッピングの目的

### BizBOKが示すクロスマッピングの用途

1. **戦略影響分析** - Strategy impact analysis
2. **イニシアチブ・投資範囲の決定** - Initiative and investment scope determination
3. **ビジネスデザイン** - Business design efforts
4. **要件定義とソリューション展開** - Requirements definition and solution deployment

### ヒートマッピング

ケイパビリティの品質をバリューストリームステージに対してヒートマップで可視化:

- **Red**: 現状と必要状態の間に重大なギャップ
- **Yellow**: 若干の調整が必要
- **Green**: 十分なパフォーマンス

---

## 参考文献

### 一次資料（公開）

- [BizBOK Introduction v10](https://cdn.ymaws.com/www.businessarchitectureguild.org/resource/resmgr/bizbok_10/introduction_v10_final.pdf) - Business Architecture Guild
- [The Real Tie that Binds](https://cdn.ymaws.com/www.businessarchitectureguild.org/resource/resmgr/public_resources/TiethatBinds.pdf) - William Ulrich & Jim Rhyne
- [Similar Yet Different: Value Streams and Business Processes](https://cdn.ymaws.com/www.businessarchitectureguild.org/resource/resmgr/public_resources/bpm_paper_final_dec2019.pdf) - Business Architecture Guild
- [Business Architecture Metamodel](https://cdn.ymaws.com/www.businessarchitectureguild.org/resource/resmgr/whitepapers/business_architecture_metamo.pdf) - Business Architecture Guild

### 二次資料（解説）

- [Ardoq - BizBOK Metamodel](https://help.ardoq.com/en/articles/43932-business-architecture-guild-metamodel-and-industry-reference-models-in-ardoq) - Metamodel実装の詳細
- [Capstera - Business Architecture Value Streams](https://www.capstera.com/business-architecture-value-streams/) - バリューストリームの解説
- [Biz Arch Mastery - The Value Mindset](https://bizarchmastery.com/straighttalk/value-mindset-demystifying-business-architecture-value-stream) - BizBOK Section 2.4の解説

---

## 注意事項

- BizBOK Guide全文（Section 2.4含む）は[Business Architecture Guild](https://www.businessarchitectureguild.org/)会員限定
- 本ドキュメントは公開資料からの抽出であり、会員限定コンテンツは含まれていない
- 最新バージョン（v14）の内容とは異なる可能性がある

---

## 関連ドキュメント

- [TOGAF-BIZBOK-COMPARISON.md](./TOGAF-BIZBOK-COMPARISON.md) - TOGAF/BizBOKとParasol V5の比較
- [TOGAF-G178-VALUE-STREAMS.md](./TOGAF-G178-VALUE-STREAMS.md) - TOGAF G178原文
- [TOGAF-G178-VALUE-STREAMS-JA.md](./TOGAF-G178-VALUE-STREAMS-JA.md) - TOGAF G178日本語訳

---

**Parasol V5 - 理論的基盤の理解のための参照資料**
