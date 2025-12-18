#!/usr/bin/env python3
"""
Test converter to debug code block issues
"""

import re


def test_code_blocks():
    """Test code block conversion"""
    
    test_text = """
## Claude Codeとの対話：AIが基盤構築を加速する

### 情報収集の効率化

Phase 0-1では、膨大な情報を収集・整理する必要があります。Claude Codeはこの作業を劇的に効率化します。

```
あなた：企業の公開情報から、ビジネスモデルと課題を分析してください。

Claude Code：ウェブサイトと公開資料を分析します。
```

### ステークホルダー分析の深化

Claude Codeは、表面的な情報から深い洞察を導き出します。

```
あなた：組織図と議事録から、真の意思決定構造を分析してください。
```

### リスクの早期発見

Claude Codeは、人間が見落としがちなリスクを指摘します。

```
あなた：このプロジェクトの潜在的リスクを網羅的に洗い出してください。
```

## Phase 0-1の実践的テクニック
"""

    print("Original text:")
    print("=" * 50)
    print(test_text[:200] + "...")
    
    # Test 1: Simple regex
    print("\n\nTest 1: Simple fenced code block regex")
    print("=" * 50)
    
    matches = re.findall(r'```(\w*)\n(.*?)\n```', test_text, flags=re.DOTALL)
    print(f"Found {len(matches)} code blocks")
    for i, (lang, code) in enumerate(matches):
        print(f"\nBlock {i}:")
        print(f"Language: '{lang}'")
        print(f"Code: '{code[:50]}...'")
    
    # Test 2: Modified regex
    print("\n\nTest 2: Modified regex")
    print("=" * 50)
    
    def replace_code(match):
        lang = match.group(1) or ''
        code = match.group(2)
        print(f"Found code block: lang='{lang}', code='{code[:50]}...'")
        return f'CODEBLOCK{len(code_blocks)}CODEBLOCK'
    
    code_blocks = []
    result = re.sub(r'```(\w*)\n(.*?)```', replace_code, test_text, flags=re.DOTALL | re.MULTILINE)
    
    print("\nResult preview:")
    print(result[:300] + "...")
    
    # Test 3: Check for ```\n at end
    print("\n\nTest 3: Check pattern")
    print("=" * 50)
    
    # Count ``` occurrences
    count = test_text.count('```')
    print(f"Total ``` count: {count}")
    
    # Find all ``` positions
    pos = 0
    positions = []
    while True:
        pos = test_text.find('```', pos)
        if pos == -1:
            break
        # Check what's after ```
        next_char = test_text[pos+3] if pos+3 < len(test_text) else 'EOF'
        print(f"Position {pos}: next char = '{repr(next_char)}'")
        positions.append(pos)
        pos += 1


if __name__ == "__main__":
    test_code_blocks()