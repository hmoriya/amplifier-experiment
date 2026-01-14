# Parasol V5.5 → V5.6 移行ガイド

V5.5プロジェクトをV5.6に移行するための完全ガイド。

## 概要

### V5.6 の主な変更点

1. **Operational Stage (OS)** の導入
   - Value Stream内の運用段階を明示的に定義
   - Capabilityとの1:1対応を確立

2. **VC-Capability マッピング**の導入
   - Value Component (VC1-VC5) とCapabilityの対応を明示化
   - VL3のVCパターンとの整合性確保

3. **ステージ依存TVDC**
   - 同一Capabilityでもステージによって競争優位への貢献度が変化
   - デフォルトTVDCとステージ別オーバーライド

4. **OS-BC整合性検証**
   - OSとBounded Contextの責務整合を確保
   - aligned/partial/misalignedステータス

5. **ステージ依存アーキテクチャ判断**
   - TVDCに基づくBuild/Buy判断のステージ別設定

## 移行チェックリスト

### Phase 3 移行タスク

- [ ] **T-M1**: CL2にtvdc_default属性を追加
- [ ] **T-M2**: Value StreamごとにOS定義を作成
- [ ] **T-M3**: OS-Capabilityマッピングを作成
- [ ] **T-M4**: VC-Capabilityマッピングを作成
- [ ] **T-M5**: ステージ依存TVDCオーバーライドを設定

### Phase 4 移行タスク

- [ ] **T-M6**: OS-BCマッピングを作成
- [ ] **T-M7**: 整合性ステータスを設定
- [ ] **T-M8**: ステージ依存アーキテクチャ判断を設定

### 検証タスク

- [ ] **T-V1**: os-capability-mapping検証をパス
- [ ] **T-V2**: vc-capability-consistency検証をパス
- [ ] **T-V3**: stage-tvdc-consistency検証をパス
- [ ] **T-V4**: os-bc-alignment検証をパス
- [ ] **T-V5**: stage-architecture-consistency検証をパス
- [ ] **T-V6**: v56-integration統合テストをパス

## 詳細移行手順

### Step 1: CL2にtvdc_default追加 (T-M1)

**V5.5 形式:**
```yaml
# capability-level2.yaml
capabilities:
  - id: "CL2-001"
    name: "顧客セグメント分析"
    parent_cl1: "CL1-001"
    sub_capabilities: [...]
```

**V5.6 形式:**
```yaml
# capability-level2.yaml
capabilities:
  - id: "CL2-001"
    name: "顧客セグメント分析"
    parent_cl1: "CL1-001"
    tvdc_default: "Core"  # ← 追加
    tvdc_rationale: "競争優位の源泉となる分析能力"  # ← 追加
    sub_capabilities: [...]
```

### Step 2: Operational Stage定義作成 (T-M2)

**新規ファイル: vs{N}-operational-stages.yaml**
```yaml
value_stream:
  id: "VS1"
  name: "顧客価値創造"

operational_stages:
  - id: "OS-VS1-01"
    name: "市場理解"
    value_stage: "VS0_VS2"
    description: "市場ニーズと機会の把握"
    inputs:
      - "市場データ"
      - "競合情報"
    outputs:
      - "市場インサイト"
      - "機会マップ"

  - id: "OS-VS1-02"
    name: "顧客獲得"
    value_stage: "VS2_VS4"
    description: "見込み顧客の獲得と初期接点"
    inputs:
      - "市場インサイト"
    outputs:
      - "見込み顧客リスト"
```

### Step 3: OS-Capabilityマッピング作成 (T-M3)

**新規ファイル: os-capability-mapping.yaml**
```yaml
mappings:
  - os:
      id: "OS-VS1-01"
      name: "市場理解"
    capability:
      id: "CL2-001"
      name: "顧客セグメント分析"
    rationale: "市場理解にはセグメント分析能力が必要"
    mapping_type: "primary"

  - os:
      id: "OS-VS1-02"
      name: "顧客獲得"
    capability:
      id: "CL2-002"
      name: "リード管理"
    rationale: "顧客獲得にはリード管理能力が必要"
    mapping_type: "primary"
```

### Step 4: VC-Capabilityマッピング作成 (T-M4)

**新規ファイル: vc-capability-mapping.yaml**
```yaml
vc_capability_mapping:
  - capability:
      id: "CL2-001"
      name: "顧客セグメント分析"
    primary_vc:
      id: "VC5"
      name: "情報価値"
      contribution: "データ分析による洞察提供"
    secondary_vcs:
      - id: "VC4"
        name: "関係価値"
        contribution: "顧客理解を通じた関係構築支援"
    source_vl3:
      - id: "VL3-01"
        vc_pattern: "情報主導型"
```

