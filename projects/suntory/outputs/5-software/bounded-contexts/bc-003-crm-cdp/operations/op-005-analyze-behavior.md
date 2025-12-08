# OP-005 行動分析 AnalyzeBehavior ANALYZE_BEHAVIOR

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-005 |
| 日本語名 | 行動分析 |
| 英語名 | AnalyzeBehavior |
| 定数名 | ANALYZE_BEHAVIOR |
| 所属Capability | CAP-002 顧客分析 |

## 説明

顧客の行動パターンを分析し、インサイトを導出する。

## トリガー

| トリガー | 説明 |
|----------|------|
| 日次バッチ | 定期分析 |
| アドホック | 分析リクエスト |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| targetSegment | Segment | 分析対象セグメント |
| analysisType | AnalysisType | 分析タイプ |
| dateRange | DateRange | 分析期間 |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| behaviorPatterns | BehaviorPattern[] | 行動パターン |
| insights | CustomerInsight[] | インサイト |
| visualizations | Visualization[] | 可視化データ |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| 最小サンプル | 統計的有意性確保 |
| 匿名化 | 個人特定不可な形での分析 |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-008 顧客行動分析 | 主UseCase |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
