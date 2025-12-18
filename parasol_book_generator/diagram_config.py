"""
図表生成のための設定定義
データ駆動で様々な図表タイプを生成するための設定システム
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class DiagramType(Enum):
    """図表の種類"""
    FLOW_CHART = "flow_chart"           # フローチャート（プロセス図）
    TABLE = "table"                     # 表形式
    HIERARCHY = "hierarchy"             # 階層構造図
    COMPARISON = "comparison"           # 比較表
    TIMELINE = "timeline"              # タイムライン
    MATRIX = "matrix"                  # マトリックス図
    CARD_LAYOUT = "card_layout"        # カードレイアウト
    NETWORK = "network"                # ネットワーク図

class ColorTheme(Enum):
    """カラーテーマ"""
    PARASOL_DEFAULT = "parasol_default"
    BUSINESS = "business" 
    TECHNICAL = "technical"
    PROCESS = "process"
    VALUE = "value"

@dataclass
class StyleConfig:
    """スタイル設定"""
    primary_color: str
    secondary_color: str
    background: str
    border_color: str
    text_color: str
    header_bg: str
    font_size: str = "0.8em"
    border_radius: str = "8px"
    padding: str = "8px 12px"
    margin: str = "15px auto"
    max_width: str = "600px"

@dataclass 
class DiagramDefinition:
    """図表定義"""
    name: str
    type: DiagramType
    title: str
    data_structure: Dict[str, Any]
    style_theme: ColorTheme
    layout_options: Dict[str, Any]
    custom_styles: Optional[Dict[str, str]] = None

# カラーテーマ定義
COLOR_THEMES = {
    ColorTheme.PARASOL_DEFAULT: StyleConfig(
        primary_color="#01579b",
        secondary_color="#0277bd", 
        background="linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        border_color="#dee2e6",
        text_color="#333",
        header_bg="#495057"
    ),
    ColorTheme.BUSINESS: StyleConfig(
        primary_color="#2e7d32",
        secondary_color="#4caf50",
        background="linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%)",
        border_color="#81c784",
        text_color="#1b5e20",
        header_bg="#388e3c"
    ),
    ColorTheme.TECHNICAL: StyleConfig(
        primary_color="#1565c0",
        secondary_color="#1976d2",
        background="linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)",
        border_color="#64b5f6",
        text_color="#0d47a1",
        header_bg="#1976d2"
    ),
    ColorTheme.PROCESS: StyleConfig(
        primary_color="#7b1fa2", 
        secondary_color="#9c27b0",
        background="linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%)",
        border_color="#ba68c8",
        text_color="#4a148c",
        header_bg="#8e24aa"
    ),
    ColorTheme.VALUE: StyleConfig(
        primary_color="#d84315",
        secondary_color="#ff5722", 
        background="linear-gradient(135deg, #fff3e0 0%, #ffccbc 100%)",
        border_color="#ff8a65",
        text_color="#bf360c",
        header_bg="#f4511e"
    )
}

# 図表定義集
DIAGRAM_DEFINITIONS = {
    "parasol_8_phases": DiagramDefinition(
        name="parasol_8_phases",
        type=DiagramType.FLOW_CHART,
        title="🏗️ Parasol V5 - 8フェーズプロセス",
        style_theme=ColorTheme.PARASOL_DEFAULT,
        layout_options={
            "direction": "vertical",
            "box_width": "150px",
            "box_height": "30px",
            "gap": "4px",
            "icon_position": "left"
        },
        data_structure={
            "phases": [
                {"id": 0, "title": "Phase 0-1", "description": "事業コンテキスト", "icon": "🎯", "color_group": "preparation"},
                {"id": 2, "title": "Phase 2", "description": "価値発見", "icon": "💎", "color_group": "value"},
                {"id": 3, "title": "Phase 3", "description": "ケイパビリティ定義", "icon": "⚙️", "color_group": "capability"},
                {"id": 4, "title": "Phase 4", "description": "アーキテクチャ設計", "icon": "🏛️", "color_group": "architecture"},
                {"id": 5, "title": "Phase 5", "description": "ソフトウェア設計", "icon": "💻", "color_group": "software"},
                {"id": 6, "title": "Phase 6", "description": "実装", "icon": "🔨", "color_group": "implementation"},
                {"id": 7, "title": "Phase 7", "description": "プラットフォーム", "icon": "☁️", "color_group": "platform"}
            ],
            "completion": {"title": "システム完成", "description": "価値の実現", "icon": "🎉"},
            "color_groups": {
                "preparation": {"bg": "#fce4ec", "border": "#c2185b"},
                "value": {"bg": "#e3f2fd", "border": "#1976d2"},
                "capability": {"bg": "#e8f5e9", "border": "#388e3c"},
                "architecture": {"bg": "#fff3e0", "border": "#f57c00"},
                "software": {"bg": "#f3e5f5", "border": "#7b1fa2"},
                "implementation": {"bg": "#e8eaf6", "border": "#3f51b5"},
                "platform": {"bg": "#e0f2f1", "border": "#00796b"}
            },
            "summary": "※ 各フェーズは価値にトレース可能"
        }
    ),
    
    "six_axis_system": DiagramDefinition(
        name="six_axis_system", 
        type=DiagramType.TABLE,
        title="📊 6軸システム",
        style_theme=ColorTheme.PARASOL_DEFAULT,
        layout_options={
            "show_header": True,
            "alternating_rows": True,
            "show_insights": True
        },
        data_structure={
            "headers": ["軸", "問い"],
            "rows": [
                {"axis": "❓ Why（目的・意義）", "question": "なぜこのシステムが必要なのか？ビジネス価値は何か？", "text_color": "#dc3545"},
                {"axis": "🎯 What（機能・要件）", "question": "何を実現するのか？どんな機能が必要か？", "text_color": "#fd7e14"},
                {"axis": "🔧 How（実現方法）", "question": "どのように実装するか？技術的アプローチは？", "text_color": "#ffc107"},
                {"axis": "👥 Who（関係者）", "question": "誰が使うのか？誰が開発するか？ステークホルダーは？", "text_color": "#28a745"},
                {"axis": "⏰ When（時期・期限）", "question": "いつまでに完成させるか？フェーズ分けは？", "text_color": "#17a2b8"},
                {"axis": "📍 Where（環境・制約）", "question": "どこで動作するか？制約条件は？既存システムとの関係は？", "text_color": "#6610f2"}
            ],
            "insights": [
                {"combination": "Why × What", "example": "ビジネス価値と機能の整合性を確認", "color": "#dc3545"},
                {"combination": "What × How", "example": "要件と技術的実現性のバランスを検証", "color": "#fd7e14"},
                {"combination": "Who × When", "example": "リソースとスケジュールの現実性を評価", "color": "#28a745"},
                {"combination": "Where × How", "example": "制約条件下での最適な実装方法を模索", "color": "#6610f2"}
            ]
        }
    ),
    
    "capability_hierarchy": DiagramDefinition(
        name="capability_hierarchy",
        type=DiagramType.HIERARCHY,
        title="🔗 ケイパビリティ階層図",
        style_theme=ColorTheme.TECHNICAL,
        layout_options={
            "orientation": "top_down",
            "level_spacing": "40px",
            "node_spacing": "20px",
            "show_connections": True
        },
        data_structure={
            "levels": [
                {"level": 1, "name": "CL1 - 活動領域", "nodes": [
                    {"id": "customer_management", "name": "顧客管理", "description": "顧客との関係構築"}
                ]},
                {"level": 2, "name": "CL2 - ケイパビリティ", "nodes": [
                    {"id": "customer_analysis", "name": "顧客分析", "parent": "customer_management"},
                    {"id": "customer_support", "name": "顧客サポート", "parent": "customer_management"}
                ]},
                {"level": 3, "name": "CL3 - ビジネス実施", "nodes": [
                    {"id": "data_collection", "name": "データ収集", "parent": "customer_analysis"},
                    {"id": "insight_generation", "name": "洞察生成", "parent": "customer_analysis"},
                    {"id": "ticket_management", "name": "チケット管理", "parent": "customer_support"}
                ]}
            ]
        }
    ),
    
    "value_comparison": DiagramDefinition(
        name="value_comparison",
        type=DiagramType.COMPARISON,
        title="💰 価値比較表", 
        style_theme=ColorTheme.VALUE,
        layout_options={
            "comparison_type": "before_after",
            "show_metrics": True,
            "highlight_improvements": True
        },
        data_structure={
            "categories": ["売上", "コスト", "効率"],
            "comparison": {
                "before": {"売上": "1億円", "コスト": "3500万円", "効率": "65%"},
                "after": {"売上": "1.5億円", "コスト": "2500万円", "効率": "85%"},
                "improvement": {"売上": "+50%", "コスト": "-28%", "効率": "+20%"}
            }
        }
    ),
    
    "parasol_phases_simple": DiagramDefinition(
        name="parasol_phases_simple",
        type=DiagramType.CARD_LAYOUT,
        title="🏗️ Parasol V5 フェーズ概要",
        style_theme=ColorTheme.PROCESS,
        layout_options={
            "cards_per_row": 2,
            "card_spacing": "10px",
            "show_phase_numbers": True
        },
        data_structure={
            "phases": [
                {"phase": "Phase 0-1", "title": "基盤構築", "icon": "🔍", "description": "プロジェクト準備と現状分析"},
                {"phase": "Phase 2", "title": "価値設計", "icon": "🎯", "description": "ビジネス価値の発見と設計"},
                {"phase": "Phase 3", "title": "ケイパビリティ", "icon": "⚙️", "description": "能力分解と組織設計"},
                {"phase": "Phase 4-7", "title": "実装", "icon": "🔨", "description": "アーキテクチャから運用まで"}
            ]
        }
    ),
    
    "ddd_vs_parasol": DiagramDefinition(
        name="ddd_vs_parasol", 
        type=DiagramType.COMPARISON,
        title="🔄 DDDとParasol V5の関係性",
        style_theme=ColorTheme.TECHNICAL,
        layout_options={
            "comparison_type": "side_by_side",
            "show_connections": True
        },
        data_structure={
            "left_side": {
                "title": "DDD (ドメイン駆動設計)",
                "items": [
                    {"name": "Bounded Context", "description": "ドメインの境界定義"},
                    {"name": "Entity", "description": "ビジネスエンティティ"},
                    {"name": "Value Object", "description": "値オブジェクト"},
                    {"name": "Aggregate", "description": "集約単位"}
                ]
            },
            "right_side": {
                "title": "Parasol V5",
                "items": [
                    {"name": "Value Stream", "description": "価値の流れ設計"},
                    {"name": "Capability", "description": "ビジネス能力分解"},
                    {"name": "Business Context", "description": "BC実装境界"},
                    {"name": "Service", "description": "マイクロサービス"}
                ]
            },
            "connections": [
                {"from": "Bounded Context", "to": "Business Context", "label": "マッピング"},
                {"from": "Entity", "to": "Service", "label": "実装"}
            ]
        }
    )
}

def get_diagram_definition(name: str) -> Optional[DiagramDefinition]:
    """図表定義を取得"""
    return DIAGRAM_DEFINITIONS.get(name)

def get_style_config(theme: ColorTheme) -> StyleConfig:
    """スタイル設定を取得"""
    return COLOR_THEMES[theme]

def list_available_diagrams() -> List[str]:
    """利用可能な図表一覧を取得"""
    return list(DIAGRAM_DEFINITIONS.keys())