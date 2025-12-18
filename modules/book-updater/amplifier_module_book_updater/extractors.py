"""
Content extractors for latest implementations.

Extract information from commands, patterns, and examples.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional

import yaml
from rich.console import Console

console = Console()


class CommandExtractor:
    """Extract command information from parasol commands"""
    
    def __init__(self, commands_path: Path):
        self.commands_path = commands_path
    
    async def extract_all(self) -> Dict[str, Dict]:
        """Extract all command information"""
        commands = {}
        
        # Look for command markdown files
        for cmd_file in self.commands_path.glob("*.md"):
            if cmd_file.name == "README.md":
                continue
            
            cmd_info = await self.extract_command(cmd_file)
            if cmd_info:
                cmd_name = cmd_file.stem
                commands[cmd_name] = cmd_info
        
        return commands
    
    async def extract_command(self, cmd_file: Path) -> Optional[Dict]:
        """Extract information from a single command file"""
        try:
            content = cmd_file.read_text(encoding='utf-8')
            
            info = {
                "name": cmd_file.stem,
                "description": self._extract_description(content),
                "usage": self._extract_usage(content),
                "options": self._extract_options(content),
                "examples": self._extract_examples(content),
                "last_modified": cmd_file.stat().st_mtime
            }
            
            return info
        
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to extract from {cmd_file}: {e}[/yellow]")
            return None
    
    def _extract_description(self, content: str) -> str:
        """Extract command description"""
        # Look for first paragraph after title
        lines = content.split('\n')
        description_lines = []
        in_description = False
        
        for line in lines:
            if line.startswith('# '):
                in_description = True
                continue
            elif in_description and line.strip() == '':
                break
            elif in_description:
                description_lines.append(line)
        
        return ' '.join(description_lines).strip()
    
    def _extract_usage(self, content: str) -> str:
        """Extract usage pattern"""
        # Look for usage section or code block with usage
        usage_match = re.search(r'(?:Usage|使用方法|使い方).*?\n+```(?:bash)?\n(.+?)\n```', 
                              content, re.IGNORECASE | re.DOTALL)
        if usage_match:
            return usage_match.group(1).strip()
        
        # Fallback: look for parasol command pattern
        cmd_match = re.search(r'`(parasol\s+\w+[^`]*)`', content)
        if cmd_match:
            return cmd_match.group(1)
        
        return ""
    
    def _extract_options(self, content: str) -> List[Dict]:
        """Extract command options"""
        options = []
        
        # Look for options section
        options_section = re.search(r'(?:Options|オプション).*?\n(.+?)(?=\n#|\Z)', 
                                  content, re.IGNORECASE | re.DOTALL)
        if options_section:
            # Parse option lines
            option_pattern = r'^\s*(?:-{1,2}[\w-]+)(?:,\s*-{1,2}[\w-]+)?\s+(.+)$'
            for line in options_section.group(1).split('\n'):
                match = re.match(option_pattern, line)
                if match:
                    options.append({
                        "name": line.split()[0],
                        "description": match.group(1)
                    })
        
        return options
    
    def _extract_examples(self, content: str) -> List[str]:
        """Extract command examples"""
        examples = []
        
        # Find all bash code blocks that contain parasol commands
        code_blocks = re.findall(r'```(?:bash|sh)?\n(.*?)```', content, re.DOTALL)
        for block in code_blocks:
            if 'parasol' in block:
                examples.append(block.strip())
        
        return examples


class PatternExtractor:
    """Extract pattern information from pattern files"""
    
    def __init__(self, patterns_path: Path):
        self.patterns_path = patterns_path
    
    async def extract_all(self) -> Dict[str, Dict]:
        """Extract all pattern information"""
        patterns = {}
        
        # Look for pattern markdown files
        for pattern_file in self.patterns_path.glob("**/*.md"):
            if pattern_file.name == "README.md":
                continue
            
            pattern_info = await self.extract_pattern(pattern_file)
            if pattern_info:
                pattern_name = pattern_file.stem
                patterns[pattern_name] = pattern_info
        
        return patterns
    
    async def extract_pattern(self, pattern_file: Path) -> Optional[Dict]:
        """Extract information from a single pattern file"""
        try:
            content = pattern_file.read_text(encoding='utf-8')
            
            info = {
                "name": pattern_file.stem,
                "title": self._extract_title(content),
                "description": self._extract_description(content),
                "when_to_use": self._extract_when_to_use(content),
                "implementation": self._extract_implementation(content),
                "examples": self._extract_examples(content),
                "related_patterns": self._extract_related_patterns(content),
                "last_modified": pattern_file.stat().st_mtime
            }
            
            return info
        
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to extract from {pattern_file}: {e}[/yellow]")
            return None
    
    def _extract_title(self, content: str) -> str:
        """Extract pattern title"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else ""
    
    def _extract_description(self, content: str) -> str:
        """Extract pattern description"""
        # Similar to CommandExtractor._extract_description
        lines = content.split('\n')
        description_lines = []
        in_description = False
        
        for line in lines:
            if line.startswith('# '):
                in_description = True
                continue
            elif in_description and line.startswith('## '):
                break
            elif in_description and line.strip():
                description_lines.append(line)
        
        return ' '.join(description_lines).strip()
    
    def _extract_when_to_use(self, content: str) -> List[str]:
        """Extract when to use this pattern"""
        when_section = re.search(r'##\s*(?:When to Use|いつ使うか|適用場面)(.+?)(?=##|\Z)', 
                               content, re.IGNORECASE | re.DOTALL)
        if when_section:
            # Extract bullet points
            bullets = re.findall(r'^\s*[-*]\s+(.+)$', when_section.group(1), re.MULTILINE)
            return bullets
        
        return []
    
    def _extract_implementation(self, content: str) -> Dict:
        """Extract implementation details"""
        impl_section = re.search(r'##\s*(?:Implementation|実装|実装方法)(.+?)(?=##|\Z)', 
                               content, re.IGNORECASE | re.DOTALL)
        if impl_section:
            # Extract code blocks
            code_blocks = re.findall(r'```(\w+)\n(.*?)```', impl_section.group(1), re.DOTALL)
            return {
                "description": impl_section.group(1).split('```')[0].strip(),
                "code_blocks": [{"language": lang, "code": code} for lang, code in code_blocks]
            }
        
        return {}
    
    def _extract_examples(self, content: str) -> List[Dict]:
        """Extract pattern examples"""
        examples = []
        
        example_section = re.search(r'##\s*(?:Examples?|例|サンプル)(.+?)(?=##|\Z)', 
                                  content, re.IGNORECASE | re.DOTALL)
        if example_section:
            # Extract code blocks with titles
            parts = example_section.group(1).split('```')
            for i in range(0, len(parts)-1, 2):
                if i+1 < len(parts):
                    title = parts[i].strip().split('\n')[-1] if parts[i].strip() else "Example"
                    code_with_lang = parts[i+1]
                    lang_match = re.match(r'^(\w+)\n', code_with_lang)
                    if lang_match:
                        examples.append({
                            "title": title,
                            "language": lang_match.group(1),
                            "code": code_with_lang[len(lang_match.group(0)):]
                        })
        
        return examples
    
    def _extract_related_patterns(self, content: str) -> List[str]:
        """Extract related patterns"""
        related = []
        
        related_section = re.search(r'##\s*(?:Related|関連|See Also)(.+?)(?=##|\Z)', 
                                  content, re.IGNORECASE | re.DOTALL)
        if related_section:
            # Extract pattern names from links or bullets
            links = re.findall(r'\[([^\]]+)\]', related_section.group(1))
            related.extend(links)
            
            bullets = re.findall(r'^\s*[-*]\s+(.+)$', related_section.group(1), re.MULTILINE)
            for bullet in bullets:
                if bullet not in related:
                    related.append(bullet.strip())
        
        return related


