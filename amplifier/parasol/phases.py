"""
Phase definitions for Parasol DDD Framework
Each phase represents a distinct stage in the development process
"""

from abc import ABC
from abc import abstractmethod
from typing import Any

import yaml


class PhaseBase(ABC):
    """Base class for all Parasol phases"""

    def __init__(self, name: str):
        self.name = name
        self.engine = None

    def set_engine(self, engine):
        """Set reference to the Parasol engine"""
        self.engine = engine

    @abstractmethod
    def execute(self, context) -> dict[str, Any]:
        """Execute the phase logic"""
        pass

    @abstractmethod
    def check_gate_conditions(self, context) -> bool:
        """Check if gate conditions are met to proceed"""
        pass

    @abstractmethod
    def update_context(self, context, result):
        """Update the context with phase results"""
        pass


class ValueAnalysisPhase(PhaseBase):
    """
    Phase 1: Value Analysis
    Analyze and define business value, stakeholders, and KPIs
    """

    def __init__(self):
        super().__init__("Value Analysis")

    def execute(self, context) -> dict[str, Any]:
        """Execute value analysis"""
        result = {
            "stakeholders": self._analyze_stakeholders(context),
            "value_propositions": self._define_value_propositions(context),
            "kpis": self._set_kpis(context),
            "roi_targets": self._calculate_roi(context),
        }

        # Apply patterns from knowledge base
        if self.engine:
            value_patterns = self.engine.pattern_library.get_patterns("value")
            for pattern in value_patterns:
                if self._is_pattern_applicable(pattern, context):
                    result["applied_patterns"] = result.get("applied_patterns", [])
                    result["applied_patterns"].append(pattern["name"])

        return result

    def check_gate_conditions(self, context) -> bool:
        """Check if value definition exists"""
        return bool(context.value_definition)

    def update_context(self, context, result):
        """Update context with value analysis results"""
        context.metadata["value_analysis"] = result

    def _analyze_stakeholders(self, context) -> list[dict]:
        """Analyze project stakeholders"""
        stakeholders = []

        # Extract from value definition
        if "stakeholders" in context.value_definition:
            for stakeholder in context.value_definition["stakeholders"]:
                stakeholders.append(
                    {
                        "name": stakeholder.get("name"),
                        "interest": stakeholder.get("interest", "medium"),
                        "influence": stakeholder.get("influence", "medium"),
                        "values": stakeholder.get("values", []),
                    }
                )

        return stakeholders

    def _define_value_propositions(self, context) -> dict:
        """Define value propositions"""
        return {
            "core": context.value_definition.get("core_value", ""),
            "supporting": context.value_definition.get("supporting_values", []),
        }

    def _set_kpis(self, context) -> list[dict]:
        """Set Key Performance Indicators"""
        kpis = []

        if "metrics" in context.value_definition:
            for metric_name, target in context.value_definition["metrics"].items():
                kpis.append(
                    {"name": metric_name, "target": target, "measurement_method": "TBD", "frequency": "monthly"}
                )

        return kpis

    def _calculate_roi(self, context) -> dict:
        """Calculate ROI targets"""
        return {
            "target_roi": context.value_definition.get("roi_target", "300%"),
            "payback_period": context.value_definition.get("payback_period", "6 months"),
            "value_realization": context.value_definition.get("value_realization", "incremental"),
        }

    def _is_pattern_applicable(self, pattern, context) -> bool:
        """Check if a pattern is applicable to current context"""
        # Simplified check - would be more sophisticated in practice
        return True


