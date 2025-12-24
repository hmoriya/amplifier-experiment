#!/usr/bin/env python3
"""
V5アジャイル初心者ガイド第1部 書籍生成スクリプト
"""

import os
import webbrowser
from pathlib import Path
from generate_book_with_diagrams import convert_markdown_to_html

def generate_v5_agile_guide_part1():
    """V5アジャイル初心者ガイド第1部を生成する"""
    
    # ベースディレクトリ
    base_dir = Path("/Users/hmoriya/Develop/github/github.com/hmoriya/amplifier-experiment/.claude/commands/parasol/docs/v5-agile-guide")
    
    # 第1部の章ファイル
    chapters = [
        "part1-foundation/chapter1-why-value-driven-agile.md",
        "part1-foundation/chapter2-v5-agile-integration.md", 
        "part1-foundation/chapter3-value-driven-sprint-overview.md"
    ]
    
    # 書籍の前書き
    front_matter = """# はじめてのParasol V5 × アジャイル実践ガイド

**第1部：基礎理解編（30分で読める）**

価値駆動スクラムで変わるチーム開発

---

## 本書について

このガイドは、アジャイル開発経験1-3年の開発者・スクラムマスター向けに、Parasol V5とアジャイルを統合した価値駆動開発手法を実践的に解説します。

### 第1部の構成

- **第1章**: なぜ価値駆動アジャイルが必要なのか
- **第2章**: V5とアジャイルの美しい統合  
- **第3章**: 価値駆動スプリントの全体像

### 読者対象

- アジャイル開発者（経験1-3年）
- スクラムマスター（初級〜中級）
- プロダクトオーナー（V5を知りたい方）

### 前提知識

- スクラムの基本的な流れを理解している
- ユーザーストーリーとスプリントの概念を知っている  
- 開発チームでの作業経験がある

---
"""
    
    # 全章のマークダウンを結合
    full_markdown = front_matter
    
    for chapter_path in chapters:
        chapter_file = base_dir / chapter_path
        if chapter_file.exists():
            print(f"章を読み込み中: {chapter_path}")
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
                full_markdown += "\n\n" + content
        else:
            print(f"警告: 章ファイルが見つかりません: {chapter_file}")
    
    # 出力パス
    output_path = base_dir.parent / "v5_agile_guide_part1.html"
    
    # HTMLに変換
    print("HTMLに変換中...")
    html_body = convert_markdown_to_html(full_markdown)
    
    # 完全なHTMLドキュメント作成
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>はじめてのParasol V5 × アジャイル実践ガイド - 第1部：基礎理解編</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", "Yu Gothic UI", sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #fff;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            margin-top: 40px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 30px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
            font-style: italic;
        }}
        .toc {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .toc ul ul {{
            padding-left: 20px;
        }}
        .toc li {{
            margin: 5px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #2c3e50;
        }}
        .toc a:hover {{
            color: #3498db;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""
    
    # ファイルに書き出し
    print(f"HTMLファイルを生成中: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ 書籍生成完了!")
    print(f"📖 ファイル場所: {output_path}")
    print(f"🌐 ブラウザで開くには: open '{output_path}'")
    
    return output_path

if __name__ == "__main__":
    output_file = generate_v5_agile_guide_part1()
    
    # ブラウザで開く
    webbrowser.open(f'file://{output_file}')
    print("\n📱 ブラウザで開きました！")