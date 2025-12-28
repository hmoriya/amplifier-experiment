"""Book structure management for Parasol V5.4."""

import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from .models import PartConfig, ChapterMetadata
from .constants import CHAPTER_DEFINITIONS, APPENDIX_DEFINITIONS, TARGET_TOTAL_PAGES
from .utils import format_part_number, format_chapter_number

logger = logging.getLogger(__name__)


class StructureManager:
    """Manages the book structure and chapter organization."""
    
    def __init__(self, parts: Optional[List[PartConfig]] = None):
        """Initialize with book parts configuration."""
        self.parts = parts or self._get_default_parts()
        self.chapter_definitions = CHAPTER_DEFINITIONS
        self.appendix_definitions = APPENDIX_DEFINITIONS
        self._validate_structure()
    
    def _get_default_parts(self) -> List[PartConfig]:
        """Get default V5.4 book parts."""
        return [
            PartConfig("part1", "基礎編「Parasol V5への招待」", 5, 50),
            PartConfig("part2", "組織理解編「プロジェクトの土台」", 3, 30),
            PartConfig("part3", "価値領域編「WHY - なぜ作るのか」", 4, 60),
            PartConfig("part4", "問題領域編「WHAT - 何を作るのか」", 4, 60),
            PartConfig("part5", "解決領域編「HOW - どう作るのか」", 12, 160),
            PartConfig("part6", "統合編「価値の実現」", 3, 40),
            PartConfig("part7", "実践編「チームでの適用」", 4, 60),
            PartConfig("part8", "発展編「未来への道」", 3, 40),
        ]
    
    def _validate_structure(self) -> None:
        """Validate the book structure for completeness."""
        total_chapters = sum(part.chapters for part in self.parts)
        if total_chapters != 38:
            raise ValueError(f"Expected 38 chapters, got {total_chapters}")
        
        # Validate chapter definitions match
        defined_chapters = self._count_defined_chapters()
        if defined_chapters != 38:
            raise ValueError(f"Chapter definitions mismatch: {defined_chapters} defined")
    
    def _count_defined_chapters(self) -> int:
        """Count total chapters in definitions."""
        count = 0
        for part_id, part_data in self.chapter_definitions.items():
            if 'chapters' in part_data:
                count += len(part_data['chapters'])
            elif 'sections' in part_data:
                for section_data in part_data['sections'].values():
                    count += len(section_data['chapters'])
        return count
    
    def get_all_chapters(self) -> List[ChapterMetadata]:
        """Get all chapter metadata in order."""
        chapters = []
        
        for part_index, part in enumerate(self.parts, 1):
            part_id = part.id
            if part_id not in self.chapter_definitions:
                logger.warning(f"No chapter definitions for {part_id}")
                continue
            
            part_data = self.chapter_definitions[part_id]
            
            # Handle regular chapters
            if 'chapters' in part_data:
                chapters.extend(self._process_chapters(
                    part_id, part_data['chapters'], part.target_pages
                ))
            
            # Handle sections (Part 5)
            elif 'sections' in part_data:
                total_section_chapters = 0
                for section_data in part_data['sections'].values():
                    total_section_chapters += len(section_data['chapters'])
                
                pages_per_chapter = part.target_pages // total_section_chapters
                
                for section_id, section_data in part_data['sections'].items():
                    chapters.extend(self._process_chapters(
                        part_id, section_data['chapters'], 
                        pages_per_chapter * len(section_data['chapters'])
                    ))
        
        return chapters
    
    def _process_chapters(self, part_id: str, chapters_data: List[Dict], 
                         total_pages: int) -> List[ChapterMetadata]:
        """Process chapter data into metadata objects."""
        chapters = []
        pages_per_chapter = total_pages // len(chapters_data) if chapters_data else 0
        
        for chapter_data in chapters_data:
            chapter = ChapterMetadata(
                part_id=part_id,
                chapter_id=chapter_data['id'],
                number=chapter_data['number'],
                title=chapter_data['title'],
                target_pages=chapter_data.get('target_pages', pages_per_chapter),
                keywords=chapter_data.get('keywords', [])
            )
            chapters.append(chapter)
        
        return chapters
    
    def get_chapter_path(self, chapter: ChapterMetadata) -> str:
        """Get the file path for a chapter."""
        part_id = chapter.part_id
        
        # Special handling for Part 5 sections
        if part_id == "part5":
            # Find which section this chapter belongs to
            for section_id, section_data in self.chapter_definitions[part_id]['sections'].items():
                for ch in section_data['chapters']:
                    if ch['id'] == chapter.chapter_id:
                        return f"{part_id}-solution-domain/{section_id}/{ch['file']}"
        
        # Regular parts
        part_dir_map = {
            "part1": "part1-foundation",
            "part2": "part2-organization", 
            "part3": "part3-value-domain",
            "part4": "part4-problem-domain",
            "part6": "part6-integration",
            "part7": "part7-practice",
            "part8": "part8-evolution"
        }
        
        part_dir = part_dir_map.get(part_id, part_id)
        
        # Find the file name from definitions
        if part_id in self.chapter_definitions:
            if 'chapters' in self.chapter_definitions[part_id]:
                for ch in self.chapter_definitions[part_id]['chapters']:
                    if ch['id'] == chapter.chapter_id:
                        return f"{part_dir}/{ch['file']}"
        
        # Fallback
        return f"{part_dir}/{chapter.chapter_id}.md"
    
    def get_part_info(self, part_id: str) -> Optional[PartConfig]:
        """Get part configuration by ID."""
        for part in self.parts:
            if part.id == part_id:
                return part
        return None
    
    def get_total_page_target(self) -> int:
        """Get total target pages for the book."""
        return sum(part.target_pages for part in self.parts)
    
    def get_appendix_list(self) -> List[Dict[str, any]]:
        """Get list of appendices."""
        appendices = []
        for appendix_id, appendix_data in self.appendix_definitions.items():
            appendices.append({
                'id': appendix_id,
                'title': appendix_data['title'],
                'file': appendix_data['file'],
                'target_pages': appendix_data['target_pages']
            })
        return appendices
    
    def validate_chapter_count(self, generated_chapters: List[str]) -> Tuple[bool, List[str]]:
        """Validate that all expected chapters were generated.
        
        Returns:
            Tuple of (is_valid, missing_chapters)
        """
        expected_chapters = set()
        for chapter in self.get_all_chapters():
            expected_chapters.add(chapter.chapter_id)
        
        generated_set = set(ch.split('/')[-1].replace('.md', '') for ch in generated_chapters)
        missing = expected_chapters - generated_set
        
        return len(missing) == 0, list(missing)
    
    def get_chapter_by_number(self, number: int) -> Optional[ChapterMetadata]:
        """Get chapter metadata by chapter number."""
        for chapter in self.get_all_chapters():
            if chapter.number == number:
                return chapter
        return None
    
    def get_chapters_by_part(self, part_id: str) -> List[ChapterMetadata]:
        """Get all chapters for a specific part."""
        return [ch for ch in self.get_all_chapters() if ch.part_id == part_id]