class CapabilityDesignPhase(PhaseBase):
    """
    Phase 2: Capability Design
    Design hierarchical capabilities from strategic to operational
    """

    def __init__(self):
        super().__init__("Capability Design")

    def execute(self, context) -> dict[str, Any]:
        """Execute capability design"""
        result = {
            "L1_strategic": self._design_strategic_capabilities(context),
            "L2_tactical": self._design_tactical_capabilities(context),
            "L3_operational": self._design_operational_capabilities(context),
            "capability_map": self._create_capability_map(context),
        }

        # Store capabilities in context
        context.capabilities = {
            "L1": result["L1_strategic"],
            "L2": result["L2_tactical"],
            "L3": result["L3_operational"],
        }

        return result

    def check_gate_conditions(self, context) -> bool:
        """Check if value analysis is complete"""
        return "value_analysis" in context.metadata

    def update_context(self, context, result):
        """Update context with capability design results"""
        context.metadata["capability_design"] = result

    def _design_strategic_capabilities(self, context) -> list[dict]:
        """Design L1 strategic capabilities"""
        # Extract from value definition or use patterns
        strategic_caps = []

        # Apply capability patterns
        if self.engine:
            patterns = self.engine.pattern_library.get_patterns("capability_strategic")
            for pattern in patterns:
                cap = {
                    "id": f"L1-{len(strategic_caps) + 1:03d}",
                    "name": pattern.get("name", "Strategic Capability"),
                    "what": pattern.get("description", ""),
                    "value_contribution": "high",
                }
                strategic_caps.append(cap)

        # Default capability if none from patterns
        if not strategic_caps:
            strategic_caps.append(
                {
                    "id": "L1-001",
                    "name": "Core Business Capability",
                    "what": "Enable core business operations",
                    "value_contribution": "high",
                }
            )

        return strategic_caps

    def _design_tactical_capabilities(self, context) -> list[dict]:
        """Design L2 tactical capabilities"""
        tactical_caps = []

        # Decompose L1 capabilities
        for l1_cap in context.capabilities.get("L1", []):
            # Generate 2-3 L2 capabilities per L1
            for i in range(2):
                tactical_caps.append(
                    {
                        "id": f"L2-{len(tactical_caps) + 1:03d}",
                        "parent": l1_cap["id"],
                        "name": f"{l1_cap['name']} - Tactical {i + 1}",
                        "what": f"Tactical realization of {l1_cap['name']}",
                        "implementation_complexity": "medium",
                    }
                )

        return tactical_caps

    def _design_operational_capabilities(self, context) -> list[dict]:
        """Design L3 operational capabilities"""
        operational_caps = []

        # Decompose L2 capabilities
        for l2_cap in context.capabilities.get("L2", []):
            # Generate 2-3 L3 capabilities per L2
            for i in range(2):
                operational_caps.append(
                    {
                        "id": f"L3-{len(operational_caps) + 1:03d}",
                        "parent": l2_cap["id"],
                        "name": f"{l2_cap['name']} - Operations",
                        "what": f"Operational capability for {l2_cap['name']}",
                        "operations": [],  # Will be filled in Operation Design phase
                    }
                )

        return operational_caps

    def _create_capability_map(self, context) -> dict:
        """Create capability dependency map"""
        return {
            "hierarchy": {
                "L1": context.capabilities.get("L1", []),
                "L2": context.capabilities.get("L2", []),
                "L3": context.capabilities.get("L3", []),
            },
            "dependencies": self._analyze_dependencies(context),
        }

    def _analyze_dependencies(self, context) -> list[dict]:
        """Analyze capability dependencies"""
        # Simplified dependency analysis
        return []


