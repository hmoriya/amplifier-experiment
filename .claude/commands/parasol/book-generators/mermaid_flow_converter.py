#!/usr/bin/env python3
"""
Convert various flow diagrams to Mermaid format
"""

import re
from typing import List, Dict, Tuple, Optional


class MermaidFlowConverter:
    """Convert text-based flow diagrams to Mermaid format"""
    
    def __init__(self):
        self.flow_patterns = []
    
    def convert_to_mermaid(self, text: str) -> str:
        """Main conversion method"""
        # Detect and convert hierarchical flows
        if self._is_hierarchical_flow(text):
            return self._convert_hierarchical_flow(text)
        
        # Detect and convert process flows
        if self._is_process_flow(text):
            return self._convert_process_flow(text)
        
        # Detect and convert ASCII box flows
        if self._is_ascii_box_flow(text):
            return self._convert_ascii_box_flow(text)
        
        # Return original if no pattern matches
        return text
    
    def _is_hierarchical_flow(self, text: str) -> bool:
        """Check if text contains hierarchical flow pattern"""
        lines = text.strip().split('\n')
        # Look for patterns with arrows and indentation
        arrow_count = sum(1 for line in lines if '→' in line or '←' in line or '▼' in line or '│' in line or '↑' in line)
        # Also check for phase-based flows
        phase_count = sum(1 for line in lines if 'Phase' in line or 'フェーズ' in line)
        # Check for emoji-based flows
        emoji_flow = sum(1 for line in lines if any(emoji in line for emoji in ['🏠', '🔨', '🎨', '📐', '🏗️', '✏️', '🎯', '🔍', '📋']))
        # Check for architectural flow indicators
        architectural_indicators = ['建築', '構築', '設計', '施工', '完成したシステム']
        architectural_count = sum(1 for line in lines for indicator in architectural_indicators if indicator in line)
        # Check for section separators (━━━)
        separator_count = sum(1 for line in lines if '━' in line)
        
        return (arrow_count >= 1 and any('[' in line and ']' in line for line in lines)) or \
               (phase_count >= 3) or \
               (emoji_flow >= 3) or \
               (architectural_count >= 2 and separator_count >= 2) or \
               ('理想のシステムを建築する' in text)
    
    def _convert_hierarchical_flow(self, text: str) -> str:
        """Convert hierarchical flow to Mermaid"""
        lines = text.strip().split('\n')
        mermaid_lines = ['```mermaid', 'flowchart TD']
        
        # Extract title if present
        title_line = lines[0] if lines else ""
        if '[' in title_line and ']' in title_line:
            # Extract title from brackets
            title_match = re.search(r'\[([^\]]+)\]', title_line)
            if title_match:
                title = title_match.group(1)
                # Skip title line
                lines = lines[1:]
        
        # Process flow elements
        phases = []
        current_section = ""
        
        for line in lines:
            # Skip empty lines and pure decorative lines
            if not line.strip() or line.strip() == '↑' or all(c in '━─═・ ' for c in line.strip()):
                continue
                
            # Check for section headers (text that's not emoji-prefixed)
            if ('フェーズ' in line or 'Phase' in line) and not any(emoji in line for emoji in ['🏠', '🔨', '🎨', '📐', '🏗️', '✏️', '🎯', '🔍', '📋']):
                current_section = line.strip()
                continue
            
            # Extract phase content (emoji + text)
            if any(emoji in line for emoji in ['🏠', '🔨', '🎨', '📐', '🏗️', '✏️', '🎯', '🔍', '📋']):
                clean_line = line.strip()
                
                # Parse the line to extract emoji and description
                emoji_match = re.search(r'([🏠🔨🎨📐🏗️✏️🎯🔍📋])\s*(.*)', clean_line)
                if emoji_match:
                    emoji = emoji_match.group(1)
                    description = emoji_match.group(2).strip()
                    
                    # Create phase entry
                    if emoji == '🏠':
                        phase_id = "goal"
                        phase_text = "完成したシステム"
                    elif 'Phase' in description:
                        phase_match = re.search(r'Phase (\d+):\s*(.*)', description)
                        if phase_match:
                            phase_num = phase_match.group(1)
                            phase_desc = phase_match.group(2).strip()
                            phase_id = f"phase{phase_num}"
                            phase_text = f"Phase {phase_num}<br/>{phase_desc}"
                        else:
                            phase_id = f"phase{len(phases)}"
                            phase_text = description
                    else:
                        # Look for the pattern "Phase X:" in the description
                        if ':' in description:
                            parts = description.split(':', 1)
                            if len(parts) == 2:
                                phase_name = parts[0].strip()
                                phase_desc = parts[1].strip()
                                phase_id = f"phase{len(phases)}"
                                phase_text = f"{phase_name}<br/>{phase_desc}"
                            else:
                                phase_id = f"phase{len(phases)}"
                                phase_text = description
                        else:
                            phase_id = f"phase{len(phases)}"
                            phase_text = description
                    
                    phases.append((phase_id, phase_text))
            
            # Handle non-emoji lines that might contain phase info
            elif 'Phase' in line and ':' in line:
                phase_match = re.search(r'Phase (\d+):\s*(.*)', line.strip())
                if phase_match:
                    phase_num = phase_match.group(1)
                    phase_desc = phase_match.group(2).strip()
                    phase_id = f"phase{phase_num}"
                    phase_text = f"Phase {phase_num}<br/>{phase_desc}"
                    phases.append((phase_id, phase_text))
            
            # Handle lines with meaningful content that might be phases
            elif line.strip() and not line.strip().startswith('━') and 'フェーズ' not in line:
                # This might be a multi-line description
                content = line.strip()
                if content and len(content) > 3:  # Meaningful content
                    # If previous phases exist, this might be a description for the last phase
                    if phases and len(phases) > 0:
                        # Check if this looks like a continuation
                        if not any(char in content for char in ['Phase', ':', '━']):
                            # Update the last phase with additional description
                            last_phase_id, last_phase_text = phases[-1]
                            if '<br/>' not in last_phase_text and len(last_phase_text) < 30:
                                phases[-1] = (last_phase_id, f"{last_phase_text}<br/>{content}")
        
        # If no phases found, create a simple fallback
        if not phases:
            phases = [("goal", "システム完成")]
        
        # Generate Mermaid nodes (reverse order for bottom-up flow)
        phases.reverse()
        for i, (phase_id, phase_text) in enumerate(phases):
            if i == 0:  # Top level (goal)
                mermaid_lines.append(f'    {phase_id}["{phase_text}"]')
                mermaid_lines.append(f'    style {phase_id} fill:#e1f5fe,stroke:#01579b,stroke-width:2px')
            else:
                mermaid_lines.append(f'    {phase_id}["{phase_text}"]')
                mermaid_lines.append(f'    style {phase_id} fill:#f3e5f5,stroke:#4a148c,stroke-width:1px')
        
        # Add connections (bottom to top)
        for i in range(len(phases) - 1):
            current_id = phases[i + 1][0]
            next_id = phases[i][0]
            mermaid_lines.append(f'    {current_id} --> {next_id}')
        
        mermaid_lines.append('```')
        return '\n'.join(mermaid_lines)
    
    def _is_process_flow(self, text: str) -> bool:
        """Check if text contains process flow in table format"""
        lines = text.strip().split('\n')
        # Look for table with process steps
        return any('ステップ' in line or '処理' in line for line in lines) and '|' in text
    
    def _convert_process_flow(self, text: str) -> str:
        """Convert process flow table to Mermaid"""
        lines = text.strip().split('\n')
        mermaid_lines = ['```mermaid', 'flowchart LR']
        
        # Find the table content
        table_started = False
        steps = []
        
        for line in lines:
            if '|' in line and not all(c in '|-' for c in line.replace(' ', '')):
                # This is a content row
                cells = [cell.strip() for cell in line.split('|')]
                cells = [c for c in cells if c]  # Remove empty cells
                
                if len(cells) >= 2 and not any(word in cells[0] for word in ['ステップ', '観点']):
                    # This is a data row
                    step_name = cells[1] if len(cells) > 1 else cells[0]
                    step_detail = cells[2] if len(cells) > 2 else ""
                    steps.append((step_name, step_detail))
        
        # Create nodes and connections
        for i, (name, detail) in enumerate(steps):
            node_id = f"step{i+1}"
            if detail:
                mermaid_lines.append(f'    {node_id}["{name}<br/>{detail}"]')
            else:
                mermaid_lines.append(f'    {node_id}["{name}"]')
            
            if i > 0:
                mermaid_lines.append(f'    step{i} --> {node_id}')
        
        mermaid_lines.append('```')
        return '\n'.join(mermaid_lines)
    
    def _is_ascii_box_flow(self, text: str) -> bool:
        """Check if text contains ASCII box flow"""
        # Look for box drawing characters
        box_chars = '┌├└┼┬┴┤┐┘─━│'
        return any(char in text for char in box_chars)
    
    def _convert_ascii_box_flow(self, text: str) -> str:
        """Convert ASCII box flow to Mermaid"""
        lines = text.strip().split('\n')
        mermaid_lines = ['```mermaid', 'flowchart TD']
        
        # Extract content from ASCII boxes
        content_lines = []
        for line in lines:
            if '│' in line and not all(c in '─━┌├└┼┬┴┤┐┘│ ' for c in line):
                # Extract content between vertical bars
                parts = line.split('│')
                for part in parts:
                    content = part.strip()
                    if content and not all(c in '─━' for c in content):
                        content_lines.append(content)
        
        # Group content into nodes
        current_node = []
        nodes = []
        
        for content in content_lines:
            if content.startswith('★') or content.startswith('▼'):
                if current_node:
                    nodes.append('<br/>'.join(current_node))
                    current_node = []
                current_node.append(content)
            else:
                current_node.append(content)
        
        if current_node:
            nodes.append('<br/>'.join(current_node))
        
        # Create Mermaid nodes
        for i, node_content in enumerate(nodes):
            node_id = f"box{i+1}"
            # Clean up special characters
            node_content = node_content.replace('★', '').strip()
            mermaid_lines.append(f'    {node_id}["{node_content}"]')
        
        # Add simple linear connections
        for i in range(len(nodes) - 1):
            mermaid_lines.append(f'    box{i+1} --> box{i+2}')
        
        mermaid_lines.append('```')
        return '\n'.join(mermaid_lines)
    
    def convert_document(self, content: str) -> str:
        """Convert all flow diagrams in a document"""
        # Find potential flow diagram blocks
        lines = content.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            # Check for code block start
            if lines[i].strip() == '```':
                # Check if this is a flow diagram in a code block
                if i + 1 < len(lines) and self._could_be_flow_start(lines[i+1:]):
                    flow_block, end_idx = self._extract_flow_block(lines[i:])
                    if flow_block:
                        # Try to convert it
                        converted = self.convert_to_mermaid('\n'.join(flow_block))
                        if converted != '\n'.join(flow_block):
                            # Replace the code block with mermaid
                            result_lines.extend(converted.split('\n'))
                            i += end_idx
                            continue
            
            # Check if this might be the start of a non-code block flow diagram
            elif self._could_be_flow_start(lines[i:]):
                # Extract the flow block
                flow_block, end_idx = self._extract_flow_block(lines[i:])
                
                if flow_block:
                    # Try to convert it
                    converted = self.convert_to_mermaid('\n'.join(flow_block))
                    if converted != '\n'.join(flow_block):
                        # Conversion successful
                        result_lines.extend(converted.split('\n'))
                        i += end_idx
                        continue
            
            result_lines.append(lines[i])
            i += 1
        
        return '\n'.join(result_lines)
    
    def _could_be_flow_start(self, lines: List[str]) -> bool:
        """Check if the current position could be the start of a flow diagram"""
        if not lines:
            return False
        
        # Check for common flow diagram indicators in the next few lines
        preview = '\n'.join(lines[:10])
        
        indicators = [
            '価値トレーサビリティ',
            '階層構造',
            '処理フロー',
            '→', '←', '▼', '│', '↑',
            '┌', '├', '└',
            'ステップ',
            # Architectural flow indicators
            '建築', '構築', '設計', '施工', '完成したシステム',
            # Emoji indicators
            '🏠', '🔨', '🎨', '📐', '🏗️', '✏️', '🎯', '🔍', '📋',
            # Specific flow titles
            '理想のシステムを建築する',
            # Phase indicators
            'Phase', 'フェーズ',
            # Section separators
            '━'
        ]
        
        return any(indicator in preview for indicator in indicators)
    
    def _extract_flow_block(self, lines: List[str]) -> Tuple[List[str], int]:
        """Extract a complete flow diagram block"""
        flow_lines = []
        
        # For code blocks - check if it contains flow elements
        if lines[0].strip() == '```':
            block_lines = []
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '```':
                    # Check if this code block contains flow elements
                    block_content = '\n'.join(lines[1:i])
                    if self._is_hierarchical_flow(block_content) or self._is_process_flow(block_content) or self._is_ascii_box_flow(block_content):
                        return lines[1:i], i+1
                    return [], 0
            return [], 0
        
        # For non-code block flows
        in_flow = False
        empty_line_count = 0
        
        for i, line in enumerate(lines):
            # Check if we're in a flow
            if not in_flow and any(char in line for char in '→←▼│┌├└'):
                in_flow = True
            
            if in_flow:
                if line.strip() == '':
                    empty_line_count += 1
                    if empty_line_count > 1:
                        # End of flow
                        return flow_lines, i
                else:
                    empty_line_count = 0
                flow_lines.append(line)
            elif flow_lines:
                # We've collected some lines but current line doesn't look like flow
                return flow_lines, i
        
        return flow_lines, len(lines)


def main():
    """Test the converter"""
    test_flow = """
価値トレーサビリティの階層構造
================================

  [価値ストリーム]        ← 最上位：ビジネス価値
       購買判断支援
           │
           ▼
    [ケイパビリティ]      ← 能力の定義
    商品評価情報管理
           │
           ▼
  [Bounded Context]      ← ドメイン境界
  レビュー管理コンテキスト
           │
           ▼
      [Service]          ← 技術実装
    レビューサービス
           │
           ▼
        [API]            ← インターフェース
    POST /reviews
    GET /products/{id}/reviews
"""
    
    converter = MermaidFlowConverter()
    result = converter.convert_to_mermaid(test_flow)
    print(result)


if __name__ == "__main__":
    main()