# Operation: op-006 技術移転 [TransferTechnology]

## 概要

| 項目 | 値 |
|------|-----|
| ID | op-006 |
| 日本語名 | 技術移転 |
| 英語名 | TransferTechnology |
| 定数名 | TRANSFER_TECHNOLOGY |
| 所属Capability | cap-003 浄水技術 |
| ステータス | Draft |

## 説明

研究開発で確立した浄水プロセスを製造部門へ移転する。
技術ドキュメント、トレーニング、検証テストを含む移転プロセスを管理する。

## 事前条件

- 移転対象の浄水プロセスが承認済みであること
- 移転先の製造部門が特定されていること
- 移転計画が承認済みであること

## 事後条件

- 技術ドキュメントが製造部門に提供されていること
- トレーニングが完了していること
- 検証テストが合格していること
- 移転完了が記録されていること

## 入力

| パラメータ | 型 | 必須 | 説明 |
|------------|-----|------|------|
| processId | UUID | Yes | 浄水プロセスID |
| targetBusinessUnit | String | Yes | 移転先事業部（Beverage/Spirits/Beer/Wine/Health） |
| targetFactory | String | Yes | 移転先工場 |
| plannedDate | Date | Yes | 移転予定日 |
| transferLead | UUID | Yes | 移転責任者ID |
| documents | Document[] | Yes | 技術ドキュメント |

## 出力

| フィールド | 型 | 説明 |
|------------|-----|------|
| transferId | UUID | 移転ID |
| status | Enum | ステータス（PLANNED/IN_PROGRESS/COMPLETED/FAILED） |
| phases | TransferPhase[] | 移転フェーズ一覧 |
| completedAt | DateTime | 完了日時（完了時のみ） |

## ビジネスルール

1. **BR-001**: 移転は3フェーズ（ドキュメント提供→トレーニング→検証）で実施
2. **BR-002**: 各フェーズは順次完了が必要
3. **BR-003**: 検証テストは製造部門と共同で実施
4. **BR-004**: 移転完了後3ヶ月はフォローアップ期間

## 例外・エラー

| エラーコード | 条件 | メッセージ |
|--------------|------|------------|
| E001 | プロセス未承認 | 浄水プロセスが承認されていません |
| E002 | 移転先不正 | 指定された移転先が存在しません |
| E003 | 検証不合格 | 検証テストが不合格です |

## 関連UseCase

| ID | 名称 |
|----|------|
| uc-006 | 技術移転 [TechTransfer] |

## シーケンス

```
1. 移転計画を受け付ける
2. プロセスの承認状況を検証する
3. 移転先の準備状況を確認する
4. Phase 1: 技術ドキュメントを提供する
5. Phase 2: トレーニングを実施する
6. Phase 3: 検証テストを実施する
7. 検証結果を評価する
8. 移転完了を記録する
9. 技術移転イベントを発行する
```

## ドメインイベント

| イベント | 発行条件 |
|----------|----------|
| TechnologyTransferStarted | 移転開始時 |
| TechnologyTransferCompleted | 移転完了時 |
| TechnologyTransferFailed | 移転失敗時 |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
**作成者**: AI Assistant