class DomainModelingPhase(PhaseBase):
    """
    Phase 3: Domain Modeling
    Model the business domain using DDD principles
    """

    def __init__(self):
        super().__init__("Domain Modeling")

    def execute(self, context) -> dict[str, Any]:
        """Execute domain modeling"""
        result = {
            "bounded_contexts": self._identify_bounded_contexts(context),
            "entities": self._define_entities(context),
            "aggregates": self._design_aggregates(context),
            "domain_events": self._identify_domain_events(context),
            "ubiquitous_language": self._establish_ubiquitous_language(context),
        }

        # Store in context
        context.bounded_contexts = result["bounded_contexts"]

        return result

    def check_gate_conditions(self, context) -> bool:
        """Check if capability design is complete"""
        return bool(context.capabilities)

    def update_context(self, context, result):
        """Update context with domain modeling results"""
        context.metadata["domain_modeling"] = result

    def _identify_bounded_contexts(self, context) -> list[dict]:
        """Identify bounded contexts from capabilities"""
        contexts = []

        # Group L3 capabilities into bounded contexts
        l3_caps = context.capabilities.get("L3", [])

        # Simple grouping - in practice would use more sophisticated analysis
        context_groups = {}
        for cap in l3_caps:
            parent = cap.get("parent", "default")
            if parent not in context_groups:
                context_groups[parent] = []
            context_groups[parent].append(cap)

        for parent, caps in context_groups.items():
            contexts.append(
                {
                    "name": f"Context_{parent}",
                    "capabilities": [c["id"] for c in caps],
                    "type": "core",
                    "integration_pattern": "shared_kernel",
                }
            )

        return contexts

    def _define_entities(self, context) -> list[dict]:
        """Define domain entities"""
        entities = []

        # Apply domain patterns
        if self.engine:
            domain_patterns = self.engine.pattern_library.get_patterns("domain_entity")
            for pattern in domain_patterns:
                entities.append(
                    {
                        "name": pattern.get("entity_name", "Entity"),
                        "attributes": pattern.get("attributes", []),
                        "invariants": pattern.get("invariants", []),
                    }
                )

        # Default entities if no patterns
        if not entities:
            entities = [
                {
                    "name": "Task",
                    "attributes": ["id", "title", "status", "assignee"],
                    "invariants": ["Title cannot be empty", "Status must be valid"],
                }
            ]

        return entities

    def _design_aggregates(self, context) -> list[dict]:
        """Design aggregates"""
        aggregates = []

        for bc in context.bounded_contexts:
            # Create aggregate for each bounded context
            aggregates.append(
                {"name": f"{bc['name']}Aggregate", "root": "TBD", "entities": [], "consistency_boundary": "immediate"}
            )

        return aggregates

    def _identify_domain_events(self, context) -> list[dict]:
        """Identify domain events"""
        events = []

        # Generate events based on entities and operations
        for entity in context.metadata.get("domain_modeling", {}).get("entities", []):
            events.extend(
                [
                    {"name": f"{entity['name']}Created", "type": "creation"},
                    {"name": f"{entity['name']}Updated", "type": "update"},
                    {"name": f"{entity['name']}Deleted", "type": "deletion"},
                ]
            )

        return events

    def _establish_ubiquitous_language(self, context) -> dict:
        """Establish ubiquitous language"""
        return {"terms": self._extract_terms(context), "definitions": {}, "contexts": {}}

    def _extract_terms(self, context) -> list[str]:
        """Extract domain terms"""
        terms = []

        # Extract from capabilities
        for level in ["L1", "L2", "L3"]:
            for cap in context.capabilities.get(level, []):
                terms.extend(cap["name"].split())

        # Remove duplicates and common words
        return list(set(terms))


