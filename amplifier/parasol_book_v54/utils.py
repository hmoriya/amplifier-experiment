"""Utility functions for book generation."""

import os
import re
import hashlib
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import unicodedata


def ensure_directory(path: str) -> None:
    """Ensure a directory exists, creating it if necessary."""
    Path(path).mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to be filesystem safe."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"|?*]', '', filename)
    filename = filename.replace('/', '-')
    filename = filename.replace('\\', '-')
    # Remove control characters
    filename = ''.join(ch for ch in filename if unicodedata.category(ch)[0] != 'C')
    return filename.strip()


def calculate_word_count(text: str) -> int:
    """Calculate word count for Japanese text.
    
    Japanese doesn't use spaces, so we count characters for CJK
    and words for other languages.
    """
    # Count CJK characters
    cjk_chars = 0
    for char in text:
        if '\u4e00' <= char <= '\u9fff' or \
           '\u3040' <= char <= '\u309f' or \
           '\u30a0' <= char <= '\u30ff':
            cjk_chars += 1
    
    # Count non-CJK words
    non_cjk_text = re.sub(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]+', ' ', text)
    words = len(non_cjk_text.split())
    
    # For Japanese text, characters are roughly equivalent to words
    return cjk_chars + words


def calculate_page_count(text: str, words_per_page: int = 500) -> int:
    """Calculate estimated page count from text."""
    word_count = calculate_word_count(text)
    return max(1, (word_count + words_per_page - 1) // words_per_page)


def extract_front_matter(markdown_text: str) -> Tuple[Dict[str, any], str]:
    """Extract YAML front matter from markdown text.
    
    Returns:
        Tuple of (front_matter_dict, content_without_front_matter)
    """
    if not markdown_text.startswith('---'):
        return {}, markdown_text
    
    try:
        # Find the closing ---
        end_index = markdown_text.find('\n---\n', 3)
        if end_index == -1:
            return {}, markdown_text
        
        front_matter_text = markdown_text[3:end_index]
        content = markdown_text[end_index + 5:]
        
        # Simple YAML parsing (for basic key: value pairs)
        front_matter = {}
        for line in front_matter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip()
        
        return front_matter, content
    except Exception:
        return {}, markdown_text


def format_chapter_number(number: int) -> str:
    """Format chapter number for display."""
    return f"第{number}章"


def format_part_number(number: int) -> str:
    """Format part number for display using Roman numerals."""
    roman_numerals = [
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    result = ''
    for value, numeral in roman_numerals:
        count, number = divmod(number, value)
        result += numeral * count
    return f"第{result}部"


def generate_toc_entry(chapter_id: str, title: str, page_number: int, level: int = 1) -> str:
    """Generate a table of contents entry."""
    indent = '  ' * (level - 1)
    dots = '.' * (50 - len(title) - len(str(page_number)))
    return f"{indent}{title} {dots} {page_number}"


def validate_mermaid_syntax(mermaid_code: str) -> Tuple[bool, Optional[str]]:
    """Basic validation of Mermaid diagram syntax.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not mermaid_code.strip():
        return False, "Empty diagram"
    
    # Check for basic Mermaid diagram types
    valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
                   'stateDiagram', 'erDiagram', 'gantt', 'pie', 'mindmap']
    
    first_line = mermaid_code.strip().split('\n')[0].strip()
    has_valid_type = any(first_line.startswith(t) for t in valid_types)
    
    if not has_valid_type:
        return False, f"Invalid diagram type. First line: {first_line}"
    
    # Check for balanced brackets/parentheses
    brackets = {'[': ']', '{': '}', '(': ')'}
    stack = []
    
    for char in mermaid_code:
        if char in brackets.keys():
            stack.append(char)
        elif char in brackets.values():
            if not stack:
                return False, "Unbalanced closing bracket"
            last = stack.pop()
            if brackets[last] != char:
                return False, f"Mismatched brackets: {last} and {char}"
    
    if stack:
        return False, f"Unclosed brackets: {stack}"
    
    return True, None


def create_chapter_id(part_number: int, chapter_number: int, title: str) -> str:
    """Create a standardized chapter ID."""
    # Simplify title for ID
    simple_title = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    simple_title = re.sub(r'\s+', '-', simple_title).lower()
    simple_title = simple_title[:30]  # Limit length
    
    return f"chapter{chapter_number}-{simple_title}"


def calculate_content_hash(content: str) -> str:
    """Calculate hash of content for caching."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]


def format_cross_reference(target_chapter: str, reference_type: str = "see") -> str:
    """Format a cross-reference link."""
    reference_texts = {
        "see": "参照",
        "refer": "詳細は",
        "detail": "詳しくは", 
        "example": "例として"
    }
    
    ref_text = reference_texts.get(reference_type, "参照")
    return f"[{ref_text}: {target_chapter}](#{target_chapter})"


def wrap_in_details(content: str, summary: str) -> str:
    """Wrap content in HTML details element for collapsible sections."""
    return f"""<details>
<summary>{summary}</summary>

{content}
</details>"""


def create_breadcrumb(part_title: str, chapter_title: Optional[str] = None) -> str:
    """Create breadcrumb navigation."""
    breadcrumb = f"[Parasol V5.4 完全ガイド](../index.md) > [{part_title}](index.md)"
    if chapter_title:
        breadcrumb += f" > {chapter_title}"
    return breadcrumb