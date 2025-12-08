# OP-008 配信実行 ExecuteDelivery EXECUTE_DELIVERY

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-008 |
| 日本語名 | 配信実行 |
| 英語名 | ExecuteDelivery |
| 定数名 | EXECUTE_DELIVERY |
| 所属Capability | CAP-003 マーケティングオートメーション |

## 説明

メール、Push、SMS等のコミュニケーションを顧客に配信する。

## トリガー

| トリガー | 説明 |
|----------|------|
| ジャーニーステップ | ジャーニー内のアクション |
| スケジュール | 予定配信 |
| イベント | リアルタイムトリガー |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| communication | Communication | コミュニケーション定義 |
| recipients | CustomerProfile[] | 配信先顧客 |
| channel | Channel | 配信チャネル |
| content | Content | コンテンツ |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| deliveryResult | DeliveryResult | 配信結果 |
| deliveryLogs | DeliveryLog[] | 配信ログ |
| failedDeliveries | FailedDelivery[] | 失敗レコード |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| オプトアウト確認 | 配信前に同意確認 |
| 配信時間制限 | 深夜帯配信禁止 |
| 頻度制限 | 顧客あたりの配信頻度制限 |
| リトライ | 失敗時の自動リトライ |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-012 配信実行 | 主UseCase |
| UC-013 配信モニタリング | 監視 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
