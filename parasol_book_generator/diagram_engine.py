"""
モジュラー図表生成エンジン
設定ベースで様々な図表を生成
"""

from typing import Dict, List, Any, Optional
import json
import logging
try:
    from .diagram_config import (
        DiagramDefinition, DiagramType, ColorTheme, StyleConfig,
        get_diagram_definition, get_style_config, DIAGRAM_DEFINITIONS
    )
except ImportError:
    from diagram_config import (
        DiagramDefinition, DiagramType, ColorTheme, StyleConfig,
        get_diagram_definition, get_style_config, DIAGRAM_DEFINITIONS
    )

logger = logging.getLogger(__name__)

class DiagramEngine:
    """図表生成エンジン"""
    
    def __init__(self):
        self.generators = {
            DiagramType.FLOW_CHART: self._generate_flow_chart,
            DiagramType.TABLE: self._generate_table,
            DiagramType.HIERARCHY: self._generate_hierarchy,
            DiagramType.COMPARISON: self._generate_comparison,
            DiagramType.TIMELINE: self._generate_timeline,
            DiagramType.MATRIX: self._generate_matrix,
            DiagramType.CARD_LAYOUT: self._generate_card_layout,
            DiagramType.NETWORK: self._generate_network
        }
    
    def generate_diagram(self, diagram_name: str, custom_data: Optional[Dict] = None) -> str:
        """
        図表を生成
        
        Args:
            diagram_name: 図表名（diagram_config.pyで定義済み）
            custom_data: カスタムデータ（定義をオーバーライド）
        
        Returns:
            HTML文字列
        """
        # 図表定義を取得
        definition = get_diagram_definition(diagram_name)
        if not definition:
            logger.error(f"Unknown diagram: {diagram_name}")
            return f"<!-- Unknown diagram: {diagram_name} -->"
        
        # カスタムデータでオーバーライド
        if custom_data:
            definition.data_structure.update(custom_data)
        
        # 図表タイプに応じて生成
        generator = self.generators.get(definition.type)
        if not generator:
            logger.error(f"No generator for diagram type: {definition.type}")
            return f"<!-- No generator for type: {definition.type} -->"
        
        try:
            return generator(definition)
        except Exception as e:
            logger.error(f"Failed to generate diagram {diagram_name}: {e}")
            return f"<!-- Failed to generate diagram: {diagram_name} -->"
    
    def _generate_flow_chart(self, definition: DiagramDefinition) -> str:
        """フローチャート生成"""
        style = get_style_config(definition.style_theme)
        data = definition.data_structure
        layout = definition.layout_options
        
        # コンテナスタイル
        container_style = f"""
            margin: {style.margin};
            padding: 15px;
            background: {style.background};
            border-radius: {style.border_radius};
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: {layout.get('max_width', style.max_width)};
            font-family: 'Hiragino Sans', 'Yu Gothic', 'Meiryo', sans-serif;
        """
        
        html_parts = [f'<div class="diagram-flow-chart" style="{container_style}">']
        
        # タイトル
        html_parts.append(f'''
            <h4 style="text-align: center; color: {style.text_color}; margin: 0 0 15px 0; font-size: 1.1em;">
                {definition.title}
            </h4>
        ''')
        
        # フロー部分のコンテナ
        flow_container_style = f"""
            display: flex;
            flex-direction: {layout.get('direction', 'vertical')};
            align-items: center;
            justify-content: center;
            gap: {layout.get('gap', '8px')};
        """
        
        html_parts.append(f'<div style="{flow_container_style}">')
        
        # フェーズボックス生成
        phases = data.get('phases', [])
        color_groups = data.get('color_groups', {})
        
        for i, phase in enumerate(phases):
            # カラーグループから色を取得
            color_group = color_groups.get(phase.get('color_group', 'default'), {})
            bg_color = color_group.get('bg', '#f8f9fa')
            border_color = color_group.get('border', style.border_color)
            
            # アイコン位置に応じてレイアウト調整
            if layout.get('icon_position') == 'left':
                box_layout = 'flex'
                box_align = 'align-items: center; gap: 8px;'
                icon_style = 'font-size: 1.4em; flex-shrink: 0;'
                text_layout = 'flex: 1;'
            else:
                box_layout = 'flex'
                box_align = 'flex-direction: column; justify-content: center;'
                icon_style = 'font-size: 1.2em;'
                text_layout = ''
            
            box_style = f"""
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: {style.border_radius};
                padding: 6px 8px;
                width: {layout.get('box_width', '150px')};
                height: {layout.get('box_height', '30px')};
                display: {box_layout};
                {box_align}
                font-size: {style.font_size};
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            """
            
            html_parts.append(f'<div style="{box_style}">')
            html_parts.append(f'<div style="{icon_style}">{phase.get("icon", "")}</div>')
            
            if text_layout:
                html_parts.append(f'<div style="{text_layout}">')
                html_parts.append(f'<div style="font-weight: bold; color: {style.text_color}; line-height: 1.2;">{phase.get("title", "")}</div>')
                html_parts.append(f'<div style="font-size: 0.85em; color: #666; line-height: 1.0;">{phase.get("description", "")}</div>')
                html_parts.append('</div>')
            else:
                html_parts.append(f'<div style="font-weight: bold; color: {style.text_color};">{phase.get("title", "")}</div>')
                html_parts.append(f'<div style="font-size: 0.8em; color: #666;">{phase.get("description", "")}</div>')
            
            html_parts.append('</div>')
            
            # 矢印追加（最後以外）
            if i < len(phases) - 1:
                html_parts.append('<div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>')
        
        # 完成ボックス（もしあれば）
        completion = data.get('completion')
        if completion:
            html_parts.append('<div style="color: #666; font-size: 0.8em; margin: 0; line-height: 1;">↓</div>')
            
            completion_style = f"""
                background: #e1f5fe;
                border: 3px solid {style.primary_color};
                border-radius: {style.border_radius};
                padding: 8px 10px;
                width: 160px;
                height: 32px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 0.85em;
                box-shadow: 0 4px 8px rgba(1,87,155,0.3);
            """
            
            html_parts.append(f'<div style="{completion_style}">')
            html_parts.append(f'<div style="font-size: 1.5em; flex-shrink: 0;">{completion.get("icon", "")}</div>')
            html_parts.append('<div style="flex: 1;">')
            html_parts.append(f'<div style="font-weight: bold; color: {style.primary_color}; line-height: 1.2;">{completion.get("title", "")}</div>')
            html_parts.append(f'<div style="font-size: 0.9em; color: {style.primary_color}; line-height: 1.0;">{completion.get("description", "")}</div>')
            html_parts.append('</div></div>')
        
        html_parts.append('</div>')  # フローコンテナ終了
        
        # サマリー（もしあれば）
        if 'summary' in data:
            html_parts.append(f'''
                <div style="text-align: center; margin-top: 8px; font-size: 0.7em; color: #666;">
                    {data['summary']}
                </div>
            ''')
        
        html_parts.append('</div>')  # メインコンテナ終了
        
        return ''.join(html_parts)
    
    def _generate_table(self, definition: DiagramDefinition) -> str:
        """テーブル生成"""
        style = get_style_config(definition.style_theme)
        data = definition.data_structure
        layout = definition.layout_options
        
        container_style = f"""
            margin: {style.margin};
            padding: 15px;
            background: {style.background};
            border-radius: {style.border_radius};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: {style.max_width};
            font-family: 'Hiragino Sans', 'Yu Gothic', 'Meiryo', sans-serif;
        """
        
        html_parts = [f'<div class="diagram-table" style="{container_style}">']
        
        # タイトル
        html_parts.append(f'''
            <h4 style="text-align: center; color: {style.text_color}; margin: 0 0 15px 0; font-size: 1.1em;">
                {definition.title}
            </h4>
        ''')
        
        # ヘッダー生成
        if layout.get('show_header', True) and 'headers' in data:
            header_style = f"""
                display: flex;
                background: {style.header_bg};
                color: white;
                font-weight: bold;
                border-radius: {style.border_radius} {style.border_radius} 0 0;
                font-size: 0.85em;
            """
            html_parts.append(f'<div style="{header_style}">')
            
            headers = data['headers']
            for i, header in enumerate(headers):
                flex_value = "2" if i == 0 else "3"  # 最初の列を狭く
                border_style = "border-right: 1px solid #6c757d;" if i < len(headers) - 1 else ""
                html_parts.append(f'<div style="flex: {flex_value}; padding: 10px 12px; {border_style}">{header}</div>')
            
            html_parts.append('</div>')
        
        # テーブル本体
        table_body_style = f"""
            border: 1px solid {style.border_color};
            border-top: none;
            border-radius: 0 0 {style.border_radius} {style.border_radius};
            overflow: hidden;
        """
        html_parts.append(f'<div style="{table_body_style}">')
        
        # 行生成
        rows = data.get('rows', [])
        for i, row in enumerate(rows):
            # 交互背景色
            if layout.get('alternating_rows') and i % 2 == 1:
                bg_color = "#f8f9fa"
            else:
                bg_color = row.get('color', '#ffffff')
            
            border_bottom = "border-bottom: 1px solid " + style.border_color + ";" if i < len(rows) - 1 else ""
            
            row_style = f"""
                display: flex;
                background: {bg_color};
                {border_bottom}
                font-size: {style.font_size};
            """
            
            html_parts.append(f'<div style="{row_style}">')
            
            # セル内容（軸名）
            text_color = row.get('text_color', style.text_color)
            html_parts.append(f'''
                <div style="flex: 2; padding: {style.padding}; font-weight: bold; color: {text_color}; border-right: 1px solid {style.border_color};">
                    {row.get('axis', '')}
                </div>
            ''')
            
            # セル内容（説明）
            html_parts.append(f'''
                <div style="flex: 3; padding: {style.padding};">
                    {row.get('question', '')}
                </div>
            ''')
            
            html_parts.append('</div>')
        
        html_parts.append('</div>')  # テーブル本体終了
        
        # インサイトセクション
        if layout.get('show_insights') and 'insights' in data:
            insights_style = f"""
                margin-top: 15px;
                padding: 12px;
                background: #f8f9fa;
                border-radius: {style.border_radius};
                border-left: 4px solid {style.primary_color};
            """
            
            html_parts.append(f'<div style="{insights_style}">')
            html_parts.append('<h5 style="margin: 0 0 8px 0; color: #333; font-size: 0.9em;">💡 軸の組み合わせによる発見</h5>')
            html_parts.append('<div style="font-size: 0.75em; line-height: 1.4; color: #555;">')
            
            for insight in data['insights']:
                html_parts.append(f'''
                    <p style="margin: 4px 0;">
                        <strong style="color: {insight.get('color', style.primary_color)};">{insight['combination']}</strong>
                        → {insight['example']}
                    </p>
                ''')
            
            html_parts.append('</div></div>')
        
        html_parts.append('</div>')  # メインコンテナ終了
        
        return ''.join(html_parts)
    
    def _generate_hierarchy(self, definition: DiagramDefinition) -> str:
        """階層構造図生成"""
        # TODO: 実装
        return f"<!-- Hierarchy diagram '{definition.name}' not yet implemented -->"
    
    def _generate_comparison(self, definition: DiagramDefinition) -> str:
        """比較表生成"""
        # TODO: 実装
        return f"<!-- Comparison diagram '{definition.name}' not yet implemented -->"
    
    def _generate_timeline(self, definition: DiagramDefinition) -> str:
        """タイムライン生成"""
        # TODO: 実装
        return f"<!-- Timeline diagram '{definition.name}' not yet implemented -->"
    
    def _generate_matrix(self, definition: DiagramDefinition) -> str:
        """マトリックス図生成"""
        # TODO: 実装
        return f"<!-- Matrix diagram '{definition.name}' not yet implemented -->"
    
    def _generate_card_layout(self, definition: DiagramDefinition) -> str:
        """カードレイアウト生成"""
        # TODO: 実装
        return f"<!-- Card layout diagram '{definition.name}' not yet implemented -->"
    
    def _generate_network(self, definition: DiagramDefinition) -> str:
        """ネットワーク図生成"""
        # TODO: 実装
        return f"<!-- Network diagram '{definition.name}' not yet implemented -->"

# グローバルエンジンインスタンス
_engine = DiagramEngine()

def generate_diagram(name: str, custom_data: Optional[Dict] = None) -> str:
    """図表生成のショートカット関数"""
    return _engine.generate_diagram(name, custom_data)

def list_available_diagrams() -> List[str]:
    """利用可能な図表一覧"""
    return list(DIAGRAM_DEFINITIONS.keys())

# 後方互換性のための関数
def generate_parasol_phase_diagram():
    """8フェーズ図表生成（後方互換）"""
    return generate_diagram("parasol_8_phases")

def generate_six_axis_system():
    """6軸システム生成（後方互換）"""
    return generate_diagram("six_axis_system")