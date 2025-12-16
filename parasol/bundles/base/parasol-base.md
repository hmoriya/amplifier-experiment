---
bundle:
  name: parasol-base
  version: 1.0.0
  description: Parasol DDD Framework base bundle with 7-phase methodology
  
config:
  project:
    default_approach: value-driven
    phases_enabled: [1, 2, 3, 4, 5, 6, 7]
    
  outputs:
    format: markdown
    structure: hierarchical
    auto_save: true
    
  phases:
    phase1:
      outputs:
        - organization-analysis.md
        - market-assessment.md
        - stakeholder-map.md
        - constraints.md
      templates:
        organization:
          sections: [overview, structure, culture, capabilities]
        market:
          sections: [segments, competition, trends, opportunities]
          
    phase2:
      value_stream_style: hierarchical
      depth: 3
      outputs:
        - value-streams-mapping.md
        - enterprise-activities.md
        - value-definition.md
      templates:
        value_stream:
          required_fields: [id, name, description, activities]
          
    phase3:
      classification_levels: [CL1, CL2, CL3]
      auto_generate_cl3: false
      outputs:
        - domain-classification.md
        - subdomain-design.md
        - capability-map.md
        
  quality_gates:
    phase1_complete:
      required_outputs: [organization-analysis, market-assessment, stakeholder-map]
      validation_rules:
        stakeholder_count: ">=3"
        market_segments: ">=1"
        
    phase2_complete:
      required_outputs: [value-streams-mapping, enterprise-activities]
      validation_rules:
        value_streams: ">=3"
        activities_per_stream: ">=5"

agents:
  phase_agents:
    - parasol-phase1-context
    - parasol-phase2-value
    - parasol-phase3-capabilities
    - parasol-phase4-architecture
    - parasol-phase5-software
    - parasol-phase6-implementation
    - parasol-phase7-platform
    
  support_agents:
    - parasol-value-tracer
    - parasol-quality-gate
    - parasol-milestone-checker
    
  architecture_variants:
    traditional:
      - event_sourcing
      - backend_saga
      - complex_cqrs
      
    v5_lightweight:
      - crud_plus_notifications
      - frontend_orchestration
      - edge_transactions
      - simple_state_management
---

# Parasol Base Bundle

This is the foundational bundle for the Parasol DDD Framework, providing the core 7-phase methodology for enterprise software development.

## Included Phases

1. **Context**: Organization, market, and stakeholder analysis
2. **Value**: Value stream identification and mapping
3. **Capabilities**: Domain classification and capability design
4. **Architecture**: Application and integration design
5. **Software**: API and database design
6. **Implementation**: Code generation and module development
7. **Platform**: Deployment and operations

## Default Configuration

- **Approach**: Value-driven (can be overridden)
- **Output Format**: Markdown with hierarchical structure
- **Quality Gates**: Automatic validation at phase boundaries
- **All phases enabled**: Can be selectively disabled

## Usage

This bundle is typically included by other more specific bundles:

```yaml
includes:
  - bundle: ./base/parasol-base.md
```

Or used directly:

```bash
parasol --bundle ./bundles/base/parasol-base.md init my-project
```