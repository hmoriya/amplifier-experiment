---
bundle:
  name: parasol-capability-decomposition
  version: 1.0.0
  description: Capability decomposition patterns for V5 value-driven development
  
includes:
  - bundle: ./v5-event-driven-patterns.md
  - bundle: ./bc-architecture-patterns.md
  
config:
  decomposition_methods:
    - zigzag_pattern
    - value_chain_analysis
    - business_capability_mapping
    - functional_decomposition
    - service_blueprint
---

# Capability Decomposition Patterns

Parasol V5 Phase 3で使用する、価値からケイパビリティへの体系的な分解パターンです。

## 基本概念

### ケイパビリティとは

ケイパビリティ（Capability）は「ビジネスが何をできるか」を表す能力単位です。

```yaml
capability:
  definition: "ビジネスが価値を生み出すために必要な能力"
  characteristics:
    - business_focused: 技術ではなくビジネス視点
    - stable: 技術が変わっても能力は不変
    - measurable: 成熟度や効果を測定可能
    - value_linked: 特定の価値に貢献
```

## 1. ZIGZAG Pattern (推奨)

Phase 3の中核となる分解パターンです。

### パターン概要

```
Value Stream (VS)
    ↓ [展開]
CL1: Activity Areas (活動領域)
    ↓ [詳細化] 
CL2: Business Capabilities (ビジネスケイパビリティ)
    ↓ [実装化]
CL3: Sub-capability + BO (詳細能力 + 業務オペレーション対応)
    ↓ [技術化]
BC Implementation Design
```

### 実装例：ECサイトの24時間配送

```yaml
# Value Stream
VS-001:
  name: "24時間配送の実現"
  target_value: "注文から24時間以内の配送"
  
# CL1: Activity Areas
CL1_activity_areas:
  AA-001:
    name: "注文処理"
    description: "顧客の注文を受け付け、処理する活動"
    
  AA-002:
    name: "在庫管理"
    description: "商品の在庫を最適に管理する活動"
    
  AA-003:
    name: "配送管理"
    description: "商品を迅速に配送する活動"

# CL2: Business Capabilities
CL2_capabilities:
  # 注文処理から展開
  BC-001:
    name: "リアルタイム注文受付"
    parent: AA-001
    maturity_target: 4  # 1-5
    
  BC-002:
    name: "注文優先度判定"
    parent: AA-001
    maturity_target: 3
    
  # 在庫管理から展開
  BC-003:
    name: "在庫可視化"
    parent: AA-002
    maturity_target: 5
    
  BC-004:
    name: "自動補充予測"
    parent: AA-002
    maturity_target: 3
    
  # 配送管理から展開
  BC-005:
    name: "配送ルート最適化"
    parent: AA-003
    maturity_target: 4
    
  BC-006:
    name: "リアルタイム配送追跡"
    parent: AA-003
    maturity_target: 5

# CL3: Business Operations
CL3_operations:
  BO-001:
    name: "注文データ取り込み"
    capability: BC-001
    sla: "99.9% uptime, <100ms response"
    
  BO-002:
    name: "在庫引き当て処理"
    capability: BC-003
    sla: "リアルタイム更新, 在庫精度99%"
    
  BO-003:
    name: "配送指示生成"
    capability: BC-005
    sla: "注文後5分以内に配送指示"
```

## 2. Value Chain Analysis

価値連鎖に基づくケイパビリティ分解。

### プライマリー活動

```yaml
primary_activities:
  inbound_logistics:
    capabilities:
      - 仕入先管理
      - 受入検査
      - 在庫受入
      
  operations:
    capabilities:
      - 商品管理
      - 品質管理
      - プロセス最適化
      
  outbound_logistics:
    capabilities:
      - 注文処理
      - 梱包
      - 配送管理
      
  marketing_sales:
    capabilities:
      - 顧客分析
      - プロモーション管理
      - 価格最適化
      
  service:
    capabilities:
      - カスタマーサポート
      - 返品処理
      - アフターサービス
```

### サポート活動

```yaml
support_activities:
  firm_infrastructure:
    capabilities:
      - 経営管理
      - 法務・コンプライアンス
      - 財務管理
      
  hr_management:
    capabilities:
      - 採用・育成
      - パフォーマンス管理
      - 組織開発
      
  technology_development:
    capabilities:
      - システム開発
      - データ分析基盤
      - イノベーション管理
      
  procurement:
    capabilities:
      - 調達管理
      - サプライヤー評価
      - コスト最適化
```

## 3. Capability Maturity Model

各ケイパビリティの成熟度を定義。

```yaml
maturity_levels:
  level_1:
    name: "初期"
    description: "場当たり的、属人的"
    characteristics:
      - no_standard_process
      - manual_operation
      - reactive_response
      
  level_2:
    name: "管理"
    description: "基本的なプロセスが存在"
    characteristics:
      - documented_process
      - basic_automation
      - planned_activities
      
  level_3:
    name: "確立"
    description: "標準化され、組織全体で実施"
    characteristics:
      - standardized_process
      - cross_functional
      - proactive_management
      
  level_4:
    name: "予測可能"
    description: "測定され、制御されている"
    characteristics:
      - quantitative_management
      - predictive_analytics
      - continuous_monitoring
      
  level_5:
    name: "最適化"
    description: "継続的に改善されている"
    characteristics:
      - continuous_improvement
      - innovation_driven
      - self_optimizing
```

## 4. Capability to Service Mapping

ケイパビリティをサービスに変換するパターン。

### マッピングルール

