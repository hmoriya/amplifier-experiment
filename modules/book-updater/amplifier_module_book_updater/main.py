#!/usr/bin/env python3
"""
Book Updater - Main CLI entry point.

Updates Parasol V5 book content from latest commands and implementation guides.
"""

import asyncio
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

import click
import yaml
from deepdiff import DeepDiff
from git import Repo
from rich import print as rprint
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .analyzers import ContentAnalyzer, DifferenceAnalyzer
from .extractors import CommandExtractor, PatternExtractor, ExampleExtractor
from .updaters import ChapterUpdater, CodeBlockUpdater, TerminologyUpdater
from .validators import LinkValidator, CodeValidator, ConsistencyValidator

console = Console()


class BookUpdater:
    """Main book updater class"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path.cwd()
        self.book_path = self.base_path / ".claude" / "commands" / "parasol" / "docs" / "book"
        self.commands_path = self.base_path / ".claude" / "commands" / "parasol" / "commands"
        self.modules_path = self.base_path / "modules"
        self.patterns_path = self.base_path / "parasol" / "bundles" / "patterns"
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.content_analyzer = ContentAnalyzer(self.base_path)
        self.command_extractor = CommandExtractor(self.commands_path)
        self.pattern_extractor = PatternExtractor(self.patterns_path)
        self.example_extractor = ExampleExtractor(self.modules_path)
        
        self.chapter_updater = ChapterUpdater(self.config)
        self.code_updater = CodeBlockUpdater()
        self.terminology_updater = TerminologyUpdater(self.config.get("terminology", {}))
        
        self.link_validator = LinkValidator(self.base_path)
        self.code_validator = CodeValidator()
        self.consistency_validator = ConsistencyValidator()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load update configuration"""
        config_path = self.base_path / "update-rules.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            "rules": {
                "command_sync": {
                    "enabled": True,
                    "update_mode": "merge"
                },
                "code_examples": {
                    "validation": True,
                    "syntax_check": True
                },
                "terminology": {
                    "strict_mode": False
                }
            },
            "deprecated": [
                {
                    "pattern": "Event Sourcing",
                    "replacement": "軽量イベント通知"
                },
                {
                    "pattern": "Backend SAGA",
                    "replacement": "フロントエンドオーケストレーション"
                }
            ]
        }
    
    async def analyze(self) -> Dict[str, Any]:
        """Analyze differences between book and latest implementations"""
        console.print("\n[bold blue]📊 書籍コンテンツの分析中...[/bold blue]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Extract latest information
            task = progress.add_task("最新コマンドの抽出...", total=None)
            latest_commands = await self.command_extractor.extract_all()
            progress.update(task, completed=True)
            
            task = progress.add_task("パターンの抽出...", total=None)
            latest_patterns = await self.pattern_extractor.extract_all()
            progress.update(task, completed=True)
            
            task = progress.add_task("実装例の抽出...", total=None)
            latest_examples = await self.example_extractor.extract_all()
            progress.update(task, completed=True)
            
            # Analyze current book content
            task = progress.add_task("書籍コンテンツの分析...", total=None)
            book_analysis = await self.content_analyzer.analyze_book(self.book_path)
            progress.update(task, completed=True)
        
        # Compare and find differences
        differences = {
            "new_commands": self._find_new_items(latest_commands, book_analysis.get("commands", {})),
            "updated_patterns": self._find_updated_items(latest_patterns, book_analysis.get("patterns", {})),
            "outdated_examples": self._find_outdated_examples(latest_examples, book_analysis.get("examples", {})),
            "deprecated_terms": self._find_deprecated_terms(book_analysis.get("content", "")),
            "broken_links": await self.link_validator.validate_all(self.book_path),
            "invalid_code": await self.code_validator.validate_book(self.book_path)
        }
        
        # Generate summary
        summary = {
            "total_issues": sum(len(v) for v in differences.values()),
            "new_commands": len(differences["new_commands"]),
            "updated_patterns": len(differences["updated_patterns"]),
            "outdated_examples": len(differences["outdated_examples"]),
            "deprecated_terms": len(differences["deprecated_terms"]),
            "broken_links": len(differences["broken_links"]),
            "invalid_code": len(differences["invalid_code"])
        }
        
        # Display results
        self._display_analysis_results(summary, differences)
        
        return {
            "summary": summary,
            "differences": differences,
            "timestamp": datetime.now().isoformat()
        }
    
    def _find_new_items(self, latest: Dict, current: Dict) -> List[str]:
        """Find new items not in book"""
        return [k for k in latest.keys() if k not in current]
    
    def _find_updated_items(self, latest: Dict, current: Dict) -> List[Dict]:
        """Find items that have been updated"""
        updated = []
        for key in set(latest.keys()) & set(current.keys()):
            diff = DeepDiff(current[key], latest[key], ignore_order=True)
            if diff:
                updated.append({
                    "name": key,
                    "changes": self._summarize_diff(diff)
                })
        return updated
    
    def _find_outdated_examples(self, latest: Dict, current: Dict) -> List[Dict]:
        """Find examples that are outdated"""
        outdated = []
        for key in current.keys():
            if key in latest:
                # Check if example code has changed significantly
                if self._is_code_different(current[key], latest[key]):
                    outdated.append({
                        "name": key,
                        "location": current[key].get("location", "unknown"),
                        "reason": "Code has been updated in implementation"
                    })
        return outdated
    
    def _find_deprecated_terms(self, content: str) -> List[Dict]:
        """Find deprecated terms in content"""
        found = []
        for deprecated in self.config.get("deprecated", []):
            pattern = deprecated["pattern"]
            if pattern in content:
                occurrences = len(re.findall(pattern, content))
                found.append({
                    "term": pattern,
                    "replacement": deprecated["replacement"],
                    "occurrences": occurrences
                })
        return found
    
    def _is_code_different(self, old_code: str, new_code: str) -> bool:
        """Check if code has significant differences"""
        # Normalize whitespace and comments
        old_normalized = re.sub(r'\s+', ' ', re.sub(r'#.*$', '', old_code, flags=re.MULTILINE))
        new_normalized = re.sub(r'\s+', ' ', re.sub(r'#.*$', '', new_code, flags=re.MULTILINE))
        
        # Simple similarity check (could be enhanced)
        return old_normalized != new_normalized
    
    def _summarize_diff(self, diff: DeepDiff) -> str:
        """Summarize DeepDiff results"""
        summary_parts = []
        if 'values_changed' in diff:
            summary_parts.append(f"{len(diff['values_changed'])} values changed")
        if 'dictionary_item_added' in diff:
            summary_parts.append(f"{len(diff['dictionary_item_added'])} items added")
        if 'dictionary_item_removed' in diff:
            summary_parts.append(f"{len(diff['dictionary_item_removed'])} items removed")
        return ", ".join(summary_parts)
    
    def _display_analysis_results(self, summary: Dict, differences: Dict):
        """Display analysis results in a nice format"""
        # Summary table
        table = Table(title="分析結果サマリー")
        table.add_column("項目", style="cyan")
        table.add_column("件数", style="magenta")
        
        table.add_row("新しいコマンド", str(summary["new_commands"]))
        table.add_row("更新されたパターン", str(summary["updated_patterns"]))
        table.add_row("古い実装例", str(summary["outdated_examples"]))
        table.add_row("廃止された用語", str(summary["deprecated_terms"]))
        table.add_row("壊れたリンク", str(summary["broken_links"]))
        table.add_row("無効なコード", str(summary["invalid_code"]))
        table.add_row("", "")
        table.add_row("[bold]合計[/bold]", f"[bold]{summary['total_issues']}[/bold]")
        
        console.print(table)
        
        # Details
        if summary["total_issues"] > 0:
            console.print("\n[bold]詳細:[/bold]")
            
            if differences["new_commands"]:
                console.print("\n[yellow]新しいコマンド:[/yellow]")
                for cmd in differences["new_commands"][:5]:
                    console.print(f"  • {cmd}")
                if len(differences["new_commands"]) > 5:
                    console.print(f"  ... 他 {len(differences['new_commands']) - 5} 件")
            
            if differences["deprecated_terms"]:
                console.print("\n[yellow]廃止された用語:[/yellow]")
                for term in differences["deprecated_terms"]:
                    console.print(f"  • '{term['term']}' → '{term['replacement']}' ({term['occurrences']}箇所)")
    
    async def update(self, 
                    chapters: Optional[List[int]] = None,
                    dry_run: bool = False,
                    interactive: bool = False,
                    backup: bool = True) -> Dict[str, Any]:
        """Update book content"""
        
        # Create backup if requested
        if backup and not dry_run:
            self._create_backup()
        
        # Analyze first
        analysis = await self.analyze()
        
        if analysis["summary"]["total_issues"] == 0:
            console.print("\n[green]✅ 更新の必要はありません。書籍は最新の状態です。[/green]")
            return {"status": "up_to_date"}
        
        # Plan updates
        update_plan = self._create_update_plan(analysis["differences"])
        
        if interactive:
            # Show plan and ask for confirmation
            self._display_update_plan(update_plan)
            if not click.confirm("\n更新を実行しますか？"):
                return {"status": "cancelled"}
        
        # Execute updates
        if not dry_run:
            results = await self._execute_updates(update_plan, chapters)
            
            # Validate after update
            validation_results = await self._validate_updates()
            
            # Generate report
            report = self._generate_update_report(results, validation_results)
            
            # Save report
            report_path = self.base_path / f"book-update-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            console.print(f"\n[green]✅ 更新完了！レポート: {report_path}[/green]")
            
            return {
                "status": "completed",
                "report_path": str(report_path),
                "results": results
            }
        else:
            console.print("\n[yellow]ドライランモード - 実際の更新は行われませんでした。[/yellow]")
            return {
                "status": "dry_run",
                "plan": update_plan
            }
    
    def _create_backup(self):
        """Create backup of current book"""
        backup_dir = self.base_path / "backups" / f"book-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        shutil.copytree(self.book_path, backup_dir / "book", dirs_exist_ok=True)
        console.print(f"[green]バックアップ作成完了: {backup_dir}[/green]")
    
    def _create_update_plan(self, differences: Dict) -> List[Dict]:
        """Create update plan from differences"""
        plan = []
        
        # Commands updates
        for cmd in differences["new_commands"]:
            plan.append({
                "type": "add_command",
                "target": cmd,
                "priority": "high",
                "description": f"新しいコマンド '{cmd}' を追加"
            })
        
        # Pattern updates
        for pattern in differences["updated_patterns"]:
            plan.append({
                "type": "update_pattern",
                "target": pattern["name"],
                "priority": "medium",
                "description": f"パターン '{pattern['name']}' を更新: {pattern['changes']}"
            })
        
        # Example updates
        for example in differences["outdated_examples"]:
            plan.append({
                "type": "update_example",
                "target": example["name"],
                "location": example["location"],
                "priority": "medium",
                "description": f"実装例 '{example['name']}' を更新"
            })
        
        # Terminology updates
        for term in differences["deprecated_terms"]:
            plan.append({
                "type": "update_terminology",
                "target": term["term"],
                "replacement": term["replacement"],
                "priority": "high",
                "description": f"用語 '{term['term']}' を '{term['replacement']}' に置換 ({term['occurrences']}箇所)"
            })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        plan.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return plan
    
    def _display_update_plan(self, plan: List[Dict]):
        """Display update plan"""
        console.print("\n[bold]更新計画:[/bold]")
        
        table = Table()
        table.add_column("優先度", style="cyan")
        table.add_column("種類", style="magenta")
        table.add_column("説明", style="white")
        
        for item in plan:
            priority_style = {
                "high": "[red]高[/red]",
                "medium": "[yellow]中[/yellow]",
                "low": "[green]低[/green]"
            }
            table.add_row(
                priority_style.get(item["priority"], item["priority"]),
                item["type"],
                item["description"]
            )
        
        console.print(table)
    
    async def _execute_updates(self, plan: List[Dict], chapters: Optional[List[int]] = None) -> Dict:
        """Execute update plan"""
        results = {
            "successful": [],
            "failed": [],
            "skipped": []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            for item in plan:
                task = progress.add_task(f"更新中: {item['description']}", total=None)
                
                try:
                    if item["type"] == "update_terminology":
                        # Update terminology across all chapters
                        updated_files = await self.terminology_updater.update_all(
                            self.book_path,
                            item["target"],
                            item["replacement"]
                        )
                        results["successful"].append({
                            "item": item,
                            "updated_files": updated_files
                        })
                    
                    elif item["type"] == "add_command":
                        # Add new command reference
                        chapter_file = self._find_command_chapter()
                        if chapter_file:
                            await self.chapter_updater.add_command_reference(
                                chapter_file,
                                item["target"]
                            )
                            results["successful"].append({
                                "item": item,
                                "updated_file": str(chapter_file)
                            })
                    
                    elif item["type"] == "update_example":
                        # Update code example
                        if chapters and not self._is_in_chapters(item["location"], chapters):
                            results["skipped"].append(item)
                        else:
                            updated = await self.code_updater.update_example(
                                Path(item["location"]),
                                item["target"]
                            )
                            if updated:
                                results["successful"].append({
                                    "item": item,
                                    "updated_file": item["location"]
                                })
                    
                    # Add more update types as needed
                    
                except Exception as e:
                    results["failed"].append({
                        "item": item,
                        "error": str(e)
                    })
                
                progress.update(task, completed=True)
        
        return results
    
    def _find_command_chapter(self) -> Optional[Path]:
        """Find chapter containing command reference"""
        # Look for command reference chapter
        for chapter_file in self.book_path.glob("part*/chapter*.md"):
            content = chapter_file.read_text(encoding='utf-8')
            if "コマンドリファレンス" in content or "Command Reference" in content:
                return chapter_file
        return None
    
    def _is_in_chapters(self, location: str, chapters: List[int]) -> bool:
        """Check if location is in specified chapters"""
        # Extract chapter number from location
        match = re.search(r'chapter(\d+)', location)
        if match:
            chapter_num = int(match.group(1))
            return chapter_num in chapters
        return False
    
    async def _validate_updates(self) -> Dict:
        """Validate updates"""
        return {
            "links": await self.link_validator.validate_all(self.book_path),
            "code": await self.code_validator.validate_book(self.book_path),
            "consistency": await self.consistency_validator.validate_book(self.book_path)
        }
    
    def _generate_update_report(self, results: Dict, validation: Dict) -> str:
        """Generate update report"""
        report = f"""# Book Update Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 概要

- 成功した更新: {len(results['successful'])}
- 失敗した更新: {len(results['failed'])}
- スキップした更新: {len(results['skipped'])}

## 詳細

### 成功した更新

"""
        for item in results['successful']:
            report += f"- {item['item']['description']}\n"
            if 'updated_files' in item:
                for f in item['updated_files']:
                    report += f"  - {f}\n"
            elif 'updated_file' in item:
                report += f"  - {item['updated_file']}\n"
        
        if results['failed']:
            report += "\n### 失敗した更新\n\n"
            for item in results['failed']:
                report += f"- {item['item']['description']}\n"
                report += f"  - エラー: {item['error']}\n"
        
        report += "\n## 検証結果\n\n"
        
        if validation['links']:
            report += f"- 壊れたリンク: {len(validation['links'])}\n"
        if validation['code']:
            report += f"- 無効なコード: {len(validation['code'])}\n"
        if validation['consistency']:
            report += f"- 一貫性の問題: {len(validation['consistency'])}\n"
        
        return report


@click.group()
def cli():
    """Book updater for Parasol V5 documentation"""
    pass


@cli.command()
@click.option('--chapter', '-c', type=int, multiple=True, help='Specific chapter(s) to analyze')
@click.option('--save', '-s', type=click.Path(), help='Save analysis results to file')
def check(chapter: tuple, save: Optional[str]):
    """Check for updates needed in the book"""
    asyncio.run(_check(chapter, save))


async def _check(chapter: tuple, save: Optional[str]):
    """Async implementation of check command"""
    updater = BookUpdater()
    
    try:
        analysis = await updater.analyze()
        
        if save:
            save_path = Path(save)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            console.print(f"\n分析結果を保存しました: {save_path}")
    
    except Exception as e:
        console.print(f"[red]エラー: {e}[/red]")
        raise


@cli.command()
@click.option('--chapter', '-c', type=int, multiple=True, help='Specific chapter(s) to update')
@click.option('--dry-run', is_flag=True, help='Show what would be updated without making changes')
@click.option('--interactive', '-i', is_flag=True, help='Confirm each update interactively')
@click.option('--no-backup', is_flag=True, help='Skip creating backup')
@click.option('--config', type=click.Path(exists=True), help='Custom configuration file')
def update(chapter: tuple, dry_run: bool, interactive: bool, no_backup: bool, config: Optional[str]):
    """Update book content from latest implementations"""
    asyncio.run(_update(chapter, dry_run, interactive, no_backup, config))


async def _update(chapter: tuple, dry_run: bool, interactive: bool, no_backup: bool, config: Optional[str]):
    """Async implementation of update command"""
    updater = BookUpdater()
    
    try:
        results = await updater.update(
            chapters=list(chapter) if chapter else None,
            dry_run=dry_run,
            interactive=interactive,
            backup=not no_backup
        )
        
        if results["status"] == "completed":
            console.print(f"\n[green]✅ 更新が完了しました！[/green]")
            console.print(f"レポート: {results['report_path']}")
    
    except Exception as e:
        console.print(f"[red]エラー: {e}[/red]")
        raise


@cli.command()
@click.argument('backup_path', type=click.Path(exists=True))
def restore(backup_path: str):
    """Restore book from backup"""
    backup_path = Path(backup_path)
    book_path = Path.cwd() / ".claude" / "commands" / "parasol" / "docs" / "book"
    
    if not backup_path.exists():
        console.print(f"[red]バックアップが見つかりません: {backup_path}[/red]")
        return
    
    # Confirm
    if not click.confirm(f"本当に {backup_path} から復元しますか？"):
        return
    
    # Restore
    shutil.rmtree(book_path, ignore_errors=True)
    shutil.copytree(backup_path / "book", book_path)
    
    console.print("[green]✅ 復元完了！[/green]")


@cli.command()
def clear_cache():
    """Clear analysis cache"""
    cache_dir = Path.cwd() / ".book-updater-cache"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        console.print("[green]キャッシュをクリアしました。[/green]")
    else:
        console.print("[yellow]キャッシュは存在しません。[/yellow]")


if __name__ == '__main__':
    cli()