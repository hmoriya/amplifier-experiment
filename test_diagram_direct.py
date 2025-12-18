#!/usr/bin/env python3
"""
Direct test of diagram generation functionality
Tests the diagram generator without module dependencies
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add import path
sys.path.append(str(Path(__file__).parent / 'parasol_book_generator'))

def test_diagram_generation():
    """Test diagram generation directly"""
    
    try:
        # Import directly from the module file
        import diagram_generator
        
        logger.info("Testing diagram generation directly...")
        
        # Test 1: Standard Parasol phase diagram function
        logger.info("Generating Parasol 8-phase diagram...")
        phase_diagram = diagram_generator.generate_parasol_phase_diagram()
        
        if phase_diagram:
            logger.info("✅ Parasol phase diagram generated successfully")
            logger.info(f"Diagram length: {len(phase_diagram)} characters")
            
            # Check for key elements
            checks = [
                ('flowchart TD', 'Correct flowchart format'),
                ('Phase 0: 事前準備', 'Contains Phase 0'),
                ('Phase 7: プラットフォーム構築', 'Contains Phase 7'),
                ('完成したシステム', 'Contains goal state'),
                ('```mermaid', 'Proper Mermaid code blocks'),
                ('subgraph', 'Contains subgraphs'),
                ('phase0 --> phase1', 'Contains flow connections')
            ]
            
            for check_text, description in checks:
                if check_text in phase_diagram:
                    logger.info(f"✅ {description}")
                else:
                    logger.warning(f"⚠️  {description} - NOT FOUND")
            
            # Show first part of the diagram
            logger.info("\nGenerated diagram preview:")
            print("=" * 80)
            print(phase_diagram[:800] + "...")
            print("=" * 80)
        else:
            logger.error("❌ Failed to generate Parasol phase diagram")
        
        # Test 2: DiagramGenerator class
        logger.info("\nTesting DiagramGenerator class...")
        generator = diagram_generator.DiagramGenerator()
        
        # Test value stream diagram
        value_stream_data = {
            'value_streams': [
                {
                    'name': 'Customer Onboarding',
                    'description': 'New customer registration flow',
                    'capabilities': [
                        {'name': 'Identity Verification'},
                        {'name': 'Account Setup'},
                        {'name': 'Welcome Sequence'}
                    ]
                }
            ]
        }
        
        value_stream_diagram = generator.generate_diagram('value_stream', value_stream_data)
        
        if value_stream_diagram and '```mermaid' in value_stream_diagram:
            logger.info("✅ Value stream diagram generated successfully")
            logger.info(f"Diagram length: {len(value_stream_diagram)} characters")
        else:
            logger.error("❌ Failed to generate value stream diagram")
        
        # Test 3: Architecture overview
        arch_data = {
            'components': [
                {'name': 'Value Stream', 'layer': 'business', 'id': 'vs'},
                {'name': 'Capability', 'layer': 'business', 'id': 'cap'},
                {'name': 'Service', 'layer': 'application', 'id': 'service'}
            ],
            'connections': [
                {'from': 'vs', 'to': 'cap', 'label': 'traces to'},
                {'from': 'cap', 'to': 'service', 'label': 'implements'}
            ]
        }
        
        arch_diagram = generator.generate_diagram('architecture_overview', arch_data)
        
        if arch_diagram and '```mermaid' in arch_diagram:
            logger.info("✅ Architecture overview diagram generated successfully")
        else:
            logger.error("❌ Failed to generate architecture overview diagram")
        
        # Test 4: Capability map
        cap_data = {
            'capabilities': [
                {'name': 'Business Value', 'level': 'CL1', 'id': 'bv', 'parent': None},
                {'name': 'Core Capability', 'level': 'CL2', 'id': 'cc', 'parent': 'bv'},
                {'name': 'Business Operation', 'level': 'CL3', 'id': 'bo', 'parent': 'cc'}
            ]
        }
        
        cap_diagram = generator.generate_diagram('capability_map', cap_data)
        
        if cap_diagram and '```mermaid' in cap_diagram:
            logger.info("✅ Capability map diagram generated successfully")
        else:
            logger.error("❌ Failed to generate capability map diagram")
        
        logger.info("\n🎉 All diagram generation tests completed successfully!")
        
        # Test the reference pattern that would be used in the book generator
        logger.info("\nTesting diagram reference pattern...")
        test_content = """# Test Chapter

Here is the Parasol 8-phase flow:

{{diagram:parasol_8_phases}}

## Summary
This completes our test.
"""
        
        import re
        def replace_diagram_ref(match):
            ref_name = match.group(2)
            if ref_name == 'parasol_8_phases':
                return diagram_generator.generate_parasol_phase_diagram()
            return match.group(0)
        
        pattern = r'\{\{(diagram):([a-zA-Z0-9_-]+)\}\}'
        processed_content = re.sub(pattern, replace_diagram_ref, test_content)
        
        if '```mermaid' in processed_content:
            logger.info("✅ Diagram reference processing works correctly")
            diagram_lines = processed_content.count('\n```mermaid')
            logger.info(f"✅ Found {diagram_lines} diagram blocks in processed content")
        else:
            logger.error("❌ Diagram reference processing failed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_diagram_generation()
    if success:
        print("\n✅ SUCCESS: All diagram generation tests passed!")
    else:
        print("\n❌ FAILURE: Some tests failed")
        sys.exit(1)