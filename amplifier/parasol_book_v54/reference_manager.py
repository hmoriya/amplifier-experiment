"""Cross-reference management for Parasol V5.4 book."""

import logging
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import re

from .models import CrossReference, ChapterMetadata
from .utils import format_cross_reference, format_chapter_number

logger = logging.getLogger(__name__)


class ReferenceManager:
    """Manages cross-references and link integrity in the book."""
    
    def __init__(self):
        """Initialize reference manager."""
        self.references: List[CrossReference] = []
        self.reference_graph: Dict[str, Set[str]] = defaultdict(set)
        self.chapter_index: Dict[str, ChapterMetadata] = {}
        self.glossary_terms: Dict[str, str] = {}
        self.index_entries: Dict[str, List[str]] = defaultdict(list)
    
    def register_chapter(self, chapter: ChapterMetadata) -> None:
        """Register a chapter for reference tracking."""
        self.chapter_index[chapter.chapter_id] = chapter
    
    def add_reference(self, source_chapter: str, target_chapter: str, 
                     reference_text: str, reference_type: str = "see") -> None:
        """Add a cross-reference between chapters."""
        ref = CrossReference(
            source_chapter=source_chapter,
            target_chapter=target_chapter,
            reference_text=reference_text,
            reference_type=reference_type
        )
        
        self.references.append(ref)
        self.reference_graph[source_chapter].add(target_chapter)
        
        logger.debug(f"Added reference: {source_chapter} -> {target_chapter}")
    
    def add_glossary_term(self, term: str, definition: str) -> None:
        """Add a term to the glossary."""
        self.glossary_terms[term] = definition
    
    def add_index_entry(self, term: str, chapter_id: str) -> None:
        """Add an index entry."""
        if chapter_id not in self.index_entries[term]:
            self.index_entries[term].append(chapter_id)
    
    def process_chapter_content(self, chapter_id: str, content: str) -> str:
        """Process chapter content to add cross-references.
        
        Looks for patterns like:
        - [[chapter-id]] - Simple reference
        - [[chapter-id|display text]] - Reference with custom text
        - {{term}} - Glossary term
        - @{keyword} - Index entry
        """
        # Process simple references [[chapter-id]]
        def replace_simple_ref(match):
            target_id = match.group(1)
            if target_id in self.chapter_index:
                target = self.chapter_index[target_id]
                ref_text = f"{format_chapter_number(target.number)}：{target.title}"
                self.add_reference(chapter_id, target_id, ref_text)
                return format_cross_reference(ref_text, "see")
            return match.group(0)
        
        content = re.sub(r'\[\[([^\]|]+)\]\]', replace_simple_ref, content)
        
        # Process references with custom text [[chapter-id|text]]
        def replace_custom_ref(match):
            target_id = match.group(1)
            display_text = match.group(2)
            if target_id in self.chapter_index:
                self.add_reference(chapter_id, target_id, display_text)
                return format_cross_reference(display_text, "see")
            return match.group(0)
        
        content = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', replace_custom_ref, content)
        
        # Process glossary terms {{term}}
        def replace_glossary_term(match):
            term = match.group(1)
            if term in self.glossary_terms:
                return f'<abbr title="{self.glossary_terms[term]}">{term}</abbr>'
            return match.group(0)
        
        content = re.sub(r'\{\{([^}]+)\}\}', replace_glossary_term, content)
        
        # Process index entries @{keyword}
        def process_index_entry(match):
            keyword = match.group(1)
            self.add_index_entry(keyword, chapter_id)
            return f'<span class="index-term">{keyword}</span>'
        
        content = re.sub(r'@\{([^}]+)\}', process_index_entry, content)
        
        return content
    
    def generate_reference_section(self, chapter_id: str) -> str:
        """Generate the references section for a chapter."""
        outgoing_refs = [r for r in self.references if r.source_chapter == chapter_id]
        incoming_refs = [r for r in self.references if r.target_chapter == chapter_id]
        
        if not outgoing_refs and not incoming_refs:
            return ""
        
        section = "\n## 関連項目\n\n"
        
        if outgoing_refs:
            section += "### 参照先\n\n"
            for ref in outgoing_refs:
                if ref.target_chapter in self.chapter_index:
                    target = self.chapter_index[ref.target_chapter]
                    section += f"- [{format_chapter_number(target.number)}: {target.title}](#{ref.target_chapter})\n"
        
        if incoming_refs:
            section += "\n### この章を参照している章\n\n"
            for ref in incoming_refs:
                if ref.source_chapter in self.chapter_index:
                    source = self.chapter_index[ref.source_chapter]
                    section += f"- [{format_chapter_number(source.number)}: {source.title}](#{ref.source_chapter})\n"
        
        return section
    
    def generate_index(self) -> str:
        """Generate the book index."""
        if not self.index_entries:
            return ""
        
        index_content = "# 索引\n\n"
        
        # Sort terms alphabetically
        sorted_terms = sorted(self.index_entries.keys())
        
        current_section = ""
        for term in sorted_terms:
            # Group by first character
            first_char = term[0].upper()
            if first_char != current_section:
                current_section = first_char
                index_content += f"\n## {current_section}\n\n"
            
            # List chapters where term appears
            chapters = self.index_entries[term]
            chapter_refs = []
            for ch_id in chapters:
                if ch_id in self.chapter_index:
                    ch = self.chapter_index[ch_id]
                    chapter_refs.append(f"{ch.number}")
            
            if chapter_refs:
                index_content += f"- **{term}**: {", ".join(chapter_refs)}\n"
        
        return index_content
    
    def generate_glossary(self) -> str:
        """Generate the glossary."""
        if not self.glossary_terms:
            return ""
        
        glossary_content = "# 用語集\n\n"
        
        # Group terms by first character
        grouped_terms = defaultdict(list)
        for term in sorted(self.glossary_terms.keys()):
            first_char = term[0].upper()
            grouped_terms[first_char].append(term)
        
        for section in sorted(grouped_terms.keys()):
            glossary_content += f"\n## {section}\n\n"
            for term in grouped_terms[section]:
                definition = self.glossary_terms[term]
                glossary_content += f"**{term}**\n: {definition}\n\n"
        
        return glossary_content
    
    def validate_references(self) -> Tuple[bool, List[str]]:
        """Validate all references point to valid chapters.
        
        Returns:
            Tuple of (is_valid, list_of_broken_references)
        """
        broken_refs = []
        
        for ref in self.references:
            if ref.target_chapter not in self.chapter_index:
                broken_refs.append(
                    f"{ref.source_chapter} -> {ref.target_chapter} (不明な章)"
                )
        
        return len(broken_refs) == 0, broken_refs
    
    def get_chapter_references(self, chapter_id: str) -> Dict[str, List[str]]:
        """Get all references for a chapter.
        
        Returns:
            Dictionary with 'outgoing' and 'incoming' reference lists
        """
        return {
            'outgoing': list(self.reference_graph.get(chapter_id, set())),
            'incoming': [ch for ch, refs in self.reference_graph.items() if chapter_id in refs]
        }
    
    def find_orphan_chapters(self) -> List[str]:
        """Find chapters with no incoming or outgoing references."""
        referenced_chapters = set()
        
        for source, targets in self.reference_graph.items():
            referenced_chapters.add(source)
            referenced_chapters.update(targets)
        
        all_chapters = set(self.chapter_index.keys())
        orphans = all_chapters - referenced_chapters
        
        return list(orphans)
    
    def generate_reference_graph_dot(self) -> str:
        """Generate DOT format graph of references."""
        dot_content = "digraph references {\n"
        dot_content += "  rankdir=LR;\n"
        dot_content += "  node [shape=box];\n\n"
        
        # Add nodes
        for ch_id, chapter in self.chapter_index.items():
            label = f"{format_chapter_number(chapter.number)}\\n{chapter.title[:20]}..."
            dot_content += f'  "{ch_id}" [label="{label}"];\n'
        
        dot_content += "\n"
        
        # Add edges
        for source, targets in self.reference_graph.items():
            for target in targets:
                dot_content += f'  "{source}" -> "{target}";\n'
        
        dot_content += "}\n"
        return dot_content