### Step 5: ステージ依存TVDCオーバーライド設定 (T-M5)

**新規ファイル: stage-tvdc-overrides.yaml**
```yaml
stage_dependent_tvdc:
  - capability:
      id: "CL2-001"
      name: "顧客セグメント分析"
    tvdc_default: "Core"
    tvdc_rationale: "全体として競争優位の源泉"
    stage_overrides:
      VS4_VS7:
        enabled: true
        tvdc: "Supporting"
        rationale: "提供後は基本機能として定着"
```

### Step 6: OS-BCマッピング作成 (T-M6)

**新規ファイル: os-bc-mapping.yaml**
```yaml
os_bc_mapping:
  value_stream:
    id: "VS1"
    name: "顧客価値創造"

  mappings:
    - os:
        id: "OS-VS1-01"
        name: "市場理解"
        capability_id: "CL2-001"
      bc:
        id: "BC-Analytics"
        name: "分析コンテキスト"
        responsibility: "市場・顧客データの分析と洞察提供"
      alignment:
        status: "aligned"
        notes: ""
```

### Step 7: 整合性ステータス設定 (T-M7)

alignment.statusには以下の値を設定:

| ステータス | 意味 | 対応 |
|-----------|------|------|
| `aligned` | 完全に整合 | なし |
| `partial` | 部分的に整合 | notesに理由を記載 |
| `misaligned` | 不整合 | remediation_actionを記載 |

```yaml
alignment:
  status: "misaligned"
  notes: "BC境界がOS責務と一致していない"
  remediation_action: "BC分割を検討"
```

### Step 8: ステージ依存アーキテクチャ判断 (T-M8)

**新規ファイル: stage-architecture-decisions.yaml**
```yaml
stage_architecture_decisions:
  - bc:
      id: "BC-Analytics"
      name: "分析コンテキスト"
    stage_tvdc:
      default: "Core"
      overrides:
        VS4_VS7: "Supporting"
    architecture_decisions:
      VS0_VS4:
        stage: "開発〜提供"
        tvdc: "Core"
        recommendations:
          build_buy: "Build"
          rationale: "競争優位の源泉のため内製"
          integration_pattern: "Direct API"
          non_functional:
            availability: "99.99%"
            latency: "<500ms"
      VS4_VS7:
        stage: "維持〜拡張"
        tvdc: "Supporting"
        recommendations:
          build_buy: "Buy + Customize"
          rationale: "成熟期には標準ソリューション活用"
          integration_pattern: "SDK Integration"
          non_functional:
            availability: "99.9%"
            latency: "<1s"
```

## 検証コマンド

移行完了後、以下のコマンドで検証:

```bash
# 個別検証
/parasol:validate os-capability-mapping
/parasol:validate vc-capability-consistency
/parasol:validate stage-tvdc-consistency
/parasol:validate os-bc-alignment
/parasol:validate stage-architecture-consistency

# 統合テスト
/parasol:validate v56-integration
```

## よくある移行エラー

### エラー1: OS-Capability 1:1違反

```
OSCAP-001: OS-Capability 1:1 Mapping - FAILED
  OS "OS-VS1-01" has 2 capabilities mapped
```

**原因**: 1つのOSに複数のCapabilityを対応させている

**対応**:
- OSを分割するか
- Capabilityを統合するか
- 主対応(primary)と補助対応(supporting)を区別

### エラー2: VC ID無効

```
VCCAP-002: Primary VC Valid - FAILED
  primary_vc.id "VC6" is not valid
```

**原因**: VC1-VC5以外のID

**対応**: 有効なVC ID (VC1〜VC5) に修正

### エラー3: Value Stage形式エラー

```
STVDC-004: Value Stage Format Valid - FAILED
  Stage key "VS1-VS3" is invalid format
```

**原因**: アンダースコアではなくハイフンを使用

**対応**: `VS1_VS3` 形式に修正

### エラー4: misalignedに対応アクションなし

```
OSBC-004: Misaligned Requires Action - FAILED
  Mapping has status "misaligned" but no remediation_action
```

**原因**: misaligned状態なのに対応策がない

**対応**: `remediation_action` を追加

## 移行サポート

移行中に問題が発生した場合:

1. バリデータのエラーメッセージを確認
2. 該当ルールの`fix`ガイダンスを参照
3. 本ガイドのエラー対応セクションを確認

## バージョン互換性

- V5.6はV5.5の既存ファイルをそのまま読み込み可能
- 新規ファイル追加による拡張方式
- 既存のPhase 1-3成果物は変更不要（tvdc_default追加を除く）
