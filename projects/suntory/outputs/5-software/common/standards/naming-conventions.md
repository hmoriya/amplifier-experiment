# 命名規則 Naming Conventions

## 概要

本ドキュメントは、サントリーグループのソフトウェアデザインにおける命名規則を定義する。
ConsultingToolのParasol V3 MVPフレームワークに準拠。

---

## 基本原則

### 3要素命名規則

すべての設計要素は以下の3形式で命名する：

| 形式 | 用途 | 例 |
|------|------|-----|
| 日本語名 | ドキュメント、UI | 水質分析 |
| EnglishName | コード、API | WaterQualityAnalysis |
| SCREAMING_SNAKE_CASE | 定数、設定 | WATER_QUALITY_ANALYSIS |

---

## 要素別命名規則

### Bounded Context

| 項目 | 規則 | 例 |
|------|------|-----|
| ID形式 | `bc-{number:03d}-{name}` | bc-001-rd-water-science |
| 番号 | 3桁ゼロ埋め | 001, 002, ... 024 |
| 名前 | kebab-case、英語 | rd-water-science |

### L3 Capability

| 項目 | 規則 | 例 |
|------|------|-----|
| ID形式 | `cap-{number:03d}-{name}` | cap-001-water-quality-analysis |
| 番号 | BC内で連番、3桁ゼロ埋め | 001, 002, 003 |
| 名前 | kebab-case、英語 | water-quality-analysis |

### Business Operation

| 項目 | 規則 | 例 |
|------|------|-----|
| ID形式 | `op-{number:03d}-{name}` | op-001-analyze-water-quality |
| 番号 | BC内で連番、3桁ゼロ埋め | 001, 002, ... |
| 名前 | kebab-case、動詞始まり | analyze-water-quality |

### Use Case

| 項目 | 規則 | 例 |
|------|------|-----|
| ID形式 | `uc-{number:03d}-{name}` | uc-001-water-quality-test |
| 番号 | BC内で連番、3桁ゼロ埋め | 001, 002, ... |
| 名前 | kebab-case、名詞句 | water-quality-test |

### Page

| 項目 | 規則 | 例 |
|------|------|-----|
| ID形式 | `page-{number:03d}-{name}` | page-001-water-quality-dashboard |
| 番号 | BC内で連番、3桁ゼロ埋め | 001, 002, ... |
| 名前 | kebab-case、名詞句 | water-quality-dashboard |

---

## ファイル命名規則

### ディレクトリ構造

```
bounded-contexts/
└── {bc-id}/
    ├── README.md
    ├── l3-capabilities/
    │   └── {cap-id}.md
    ├── operations/
    │   └── {op-id}.md
    ├── usecases/
    │   └── {uc-id}.md
    ├── pages/
    │   └── {page-id}.md
    └── domain-language/
        ├── entities.md
        ├── value-objects.md
        ├── aggregates.md
        ├── domain-services.md
        └── domain-events.md
```

### ファイル名規則

| 要素 | ファイル名 | 例 |
|------|------------|-----|
| Capability | `{cap-id}.md` | cap-001-water-quality-analysis.md |
| Operation | `{op-id}.md` | op-001-analyze-water-quality.md |
| UseCase | `{uc-id}.md` | uc-001-water-quality-test.md |
| Page | `{page-id}.md` | page-001-water-quality-dashboard.md |

---

## コード命名規則

### TypeScript/JavaScript

| 要素 | 規則 | 例 |
|------|------|-----|
| クラス | PascalCase | `WaterQualityAnalysis` |
| インターフェース | PascalCase、I接頭辞なし | `WaterSource` |
| 関数 | camelCase | `analyzeWaterQuality` |
| 定数 | SCREAMING_SNAKE_CASE | `WATER_QUALITY_ANALYSIS` |
| 変数 | camelCase | `waterSource` |
| ファイル | kebab-case | `water-quality-analysis.ts` |

### Python

| 要素 | 規則 | 例 |
|------|------|-----|
| クラス | PascalCase | `WaterQualityAnalysis` |
| 関数 | snake_case | `analyze_water_quality` |
| 定数 | SCREAMING_SNAKE_CASE | `WATER_QUALITY_ANALYSIS` |
| 変数 | snake_case | `water_source` |
| ファイル | snake_case | `water_quality_analysis.py` |

---

## API命名規則

### RESTful API

| 要素 | 規則 | 例 |
|------|------|-----|
| リソース | 複数形、kebab-case | `/water-sources` |
| パス | 小文字、kebab-case | `/api/v1/water-sources/{id}/tests` |
| クエリパラメータ | camelCase | `?sourceType=underground` |

### GraphQL

| 要素 | 規則 | 例 |
|------|------|-----|
| Type | PascalCase | `WaterSource` |
| Query | camelCase | `waterSource`, `waterSources` |
| Mutation | camelCase、動詞始まり | `createWaterSource` |
| Field | camelCase | `waterQuality` |

---

## データベース命名規則

### テーブル/コレクション

| 要素 | 規則 | 例 |
|------|------|-----|
| テーブル名 | snake_case、複数形 | `water_sources` |
| カラム名 | snake_case | `water_quality` |
| 主キー | `id` | `id` |
| 外部キー | `{table}_id` | `water_source_id` |
| タイムスタンプ | `created_at`, `updated_at` | - |

---

## 禁止事項

1. **略語の多用**: 意味不明な略語は使用しない
   - NG: `wq_anlys` → OK: `water_quality_analysis`

2. **数字のみのID**: 意味のある名前を付ける
   - NG: `001` → OK: `cap-001-water-quality-analysis`

3. **混在したケース**: 1ファイル内でケースを混ぜない
   - NG: `waterSource` と `water_source` の混在

4. **日本語ファイル名**: ファイル名には英語のみ使用
   - NG: `水質分析.md` → OK: `water-quality-analysis.md`

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
