#!/usr/bin/env python3
"""
サントリープロジェクト コンプライアンス対応スクリプト

顧客データのマスキングと機密ファイルの削除を実行
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

import yaml


def load_rules(rules_path: Path) -> dict:
    """マスキングルールをYAMLから読み込み"""
    with open(rules_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def apply_replacements(content: str, replacements: dict) -> tuple[str, int]:
    """固定文字列の置換を適用"""
    count = 0
    for old, new in replacements.items():
        if old in content:
            occurrences = content.count(old)
            content = content.replace(old, new)
            count += occurrences
    return content, count


def apply_patterns(content: str, patterns: list) -> tuple[str, int]:
    """正規表現パターンの置換を適用"""
    count = 0
    for pattern_def in patterns:
        pattern = pattern_def["pattern"]
        replacement = pattern_def["replacement"]
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            count += matches
    return content, count


def process_file(file_path: Path, rules: dict) -> dict:
    """単一ファイルを処理"""
    result = {
        "file": str(file_path),
        "company_replacements": 0,
        "partner_replacements": 0,
        "person_replacements": 0,
        "contact_replacements": 0,
        "numeric_replacements": 0,
        "modified": False,
    }

    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # 企業名マスキング
        content, count = apply_replacements(content, rules.get("company_names", {}))
        result["company_replacements"] = count

        # 取引先マスキング
        content, count = apply_replacements(content, rules.get("partners", {}))
        result["partner_replacements"] = count

        # 人名マスキング
        content, count = apply_patterns(content, rules.get("person_patterns", []))
        result["person_replacements"] = count

        # 連絡先マスキング
        content, count = apply_patterns(content, rules.get("contact_patterns", []))
        result["contact_replacements"] = count

        # 数値マスキング
        content, count = apply_patterns(content, rules.get("numeric_patterns", []))
        result["numeric_replacements"] = count

        # 変更があれば書き込み
        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            result["modified"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def delete_files(project_path: Path, delete_list: list) -> list:
    """指定ファイルを削除"""
    deleted = []
    for file_pattern in delete_list:
        target = project_path / file_pattern
        if target.exists():
            # バックアップを作成
            backup_path = target.with_suffix(target.suffix + ".backup")
            shutil.copy2(target, backup_path)
            target.unlink()
            deleted.append(str(target))
    return deleted


def generate_report(results: list, deleted: list, output_path: Path) -> None:
    """コンプライアンス対応レポートを生成"""
    report = []
    report.append("# コンプライアンス対応レポート")
    report.append(f"\n**実行日時**: {datetime.now().isoformat()}")
    report.append("\n---\n")

    # サマリー
    total_replacements = sum(
        r["company_replacements"]
        + r["partner_replacements"]
        + r["person_replacements"]
        + r["contact_replacements"]
        + r["numeric_replacements"]
        for r in results
    )
    modified_files = [r for r in results if r["modified"]]

    report.append("## サマリー")
    report.append(f"\n- **処理ファイル数**: {len(results)}")
    report.append(f"- **変更ファイル数**: {len(modified_files)}")
    report.append(f"- **総置換数**: {total_replacements}")
    report.append(f"- **削除ファイル数**: {len(deleted)}")

    # 削除ファイル
    if deleted:
        report.append("\n## 削除ファイル")
        for f in deleted:
            report.append(f"- `{f}`")

    # マスキング詳細
    report.append("\n## マスキング詳細")
    report.append("\n| ファイル | 企業名 | 取引先 | 人名 | 連絡先 | 数値 |")
    report.append("|----------|--------|--------|------|--------|------|")

    for r in modified_files:
        file_name = Path(r["file"]).name
        report.append(
            f"| {file_name} | {r['company_replacements']} | {r['partner_replacements']} | "
            f"{r['person_replacements']} | {r['contact_replacements']} | {r['numeric_replacements']} |"
        )

    # エラー
    errors = [r for r in results if "error" in r]
    if errors:
        report.append("\n## エラー")
        for r in errors:
            report.append(f"- `{r['file']}`: {r['error']}")

    report.append("\n---\n")
    report.append("**ステータス**: ✅ 完了")

    output_path.write_text("\n".join(report), encoding="utf-8")


def main():
    """メイン処理"""
    script_dir = Path(__file__).parent
    rules_path = script_dir / "masking_rules.yaml"
    project_path = script_dir.parent.parent / "projects" / "suntory"
    report_path = script_dir / "compliance_report.md"

    print(f"🔍 プロジェクトパス: {project_path}")
    print(f"📋 ルールファイル: {rules_path}")

    if not project_path.exists():
        print(f"❌ プロジェクトが見つかりません: {project_path}")
        return

    # ルール読み込み
    rules = load_rules(rules_path)
    print(f"✅ ルール読み込み完了")

    # 全Markdownファイルを処理
    md_files = list(project_path.glob("**/*.md"))
    print(f"📁 対象ファイル数: {len(md_files)}")

    results = []
    for md_file in md_files:
        result = process_file(md_file, rules)
        results.append(result)
        if result["modified"]:
            print(f"  ✏️  {md_file.relative_to(project_path)}")

    # ファイル削除
    deleted = delete_files(project_path, rules.get("delete_files", []))
    for d in deleted:
        print(f"  🗑️  削除: {d}")

    # レポート生成
    generate_report(results, deleted, report_path)
    print(f"\n📊 レポート生成: {report_path}")

    # サマリー表示
    modified_count = len([r for r in results if r["modified"]])
    print(f"\n✅ 完了: {modified_count}ファイル変更, {len(deleted)}ファイル削除")


if __name__ == "__main__":
    main()