class ExampleExtractor:
    """Extract examples from module implementations"""
    
    def __init__(self, modules_path: Path):
        self.modules_path = modules_path
    
    async def extract_all(self) -> Dict[str, Dict]:
        """Extract all examples from modules"""
        examples = {}
        
        # Look for example files in modules
        for example_file in self.modules_path.glob("*/examples/*.md"):
            example_info = await self.extract_example(example_file)
            if example_info:
                example_name = f"{example_file.parent.parent.name}/{example_file.stem}"
                examples[example_name] = example_info
        
        # Also look for example code files
        for code_file in self.modules_path.glob("*/examples/*.{py,ts,js}"):
            example_info = await self.extract_code_example(code_file)
            if example_info:
                example_name = f"{code_file.parent.parent.name}/{code_file.stem}"
                examples[example_name] = example_info
        
        return examples
    
    async def extract_example(self, example_file: Path) -> Optional[Dict]:
        """Extract information from example markdown file"""
        try:
            content = example_file.read_text(encoding='utf-8')
            
            info = {
                "name": example_file.stem,
                "module": example_file.parent.parent.name,
                "title": self._extract_title(content),
                "description": self._extract_description(content),
                "code_blocks": self._extract_code_blocks(content),
                "concepts": self._extract_concepts(content),
                "last_modified": example_file.stat().st_mtime
            }
            
            return info
        
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to extract from {example_file}: {e}[/yellow]")
            return None
    
    async def extract_code_example(self, code_file: Path) -> Optional[Dict]:
        """Extract information from code example file"""
        try:
            content = code_file.read_text(encoding='utf-8')
            
            # Extract docstring or header comments
            if code_file.suffix == '.py':
                doc_match = re.search(r'"""(.+?)"""', content, re.DOTALL)
                description = doc_match.group(1).strip() if doc_match else ""
            else:
                # JS/TS - look for JSDoc
                doc_match = re.search(r'/\*\*(.+?)\*/', content, re.DOTALL)
                description = doc_match.group(1).strip() if doc_match else ""
            
            info = {
                "name": code_file.stem,
                "module": code_file.parent.parent.name,
                "language": code_file.suffix[1:],  # Remove dot
                "description": description,
                "code": content,
                "last_modified": code_file.stat().st_mtime
            }
            
            return info
        
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to extract from {code_file}: {e}[/yellow]")
            return None
    
    def _extract_title(self, content: str) -> str:
        """Extract example title"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else ""
    
    def _extract_description(self, content: str) -> str:
        """Extract example description"""
        # Same as pattern extractor
        lines = content.split('\n')
        description_lines = []
        in_description = False
        
        for line in lines:
            if line.startswith('# '):
                in_description = True
                continue
            elif in_description and line.startswith('## '):
                break
            elif in_description and line.strip():
                description_lines.append(line)
        
        return ' '.join(description_lines).strip()
    
    def _extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract code blocks from content"""
        blocks = []
        
        code_block_pattern = r'```(\w*)\n(.*?)```'
        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            blocks.append({
                "language": match.group(1) or "text",
                "code": match.group(2).strip()
            })
        
        return blocks
    
    def _extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts demonstrated"""
        concepts = []
        
        # Look for concepts section
        concepts_section = re.search(r'##\s*(?:Concepts?|Key Points?|ポイント)(.+?)(?=##|\Z)', 
                                   content, re.IGNORECASE | re.DOTALL)
        if concepts_section:
            bullets = re.findall(r'^\s*[-*]\s+(.+)$', concepts_section.group(1), re.MULTILINE)
            concepts.extend(bullets)
        
        # Also look for tagged concepts
        tag_matches = re.findall(r'(?:Demonstrates?|Shows?|説明):\s*(.+)', content)
        concepts.extend(tag_matches)
        
        return concepts