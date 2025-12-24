# 第1章：なぜ「正しい設計」が失敗するのか

## プロローグ：ある失敗プロジェクトの真実

2023年、あるフィンテック企業で起きた実話です。

技術責任者のAさんは、新しい決済プラットフォームの設計を任されました。彼は業界でも有名なアーキテクトで、DDDの専門家としても知られていました。

6ヶ月後、完成したシステムは技術的には完璧でした：

- **マイクロサービス**: 12個の美しく分離されたサービス
- **イベント駆動**: CQRSとEvent Sourcingの教科書的実装
- **可観測性**: 完全なトレーシングとメトリクス
- **スケーラビリティ**: 理論上は秒間100万トランザクション対応

技術カンファレンスでは賞賛されました。でも...

**1年後、このシステムは廃棄されました。**

なぜでしょうか？

## 技術的正しさの罠

### 罠その1：過剰な一般化

Aさんのチームは「将来の拡張性」を重視しました：

```java
// 「拡張可能な」決済インターフェース
public interface PaymentProcessor<T extends PaymentRequest, 
                                  R extends PaymentResponse,
                                  C extends PaymentContext> {
    R process(T request, C context) throws PaymentException;
}

// 実際の使用例
public class CreditCardProcessor 
    implements PaymentProcessor<CreditCardRequest, 
                                 CreditCardResponse, 
                                 StandardContext> {
    // 実装...
}
```

**問題**: 
- 実際には2種類の決済方法しか必要なかった
- 複雑なジェネリクスがコードの理解を困難に
- 新人エンジニアは実装に2週間かかった（本来なら2日）

### 罠その2：境界の過剰分離

```
決済サービス群：
- payment-api-gateway
- payment-validator
- payment-processor
- payment-state-manager
- payment-notification
- payment-audit
- payment-reconciliation
- payment-reporting
- payment-configuration
- payment-monitoring
- payment-retry-handler
- payment-event-publisher
```

**問題**:
- デプロイに45分（12サービス × 各種環境）
- 1つのバグ修正に平均3つのサービス変更
- 分散トランザクションの複雑性で障害多発

### 罠その3：抽象化の深淵

```java
// 5層の抽象化
Controller → UseCase → DomainService → Repository → DataMapper

// 単純な残高照会が...
@RestController
public class BalanceController {
    @Autowired private BalanceUseCase useCase;
    
    @GetMapping("/balance/{accountId}")
    public BalanceResponse getBalance(@PathVariable String accountId) {
        return useCase.execute(new BalanceQuery(accountId));
    }
}

@Component 
public class BalanceUseCase {
    @Autowired private AccountDomainService domainService;
    
    public BalanceResponse execute(BalanceQuery query) {
        return domainService.getBalance(query.getAccountId());
    }
}

// ... さらに3層続く
```

**問題**:
- 単純なSELECT文が5つのクラスを通過
- デバッグ時に迷子になる新人続出
- パフォーマンス問題の原因特定に苦労

## 失敗の本質：価値の不在

### ユーザーが本当に必要としていたもの

後の調査で判明した事実：

**ユーザーの要求**:
1. 決済が**確実に**処理される（99.9%では不十分）
2. 処理が**速い**（1秒以内）
3. **シンプルな**統合（1日で実装可能）

**実際のシステム**:
1. 分散システムの複雑性で可用性は99.5%
2. マイクロサービス間通信で平均2.5秒
3. 統合に平均2週間

### 価値の定義不在がもたらしたもの

チームは「技術的に正しい」ことに熱中し、最も重要な質問を忘れていました：

> 「このシステムは、誰に、どんな価値を提供するのか？」

## 良い設計への第一歩：価値を問う

### 価値駆動の問いかけ

もしAさんがParasol V5の価値駆動設計を知っていたら、最初にこう問いかけたでしょう：

```
Step 1: 価値の特定
Q: この決済システムで、顧客は何を達成したいのか？
A: ECサイトでの購入を完了したい

Step 2: 価値の深掘り
Q: なぜそれが重要なのか？
A: 購入プロセスでの離脱が売上損失に直結する

Step 3: 測定可能な価値へ
Q: 具体的に何が改善されれば価値となるか？
A: 決済成功率99.99%、処理時間1秒以内、実装1日
```

### 価値から導かれる設計

この価値定義から、全く異なる設計が生まれます：

```
価値: 確実で高速な決済処理
  ↓
設計方針:
- モノリシックな決済コア（信頼性優先）
- 非同期処理は補助的機能のみ
- シンプルなSDKで1日統合
```

## 正しい設計 vs 良い設計

### 「正しい設計」の特徴

1. **技術的な一貫性**: パターンの厳格な適用
2. **理論的な美しさ**: 教科書的な実装
3. **将来の可能性**: あらゆる拡張への対応

### 「良い設計」の特徴

1. **価値の実現**: 定義された価値を確実に提供
2. **適切な複雑さ**: 必要十分な抽象化
3. **進化可能性**: 価値の変化に追従可能

### 判断基準の転換

| 観点 | 正しい設計の問い | 良い設計の問い |
|-----|-----------------|---------------|
| 境界 | Bounded Contextは適切か？ | この境界は価値提供に貢献するか？ |
| 抽象化 | SOLID原則に従っているか？ | この抽象化で開発速度は上がるか？ |
| 技術選定 | 最新のベストプラクティスか？ | 価値実現に最適な技術か？ |

## 良い設計への道筋

### 1. 価値の明確化

まず、誰に何を提供するのかを明確にします：

```
顧客セグメント: 中小ECサイト運営者
提供価値: 簡単・確実・高速な決済機能
成功指標: 
- 統合時間: 1日以内
- 決済成功率: 99.99%
- 処理時間: 1秒以内
```

### 2. 価値からの逆算

価値から必要な要素を逆算します：

```
価値「1日で統合」
  ↓ 必要なもの
- シンプルなAPI（5個以下）
- 分かりやすいエラーメッセージ
- コピペで動くサンプルコード
  ↓ 設計判断
- REST API（GraphQLは不要）
- 同期処理メイン
- モノリシックな実装
```

### 3. トレードオフの受容

完璧を求めず、価値に基づいてトレードオフします：

```
採用:
✓ シンプルさ（価値：簡単な統合）
✓ 信頼性（価値：確実な決済）
✓ 性能（価値：高速処理）

犠牲:
✗ 拡張性の一部
✗ 技術的な先進性
✗ 理論的な美しさ
```

## まとめ：設計の新しい評価軸

本章で見てきたように、「技術的に正しい設計」は必ずしも「良い設計」ではありません。

**良い設計とは**：
- 明確な価値を実現する設計
- 適切な複雑さを持つ設計
- 進化可能な設計

**そのために必要なこと**：
1. 価値の明確な定義
2. 価値からの逆算思考
3. 適切なトレードオフ

次章では、Parasol V5が提示する「良い設計」の具体的な定義と、それを実現するための体系的アプローチを詳しく見ていきます。

技術的正しさという呪縛から解放され、真に価値ある設計を生み出す旅が、ここから始まります。