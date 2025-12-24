#!/usr/bin/env python3
"""
Generate all Parasol V5 books
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_generator(script_name: str, description: str):
    """Run a book generator script"""
    print(f"\n{'=' * 60}")
    print(f"📚 {description}")
    print(f"{'=' * 60}")
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"⚠️  Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Failed: {description}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Generate all books"""
    print(f"\n🚀 Parasol V5 Book Generation Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define books to generate
    books = [
        ("generate_parasol_book.py", "Parasol V5 完全ガイド（15章）"),
        ("generate_good_design_book_part1.py", "良い設計とは何か - 第1部"),
        ("generate_v5_agile_guide.py", "アジャイル原点回帰ガイド（改訂版）"),
        ("generate_v5_agile_guide_part1.py", "アジャイル実践ガイド（初版）"),
    ]
    
    # Track results
    results = []
    
    # Generate each book
    for script, description in books:
        success = run_generator(script, description)
        results.append((description, success))
    
    # Summary
    print(f"\n{'=' * 60}")
    print("📊 生成結果サマリー")
    print(f"{'=' * 60}")
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    for description, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {description}")
    
    print(f"\n完了: {success_count}/{total_count} 成功")
    print(f"終了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return exit code based on results
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())