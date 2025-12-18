"""
Content updaters for book chapters.

Updates book content based on analysis results.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set

from rich.console import Console

console = Console()


class ChapterUpdater:
    """Update chapter content"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    async def add_command_reference(self, chapter_file: Path, command_name: str) -> bool:
        """Add new command reference to chapter"""
        try:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find command reference section
            ref_section = re.search(r'(##\s*(?:Command Reference|コマンドリファレンス).+?)(?=##|\Z)', 
                                  content, re.IGNORECASE | re.DOTALL)
            
            if ref_section:
                # Check if command already exists
                if f'parasol {command_name}' in ref_section.group(1):
                    return False
                
                # Add new command entry
                new_entry = f"\n\n### parasol {command_name}\n\n"
                new_entry += f"V5で追加された新しいコマンドです。詳細は `/parasol {command_name} --help` を参照してください。\n"
                
                # Insert before next section or at end
                insert_pos = ref_section.end()
                new_content = content[:insert_pos] + new_entry + content[insert_pos:]
                
                # Write back
                chapter_file.write_text(new_content, encoding='utf-8')
                return True
            
            return False
            
        except Exception as e:
            console.print(f"[red]Error updating {chapter_file}: {e}[/red]")
            return False
    
    async def update_pattern_reference(self, chapter_file: Path, pattern_name: str, 
                                     pattern_info: Dict) -> bool:
        """Update pattern reference in chapter"""
        try:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find pattern mentions
            pattern_mentions = list(re.finditer(rf'\b{re.escape(pattern_name)}\b', content, re.IGNORECASE))
            
            if not pattern_mentions:
                return False
            
            # Update pattern descriptions
            for mention in reversed(pattern_mentions):  # Reverse to maintain positions
                # Check context
                context_start = max(0, mention.start() - 200)
                context_end = min(len(content), mention.end() + 200)
                context = content[context_start:context_end]
                
                # If this is in a code block, skip
                if '```' in context:
                    code_block_before = context[:mention.start() - context_start].rfind('```')
                    code_block_after = context[mention.end() - context_start:].find('```')
                    if code_block_before > -1 and code_block_after > -1:
                        continue
                
                # Update if needed based on pattern info
                if pattern_info.get("deprecated"):
                    # Add deprecation notice
                    notice = f" (注意: このパターンは非推奨です。{pattern_info.get('alternative', '')}を使用してください)"
                    content = content[:mention.end()] + notice + content[mention.end():]
            
            # Write back if changed
            if content != chapter_file.read_text(encoding='utf-8'):
                chapter_file.write_text(content, encoding='utf-8')
                return True
            
            return False
            
        except Exception as e:
            console.print(f"[red]Error updating pattern in {chapter_file}: {e}[/red]")
            return False


