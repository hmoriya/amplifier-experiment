---
bundle:
  name: parasol-regeneratable-modules
  version: 1.0.0
  description: Contract-driven regeneratable module system for true modularity
  
includes:
  - bundle: ./bc-architecture-patterns.md
  
config:
  regeneration:
    trigger_on:
      - contract_change
      - architecture_pattern_change
      - dependency_update
      - requirement_change
      
    preserve:
      - business_logic
      - custom_implementations
      - test_data
      - configuration
      
    regenerate:
      - infrastructure_code
      - api_contracts
      - database_schemas
      - integration_adapters
---

# Regeneratable Modules System

契約ベースでモジュールを自動生成・再生成する「真のモジュラー」システムです。

## コンセプト：Code as Data, Contracts as Source of Truth

### 従来のアプローチ
```
要求 → 手動コーディング → テスト → デプロイ
↓ 要求変更
修正作業 → 影響範囲調査 → 手動更新 → 再テスト
```

### 再生成可能アプローチ
```
要求 → 契約定義 → 自動生成 → テスト → デプロイ  
↓ 要求変更
契約更新 → 自動再生成 → 差分テスト → デプロイ
```

## 1. Module Contract Definition Language

### 基本契約構造

```yaml
# contracts/modules/product-management.module.yaml
module:
  name: ProductManagement
  version: "1.2.0"
  description: 商品情報の管理と価格設定
  
  architecture:
    pattern: hexagonal
    layers:
      - domain
      - application  
      - adapters
      
  domain:
    aggregates:
      Product:
        root_entity: Product
        entities:
          - Product
          - ProductVariant
        value_objects:
          - ProductId
          - SKU
          - Price
          - ProductName
        invariants:
          - "price > 0"
          - "name.length > 0"
          - "variants.size <= 100"
          
    events:
      - ProductCreated
      - ProductUpdated  
      - PriceChanged
      - ProductDiscontinued
      
  use_cases:
    CreateProduct:
      input:
        name: string
        category_id: string
        price: Money
      output:
        product_id: ProductId
      events: [ProductCreated]
      
    UpdatePrice:
      input:
        product_id: ProductId
        new_price: Money
        reason: string
      output:
        success: boolean
      events: [PriceChanged]
      
  adapters:
    primary:
      rest_api:
        base_path: "/api/v1/products"
        endpoints:
          - POST /products
          - PUT /products/{id}/price
          - GET /products/{id}
          
      graphql_api:
        types:
          - Product
          - ProductInput
        queries:
          - product(id: ID!): Product
        mutations:
          - createProduct(input: ProductInput!): Product
          
    secondary:
      repository:
        interface: ProductRepository
        methods:
          - findById(id: ProductId): Product?
          - save(product: Product): void
          
      event_publisher:
        interface: EventPublisher
        events: domain.events
        
  variants:
    databases:
      postgresql:
        schema: |
          CREATE TABLE products (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP NOT NULL
          );
          
      mongodb:
        collections:
          products:
            schema:
              bsonType: object
              required: [name, price]
              
    frontends:
      react:
        components:
          - ProductList
          - ProductDetail
          - ProductForm
        hooks:
          - useProducts
          - useProductMutations
          
      vue:
        components:
          - ProductList.vue
          - ProductDetail.vue
          - ProductForm.vue
        composables:
          - useProducts
          - useProductMutations
```

## 2. Code Generation Templates

### Template Engine Architecture

```typescript
// modules/code-generator/template-engine.ts
interface CodeTemplate {
  pattern: string;      // glob pattern for files
  engine: 'handlebars' | 'jinja2' | 'mustache';
  variables: Record<string, any>;
  conditions?: string[]; // when to apply template
}

interface ModuleGenerator {
  generate(contract: ModuleContract, variant: Variant): GeneratedModule;
  regenerate(contract: ModuleContract, existing: ExistingModule): RegeneratedModule;
  preserve(existing: ExistingModule): PreservedCode;
}
```

### Domain Layer Templates

