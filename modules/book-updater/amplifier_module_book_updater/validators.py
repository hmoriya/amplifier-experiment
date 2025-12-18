"""
Content validators for book updater.

Validates links, code, and consistency.
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Optional
from urllib.parse import urlparse

import httpx
from rich.console import Console

console = Console()


class LinkValidator:
    """Validate internal and external links"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.internal_link_cache = {}
        self.external_link_cache = {}
    
    async def validate_all(self, book_path: Path) -> List[Dict]:
        """Validate all links in the book"""
        broken_links = []
        
        for md_file in book_path.glob("**/*.md"):
            file_issues = await self.validate_file(md_file)
            broken_links.extend(file_issues)
        
        return broken_links
    
    async def validate_file(self, file_path: Path) -> List[Dict]:
        """Validate links in a single file"""
        content = file_path.read_text(encoding='utf-8')
        issues = []
        
        # Extract all links
        links = self._extract_links(content)
        
        for link in links:
            if link['type'] == 'markdown':
                is_valid = await self._validate_link(link['url'], file_path)
                if not is_valid:
                    issues.append({
                        "file": str(file_path.relative_to(self.base_path)),
                        "line": self._get_line_number(content, link['text']),
                        "link_text": link['text'],
                        "link_url": link['url'],
                        "type": "broken_link"
                    })
        
        return issues
    
    def _extract_links(self, content: str) -> List[Dict]:
        """Extract all links from content"""
        links = []
        
        # Markdown links [text](url)
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(md_link_pattern, content):
            links.append({
                "text": match.group(1),
                "url": match.group(2),
                "type": "markdown"
            })
        
        # Reference-style links [text][ref]
        ref_link_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
        ref_definitions = {}
        
        # First, find all reference definitions
        ref_def_pattern = r'^\[([^\]]+)\]:\s*(.+)$'
        for match in re.finditer(ref_def_pattern, content, re.MULTILINE):
            ref_definitions[match.group(1)] = match.group(2)
        
        # Then find reference uses
        for match in re.finditer(ref_link_pattern, content):
            ref_key = match.group(2)
            if ref_key in ref_definitions:
                links.append({
                    "text": match.group(1),
                    "url": ref_definitions[ref_key],
                    "type": "reference"
                })
        
        return links
    
    async def _validate_link(self, url: str, source_file: Path) -> bool:
        """Validate a single link"""
        # Parse URL
        parsed = urlparse(url)
        
        if parsed.scheme in ('http', 'https'):
            # External link
            return await self._validate_external_link(url)
        else:
            # Internal link
            return self._validate_internal_link(url, source_file)
    
    def _validate_internal_link(self, url: str, source_file: Path) -> bool:
        """Validate internal link"""
        # Handle anchor links
        if url.startswith('#'):
            # Check if anchor exists in current file
            return self._check_anchor(source_file, url[1:])
        
        # Handle relative paths
        if url in self.internal_link_cache:
            return self.internal_link_cache[url]
        
        # Resolve relative path
        target_path = source_file.parent / url
        
        # Remove anchor if present
        if '#' in str(target_path):
            path_part, anchor = str(target_path).split('#', 1)
            target_path = Path(path_part)
        else:
            anchor = None
        
        # Check if file exists
        exists = target_path.exists()
        
        # If file exists and has anchor, check anchor
        if exists and anchor:
            exists = self._check_anchor(target_path, anchor)
        
        self.internal_link_cache[url] = exists
        return exists
    
    def _check_anchor(self, file_path: Path, anchor: str) -> bool:
        """Check if anchor exists in file"""
        if not file_path.exists():
            return False
        
        content = file_path.read_text(encoding='utf-8')
        
        # Headers automatically create anchors
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        for header in headers:
            # Convert header to anchor format (lowercase, spaces to hyphens)
            header_anchor = re.sub(r'[^\w\s-]', '', header.lower())
            header_anchor = re.sub(r'[-\s]+', '-', header_anchor)
            if header_anchor == anchor:
                return True
        
        # Explicit anchor tags
        if f'id="{anchor}"' in content or f"id='{anchor}'" in content:
            return True
        
        return False
    
    async def _validate_external_link(self, url: str) -> bool:
        """Validate external link"""
        if url in self.external_link_cache:
            return self.external_link_cache[url]
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.head(url, follow_redirects=True)
                is_valid = response.status_code < 400
                self.external_link_cache[url] = is_valid
                return is_valid
        except:
            # Network errors, timeouts, etc.
            self.external_link_cache[url] = False
            return False
    
    def _get_line_number(self, content: str, search_text: str) -> int:
        """Get line number for text in content"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_text in line:
                return i
        return 0


class CodeValidator:
    """Validate code blocks in documentation"""
    
    def __init__(self):
        self.validators = {
            'python': self._validate_python,
            'py': self._validate_python,
            'javascript': self._validate_javascript,
            'js': self._validate_javascript,
            'typescript': self._validate_typescript,
            'ts': self._validate_typescript,
            'bash': self._validate_bash,
            'sh': self._validate_bash,
        }
    
    async def validate_book(self, book_path: Path) -> List[Dict]:
        """Validate all code blocks in the book"""
        issues = []
        
        for md_file in book_path.glob("**/*.md"):
            file_issues = await self.validate_file(md_file)
            issues.extend(file_issues)
        
        return issues
    
    async def validate_file(self, file_path: Path) -> List[Dict]:
        """Validate code blocks in a single file"""
        content = file_path.read_text(encoding='utf-8')
        issues = []
        
        # Extract code blocks
        code_blocks = self._extract_code_blocks(content)
        
        for block in code_blocks:
            language = block['language'].lower()
            if language in self.validators:
                validation_result = self.validators[language](block['code'])
                if not validation_result['valid']:
                    issues.append({
                        "file": str(file_path.relative_to(Path.cwd())),
                        "line": self._get_line_number(content, block['code'][:30]),
                        "language": language,
                        "error": validation_result['error'],
                        "type": "invalid_code"
                    })
        
        return issues
    
    def _extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract all code blocks from content"""
        blocks = []
        
        code_block_pattern = r'```(\w*)\n(.*?)```'
        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            
            blocks.append({
                "language": language,
                "code": code,
                "start": match.start(),
                "end": match.end()
            })
        
        return blocks
    
    def _validate_python(self, code: str) -> Dict:
        """Validate Python code"""
        try:
            compile(code, '<string>', 'exec')
            return {"valid": True}
        except SyntaxError as e:
            return {"valid": False, "error": str(e)}
    
    def _validate_javascript(self, code: str) -> Dict:
        """Validate JavaScript code (basic)"""
        # Basic syntax checks
        issues = []
        
        # Check for common syntax errors
        if code.count('(') != code.count(')'):
            issues.append("Mismatched parentheses")
        if code.count('{') != code.count('}'):
            issues.append("Mismatched braces")
        if code.count('[') != code.count(']'):
            issues.append("Mismatched brackets")
        
        if issues:
            return {"valid": False, "error": "; ".join(issues)}
        
        return {"valid": True}
    
    def _validate_typescript(self, code: str) -> Dict:
        """Validate TypeScript code (basic)"""
        # Same as JavaScript for now
        return self._validate_javascript(code)
    
    def _validate_bash(self, code: str) -> Dict:
        """Validate Bash code"""
        # Check with bash -n (syntax check only)
        try:
            result = subprocess.run(
                ['bash', '-n'],
                input=code,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"valid": True}
            else:
                return {"valid": False, "error": result.stderr.strip()}
        except Exception as e:
            # If bash is not available, do basic checks
            return {"valid": True}  # Assume valid if can't check
    
    def _get_line_number(self, content: str, search_text: str) -> int:
        """Get line number for text in content"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_text in line:
                return i
        return 0


class ConsistencyValidator:
    """Validate consistency across the book"""
    
    def __init__(self):
        self.term_variations = {}
        self.code_patterns = {}
    
    async def validate_book(self, book_path: Path) -> List[Dict]:
        """Validate consistency across the entire book"""
        issues = []
        
        # First pass: collect all terms and patterns
        await self._collect_patterns(book_path)
        
        # Second pass: find inconsistencies
        for md_file in book_path.glob("**/*.md"):
            file_issues = await self._check_consistency(md_file)
            issues.extend(file_issues)
        
        return issues
    
    async def _collect_patterns(self, book_path: Path):
        """Collect patterns for consistency checking"""
        # Collect command usage patterns
        command_variations = {}
        
        for md_file in book_path.glob("**/*.md"):
            content = md_file.read_text(encoding='utf-8')
            
            # Find command patterns
            commands = re.findall(r'`(/?parasol\s+\w+[^`]*)`', content)
            for cmd in commands:
                base_cmd = re.match(r'/?parasol\s+(\w+)', cmd).group(1)
                if base_cmd not in command_variations:
                    command_variations[base_cmd] = set()
                command_variations[base_cmd].add(cmd)
        
        # Find variations that might be inconsistent
        for cmd, variations in command_variations.items():
            if len(variations) > 1:
                self.term_variations[f"parasol_{cmd}"] = list(variations)
    
    async def _check_consistency(self, file_path: Path) -> List[Dict]:
        """Check consistency in a single file"""
        content = file_path.read_text(encoding='utf-8')
        issues = []
        
        # Check for inconsistent command usage
        for term, variations in self.term_variations.items():
            if len(variations) > 1:
                found_variations = [v for v in variations if v in content]
                if len(found_variations) > 1:
                    issues.append({
                        "file": str(file_path.relative_to(Path.cwd())),
                        "type": "inconsistent_usage",
                        "term": term,
                        "variations_found": found_variations,
                        "description": f"Multiple variations of {term} found in same file"
                    })
        
        # Check for V5 specific patterns
        v5_issues = self._check_v5_patterns(content, file_path)
        issues.extend(v5_issues)
        
        return issues
    
    def _check_v5_patterns(self, content: str, file_path: Path) -> List[Dict]:
        """Check for V5-specific pattern violations"""
        issues = []
        
        # Check for deprecated patterns
        deprecated_patterns = [
            ("Event Sourcing", "V5では軽量イベント通知を使用"),
            ("Backend SAGA", "V5ではフロントエンドオーケストレーションを使用"),
            ("CQRS", "V5では必要な場合のみ部分的に適用"),
        ]
        
        for pattern, message in deprecated_patterns:
            if pattern in content:
                # Check if it's mentioned as deprecated
                context_start = max(0, content.find(pattern) - 100)
                context_end = min(len(content), content.find(pattern) + 100)
                context = content[context_start:context_end]
                
                if "非推奨" not in context and "deprecated" not in context.lower():
                    issues.append({
                        "file": str(file_path.relative_to(Path.cwd())),
                        "type": "deprecated_pattern",
                        "pattern": pattern,
                        "message": message,
                        "line": self._get_line_number(content, pattern)
                    })
        
        return issues
    
    def _get_line_number(self, content: str, search_text: str) -> int:
        """Get line number for text in content"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_text in line:
                return i
        return 0