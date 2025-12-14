# Parasol 6軸システム更新状況

## 更新完了ファイル ✅

### 1. explore-v2.md (新規作成)
- 6軸から動的に3軸を選択する新システム
- 業界別推奨軸の自動提示機能
- インタラクティブな軸選択フロー

### 2. 2-value.md (更新済み)
- 探索モードを5軸から6軸に更新
- 新しい軸名に対応（capability-axis等）
- コングロマリットスコアに基づく推奨を3軸選択方式に変更

### 3. explore.md (旧版として維持)
- explore-v2.mdへの移行を推奨
- 互換性のため現状維持

## 更新が必要なファイル 🔄

### 優先度: 高

1. **1-context.md**
   - 価値軸、事業部軸、フュージョン型の参照が残存
   - 推奨パターンの記述を6軸ベースに更新必要

2. **_axis-selection-guide.md**
   - 軸選択ガイド全体を6軸システムに更新必要
   - スコアリング基準の見直し

3. **4-application-design.md**
   - 軸パターンへの参照確認と更新

### 優先度: 中

1. **industry-specific guides** (業界別ガイド)
   - beverage-food/axis-selection-guide.md
   - regional-bank/axis-selection-guide.md
   - staffing-agency/axis-selection-guide.md
   → 各ファイルの推奨軸を6軸システムに更新

2. **_patterns/_axes/各軸定義ファイル**
   - 既存の軸定義ファイルは英語名で正しく配置済み
   - 内容の整合性確認が必要

### 優先度: 低

1. **サンプルファイル・参考資料**
   - 実際の実行には影響しないが、整合性のため更新推奨

## 6つの軸（標準名称）

1. **capability-axis** - ケイパビリティ軸
2. **business-unit-axis** - 事業部軸  
3. **value-axis** - 価値軸
4. **platform-axis** - プラットフォーム軸
5. **fusion-axis** - 融合軸
6. **multi-tier-vstr-axis** - 多層VST-R軸

## 推奨アクション

1. explore-v2.mdを正式版として採用
2. 1-context.mdの軸参照を更新
3. _axis-selection-guide.mdを6軸システムに全面改訂
4. 業界別ガイドを順次更新

## 注意事項

- 日本語での説明は維持しつつ、軸の識別子は英語名に統一
- 固定3軸選択から動的3軸選択への移行を明確化
- 業界特性に応じた推奨軸の提供を強化