```handlebars
{{!-- templates/domain/entity.ts.hbs --}}
// Generated from {{contract.name}} module contract v{{contract.version}}
// DO NOT MODIFY - This file is auto-generated

import { DomainEvent } from '../../../shared/domain/domain-event';
{{#each imports}}
import { {{this}} } from '../{{this.path}}';
{{/each}}

export class {{entity.name}} {
  {{#each entity.properties}}
  private {{name}}: {{type}};
  {{/each}}
  
  constructor(
    {{#each entity.constructor_params}}
    private readonly {{name}}: {{type}},
    {{/each}}
  ) {
    {{#each entity.invariants}}
    this.enforceInvariant("{{condition}}", {{check}});
    {{/each}}
  }
  
  {{#each entity.methods}}
  {{name}}({{#each params}}{{name}}: {{type}}{{#unless @last}}, {{/unless}}{{/each}}): {{return_type}} {
    {{#if generates_events}}
    const events: DomainEvent[] = [];
    {{/if}}
    
    // Business logic placeholder - PRESERVE on regeneration
    // CUSTOM_LOGIC_START:{{../entity.name}}.{{name}}
    {{#if has_custom_logic}}
    {{{custom_logic}}}
    {{else}}
    throw new Error('Business logic not implemented');
    {{/if}}
    // CUSTOM_LOGIC_END:{{../entity.name}}.{{name}}
    
    {{#if generates_events}}
    events.push(new {{event_name}}(this.{{id_field}}, /* event data */));
    return events;
    {{/if}}
  }
  {{/each}}
}
```

### API Layer Templates

```handlebars
{{!-- templates/adapters/graphql/resolvers.ts.hbs --}}
// Generated GraphQL resolver for {{module.name}}
// Last generated: {{generated_at}}

import { Resolver, Query, Mutation, Args } from '@nestjs/graphql';
{{#each use_cases}}
import { {{name}}UseCase } from '../../application/use-cases/{{kebab_case name}}';
{{/each}}

@Resolver('{{module.name}}')
export class {{module.name}}Resolver {
  constructor(
    {{#each use_cases}}
    private {{camel_case name}}UseCase: {{name}}UseCase,
    {{/each}}
  ) {}
  
  {{#each api.queries}}
  @Query(() => {{return_type}})
  async {{name}}(@Args() args: {{input_type}}): Promise<{{return_type}}> {
    return this.{{linked_use_case}}UseCase.execute(args);
  }
  {{/each}}
  
  {{#each api.mutations}}
  @Mutation(() => {{return_type}})
  async {{name}}(@Args() args: {{input_type}}): Promise<{{return_type}}> {
    return this.{{linked_use_case}}UseCase.execute(args);
  }
  {{/each}}
}
```

## 3. Regeneration Engine

### Change Detection

```typescript
// modules/regeneration/change-detector.ts
interface ContractChange {
  type: 'added' | 'modified' | 'removed';
  path: string;
  old_value?: any;
  new_value?: any;
  impact_score: number;
}

export class ContractChangeDetector {
  detectChanges(oldContract: ModuleContract, newContract: ModuleContract): ContractChange[] {
    const changes: ContractChange[] = [];
    
    // Domain changes
    changes.push(...this.detectDomainChanges(oldContract.domain, newContract.domain));
    
    // API changes
    changes.push(...this.detectApiChanges(oldContract.api, newContract.api));
    
    // Use case changes  
    changes.push(...this.detectUseCaseChanges(oldContract.use_cases, newContract.use_cases));
    
    return changes.sort((a, b) => b.impact_score - a.impact_score);
  }
  
  private calculateImpactScore(change: ContractChange): number {
    const weights = {
      domain: 10,      // High impact
      use_cases: 8,    // High impact
      api: 6,          // Medium impact
      adapters: 4,     // Low-medium impact
      variants: 2,     // Low impact
    };
    
    const pathSegments = change.path.split('.');
    const category = pathSegments[0];
    
    return weights[category] || 1;
  }
}
```

### Intelligent Regeneration

