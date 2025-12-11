# BC-003 CRM-CDP 顧客データプラットフォーム

## 概要

顧客データの統合管理、セグメンテーション、顧客インサイト分析、マーケティングオートメーションを担当するBounded Context。

## スコープ

### 含むもの

- 顧客データ統合（CDP機能）
- 顧客ID統合・名寄せ
- 顧客セグメンテーション
- 顧客インサイト分析
- カスタマージャーニー管理
- マーケティングオートメーション
- コミュニケーション配信管理
- パーソナライゼーション

### 含まないもの

- マーケティングキャンペーン企画（→ BC-002 MKT-Beverage）
- EC販売管理（→ BC-008 SLS-Direct）
- ポイントプログラム（→ BC-006 SVC-Loyalty）

## サブドメイン分類

| 分類 | 理由 |
|------|------|
| Core Domain | 顧客理解と1to1マーケティングの基盤 |

## コンテキストマップ

### 上流（依存先）

| BC | 関係 | 受け取るデータ |
|----|------|----------------|
| BC-008 SLS-Direct | Customer-Supplier | EC購買データ |
| BC-006 SVC-Loyalty | Customer-Supplier | ポイント活動データ |
| BC-010 DX-Web | Customer-Supplier | Webアクセスログ |
| BC-011 DX-Mobile | Customer-Supplier | アプリ行動データ |

### 下流（依存元）

| BC | 関係 | 提供するデータ |
|----|------|----------------|
| BC-002 MKT-Beverage | Customer-Supplier | 顧客セグメント、インサイト |
| BC-008 SLS-Direct | Customer-Supplier | パーソナライズ推奨 |
| BC-010 DX-Web | Customer-Supplier | パーソナライズコンテンツ |

## L3 Capabilities

| ID | 名前 | 説明 |
|----|------|------|
| CAP-001 | 顧客データ統合 CustomerDataIntegration | 複数チャネルからのデータ統合とID連携 |
| CAP-002 | 顧客分析 CustomerAnalytics | 顧客行動分析とインサイト導出 |
| CAP-003 | マーケティングオートメーション MarketingAutomation | 自動化されたコミュニケーション配信 |

## 主要サービス

| サービス | 責務 |
|----------|------|
| CustomerProfileService | 統合顧客プロファイル管理 |
| IdentityResolutionService | 顧客ID統合・名寄せ |
| SegmentationService | セグメント作成・管理 |
| InsightService | 顧客インサイト分析 |
| JourneyService | カスタマージャーニー管理 |
| CampaignExecutionService | MA配信実行 |
| PersonalizationService | パーソナライゼーション |

## 主要ユーザー

| ユーザー | 役割 |
|----------|------|
| CRMマネージャー | CRM戦略策定、顧客理解推進 |
| データアナリスト | 顧客分析、セグメント設計 |
| MAオペレーター | キャンペーン配信運用 |
| マーケティング担当者 | セグメント活用、施策実行 |

## 成功指標

| 指標 | 目標値 |
|------|--------|
| 顧客ID統合率 | 85%以上 |
| セグメント精度 | 予測精度80%以上 |
| MA配信成功率 | 99.5%以上 |
| パーソナライズCVR向上 | 基準比+30% |

---

**作成日**: 2025-12-05
**更新日**: 2025-12-05
