# V3.0×V4統合フレームワーク自動生成レシピ

## Recipe: Generate Unified Parasol Implementation

### Purpose
コンサルティングツールのV3.0構造とパラソルV4のWHAT-HOW構造を統合し、実装コードを自動生成する

### Context
- V3.0: L3 Capability ⊃ Operations（親子関係）
- V4: WHAT-HOW ZIGZAG構造
- 統合: トップダウン（EA）×ボトムアップ（DDD）

### Prerequisites
```yaml
required_files:
  - consulting-tool domain designs (V3.0)
  - value definition
  - capability hierarchy (L1→L2→L3)
  - bounded context definitions
```

### Steps

#### Step 1: Import and Analyze V3.0 Design
```python
def import_v3_design(source_path):
    """
    コンサルティングツールのV3.0設計をインポート
    """
    design = {
        "capabilities": extract_capabilities(source_path),
        "operations": extract_operations(source_path),
        "bounded_contexts": extract_contexts(source_path),
        "domain_language": extract_domain_language(source_path)
    }

    # V3.0の重要な特徴を検証
    validate_l3_operation_relationship(design)

    return design
```

#### Step 2: Map to Unified Structure
```python
def map_to_unified_structure(v3_design):
    """
    V3.0設計を統合構造にマッピング
    """
    unified = {
        "value_definition": create_value_definition(v3_design),
        "capability_hierarchy": {
            "L1": map_strategic_capabilities(v3_design),
            "L2": map_tactical_capabilities(v3_design),
            "L3": map_operational_capabilities(v3_design)
        },
        "bounded_contexts": integrate_contexts(v3_design),
        "operations": classify_operations(v3_design)
    }

    # L3とOperationsの親子関係を保持
    for l3_cap in unified["capability_hierarchy"]["L3"]:
        l3_cap["operations"] = get_child_operations(l3_cap.id)

    return unified
```

#### Step 3: Apply V4 WHAT-HOW Patterns
```python
def apply_v4_patterns(unified_design):
    """
    V4のWHAT-HOW ZIGZAG構造を適用
    """
    # 各レベルで WHAT → HOW の変換
    for level in ["L1", "L2", "L3"]:
        capabilities = unified_design["capability_hierarchy"][level]

        for capability in capabilities:
            # WHATの定義
            capability["what"] = define_what(capability)

            # HOWの定義（次レベルのWHATになる）
            capability["how"] = define_how(capability)

            # 価値メトリクスの追加
            capability["metrics"] = generate_value_metrics(capability)

    return unified_design
```

#### Step 4: Classify Operations by Pattern
```python
def classify_operations(operations):
    """
    操作をパターンで分類
    """
    patterns = {
        "CRUD": [],
        "Workflow": [],
        "Analytics": [],
        "Collaboration": []
    }

    for operation in operations:
        pattern = detect_pattern(operation)
        patterns[pattern].append(enrich_operation(operation, pattern))

    return patterns
```

#### Step 5: Generate Domain Model
```python
def generate_domain_model(unified_design):
    """
    ドメインモデルのコード生成
    """
    code = {
        "entities": [],
        "aggregates": [],
        "services": [],
        "repositories": []
    }

    # エンティティ生成（V3属性 + V4価値要素）
    for entity in unified_design["domain_entities"]:
        code["entities"].append(
            generate_entity_code(
                v3_attributes=entity.attributes,
                v4_enhancements=entity.value_elements
            )
        )

    # 集約生成（L3能力を実現）
    for bc in unified_design["bounded_contexts"]:
        for l3_cap in bc["capabilities"]:
            aggregate = generate_aggregate(
                capability=l3_cap,
                operations=l3_cap["operations"]
            )
            code["aggregates"].append(aggregate)

    return code
```

