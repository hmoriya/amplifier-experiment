"""Regeneration engine for contract-driven module generation."""

import json
import yaml
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import hashlib
import jinja2
from abc import ABC, abstractmethod


class ChangeType(Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"


@dataclass
class ContractChange:
    """Represents a change in a module contract."""
    type: ChangeType
    path: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    impact_score: int = 0


@dataclass
class PreservedCode:
    """Code segments that should be preserved during regeneration."""
    business_logic: Dict[str, str]
    test_data: Dict[str, Any]
    configuration: Dict[str, Any]
    custom_implementations: Dict[str, str]


@dataclass
class GenerationContext:
    """Context for code generation."""
    module_name: str
    contract: Dict[str, Any]
    variant: str
    preserved_code: Optional[PreservedCode] = None
    template_vars: Optional[Dict[str, Any]] = None


class CodeTemplate(ABC):
    """Abstract base class for code templates."""
    
    @abstractmethod
    def generate(self, context: GenerationContext) -> str:
        pass
    
    @abstractmethod
    def get_output_path(self, context: GenerationContext) -> Path:
        pass


class HandlebarsTemplate(CodeTemplate):
    """Handlebars-style template implementation."""
    
    def __init__(self, template_path: Path, output_pattern: str):
        self.template_path = template_path
        self.output_pattern = output_pattern
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path.parent),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def generate(self, context: GenerationContext) -> str:
        template = self.env.get_template(self.template_path.name)
        
        # Add helper functions for templates
        template_vars = {
            'module': context.contract,
            'variant': context.variant,
            'generated_at': datetime.now().isoformat(),
            'preserved_code': context.preserved_code or {},
            'helpers': self._get_helpers(),
            **(context.template_vars or {})
        }
        
        return template.render(**template_vars)
    
    def get_output_path(self, context: GenerationContext) -> Path:
        # Simple pattern replacement
        output_path = self.output_pattern.format(
            module_name=context.module_name,
            variant=context.variant
        )
        return Path(output_path)
    
    def _get_helpers(self) -> Dict[str, Any]:
        return {
            'kebab_case': lambda s: re.sub(r'([A-Z])', r'-\1', s).lower().lstrip('-'),
            'snake_case': lambda s: re.sub(r'([A-Z])', r'_\1', s).lower().lstrip('_'),
            'camel_case': lambda s: s[0].lower() + s[1:] if s else '',
            'pascal_case': lambda s: s[0].upper() + s[1:] if s else '',
        }


class ContractChangeDetector:
    """Detects changes between module contracts."""
    
    def detect_changes(self, old_contract: Dict, new_contract: Dict) -> List[ContractChange]:
        changes = []
        
        # Domain changes
        changes.extend(self._detect_domain_changes(
            old_contract.get('domain', {}), 
            new_contract.get('domain', {})
        ))
        
        # API changes
        changes.extend(self._detect_api_changes(
            old_contract.get('adapters', {}).get('primary', {}),
            new_contract.get('adapters', {}).get('primary', {})
        ))
        
        # Use case changes
        changes.extend(self._detect_use_case_changes(
            old_contract.get('use_cases', {}),
            new_contract.get('use_cases', {})
        ))
        
        # Calculate impact scores
        for change in changes:
            change.impact_score = self._calculate_impact_score(change)
        
        return sorted(changes, key=lambda c: c.impact_score, reverse=True)
    
    def _detect_domain_changes(self, old_domain: Dict, new_domain: Dict) -> List[ContractChange]:
        changes = []
        
        # Check aggregates
        old_aggregates = old_domain.get('aggregates', {})
        new_aggregates = new_domain.get('aggregates', {})
        
        for name in set(old_aggregates.keys()) | set(new_aggregates.keys()):
            if name not in old_aggregates:
                changes.append(ContractChange(
                    type=ChangeType.ADDED,
                    path=f"domain.aggregates.{name}",
                    new_value=new_aggregates[name]
                ))
            elif name not in new_aggregates:
                changes.append(ContractChange(
                    type=ChangeType.REMOVED,
                    path=f"domain.aggregates.{name}",
                    old_value=old_aggregates[name]
                ))
            elif old_aggregates[name] != new_aggregates[name]:
                changes.append(ContractChange(
                    type=ChangeType.MODIFIED,
                    path=f"domain.aggregates.{name}",
                    old_value=old_aggregates[name],
                    new_value=new_aggregates[name]
                ))
        
        return changes
    
    def _detect_api_changes(self, old_api: Dict, new_api: Dict) -> List[ContractChange]:
        changes = []
        
        # Check REST endpoints
        old_rest = old_api.get('rest_api', {}).get('endpoints', [])
        new_rest = new_api.get('rest_api', {}).get('endpoints', [])
        
        if old_rest != new_rest:
            changes.append(ContractChange(
                type=ChangeType.MODIFIED,
                path="adapters.primary.rest_api.endpoints",
                old_value=old_rest,
                new_value=new_rest
            ))
        
        return changes
    
    def _detect_use_case_changes(self, old_use_cases: Dict, new_use_cases: Dict) -> List[ContractChange]:
        changes = []
        
        for name in set(old_use_cases.keys()) | set(new_use_cases.keys()):
            if name not in old_use_cases:
                changes.append(ContractChange(
                    type=ChangeType.ADDED,
                    path=f"use_cases.{name}",
                    new_value=new_use_cases[name]
                ))
            elif name not in new_use_cases:
                changes.append(ContractChange(
                    type=ChangeType.REMOVED,
                    path=f"use_cases.{name}",
                    old_value=old_use_cases[name]
                ))
            elif old_use_cases[name] != new_use_cases[name]:
                changes.append(ContractChange(
                    type=ChangeType.MODIFIED,
                    path=f"use_cases.{name}",
                    old_value=old_use_cases[name],
                    new_value=new_use_cases[name]
                ))
        
        return changes
    
    def _calculate_impact_score(self, change: ContractChange) -> int:
        weights = {
            'domain': 10,
            'use_cases': 8,
            'adapters': 6,
            'variants': 2,
        }
        
        path_segments = change.path.split('.')
        category = path_segments[0] if path_segments else 'unknown'
        base_score = weights.get(category, 1)
        
        # Adjust based on change type
        type_multipliers = {
            ChangeType.REMOVED: 1.5,
            ChangeType.MODIFIED: 1.2,
            ChangeType.ADDED: 1.0,
        }
        
        return int(base_score * type_multipliers[change.type])


