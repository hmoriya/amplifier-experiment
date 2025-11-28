# BC3: Brand Portfolio - API仕様

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS3 ブランド・マーケティング |
| BC | Brand Portfolio |
| 技術スタック | TypeScript / NestJS |
| API形式 | REST + GraphQL |
| 認証 | OAuth 2.0 / JWT |

---

## OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: Brand Portfolio API
  version: 1.0.0
  description: |
    アサヒグループブランドポートフォリオ管理API
    グローバル・ローカルブランド管理、キャンペーン企画管理

servers:
  - url: https://api.asahi-brand.internal/portfolio/v1
    description: Production (内部)
  - url: https://api-staging.asahi-brand.internal/portfolio/v1
    description: Staging

tags:
  - name: Brands
    description: ブランド管理
  - name: Guidelines
    description: ブランドガイドライン
  - name: Assets
    description: ブランドアセット
  - name: Campaigns
    description: キャンペーン管理
  - name: Markets
    description: 市場プレゼンス

paths:
  # ============================================
  # Brands
  # ============================================
  /brands:
    get:
      summary: ブランド一覧取得
      operationId: listBrands
      tags: [Brands]
      parameters:
        - name: type
          in: query
          schema:
            $ref: '#/components/schemas/BrandType'
        - name: scope
          in: query
          schema:
            $ref: '#/components/schemas/BrandScope'
        - name: status
          in: query
          schema:
            $ref: '#/components/schemas/BrandStatus'
        - name: market
          in: query
          schema:
            type: string
          description: 市場コード (ISO 3166-1 alpha-2)
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: pageSize
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandList'

    post:
      summary: ブランド作成
      operationId: createBrand
      tags: [Brands]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateBrandRequest'
      responses:
        '201':
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Brand'
        '400':
          $ref: '#/components/responses/BadRequest'

  /brands/{brandId}:
    get:
      summary: ブランド詳細取得
      operationId: getBrand
      tags: [Brands]
      parameters:
        - $ref: '#/components/parameters/brandId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandDetail'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: ブランド更新
      operationId: updateBrand
      tags: [Brands]
      parameters:
        - $ref: '#/components/parameters/brandId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateBrandRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Brand'

  /brands/{brandId}/identity:
    get:
      summary: ブランドアイデンティティ取得
      operationId: getBrandIdentity
      tags: [Brands]
      parameters:
        - $ref: '#/components/parameters/brandId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandIdentity'

    put:
      summary: ブランドアイデンティティ更新
      operationId: updateBrandIdentity
      tags: [Brands]
      parameters:
        - $ref: '#/components/parameters/brandId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BrandIdentity'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandIdentity'

  /brands/{brandId}/hierarchy:
    get:
      summary: ブランド階層取得
      operationId: getBrandHierarchy
      tags: [Brands]
      parameters:
        - $ref: '#/components/parameters/brandId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandHierarchy'

  /brands/portfolio:
    get:
      summary: ブランドポートフォリオ概要
      operationId: getPortfolioOverview
      tags: [Brands]
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PortfolioOverview'

  # ============================================
  # Guidelines
  # ============================================
  /brands/{brandId}/guidelines:
    get:
      summary: ブランドガイドライン取得
      operationId: getBrandGuidelines
      tags: [Guidelines]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - name: market
          in: query
          schema:
            type: string
          description: 市場固有ガイドライン取得時
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandGuidelines'

    put:
      summary: ブランドガイドライン更新
      operationId: updateBrandGuidelines
      tags: [Guidelines]
      parameters:
        - $ref: '#/components/parameters/brandId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateGuidelinesRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandGuidelines'

  /brands/{brandId}/guidelines/visual:
    get:
      summary: ビジュアルアイデンティティガイドライン取得
      operationId: getVisualGuidelines
      tags: [Guidelines]
      parameters:
        - $ref: '#/components/parameters/brandId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/VisualIdentityGuideline'

  /brands/{brandId}/guidelines/voice:
    get:
      summary: ボイス&トーンガイドライン取得
      operationId: getVoiceGuidelines
      tags: [Guidelines]
      parameters:
        - $ref: '#/components/parameters/brandId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/VoiceToneGuideline'

  /brands/{brandId}/guidelines/export:
    get:
      summary: スタイルガイドエクスポート
      operationId: exportStyleGuide
      tags: [Guidelines]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - name: format
          in: query
          schema:
            type: string
            enum: [pdf, html, figma]
            default: pdf
      responses:
        '200':
          description: 成功
          content:
            application/pdf:
              schema:
                type: string
                format: binary
            text/html:
              schema:
                type: string

  # ============================================
  # Assets
  # ============================================
  /brands/{brandId}/assets:
    get:
      summary: ブランドアセット一覧取得
      operationId: listBrandAssets
      tags: [Assets]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - name: type
          in: query
          schema:
            $ref: '#/components/schemas/AssetType'
        - name: usage
          in: query
          schema:
            $ref: '#/components/schemas/AssetUsage'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AssetList'

    post:
      summary: ブランドアセット追加
      operationId: addBrandAsset
      tags: [Assets]
      parameters:
        - $ref: '#/components/parameters/brandId'
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AddAssetRequest'
      responses:
        '201':
          description: 追加成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandAsset'

  /brands/{brandId}/assets/{assetId}:
    get:
      summary: ブランドアセット詳細取得
      operationId: getBrandAsset
      tags: [Assets]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - $ref: '#/components/parameters/assetId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BrandAsset'

    delete:
      summary: ブランドアセット削除
      operationId: deleteBrandAsset
      tags: [Assets]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - $ref: '#/components/parameters/assetId'
      responses:
        '204':
          description: 削除成功

  /brands/{brandId}/assets/{assetId}/download:
    get:
      summary: アセットダウンロード
      operationId: downloadAsset
      tags: [Assets]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - $ref: '#/components/parameters/assetId'
        - name: resolution
          in: query
          schema:
            type: string
            enum: [original, high, medium, low, thumbnail]
            default: original
      responses:
        '200':
          description: 成功
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary

  # ============================================
  # Campaigns
  # ============================================
  /campaigns:
    get:
      summary: キャンペーン一覧取得
      operationId: listCampaigns
      tags: [Campaigns]
      parameters:
        - name: brandId
          in: query
          schema:
            type: string
            format: uuid
        - name: status
          in: query
          schema:
            $ref: '#/components/schemas/CampaignStatus'
        - name: fromDate
          in: query
          schema:
            type: string
            format: date
        - name: toDate
          in: query
          schema:
            type: string
            format: date
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: pageSize
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CampaignList'

    post:
      summary: キャンペーン作成
      operationId: createCampaign
      tags: [Campaigns]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateCampaignRequest'
      responses:
        '201':
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Campaign'

  /campaigns/{campaignId}:
    get:
      summary: キャンペーン詳細取得
      operationId: getCampaign
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CampaignDetail'

    put:
      summary: キャンペーン更新
      operationId: updateCampaign
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateCampaignRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Campaign'

  /campaigns/{campaignId}/brief:
    get:
      summary: キャンペーンブリーフ取得
      operationId: getCampaignBrief
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CampaignBrief'

    put:
      summary: キャンペーンブリーフ更新
      operationId: updateCampaignBrief
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CampaignBrief'
      responses:
        '200':
          description: 更新成功

  /campaigns/{campaignId}/approve:
    post:
      summary: キャンペーン承認
      operationId: approveCampaign
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                comments:
                  type: string
      responses:
        '200':
          description: 承認成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Campaign'

  /campaigns/{campaignId}/launch:
    post:
      summary: キャンペーン開始
      operationId: launchCampaign
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      responses:
        '200':
          description: 開始成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Campaign'

  /campaigns/{campaignId}/complete:
    post:
      summary: キャンペーン完了
      operationId: completeCampaign
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CampaignResultsRequest'
      responses:
        '200':
          description: 完了成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CampaignDetail'

  /campaigns/{campaignId}/creatives:
    get:
      summary: クリエイティブ一覧取得
      operationId: listCreatives
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreativeList'

    post:
      summary: クリエイティブ追加
      operationId: addCreative
      tags: [Campaigns]
      parameters:
        - $ref: '#/components/parameters/campaignId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AddCreativeRequest'
      responses:
        '201':
          description: 追加成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Creative'

  # ============================================
  # Markets
  # ============================================
  /brands/{brandId}/markets:
    get:
      summary: ブランド展開市場一覧
      operationId: listBrandMarkets
      tags: [Markets]
      parameters:
        - $ref: '#/components/parameters/brandId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketPresenceList'

    post:
      summary: 市場展開
      operationId: expandToMarket
      tags: [Markets]
      parameters:
        - $ref: '#/components/parameters/brandId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExpandToMarketRequest'
      responses:
        '201':
          description: 展開成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketPresence'

  /brands/{brandId}/markets/{marketId}:
    get:
      summary: 市場プレゼンス詳細
      operationId: getMarketPresence
      tags: [Markets]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - $ref: '#/components/parameters/marketId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketPresenceDetail'

    put:
      summary: 市場プレゼンス更新
      operationId: updateMarketPresence
      tags: [Markets]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - $ref: '#/components/parameters/marketId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateMarketPresenceRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketPresence'

  /brands/{brandId}/markets/{marketId}/performance:
    get:
      summary: 市場パフォーマンス取得
      operationId: getMarketPerformance
      tags: [Markets]
      parameters:
        - $ref: '#/components/parameters/brandId'
        - $ref: '#/components/parameters/marketId'
        - name: period
          in: query
          schema:
            type: string
            enum: [monthly, quarterly, yearly]
            default: quarterly
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketPerformance'

