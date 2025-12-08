# OP-009 トレンド分析 AnalyzeTrends ANALYZE_TRENDS

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-009 |
| 日本語名 | トレンド分析 |
| 英語名 | AnalyzeTrends |
| 定数名 | ANALYZE_TRENDS |
| 所属Capability | CAP-003 市場分析 |

## 説明

消費者行動、市場動向、社会トレンドを分析し、将来の市場変化を予測する。

## トリガー

| トリガー | 説明 |
|----------|------|
| 定期分析 | 四半期のトレンドレビュー |
| 社会変化 | 大きな社会変化の発生時 |
| 戦略計画 | 中長期計画策定時 |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| consumerData | ConsumerData | 消費者行動データ |
| socialTrends | SocialTrendData | 社会トレンドデータ |
| searchTrends | SearchTrendData | 検索トレンドデータ |
| industryReports | IndustryReport[] | 業界レポート |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| trendReport | TrendReport | トレンドレポート |
| emergingTrends | EmergingTrend[] | 新興トレンド |
| implications | Implication[] | 自社への影響 |
| opportunities | Opportunity[] | 機会 |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| 多角的分析 | 複数データソースの統合 |
| 時間軸 | 短期・中期・長期の視点 |
| 検証 | 仮説は定量データで検証 |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-014 トレンド分析 | 主UseCase |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
