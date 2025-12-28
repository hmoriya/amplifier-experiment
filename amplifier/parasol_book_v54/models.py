"""Data models for Parasol Book V5.4 Generator."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class IssueType(Enum):
    """Types of validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class PartConfig:
    """Configuration for a book part."""
    id: str
    title: str
    chapters: int
    target_pages: int
    description: Optional[str] = None


@dataclass
class BookConfig:
    """Configuration for book generation."""
    language: str = "ja"
    format: str = "markdown"
    include_diagrams: bool = True
    diagram_format: str = "mermaid"
    target_pages: int = 500
    parts: List[PartConfig] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    max_parallel: int = 4
    output_encoding: str = "utf-8"
    
    def __post_init__(self):
        """Initialize default parts if not provided."""
        if not self.parts:
            self.parts = self._default_parts()
    
    def _default_parts(self) -> List[PartConfig]:
        """Get default V5.4 book structure."""
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


@dataclass
class GenerationStatistics:
    """Statistics about the generated book."""
    total_chapters: int = 0
    total_pages: int = 0
    total_words: int = 0
    total_diagrams: int = 0
    generation_time_seconds: float = 0.0
    chapters_per_part: Dict[str, int] = field(default_factory=dict)
    pages_per_part: Dict[str, int] = field(default_factory=dict)


@dataclass
class BookResult:
    """Result of book generation."""
    success: bool
    generated_files: List[str] = field(default_factory=list)
    statistics: GenerationStatistics = field(default_factory=GenerationStatistics)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    def add_file(self, file_path: str) -> None:
        """Add a generated file to the result."""
        self.generated_files.append(file_path)
    
    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)
    
    def add_error(self, message: str) -> None:
        """Add an error message and mark as failed."""
        self.errors.append(message)
        self.success = False


@dataclass
class ValidationIssue:
    """A validation issue found in the book."""
    type: IssueType
    file: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    line_number: Optional[int] = None


@dataclass
class ValidationStatistics:
    """Statistics from book validation."""
    total_files: int = 0
    total_chapters: int = 0
    missing_chapters: List[str] = field(default_factory=list)
    broken_links: List[str] = field(default_factory=list)
    invalid_diagrams: List[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of book structure validation."""
    valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    statistics: ValidationStatistics = field(default_factory=ValidationStatistics)
    
    def add_issue(self, issue: ValidationIssue) -> None:
        """Add a validation issue."""
        self.issues.append(issue)
        if issue.type == IssueType.ERROR:
            self.valid = False


@dataclass
class ChapterMetadata:
    """Metadata for a book chapter."""
    part_id: str
    chapter_id: str
    number: int
    title: str
    target_pages: int
    keywords: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    

@dataclass
class DiagramMetadata:
    """Metadata for a diagram."""
    id: str
    type: str  # flow, architecture, sequence, etc.
    title: str
    description: str
    chapter_id: str
    mermaid_code: str = ""


@dataclass 
class CrossReference:
    """A cross-reference between chapters."""
    source_chapter: str
    target_chapter: str
    reference_text: str
    reference_type: str = "see"  # see, refer, detail, example