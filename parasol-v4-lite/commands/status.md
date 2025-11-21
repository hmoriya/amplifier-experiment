# /parasol:status - プロジェクトステータス確認

## コマンド: `/parasol:status`

現在のParasol V4 Liteプロジェクトの進行状況を確認します。

## 実行内容

このコマンドは以下を確認します：
1. 完了済みフェーズ
2. 現在のフェーズ
3. 未実行フェーズ
4. 各フェーズの成果物状態

## ステータス確認スクリプト

```bash
#!/bin/bash

echo "========================================="
echo "  Parasol V4 Lite プロジェクトステータス"
echo "========================================="
echo ""

# 基本パス
OUTPUT_DIR="outputs"

# フェーズ定義
declare -a phases=(
    "1-context:プロジェクトコンテキスト"
    "2-value:価値定義"
    "3-business:ビジネス設計"
    "4-architecture:アーキテクチャ設計"
    "5-software:ソフトウェア設計"
    "6-implementation:実装"
    "7-platform:プラットフォーム"
)

# 各フェーズのステータス確認
echo "【フェーズ進行状況】"
echo ""

completed=0
current=""
pending=0

for phase_info in "${phases[@]}"; do
    IFS=':' read -r phase_dir phase_name <<< "$phase_info"

    if [ -d "$OUTPUT_DIR/$phase_dir" ] && [ "$(ls -A $OUTPUT_DIR/$phase_dir 2>/dev/null)" ]; then
        echo "✅ Phase ${phase_dir%%-*}: $phase_name - 完了"
        ((completed++))

        # 成果物をリスト
        echo "   成果物:"
        for file in $OUTPUT_DIR/$phase_dir/*; do
            if [ -f "$file" ]; then
                echo "   - $(basename $file)"
            fi
        done
    elif [ -d "$OUTPUT_DIR/$phase_dir" ]; then
        if [ -z "$current" ]; then
            echo "🔄 Phase ${phase_dir%%-*}: $phase_name - 進行中"
            current=$phase_dir
        else
            echo "⏸️  Phase ${phase_dir%%-*}: $phase_name - 待機中"
            ((pending++))
        fi
    else
        echo "⏸️  Phase ${phase_dir%%-*}: $phase_name - 未開始"
        ((pending++))
    fi
    echo ""
done

echo "========================================="
echo "【サマリー】"
echo "完了: $completed フェーズ"
echo "進行中: $([ -n "$current" ] && echo "1" || echo "0") フェーズ"
echo "未着手: $pending フェーズ"
echo "========================================="

# 次のアクション提案
echo ""
echo "【次のアクション】"
if [ $completed -eq 0 ]; then
    echo "👉 /parasol:1-context でプロジェクトを開始してください"
elif [ -n "$current" ]; then
    echo "👉 現在のフェーズを完了するか、次のフェーズに進んでください"
elif [ $completed -lt 7 ]; then
    next_phase=$((completed + 1))
    echo "👉 /parasol:$next_phase-$(echo ${phases[$completed]} | cut -d: -f1 | cut -d- -f2) を実行してください"
else
    echo "🎉 すべてのフェーズが完了しています！"
fi
```

## 実行例

```bash
=========================================
  Parasol V4 Lite プロジェクトステータス
=========================================

【フェーズ進行状況】

✅ Phase 1: プロジェクトコンテキスト - 完了
   成果物:
   - organization-analysis.md
   - market-assessment.md
   - constraints.md

✅ Phase 2: 価値定義 - 完了
   成果物:
   - value-declaration.md
   - value-decomposition.md
   - value-milestones.md

🔄 Phase 3: ビジネス設計 - 進行中

⏸️  Phase 4: アーキテクチャ設計 - 待機中
⏸️  Phase 5: ソフトウェア設計 - 未開始
⏸️  Phase 6: 実装 - 未開始
⏸️  Phase 7: プラットフォーム - 未開始

=========================================
【サマリー】
完了: 2 フェーズ
進行中: 1 フェーズ
未着手: 4 フェーズ
=========================================

【次のアクション】
👉 現在のフェーズを完了するか、次のフェーズに進んでください
```

## 決定記録の確認

```bash
# 決定記録がある場合は表示
echo ""
echo "【決定記録】"
for dr_type in VDR BDR AADR SADR PDR; do
    count=$(find $OUTPUT_DIR -name "${dr_type,,}-*.md" 2>/dev/null | wc -l)
    if [ $count -gt 0 ]; then
        echo "- $dr_type: $count 件"
    fi
done
```

## カスタムステータス確認

特定フェーズの詳細ステータス：

```bash
/parasol:status --phase=3-business
```

成果物の検証：

```bash
/parasol:status --validate
```

## トラブルシューティング

### 成果物が認識されない場合
- `outputs/`ディレクトリの権限を確認
- ファイル名が適切な形式か確認

### ステータスが正しく表示されない場合
- 各フェーズのディレクトリが存在するか確認
- 成果物ファイルが適切な場所にあるか確認

---

*プロジェクトの進行状況を定期的に確認して、計画的に開発を進めましょう。*