class CodeBlockUpdater:
    """Update code blocks in documentation"""
    
    def __init__(self):
        self.language_validators = {
            'python': self._validate_python,
            'typescript': self._validate_typescript,
            'javascript': self._validate_javascript,
        }
    
    async def update_example(self, file_path: Path, example_name: str) -> bool:
        """Update a specific example in file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Find example by name (in comment or heading)
            example_pattern = rf'(?:#|//)\s*(?:Example:|例:)\s*{re.escape(example_name)}'
            example_match = re.search(example_pattern, content, re.IGNORECASE)
            
            if not example_match:
                return False
            
            # Find the code block containing this example
            # Look for the next code block after the example marker
            code_block_pattern = r'```(\w*)\n(.*?)```'
            code_blocks = list(re.finditer(code_block_pattern, content[example_match.end():], re.DOTALL))
            
            if not code_blocks:
                return False
            
            # Get the first code block after example marker
            first_block = code_blocks[0]
            language = first_block.group(1) or 'text'
            old_code = first_block.group(2)
            
            # Get new code from latest implementation
            new_code = await self._get_latest_example_code(example_name, language)
            
            if new_code and new_code != old_code:
                # Replace code block
                start_pos = example_match.end() + first_block.start()
                end_pos = example_match.end() + first_block.end()
                
                new_block = f"```{language}\n{new_code}\n```"
                new_content = content[:start_pos] + new_block + content[end_pos:]
                
                # Validate new code
                if language in self.language_validators:
                    if not self.language_validators[language](new_code):
                        console.print(f"[yellow]Warning: New code for {example_name} has validation issues[/yellow]")
                
                file_path.write_text(new_content, encoding='utf-8')
                return True
            
            return False
            
        except Exception as e:
            console.print(f"[red]Error updating example in {file_path}: {e}[/red]")
            return False
    
    async def _get_latest_example_code(self, example_name: str, language: str) -> Optional[str]:
        """Get latest example code from implementation"""
        # This would fetch from the actual implementation
        # For now, return None (would be implemented with actual logic)
        return None
    
    def _validate_python(self, code: str) -> bool:
        """Basic Python code validation"""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    
    def _validate_typescript(self, code: str) -> bool:
        """Basic TypeScript validation (syntax only)"""
        # Simple validation - check for common issues
        # Real validation would use TypeScript compiler
        return not any([
            'var ' in code,  # Prefer const/let
            'function(' in code and '=>' not in code,  # Prefer arrow functions
        ])
    
    def _validate_javascript(self, code: str) -> bool:
        """Basic JavaScript validation"""
        # Similar to TypeScript but less strict
        return True


class TerminologyUpdater:
    """Update terminology throughout the book"""
    
    def __init__(self, terminology_config: Dict):
        self.glossary = terminology_config.get("glossary", {})
        self.strict_mode = terminology_config.get("strict_mode", False)
    
    async def update_all(self, book_path: Path, old_term: str, new_term: str) -> List[str]:
        """Update terminology across all files"""
        updated_files = []
        
        # Process all markdown files
        for md_file in book_path.glob("**/*.md"):
            if await self.update_file(md_file, old_term, new_term):
                updated_files.append(str(md_file.relative_to(book_path)))
        
        return updated_files
    
    async def update_file(self, file_path: Path, old_term: str, new_term: str) -> bool:
        """Update terminology in a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Create pattern for whole word matching
            # Handle both English and Japanese
            if self._is_japanese(old_term):
                # Japanese terms don't need word boundaries
                pattern = re.escape(old_term)
            else:
                # English terms use word boundaries
                pattern = r'\b' + re.escape(old_term) + r'\b'
            
            # Replace with case preservation
            def replace_with_case(match):
                matched_text = match.group(0)
                if matched_text.isupper():
                    return new_term.upper()
                elif matched_text[0].isupper():
                    return new_term[0].upper() + new_term[1:]
                else:
                    return new_term
            
            # Perform replacement
            content = re.sub(pattern, replace_with_case, content, flags=re.IGNORECASE)
            
            # Write back if changed
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                return True
            
            return False
            
        except Exception as e:
            console.print(f"[red]Error updating terminology in {file_path}: {e}[/red]")
            return False
    
    def _is_japanese(self, text: str) -> bool:
        """Check if text contains Japanese characters"""
        return bool(re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]', text))
    
    async def validate_terminology(self, book_path: Path) -> List[Dict]:
        """Validate terminology usage across the book"""
        issues = []
        
        if not self.glossary:
            return issues
        
        # Check each file
        for md_file in book_path.glob("**/*.md"):
            content = md_file.read_text(encoding='utf-8')
            
            # Check for incorrect usage
            for correct_term, variations in self.glossary.items():
                for variation in variations:
                    if variation != correct_term and variation in content:
                        issues.append({
                            "file": str(md_file.relative_to(book_path)),
                            "incorrect": variation,
                            "correct": correct_term,
                            "occurrences": content.count(variation)
                        })
        
        return issues