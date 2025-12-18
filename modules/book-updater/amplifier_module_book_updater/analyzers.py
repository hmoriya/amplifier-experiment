"""
Content analyzers for book updater.

Analyzes book content to find what needs updating.
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Any

import yaml
from rich.console import Console

console = Console()


class ContentAnalyzer:
    """Analyze book content structure and elements"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        
    async def analyze_book(self, book_path: Path) -> Dict[str, Any]:
        """Analyze entire book structure and content"""
        analysis = {
            "structure": {},
            "commands": {},
            "patterns": {},
            "examples": {},
            "terms": {},
            "content": ""
        }
        
        # Analyze structure
        parts = []
        for part_dir in sorted(book_path.glob("part*")):
            if part_dir.is_dir():
                part_info = {
                    "name": part_dir.name,
                    "chapters": []
                }
                
                for chapter_file in sorted(part_dir.glob("chapter*.md")):
                    chapter_analysis = await self.analyze_chapter(chapter_file)
                    part_info["chapters"].append({
                        "file": chapter_file.name,
                        "title": chapter_analysis.get("title", "Unknown"),
                        "sections": chapter_analysis.get("sections", []),
                        "code_blocks": len(chapter_analysis.get("code_blocks", [])),
                        "links": len(chapter_analysis.get("links", []))
                    })
                    
                    # Aggregate data
                    analysis["commands"].update(chapter_analysis.get("commands", {}))
                    analysis["patterns"].update(chapter_analysis.get("patterns", {}))
                    analysis["examples"].update(chapter_analysis.get("examples", {}))
                    analysis["content"] += chapter_analysis.get("content", "")
                
                parts.append(part_info)
        
        analysis["structure"]["parts"] = parts
        
        # Extract terms
        analysis["terms"] = self._extract_terms(analysis["content"])
        
        return analysis
    
    async def analyze_chapter(self, chapter_file: Path) -> Dict[str, Any]:
        """Analyze a single chapter"""
        content = chapter_file.read_text(encoding='utf-8')
        
        analysis = {
            "title": self._extract_title(content),
            "sections": self._extract_sections(content),
            "commands": self._extract_commands(content),
            "patterns": self._extract_patterns(content),
            "examples": self._extract_code_examples(content),
            "code_blocks": self._extract_code_blocks(content),
            "links": self._extract_links(content),
            "content": content
        }
        
        return analysis
    
    def _extract_title(self, content: str) -> str:
        """Extract chapter title"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else "Unknown"
    
    def _extract_sections(self, content: str) -> List[str]:
        """Extract section headers"""
        return re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    
    def _extract_commands(self, content: str) -> Dict[str, Dict]:
        """Extract command references"""
        commands = {}
        
        # Look for command patterns like `parasol init` or `/parasol generate`
        command_pattern = r'`(?:/)?parasol\s+(\w+)(?:\s+[^`]+)?`'
        for match in re.finditer(command_pattern, content):
            cmd_name = match.group(1)
            if cmd_name not in commands:
                commands[cmd_name] = {
                    "occurrences": 0,
                    "contexts": []
                }
            commands[cmd_name]["occurrences"] += 1
            
            # Extract context (surrounding text)
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end].strip()
            commands[cmd_name]["contexts"].append(context)
        
        return commands
    
    def _extract_patterns(self, content: str) -> Dict[str, Dict]:
        """Extract pattern references"""
        patterns = {}
        
        # Look for pattern mentions
        pattern_keywords = [
            "ZIGZAG", "Event-Driven", "CQRS", "Event Sourcing",
            "フロントエンドオーケストレーション", "軽量イベント",
            "契約駆動", "再生成可能"
        ]
        
        for keyword in pattern_keywords:
            if keyword in content:
                patterns[keyword] = {
                    "occurrences": content.count(keyword),
                    "normalized_name": keyword.lower().replace(" ", "-")
                }
        
        return patterns
    
    def _extract_code_examples(self, content: str) -> Dict[str, Dict]:
        """Extract code examples with metadata"""
        examples = {}
        
        # Extract code blocks with language
        code_block_pattern = r'```(\w+)\n(.*?)```'
        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            lang = match.group(1)
            code = match.group(2)
            
            # Try to extract example name from comment or context
            name_match = re.search(r'#\s*(?:Example:|例:)\s*(.+)', code)
            if name_match:
                example_name = name_match.group(1).strip()
                examples[example_name] = {
                    "language": lang,
                    "code": code,
                    "location": f"{match.start()}-{match.end()}"
                }
        
        return examples
    
    def _extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract all code blocks"""
        blocks = []
        
        code_block_pattern = r'```(\w*)\n(.*?)```'
        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            blocks.append({
                "language": match.group(1) or "text",
                "code": match.group(2),
                "start": match.start(),
                "end": match.end()
            })
        
        return blocks
    
    def _extract_links(self, content: str) -> List[Dict]:
        """Extract all links"""
        links = []
        
        # Markdown links
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(md_link_pattern, content):
            links.append({
                "text": match.group(1),
                "url": match.group(2),
                "type": "markdown"
            })
        
        # Reference-style links
        ref_link_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
        for match in re.finditer(ref_link_pattern, content):
            links.append({
                "text": match.group(1),
                "ref": match.group(2),
                "type": "reference"
            })
        
        return links
    
    def _extract_terms(self, content: str) -> Set[str]:
        """Extract key terms and concepts"""
        # Simple term extraction - could be enhanced with NLP
        terms = set()
        
        # Extract capitalized terms
        cap_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        terms.update(cap_terms)
        
        # Extract Japanese key terms in 「」
        jp_terms = re.findall(r'「([^」]+)」', content)
        terms.update(jp_terms)
        
        return terms


class DifferenceAnalyzer:
    """Analyze differences between versions"""
    
    def __init__(self):
        self.ignore_patterns = [
            r'^\s*$',  # Empty lines
            r'^#.*$',  # Comments
            r'^\s*//.*$',  # JS comments
        ]
    
    def compare_code(self, old_code: str, new_code: str) -> Dict[str, Any]:
        """Compare two code snippets"""
        # Normalize for comparison
        old_normalized = self._normalize_code(old_code)
        new_normalized = self._normalize_code(new_code)
        
        if old_normalized == new_normalized:
            return {"identical": True}
        
        # Find differences
        old_lines = old_normalized.split('\n')
        new_lines = new_normalized.split('\n')
        
        added_lines = [line for line in new_lines if line not in old_lines]
        removed_lines = [line for line in old_lines if line not in new_lines]
        
        return {
            "identical": False,
            "added_lines": len(added_lines),
            "removed_lines": len(removed_lines),
            "similarity": self._calculate_similarity(old_normalized, new_normalized)
        }
    
    def _normalize_code(self, code: str) -> str:
        """Normalize code for comparison"""
        lines = code.split('\n')
        normalized_lines = []
        
        for line in lines:
            # Skip lines matching ignore patterns
            if any(re.match(pattern, line) for pattern in self.ignore_patterns):
                continue
            
            # Normalize whitespace
            normalized_line = ' '.join(line.split())
            if normalized_line:
                normalized_lines.append(normalized_line)
        
        return '\n'.join(normalized_lines)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity ratio"""
        # Simple character-based similarity
        longer = max(len(text1), len(text2))
        if longer == 0:
            return 1.0
        
        # Count matching characters at same positions
        matches = sum(1 for i in range(min(len(text1), len(text2))) 
                     if text1[i] == text2[i])
        
        return matches / longer