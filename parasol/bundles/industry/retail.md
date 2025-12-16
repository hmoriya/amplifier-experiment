---
bundle:
  name: parasol-industry-retail
  version: 1.0.0
  description: Retail industry templates and patterns for Parasol DDD Framework
  
includes:
  - bundle: ../base/parasol-base.md
  
config:
  industry:
    name: Retail
    segments:
      - physical-stores
      - e-commerce
      - omnichannel
      - marketplace
      
  phases:
    phase2:
      value_stream_templates:
        - id: VS0_customer_journey
          name: カスタマージャーニー
          description: 顧客の購買体験全体の価値創造プロセス
          typical_activities:
            - 商品発見・認知
            - 商品比較・検討
            - 購入決定・決済
            - 商品受取・配送
            - アフターサービス
            
        - id: VS0_merchandise
          name: 商品ライフサイクル管理
          description: 商品の調達から販売までの価値創造
          typical_activities:
            - 市場調査・トレンド分析
            - 商品企画・選定
            - 調達・仕入れ
            - 在庫管理・配置
            - 価格設定・プロモーション
            - 販売分析・改善
            
        - id: VS0_supply_chain
          name: サプライチェーン最適化
          description: 調達から配送までの効率化
          typical_activities:
            - サプライヤー管理
            - 発注・補充計画
            - 物流・配送管理
            - 在庫最適化
            - リードタイム短縮
            
    phase3:
      common_capabilities:
        - name: 需要予測
          domain: core
          description: AIを活用した高精度な需要予測
          
        - name: 在庫最適化
          domain: core
          description: 店舗・倉庫間の在庫配置最適化
          
        - name: 価格最適化
          domain: core
          description: 動的価格設定とプロモーション管理
          
        - name: 顧客分析
          domain: supporting
          description: 購買履歴に基づく顧客セグメンテーション
          
        - name: オムニチャネル統合
          domain: core
          description: 店舗・EC・アプリの統合体験
          
      subdomain_patterns:
        - pattern: 商品管理
          classification: CL2
          typical_contexts:
            - 商品マスター管理
            - カテゴリー管理
            - 商品属性管理
            
        - pattern: 顧客管理
          classification: CL2
          typical_contexts:
            - 顧客プロファイル
            - ロイヤリティプログラム
            - 顧客コミュニケーション
            
    phase4:
      architecture_patterns:
        - name: Headless Commerce
          description: フロントエンドとバックエンドの分離
          when_to_use:
            - 複数のフロントエンドチャネル
            - 高いカスタマイゼーション要求
            - 独立したスケーリング要件
            
        - name: Event-Driven Inventory
          description: イベント駆動の在庫管理
          when_to_use:
            - リアルタイム在庫同期
            - 複数倉庫・店舗運営
            - 高頻度の在庫変動
            
  templates:
    stakeholders:
      - role: 店舗運営責任者
        concerns:
          - 売上目標達成
          - 在庫回転率
          - 顧客満足度
          
      - role: EC事業責任者
        concerns:
          - オンライン売上成長
          - カート放棄率削減
          - 配送効率
          
      - role: マーチャンダイザー
        concerns:
          - 商品構成最適化
          - 仕入原価削減
          - トレンド対応
---

# Retail Industry Bundle for Parasol

小売業界向けのParasolテンプレートとパターンを提供します。

## 含まれるテンプレート

### Value Streams（価値の流れ）
- **カスタマージャーニー**: 認知から購買、アフターサービスまで
- **商品ライフサイクル**: 企画から販売分析まで
- **サプライチェーン**: 調達から配送まで

### 共通ケイパビリティ
- 需要予測
- 在庫最適化
- 価格最適化
- 顧客分析
- オムニチャネル統合

### アーキテクチャパターン
- Headless Commerce
- Event-Driven Inventory
- Microservices per Channel

## 業界特有の考慮事項

### 季節性への対応
- 需要の季節変動を考慮したアーキテクチャ
- スケーラビリティの確保
- プロモーション期間の負荷対策

### オムニチャネル要件
- 店舗とECの在庫統合
- 統一された顧客体験
- チャネル横断の注文管理

### リアルタイム性
- 在庫のリアルタイム同期
- 価格の動的変更
- 即時の顧客対応

## 使用方法

```bash
parasol \
  --bundle ./bundles/base/parasol-base.md \
  --bundle ./bundles/industry/retail.md \
  init my-retail-project
```