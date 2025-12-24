# 「価値駆動設計」実例・サンプルコードカタログ

## 実例カテゴリ

### 1. 失敗事例（アンチパターン）

#### 事例1-1: 過剰マイクロサービス化の罠
- **業界**: フィンテック
- **状況**: 決済システムを12のマイクロサービスに分割
- **結果**: 複雑性爆発、運用コスト3倍、開発速度1/4
- **教訓**: 境界は価値から導出すべき

#### 事例1-2: 抽象化の迷宮
- **業界**: EC
- **状況**: 5層のレイヤードアーキテクチャ
- **結果**: 単純な機能追加に2週間
- **教訓**: 適切な抽象度の重要性

#### 事例1-3: 技術駆動の失敗
- **業界**: ヘルスケア
- **状況**: 最新技術（GraphQL、K8s、Kafka）の全採用
- **結果**: 運用できる人材不在で頓挫
- **教訓**: 組織の成熟度を考慮

### 2. 成功事例（ベストプラクティス）

#### 事例2-1: 価値からの逆算設計
- **業界**: 物流
- **状況**: リアルタイム配送追跡システム
- **アプローチ**: 顧客価値「不安の解消」から設計
- **結果**: シンプルな3API、顧客満足度40%向上

#### 事例2-2: 段階的な複雑性導入
- **業界**: 製造業
- **状況**: IoTセンサーデータ分析基盤
- **アプローチ**: モノリスから始めて段階的分離
- **結果**: 6ヶ月で本番稼働、その後スケール

#### 事例2-3: トレードオフの明示的管理
- **業界**: 金融
- **状況**: 取引システムのリニューアル
- **アプローチ**: 一貫性>性能>拡張性の優先順位
- **結果**: 明確な判断基準で迅速な意思決定

### 3. 変革事例（Before/After）

#### 事例3-1: ECサイトのレコメンドエンジン

**Before（技術駆動）**:
```
問題：
- 機械学習エンジニアが最新アルゴリズムを実装
- 精度は高いが、結果が出るまで5秒
- 複雑すぎて他のエンジニアがメンテ不可

設計：
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Data Lake   │────→│ ML Pipeline  │────→│ Serving API │
└─────────────┘     └──────────────┘     └─────────────┘
       ↓                    ↓                     ↓
  (100TB規模)         (GPUクラスタ)         (リアルタイム推論)
```

**After（価値駆動）**:
```
価値定義：
VL1: 買い物体験の向上
VL2: 関連商品の素早い発見
VL3: 1秒以内に3つの関連商品表示

設計：
┌─────────────┐     ┌──────────────┐
│ Product DB  │────→│ Simple Rules │────→ [Results]
└─────────────┘     └──────────────┘
                          ↓
                    (同カテゴリ商品
                     ＋購買履歴)

結果：
- レスポンス: 5秒 → 200ms
- 実装期間: 3ヶ月 → 1週間
- 売上影響: +15%（十分な成果）
```

## サンプルコード集

### 1. 価値定義の具体例

```yaml
# value-definition.yml
VL1_顧客価値:
  statement: "安心して買い物ができる"
  stakeholder: "ECサイト利用者"
  
VL2_価値要素:
  - id: VL2-1
    name: "商品の信頼性"
    description: "商品が期待通りであること"
  - id: VL2-2  
    name: "取引の安全性"
    description: "決済や個人情報が守られること"
  - id: VL2-3
    name: "問題解決の迅速性"
    description: "トラブル時にすぐ対応してもらえること"

VL3_測定可能価値:
  - id: VL3-1
    parent: VL2-1
    metric: "レビュー評価4.0以上の商品のみ表示"
    target: "95%以上"
  - id: VL3-2
    parent: VL2-2
    metric: "PCI-DSS準拠の決済システム"
    target: "100%準拠"
  - id: VL3-3
    parent: VL2-3
    metric: "カスタマーサポート初回応答時間"
    target: "1時間以内"
```

### 2. ケイパビリティ設計の例

```java
// 価値から導出されたケイパビリティ
public interface ProductReliabilityCapability {
    /**
     * VL3-1: レビュー評価4.0以上の商品のみ表示
     */
    List<Product> getReliableProducts(Category category);
    
    /**
     * 関連する品質指標を提供
     */
    ReliabilityMetrics calculateMetrics(Product product);
}

// 実装（シンプルさ優先）
@Service
public class SimpleProductReliability 
    implements ProductReliabilityCapability {
    
    private static final double RELIABILITY_THRESHOLD = 4.0;
    
    @Override
    public List<Product> getReliableProducts(Category category) {
        return productRepository
            .findByCategory(category)
            .stream()
            .filter(p -> p.getAverageRating() >= RELIABILITY_THRESHOLD)
            .filter(p -> p.getReviewCount() >= 10) // 統計的信頼性
            .collect(Collectors.toList());
    }
}
```

