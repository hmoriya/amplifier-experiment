#!/usr/bin/env python3
"""
Test different Mermaid diagram formats for browser compatibility
"""

def test_simple_diagram():
    """Test ultra-simple diagram"""
    return """```mermaid
flowchart LR
    A[Phase 0] --> B[Phase 1] --> C[Phase 2] --> D[完成]
```"""

def test_horizontal_flow():
    """Test horizontal flow with 8 phases"""
    return """```mermaid
flowchart LR
    P0[📋 Phase 0] --> P1[🔍 Phase 1] --> P2[🎯 Phase 2] --> P3[✏️ Phase 3] --> P4[🏗️ Phase 4] --> P5[📐 Phase 5] --> P6[🎨 Phase 6] --> P7[🔨 Phase 7] --> Goal[🏠 完成]
```"""

def test_vertical_minimal():
    """Test vertical minimal"""
    return """```mermaid
graph TD
    A[開始] --> B[Phase 1] --> C[Phase 2] --> D[完了]
```"""

# Test all formats
if __name__ == '__main__':
    print("=== Simple Test ===")
    print(test_simple_diagram())
    
    print("\n=== Horizontal Test ===")
    print(test_horizontal_flow())
    
    print("\n=== Vertical Test ===")
    print(test_vertical_minimal())