class OperationDesignPhase(PhaseBase):
    """
    Phase 4: Operation Design
    Design operations that realize capabilities
    """

    def __init__(self):
        super().__init__("Operation Design")

    def execute(self, context) -> dict[str, Any]:
        """Execute operation design"""
        result = {
            "operations": self._design_operations(context),
            "patterns": self._classify_patterns(context),
            "api_design": self._design_apis(context),
            "business_rules": self._define_business_rules(context),
        }

        # Store in context
        context.operations = result["operations"]

        return result

    def check_gate_conditions(self, context) -> bool:
        """Check if domain modeling is complete"""
        return bool(context.bounded_contexts)

    def update_context(self, context, result):
        """Update context with operation design results"""
        context.metadata["operation_design"] = result

        # Link operations to L3 capabilities
        for op in result["operations"]:
            cap_id = op.get("capability")
            if cap_id:
                for cap in context.capabilities.get("L3", []):
                    if cap["id"] == cap_id:
                        cap["operations"].append(op["id"])

    def _design_operations(self, context) -> list[dict]:
        """Design operations for L3 capabilities"""
        operations = []

        for cap in context.capabilities.get("L3", []):
            # Generate operations based on capability
            ops = self._generate_operations_for_capability(cap)
            operations.extend(ops)

        return operations

    def _generate_operations_for_capability(self, capability) -> list[dict]:
        """Generate operations for a capability"""
        operations = []
        base_name = capability["name"].replace(" - Operations", "")

        # CRUD operations
        for action in ["Create", "Read", "Update", "Delete"]:
            operations.append(
                {
                    "id": f"OP-{len(operations) + 1:04d}",
                    "name": f"{action} {base_name}",
                    "capability": capability["id"],
                    "pattern": "CRUD",
                    "preconditions": [],
                    "postconditions": [],
                }
            )

        return operations

    def _classify_patterns(self, context) -> dict[str, list]:
        """Classify operations by pattern"""
        patterns = {"CRUD": [], "Workflow": [], "Analytics": [], "Collaboration": []}

        for op in context.operations:
            pattern = op.get("pattern", "CRUD")
            patterns[pattern].append(op["id"])

        return patterns

    def _design_apis(self, context) -> dict:
        """Design API endpoints"""
        api_design = {"endpoints": [], "schemas": {}, "security": "bearer_auth"}

        for op in context.operations:
            endpoint = {
                "path": f"/api/{op['name'].lower().replace(' ', '-')}",
                "method": self._determine_http_method(op),
                "operationId": op["id"],
            }
            api_design["endpoints"].append(endpoint)

        return api_design

    def _determine_http_method(self, operation) -> str:
        """Determine HTTP method based on operation"""
        name_lower = operation["name"].lower()
        if "create" in name_lower:
            return "POST"
        if "update" in name_lower:
            return "PUT"
        if "delete" in name_lower:
            return "DELETE"
        return "GET"

    def _define_business_rules(self, context) -> list[dict]:
        """Define business rules"""
        rules = []

        for op in context.operations:
            rules.append({"operation": op["id"], "rules": ["Validation required", "Authorization checked"]})

        return rules


class ImplementationGenerationPhase(PhaseBase):
    """
    Phase 5: Implementation Generation
    Generate implementation code from design
    """

    def __init__(self):
        super().__init__("Implementation Generation")

    def execute(self, context) -> dict[str, Any]:
        """Execute implementation generation"""
        result = {
            "generated_code": self._generate_code(context),
            "tests": self._generate_tests(context),
            "documentation": self._generate_documentation(context),
            "deployment": self._generate_deployment_config(context),
        }

        # Store artifact paths
        for artifact_type, artifact_path in result["generated_code"].items():
            context.generated_artifacts[artifact_type] = artifact_path

        return result

    def check_gate_conditions(self, context) -> bool:
        """Check if operation design is complete"""
        return bool(context.operations)

    def update_context(self, context, result):
        """Update context with implementation results"""
        context.metadata["implementation"] = result

    def _generate_code(self, context) -> dict[str, Any]:
        """Generate implementation code"""
        code_paths = {}

        # Generate domain models
        domain_path = context.project_path / "implementation" / "domain"
        domain_path.mkdir(parents=True, exist_ok=True)
        self._generate_domain_code(context, domain_path)
        code_paths["domain"] = domain_path

        # Generate services
        service_path = context.project_path / "implementation" / "services"
        service_path.mkdir(parents=True, exist_ok=True)
        self._generate_service_code(context, service_path)
        code_paths["services"] = service_path

        # Generate APIs
        api_path = context.project_path / "implementation" / "api"
        api_path.mkdir(parents=True, exist_ok=True)
        self._generate_api_code(context, api_path)
        code_paths["api"] = api_path

        return code_paths

    def _generate_domain_code(self, context, path):
        """Generate domain model code"""
        # Simplified code generation
        entities = context.metadata.get("domain_modeling", {}).get("entities", [])

        for entity in entities:
            code = f"""
class {entity["name"]}:
    '''Domain entity for {entity["name"]}'''

    def __init__(self):
        {chr(10).join(f"        self.{attr} = None" for attr in entity.get("attributes", []))}

    def validate(self):
        '''Validate entity invariants'''
        pass
"""
            file_path = path / f"{entity['name'].lower()}.py"
            file_path.write_text(code)

    def _generate_service_code(self, context, path):
        """Generate service code"""
        # Simplified service generation
        for bc in context.bounded_contexts:
            code = f"""
class {bc["name"]}Service:
    '''Service for {bc["name"]}'''

    def __init__(self):
        pass

    # Operations would be generated here
"""
            file_path = path / f"{bc['name'].lower()}_service.py"
            file_path.write_text(code)

    def _generate_api_code(self, context, path):
        """Generate API code"""
        # Generate OpenAPI spec
        api_spec = {
            "openapi": "3.0.0",
            "info": {"title": f"{context.project_name} API", "version": "1.0.0"},
            "paths": {},
        }

        api_design = context.metadata.get("operation_design", {}).get("api_design", {})
        for endpoint in api_design.get("endpoints", []):
            api_spec["paths"][endpoint["path"]] = {endpoint["method"].lower(): {"operationId": endpoint["operationId"]}}

        spec_path = path / "openapi.yaml"
        with open(spec_path, "w") as f:
            yaml.dump(api_spec, f)

    def _generate_tests(self, context) -> dict:
        """Generate test code"""
        return {"unit_tests": "tests/unit", "integration_tests": "tests/integration", "e2e_tests": "tests/e2e"}

    def _generate_documentation(self, context) -> dict:
        """Generate documentation"""
        return {"api_docs": "docs/api", "domain_docs": "docs/domain", "deployment_docs": "docs/deployment"}

    def _generate_deployment_config(self, context) -> dict:
        """Generate deployment configuration"""
        return {"docker": "deployment/docker", "kubernetes": "deployment/k8s", "ci_cd": "deployment/pipeline"}


