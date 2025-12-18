"""
Diagram content generator for Parasol V5 book
Generates diagrams from content specifications using the modular engine
"""

import logging
from typing import Dict, List, Any, Optional

# 新しいモジュラーエンジンをインポート
try:
    from .diagram_engine import generate_diagram, list_available_diagrams
    from .diagram_config import DIAGRAM_DEFINITIONS
    MODULAR_ENGINE_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("Modular diagram engine loaded successfully")
except ImportError as e:
    MODULAR_ENGINE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"Modular diagram engine not available: {e}")


class DiagramGenerator:
    """Generate diagram content in Mermaid format from data specifications"""
    
    def __init__(self):
        """Initialize diagram generator"""
        self.diagram_templates = {
            'phase_flow': self._generate_phase_flow,
            'value_stream': self._generate_value_stream,
            'capability_map': self._generate_capability_map,
            'architecture_overview': self._generate_architecture_overview,
            'process_flow': self._generate_process_flow,
            'hierarchy_tree': self._generate_hierarchy_tree
        }
    
    def generate_diagram(self, diagram_type: str, data: Dict[str, Any], **kwargs) -> str:
        """
        Generate Mermaid diagram from specification
        
        Args:
            diagram_type: Type of diagram to generate
            data: Data specification for the diagram
            **kwargs: Additional options
        
        Returns:
            Mermaid diagram code
        """
        if diagram_type not in self.diagram_templates:
            logger.error(f"Unknown diagram type: {diagram_type}")
            return f"<!-- Unknown diagram type: {diagram_type} -->"
        
        try:
            return self.diagram_templates[diagram_type](data, **kwargs)
        except Exception as e:
            logger.error(f"Failed to generate {diagram_type} diagram: {e}")
            return f"<!-- Failed to generate {diagram_type} diagram: {e} -->"
    
    def _generate_phase_flow(self, data: Dict[str, Any], **kwargs) -> str:
        """Generate Parasol phase flow diagram"""
        phases = data.get('phases', [])
        title = data.get('title', '8フェーズプロセス')
        flow_direction = kwargs.get('direction', 'TD')  # Top-Down
        
        lines = [
            '```mermaid',
            f'flowchart {flow_direction}'
        ]
        
        # Group phases by category
        phase_groups = {}
        for phase in phases:
            group = phase.get('group', 'default')
            if group not in phase_groups:
                phase_groups[group] = []
            phase_groups[group].append(phase)
        
        # Generate subgraphs for each group
        group_colors = {
            'goal': '#e1f5fe',
            'implementation': '#f3e5f5', 
            'detail_design': '#e8f5e8',
            'basic_design': '#fff3e0',
            'preparation': '#fce4ec'
        }
        
        node_ids = []
        
        for group_name, group_phases in phase_groups.items():
            if len(group_phases) > 1:
                lines.append(f'    subgraph {group_name} ["{group_phases[0].get("group_title", group_name)}"]')
                for phase in group_phases:
                    node_id = f"phase{phase['number']}" if 'number' in phase else phase['id']
                    emoji = phase.get('emoji', '')
                    title = phase.get('title', '')
                    description = phase.get('description', '')
                    
                    if description:
                        lines.append(f'        {node_id}["{emoji} {title}<br/>{description}"]')
                    else:
                        lines.append(f'        {node_id}["{emoji} {title}"]')
                    
                    node_ids.append(node_id)
                lines.append('    end')
            else:
                # Single phase
                phase = group_phases[0]
                node_id = f"phase{phase['number']}" if 'number' in phase else phase['id']
                emoji = phase.get('emoji', '')
                title = phase.get('title', '')
                description = phase.get('description', '')
                
                if description:
                    lines.append(f'    {node_id}["{emoji} {title}<br/>{description}"]')
                else:
                    lines.append(f'    {node_id}["{emoji} {title}"]')
                
                node_ids.append(node_id)
        
        # Add flow connections
        lines.append('')
        lines.append('    %% フロー定義')
        
        # Connect phases in order
        if 'flow' in data:
            for connection in data['flow']:
                from_node = connection['from']
                to_node = connection['to']
                lines.append(f'    {from_node} --> {to_node}')
        else:
            # Default linear flow
            for i in range(len(node_ids) - 1):
                lines.append(f'    {node_ids[i]} --> {node_ids[i+1]}')
        
        # Add styling
        lines.append('')
        lines.append('    %% スタイリング')
        for group_name, color in group_colors.items():
            if group_name in phase_groups:
                lines.append(f'    classDef {group_name}Style fill:{color},stroke:#333,stroke-width:2px,color:#000')
                for phase in phase_groups[group_name]:
                    node_id = f"phase{phase['number']}" if 'number' in phase else phase['id']
                    lines.append(f'    class {node_id} {group_name}Style')
        
        lines.append('```')
        return '\n'.join(lines)
    
    def _generate_value_stream(self, data: Dict[str, Any], **kwargs) -> str:
        """Generate value stream diagram"""
        streams = data.get('value_streams', [])
        
        lines = [
            '```mermaid',
            'flowchart LR'
        ]
        
        # Generate nodes for each value stream
        for i, stream in enumerate(streams):
            stream_id = f"vs{i}"
            name = stream.get('name', f'VS{i}')
            description = stream.get('description', '')
            
            if description:
                lines.append(f'    {stream_id}["{name}<br/>{description}"]')
            else:
                lines.append(f'    {stream_id}["{name}"]')
            
            # Add sub-capabilities if any
            capabilities = stream.get('capabilities', [])
            for j, cap in enumerate(capabilities):
                cap_id = f"cap{i}_{j}"
                cap_name = cap.get('name', f'Cap {j}')
                lines.append(f'    {cap_id}["{cap_name}"]')
                lines.append(f'    {stream_id} --> {cap_id}')
        
        lines.append('```')
        return '\n'.join(lines)
    
    def _generate_capability_map(self, data: Dict[str, Any], **kwargs) -> str:
        """Generate capability mapping diagram"""
        capabilities = data.get('capabilities', [])
        
        lines = [
            '```mermaid',
            'graph TD'
        ]
        
        # Group capabilities by level
        levels = {}
        for cap in capabilities:
            level = cap.get('level', 'CL3')
            if level not in levels:
                levels[level] = []
            levels[level].append(cap)
        
        # Generate subgraph for each level
        for level_name, level_caps in levels.items():
            lines.append(f'    subgraph {level_name} ["{level_name} レベル"]')
            
            for cap in level_caps:
                cap_id = cap.get('id', cap['name'].replace(' ', '_'))
                cap_name = cap.get('name', '')
                lines.append(f'        {cap_id}["{cap_name}"]')
            
            lines.append('    end')
        
        # Add relationships
        for cap in capabilities:
            parent_id = cap.get('parent')
            if parent_id:
                cap_id = cap.get('id', cap['name'].replace(' ', '_'))
                lines.append(f'    {parent_id} --> {cap_id}')
        
        lines.append('```')
        return '\n'.join(lines)
    
    def _generate_architecture_overview(self, data: Dict[str, Any], **kwargs) -> str:
        """Generate system architecture overview"""
        components = data.get('components', [])
        
        lines = [
            '```mermaid',
            'graph TB'
        ]
        
        # Group by layer
        layers = {}
        for comp in components:
            layer = comp.get('layer', 'application')
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(comp)
        
        # Generate each layer
        layer_order = ['presentation', 'application', 'domain', 'infrastructure']
        for layer in layer_order:
            if layer in layers:
                lines.append(f'    subgraph {layer} ["{layer.title()} Layer"]')
                
                for comp in layers[layer]:
                    comp_id = comp.get('id', comp['name'].replace(' ', '_'))
                    comp_name = comp.get('name', '')
                    lines.append(f'        {comp_id}["{comp_name}"]')
                
                lines.append('    end')
        
        # Add connections
        if 'connections' in data:
            for conn in data['connections']:
                from_comp = conn['from']
                to_comp = conn['to']
                label = conn.get('label', '')
                if label:
                    lines.append(f'    {from_comp} -->|{label}| {to_comp}')
                else:
                    lines.append(f'    {from_comp} --> {to_comp}')
        
        lines.append('```')
        return '\n'.join(lines)
    
    def _generate_process_flow(self, data: Dict[str, Any], **kwargs) -> str:
        """Generate process flow diagram"""
        steps = data.get('steps', [])
        
        lines = [
            '```mermaid',
            'flowchart LR'
        ]
        
        # Generate steps
        step_ids = []
        for i, step in enumerate(steps):
            step_id = f"step{i+1}"
            step_name = step.get('name', f'Step {i+1}')
            step_type = step.get('type', 'process')  # process, decision, start, end
            
            if step_type == 'decision':
                lines.append(f'    {step_id}{{{step_name}}}')
            elif step_type == 'start':
                lines.append(f'    {step_id}([{step_name}])')
            elif step_type == 'end':
                lines.append(f'    {step_id}([{step_name}])')
            else:
                lines.append(f'    {step_id}[{step_name}]')
            
            step_ids.append(step_id)
        
        # Add connections
        for i in range(len(step_ids) - 1):
            lines.append(f'    {step_ids[i]} --> {step_ids[i+1]}')
        
        # Add decision paths if any
        if 'decisions' in data:
            for decision in data['decisions']:
                from_step = decision['from']
                to_step = decision['to']
                condition = decision.get('condition', '')
                lines.append(f'    {from_step} -->|{condition}| {to_step}')
        
        lines.append('```')
        return '\n'.join(lines)
    
    def _generate_hierarchy_tree(self, data: Dict[str, Any], **kwargs) -> str:
        """Generate hierarchical tree diagram"""
        root = data.get('root', {})
        
        lines = [
            '```mermaid',
            'graph TD'
        ]
        
        def add_node(node, parent_id=None):
            node_id = node.get('id', node['name'].replace(' ', '_'))
            node_name = node.get('name', '')
            
            lines.append(f'    {node_id}["{node_name}"]')
            
            if parent_id:
                lines.append(f'    {parent_id} --> {node_id}')
            
            # Add children
            children = node.get('children', [])
            for child in children:
                add_node(child, node_id)
        
        add_node(root)
        lines.append('```')
        return '\n'.join(lines)


