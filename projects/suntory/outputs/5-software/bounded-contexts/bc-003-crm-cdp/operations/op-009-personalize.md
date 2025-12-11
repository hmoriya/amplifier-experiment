# OP-009 パーソナライズ Personalize PERSONALIZE

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-009 |
| 日本語名 | パーソナライズ |
| 英語名 | Personalize |
| 定数名 | PERSONALIZE |
| 所属Capability | CAP-003 マーケティングオートメーション |

## 説明

顧客属性・行動に基づき、コンテンツ・オファーをパーソナライズする。

## トリガー

| トリガー | 説明 |
|----------|------|
| コンテンツ要求 | Webページ表示時 |
| メール生成 | メール作成時 |
| 推奨要求 | 商品推奨時 |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| customerId | UUID | 顧客ID |
| context | PersonalizationContext | コンテキスト情報 |
| contentSlots | ContentSlot[] | コンテンツ枠 |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| personalizedContent | PersonalizedContent | パーソナライズコンテンツ |
| recommendations | Recommendation[] | 推奨アイテム |
| explanations | Explanation[] | 推奨理由 |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| フォールバック | パーソナライズ不可時はデフォルト |
| A/Bテスト | 複数バリエーションのテスト対応 |
| パフォーマンス | 100ms以内でレスポンス |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-014 Webパーソナライズ | Web向け |
| UC-015 メールパーソナライズ | メール向け |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
