"""Mermaid diagram generation for Parasol V5.4 book."""

import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import re

from .models import DiagramMetadata, ChapterMetadata
from .utils import validate_mermaid_syntax
from .constants import DIAGRAM_TYPES

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """Generates Mermaid diagrams for book chapters."""
    
    def __init__(self):
        """Initialize diagram generator."""
        self.diagram_templates = self._load_templates()
        self.generated_diagrams: List[DiagramMetadata] = []
    
    def _load_templates(self) -> Dict[str, str]:
        """Load diagram templates."""
        return {
            "phase_flow": self._phase_flow_template(),
            "value_stream": self._value_stream_template(),
            "architecture": self._architecture_template(),
            "capability_hierarchy": self._capability_hierarchy_template(),
            "design_matrix": self._design_matrix_template(),
            "zigzag_process": self._zigzag_process_template()
        }
    
    def generate_chapter_diagrams(self, chapter: ChapterMetadata) -> List[DiagramMetadata]:
        """Generate appropriate diagrams for a chapter."""
        diagrams = []
        
        # Determine which diagrams to generate based on chapter
        if "phase" in chapter.chapter_id.lower():
            diagrams.append(self._create_phase_diagram(chapter))
        
        if "value" in chapter.chapter_id.lower() and "stream" in chapter.title:
            diagrams.append(self._create_value_stream_diagram(chapter))
        
        if "architecture" in chapter.chapter_id.lower():
            diagrams.append(self._create_architecture_diagram(chapter))
        
        if "capability" in chapter.chapter_id.lower() or "cl" in chapter.chapter_id.lower():
            diagrams.append(self._create_capability_hierarchy_diagram(chapter))
        
        if "design-matrix" in chapter.chapter_id:
            diagrams.append(self._create_design_matrix_diagram(chapter))
        
        if "zigzag" in chapter.chapter_id.lower():
            diagrams.append(self._create_zigzag_diagram(chapter))
        
        # Validate all generated diagrams
        valid_diagrams = []
        for diagram in diagrams:
            is_valid, error = validate_mermaid_syntax(diagram.mermaid_code)
            if is_valid:
                valid_diagrams.append(diagram)
            else:
                logger.warning(f"Invalid diagram {diagram.id}: {error}")
        
        self.generated_diagrams.extend(valid_diagrams)
        return valid_diagrams
    
    def _create_phase_diagram(self, chapter: ChapterMetadata) -> DiagramMetadata:
        """Create a phase flow diagram."""
        # Extract phase number from chapter ID
        phase_match = re.search(r'phase(\d)', chapter.chapter_id.lower())
        phase_num = int(phase_match.group(1)) if phase_match else 0
        
        diagram_code = self._phase_flow_template(phase_num)
        
        return DiagramMetadata(
            id=f"{chapter.chapter_id}-phase-flow",
            type="flow",
            title=f"Phase {phase_num} フロー",
            description=f"Phase {phase_num}のプロセスフロー",
            chapter_id=chapter.chapter_id,
            mermaid_code=diagram_code
        )
    
    def _create_value_stream_diagram(self, chapter: ChapterMetadata) -> DiagramMetadata:
        """Create a value stream diagram."""
        diagram_code = self._value_stream_template()
        
        return DiagramMetadata(
            id=f"{chapter.chapter_id}-value-stream",
            type="flow",
            title="価値ストリームマップ",
            description="価値の流れを表すストリームマップ",
            chapter_id=chapter.chapter_id,
            mermaid_code=diagram_code
        )
    
    def _create_architecture_diagram(self, chapter: ChapterMetadata) -> DiagramMetadata:
        """Create an architecture diagram."""
        diagram_code = self._architecture_template()
        
        return DiagramMetadata(
            id=f"{chapter.chapter_id}-architecture",
            type="architecture",
            title="アーキテクチャ概要",
            description="システムアーキテクチャの概要図",
            chapter_id=chapter.chapter_id,
            mermaid_code=diagram_code
        )
    
    def _create_capability_hierarchy_diagram(self, chapter: ChapterMetadata) -> DiagramMetadata:
        """Create a capability hierarchy diagram."""
        diagram_code = self._capability_hierarchy_template()
        
        return DiagramMetadata(
            id=f"{chapter.chapter_id}-capability-hierarchy",
            type="mindmap",
            title="ケイパビリティ階層",
            description="CL0からCL3までのケイパビリティ階層",
            chapter_id=chapter.chapter_id,
            mermaid_code=diagram_code
        )
    
    def _create_design_matrix_diagram(self, chapter: ChapterMetadata) -> DiagramMetadata:
        """Create a design matrix diagram."""
        diagram_code = self._design_matrix_template()
        
        return DiagramMetadata(
            id=f"{chapter.chapter_id}-design-matrix",
            type="flow",
            title="Design Matrix",
            description="FRとDPの関係を示すDesign Matrix",
            chapter_id=chapter.chapter_id,
            mermaid_code=diagram_code
        )
    
    def _create_zigzag_diagram(self, chapter: ChapterMetadata) -> DiagramMetadata:
        """Create a ZIGZAG process diagram."""
        diagram_code = self._zigzag_process_template()
        
        return DiagramMetadata(
            id=f"{chapter.chapter_id}-zigzag",
            type="flow",
            title="ZIGZAGプロセス",
            description="FRとDPの往復による設計プロセス",
            chapter_id=chapter.chapter_id,
            mermaid_code=diagram_code
        )
    
    # Diagram templates
    
    def _phase_flow_template(self, phase: int = 0) -> str:
        """Template for phase flow diagrams."""
        if phase == 0:
            return """graph LR
    A[組織理解] --> B[ドメイン分析]
    B --> C[ステークホルダー識別]
    C --> D[現状課題の整理]
    D --> E[Phase 0 完了]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#9f9,stroke:#333,stroke-width:2px"""
        elif phase == 1:
            return """graph LR
    A[Phase 0 完了] --> B[プロジェクト立ち上げ]
    B --> C[チーム編成]
    C --> D[ツールセットアップ]
    D --> E[産業パターン選択]
    E --> F[Phase 1 完了]
    
    style A fill:#9f9,stroke:#333,stroke-width:2px
    style F fill:#9f9,stroke:#333,stroke-width:2px"""
        elif phase == 2:
            return """graph TD
    A[Phase 1 完了] --> B[価値探索]
    B --> C[価値ストリーム定義]
    C --> D[VS（価値ステージ）設計]
    D --> E[VL（価値レベル）定義]
    E --> F[価値指標設定]
    F --> G[Phase 2 完了]
    
    style A fill:#9f9,stroke:#333,stroke-width:2px
    style G fill:#9f9,stroke:#333,stroke-width:2px"""
        else:
            return """graph LR
    A[開始] --> B[分析]
    B --> C[設計]
    C --> D[実装]
    D --> E[検証]
    E --> F[完了]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#9f9,stroke:#333,stroke-width:2px"""
    
    def _value_stream_template(self) -> str:
        """Template for value stream diagrams."""
        return """graph LR
    subgraph "顧客価値"
        V1[時間短縮]
        V2[品質向上]
        V3[コスト削減]
    end
    
    subgraph "価値ステージ"
        VS1[発注]
        VS2[製造]
        VS3[配送]
        VS4[サポート]
    end
    
    subgraph "ケイパビリティ"
        C1[受注管理]
        C2[在庫管理]
        C3[配送管理]
    end
    
    V1 --> VS1
    V2 --> VS2
    V3 --> VS3
    VS1 --> C1
    VS2 --> C2
    VS3 --> C3"""
    
    def _architecture_template(self) -> str:
        """Template for architecture diagrams."""
        return """graph TB
    subgraph "UI Layer"
        UI1[Web Frontend]
        UI2[Mobile App]
    end
    
    subgraph "API Gateway"
        GW[API Gateway]
    end
    
    subgraph "Application Services"
        AS1[Order Service]
        AS2[Inventory Service]
        AS3[Delivery Service]
    end
    
    subgraph "Domain Layer"
        D1[Order Domain]
        D2[Inventory Domain]
        D3[Delivery Domain]
    end
    
    subgraph "Infrastructure"
        DB[(Database)]
        MQ[Message Queue]
        Cache[(Cache)]
    end
    
    UI1 --> GW
    UI2 --> GW
    GW --> AS1
    GW --> AS2
    GW --> AS3
    AS1 --> D1
    AS2 --> D2
    AS3 --> D3
    D1 --> DB
    D2 --> DB
    D3 --> DB
    AS1 --> MQ
    AS2 --> MQ
    AS3 --> Cache"""
    
    def _capability_hierarchy_template(self) -> str:
        """Template for capability hierarchy diagrams."""
        return """mindmap
  root((ビジネス能力))
    CL0[コアケイパビリティ]
      顧客管理
      商品管理
      受注管理
    CL1[サポートケイパビリティ]
      在庫管理
      配送管理
      請求管理
    CL2[基盤ケイパビリティ]
      認証認可
      監査
      ログ管理
    CL3[汎用ケイパビリティ]
      メール送信
      ファイル管理
      スケジュール"""
    
    def _design_matrix_template(self) -> str:
        """Template for design matrix diagrams."""
        return """graph LR
    subgraph "Functional Requirements (FR)"
        FR1[高速処理]
        FR2[高可用性]
        FR3[セキュリティ]
    end
    
    subgraph "Design Parameters (DP)"
        DP1[キャッシュ機構]
        DP2[冗長構成]
        DP3[暗号化]
    end
    
    subgraph "Design Matrix"
        M[X 0 0<br>X X 0<br>0 X X]
    end
    
    FR1 -.->|X| DP1
    FR1 -.->|X| DP2
    FR2 -.->|X| DP2
    FR2 -.->|X| DP3
    FR3 -.->|X| DP3
    
    style M fill:#ffe,stroke:#333,stroke-width:2px"""
    
    def _zigzag_process_template(self) -> str:
        """Template for ZIGZAG process diagrams."""
        return """graph TB
    subgraph "Functional Domain"
        FR1[機能要求 FR1]
        FR2[機能要求 FR2]
        FR3[機能要求 FR3]
    end
    
    subgraph "Physical Domain"
        DP1[設計パラメータ DP1]
        DP2[設計パラメータ DP2]
        DP3[設計パラメータ DP3]
    end
    
    FR1 ==>|1. 定義| DP1
    DP1 -.->|2. 影響確認| FR2
    FR2 ==>|3. 定義| DP2
    DP2 -.->|4. 影響確認| FR3
    FR3 ==>|5. 定義| DP3
    
    style FR1 fill:#f9f,stroke:#333,stroke-width:2px
    style FR2 fill:#f9f,stroke:#333,stroke-width:2px
    style FR3 fill:#f9f,stroke:#333,stroke-width:2px
    style DP1 fill:#9ff,stroke:#333,stroke-width:2px
    style DP2 fill:#9ff,stroke:#333,stroke-width:2px
    style DP3 fill:#9ff,stroke:#333,stroke-width:2px"""
    
    def get_diagram_by_id(self, diagram_id: str) -> Optional[DiagramMetadata]:
        """Get a generated diagram by ID."""
        for diagram in self.generated_diagrams:
            if diagram.id == diagram_id:
                return diagram
        return None
    
    def get_chapter_diagrams(self, chapter_id: str) -> List[DiagramMetadata]:
        """Get all diagrams for a chapter."""
        return [d for d in self.generated_diagrams if d.chapter_id == chapter_id]
    
    def export_diagram(self, diagram: DiagramMetadata, output_path: str) -> None:
        """Export diagram to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"```mermaid\n{diagram.mermaid_code}\n```\n")
            f.write(f"\n*{diagram.title}: {diagram.description}*\n")