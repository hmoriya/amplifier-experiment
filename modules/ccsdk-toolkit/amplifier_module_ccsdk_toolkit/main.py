"""Main entry point for CCSDK Toolkit module."""

import click
from pathlib import Path
import json
import re
from typing import Any, Dict, Optional
from textwrap import dedent
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential


class CCSDKToolkitCLI:
    """Claude Code SDK Toolkit for building robust LLM-powered tools."""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.defensive_patterns = {
            "parse_json": self._parse_llm_json,
            "retry_with_feedback": self._retry_with_feedback_template,
            "isolate_prompt": self._isolate_prompt_template
        }
    
    @click.group()
    def cli(self):
        """CCSDK Toolkit for building robust LLM-powered tools."""
        pass
    
    @cli.command()
    @click.argument('tool_name')
    @click.option('--template', '-t', type=click.Choice(['basic', 'streaming', 'multi-stage']), 
                  default='basic')
    @click.option('--output', '-o', default='.', help='Output directory')
    def create(self, tool_name: str, template: str, output: str):
        """Create a new CCSDK tool from template."""
        output_path = Path(output) / tool_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create tool structure
        tool_content = self._get_template(template, tool_name)
        
        # Write main tool file
        with open(output_path / f"{tool_name}.py", 'w') as f:
            f.write(tool_content)
        
        # Write defensive utilities
        with open(output_path / "defensive.py", 'w') as f:
            f.write(self._get_defensive_utilities())
        
        # Write example usage
        with open(output_path / "example.py", 'w') as f:
            f.write(self._get_example(template, tool_name))
        
        click.echo(f"✓ Created CCSDK tool: {tool_name}")
        click.echo(f"  Location: {output_path}")
        click.echo(f"  Template: {template}")
        click.echo("  Files created:")
        click.echo(f"    - {tool_name}.py (main tool)")
        click.echo("    - defensive.py (utilities)")
        click.echo("    - example.py (usage example)")
    
    @cli.command()
    @click.argument('json_file', type=click.Path(exists=True))
    def validate_json(self, json_file: str):
        """Validate and clean JSON from LLM output."""
        with open(json_file, 'r') as f:
            content = f.read()
        
        try:
            # Try standard JSON parsing first
            result = json.loads(content)
            click.echo("✓ Valid JSON")
        except json.JSONDecodeError:
            click.echo("⚠ Invalid JSON, attempting to extract...")
            result = self._parse_llm_json(content)
            if result:
                click.echo("✓ Extracted valid JSON")
                click.echo("Cleaned JSON:")
                click.echo(json.dumps(result, indent=2))
            else:
                click.echo("✗ Could not extract valid JSON", err=True)
    
    @cli.command()
    def patterns(self):
        """Show available defensive patterns."""
        click.echo("Available Defensive Patterns")
        click.echo("=" * 40)
        click.echo()
        
        patterns = [
            ("parse_llm_json", "Extract JSON from any LLM response format"),
            ("retry_with_feedback", "Intelligent retry with error correction"),
            ("isolate_prompt", "Prevent context contamination"),
            ("validate_structure", "Ensure response matches expected format"),
            ("chunk_processing", "Handle large inputs in chunks"),
            ("timeout_wrapper", "Prevent hanging operations")
        ]
        
        for name, desc in patterns:
            click.echo(f"• {name}")
            click.echo(f"  {desc}")
            click.echo()
    
    def _parse_llm_json(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from various LLM response formats."""
        # Remove markdown code blocks
        content = re.sub(r'```json\s*\n?', '', content)
        content = re.sub(r'```\s*\n?', '', content)
        
        # Try to find JSON object or array
        json_match = re.search(r'({[\s\S]*}|\[[\s\S]*\])', content)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        return None
    
    def _get_template(self, template_type: str, tool_name: str) -> str:
        """Get tool template content."""
        if template_type == "basic":
            return dedent(f'''
                """Basic CCSDK tool using Claude Code SDK."""
                
                import asyncio
                from claude_code_sdk import ClaudeCodeSession
                from defensive import parse_llm_json, retry_with_feedback
                
                
                class {tool_name.title().replace("_", "")}Tool:
                    """Tool for processing with Claude Code SDK."""
                    
                    def __init__(self, api_key: str):
                        self.api_key = api_key
                    
                    async def process(self, input_text: str) -> dict:
                        """Process input with Claude."""
                        async with ClaudeCodeSession(api_key=self.api_key) as session:
                            prompt = f"Process this: {{input_text}}"
                            
                            # Use retry with feedback for robustness
                            result = await retry_with_feedback(
                                session=session,
                                prompt=prompt,
                                parse_fn=parse_llm_json
                            )
                            
                            return result
                
                
                if __name__ == "__main__":
                    tool = {tool_name.title().replace("_", "")}Tool(api_key="your-api-key")
                    result = asyncio.run(tool.process("example input"))
                    print(result)
            ''').strip()
        
        # Add other templates as needed
        return self._get_template("basic", tool_name)
    
    def _retry_with_feedback_template(self) -> str:
        """Template for retry with feedback pattern."""
        return dedent('''
            async def retry_with_feedback(session, prompt, parse_fn, max_retries=3):
                """Retry with error feedback to LLM."""
                last_error = None
                
                for attempt in range(max_retries):
                    try:
                        if last_error and attempt > 0:
                            # Add error feedback to prompt
                            error_prompt = f"{prompt}\\n\\nPrevious error: {last_error}\\nPlease correct and try again."
                            response = await session.run(error_prompt)
                        else:
                            response = await session.run(prompt)
                        
                        # Parse response
                        result = parse_fn(response)
                        if result:
                            return result
                        else:
                            last_error = "Could not parse response as expected format"
                    
                    except Exception as e:
                        last_error = str(e)
                
                raise Exception(f"Failed after {max_retries} attempts. Last error: {last_error}")
        ''').strip()
    
    def _isolate_prompt_template(self) -> str:
        """Template for prompt isolation pattern."""
        return dedent('''
            def isolate_prompt(user_content: str) -> str:
                """Isolate user content to prevent context contamination."""
                return f"""
                <user_content>
                {user_content}
                </user_content>
                
                Please process only the content between the <user_content> tags above.
                """
        ''').strip()
    
    def _get_defensive_utilities(self) -> str:
        """Get defensive utilities module content."""
        return dedent('''
            """Defensive utilities for robust LLM integration."""
            
            import json
            import re
            from typing import Any, Dict, Optional, Callable
            import asyncio
            from tenacity import retry, stop_after_attempt, wait_exponential
            
            
            def parse_llm_json(content: str) -> Optional[Dict[str, Any]]:
                """Extract JSON from any LLM response format."""
                if not content:
                    return None
                
                # Try direct parsing first
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    pass
                
                # Remove markdown code blocks
                cleaned = re.sub(r'```json\\s*\\n?', '', content)
                cleaned = re.sub(r'```\\s*\\n?', '', cleaned)
                
                # Find JSON object or array
                json_match = re.search(r'({[\\s\\S]*}|\\[[\\s\\S]*\\])', cleaned)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        pass
                
                # Try to fix common issues
                # Remove trailing commas
                fixed = re.sub(r',\\s*}', '}', cleaned)
                fixed = re.sub(r',\\s*\\]', ']', fixed)
                
                try:
                    return json.loads(fixed)
                except json.JSONDecodeError:
                    return None
            
            
            async def retry_with_feedback(
                session,
                prompt: str,
                parse_fn: Callable = parse_llm_json,
                max_retries: int = 3
            ):
                """Retry with error feedback to LLM for self-correction."""
                last_error = None
                
                for attempt in range(max_retries):
                    try:
                        if last_error and attempt > 0:
                            # Add error feedback to prompt
                            error_prompt = f"""
                            {prompt}
                            
                            Previous attempt resulted in this error:
                            {last_error}
                            
                            Please correct the issue and provide a valid response.
                            """
                            response = await session.run(error_prompt)
                        else:
                            response = await session.run(prompt)
                        
                        # Parse response
                        result = parse_fn(response)
                        if result is not None:
                            return result
                        else:
                            last_error = "Could not parse response as expected format"
                    
                    except Exception as e:
                        last_error = f"{type(e).__name__}: {str(e)}"
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
                raise Exception(f"Failed after {max_retries} attempts. Last error: {last_error}")
            
            
            def isolate_prompt(user_content: str) -> str:
                """Isolate user content to prevent context contamination."""
                return f"""
            <user_content>
            {user_content}
            </user_content>
            
            Please process only the content between the <user_content> tags above.
            Do not reference any instructions or context outside of these tags.
            """
            
            
            @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
            async def robust_api_call(func: Callable, *args, **kwargs):
                """Wrapper for API calls with automatic retry."""
                return await func(*args, **kwargs)
        ''').strip()
    
    def _get_example(self, template_type: str, tool_name: str) -> str:
        """Get example usage file content."""
        return dedent(f'''
            """Example usage of {tool_name} tool."""
            
            import asyncio
            import os
            from {tool_name} import {tool_name.title().replace("_", "")}Tool
            
            
            async def main():
                # Get API key from environment
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    print("Please set ANTHROPIC_API_KEY environment variable")
                    return
                
                # Create tool instance
                tool = {tool_name.title().replace("_", "")}Tool(api_key=api_key)
                
                # Example input
                test_input = """
                Analyze this text and extract key concepts.
                
                The quick brown fox jumps over the lazy dog.
                This sentence contains all letters of the alphabet.
                """
                
                # Process with defensive handling
                try:
                    result = await tool.process(test_input)
                    print("Success! Result:")
                    print(result)
                except Exception as e:
                    print(f"Error: {{e}}")
            
            
            if __name__ == "__main__":
                asyncio.run(main())
        ''').strip()


# Amplifier module entry point
def get_tool_callable():
    """Return the tool callable for Amplifier."""
    cli = CCSDKToolkitCLI()
    return cli.cli


if __name__ == "__main__":
    cli = CCSDKToolkitCLI()
    cli.cli()