```typescript
// modules/regeneration/regeneration-engine.ts
export class RegenerationEngine {
  async regenerate(
    contract: ModuleContract,
    changes: ContractChange[],
    preserveOptions: PreserveOptions
  ): Promise<RegenerationResult> {
    
    const plan = this.createRegenerationPlan(changes);
    const preserved = await this.extractPreservedCode(preserveOptions);
    
    const result = new RegenerationResult();
    
    // 1. Generate new code
    for (const step of plan.steps) {
      switch (step.type) {
        case 'generate_domain':
          result.add(await this.generateDomainLayer(contract));
          break;
          
        case 'generate_application':
          result.add(await this.generateApplicationLayer(contract, preserved.business_logic));
          break;
          
        case 'generate_adapters':
          result.add(await this.generateAdapterLayer(contract, step.variant));
          break;
          
        case 'update_tests':
          result.add(await this.updateTestLayer(contract, changes));
          break;
      }
    }
    
    // 2. Merge preserved code
    result = await this.mergePreservedCode(result, preserved);
    
    // 3. Validate integrity
    await this.validateIntegrity(result, contract);
    
    return result;
  }
  
  private async extractPreservedCode(options: PreserveOptions): Promise<PreservedCode> {
    const preserved = new PreservedCode();
    
    // Extract custom business logic
    if (options.preserve_business_logic) {
      preserved.business_logic = await this.extractCustomLogic();
    }
    
    // Extract test data
    if (options.preserve_test_data) {
      preserved.test_data = await this.extractTestData();
    }
    
    // Extract configuration
    if (options.preserve_configuration) {
      preserved.configuration = await this.extractConfiguration();
    }
    
    return preserved;
  }
  
  private async extractCustomLogic(): Promise<Map<string, string>> {
    const customLogic = new Map<string, string>();
    
    // Parse existing files for CUSTOM_LOGIC blocks
    const files = await this.findGeneratedFiles('**/*.ts');
    
    for (const file of files) {
      const content = await fs.readFile(file, 'utf-8');
      const matches = content.match(/CUSTOM_LOGIC_START:(.+?)\n([\s\S]*?)CUSTOM_LOGIC_END:\1/g);
      
      if (matches) {
        for (const match of matches) {
          const [, key, logic] = match.match(/CUSTOM_LOGIC_START:(.+?)\n([\s\S]*?)CUSTOM_LOGIC_END:\1/);
          customLogic.set(key, logic.trim());
        }
      }
    }
    
    return customLogic;
  }
}
```

## 4. Module Composition System

### Module Dependencies

```yaml
# contracts/composition/e-commerce.composition.yaml
composition:
  name: ECommerceSystem
  description: 完全なECシステム
  
  modules:
    product_management:
      contract: ./modules/product-management.module.yaml
      variants:
        api: graphql
        database: postgresql
        frontend: react
        
    order_management:
      contract: ./modules/order-management.module.yaml
      variants:
        api: graphql
        database: postgresql
        frontend: react
      depends_on:
        - product_management
        
    customer_management:
      contract: ./modules/customer-management.module.yaml
      variants:
        api: rest
        database: postgresql
        frontend: vue
        
  integration:
    event_bus:
      type: kafka
      topics:
        - product-events
        - order-events
        - customer-events
        
    api_gateway:
      type: graphql-federation
      services:
        - product_management
        - order_management
        - customer_management
        
    shared_database:
      type: postgresql
      schemas:
        - product_mgmt
        - order_mgmt  
        - customer_mgmt
```

### Composition Engine

```typescript
// modules/composition/composition-engine.ts
export class CompositionEngine {
  async compose(composition: SystemComposition): Promise<GeneratedSystem> {
    // 1. Validate dependencies
    this.validateDependencies(composition.modules);
    
    // 2. Generate modules in dependency order
    const modules = await this.generateModulesInOrder(composition.modules);
    
    // 3. Generate integration layer
    const integration = await this.generateIntegration(composition.integration, modules);
    
    // 4. Generate system configuration
    const configuration = await this.generateSystemConfiguration(composition, modules, integration);
    
    // 5. Generate deployment artifacts
    const deployment = await this.generateDeploymentArtifacts(composition);
    
    return new GeneratedSystem({
      modules,
      integration,
      configuration,
      deployment
    });
  }
  
  private validateDependencies(modules: ModuleDefinition[]): void {
    const graph = new DependencyGraph();
    
    for (const module of modules) {
      graph.addNode(module.name);
      for (const dep of module.depends_on || []) {
        graph.addEdge(module.name, dep);
      }
    }
    
    if (graph.hasCycles()) {
      throw new Error('Circular dependency detected');
    }
  }
}
```

## 5. CLI Integration

### Regeneration Commands

