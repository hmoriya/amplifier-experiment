"""
CSS styles for PDF generation.

Provides default styles optimized for Japanese text and technical documentation.
"""


def get_default_css() -> str:
    """Get default CSS for PDF generation"""
    return """
/* Base Typography */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;500&display=swap');

:root {
    --primary-color: #2C3E50;
    --accent-color: #3498DB;
    --warning-color: #E67E22;
    --success-color: #27AE60;
    --danger-color: #E74C3C;
    --gray-light: #ECF0F1;
    --gray-medium: #95A5A6;
    --gray-dark: #34495E;
    
    --font-family-main: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', sans-serif;
    --font-family-code: 'Source Code Pro', 'Consolas', 'Monaco', monospace;
    
    --base-font-size: 10pt;
    --line-height: 1.7;
    --paragraph-spacing: 0.8em;
}

/* Page Setup */
@page {
    size: A4;
    margin: 2.5cm 2cm 2cm 2.5cm;
    
    @top-center {
        content: string(chapter-title);
        font-size: 9pt;
        color: var(--gray-medium);
        font-family: var(--font-family-main);
    }
    
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: var(--gray-medium);
    }
}

@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}

/* Base Styles */
html {
    font-family: var(--font-family-main);
    font-size: var(--base-font-size);
    line-height: var(--line-height);
    color: var(--primary-color);
    text-align: justify;
    text-justify: inter-word;
}

body {
    margin: 0;
    padding: 0;
    font-feature-settings: "kern" 1, "liga" 1;
}

/* Japanese Text Optimization */
.jp-text {
    word-break: break-all;
    line-break: strict;
    hanging-punctuation: allow-end;
}

/* Cover Page */
.cover {
    page-break-after: always;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 100vh;
}

.cover-title {
    font-size: 36pt;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5em;
    letter-spacing: 0.05em;
}

.cover-subtitle {
    font-size: 18pt;
    font-weight: 400;
    color: var(--gray-dark);
    margin-bottom: 2em;
}

.cover-meta {
    font-size: 12pt;
    color: var(--gray-medium);
}

.cover-meta .version {
    margin-bottom: 0.5em;
}

/* Table of Contents */
.toc {
    page-break-after: always;
    padding: 2em 0;
}

.toc h1 {
    font-size: 24pt;
    margin-bottom: 1em;
    color: var(--primary-color);
}

.toc-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.toc-item {
    margin-bottom: 0.5em;
    position: relative;
}

.toc-item a {
    text-decoration: none;
    color: var(--primary-color);
    display: flex;
    align-items: baseline;
}

.toc-item a::after {
    content: leader(".") target-counter(attr(href), page);
    margin-left: 0.5em;
    flex: 1;
    text-align: right;
    color: var(--gray-medium);
}

.toc-level-1 { font-weight: 700; font-size: 12pt; margin-top: 1em; }
.toc-level-2 { margin-left: 2em; font-size: 11pt; }
.toc-level-3 { margin-left: 4em; font-size: 10pt; color: var(--gray-dark); }

/* Headers */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.3;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: var(--primary-color);
    break-after: avoid;
}

h1 {
    font-size: 20pt;
    border-bottom: 2px solid var(--accent-color);
    padding-bottom: 0.3em;
    string-set: chapter-title content();
}

h2 { font-size: 16pt; margin-top: 1.2em; }
h3 { font-size: 13pt; margin-top: 1em; }
h4 { font-size: 11pt; margin-top: 0.8em; }

/* Part Separator */
.part-separator {
    page-break-before: always;
    text-align: center;
    padding: 4em 0;
}

.part-separator h1 {
    font-size: 28pt;
    border: none;
    color: var(--accent-color);
}

/* Paragraphs and Text */
p {
    margin: 0 0 var(--paragraph-spacing) 0;
    text-align: justify;
}

/* Lists */
ul, ol {
    margin: 0 0 var(--paragraph-spacing) 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.3em;
}

/* Code Blocks */
.code-block, pre {
    background-color: #2C3E50;
    color: #F8F8F2;
    padding: 1em;
    margin: 1em 0;
    overflow-x: auto;
    font-family: var(--font-family-code);
    font-size: 9pt;
    line-height: 1.4;
    border-radius: 4px;
    break-inside: avoid;
}

code {
    font-family: var(--font-family-code);
    font-size: 0.9em;
    background-color: var(--gray-light);
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Syntax Highlighting (Monokai-inspired for print) */
.highlight { background: #2C3E50; color: #F8F8F2; }
.highlight .k { color: #66D9EF; font-weight: bold; } /* Keyword */
.highlight .n { color: #F8F8F2; } /* Name */
.highlight .s { color: #E6DB74; } /* String */
.highlight .c { color: #75715E; } /* Comment */
.highlight .m { color: #AE81FF; } /* Number */
.highlight .o { color: #F92672; } /* Operator */

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.95em;
    break-inside: avoid;
}

th, td {
    padding: 0.5em 0.8em;
    text-align: left;
    border: 1px solid var(--gray-light);
}

th {
    background-color: var(--gray-light);
    font-weight: 700;
    color: var(--primary-color);
}

tr:nth-child(even) {
    background-color: rgba(236, 240, 241, 0.5);
}

/* Blockquotes */
blockquote {
    margin: 1em 0;
    padding-left: 1em;
    border-left: 4px solid var(--accent-color);
    color: var(--gray-dark);
    font-style: italic;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
    break-inside: avoid;
}

.mermaid-diagram {
    background: white;
    padding: 1em;
    border: 1px solid var(--gray-light);
    border-radius: 4px;
}

.mermaid-fallback {
    background-color: var(--gray-light);
    border: 1px dashed var(--gray-medium);
    padding: 1em;
    font-family: var(--font-family-code);
    font-size: 9pt;
}

/* Links */
a {
    color: var(--accent-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Page Breaks */
.page-break, .chapter {
    page-break-before: always;
}

/* Footnotes */
.footnote {
    font-size: 8pt;
    color: var(--gray-dark);
}

/* Print Optimizations */
@media print {
    .no-print {
        display: none !important;
    }
    
    a[href^="http"]:after {
        content: " (" attr(href) ")";
        font-size: 8pt;
        color: var(--gray-medium);
    }
    
    a[href^="#"]:after {
        content: none;
    }
}

/* Alerts and Callouts */
.alert {
    padding: 1em;
    margin: 1em 0;
    border-radius: 4px;
    break-inside: avoid;
}

.alert-info {
    background-color: #D6EAF8;
    border-left: 4px solid var(--accent-color);
}

.alert-warning {
    background-color: #FCF3CF;
    border-left: 4px solid var(--warning-color);
}

.alert-danger {
    background-color: #FADBD8;
    border-left: 4px solid var(--danger-color);
}

.alert-success {
    background-color: #D5F4E6;
    border-left: 4px solid var(--success-color);
}

/* Custom Classes for Parasol V5 */
.value-stream {
    background-color: #EBF5FB;
    padding: 1em;
    border-radius: 4px;
    margin: 1em 0;
}

.capability-box {
    border: 2px solid var(--accent-color);
    padding: 1em;
    margin: 1em 0;
    border-radius: 4px;
}

.bc-boundary {
    border: 2px dashed var(--warning-color);
    padding: 1em;
    margin: 1em 0;
    background-color: rgba(230, 126, 34, 0.05);
}

/* Appendix Styling */
.appendix h1 {
    color: var(--gray-dark);
    border-bottom-color: var(--gray-medium);
}

/* Index */
.index-entry {
    margin-bottom: 0.3em;
}

.index-term {
    font-weight: 700;
}

.index-pages {
    color: var(--gray-medium);
    font-size: 0.9em;
}
"""