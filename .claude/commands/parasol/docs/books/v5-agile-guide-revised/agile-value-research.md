# アジャイルと価値に関するリサーチ

## アジャイル宣言の本質的な価値志向

### アジャイルマニフェスト（2001年）の再読

**アジャイル宣言の4つの価値**：
1. **Individuals and interactions** over processes and tools  
   （プロセスやツールよりも個人と対話を）
2. **Working software** over comprehensive documentation  
   （包括的なドキュメントよりも動くソフトウェアを）
3. **Customer collaboration** over contract negotiation  
   （契約交渉よりも顧客との協調を）
4. **Responding to change** over following a plan  
   （計画に従うことよりも変化への対応を）

**重要な注釈**：
> "That is, while there is value in the items on the right, we value the items on the left more."
> （右側の事柄にも価値はあるが、左側の事柄により価値を置く）

### アジャイルの12の原則における価値言及

1. **最優先原則**：
   > "Our highest priority is to satisfy the customer through early and continuous delivery of **valuable software**."
   > （顧客満足を最優先し、価値あるソフトウェアを早く継続的に提供する）

2. **価値の継続的デリバリー**：
   > "Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale."
   > （動くソフトウェアを、2-3週間から2-3ヶ月という短い時間間隔でリリースする）

## アジャイル手法における価値の扱い

### Scrum における価値

**スクラムガイド（2020年版）の価値言及**：
- Product Goal: "A commitment to the Product Backlog"
- Sprint Goal: "creates coherence and focus"
- Definition of Done: "creates transparency"

**プロダクトオーナーの責任**：
> "Maximizing the value of the product resulting from the work of the Scrum Team"
> （スクラムチームの作業から生まれるプロダクトの価値を最大化する）

**問題点**：
- 「価値」の定義方法が明示されていない
- 価値の測定方法が規定されていない
- 価値の優先順位付けはPOに一任

### XP（Extreme Programming）における価値

**XPの5つの価値**：
1. Communication（コミュニケーション）
2. Simplicity（シンプリシティ）
3. Feedback（フィードバック）
4. Courage（勇気）
5. Respect（尊重）

**価値に関する実践**：
- Customer Tests（顧客テスト）: 顧客価値の検証
- Small Releases（小規模リリース）: 早期の価値提供
- On-site Customer（顧客同席）: 価値の継続的確認

### Lean Software Development における価値

**7つの原則**：
1. Eliminate Waste（無駄を排除する）
2. Build Quality In（品質を作り込む）
3. Create Knowledge（知識を創造する）
4. Defer Commitment（決定を遅らせる）
5. **Deliver Fast（高速に提供する）** → 価値の早期実現
6. **Respect People（人を尊重する）** → 価値創造の主体
7. **Optimize the Whole（全体を最適化する）** → 価値の流れ全体

**Value Stream Mapping**: 価値の流れを可視化する手法

## 現実のアジャイル実践における価値の課題

### 1. 価値定義の曖昧さ

**現状**：
- 「ユーザーストーリー」が機能要求に堕落
- 「価値」が「機能の完成」と同一視される
- ビジネス価値の定量化が困難

**例**：
```
悪い例：
As a user
I want a search function
So that I can search

良い例（でもまだ不十分）：
As a customer
I want to quickly find products
So that I can complete my purchase faster

V5的な価値定義：
VL1: 購買体験の向上
VL2: 商品発見時間の短縮
VL3: 検索→購入完了時間を10分→3分に短縮
```

### 2. 価値測定の欠如

**問題**：
- ベロシティ（作業量）の測定に偏重
- アウトカム（成果）よりアウトプット（出力）を重視
- 価値実現の事後検証がない

### 3. 価値の断絶

**開発プロセスでの価値の扱い**：
```
Product Backlog → Sprint Planning → Daily Scrum → Sprint Review → Retrospective
    ↓                ↓                 ↓             ↓              ↓
価値？？？      タスク中心      進捗中心     機能デモ中心    プロセス中心
```

## アジャイルの価値志向を強化する動き

### 1. Outcome-Oriented Agile

- OKR（Objectives and Key Results）との統合
- Impact Mapping の活用
- Benefit Hypothesis の明示

### 2. Evidence-Based Management (EBM)

**Scrum.org の価値指標**：
- Current Value (CV): 現在の価値
- Unrealized Value (UV): 未実現の価値  
- Time to Market (T2M): 市場投入時間
- Ability to Innovate (A2I): イノベーション能力

### 3. Lean Startup との融合

- Build-Measure-Learn サイクル
- MVP（Minimum Viable Product）による価値仮説検証
- Pivot or Persevere の意思決定

## 分析結果：アジャイルは本来価値駆動

### 原理的には価値中心

1. アジャイル宣言の第一原則が「価値あるソフトウェア」
2. 顧客満足（＝価値提供）が最優先
3. 継続的な価値デリバリーが前提

### 実践では価値が希薄化

1. 手法やプロセスに注目が集まる
2. 「動くソフトウェア」≠「価値あるソフトウェア」の混同
3. 測定可能な価値定義の欠如

### V5が補完する部分

1. **価値の体系的定義**（VL1→VL2→VL3）
2. **価値トレーサビリティ**の確保
3. **価値測定の組み込み**
4. **価値からの逆算設計**

## 結論：V5はアジャイルの価値志向を具現化

**アジャイル**: 価値提供の理念とプロセス
**Parasol V5**: 価値実現の体系と手法

両者は競合ではなく、相互補完関係：
- アジャイルが「Why（なぜ）」と「How（どのように）」を提供
- V5が「What（何を）」と「How to measure（どう測るか）」を提供

## 文書構成への提言

### 現在の構成の問題点

1. **第1章のタイトル「なぜ価値駆動アジャイルが必要なのか」**
   - アジャイル自体が価値駆動であるべき
   - 「なぜアジャイルで価値が見失われるのか」の方が適切

2. **V5 vs アジャイルの対比構造**
   - 対立関係ではなく補完関係として描くべき
   - 「V5でアジャイルの理想を実現する」という流れ

3. **価値駆動を新しい概念として提示**
   - アジャイルの原点回帰として位置付ける
   - V5は実現手段であることを明確に

### 改訂案の方向性

1. **ストーリーライン**：
   - アジャイルの理想（価値中心）
   - 現実のギャップ（プロセス中心への堕落）
   - V5による原点回帰と具現化

2. **メッセージ**：
   - 「新しい手法」ではなく「本来のアジャイル実現」
   - V5は道具、目的はアジャイルの理想実現

3. **読者への訴求**：
   - アジャイル実践者の悩みに共感
   - 理想と現実のギャップを埋める方法提供