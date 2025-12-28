"""Constants for Parasol Book V5.4 structure and metadata."""

# Book metadata
BOOK_VERSION = "5.4"
BOOK_TITLE = "Parasol V5.4 完全ガイド"
BOOK_SUBTITLE = "3スペース明確化版"
DEFAULT_LANGUAGE = "ja"

# Page targets
TARGET_TOTAL_PAGES = 500
PAGE_TOLERANCE_PERCENT = 4  # ±4% tolerance
WORDS_PER_PAGE = 500  # Approximate for Japanese text

# Generation settings  
DEFAULT_MAX_PARALLEL = 4
GENERATION_TIMEOUT_SECONDS = 180
DIAGRAM_TIMEOUT_SECONDS = 10

# Chapter definitions for all 38 chapters
CHAPTER_DEFINITIONS = {
    "part1": {
        "title": "基礎編「Parasol V5への招待」",
        "chapters": [
            {
                "id": "chapter1-why-parasol",
                "number": 1,
                "title": "なぜParasol V5なのか",
                "file": "chapter1-why-parasol.md",
                "target_pages": 10,
                "keywords": ["動機", "背景", "価値"]
            },
            {
                "id": "chapter2-three-spaces", 
                "number": 2,
                "title": "3つのスペース - WHY・WHAT・HOW",
                "file": "chapter2-three-spaces.md",
                "target_pages": 10,
                "keywords": ["価値領域", "問題領域", "解決領域"]
            },
            {
                "id": "chapter3-philosophy",
                "number": 3,
                "title": "Parasol哲学とマインドセット",
                "file": "chapter3-philosophy.md",
                "target_pages": 10,
                "keywords": ["哲学", "マインドセット", "原則"]
            },
            {
                "id": "chapter4-axiomatic-design",
                "number": 4,
                "title": "Axiomatic Designと設計公理",
                "file": "chapter4-axiomatic-design.md",
                "target_pages": 10,
                "keywords": ["Axiomatic Design", "設計公理", "ZIGZAG"]
            },
            {
                "id": "chapter5-v5-ddd",
                "number": 5,
                "title": "V5とDDDの融合",
                "file": "chapter5-v5-ddd.md",
                "target_pages": 10,
                "keywords": ["DDD", "ドメイン駆動設計", "統合"]
            }
        ]
    },
    "part2": {
        "title": "組織理解編「プロジェクトの土台」",
        "chapters": [
            {
                "id": "chapter6-phase0-organization",
                "number": 6,
                "title": "Phase 0 - 組織とドメインの理解",
                "file": "chapter6-phase0-organization.md",
                "target_pages": 10,
                "keywords": ["Phase 0", "組織理解", "ドメイン"]
            },
            {
                "id": "chapter7-phase1-foundation",
                "number": 7,
                "title": "Phase 1 - プロジェクト基盤構築",
                "file": "chapter7-phase1-foundation.md",
                "target_pages": 10,
                "keywords": ["Phase 1", "基盤構築", "セットアップ"]
            },
            {
                "id": "chapter8-industry-patterns",
                "number": 8,
                "title": "産業パターンの選択と適用",
                "file": "chapter8-industry-patterns.md",
                "target_pages": 10,
                "keywords": ["産業パターン", "パターン選択", "適用"]
            }
        ]
    },
    "part3": {
        "title": "価値領域編「WHY - なぜ作るのか」",
        "chapters": [
            {
                "id": "chapter9-phase2-value-discovery",
                "number": 9,
                "title": "Phase 2 - 価値ストリームの発見",
                "file": "chapter9-phase2-value-discovery.md",
                "target_pages": 15,
                "keywords": ["Phase 2", "価値発見", "ストリーム"]
            },
            {
                "id": "chapter10-value-stage-design",
                "number": 10,
                "title": "価値ステージ（VS）設計",
                "file": "chapter10-value-stage-design.md",
                "target_pages": 15,
                "keywords": ["価値ステージ", "VS", "設計"]
            },
            {
                "id": "chapter11-value-level-hierarchy",
                "number": 11,
                "title": "価値レベル（VL）の階層化",
                "file": "chapter11-value-level-hierarchy.md",
                "target_pages": 15,
                "keywords": ["価値レベル", "VL", "階層化"]
            },
            {
                "id": "chapter12-value-metrics",
                "number": 12,
                "title": "価値指標とマイルストーン設定",
                "file": "chapter12-value-metrics.md",
                "target_pages": 15,
                "keywords": ["価値指標", "マイルストーン", "KPI"]
            }
        ]
    },
    "part4": {
        "title": "問題領域編「WHAT - 何を作るのか」",
        "chapters": [
            {
                "id": "chapter13-phase3-capability",
                "number": 13,
                "title": "Phase 3 - ケイパビリティの発見",
                "file": "chapter13-phase3-capability.md",
                "target_pages": 15,
                "keywords": ["Phase 3", "ケイパビリティ", "能力"]
            },
            {
                "id": "chapter14-cl-hierarchy-zigzag",
                "number": 14,
                "title": "CL階層とビジネス能力の構造化",
                "file": "chapter14-cl-hierarchy-zigzag.md",
                "target_pages": 15,
                "keywords": ["CL階層", "ビジネス能力", "構造化"]
            },
            {
                "id": "chapter15-zigzag-transformation",
                "number": 15,
                "title": "ZIGZAGプロセスによる変換",
                "file": "chapter15-zigzag-transformation.md",
                "target_pages": 15,
                "keywords": ["ZIGZAG", "変換", "プロセス"]
            },
            {
                "id": "chapter16-design-matrix",
                "number": 16,
                "title": "Design Matrixによる設計評価",
                "file": "chapter16-design-matrix.md",
                "target_pages": 15,
                "keywords": ["Design Matrix", "設計評価", "検証"]
            }
        ]
    },
    "part5": {
        "title": "解決領域編「HOW - どう作るのか」",
        "sections": {
            "section1-architecture": {
                "title": "アーキテクチャ（Phase 4）",
                "chapters": [
                    {
                        "id": "chapter17-architecture-patterns",
                        "number": 17,
                        "title": "アーキテクチャパターンの選択",
                        "file": "chapter17-architecture-patterns.md",
                        "target_pages": 13,
                        "keywords": ["アーキテクチャ", "パターン", "Phase 4"]
                    },
                    {
                        "id": "chapter18-bc-mapping",
                        "number": 18,
                        "title": "BCへのマッピングと境界設計",
                        "file": "chapter18-bc-mapping.md",
                        "target_pages": 13,
                        "keywords": ["BC", "マッピング", "境界設計"]
                    },
                    {
                        "id": "chapter19-tech-stack",
                        "number": 19,
                        "title": "技術スタックの決定",
                        "file": "chapter19-tech-stack.md",
                        "target_pages": 14,
                        "keywords": ["技術スタック", "技術選定", "意思決定"]
                    }
                ]
            },
            "section2-software-design": {
                "title": "ソフトウェア設計（Phase 5）",
                "chapters": [
                    {
                        "id": "chapter20-domain-model",
                        "number": 20,
                        "title": "ドメインモデルの詳細設計",
                        "file": "chapter20-domain-model.md",
                        "target_pages": 13,
                        "keywords": ["ドメインモデル", "Phase 5", "DDD"]
                    },
                    {
                        "id": "chapter21-api-design",
                        "number": 21,
                        "title": "APIとインターフェース設計",
                        "file": "chapter21-api-design.md",
                        "target_pages": 13,
                        "keywords": ["API", "インターフェース", "設計"]
                    },
                    {
                        "id": "chapter22-database-events",
                        "number": 22,
                        "title": "データベースとイベント設計",
                        "file": "chapter22-database-events.md",
                        "target_pages": 14,
                        "keywords": ["データベース", "イベント", "設計"]
                    }
                ]
            },
            "section3-implementation": {
                "title": "実装（Phase 6）",
                "chapters": [
                    {
                        "id": "chapter23-implementation-patterns",
                        "number": 23,
                        "title": "実装パターンとベストプラクティス",
                        "file": "chapter23-implementation-patterns.md",
                        "target_pages": 13,
                        "keywords": ["実装パターン", "Phase 6", "ベストプラクティス"]
                    },
                    {
                        "id": "chapter24-test-strategy",
                        "number": 24,
                        "title": "テスト戦略と品質保証",
                        "file": "chapter24-test-strategy.md",
                        "target_pages": 13,
                        "keywords": ["テスト", "品質保証", "QA"]
                    },
                    {
                        "id": "chapter25-code-review",
                        "number": 25,
                        "title": "コードレビューと改善",
                        "file": "chapter25-code-review.md",
                        "target_pages": 14,
                        "keywords": ["コードレビュー", "改善", "リファクタリング"]
                    }
                ]
            },
            "section4-platform": {
                "title": "プラットフォーム（Phase 7）",
                "chapters": [
                    {
                        "id": "chapter26-deployment",
                        "number": 26,
                        "title": "デプロイメントアーキテクチャ",
                        "file": "chapter26-deployment.md",
                        "target_pages": 13,
                        "keywords": ["デプロイメント", "Phase 7", "インフラ"]
                    },
                    {
                        "id": "chapter27-cicd-pipeline",
                        "number": 27,
                        "title": "CI/CDパイプライン構築",
                        "file": "chapter27-cicd-pipeline.md",
                        "target_pages": 13,
                        "keywords": ["CI/CD", "パイプライン", "自動化"]
                    },
                    {
                        "id": "chapter28-monitoring",
                        "number": 28,
                        "title": "監視とオブザーバビリティ",
                        "file": "chapter28-monitoring.md",
                        "target_pages": 14,
                        "keywords": ["監視", "オブザーバビリティ", "運用"]
                    }
                ]
            }
        }
    },
    "part6": {
        "title": "統合編「価値の実現」",
        "chapters": [
            {
                "id": "chapter29-value-traceability",
                "number": 29,
                "title": "価値トレーサビリティシステム",
                "file": "chapter29-value-traceability.md",
                "target_pages": 13,
                "keywords": ["トレーサビリティ", "価値追跡", "統合"]
            },
            {
                "id": "chapter30-golden-thread",
                "number": 30,
                "title": "Golden Threadによる一貫性確保",
                "file": "chapter30-golden-thread.md",
                "target_pages": 13,
                "keywords": ["Golden Thread", "一貫性", "接続"]
            },
            {
                "id": "chapter31-value-metrics-measurement",
                "number": 31,
                "title": "価値指標の測定と改善",
                "file": "chapter31-value-metrics-measurement.md",
                "target_pages": 14,
                "keywords": ["測定", "改善", "PDCA"]
            }
        ]
    },
    "part7": {
        "title": "実践編「チームでの適用」",
        "chapters": [
            {
                "id": "chapter32-claude-code",
                "number": 32,
                "title": "Claude Code統合実践",
                "file": "chapter32-claude-code.md",
                "target_pages": 15,
                "keywords": ["Claude Code", "AI支援", "統合"]
            },
            {
                "id": "chapter33-team-scaling",
                "number": 33,
                "title": "チーム編成とスケーリング",
                "file": "chapter33-team-scaling.md",
                "target_pages": 15,
                "keywords": ["チーム", "スケーリング", "組織"]
            },
            {
                "id": "chapter34-troubleshooting",
                "number": 34,
                "title": "よくあるトラブルと解決法",
                "file": "chapter34-troubleshooting.md",
                "target_pages": 15,
                "keywords": ["トラブルシューティング", "FAQ", "解決法"]
            },
            {
                "id": "chapter35-custom-patterns",
                "number": 35,
                "title": "カスタムパターンの開発",
                "file": "chapter35-custom-patterns.md",
                "target_pages": 15,
                "keywords": ["カスタマイズ", "パターン開発", "拡張"]
            }
        ]
    },
    "part8": {
        "title": "発展編「未来への道」",
        "chapters": [
            {
                "id": "chapter36-v5-future",
                "number": 36,
                "title": "V5の進化と最新動向",
                "file": "chapter36-v5-future.md",
                "target_pages": 13,
                "keywords": ["進化", "最新動向", "ロードマップ"]
            },
            {
                "id": "chapter37-community",
                "number": 37,
                "title": "コミュニティへの参加と貢献",
                "file": "chapter37-community.md",
                "target_pages": 13,
                "keywords": ["コミュニティ", "貢献", "オープンソース"]
            },
            {
                "id": "chapter38-next-generation",
                "number": 38,
                "title": "次世代への展望",
                "file": "chapter38-next-generation.md",
                "target_pages": 14,
                "keywords": ["次世代", "展望", "未来"]
            }
        ]
    }
}

# Appendix definitions
APPENDIX_DEFINITIONS = {
    "appendix-a": {
        "title": "コマンドリファレンス",
        "file": "appendix-a-command-reference.md",
        "target_pages": 10
    },
    "appendix-b": {
        "title": "チェックリストとテンプレート",
        "file": "appendix-b-templates.md",
        "target_pages": 10
    },
    "appendix-c": {
        "title": "用語集",
        "file": "appendix-c-glossary.md", 
        "target_pages": 10
    },
    "appendix-d": {
        "title": "参考文献とリソース",
        "file": "appendix-d-resources.md",
        "target_pages": 10
    }
}

# Diagram types supported
DIAGRAM_TYPES = [
    "flow",
    "architecture",
    "sequence",
    "state",
    "entity-relationship",
    "gantt",
    "mindmap"
]

# Error codes
ERROR_CODES = {
    "BOOK_CONFIG_INVALID": "E001",
    "OUTPUT_DIR_ERROR": "E002",
    "GENERATION_FAILED": "E003",
    "VALIDATION_FAILED": "E004"
}