# Parasol V5 ビジュアルスタイルガイド

**トンマナ（トーン＆マナー）定義 - 画像生成用参照プロンプト**

---

## 概要

Parasol V5のドキュメント・プレゼンテーション用ビジュアルの統一スタイルを定義します。
画像生成AI（Nano Banana Pro等）で一貫したデザインを維持するための参照プロンプトです。

---

## カラーパレット

| 用途 | 色名 | HEX | 説明 |
|------|------|-----|------|
| **背景** | Warm Beige | `#F5F0E6` | 温かみのあるクリーム系 |
| **主アクセント** | Coral Orange | `#E8927C` | コーラル/サーモンオレンジ |
| **副アクセント** | Teal Cyan | `#5DBFB8` | ティール/シアン |
| **第三色** | Steel Blue | `#7A9CB8` | 落ち着いたスチールブルー |
| **ニュートラル** | Warm Gray | `#A69F95` | 温かみのあるグレー |
| **ブロック（黄）** | Soft Yellow | `#F0D58C` | 柔らかい黄色 |
| **ブロック（赤）** | Light Coral | `#F0A08C` | 薄いコーラル |
| **ブロック（青）** | Soft Teal | `#8CD0C8` | 柔らかいティール |

---

## ビジュアルスタイル

### 基本スタイル
- **イラストタイプ**: アイソメトリック（等角投影）3D
- **レンダリング**: クリーンなベクター風イラスト
- **質感**: マット仕上げ（光沢なし）
- **影**: ソフトシャドウ、アンビエントオクルージョンのみ
- **角度**: 一貫した30度アイソメトリック

### 要素スタイル
- **3Dブロック/キューブ**: ソフトグラデーション、柔らかい影
- **人物アイコン**: フラットなシルエット（簡略化）
- **フローチャート**: 点線/実線の接続線
- **ラベル**: 角丸長方形、日本語テキスト
- **サービスノード**: アイコン付き小さな色付き四角
- **背景**: 薄いグリッド/設計図風の線

### 印象・ムード
- プロフェッショナル
- 温かみがある
- 親しみやすい
- 洗練されている
- 日本企業向けコンサルティング品質

---

## 画像生成プロンプト

### フルプロンプト（詳細版）

```
Style reference for consistent visual identity:

【Base Style】
Isometric business infographic illustration, Japanese enterprise consulting aesthetic

【Color Palette】
- Background: warm beige/cream (#F5F0E6)
- Primary accent: coral/salmon orange (#E8927C)
- Secondary accent: teal/cyan (#5DBFB8)
- Tertiary: muted steel blue (#7A9CB8)
- Neutral: warm gray (#A69F95)
- Blocks/cubes: soft yellow (#F0D58C), light coral, soft teal

【Visual Elements】
- Isometric 3D blocks and cubes with soft shadows
- Flat human figure icons (simplified silhouettes)
- Geometric flowchart connections with dotted/solid lines
- Rounded rectangle labels with Japanese text
- Service nodes as small colored squares with icons
- Subtle grid/blueprint lines in background

【Rendering Style】
- Clean vector-like illustration
- Soft gradients on 3D surfaces
- No harsh shadows, ambient occlusion only
- Matte finish, not glossy
- Consistent 30-degree isometric angle

【Mood】
Professional, warm, approachable, sophisticated
Japanese corporate presentation quality
```

### 短縮プロンプト（毎回使用）

```
Isometric Japanese business infographic, warm beige background,
coral-orange and teal accents, soft 3D blocks with matte finish,
clean consulting-style illustration, professional enterprise aesthetic
```

### ネガティブプロンプト（除外要素）

```
photorealistic, dark background, neon colors, cartoon style,
hand-drawn sketch, watercolor, vintage, grunge, glossy,
harsh shadows, low quality
```

---

## 使用例

### Phase図を作成する場合

```
[短縮プロンプト] +

Phase diagram showing value definition flow,
pyramid structure for VL1-VL2-VL3 hierarchy,
human figures representing customer journey stages VS0-VS7,
arrows connecting phases from left to right
```

### アーキテクチャ図を作成する場合

```
[短縮プロンプト] +

Service architecture diagram with bounded contexts,
isometric cube clusters representing microservices,
context map showing integration patterns,
Order Service, Inventory Service, Payment Service nodes
```

### ケイパビリティ分類図を作成する場合

```
[短縮プロンプト] +

Capability classification matrix,
2x2 grid showing Core/VCI/Supporting/Generic quadrants,
colored blocks representing different capability types,
TVDC framework visualization
```

---

## 参照画像

元となるトンマナ参照画像:
- 「価値を実現する設計図：Parasol V5 フレームワーク」インフォグラフィック

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2025-01-07 | 初版作成 |

---

**Parasol V5 - 一貫したビジュアルアイデンティティで価値を伝える**