```typescript
// ケイパビリティからサービスへの変換
interface CapabilityToServiceMapper {
  // 1つのケイパビリティ → 1つのサービス
  directMapping(capability: Capability): Service;
  
  // 複数のケイパビリティ → 1つの統合サービス
  aggregateMapping(capabilities: Capability[]): Service;
  
  // 1つのケイパビリティ → 複数の特化サービス
  decomposeMapping(capability: Capability): Service[];
}

// 実装例
class ServiceMapper implements CapabilityToServiceMapper {
  directMapping(capability: Capability): Service {
    return {
      name: `${capability.name}Service`,
      operations: this.deriveOperations(capability),
      sla: this.defineSLA(capability.maturityTarget),
      api: this.generateAPI(capability)
    };
  }
  
  private deriveOperations(capability: Capability): Operation[] {
    // CRUDベース + ビジネスオペレーション
    const crud = ['Create', 'Read', 'Update', 'Delete'];
    const businessOps = capability.operations || [];
    
    return [
      ...crud.map(op => ({
        name: `${op}${capability.entityName}`,
        type: 'crud'
      })),
      ...businessOps.map(op => ({
        name: op.name,
        type: 'business'
      }))
    ];
  }
}
```

### サービス設計パターン

```yaml
service_patterns:
  # Entity Service (データ中心)
  entity_service:
    example: ProductService
    capabilities:
      - Product Management
    characteristics:
      - crud_operations
      - data_ownership
      - simple_business_rules
      
  # Task Service (プロセス中心)
  task_service:
    example: OrderProcessingService
    capabilities:
      - Order Processing
      - Payment Processing
    characteristics:
      - workflow_orchestration
      - stateless_operations
      - external_integrations
      
  # Utility Service (共通機能)
  utility_service:
    example: NotificationService
    capabilities:
      - Customer Communication
    characteristics:
      - reusable_functions
      - cross_cutting_concerns
      - standardized_interface
```

## 5. Capability Dependencies

ケイパビリティ間の依存関係管理。

```yaml
dependency_types:
  data_dependency:
    description: "データの参照・更新関係"
    example: "在庫管理 → 商品マスタ"
    
  process_dependency:
    description: "処理の順序関係"
    example: "注文受付 → 在庫確認 → 決済処理"
    
  event_dependency:
    description: "イベント通知関係"
    example: "注文確定 → 在庫引当イベント"

dependency_matrix:
  order_processing:
    depends_on:
      - inventory_management: data_dependency
      - payment_processing: process_dependency
      - customer_management: data_dependency
    notifies:
      - shipping_management: event_dependency
      - inventory_management: event_dependency
```

## 6. Implementation with V5 Patterns

V5の軽量パターンでの実装例。

```typescript
// V5スタイル：ケイパビリティベースのサービス
export class InventoryCapabilityService {
  // ビジネスケイパビリティの実装
  async checkAvailability(productId: string, quantity: number): Promise<AvailabilityResult> {
    // シンプルなCRUD操作
    const inventory = await this.repository.getInventory(productId);
    const available = inventory.quantity >= quantity;
    
    // V5: 軽量な通知（イベントソーシングなし）
    if (available) {
      this.notifier.notify({
        type: 'inventory.checked',
        productId,
        requestedQuantity: quantity,
        availableQuantity: inventory.quantity,
        timestamp: new Date()
      });
    }
    
    return { available, currentStock: inventory.quantity };
  }
  
  // ケイパビリティの成熟度向上
  async optimizeInventory(): Promise<OptimizationResult> {
    // 在庫最適化ロジック（ビジネスルール）
    const products = await this.repository.getLowStockProducts();
    const recommendations = this.calculateReorderPoints(products);
    
    // 自動発注の提案（成熟度レベル4の機能）
    return { recommendations, automatedOrders: [] };
  }
}
```

## 7. Capability Governance

ケイパビリティのガバナンス構造。

```yaml
governance:
  ownership:
    business_owner:
      responsibilities:
        - capability_definition
        - success_criteria
        - investment_decisions
        
    technical_owner:
      responsibilities:
        - implementation_approach
        - technology_selection
        - operational_excellence
        
  lifecycle:
    stages:
      - identify: "ケイパビリティの特定"
      - define: "詳細定義と成熟度目標"
      - implement: "サービスとして実装"
      - operate: "運用と監視"
      - optimize: "継続的改善"
      
  metrics:
    business_metrics:
      - capability_coverage  # カバー率
      - maturity_score      # 成熟度スコア
      - value_contribution  # 価値貢献度
      
    technical_metrics:
      - service_availability
      - response_time
      - error_rate
```

## CLI Integration

```bash
# ケイパビリティ分解の実行
parasol capability decompose "24時間配送" \
  --method zigzag \
  --depth CL3 \
  --output ./capabilities/

# ケイパビリティマップの生成
parasol capability map \
  --value-stream VS-001 \
  --format mermaid \
  --show-dependencies

# 成熟度評価
parasol capability assess \
  --current-state \
  --target-state \
  --gap-analysis

# ケイパビリティからサービス生成
parasol capability to-service BC-001 \
  --pattern entity-service \
  --implementation v5-lightweight \
  --generate-contract

# ケイパビリティ依存関係の分析
parasol capability analyze-dependencies \
  --detect-cycles \
  --suggest-boundaries \
  --export graphml
```

## まとめ

Phase 3のケイパビリティ分解は、ビジネス価値を実装可能な単位に変換する重要なステップです：

1. **ZIGZAG Pattern**: V5推奨の体系的分解方法
2. **成熟度モデル**: 各ケイパビリティの目標レベル設定
3. **サービスマッピング**: ケイパビリティの技術的実装
4. **依存関係管理**: ケイパビリティ間の関係性
5. **V5統合**: 軽量パターンでの実装

これにより、価値駆動でありながら実装可能な、バランスの取れたシステム設計が実現できます。