def generate_parasol_phase_diagram():
    """Generate Parasol 8-phase diagram using modular engine"""
    if MODULAR_ENGINE_AVAILABLE:
        try:
            return generate_diagram("parasol_8_phases")
        except Exception as e:
            logger.warning(f"Modular engine failed, using fallback: {e}")
    
    # フォールバック：従来のハードコード版
    return _generate_parasol_phase_diagram_fallback()

def generate_six_axis_system():
    """Generate 6-axis system diagram using modular engine"""
    if MODULAR_ENGINE_AVAILABLE:
        try:
            return generate_diagram("six_axis_system")
        except Exception as e:
            logger.warning(f"Modular engine failed, using fallback: {e}")
    
    # フォールバック：従来のハードコード版
    return _generate_six_axis_system_fallback()

def _generate_parasol_phase_diagram_fallback():
    """Fallback 8-phase diagram - Left-aligned icons with visible text"""
    
    html_diagram = """<div class="parasol-flow-diagram" style="
        margin: 15px auto;
        padding: 12px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-width: 220px;
    ">
        <h4 style="text-align: center; color: #333; margin: 0 0 10px 0; font-size: 1.0em;">
            🏗️ Parasol V5 - 8フェーズプロセス (Fallback)
        </h4>
        
        <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
            <!-- Phase 0-1: Business Context -->
            <div style="
                background: #fce4ec;
                border: 2px solid #c2185b;
                border-radius: 6px;
                padding: 6px 8px;
                width: 150px;
                height: 30px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 1.4em; flex-shrink: 0;">🎯</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #333; line-height: 1.2;">Phase 0-1</div>
                    <div style="font-size: 0.85em; color: #666; line-height: 1.0;">事業コンテキスト</div>
                </div>
            </div>
            
            <div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>
            
            <!-- Phase 2: Value Discovery -->
            <div style="
                background: #e3f2fd;
                border: 2px solid #1976d2;
                border-radius: 6px;
                padding: 6px 8px;
                width: 150px;
                height: 30px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 1.4em; flex-shrink: 0;">💎</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #333; line-height: 1.2;">Phase 2</div>
                    <div style="font-size: 0.85em; color: #666; line-height: 1.0;">価値発見</div>
                </div>
            </div>
            
            <div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>
            
            <!-- Phase 3: Capability Definition -->
            <div style="
                background: #e8f5e9;
                border: 2px solid #388e3c;
                border-radius: 6px;
                padding: 6px 8px;
                width: 150px;
                height: 30px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 1.4em; flex-shrink: 0;">⚙️</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #333; line-height: 1.2;">Phase 3</div>
                    <div style="font-size: 0.85em; color: #666; line-height: 1.0;">ケイパビリティ定義</div>
                </div>
            </div>
            
            <div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>
            
            <!-- Phase 4: Architecture -->
            <div style="
                background: #fff3e0;
                border: 2px solid #f57c00;
                border-radius: 6px;
                padding: 6px 8px;
                width: 150px;
                height: 30px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 1.4em; flex-shrink: 0;">🏛️</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #333; line-height: 1.2;">Phase 4</div>
                    <div style="font-size: 0.85em; color: #666; line-height: 1.0;">アーキテクチャ設計</div>
                </div>
            </div>
            
            <div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>
            
            <!-- Phase 5: Software Design -->
            <div style="
                background: #f3e5f5;
                border: 2px solid #7b1fa2;
                border-radius: 6px;
                padding: 6px 8px;
                width: 150px;
                height: 30px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 1.4em; flex-shrink: 0;">💻</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #333; line-height: 1.2;">Phase 5</div>
                    <div style="font-size: 0.85em; color: #666; line-height: 1.0;">ソフトウェア設計</div>
                </div>
            </div>
            
            <div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>
            
            <!-- Phase 6: Implementation -->
            <div style="
                background: #e8eaf6;
                border: 2px solid #3f51b5;
                border-radius: 6px;
                padding: 6px 8px;
                width: 150px;
                height: 30px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 1.4em; flex-shrink: 0;">🔨</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #333; line-height: 1.2;">Phase 6</div>
                    <div style="font-size: 0.85em; color: #666; line-height: 1.0;">実装</div>
                </div>
            </div>
            
            <div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>
            
            <!-- Phase 7: Platform -->
            <div style="
                background: #e0f2f1;
                border: 2px solid #00796b;
                border-radius: 6px;
                padding: 6px 8px;
                width: 150px;
                height: 30px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 1.4em; flex-shrink: 0;">☁️</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #333; line-height: 1.2;">Phase 7</div>
                    <div style="font-size: 0.85em; color: #666; line-height: 1.0;">プラットフォーム</div>
                </div>
            </div>
            
            <div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>
            
            <!-- System Complete -->
            <div style="
                background: #e1f5fe;
                border: 3px solid #01579b;
                border-radius: 6px;
                padding: 8px 10px;
                width: 160px;
                height: 32px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 0.85em;
                box-shadow: 0 4px 8px rgba(1,87,155,0.3);
            ">
                <div style="font-size: 1.5em; flex-shrink: 0;">🎉</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: #01579b; line-height: 1.2;">システム完成</div>
                    <div style="font-size: 0.9em; color: #01579b; line-height: 1.0;">価値の実現</div>
                </div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 8px; font-size: 0.7em; color: #666;">
            ※ 各フェーズは価値にトレース可能
        </div>
    </div>"""
    
    return html_diagram

