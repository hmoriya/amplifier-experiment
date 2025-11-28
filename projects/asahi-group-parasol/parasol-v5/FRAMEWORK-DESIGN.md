# Parasol V5 Framework - Complete Design

## Executive Summary

Parasol V5 is a systematic framework for decomposing business value into software architecture through a staged, interactive process. It maps the journey from enterprise value streams to Domain-Driven Design implementation.

**Core Insight:**
```
Value Streams → Capabilities → Architecture → Software
VS0-VS7 → CL1→CL2→CL3 → Services/BCs → DDD Tactical
```

## Framework Philosophy

### Design Principles

1. **Staged Execution**: Progress through phases sequentially with clear checkpoints
2. **Interactive Guidance**: User decisions at strategic boundaries, automation for mechanics
3. **Template-Driven**: Consistent artifacts through reusable templates
4. **Incremental Refinement**: Work on one VS, one capability, one BC at a time
5. **Traceability**: Every artifact links back to business value

### Automation vs Manual Decision

**Automated:**
- Template generation and file creation
- Directory structure management
- Consistency validation (cross-references)
- Artifact formatting

**Manual (User Decision):**
- Business value prioritization
- Strategic classification (core/supporting/generic)
- Boundary definitions (subdomain, BC, service)
- Architecture pattern selection
- API contract design

**Interactive (Guided):**
- Discovery questions with templates
- Option selection with constraints
- Validation with suggestions

## Complete Execution Sequence

### Overview Flow

```
START
  ↓
Phase 1: Context (one-time)
  ↓
Phase 2: Value Definition (per VS, iterative)
  ↓
Phase 3a: CL1 Classification (holistic view)
  ↓
Phase 3b: CL2 Subdomain Design (per domain/VS)
  ↓
Phase 3c: CL3 Bounded Context Design (per subdomain)
  ↓
Phase 4: Architecture Design (holistic, integrating all BCs)
  ↓
Phase 5: Software Design (per service/BC)
  ↓
Phase 6: Implementation (per service/BC)
  ↓
Phase 7: Platform (infrastructure)
  ↓
END (iterative refinement continues)
```

### Detailed Phase Specifications

---

## Phase 1: Context Establishment

**Command:** `/parasol:1-context`

**Purpose:** Establish project foundation and constraints

**Execution:**
1. Ask discovery questions:
   - What is the business domain?
   - Who are the key stakeholders?
   - What are the business constraints?
   - What are the technical constraints?
   - What is the timeline and scope?

2. Generate `project-context.yaml`:
   ```yaml
   project:
     name: ""
     domain: ""
     description: ""

   stakeholders:
     - role: ""
       concerns: []

   constraints:
     business: []
     technical: []
     timeline: ""

   scope:
     in_scope: []
     out_of_scope: []
   ```

3. Create directory structure:
   ```
   outputs/1-context/
   └── project-context.yaml
   ```

**Next Step:** Proceed to Phase 2 (Value Definition)

---

## Phase 2: Value Definition

**Command:** `/parasol:2-value [vs-name]`

**Purpose:** Define enterprise value streams that drive all downstream design

**Value Streams:**
- VS0: Vision & Strategy
- VS1: Market Analysis
- VS2: Customer Experience
- VS3: Operations Excellence
- VS4: Innovation & Growth
- VS5: Risk & Compliance
- VS6: Partnership & Ecosystem
- VS7: Sustainability & Impact

**Execution:**

**Without parameter:**
```
→ /parasol:2-value

Shows:
  Available Value Streams:
  1. VS0: Vision & Strategy [not started]
  2. VS1: Market Analysis [not started]
  3. VS2: Customer Experience [in progress]
  ...

  Which value stream do you want to work on? [0-7]:
```

**With parameter:**
```
→ /parasol:2-value vs2

Executes:
  1. Load VS2 template questions
  2. Interactive discovery session
  3. Generate outputs/2-value/vs2-customer-experience.md
  4. Ask: "Work on another VS? [y/n]"
```

**Template Structure (per VS):**
```markdown
# VS{N}: {Name}

## Business Context
[Discovery questions specific to this VS]

## Value Proposition
- Stakeholder value
- Business metrics
- Strategic importance

## Capabilities Required
[High-level capabilities needed - feeds into Phase 3]

## Success Criteria
[How to measure value delivery]

## Dependencies
- Other VS dependencies
- External dependencies
```

**Output:**
```
outputs/2-value/
├── vs0-vision-strategy.md
├── vs1-market-analysis.md
├── vs2-customer-experience.md
├── ...
└── vs7-sustainability-impact.md
```

**Completion Criteria:**
- Minimum 2 VS defined (typically VS0 + one operational VS)
- All critical value streams identified
- Dependencies mapped

