#!/usr/bin/env python3
"""
V5アジャイルガイド HTML to PDF変換スクリプト
"""

import subprocess
import sys
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_html_to_pdf():
    """HTMLをPDFに変換する"""
    
    # ファイルパス設定
    html_path = Path("/Users/hmoriya/Develop/github/github.com/hmoriya/amplifier-experiment/.claude/commands/parasol/docs/v5_agile_guide_part1.html")
    pdf_path = html_path.with_suffix('.pdf')
    
    if not html_path.exists():
        logger.error(f"❌ HTMLファイルが見つかりません: {html_path}")
        return None
        
    logger.info(f"📖 HTMLファイル: {html_path}")
    logger.info(f"📄 PDF出力先: {pdf_path}")
    
    # Try different methods
    methods = [
        {
            'name': 'Chrome/Chromium headless',
            'check': ['which', 'google-chrome'],
            'command': [
                'google-chrome', 
                '--headless', 
                '--disable-gpu',
                '--print-to-pdf=' + str(pdf_path),
                '--no-pdf-header-footer',
                'file://' + str(html_path)
            ]
        },
        {
            'name': 'Chromium (macOS)',
            'check': ['which', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
            'command': [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                '--print-to-pdf=' + str(pdf_path),
                '--no-pdf-header-footer',
                'file://' + str(html_path)
            ]
        },
        {
            'name': 'wkhtmltopdf',
            'check': ['which', 'wkhtmltopdf'],
            'command': [
                'wkhtmltopdf',
                '--enable-local-file-access',
                '--page-size', 'A4',
                '--margin-top', '20mm',
                '--margin-bottom', '20mm',
                '--margin-left', '20mm',
                '--margin-right', '20mm',
                str(html_path),
                str(pdf_path)
            ]
        }
    ]
    
    # Try each method
    for method in methods:
        logger.info(f"\n🔍 {method['name']}を試しています...")
        
        # Check if tool is available
        check_result = subprocess.run(method['check'], capture_output=True, text=True)
        if check_result.returncode != 0:
            logger.info(f"   ❌ {method['name']}は利用できません")
            continue
            
        # Try conversion
        logger.info(f"   ⚙️  変換中...")
        try:
            result = subprocess.run(
                method['command'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and pdf_path.exists():
                file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
                logger.info(f"   ✅ 成功！ PDFファイルサイズ: {file_size_mb:.2f} MB")
                return pdf_path
            else:
                logger.info(f"   ❌ 変換失敗")
                if result.stderr:
                    logger.debug(f"   エラー: {result.stderr}")
                    
        except subprocess.TimeoutExpired:
            logger.info(f"   ❌ タイムアウト")
        except Exception as e:
            logger.info(f"   ❌ エラー: {str(e)}")
    
    # If all methods failed, suggest manual conversion
    logger.warning("\n⚠️  自動PDF変換が失敗しました")
    logger.info("\n📝 手動でPDFに変換する方法:")
    logger.info("1. ブラウザで以下のファイルを開く:")
    logger.info(f"   open '{html_path}'")
    logger.info("2. ブラウザのメニューから「印刷」を選択")
    logger.info("3. 「PDFとして保存」を選択")
    logger.info("4. 保存先とファイル名を指定")
    
    # Alternative: create a simple script to open in browser
    open_script = html_path.parent / "open_and_print.sh"
    with open(open_script, 'w') as f:
        f.write(f"""#!/bin/bash
# V5アジャイルガイドをブラウザで開く
echo "📖 ブラウザでHTMLを開いています..."
open '{html_path}'
echo ""
echo "📝 PDFに変換する手順:"
echo "1. ブラウザのメニューから「ファイル」→「印刷」を選択"
echo "2. 「PDFとして保存」を選択"
echo "3. ファイル名: v5_agile_guide_part1.pdf"
echo ""
""")
    
    import os
    os.chmod(open_script, 0o755)
    logger.info(f"\n🔧 便利スクリプトを作成しました:")
    logger.info(f"   {open_script}")
    logger.info(f"   実行: sh '{open_script}'")
    
    return None

if __name__ == "__main__":
    logger.info("🚀 V5アジャイルガイド PDF変換開始...")
    
    pdf_path = convert_html_to_pdf()
    
    if pdf_path:
        logger.info(f"\n✅ PDF変換完了!")
        logger.info(f"📄 PDFファイル: {pdf_path}")
        logger.info(f"📂 開く: open '{pdf_path}'")
    else:
        logger.info(f"\n❌ 自動PDF変換に失敗しました")
        logger.info("上記の手動変換方法をお試しください")