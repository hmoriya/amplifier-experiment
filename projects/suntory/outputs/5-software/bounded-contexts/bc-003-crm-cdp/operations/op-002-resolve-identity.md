# OP-002 ID統合 ResolveIdentity RESOLVE_IDENTITY

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-002 |
| 日本語名 | ID統合 |
| 英語名 | ResolveIdentity |
| 定数名 | RESOLVE_IDENTITY |
| 所属Capability | CAP-001 顧客データ統合 |

## 説明

異なるチャネル・システムの顧客IDを統合し、同一顧客を識別する（名寄せ）。

## トリガー

| トリガー | 説明 |
|----------|------|
| データ取り込み後 | 新規データ取り込み時 |
| 日次バッチ | 全体再計算 |
| 手動実行 | 特定顧客の再統合 |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| customerIdentifiers | Identifier[] | 顧客識別子（メール、電話等） |
| matchingRules | MatchingRule[] | マッチングルール |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| unifiedCustomerId | UUID | 統合顧客ID |
| identityGraph | IdentityGraph | ID連携グラフ |
| matchConfidence | Decimal | マッチ信頼度 |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| 決定論的マッチ | メール・電話での完全一致 |
| 確率的マッチ | 名前・住所での類似マッチ |
| 信頼度閾値 | 0.8以上で自動統合 |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-003 顧客ID統合 | 主UseCase |
| UC-004 名寄せ確認 | 手動確認 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