**Next Step:** Proceed to Phase 3a (CL1 Classification)

---

## Phase 3: Capability Design (Three Levels)

### Phase 3a: CL1 - Strategic Domain Classification

**Command:** `/parasol:3-capabilities cl1`

**Purpose:** Classify domains by strategic importance (Core/Supporting/Generic)

**Input:** All VS definitions from Phase 2

**Execution:**
1. Analyze all VS definitions
2. Extract domain concepts
3. Classify each domain:
   - **Core Domain**: Competitive differentiator, unique to business
   - **Supporting Domain**: Necessary but not differentiating
   - **Generic Domain**: Commodity, use off-the-shelf solutions

4. Generate strategic assessment

**Output:**
```
outputs/3-capabilities/domain-classification/
├── domain-map.md              # Visual map of all domains
├── strategic-assessment.md    # Classification rationale
└── investment-priorities.md   # Resource allocation guidance
```

**Template: domain-map.md**
```markdown
# Domain Classification Map

## Core Domains
- **Domain Name**: [Description]
  - Strategic Value: [Why core?]
  - Competitive Advantage: [How differentiates?]
  - Investment Level: High
  - Related VS: [VS links]

## Supporting Domains
- **Domain Name**: [Description]
  - Business Necessity: [Why needed?]
  - Investment Level: Medium
  - Related VS: [VS links]

## Generic Domains
- **Domain Name**: [Description]
  - Commodity Nature: [Why generic?]
  - Recommended Solution: [Buy vs build?]
  - Investment Level: Low
  - Related VS: [VS links]
```

**Next Step:** Proceed to Phase 3b (CL2 Subdomain Design)

---

### Phase 3b: CL2 - Tactical Subdomain Design

**Command:** `/parasol:3-capabilities cl2 [domain-name]`

**Purpose:** Decompose domains into subdomains (microservice candidates)

**Input:** CL1 domain classifications

**Execution:**

**Without parameter:**
```
→ /parasol:3-capabilities cl2

Shows:
  Classified Domains:

  Core Domains:
  1. CustomerEngagement [not decomposed]
  2. ProductRecommendation [in progress]

  Supporting Domains:
  3. OrderManagement [not decomposed]
  ...

  Which domain to decompose? [1-N]:
```

**With parameter:**
```
→ /parasol:3-capabilities cl2 CustomerEngagement

Executes:
  1. Load domain from CL1
  2. Ask decomposition questions:
     - What are the major functional areas?
     - What are the natural boundaries?
     - What changes independently?
     - What has different scalability needs?

  3. Generate subdomain specifications
  4. Create subdomain-{name}.md files
```

**Output:**
```
outputs/3-capabilities/subdomain-design/
├── CustomerEngagement/
│   ├── subdomain-overview.md
│   ├── subdomain-profile-management.md
│   ├── subdomain-loyalty-program.md
│   └── subdomain-communication-preferences.md
└── OrderManagement/
    ├── subdomain-overview.md
    ├── subdomain-order-processing.md
    └── subdomain-fulfillment.md
```

**Template: subdomain-{name}.md**
```markdown
# Subdomain: {Name}

## Parent Domain
- Name: {Domain Name}
- Classification: [Core/Supporting/Generic]

## Subdomain Overview
- Purpose: [What this subdomain handles]
- Scope: [Boundaries and responsibilities]
- Strategic Importance: [Inherits from parent + specific notes]

## Capabilities
[Tactical capabilities this subdomain provides]

## Key Concepts
[Main domain concepts - will become aggregates/entities]

## Dependencies
- Other Subdomains: [List]
- External Systems: [List]

## Scalability & Performance
- Expected Load: [Characteristics]
- Scaling Strategy: [How to scale]

## Candidate for Microservice
- Justification: [Why this could be a service?]
- Size Estimate: [Complexity indicator]

## Related Value Streams
[Links back to VS]
```

**Completion Criteria:**
- All core domains decomposed
- Critical supporting domains decomposed
- Generic domains marked for off-the-shelf solutions

**Next Step:** Proceed to Phase 3c (CL3 Bounded Context Design)

---

### Phase 3c: CL3 - Operational Bounded Context Design

**Command:** `/parasol:3-capabilities cl3 [subdomain-name]`

**Purpose:** Define bounded contexts within subdomains

**Input:** CL2 subdomain specifications

**Concept:** A subdomain (CL2) may contain multiple bounded contexts (CL3) if there are distinct models or teams. Often 1 subdomain = 1 BC, but not always.

**Execution:**