### 3. トレードオフ管理の実装

```python
# tradeoff_analyzer.py
class DesignTradeoffAnalyzer:
    """設計トレードオフを可視化し、意思決定を支援"""
    
    def __init__(self):
        self.criteria = {
            '性能': {'weight': 0.3, 'score': 0},
            '保守性': {'weight': 0.4, 'score': 0},
            '拡張性': {'weight': 0.2, 'score': 0},
            'コスト': {'weight': 0.1, 'score': 0}
        }
    
    def evaluate_option(self, option_name, scores):
        """各選択肢を評価"""
        total_score = 0
        for criterion, score in scores.items():
            weighted = score * self.criteria[criterion]['weight']
            total_score += weighted
            
        return {
            'option': option_name,
            'total_score': total_score,
            'breakdown': scores
        }
    
# 使用例
analyzer = DesignTradeoffAnalyzer()

monolith = analyzer.evaluate_option('モノリス', {
    '性能': 9,
    '保守性': 7,
    '拡張性': 4,
    'コスト': 9
})

microservices = analyzer.evaluate_option('マイクロサービス', {
    '性能': 7,
    '保守性': 5,
    '拡張性': 9,
    'コスト': 3
})
```

### 4. 進化可能な設計パターン

```typescript
// 価値の変化に適応可能な設計
interface ValueProvider<T> {
    getCurrentValue(): T;
    subscribeToChanges(callback: (newValue: T) => void): void;
}

// 実装例：配送時間の価値が変化するケース
class DeliveryTimeValue implements ValueProvider<DeliveryTimeTarget> {
    private current: DeliveryTimeTarget = {
        standard: 48, // 48時間
        express: 24   // 24時間
    };
    
    private subscribers: Array<(value: DeliveryTimeTarget) => void> = [];
    
    getCurrentValue(): DeliveryTimeTarget {
        return this.current;
    }
    
    updateValue(newTarget: DeliveryTimeTarget): void {
        this.current = newTarget;
        // すべての依存コンポーネントに通知
        this.subscribers.forEach(callback => callback(newTarget));
    }
}

// 価値の変化に自動適応するサービス
class DeliveryService {
    constructor(private valueProvider: ValueProvider<DeliveryTimeTarget>) {
        valueProvider.subscribeToChanges(this.onValueChange.bind(this));
    }
    
    private onValueChange(newTarget: DeliveryTimeTarget): void {
        // 新しい価値目標に基づいてサービスを再構成
        this.reconfigureRouting(newTarget);
        this.adjustCapacity(newTarget);
    }
}
```

### 5. 設計判断の文書化

```markdown
# 設計決定記録 (ADR-001)

## ステータス
承認済み (2024-03-15)

## コンテキスト
ECサイトの商品検索機能において、以下の価値を実現する必要がある：
- VL3-1: 検索結果表示まで1秒以内
- VL3-2: 関連度の高い商品を上位表示
- VL3-3: 在庫ありの商品を優先

## 決定
Elasticsearchを使用したシンプルな全文検索を採用する。

## 根拠
1. **価値実現性**: 1秒以内のレスポンスを確実に達成
2. **実装容易性**: 2週間で本番投入可能
3. **運用実績**: チームに経験者が3名

## 却下した選択肢
1. **自前実装**: 開発期間6ヶ月は価値実現を遅らせる
2. **AIベース検索**: 精度は高いが、レスポンス要件を満たせない
3. **GraphDBベース**: 関連性は表現できるが、チームスキル不足

## 影響
- ポジティブ: 素早い価値実現、安定運用
- ネガティブ: 高度な検索機能は将来課題

## トレードオフ
速度と実装容易性を優先し、高度な機能は段階的に追加する。
```

## 業界別設計パターン例

### 製造業向け
- リアルタイムとバッチの使い分け
- エッジコンピューティングとの連携
- 品質トレーサビリティの実装

### 金融業向け
- イベントソーシングによる監査証跡
- 分散トランザクションの管理
- リスク計算の並列化

### ヘルスケア向け
- PHI（個人健康情報）の適切な分離
- 医療機器との安全な連携
- 規制要件のシステムへの反映

## 利用ガイドライン

1. **実例の選定基準**
   - 実際のプロジェクトに基づく（守秘義務に配慮）
   - 成功/失敗の要因が明確
   - 読者が共感できる規模感

2. **コードの提示方針**
   - 本質を示す最小限のコード
   - 実行可能なレベルの具体性
   - 言語に依存しない概念の説明

3. **図表の活用**
   - Before/Afterの視覚的比較
   - トレードオフの可視化
   - アーキテクチャの進化過程