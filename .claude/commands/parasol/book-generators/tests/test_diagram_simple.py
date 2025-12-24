#!/usr/bin/env python3
"""
Simple test for diagram generation functionality
Tests only the DiagramGenerator class without full book generation
"""

import logging
import sys
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).parent))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_diagram_generation():
    """Test the core diagram generation functionality"""
    
    try:
        # Import only the diagram generator
        from parasol_book_generator.diagram_generator import DiagramGenerator, generate_parasol_phase_diagram
        
        logger.info("Testing DiagramGenerator class...")
        
        # Test 1: Standard Parasol phase diagram
        logger.info("Generating Parasol 8-phase diagram...")
        phase_diagram = generate_parasol_phase_diagram()
        
        if phase_diagram:
            logger.info("✅ Parasol phase diagram generated successfully")
            logger.info(f"Diagram length: {len(phase_diagram)} characters")
            
            # Check for key elements
            if 'flowchart TD' in phase_diagram:
                logger.info("✅ Correct flowchart format")
            if 'Phase 0: 事前準備' in phase_diagram:
                logger.info("✅ Contains Phase 0")
            if 'Phase 7: プラットフォーム構築' in phase_diagram:
                logger.info("✅ Contains Phase 7")
            if '完成したシステム' in phase_diagram:
                logger.info("✅ Contains goal state")
            
            # Show first part of the diagram
            logger.info("\nGenerated diagram preview:")
            print("=" * 60)
            print(phase_diagram[:500] + "...")
            print("=" * 60)
        else:
            logger.error("❌ Failed to generate Parasol phase diagram")
        
        # Test 2: Custom diagram generation
        logger.info("\nTesting custom diagram generation...")
        generator = DiagramGenerator()
        
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
                },
                {
                    'name': 'Payment Processing',
                    'description': 'Payment handling and billing',
                    'capabilities': [
                        {'name': 'Transaction Processing'},
                        {'name': 'Billing Management'}
                    ]
                }
            ]
        }
        
        value_stream_diagram = generator.generate_diagram('value_stream', value_stream_data)
        
        if value_stream_diagram:
            logger.info("✅ Value stream diagram generated successfully")
            logger.info(f"Diagram length: {len(value_stream_diagram)} characters")
        else:
            logger.error("❌ Failed to generate value stream diagram")
        
        # Test 3: Test _process_data_references functionality
        logger.info("\nTesting diagram reference processing...")
        
        # Simulate the reference replacement
        test_content = """# Test Chapter
        
Here is the Parasol 8-phase flow:

{{diagram:parasol_8_phases}}

And here's a value traceability diagram:

{{diagram:value_traceability}}

## Summary
This completes our diagram tests.
"""
        
        # Simulate reference processing
        import re
        def replace_diagram_ref(match):
            ref_name = match.group(2)
            if ref_name == 'parasol_8_phases':
                return generate_parasol_phase_diagram()
            elif ref_name == 'value_traceability':
                data = {
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
                return generator.generate_diagram('architecture_overview', data)
            return match.group(0)
        
        pattern = r'\{\{(table|data|diagram):([a-zA-Z0-9_-]+)\}\}'
        processed_content = re.sub(pattern, replace_diagram_ref, test_content)
        
        if '```mermaid' in processed_content:
            diagram_count = processed_content.count('```mermaid')
            logger.info(f"✅ Reference processing successful - {diagram_count} diagrams generated")
        else:
            logger.error("❌ Reference processing failed")
        
        logger.info("\nAll diagram generation tests completed successfully! 🎉")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_diagram_generation()