**Without parameter:**
```
→ /parasol:3-capabilities cl3

Shows:
  Subdomains:

  CustomerEngagement:
  1. ProfileManagement [not contextualized]
  2. LoyaltyProgram [1 BC defined]

  OrderManagement:
  3. OrderProcessing [not contextualized]

  Which subdomain to contextualize? [1-N]:
```

**With parameter:**
```
→ /parasol:3-capabilities cl3 ProfileManagement

Executes:
  1. Load subdomain specification
  2. Ask boundary questions:
     - Are there multiple models of the same concepts?
     - Are there distinct team boundaries?
     - Are there integration seams?

  3. Define BC(s) for this subdomain
  4. Generate BC specifications
```

**Output:**
```
outputs/3-capabilities/bounded-context-design/
├── ProfileManagement/
│   ├── bc-customer-profile.md
│   └── bc-preference-management.md
├── LoyaltyProgram/
│   └── bc-loyalty.md
└── context-relationships.md
```

**Template: bc-{name}.md**
```markdown
# Bounded Context: {Name}

## Parent Subdomain
- Subdomain: {Name}
- Domain: {Domain Name}

## Context Boundary
- Purpose: [What model this BC maintains]
- Scope: [What's inside, what's outside]
- Ubiquitous Language: [Key terms specific to this BC]

## Domain Model (High-Level)
[Conceptual entities/aggregates - not implementation yet]

## Integration Points
- Upstream Contexts: [What this BC depends on]
- Downstream Contexts: [What depends on this BC]
- Integration Patterns: [How integration happens]

## Team & Ownership
- Responsible Team: [Team name]
- Autonomy Level: [How independent?]

## Business Operations
[Key operations this BC supports - feeds into Phase 5]

## Related Capabilities (CL2)
[Links back to subdomain capabilities]
```

**Template: context-relationships.md**
```markdown
# Context Map

## Overview
[Visual representation of all BCs and relationships]

## Relationships

### Upstream-Downstream
- **{BC1}** → **{BC2}**
  - Pattern: [Customer-Supplier / Conformist / Anticorruption Layer]
  - Integration: [Async events / Sync API / Batch]
  - Data Flow: [What data crosses boundary]

### Shared Kernel
- **{BC1}** ↔ **{BC2}**
  - Shared Model: [What's shared]
  - Coordination: [How teams coordinate]

### Partnership
- **{BC1}** ↔ **{BC2}**
  - Mutual Dependency: [How they depend on each other]

## Integration Patterns Summary
[Catalog of integration approaches used]
```

**Completion Criteria:**
- All critical subdomains have BC definitions
- Context relationships mapped
- Integration patterns identified

**Next Step:** Proceed to Phase 4 (Architecture Design)

---

## Phase 4: Architecture Design

**Command:** `/parasol:4-architecture`

**Purpose:** Design service boundaries and integration architecture based on all BCs

**Input:** All CL3 bounded context definitions

**Execution:**
1. Analyze all BC definitions and relationships
2. Map BCs to services (may be 1:1 or N:1)
3. Design context map at architecture level
4. Define integration patterns
5. Make architectural decisions (event-driven, API gateway, etc.)
6. Generate architecture documentation

**Output:**
```
outputs/4-architecture/
├── service-boundaries.md      # Which BCs map to which services
├── context-map.md             # Architecture-level context map
├── integration-patterns.md    # How services integrate
├── architecture-decisions.md  # ADRs (Architecture Decision Records)
└── deployment-model.md        # How services deploy
```

**Template: service-boundaries.md**
```markdown
# Service Boundaries

## Service Mapping Strategy
[Rationale for how BCs map to services]

## Services

### Service: {Name}
- **Bounded Contexts Included:**
  - {BC1}
  - {BC2} (if applicable)

- **Rationale:**
  [Why these BCs are in one service]

- **Type:**
  [Core / Supporting / Generic]

- **Scalability:**
  [How this service scales]

- **Data Ownership:**
  [What data this service owns]

- **Technology Stack:**
  [Recommended tech]

- **Team Ownership:**
  [Which team owns this service]

## Service Relationships
[High-level interaction diagram]
```

**Template: integration-patterns.md**
```markdown
# Integration Patterns

## Pattern Catalog

### Asynchronous Event-Driven
- **When to Use:** [Scenarios]
- **Implementation:** [Event bus, message queue]
- **Services Using This:** [{Service list}]

### Synchronous REST API
- **When to Use:** [Scenarios]
- **Implementation:** [API Gateway, direct calls]
- **Services Using This:** [{Service list}]

### Batch/ETL
- **When to Use:** [Scenarios]
- **Implementation:** [Tools]
- **Services Using This:** [{Service list}]

## Cross-Cutting Concerns
- Authentication/Authorization
- Logging & Monitoring
- Circuit Breakers
- Rate Limiting
```

