# OP-008 競合分析 AnalyzeCompetitors ANALYZE_COMPETITORS

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-008 |
| 日本語名 | 競合分析 |
| 英語名 | AnalyzeCompetitors |
| 定数名 | ANALYZE_COMPETITORS |
| 所属Capability | CAP-003 市場分析 |

## 説明

競合他社の製品、価格、プロモーション、チャネル戦略を分析し、
自社の競争優位性を評価する。

## トリガー

| トリガー | 説明 |
|----------|------|
| 定期分析 | 月次/四半期の定期分析 |
| 競合動向 | 競合の新製品・キャンペーン発表時 |
| 戦略策定 | 自社戦略策定時の競合分析 |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| competitorProducts | CompetitorProduct[] | 競合製品情報 |
| marketShareData | MarketShareData | 市場シェアデータ |
| pricingData | PricingData | 価格情報 |
| promotionData | PromotionData[] | 競合プロモーション情報 |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| competitorProfiles | CompetitorProfile[] | 競合プロファイル |
| swotAnalysis | SWOTAnalysis | SWOT分析 |
| competitivePosition | CompetitivePosition | 競争ポジション評価 |
| actionItems | ActionItem[] | 推奨アクション |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| 情報源 | 公開情報のみ使用 |
| 更新頻度 | 主要競合は月次更新 |
| カバレッジ | 上位5社は必ずカバー |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-013 競合分析 | 主UseCase |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