class CodePreserver:
    """Preserves custom code during regeneration."""
    
    def extract_preserved_code(self, module_path: Path, preserve_options: Dict[str, bool]) -> PreservedCode:
        preserved = PreservedCode(
            business_logic={},
            test_data={},
            configuration={},
            custom_implementations={}
        )
        
        if preserve_options.get('business_logic', True):
            preserved.business_logic = self._extract_custom_logic(module_path)
        
        if preserve_options.get('test_data', True):
            preserved.test_data = self._extract_test_data(module_path)
        
        if preserve_options.get('configuration', True):
            preserved.configuration = self._extract_configuration(module_path)
        
        return preserved
    
    def _extract_custom_logic(self, module_path: Path) -> Dict[str, str]:
        custom_logic = {}
        
        # Find all TypeScript/JavaScript files
        for file_path in module_path.rglob("*.ts"):
            if file_path.is_file():
                content = file_path.read_text(encoding='utf-8')
                
                # Extract CUSTOM_LOGIC blocks
                pattern = r'// CUSTOM_LOGIC_START:(.+?)\n(.*?)// CUSTOM_LOGIC_END:\1'
                matches = re.findall(pattern, content, re.DOTALL)
                
                for key, logic in matches:
                    custom_logic[key] = logic.strip()
        
        return custom_logic
    
    def _extract_test_data(self, module_path: Path) -> Dict[str, Any]:
        test_data = {}
        
        # Look for test data files
        test_files = list(module_path.rglob("*.test.json")) + list(module_path.rglob("test-data.json"))
        
        for file_path in test_files:
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        test_data[str(file_path.relative_to(module_path))] = json.load(f)
                except json.JSONDecodeError:
                    # Skip invalid JSON files
                    continue
        
        return test_data
    
    def _extract_configuration(self, module_path: Path) -> Dict[str, Any]:
        configuration = {}
        
        # Look for configuration files
        config_files = [
            module_path / "config.json",
            module_path / "config.yaml",
            module_path / ".env.local"
        ]
        
        for file_path in config_files:
            if file_path.is_file():
                try:
                    if file_path.suffix == '.json':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            configuration[file_path.name] = json.load(f)
                    elif file_path.suffix in ['.yaml', '.yml']:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            configuration[file_path.name] = yaml.safe_load(f)
                    else:
                        # Plain text config
                        configuration[file_path.name] = file_path.read_text(encoding='utf-8')
                except (json.JSONDecodeError, yaml.YAMLError):
                    continue
        
        return configuration


