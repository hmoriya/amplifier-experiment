# OP-005 キャンペーン分析 AnalyzeCampaign ANALYZE_CAMPAIGN

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-005 |
| 日本語名 | キャンペーン分析 |
| 英語名 | AnalyzeCampaign |
| 定数名 | ANALYZE_CAMPAIGN |
| 所属Capability | CAP-002 キャンペーン管理 |

## 説明

キャンペーンの効果を測定・分析し、ROIを算出する。
得られたインサイトを次回キャンペーンの改善に活用する。

## トリガー

| トリガー | 説明 |
|----------|------|
| キャンペーン終了 | キャンペーン終了後の分析 |
| 中間レビュー | 実行中の中間分析 |
| 月次レポート | 定期的な分析レポート |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| campaignExecution | CampaignExecution | 実行データ |
| deliveryMetrics | DeliveryMetrics | 配信メトリクス |
| salesData | SalesData | 関連販売データ |
| surveyResults | SurveyResult[] | 調査結果（任意） |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| performanceReport | PerformanceReport | 効果レポート |
| roiCalculation | ROICalculation | ROI計算結果 |
| insights | Insight[] | 分析インサイト |
| recommendations | Recommendation[] | 改善提案 |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| アトリビューション | マルチタッチアトリビューションモデル使用 |
| 比較分析 | 過去キャンペーンとの比較必須 |
| セグメント分析 | ターゲットセグメント別の分析 |

## 例外処理

| 例外 | 対応 |
|------|------|
| データ欠損 | 利用可能データで部分分析 |
| 異常値検出 | 除外または補正して分析 |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-009 キャンペーンレポート作成 | 主UseCase |
| UC-010 ROI分析 | ROI算出 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