def _generate_six_axis_system_fallback():
    """Fallback 6-axis system diagram - Table format"""
    
    html_diagram = """<div class="six-axis-system" style="
        margin: 20px auto;
        padding: 15px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-width: 600px;
    ">
        <h4 style="text-align: center; color: #333; margin: 0 0 15px 0; font-size: 1.1em;">
            📊 6軸システム (Fallback)
        </h4>
        
        <!-- ヘッダー -->
        <div style="
            display: flex;
            background: #495057;
            color: white;
            font-weight: bold;
            border-radius: 6px 6px 0 0;
            font-size: 0.85em;
        ">
            <div style="flex: 2; padding: 10px 12px; border-right: 1px solid #6c757d;">軸</div>
            <div style="flex: 3; padding: 10px 12px;">問い</div>
        </div>
        
        <!-- テーブル本体 -->
        <div style="
            border: 1px solid #dee2e6;
            border-top: none;
            border-radius: 0 0 6px 6px;
            overflow: hidden;
        ">
            <!-- Why -->
            <div style="
                display: flex;
                background: #fff;
                border-bottom: 1px solid #dee2e6;
                font-size: 0.8em;
            ">
                <div style="flex: 2; padding: 10px 12px; font-weight: bold; color: #dc3545; border-right: 1px solid #dee2e6;">
                    ❓ Why（目的・意義）
                </div>
                <div style="flex: 3; padding: 10px 12px;">
                    なぜこのシステムが必要なのか？ビジネス価値は何か？
                </div>
            </div>
            
            <!-- What -->
            <div style="
                display: flex;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                font-size: 0.8em;
            ">
                <div style="flex: 2; padding: 10px 12px; font-weight: bold; color: #fd7e14; border-right: 1px solid #dee2e6;">
                    🎯 What（機能・要件）
                </div>
                <div style="flex: 3; padding: 10px 12px;">
                    何を実現するのか？どんな機能が必要か？
                </div>
            </div>
            
            <!-- How -->
            <div style="
                display: flex;
                background: #fff;
                border-bottom: 1px solid #dee2e6;
                font-size: 0.8em;
            ">
                <div style="flex: 2; padding: 10px 12px; font-weight: bold; color: #ffc107; border-right: 1px solid #dee2e6;">
                    🔧 How（実現方法）
                </div>
                <div style="flex: 3; padding: 10px 12px;">
                    どのように実装するか？技術的アプローチは？
                </div>
            </div>
            
            <!-- Who -->
            <div style="
                display: flex;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                font-size: 0.8em;
            ">
                <div style="flex: 2; padding: 10px 12px; font-weight: bold; color: #28a745; border-right: 1px solid #dee2e6;">
                    👥 Who（関係者）
                </div>
                <div style="flex: 3; padding: 10px 12px;">
                    誰が使うのか？誰が開発するか？ステークホルダーは？
                </div>
            </div>
            
            <!-- When -->
            <div style="
                display: flex;
                background: #fff;
                border-bottom: 1px solid #dee2e6;
                font-size: 0.8em;
            ">
                <div style="flex: 2; padding: 10px 12px; font-weight: bold; color: #17a2b8; border-right: 1px solid #dee2e6;">
                    ⏰ When（時期・期限）
                </div>
                <div style="flex: 3; padding: 10px 12px;">
                    いつまでに完成させるか？フェーズ分けは？
                </div>
            </div>
            
            <!-- Where -->
            <div style="
                display: flex;
                background: #f8f9fa;
                font-size: 0.8em;
            ">
                <div style="flex: 2; padding: 10px 12px; font-weight: bold; color: #6610f2; border-right: 1px solid #dee2e6;">
                    📍 Where（環境・制約）
                </div>
                <div style="flex: 3; padding: 10px 12px;">
                    どこで動作するか？制約条件は？既存システムとの関係は？
                </div>
            </div>
        </div>
        
        <!-- インサイト -->
        <div style="
            margin-top: 15px;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        ">
            <h5 style="margin: 0 0 8px 0; color: #333; font-size: 0.9em;">💡 軸の組み合わせによる発見</h5>
            <div style="font-size: 0.75em; line-height: 1.4; color: #555;">
                <p style="margin: 4px 0;">
                    <strong style="color: #dc3545;">Why × What</strong>
                    → ビジネス価値と機能の整合性を確認
                </p>
                <p style="margin: 4px 0;">
                    <strong style="color: #fd7e14;">What × How</strong>
                    → 要件と技術的実現性のバランスを検証
                </p>
                <p style="margin: 4px 0;">
                    <strong style="color: #28a745;">Who × When</strong>
                    → リソースとスケジュールの現実性を評価
                </p>
                <p style="margin: 4px 0;">
                    <strong style="color: #6610f2;">Where × How</strong>
                    → 制約条件下での最適な実装方法を模索
                </p>
            </div>
        </div>
    </div>"""
    
    return html_diagram


if __name__ == '__main__':
    # Test the phase diagram generation
    print(generate_parasol_phase_diagram())
    print("\n" + "="*50 + "\n")
    print(generate_six_axis_system())