class RegenerationEngine:
    """Main engine for regenerating modules from contracts."""
    
    def __init__(self, templates_path: Path):
        self.templates_path = templates_path
        self.change_detector = ContractChangeDetector()
        self.code_preserver = CodePreserver()
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, CodeTemplate]:
        templates = {}
        
        # Load all template files
        for template_file in self.templates_path.rglob("*.hbs"):
            template_name = template_file.stem
            output_pattern = self._get_output_pattern(template_file)
            templates[template_name] = HandlebarsTemplate(template_file, output_pattern)
        
        return templates
    
    def _get_output_pattern(self, template_file: Path) -> str:
        # Simple mapping from template name to output pattern
        # In a real implementation, this would be configurable
        patterns = {
            'entity': 'modules/{module_name}/domain/entities/{entity_name}.ts',
            'use-case': 'modules/{module_name}/application/use-cases/{use_case_name}.ts',
            'resolver': 'modules/{module_name}/adapters/{variant}/resolvers/{module_name}.resolver.ts',
            'repository': 'modules/{module_name}/adapters/{variant}/repositories/{module_name}.repository.ts',
        }
        
        return patterns.get(template_file.stem, f'modules/{{module_name}}/generated/{template_file.stem}')
    
    async def regenerate_module(
        self,
        module_name: str,
        new_contract: Dict[str, Any],
        old_contract: Optional[Dict[str, Any]] = None,
        preserve_options: Optional[Dict[str, bool]] = None
    ) -> Dict[str, Any]:
        """Regenerate a module based on contract changes."""
        
        preserve_options = preserve_options or {
            'business_logic': True,
            'test_data': True,
            'configuration': True
        }
        
        # Detect changes if old contract provided
        changes = []
        if old_contract:
            changes = self.change_detector.detect_changes(old_contract, new_contract)
        
        # Extract preserved code
        module_path = Path(f'modules/{module_name}')
        preserved_code = None
        if module_path.exists():
            preserved_code = self.code_preserver.extract_preserved_code(module_path, preserve_options)
        
        # Generate variants
        variants = new_contract.get('variants', {})
        generated_files = {}
        
        for variant_type, variant_options in variants.items():
            for variant_name in variant_options:
                variant_files = await self._generate_variant(
                    module_name,
                    new_contract,
                    f"{variant_type}_{variant_name}",
                    preserved_code
                )
                generated_files.update(variant_files)
        
        return {
            'module_name': module_name,
            'changes': [asdict(change) for change in changes],
            'generated_files': generated_files,
            'preserved_code_keys': list(preserved_code.business_logic.keys()) if preserved_code else [],
        }
    
    async def _generate_variant(
        self,
        module_name: str,
        contract: Dict[str, Any],
        variant: str,
        preserved_code: Optional[PreservedCode]
    ) -> Dict[str, str]:
        """Generate code for a specific variant."""
        
        context = GenerationContext(
            module_name=module_name,
            contract=contract,
            variant=variant,
            preserved_code=preserved_code
        )
        
        generated_files = {}
        
        # Generate domain layer
        if 'domain' in contract:
            domain_files = self._generate_domain_layer(context)
            generated_files.update(domain_files)
        
        # Generate application layer
        if 'use_cases' in contract:
            app_files = self._generate_application_layer(context)
            generated_files.update(app_files)
        
        # Generate adapter layer
        if 'adapters' in contract:
            adapter_files = self._generate_adapter_layer(context)
            generated_files.update(adapter_files)
        
        return generated_files
    
    def _generate_domain_layer(self, context: GenerationContext) -> Dict[str, str]:
        """Generate domain layer code."""
        files = {}
        
        domain = context.contract.get('domain', {})
        aggregates = domain.get('aggregates', {})
        
        # Generate entity files
        for aggregate_name, aggregate_def in aggregates.items():
            if 'entity' in self.templates:
                entity_context = GenerationContext(
                    module_name=context.module_name,
                    contract=context.contract,
                    variant=context.variant,
                    preserved_code=context.preserved_code,
                    template_vars={'entity': aggregate_def, 'entity_name': aggregate_name}
                )
                
                template = self.templates['entity']
                content = template.generate(entity_context)
                file_path = template.get_output_path(entity_context)
                files[str(file_path)] = content
        
        return files
    
    def _generate_application_layer(self, context: GenerationContext) -> Dict[str, str]:
        """Generate application layer code."""
        files = {}
        
        use_cases = context.contract.get('use_cases', {})
        
        # Generate use case files
        for use_case_name, use_case_def in use_cases.items():
            if 'use-case' in self.templates:
                use_case_context = GenerationContext(
                    module_name=context.module_name,
                    contract=context.contract,
                    variant=context.variant,
                    preserved_code=context.preserved_code,
                    template_vars={'use_case': use_case_def, 'use_case_name': use_case_name}
                )
                
                template = self.templates['use-case']
                content = template.generate(use_case_context)
                file_path = template.get_output_path(use_case_context)
                files[str(file_path)] = content
        
        return files
    
    def _generate_adapter_layer(self, context: GenerationContext) -> Dict[str, str]:
        """Generate adapter layer code."""
        files = {}
        
        adapters = context.contract.get('adapters', {})
        
        # Generate resolver files for GraphQL
        if context.variant.endswith('graphql') and 'resolver' in self.templates:
            template = self.templates['resolver']
            content = template.generate(context)
            file_path = template.get_output_path(context)
            files[str(file_path)] = content
        
        # Generate repository files
        if 'repository' in self.templates:
            template = self.templates['repository']
            content = template.generate(context)
            file_path = template.get_output_path(context)
            files[str(file_path)] = content
        
        return files


