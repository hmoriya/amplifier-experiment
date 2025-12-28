# Parasol V5.4 Book Templates

This directory contains Jinja2 templates for generating the Parasol V5.4 book.

## Templates

- `chapter_base.md.j2` - Base template for all chapters
- `index.md.j2` - Template for index pages (book and part indexes)
- `part_intro.md.j2` - Template for part introduction pages
- `diagrams/` - Mermaid diagram templates

## Variables

Common template variables:

- `title` - Chapter or section title
- `number` - Chapter number
- `part_number` - Part number (Roman numerals)
- `part_title` - Part title
- `keywords` - List of chapter keywords
- `learning_objectives` - Chapter learning objectives
- `content` - Main chapter content
- `references` - Cross-references to other chapters
- `diagrams` - List of diagrams to include