# OP-006 市場調査実施 ConductMarketResearch CONDUCT_MARKET_RESEARCH

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-006 |
| 日本語名 | 市場調査実施 |
| 英語名 | ConductMarketResearch |
| 定数名 | CONDUCT_MARKET_RESEARCH |
| 所属Capability | CAP-003 市場分析 |

## 説明

定量・定性の市場調査を計画・実施し、市場動向や消費者ニーズを把握する。

## トリガー

| トリガー | 説明 |
|----------|------|
| 定期調査 | 年次/四半期の定期調査 |
| 新製品開発 | 製品コンセプトテスト |
| 戦略策定 | 戦略立案のための調査 |
| 問題解決 | 特定課題への対応調査 |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| researchBrief | ResearchBrief | 調査概要 |
| targetAudience | AudienceDefinition | 調査対象 |
| methodology | ResearchMethodology | 調査手法 |
| budget | Budget | 調査予算 |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| researchData | ResearchData | 収集データ |
| analysisReport | MarketReport | 分析レポート |
| insights | MarketInsight[] | 市場インサイト |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| サンプルサイズ | 統計的有意性を確保するサイズ |
| 調査倫理 | 個人情報保護、調査倫理遵守 |
| 第三者機関 | 重要調査は第三者機関活用 |

## 例外処理

| 例外 | 対応 |
|------|------|
| 回収率不足 | 追加サンプリング |
| データ品質問題 | 異常回答除外、再調査検討 |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-011 市場調査実施 | 主UseCase |
| UC-012 調査レポート作成 | レポート生成 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