```bash
# Contract-based module generation
parasol generate module ProductManagement \
  --from-contract ./contracts/product-management.yaml \
  --variants api:graphql,database:postgresql,frontend:react

# Contract update and regeneration
parasol update contract ProductManagement \
  --add-use-case "UpdateProductDescription" \
  --regenerate

# Multi-variant generation
parasol generate variants ProductManagement \
  --frontend react,vue,angular \
  --compare bundle-size,performance,developer-experience

# System composition
parasol compose system ECommerce \
  --from-composition ./compositions/e-commerce.yaml \
  --environment production

# Change impact analysis
parasol analyze impact ProductManagement \
  --contract-change ./contracts/product-management-v2.yaml \
  --show affected-modules,test-requirements,migration-steps

# Intelligent regeneration
parasol regenerate ProductManagement \
  --preserve business-logic,test-data,custom-config \
  --dry-run \
  --show-diff
```

### Watch Mode

```typescript
// modules/cli/watch-mode.ts
export class ContractWatcher {
  async watch(contractPaths: string[], options: WatchOptions): Promise<void> {
    const chokidar = await import('chokidar');
    
    const watcher = chokidar.watch(contractPaths, {
      ignored: /node_modules/,
      persistent: true,
    });
    
    watcher.on('change', async (path: string) => {
      console.log(`Contract changed: ${path}`);
      
      try {
        const oldContract = this.contractCache.get(path);
        const newContract = await this.loadContract(path);
        
        const changes = this.changeDetector.detectChanges(oldContract, newContract);
        
        if (options.auto_regenerate && this.shouldAutoRegenerate(changes)) {
          await this.regenerationEngine.regenerate(newContract, changes, options.preserve);
          console.log(`✅ Module regenerated successfully`);
        } else {
          console.log(`⚠️  Changes detected. Run 'parasol regenerate' to apply.`);
        }
        
        this.contractCache.set(path, newContract);
        
      } catch (error) {
        console.error(`❌ Failed to process contract change: ${error.message}`);
      }
    });
  }
}
```

## 6. Migration and Versioning

### Contract Versioning

```yaml
# contracts/versions/product-management-v1.yaml → v2.yaml
migration:
  from_version: "1.0.0"
  to_version: "2.0.0"
  
  changes:
    - type: add_property
      target: domain.aggregates.Product.value_objects
      value: ProductDescription
      
    - type: add_use_case
      target: use_cases
      value:
        UpdateProductDescription:
          input: {product_id: ProductId, description: string}
          output: {success: boolean}
          
  migration_steps:
    database:
      - ALTER TABLE products ADD COLUMN description TEXT;
      
    api:
      - add_field: products.description
      - add_mutation: updateProductDescription
      
    frontend:
      - add_component: ProductDescriptionEditor
      - update_form: ProductForm
      
  backward_compatibility:
    api_v1: supported_until "2025-12-31"
    database: automatic_migration
```

### Zero-Downtime Migration

```typescript
// modules/migration/zero-downtime-migrator.ts
export class ZeroDowntimeMigrator {
  async migrate(from: ModuleContract, to: ModuleContract): Promise<MigrationResult> {
    const plan = this.createMigrationPlan(from, to);
    
    // 1. Deploy v2 alongside v1
    await this.deployParallel(to, { version: 'v2' });
    
    // 2. Route percentage of traffic to v2
    await this.routeTraffic({ v1: 90, v2: 10 });
    
    // 3. Monitor and gradually increase v2 traffic
    while (await this.shouldContinueMigration()) {
      const metrics = await this.monitorPerformance(['v1', 'v2']);
      
      if (metrics.v2.error_rate < metrics.v1.error_rate) {
        await this.increaseTrafficToV2();
      } else {
        await this.rollbackToV1();
        break;
      }
    }
    
    // 4. Complete migration
    await this.routeTraffic({ v2: 100 });
    await this.retireVersion('v1');
    
    return new MigrationResult({ success: true });
  }
}
```

## 実現できること

1. **真のコードレス開発**: 契約変更→自動再生成
2. **ゼロダウンタイム進化**: 段階的な移行とロールバック
3. **並列実験**: 複数バリアントの同時生成・比較
4. **知識の保存**: ビジネスロジックとカスタマイゼーションの保護
5. **完全な再現性**: 同じ契約から同じコードを生成
6. **インテリジェントな変更**: 影響範囲を自動分析
7. **システム全体の一貫性**: 依存関係を考慮した統合生成