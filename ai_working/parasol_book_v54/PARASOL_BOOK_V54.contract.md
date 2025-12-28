---
module: parasol_book_v54
artifact: contract
version: 1.0.0
status: stable
depends_on: []
---

# Parasol Book V5.4 Generator Contract

## Role & Purpose

Generates a complete 500-page book documenting the Parasol V5.4 framework in Japanese, structured as 8 parts with 38 chapters. The module produces Markdown files with embedded Mermaid diagrams, organized according to the V5.4 book structure emphasizing the three spaces (Value/Problem/Solution) and detailed Phase 4-7 coverage.

## Public API

### generate_book()

**Signature**: `generate_book(output_dir: str, config: BookConfig) -> BookResult`

**Parameters**:
- `output_dir` (str): Base directory for generated book files
- `config` (BookConfig): Configuration for book generation

**Returns**: `BookResult` with generation status and metadata

**Side Effects**:
- Creates directory structure under `output_dir`
- Writes Markdown files for all chapters and appendices
- Generates index files and cross-references
- Creates diagram files in Mermaid format

**Preconditions**:
- Output directory must be writable
- Sufficient disk space (minimum 100MB)

**Postconditions**:
- Complete book structure exists under output directory
- All 38 chapters are generated with proper formatting
- Cross-references are valid and complete
- Diagrams are syntactically correct Mermaid

### validate_structure()

**Signature**: `validate_structure(book_dir: str) -> ValidationResult`

**Parameters**:
- `book_dir` (str): Directory containing generated book

**Returns**: `ValidationResult` with validation status and issues

**Side Effects**: None (read-only operation)

**Preconditions**:
- Book directory exists and is readable

**Postconditions**:
- Returns complete validation report
- No modifications to book files

## Data Models

### BookConfig
```json
{
  "language": "ja",
  "format": "markdown",
  "include_diagrams": true,
  "diagram_format": "mermaid",
  "target_pages": 500,
  "parts": [
    {
      "id": "part1",
      "title": "基礎編「Parasol V5への招待」",
      "chapters": 5,
      "target_pages": 50
    }
    // ... other 7 parts
  ],
  "metadata": {
    "version": "5.4",
    "revision": "1.0.0"
  }
}
```

### BookResult
```json
{
  "success": true,
  "generated_files": [
    "part1-foundation/chapter1-why-parasol.md",
    // ... all file paths
  ],
  "statistics": {
    "total_chapters": 38,
    "total_pages": 500,
    "total_words": 250000,
    "total_diagrams": 45,
    "generation_time_seconds": 120
  },
  "warnings": [],
  "errors": []
}
```

### ValidationResult
```json
{
  "valid": true,
  "issues": [
    {
      "type": "warning",
      "file": "part2/chapter6.md",
      "message": "Chapter shorter than target",
      "details": {
        "target_pages": 20,
        "actual_pages": 18
      }
    }
  ],
  "statistics": {
    "total_files": 45,
    "total_chapters": 38,
    "missing_chapters": [],
    "broken_links": []
  }
}
```

## Error Model

### BOOK_CONFIG_INVALID
- **When**: Invalid configuration provided
- **Retryable**: No
- **Recovery**: Fix configuration and retry

### OUTPUT_DIR_ERROR
- **When**: Cannot create or write to output directory
- **Retryable**: Yes, after fixing permissions
- **Recovery**: Ensure directory is writable

### GENERATION_FAILED
- **When**: Chapter or diagram generation fails
- **Retryable**: Yes
- **Recovery**: Check logs for specific failure

### VALIDATION_FAILED
- **When**: Generated book doesn't meet structure requirements
- **Retryable**: No
- **Recovery**: Review generation logic

## Performance & Resource Expectations

- **Generation time**: 60-180 seconds for complete book
- **Memory usage**: Maximum 500MB during generation
- **Disk space**: 50-100MB for generated files
- **Concurrency**: Can generate multiple chapters in parallel (configurable)

## Configuration (Consumer-Visible)

### Environment Variables
- `PARASOL_BOOK_LANG`: Target language (default: "ja")
- `PARASOL_BOOK_MAX_PARALLEL`: Max parallel chapter generation (default: 4)
- `PARASOL_BOOK_DIAGRAM_ENGINE`: Diagram engine (default: "mermaid")

### Config File
- Supports `parasol_book.yaml` for default configuration
- Command-line config overrides file config

## Conformance Criteria

1. **Structure Completeness**: Generated book contains exactly 8 parts and 38 chapters as specified
2. **Content Volume**: Total content is 480-520 pages (±4% of 500 page target)
3. **Diagram Validity**: All Mermaid diagrams are syntactically valid
4. **Cross-Reference Integrity**: All internal links resolve correctly
5. **Language Consistency**: All content is in Japanese as configured
6. **Format Compliance**: All files are valid Markdown with proper front matter
7. **Phase Coverage**: Phases 4-7 have dedicated chapters with detailed content
8. **Three Spaces Clarity**: Value/Problem/Solution spaces are clearly delineated

## Compatibility & Versioning

- **Version**: 1.0.0 (follows SemVer)
- **Breaking changes**: Major version bump for structure changes
- **Deprecation**: 6-month notice for API changes
- **Backward compatibility**: Maintains compatibility within major version

## Usage Examples

```python
# Basic usage
from parasol_book_v54 import generate_book, BookConfig

config = BookConfig(language="ja", target_pages=500)
result = generate_book("output/parasol-v54-book", config)

if result.success:
    print(f"Generated {len(result.generated_files)} files")
    print(f"Total pages: {result.statistics['total_pages']}")
else:
    print(f"Generation failed: {result.errors}")

# Validation
from parasol_book_v54 import validate_structure

validation = validate_structure("output/parasol-v54-book")
if not validation.valid:
    for issue in validation.issues:
        print(f"{issue.type}: {issue.message}")
```