**Template: architecture-decisions.md**
```markdown
# Architecture Decision Records (ADRs)

## ADR-001: {Decision Title}
- **Status:** [Accepted / Proposed / Deprecated]
- **Context:** [What circumstances led to this decision]
- **Decision:** [What we decided to do]
- **Consequences:** [Positive and negative outcomes]
- **Alternatives Considered:** [What else was considered]

## ADR-002: ...
```

**Next Step:** Proceed to Phase 5 (Software Design)

---

## Phase 5: Software Design (DDD Tactical)

**Command:** `/parasol:5-software [service-name] [bc-name]`

**Purpose:** Detailed software design for each service/BC

**Input:** Architecture design for selected service/BC

**Execution:**

**Without parameters:**
```
→ /parasol:5-software

Shows:
  Services & Bounded Contexts:

  Service: CustomerEngagement
  1. BC: CustomerProfile [not designed]
  2. BC: PreferenceManagement [in progress]

  Service: OrderManagement
  3. BC: OrderProcessing [not designed]

  Which service/BC to design? [1-N]:
```

**With parameters:**
```
→ /parasol:5-software CustomerEngagement CustomerProfile

Executes:
  1. Load architecture for service/BC
  2. Define domain language (Parasol format)
  3. Design APIs (operations)
  4. Design database schema
  5. Define business operations (use cases + UI)
```

**Output:**
```
outputs/5-software/services/
├── CustomerEngagement/
│   ├── CustomerProfile/
│   │   ├── domain-language.md
│   │   ├── api-specification.md
│   │   ├── database-design.md
│   │   └── business-operations/
│   │       ├── create-customer-profile/
│   │       │   ├── use-case.md
│   │       │   └── page-definition.md
│   │       └── update-preferences/
│   │           ├── use-case.md
│   │           └── page-definition.md
│   └── PreferenceManagement/
│       └── ...
└── OrderManagement/
    └── OrderProcessing/
        └── ...
```

**Template: domain-language.md (Parasol Format)**
```markdown
# Domain Language: {BC Name}

## Aggregates

### Aggregate: {Name}
```parasol
aggregate {Name} {
  id: {Type}

  // State
  {attribute}: {Type}
  ...

  // Behavior
  command {CommandName}({params}) -> Result
  event {EventName}

  // Invariants
  invariant {rule_description}
}
```

## Entities

### Entity: {Name}
```parasol
entity {Name} {
  id: {Type}
  {attribute}: {Type}
  ...
}
```

## Value Objects

### ValueObject: {Name}
```parasol
value object {Name} {
  {attribute}: {Type}
  ...

  // Validation rules
  validate {rule}
}
```

## Domain Services

### Service: {Name}
```parasol
domain service {Name} {
  operation {OperationName}({params}) -> {ReturnType}
}
```

## Domain Events

### Event: {Name}
```parasol
event {Name} {
  aggregate_id: {Type}
  {data}: {Type}
  occurred_at: DateTime
}
```

## Repository Contracts

### Repository: {Name}
```parasol
repository {AggregateType}Repository {
  find_by_id(id: {Type}) -> Option<{AggregateType}>
  save(aggregate: {AggregateType}) -> Result
  delete(id: {Type}) -> Result
}
```
```

**Template: api-specification.md**
```markdown
# API Specification: {BC Name}

## Overview
- Base URL: `/api/{version}/{service}`
- Authentication: [Method]
- Rate Limiting: [Policy]

## Endpoints

### {Operation Name}
- **Method:** GET/POST/PUT/DELETE
- **Path:** `/{resource}/{id}`
- **Description:** [What this operation does]

**Request:**
```json
{
  "field": "type"
}
```

**Response:**
```json
{
  "result": "data"
}
```

**Errors:**
- 400: [Validation errors]
- 404: [Not found]
- 500: [Server errors]

**Business Rules:**
- [Rule 1]
- [Rule 2]

## Events Published
- {EventName}: [When published]

## Events Consumed
- {EventName}: [What happens when consumed]
```

