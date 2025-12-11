# OP-001 データ収集 CollectData COLLECT_DATA

## 概要

| 項目 | 値 |
|------|-----|
| ID | OP-001 |
| 日本語名 | データ収集 |
| 英語名 | CollectData |
| 定数名 | COLLECT_DATA |
| 所属Capability | CAP-001 顧客データ統合 |

## 説明

各チャネル・システムから顧客関連データを収集し、CDPに取り込む。

## トリガー

| トリガー | 説明 |
|----------|------|
| スケジュール | 定期バッチ収集 |
| イベント | リアルタイムイベント受信 |
| 手動実行 | アドホック取り込み |

## 入力

| 入力 | 型 | 説明 |
|------|-----|------|
| dataSource | DataSource | データソース定義 |
| extractionConfig | ExtractionConfig | 抽出設定 |
| dateRange | DateRange | 対象期間（バッチの場合） |

## 出力

| 出力 | 型 | 説明 |
|------|-----|------|
| ingestionResult | IngestionResult | 取り込み結果 |
| rawData | RawCustomerData[] | 生データ |
| errorRecords | ErrorRecord[] | エラーレコード |

## ビジネスルール

| ルール | 説明 |
|--------|------|
| 重複排除 | 同一イベントの重複取り込み防止 |
| スキーマ検証 | データスキーマの検証 |
| PII暗号化 | 個人情報の暗号化 |

## 関連UseCase

| UseCase | 関係 |
|---------|------|
| UC-001 データソース設定 | ソース設定 |
| UC-002 データ取り込み監視 | 監視 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