#### Step 6: Generate Service Layer
```python
def generate_service_layer(unified_design):
    """
    サービス層のコード生成
    """
    services = []

    for bc in unified_design["bounded_contexts"]:
        # マイクロサービス生成
        service = {
            "name": bc.name + "Service",
            "operations": [],
            "api_endpoints": [],
            "events": []
        }

        # 各操作パターンに応じた実装
        for operation in bc.operations:
            if operation.pattern == "CRUD":
                service["operations"].append(generate_crud_operation(operation))
            elif operation.pattern == "Workflow":
                service["operations"].append(generate_workflow_operation(operation))
            elif operation.pattern == "Analytics":
                service["operations"].append(generate_analytics_operation(operation))
            elif operation.pattern == "Collaboration":
                service["operations"].append(generate_collaboration_operation(operation))

        services.append(service)

    return services
```

#### Step 7: Generate UI Components
```python
def generate_ui_components(unified_design):
    """
    UIコンポーネントの生成
    """
    components = {
        "pages": [],
        "components": [],
        "hooks": [],
        "stores": []
    }

    # ページ生成（L4実装）
    for page_spec in unified_design["pages"]:
        page = generate_page_component(
            spec=page_spec,
            operations=get_page_operations(page_spec),
            use_cases=page_spec.use_cases
        )
        components["pages"].append(page)

    return components
```

#### Step 8: Generate Tests
```python
def generate_tests(unified_design, generated_code):
    """
    テストコードの生成
    """
    tests = {
        "unit": generate_unit_tests(generated_code),
        "integration": generate_integration_tests(unified_design),
        "e2e": generate_e2e_tests(unified_design["pages"]),
        "value": generate_value_metric_tests(unified_design["metrics"])
    }

    return tests
```

#### Step 9: Validate and Output
```python
def validate_and_output(unified_design, generated_code):
    """
    検証と出力
    """
    # 検証
    validations = {
        "l3_operation_relationship": validate_parent_child_relationship(),
        "what_how_structure": validate_what_how_consistency(),
        "value_traceability": validate_value_metrics(),
        "business_rules": validate_business_rules_preserved()
    }

    if all(validations.values()):
        # 出力
        output_structure = {
            "design/": unified_design,
            "src/": generated_code,
            "tests/": generated_tests,
            "docs/": generate_documentation()
        }

        write_to_filesystem(output_structure)
        return "SUCCESS: Generation completed"
    else:
        return f"VALIDATION FAILED: {validations}"
```

### Execution

```bash
# Amplifier CLIでの実行
amplifier run recipes/v3-v4-unified-generation.md \
  --source=consulting-tool \
  --target=projects/05-parasol-v3-v4-unified \
  --validate=true \
  --generate-tests=true
```

### Output Structure

```
projects/05-parasol-v3-v4-unified/
├── generated/
│   ├── design/
│   │   ├── unified-structure.yaml
│   │   ├── capability-operation-matrix.md
│   │   └── value-metrics.yaml
│   ├── src/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── aggregates/
│   │   │   └── services/
│   │   ├── application/
│   │   │   ├── services/
│   │   │   └── use-cases/
│   │   ├── infrastructure/
│   │   │   ├── repositories/
│   │   │   └── api/
│   │   └── presentation/
│   │       ├── pages/
│   │       └── components/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   └── docs/
│       ├── api-specification.md
│       ├── domain-model.md
│       └── architecture.md
```

### Success Criteria

1. **構造の整合性**
   - L3 Capability ⊃ Operations の関係が保持されている
   - WHAT-HOW構造が一貫している

2. **ビジネスルールの保持**
   - V3.0のビジネスルールがすべて継承されている
   - V4の価値ルールが追加されている

3. **コード品質**
   - テストカバレッジ > 80%
   - 型安全性が保証されている

4. **価値の追跡可能性**
   - 価値定義から実装まで追跡可能
   - メトリクスが測定可能

### Notes

- このレシピは段階的に実行可能（各ステップを個別に実行できる）
- 大規模プロジェクトの場合は、bounded contextごとに分割実行を推奨
- 生成されたコードは必ずレビューとテストを実施