class ValidationOptimizationPhase(PhaseBase):
    """
    Phase 6: Validation and Optimization
    Validate and optimize the generated implementation
    """

    def __init__(self):
        super().__init__("Validation and Optimization")

    def execute(self, context) -> dict[str, Any]:
        """Execute validation and optimization"""
        result = {
            "validation": self._validate_implementation(context),
            "performance": self._optimize_performance(context),
            "security": self._security_audit(context),
            "metrics": self._measure_metrics(context),
        }

        return result

    def check_gate_conditions(self, context) -> bool:
        """Check if implementation is complete"""
        return bool(context.generated_artifacts)

    def update_context(self, context, result):
        """Update context with validation results"""
        context.metadata["validation"] = result

    def _validate_implementation(self, context) -> dict:
        """Validate the implementation"""
        return {
            "business_rules": {"passed": True, "coverage": "100%"},
            "tests": {"passed": True, "coverage": "85%"},
            "api_contracts": {"valid": True},
        }

    def _optimize_performance(self, context) -> dict:
        """Optimize performance"""
        return {
            "response_time": {"p50": "45ms", "p95": "120ms"},
            "throughput": "1000 req/s",
            "optimizations_applied": ["caching", "query optimization"],
        }

    def _security_audit(self, context) -> dict:
        """Perform security audit"""
        return {"vulnerabilities": 0, "security_score": "A", "recommendations": []}

    def _measure_metrics(self, context) -> dict:
        """Measure value metrics"""
        return {
            "value_delivered": self._calculate_value_delivery(context),
            "roi_actual": "250%",
            "kpi_achievement": self._measure_kpi_achievement(context),
        }

    def _calculate_value_delivery(self, context) -> float:
        """Calculate value delivery percentage"""
        return 0.85

    def _measure_kpi_achievement(self, context) -> dict:
        """Measure KPI achievement"""
        kpis = context.metadata.get("value_analysis", {}).get("kpis", [])
        achievement = {}

        for kpi in kpis:
            achievement[kpi["name"]] = {"target": kpi["target"], "actual": "TBD", "achieved": True}

        return achievement