**Template: database-design.md**
```markdown
# Database Design: {BC Name}

## Schema Overview
- Database Type: [SQL/NoSQL/Graph]
- Schema Name: {bc_name}_db

## Tables/Collections

### Table: {name}
```sql
CREATE TABLE {name} (
  id UUID PRIMARY KEY,
  {column} {TYPE} NOT NULL,
  ...
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_{name}_{column} ON {name}({column});
```

**Purpose:** [What this table stores]

**Aggregate Root:** {AggregateType}

**Relationships:**
- Foreign Key to {other_table}

**Access Patterns:**
- [Query pattern 1]
- [Query pattern 2]

## Data Migration Strategy
[How to evolve schema]

## Backup & Recovery
[Strategy]
```

**Template: use-case.md**
```markdown
# Use Case: {Name}

## Metadata
- **ID:** UC-{number}
- **Actor:** {User role}
- **Trigger:** {What starts this use case}
- **Preconditions:** [What must be true before]
- **Postconditions:** [What's true after success]

## Main Flow
1. Actor does X
2. System does Y
3. System validates Z
4. System stores result
5. System notifies actor

## Alternative Flows

### A1: {Scenario}
- **Condition:** [When this happens]
- **Flow:**
  - 3a. System detects error
  - 3b. System shows error message
  - 3c. Return to step 2

## Business Rules
- BR-1: [Rule description]
- BR-2: [Rule description]

## Domain Events Triggered
- {EventName}: [When and why]

## Related Aggregates
- {AggregateName}: [How it's involved]
```

**Template: page-definition.md**
```markdown
# Page Definition: {Name}

## Page Metadata
- **Route:** `/{path}`
- **Access:** [Who can access]
- **Related Use Case:** UC-{number}

## Page Purpose
[What user accomplishes on this page]

## Page Structure

### Layout
- Header: [Components]
- Main Content: [Sections]
- Footer: [Components]

### Components

#### Component: {Name}
- **Type:** [Form / Table / Card / etc.]
- **Purpose:** [What this component does]
- **Data Source:** [API endpoint or local state]

**Fields:**
- {field_name}: {Type} [Required/Optional]
  - Validation: [Rules]
  - Default: [Value]

**Actions:**
- {Button/Link}: Triggers {use case or navigation}

### State Management
- Local State: [What's stored locally]
- Global State: [What's shared]
- API Calls: [When data is fetched/saved]

## User Interactions

### Interaction: {Name}
1. User does X
2. System responds with Y
3. Page updates Z

## Error Handling
- {Error Type}: Show {message}
- Validation Errors: Inline feedback

## Accessibility
- Keyboard navigation: [How]
- Screen reader: [ARIA labels]

## Performance
- Initial Load: [Target time]
- Interaction Response: [Target time]
```

**Completion Criteria per Service/BC:**
- Domain language defined (all aggregates, entities, VOs)
- APIs specified (all operations)
- Database designed (all tables, indexes)
- Business operations defined (use cases + pages)

**Next Step:** Proceed to Phase 6 (Implementation)

---

## Phase 6: Implementation

**Command:** `/parasol:6-implementation [service] [bc]`

**Purpose:** Generate implementation code from specifications

**Input:** Software design from Phase 5

**Execution:**
1. Load domain language, API specs, DB design, business operations
2. Generate code based on tech stack
3. Create directory structure
4. Generate tests

**Output:**
```
src/
├── services/
│   ├── CustomerEngagement/
│   │   ├── CustomerProfile/
│   │   │   ├── domain/
│   │   │   │   ├── aggregates/
│   │   │   │   ├── entities/
│   │   │   │   ├── value_objects/
│   │   │   │   └── services/
│   │   │   ├── application/
│   │   │   │   ├── use_cases/
│   │   │   │   └── services/
│   │   │   ├── infrastructure/
│   │   │   │   ├── repositories/
│   │   │   │   └── adapters/
│   │   │   └── interfaces/
│   │   │       ├── api/
│   │   │       └── events/
│   │   └── PreferenceManagement/
│   │       └── ...
│   └── OrderManagement/
│       └── ...
└── shared/
    ├── common/
    └── infrastructure/
```

**Note:** Implementation details depend on tech stack (Python/TypeScript/etc.)

**Next Step:** Proceed to Phase 7 (Platform)

---

## Phase 7: Platform & Infrastructure

**Command:** `/parasol:7-platform`

**Purpose:** Setup infrastructure, deployment, and operational concerns

**Input:** All implementations

**Execution:**
1. Generate infrastructure as code (IaC)
2. Setup CI/CD pipelines
3. Configure monitoring & logging
4. Define deployment strategy

**Output:**
```
infrastructure/
├── terraform/         # or CloudFormation, Pulumi
│   ├── network.tf
│   ├── compute.tf
│   └── databases.tf
├── kubernetes/        # if using K8s
│   ├── deployments/
│   ├── services/
│   └── ingress/
├── docker/
│   └── Dockerfile (per service)
└── monitoring/
    ├── prometheus/
    ├── grafana/
    └── alerts/

.github/workflows/     # or GitLab CI, Jenkins
├── ci.yml
└── cd.yml
```

---

## Status & Help Commands

### Status Command

**Command:** `/parasol:status`

**Purpose:** Show current progress and suggest next steps

**Execution:**
```
→ /parasol:status

Project: Asahi Digital Transformation
Status: Phase 3b - Subdomain Design

✅ Completed:
  Phase 1: Context established
  Phase 2: 5 of 8 value streams defined
    ✅ VS0: Vision & Strategy
    ✅ VS2: Customer Experience
    ✅ VS3: Operations Excellence
    ✅ VS4: Innovation & Growth
    ✅ VS5: Risk & Compliance
    ⏳ VS1: Market Analysis (in progress)
    ❌ VS6: Partnership & Ecosystem (not started)
    ❌ VS7: Sustainability & Impact (not started)

  Phase 3a: Domain classification complete (3 core, 4 supporting, 2 generic)
  Phase 3b: 5 of 9 subdomains designed

⏳ In Progress:
  Phase 3b: Subdomain design
    ✅ CustomerEngagement (3 subdomains)
    ✅ OrderManagement (2 subdomains)
    ⏳ ProductCatalog (in progress)
    ❌ InventoryManagement (not started)
    ...

📋 Next Suggested Steps:
  1. Complete subdomain design for ProductCatalog
  2. Design remaining 3 subdomains
  3. Proceed to Phase 3c (Bounded Context Design)

💡 Tips:
  - Can skip VS6 and VS7 if not critical for MVP
  - ProductCatalog is high priority (linked to VS2 and VS3)

Commands:
  /parasol:3-capabilities cl2 ProductCatalog  # Continue current work
  /parasol:2-value vs6                        # Add missing VS
```

### Help Command

**Command:** `/parasol:0-help [topic]`

**Purpose:** Provide guidance and troubleshooting

**Execution:**

**General help:**
```
→ /parasol:0-help

Parasol V5 - Quick Guide

Workflow:
  1. /parasol:1-context       - Establish project context
  2. /parasol:2-value [vs]    - Define value streams
  3. /parasol:3-capabilities  - Design capabilities (CL1→CL2→CL3)
  4. /parasol:4-architecture  - Design architecture
  5. /parasol:5-software      - Design software (per service/BC)
  6. /parasol:6-implementation - Generate code
  7. /parasol:7-platform      - Setup infrastructure

Status:
  /parasol:status             - Show current progress

Help:
  /parasol:0-help [topic]     - Get detailed help

Topics: workflow, value-streams, capabilities, architecture,
        software-design, implementation, troubleshooting

Example:
  /parasol:0-help capabilities
```

**Topic-specific help:**
```
→ /parasol:0-help capabilities

Phase 3: Capability Design

Three levels:
  CL1: Strategic classification (Core/Supporting/Generic)
  CL2: Tactical subdomain design (microservice candidates)
  CL3: Operational bounded context design (BC boundaries)

Execute in order:
  1. /parasol:3-capabilities cl1          # Classify all domains
  2. /parasol:3-capabilities cl2 [domain] # Decompose each domain
  3. /parasol:3-capabilities cl3 [subdomain] # Define BCs

Key concepts:
  - CL1: Determines investment priorities
  - CL2: Maps to microservice candidates (roughly)
  - CL3: Defines team boundaries and integration points

Outputs:
  CL1: outputs/3-capabilities/domain-classification/
  CL2: outputs/3-capabilities/subdomain-design/
  CL3: outputs/3-capabilities/bounded-context-design/

Next: /parasol:4-architecture (when all CL3 complete)
```

---

## Feedback Loops & Iteration

### When to Iterate Back

**Common scenarios:**

1. **Phase 5 → Phase 4:** Implementation insights reveal architecture issues
   - Command: `/parasol:4-architecture` (re-run with new understanding)

2. **Phase 4 → Phase 3c:** Architecture reveals BC boundaries were wrong
   - Command: `/parasol:3-capabilities cl3 [subdomain]` (redefine BCs)

3. **Phase 3 → Phase 2:** Capability design reveals missing value streams
   - Command: `/parasol:2-value [new-vs]` (add missing VS)

4. **Any phase → Phase 1:** Fundamental assumption changes
   - Command: `/parasol:1-context` (update context)

### Validation Points

**Automated validation:**
- Cross-references between phases
- Completeness checks (all VS linked to capabilities, etc.)
- Consistency checks (naming, references)

**Manual validation (user):**
- Strategic alignment (does CL1 match business priorities?)
- Boundary appropriateness (are BCs right-sized?)
- Integration patterns (do they make sense?)

**Command:** `/parasol:validate`
```
→ /parasol:validate

Validation Report:

✅ Consistency:
  - All VS referenced in capabilities
  - All capabilities mapped to BCs
  - All BCs mapped to services

⚠️  Warnings:
  - VS6 (Partnership) not defined but referenced in CL2
  - BC "LoyaltyProgram" has no business operations defined

❌ Errors:
  - Service "Analytics" not found in architecture but referenced in Phase 5

Recommendations:
  1. Define VS6 or remove references
  2. Complete business operations for LoyaltyProgram
  3. Add Analytics service to architecture or remove references
```

---

## Directory Structure (Complete)

```
parasol-v5/
├── README.md                    # Overview and quick start
├── FRAMEWORK-DESIGN.md          # This document
├── QUICK-START.md               # Step-by-step beginner guide
│
├── commands/                    # Slash command implementations
│   ├── 0-help.md
│   ├── 1-context.md
│   ├── 2-value.md
│   ├── 3-capabilities.md
│   ├── 4-architecture.md
│   ├── 5-software.md
│   ├── 6-implementation.md
│   ├── 7-platform.md
│   ├── status.md
│   └── validate.md
│
├── specifications/              # Design specifications
│   ├── value-streams/          # VS0-VS7 specifications
│   │   ├── vs0-vision-strategy.md
│   │   ├── vs1-market-analysis.md
│   │   └── ...
│   ├── capabilities/           # Capability level specs
│   │   ├── cl1-classification-guide.md
│   │   ├── cl2-subdomain-design-guide.md
│   │   └── cl3-bounded-context-guide.md
│   ├── architecture/           # Architecture patterns
│   │   ├── service-patterns.md
│   │   ├── integration-patterns.md
│   │   └── deployment-patterns.md
│   └── software-design/        # DDD tactical patterns
│       ├── domain-language-guide.md
│       ├── api-design-guide.md
│       └── database-design-guide.md
│
├── templates/                   # Reusable templates
│   ├── phase-2/                # Value stream templates
│   │   ├── vs0-template.md
│   │   ├── vs1-template.md
│   │   └── ...
│   ├── phase-3/                # Capability templates
│   │   ├── domain-classification-template.md
│   │   ├── subdomain-template.md
│   │   └── bounded-context-template.md
│   ├── phase-4/                # Architecture templates
│   │   ├── service-boundary-template.md
│   │   ├── context-map-template.md
│   │   └── adr-template.md
│   └── phase-5/                # Software design templates
│       ├── domain-language-template.md
│       ├── api-spec-template.md
│       ├── database-design-template.md
│       ├── use-case-template.md
│       └── page-definition-template.md
│
├── examples/                    # Sample implementations
│   ├── e-commerce/             # E-commerce domain example
│   │   ├── outputs/            # Complete example outputs
│   │   └── README.md           # Walkthrough
│   └── saas-platform/          # SaaS platform example
│       ├── outputs/
│       └── README.md
│
└── guides/                      # Additional documentation
    ├── concepts/               # Core concepts explained
    │   ├── value-streams.md
    │   ├── capability-hierarchy.md
    │   ├── ddd-mapping.md
    │   └── bounded-contexts.md
    ├── workflows/              # Common workflows
    │   ├── new-project.md
    │   ├── add-feature.md
    │   └── refactor-boundaries.md
    └── troubleshooting/        # Common issues
        ├── boundary-issues.md
        ├── integration-challenges.md
        └── faq.md
```

### Project Outputs Structure

```
outputs/                         # Generated artifacts
├── 1-context/
│   └── project-context.yaml
│
├── 2-value/
│   ├── vs0-vision-strategy.md
│   ├── vs1-market-analysis.md
│   └── ...
│
├── 3-capabilities/
│   ├── domain-classification/
│   │   ├── domain-map.md
│   │   ├── strategic-assessment.md
│   │   └── investment-priorities.md
│   ├── subdomain-design/
│   │   ├── {DomainName}/
│   │   │   ├── subdomain-overview.md
│   │   │   ├── subdomain-{name}.md
│   │   │   └── ...
│   │   └── ...
│   └── bounded-context-design/
│       ├── {SubdomainName}/
│       │   ├── bc-{name}.md
│       │   └── ...
│       └── context-relationships.md
│
├── 4-architecture/
│   ├── service-boundaries.md
│   ├── context-map.md
│   ├── integration-patterns.md
│   ├── architecture-decisions.md
│   └── deployment-model.md
│
├── 5-software/
│   └── services/
│       ├── {ServiceName}/
│       │   └── {BCName}/
│       │       ├── domain-language.md
│       │       ├── api-specification.md
│       │       ├── database-design.md
│       │       └── business-operations/
│       │           ├── {operation-name}/
│       │           │   ├── use-case.md
│       │           │   └── page-definition.md
│       │           └── ...
│       └── ...
│
├── 6-implementation/           # Links to src/ (not duplicated)
│   └── implementation-status.md
│
└── 7-platform/                 # Links to infrastructure/ (not duplicated)
    └── platform-status.md
```

---

## Command Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ Parasol V5 - Command Quick Reference                  │
├─────────────────────────────────────────────────────────────┤
│ Phase 1: Context                                            │
│   /parasol:1-context                                        │
│                                                             │
│ Phase 2: Value Definition                                   │
│   /parasol:2-value [vs-name]                               │
│     vs-name: vs0-vs7 or omit to select interactively       │
│                                                             │
│ Phase 3: Capability Design                                  │
│   /parasol:3-capabilities cl1                              │
│   /parasol:3-capabilities cl2 [domain-name]                │
│   /parasol:3-capabilities cl3 [subdomain-name]             │
│                                                             │
│ Phase 4: Architecture                                       │
│   /parasol:4-architecture                                  │
│                                                             │
│ Phase 5: Software Design                                    │
│   /parasol:5-software [service-name] [bc-name]            │
│                                                             │
│ Phase 6: Implementation                                     │
│   /parasol:6-implementation [service] [bc]                 │
│                                                             │
│ Phase 7: Platform                                           │
│   /parasol:7-platform                                      │
│                                                             │
│ Utilities                                                   │
│   /parasol:status          - Show progress                 │
│   /parasol:validate        - Check consistency             │
│   /parasol:0-help [topic]  - Get help                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

### 1. Staged vs All-at-Once
**Decision:** Staged execution with checkpoints
**Rationale:**
- Reduces cognitive load
- Allows validation at each stage
- Enables iterative refinement
- Users can stop/resume

### 2. Interactive vs Fully Automated
**Decision:** Interactive guidance with automation for mechanics
**Rationale:**
- Strategic decisions require human judgment
- Automation ensures consistency
- Templates provide structure without rigidity

### 3. Granularity of Commands
**Decision:** Phase-level commands with optional parameters
**Rationale:**
- Clear progression (Phase 1 → 2 → 3...)
- Flexibility (parameters enable targeted work)
- Discoverability (help shows logical next steps)

### 4. Output Structure
**Decision:** Hierarchical outputs mirroring conceptual hierarchy
**Rationale:**
- Traceability from value → implementation
- Clear dependencies between artifacts
- Intuitive navigation

### 5. Template Philosophy
**Decision:** Rich templates with placeholders, not blank canvases
**Rationale:**
- Reduces "blank page syndrome"
- Ensures completeness
- Teaches good practices
- Maintains consistency

---

## Success Criteria

A well-designed Parasol V5 implementation should achieve:

### User Experience
- [ ] New users can start within 5 minutes
- [ ] Clear next steps at every stage
- [ ] Minimal context switching
- [ ] Recoverable from mistakes

### Artifact Quality
- [ ] Complete traceability (value → code)
- [ ] Consistent formatting
- [ ] Validated cross-references
- [ ] Actionable specifications

### Framework Flexibility
- [ ] Works for small projects (2-3 BCs)
- [ ] Scales to large projects (20+ BCs)
- [ ] Supports iteration
- [ ] Allows customization

### Learning Curve
- [ ] Concepts introduced progressively
- [ ] Examples for every template
- [ ] Help available in context
- [ ] Troubleshooting guides

---

## Implementation Roadmap

### Phase 1: Core Framework (MVP)
1. Directory structure
2. Core commands (Phase 1-3)
3. Basic templates
4. Status command
5. One complete example

### Phase 2: Full Workflow
1. Architecture design (Phase 4)
2. Software design (Phase 5)
3. Integration patterns
4. Validation command
5. Multiple examples

### Phase 3: Advanced Features
1. Implementation generation (Phase 6)
2. Platform setup (Phase 7)
3. Migration tools
4. Visual diagrams
5. IDE integration

### Phase 4: Optimization
1. Performance improvements
2. Enhanced validation
3. AI-assisted generation
4. Collaboration features
5. Analytics & insights

---

## Conclusion

Parasol V5 provides a systematic, staged approach to translating business value into software architecture. By mapping enterprise value streams through capability hierarchies into Domain-Driven Design, it creates clear traceability from "why we build" to "how we implement."

The framework balances structure (templates, phases) with flexibility (parameters, iteration), automation (consistency) with guidance (strategic decisions), and completeness (all phases) with practicality (staged execution).

**Core Innovation:** Explicit mapping of business value → strategic capabilities → tactical subdomains → operational bounded contexts → software design, making the entire chain visible and traceable.

**Next Steps:**
1. Review this design document
2. Create command implementations
3. Develop templates
4. Build first example
5. Test with real project