components:
  parameters:
    brandId:
      name: brandId
      in: path
      required: true
      schema:
        type: string
        format: uuid

    assetId:
      name: assetId
      in: path
      required: true
      schema:
        type: string
        format: uuid

    campaignId:
      name: campaignId
      in: path
      required: true
      schema:
        type: string
        format: uuid

    marketId:
      name: marketId
      in: path
      required: true
      schema:
        type: string
        pattern: '^[A-Z]{2}$'

  responses:
    BadRequest:
      description: バリデーションエラー
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: リソースが見つからない
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  schemas:
    # ============================================
    # Enums
    # ============================================
    BrandType:
      type: string
      enum: [corporate, master, sub, product, endorsed]

    BrandScope:
      type: string
      enum: [global, regional, local]

    BrandStatus:
      type: string
      enum: [draft, active, sunset, archived]

    AssetType:
      type: string
      enum: [logo, image, video, document, template]

    AssetUsage:
      type: string
      enum: [primary, secondary, digital, print, social]

    CampaignStatus:
      type: string
      enum: [draft, planning, approved, in_execution, completed, cancelled]

    MarketingChannel:
      type: string
      enum: [tv, radio, print, ooh, digital, social, influencer, event, sponsorship, retail]

    # ============================================
    # Brand Schemas
    # ============================================
    Brand:
      type: object
      properties:
        brandId:
          type: string
          format: uuid
        brandCode:
          type: string
        name:
          type: string
        brandType:
          $ref: '#/components/schemas/BrandType'
        scope:
          $ref: '#/components/schemas/BrandScope'
        parentBrandId:
          type: string
          format: uuid
        status:
          $ref: '#/components/schemas/BrandStatus'
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    BrandDetail:
      allOf:
        - $ref: '#/components/schemas/Brand'
        - type: object
          properties:
            identity:
              $ref: '#/components/schemas/BrandIdentity'
            markets:
              type: array
              items:
                type: string
            assetCount:
              type: integer
            activeCampaignCount:
              type: integer

    BrandList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Brand'
        totalCount:
          type: integer
        page:
          type: integer
        pageSize:
          type: integer

    BrandIdentity:
      type: object
      properties:
        mission:
          type: string
        vision:
          type: string
        values:
          type: array
          items:
            type: string
        personality:
          $ref: '#/components/schemas/BrandPersonality'
        positioning:
          type: string
        tagline:
          type: string
        storyNarrative:
          type: string

    BrandPersonality:
      type: object
      properties:
        traits:
          type: array
          items:
            type: string
        archetypes:
          type: array
          items:
            type: string
        toneOfVoice:
          type: string

    BrandHierarchy:
      type: object
      properties:
        brand:
          $ref: '#/components/schemas/Brand'
        parent:
          $ref: '#/components/schemas/Brand'
        siblings:
          type: array
          items:
            $ref: '#/components/schemas/Brand'
        children:
          type: array
          items:
            $ref: '#/components/schemas/Brand'

    PortfolioOverview:
      type: object
      properties:
        totalBrands:
          type: integer
        globalBrands:
          type: array
          items:
            $ref: '#/components/schemas/Brand'
        regionalBrands:
          type: array
          items:
            $ref: '#/components/schemas/Brand'
        localBrands:
          type: array
          items:
            $ref: '#/components/schemas/Brand'
        metrics:
          type: object
          properties:
            totalMarkets:
              type: integer
            activeCampaigns:
              type: integer
            totalAssets:
              type: integer

    CreateBrandRequest:
      type: object
      required: [name, brandType, scope]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        brandType:
          $ref: '#/components/schemas/BrandType'
        scope:
          $ref: '#/components/schemas/BrandScope'
        parentBrandId:
          type: string
          format: uuid
        identity:
          $ref: '#/components/schemas/BrandIdentity'

    UpdateBrandRequest:
      type: object
      properties:
        name:
          type: string
        status:
          $ref: '#/components/schemas/BrandStatus'

    # ============================================
    # Guidelines Schemas
    # ============================================
    BrandGuidelines:
      type: object
      properties:
        brandId:
          type: string
          format: uuid
        visualIdentity:
          $ref: '#/components/schemas/VisualIdentityGuideline'
        voiceTone:
          $ref: '#/components/schemas/VoiceToneGuideline'
        messaging:
          $ref: '#/components/schemas/MessagingGuideline'
        usageRules:
          type: array
          items:
            $ref: '#/components/schemas/UsageRule'
        updatedAt:
          type: string
          format: date-time

    VisualIdentityGuideline:
      type: object
      properties:
        primaryColors:
          type: array
          items:
            $ref: '#/components/schemas/ColorSpec'
        secondaryColors:
          type: array
          items:
            $ref: '#/components/schemas/ColorSpec'
        typography:
          $ref: '#/components/schemas/TypographySpec'
        logoUsage:
          $ref: '#/components/schemas/LogoUsageSpec'
        spacing:
          type: object

    ColorSpec:
      type: object
      properties:
        name:
          type: string
        hex:
          type: string
          pattern: '^#[0-9A-Fa-f]{6}$'
        rgb:
          type: object
          properties:
            r:
              type: integer
            g:
              type: integer
            b:
              type: integer
        pantone:
          type: string

    TypographySpec:
      type: object
      properties:
        primaryFont:
          type: string
        secondaryFont:
          type: string
        headingStyles:
          type: object
        bodyStyles:
          type: object

    LogoUsageSpec:
      type: object
      properties:
        clearSpace:
          type: string
        minimumSize:
          type: string
        colorVariations:
          type: array
          items:
            type: string
        prohibitedUsages:
          type: array
          items:
            type: string

    VoiceToneGuideline:
      type: object
      properties:
        voiceAttributes:
          type: array
          items:
            type: string
        doList:
          type: array
          items:
            type: string
        dontList:
          type: array
          items:
            type: string
        examples:
          type: array
          items:
            type: object
            properties:
              context:
                type: string
              good:
                type: string
              bad:
                type: string

    MessagingGuideline:
      type: object
      properties:
        keyMessages:
          type: array
          items:
            type: string
        proofPoints:
          type: array
          items:
            type: string
        callToActions:
          type: array
          items:
            type: string

    UsageRule:
      type: object
      properties:
        category:
          type: string
        rule:
          type: string
        examples:
          type: array
          items:
            type: string

    UpdateGuidelinesRequest:
      type: object
      properties:
        visualIdentity:
          $ref: '#/components/schemas/VisualIdentityGuideline'
        voiceTone:
          $ref: '#/components/schemas/VoiceToneGuideline'
        messaging:
          $ref: '#/components/schemas/MessagingGuideline'

    # ============================================
    # Asset Schemas
    # ============================================
    BrandAsset:
      type: object
      properties:
        assetId:
          type: string
          format: uuid
        assetType:
          $ref: '#/components/schemas/AssetType'
        name:
          type: string
        url:
          type: string
          format: uri
        format:
          type: string
        resolution:
          type: string
        usage:
          $ref: '#/components/schemas/AssetUsage'
        fileSize:
          type: integer
        createdAt:
          type: string
          format: date-time
        expiresAt:
          type: string
          format: date-time

    AssetList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/BrandAsset'
        totalCount:
          type: integer

    AddAssetRequest:
      type: object
      required: [assetType, name, file]
      properties:
        assetType:
          $ref: '#/components/schemas/AssetType'
        name:
          type: string
        usage:
          $ref: '#/components/schemas/AssetUsage'
        file:
          type: string
          format: binary

    # ============================================
    # Campaign Schemas
    # ============================================
    Campaign:
      type: object
      properties:
        campaignId:
          type: string
          format: uuid
        campaignCode:
          type: string
        name:
          type: string
        brandId:
          type: string
          format: uuid
        brandName:
          type: string
        status:
          $ref: '#/components/schemas/CampaignStatus'
        launchDate:
          type: string
          format: date
        endDate:
          type: string
          format: date
        createdAt:
          type: string
          format: date-time

    CampaignDetail:
      allOf:
        - $ref: '#/components/schemas/Campaign'
        - type: object
          properties:
            objective:
              $ref: '#/components/schemas/CampaignObjective'
            targetAudience:
              $ref: '#/components/schemas/TargetAudience'
            brief:
              $ref: '#/components/schemas/CampaignBrief'
            budget:
              $ref: '#/components/schemas/Budget'
            timeline:
              $ref: '#/components/schemas/CampaignTimeline'
            channels:
              type: array
              items:
                $ref: '#/components/schemas/MarketingChannel'
            kpis:
              type: array
              items:
                $ref: '#/components/schemas/CampaignKPI'
            results:
              $ref: '#/components/schemas/CampaignResults'

    CampaignList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Campaign'
        totalCount:
          type: integer
        page:
          type: integer
        pageSize:
          type: integer

    CampaignObjective:
      type: object
      properties:
        type:
          type: string
          enum: [awareness, consideration, conversion, loyalty, advocacy]
        description:
          type: string
        targets:
          type: array
          items:
            type: object
            properties:
              metric:
                type: string
              targetValue:
                type: number

    TargetAudience:
      type: object
      properties:
        demographics:
          type: object
          properties:
            ageRange:
              type: object
              properties:
                min:
                  type: integer
                max:
                  type: integer
            gender:
              type: array
              items:
                type: string
            location:
              type: array
              items:
                type: string
        psychographics:
          type: object
          properties:
            lifestyles:
              type: array
              items:
                type: string
            interests:
              type: array
              items:
                type: string

    CampaignBrief:
      type: object
      properties:
        background:
          type: string
        challenge:
          type: string
        opportunity:
          type: string
        keyMessage:
          type: string
        creativeDirection:
          type: string
        mandatories:
          type: array
          items:
            type: string
        restrictions:
          type: array
          items:
            type: string

    Budget:
      type: object
      properties:
        totalAmount:
          type: number
        currency:
          type: string
        allocation:
          type: object
          additionalProperties:
            type: number
        contingency:
          type: number

    CampaignTimeline:
      type: object
      properties:
        planningStart:
          type: string
          format: date
        creativeDeadline:
          type: string
          format: date
        launchDate:
          type: string
          format: date
        endDate:
          type: string
          format: date
        milestones:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              date:
                type: string
                format: date

    CampaignKPI:
      type: object
      properties:
        metric:
          type: string
        target:
          type: number
        unit:
          type: string

    CampaignResults:
      type: object
      properties:
        kpiResults:
          type: array
          items:
            type: object
            properties:
              metric:
                type: string
              target:
                type: number
              actual:
                type: number
              achievement:
                type: number
        roi:
          type: number
        learnings:
          type: array
          items:
            type: string

    CreateCampaignRequest:
      type: object
      required: [name, brandId, objective]
      properties:
        name:
          type: string
        brandId:
          type: string
          format: uuid
        objective:
          $ref: '#/components/schemas/CampaignObjective'
        targetAudience:
          $ref: '#/components/schemas/TargetAudience'

    UpdateCampaignRequest:
      type: object
      properties:
        name:
          type: string
        objective:
          $ref: '#/components/schemas/CampaignObjective'
        budget:
          $ref: '#/components/schemas/Budget'
        timeline:
          $ref: '#/components/schemas/CampaignTimeline'

    CampaignResultsRequest:
      type: object
      properties:
        kpiResults:
          type: array
          items:
            type: object
            properties:
              metric:
                type: string
              actual:
                type: number
        learnings:
          type: array
          items:
            type: string

    Creative:
      type: object
      properties:
        creativeId:
          type: string
          format: uuid
        name:
          type: string
        format:
          type: string
        channel:
          $ref: '#/components/schemas/MarketingChannel'
        status:
          type: string
          enum: [draft, in_review, approved, rejected]
        createdAt:
          type: string
          format: date-time

    CreativeList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Creative'
        totalCount:
          type: integer

    AddCreativeRequest:
      type: object
      required: [name, format, channel]
      properties:
        name:
          type: string
        format:
          type: string
        channel:
          $ref: '#/components/schemas/MarketingChannel'
        assetIds:
          type: array
          items:
            type: string
            format: uuid

    # ============================================
    # Market Schemas
    # ============================================
    MarketPresence:
      type: object
      properties:
        presenceId:
          type: string
          format: uuid
        brandId:
          type: string
          format: uuid
        marketId:
          type: string
        localBrandName:
          type: string
        localTagline:
          type: string
        status:
          type: string
          enum: [active, suspended, terminated]
        launchedAt:
          type: string
          format: date

    MarketPresenceDetail:
      allOf:
        - $ref: '#/components/schemas/MarketPresence'
        - type: object
          properties:
            localization:
              $ref: '#/components/schemas/MarketLocalization'
            performance:
              $ref: '#/components/schemas/MarketPerformance'
            competitors:
              type: array
              items:
                $ref: '#/components/schemas/CompetitorInfo'

    MarketPresenceList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/MarketPresence'
        totalCount:
          type: integer

    MarketLocalization:
      type: object
      properties:
        language:
          type: string
        culturalAdaptations:
          type: array
          items:
            type: string
        regulatoryCompliance:
          type: array
          items:
            type: string

    MarketPerformance:
      type: object
      properties:
        period:
          type: string
        marketShare:
          type: number
        salesVolume:
          type: number
        brandAwareness:
          type: number
        brandPreference:
          type: number
        nps:
          type: number

    CompetitorInfo:
      type: object
      properties:
        competitorName:
          type: string
        marketShare:
          type: number
        positioning:
          type: string

    ExpandToMarketRequest:
      type: object
      required: [marketId]
      properties:
        marketId:
          type: string
        localBrandName:
          type: string
        localTagline:
          type: string
        localization:
          $ref: '#/components/schemas/MarketLocalization'

    UpdateMarketPresenceRequest:
      type: object
      properties:
        localBrandName:
          type: string
        localTagline:
          type: string
        localization:
          $ref: '#/components/schemas/MarketLocalization'

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## イベント連携

### 受信イベント（← VS2 製品開発）

| イベント | トピック | 処理 |
|---------|---------|------|
| RecipeApproved | vs2.recipe.events | 製品情報の取り込み |
| ProductApproved | vs2.recipe.events | ブランドと製品の紐付け |

---

**作成日**: 2025-11-28
**VS**: VS3 ブランド・マーケティング
**BC**: BC3 Brand Portfolio
**次成果物**: database-design.md