class ModuleCompositionEngine:
    """Engine for composing multiple modules into a system."""
    
    def __init__(self, regeneration_engine: RegenerationEngine):
        self.regeneration_engine = regeneration_engine
    
    async def compose_system(self, composition_config: Dict[str, Any]) -> Dict[str, Any]:
        """Compose a complete system from module composition configuration."""
        
        modules = composition_config.get('modules', {})
        integration = composition_config.get('integration', {})
        
        # Validate dependencies
        self._validate_dependencies(modules)
        
        # Generate modules in dependency order
        generated_modules = {}
        for module_name, module_config in self._sort_by_dependencies(modules):
            contract_path = Path(module_config['contract'])
            contract = self._load_contract(contract_path)
            
            result = await self.regeneration_engine.regenerate_module(
                module_name,
                contract,
                preserve_options=module_config.get('preserve_options')
            )
            
            generated_modules[module_name] = result
        
        # Generate integration layer
        integration_files = self._generate_integration_layer(integration, generated_modules)
        
        return {
            'modules': generated_modules,
            'integration': integration_files,
            'composition': composition_config['name']
        }
    
    def _validate_dependencies(self, modules: Dict[str, Any]) -> None:
        """Validate module dependencies for cycles."""
        # Simple cycle detection
        visited = set()
        rec_stack = set()
        
        def has_cycle(module_name: str) -> bool:
            visited.add(module_name)
            rec_stack.add(module_name)
            
            module_config = modules.get(module_name, {})
            dependencies = module_config.get('depends_on', [])
            
            for dep in dependencies:
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(module_name)
            return False
        
        for module_name in modules:
            if module_name not in visited:
                if has_cycle(module_name):
                    raise ValueError(f"Circular dependency detected involving {module_name}")
    
    def _sort_by_dependencies(self, modules: Dict[str, Any]) -> List[Tuple[str, Any]]:
        """Sort modules by their dependencies."""
        # Topological sort
        in_degree = {name: 0 for name in modules}
        
        # Calculate in-degrees
        for name, config in modules.items():
            dependencies = config.get('depends_on', [])
            for dep in dependencies:
                if dep in in_degree:
                    in_degree[dep] += 1
        
        # Process modules with no dependencies first
        queue = [name for name, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append((current, modules[current]))
            
            # Update in-degrees of dependent modules
            dependencies = modules[current].get('depends_on', [])
            for dep in dependencies:
                if dep in in_degree:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        queue.append(dep)
        
        return result
    
    def _load_contract(self, contract_path: Path) -> Dict[str, Any]:
        """Load a module contract from file."""
        with open(contract_path, 'r', encoding='utf-8') as f:
            if contract_path.suffix == '.yaml' or contract_path.suffix == '.yml':
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def _generate_integration_layer(
        self,
        integration_config: Dict[str, Any],
        modules: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate integration layer code."""
        integration_files = {}
        
        # Generate API gateway configuration
        if 'api_gateway' in integration_config:
            gateway_config = self._generate_api_gateway_config(
                integration_config['api_gateway'],
                modules
            )
            integration_files['api-gateway.yaml'] = yaml.dump(gateway_config)
        
        # Generate event bus configuration
        if 'event_bus' in integration_config:
            event_config = self._generate_event_bus_config(
                integration_config['event_bus'],
                modules
            )
            integration_files['event-bus.yaml'] = yaml.dump(event_config)
        
        return integration_files
    
    def _generate_api_gateway_config(
        self,
        gateway_config: Dict[str, Any],
        modules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate API gateway configuration."""
        return {
            'type': gateway_config.get('type', 'graphql-federation'),
            'services': [
                {
                    'name': module_name,
                    'url': f'http://{module_name}:4000/graphql'
                }
                for module_name in gateway_config.get('services', [])
            ]
        }
    
    def _generate_event_bus_config(
        self,
        event_config: Dict[str, Any],
        modules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate event bus configuration."""
        return {
            'type': event_config.get('type', 'kafka'),
            'topics': event_config.get('topics', []),
            'brokers': ['localhost:9092']
        }