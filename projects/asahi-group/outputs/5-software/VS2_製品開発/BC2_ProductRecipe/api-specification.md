# BC2: Product Recipe - API仕様

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS2 製品開発 |
| BC | Product Recipe |
| 技術スタック | Java / Spring Boot |
| API形式 | REST (CQRS: 読み書き分離) |
| 認証 | OAuth 2.0 / JWT |

---

## CQRS構成

```
┌─────────────────────────────────────────────────────────────┐
│                    Product Recipe API                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────┐    ┌────────────────────┐          │
│  │   Command Side     │    │    Query Side      │          │
│  │  (Write Model)     │    │   (Read Model)     │          │
│  │                    │    │                    │          │
│  │ POST /recipes      │    │ GET /recipes       │          │
│  │ PUT /recipes/{id}  │    │ GET /recipes/{id}  │          │
│  │ POST /evaluations  │    │ GET /search        │          │
│  └─────────┬──────────┘    └─────────┬──────────┘          │
│            ▼                         ▼                      │
│  ┌────────────────────┐    ┌────────────────────┐          │
│  │   PostgreSQL       │    │   Elasticsearch    │          │
│  │  (Master Data)     │    │ (Search/Analytics) │          │
│  └────────────────────┘    └────────────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: Product Recipe API
  version: 1.0.0
  description: |
    アサヒグループ製品処方管理API
    処方設計、品質基準管理、官能評価管理

servers:
  - url: https://api.asahi-pd.internal/recipe/v1
    description: Production (内部)
  - url: https://api-staging.asahi-pd.internal/recipe/v1
    description: Staging

tags:
  - name: Recipes
    description: 処方管理
  - name: QualityStandards
    description: 品質基準管理
  - name: SensoryEvaluations
    description: 官能評価管理
  - name: Search
    description: 検索（Read Model）

paths:
  # ============================================
  # Recipes - Command Side
  # ============================================
  /recipes:
    post:
      summary: 処方作成
      operationId: createRecipe
      tags: [Recipes]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateRecipeRequest'
      responses:
        '201':
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'
        '400':
          $ref: '#/components/responses/BadRequest'

    get:
      summary: 処方一覧取得
      operationId: listRecipes
      tags: [Recipes]
      parameters:
        - name: productType
          in: query
          schema:
            $ref: '#/components/schemas/ProductType'
        - name: status
          in: query
          schema:
            $ref: '#/components/schemas/RecipeStatus'
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
                $ref: '#/components/schemas/RecipeList'

  /recipes/{recipeId}:
    get:
      summary: 処方詳細取得
      operationId: getRecipe
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RecipeDetail'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: 処方更新
      operationId: updateRecipe
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateRecipeRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'

  /recipes/{recipeId}/ingredients:
    put:
      summary: 原料構成更新
      operationId: updateIngredients
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateIngredientsRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'

  /recipes/{recipeId}/process-spec:
    put:
      summary: 製造仕様更新
      operationId: updateProcessSpec
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProcessSpecification'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'

  /recipes/{recipeId}/submit:
    post:
      summary: 承認申請
      operationId: submitRecipe
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
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
          description: 申請成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'

  /recipes/{recipeId}/approve:
    post:
      summary: 処方承認
      operationId: approveRecipe
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
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
                $ref: '#/components/schemas/Recipe'

  /recipes/{recipeId}/reject:
    post:
      summary: 処方却下
      operationId: rejectRecipe
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [reason]
              properties:
                reason:
                  type: string
      responses:
        '200':
          description: 却下成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'

  /recipes/{recipeId}/versions:
    get:
      summary: バージョン履歴取得
      operationId: getVersionHistory
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/VersionHistory'

    post:
      summary: 新バージョン作成
      operationId: createNewVersion
      tags: [Recipes]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                changeDescription:
                  type: string
      responses:
        '201':
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'

  # ============================================
  # Quality Standards
  # ============================================
  /recipes/{recipeId}/quality-standards:
    get:
      summary: 品質基準取得
      operationId: getQualityStandard
      tags: [QualityStandards]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/QualityStandard'

    post:
      summary: 品質基準定義
      operationId: defineQualityStandard
      tags: [QualityStandards]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DefineQualityStandardRequest'
      responses:
        '201':
          description: 定義成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/QualityStandard'

    put:
      summary: 品質基準更新
      operationId: updateQualityStandard
      tags: [QualityStandards]
      parameters:
        - $ref: '#/components/parameters/recipeId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateQualityStandardRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/QualityStandard'

  /quality-assessments:
    post:
      summary: 品質評価実行
      operationId: assessQuality
      tags: [QualityStandards]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/QualityAssessmentRequest'
      responses:
        '200':
          description: 評価完了
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/QualityAssessmentResult'

  # ============================================
  # Sensory Evaluations
  # ============================================
  /sensory-evaluations:
    get:
      summary: 官能評価一覧取得
      operationId: listSensoryEvaluations
      tags: [SensoryEvaluations]
      parameters:
        - name: recipeId
          in: query
          schema:
            type: string
            format: uuid
        - name: status
          in: query
          schema:
            $ref: '#/components/schemas/EvaluationStatus'
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
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SensoryEvaluationList'

    post:
      summary: 官能評価スケジュール
      operationId: scheduleSensoryEvaluation
      tags: [SensoryEvaluations]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ScheduleEvaluationRequest'
      responses:
        '201':
          description: スケジュール成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SensoryEvaluation'

  /sensory-evaluations/{evaluationId}:
    get:
      summary: 官能評価詳細取得
      operationId: getSensoryEvaluation
      tags: [SensoryEvaluations]
      parameters:
        - $ref: '#/components/parameters/evaluationId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SensoryEvaluationDetail'

  /sensory-evaluations/{evaluationId}/panelists:
    post:
      summary: パネリスト追加
      operationId: addPanelist
      tags: [SensoryEvaluations]
      parameters:
        - $ref: '#/components/parameters/evaluationId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AddPanelistRequest'
      responses:
        '200':
          description: 追加成功

  /sensory-evaluations/{evaluationId}/scores:
    post:
      summary: スコア記録
      operationId: recordScore
      tags: [SensoryEvaluations]
      parameters:
        - $ref: '#/components/parameters/evaluationId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RecordScoreRequest'
      responses:
        '200':
          description: 記録成功

  /sensory-evaluations/{evaluationId}/complete:
    post:
      summary: 評価完了
      operationId: completeEvaluation
      tags: [SensoryEvaluations]
      parameters:
        - $ref: '#/components/parameters/evaluationId'
      responses:
        '200':
          description: 完了成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SensoryEvaluationDetail'

  /sensory-evaluations/{evaluationId}/report:
    get:
      summary: 評価レポート取得
      operationId: getEvaluationReport
      tags: [SensoryEvaluations]
      parameters:
        - $ref: '#/components/parameters/evaluationId'
        - name: format
          in: query
          schema:
            type: string
            enum: [json, pdf]
            default: json
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EvaluationReport'
            application/pdf:
              schema:
                type: string
                format: binary

  # ============================================
  # Search - Query Side (Elasticsearch)
  # ============================================
  /search/recipes:
    get:
      summary: 処方検索
      operationId: searchRecipes
      tags: [Search]
      parameters:
        - name: q
          in: query
          schema:
            type: string
          description: フリーワード検索
        - name: productType
          in: query
          schema:
            type: array
            items:
              $ref: '#/components/schemas/ProductType'
        - name: status
          in: query
          schema:
            type: array
            items:
              $ref: '#/components/schemas/RecipeStatus'
        - name: ingredientType
          in: query
          schema:
            type: array
            items:
              $ref: '#/components/schemas/IngredientType'
        - name: alcoholMin
          in: query
          schema:
            type: number
        - name: alcoholMax
          in: query
          schema:
            type: number
        - name: bitternessMin
          in: query
          schema:
            type: number
        - name: bitternessMax
          in: query
          schema:
            type: number
        - name: sort
          in: query
          schema:
            type: string
            enum: [relevance, created_desc, created_asc, name_asc]
            default: relevance
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
                $ref: '#/components/schemas/RecipeSearchResult'

  /search/recipes/suggest:
    get:
      summary: 処方サジェスト
      operationId: suggestRecipes
      tags: [Search]
      parameters:
        - name: q
          in: query
          required: true
          schema:
            type: string
            minLength: 2
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RecipeSuggestions'

  /search/recipes/similar/{recipeId}:
    get:
      summary: 類似処方検索
      operationId: findSimilarRecipes
      tags: [Search]
      parameters:
        - $ref: '#/components/parameters/recipeId'
        - name: limit
          in: query
          schema:
            type: integer
            default: 5
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SimilarRecipes'

components:
  parameters:
    recipeId:
      name: recipeId
      in: path
      required: true
      schema:
        type: string
        format: uuid

    evaluationId:
      name: evaluationId
      in: path
      required: true
      schema:
        type: string
        format: uuid

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
    ProductType:
      type: string
      enum: [beer, low_malt_beer, happoshu, non_alcohol, rtd, spirits]

    RecipeStatus:
      type: string
      enum: [draft, under_review, approved, production, archived]

    IngredientType:
      type: string
      enum: [malt, hop, yeast, water, adjunct, additive]

    EvaluationStatus:
      type: string
      enum: [scheduled, in_progress, completed, cancelled]

    EvaluationType:
      type: string
      enum: [development, quality_check, benchmark, consumer]

    # ============================================
    # Recipe Schemas
    # ============================================
    Recipe:
      type: object
      properties:
        recipeId:
          type: string
          format: uuid
        recipeCode:
          type: string
        name:
          type: string
        productType:
          $ref: '#/components/schemas/ProductType'
        version:
          $ref: '#/components/schemas/RecipeVersion'
        status:
          $ref: '#/components/schemas/RecipeStatus'
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    RecipeVersion:
      type: object
      properties:
        major:
          type: integer
        minor:
          type: integer
        patch:
          type: integer
        display:
          type: string

    RecipeDetail:
      allOf:
        - $ref: '#/components/schemas/Recipe'
        - type: object
          properties:
            concept:
              $ref: '#/components/schemas/ProductConcept'
            ingredients:
              type: array
              items:
                $ref: '#/components/schemas/RecipeIngredient'
            processSpec:
              $ref: '#/components/schemas/ProcessSpecification'
            targetProfile:
              $ref: '#/components/schemas/TargetFlavorProfile'
            qualitySpec:
              $ref: '#/components/schemas/QualitySpecification'
            approvedAt:
              type: string
              format: date-time
            approvedBy:
              type: string
              format: uuid

    RecipeList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Recipe'
        totalCount:
          type: integer
        page:
          type: integer
        pageSize:
          type: integer

    ProductConcept:
      type: object
      properties:
        description:
          type: string
        targetConsumer:
          type: string
        positioning:
          type: string
        keyFeatures:
          type: array
          items:
            type: string
        brandId:
          type: string
          format: uuid

    RecipeIngredient:
      type: object
      properties:
        ingredientId:
          type: string
          format: uuid
        ingredientType:
          $ref: '#/components/schemas/IngredientType'
        name:
          type: string
        ratio:
          type: number
          minimum: 0
          maximum: 100
        specification:
          $ref: '#/components/schemas/IngredientSpec'

    IngredientSpec:
      type: object
      properties:
        grade:
          type: string
        origin:
          type: string
        characteristics:
          type: object
          additionalProperties:
            type: string

    ProcessSpecification:
      type: object
      properties:
        mashingSpec:
          $ref: '#/components/schemas/MashingSpec'
        boilingSpec:
          $ref: '#/components/schemas/BoilingSpec'
        fermentationSpec:
          $ref: '#/components/schemas/FermentationSpec'
        maturationSpec:
          $ref: '#/components/schemas/MaturationSpec'

    MashingSpec:
      type: object
      properties:
        mashInTemperature:
          type: number
        mashSteps:
          type: array
          items:
            type: object
            properties:
              temperature:
                type: number
              durationMinutes:
                type: integer
              purpose:
                type: string
        waterToGrainRatio:
          type: number

    BoilingSpec:
      type: object
      properties:
        boilDurationMinutes:
          type: integer
        hopAdditions:
          type: array
          items:
            $ref: '#/components/schemas/HopAddition'
        evaporationRate:
          type: number

    HopAddition:
      type: object
      properties:
        hopVariety:
          type: string
        amountGrams:
          type: number
        additionTimeMinutes:
          type: integer
        purpose:
          type: string
          enum: [bittering, flavor, aroma, dry_hop]

    FermentationSpec:
      type: object
      properties:
        yeastStrainId:
          type: string
          format: uuid
        pitchRate:
          type: number
        fermentationTemperature:
          type: number
        fermentationDays:
          type: integer
        attenuationTarget:
          type: number

    MaturationSpec:
      type: object
      properties:
        temperature:
          type: number
        durationDays:
          type: integer
        dryHopping:
          type: boolean

    TargetFlavorProfile:
      type: object
      properties:
        appearance:
          type: string
        aroma:
          type: string
        taste:
          type: string
        mouthfeel:
          type: string
        targetBitterness:
          type: number
        targetAlcohol:
          type: number

    QualitySpecification:
      type: object
      properties:
        alcoholContent:
          $ref: '#/components/schemas/RangeSpec'
        originalGravity:
          $ref: '#/components/schemas/RangeSpec'
        color:
          $ref: '#/components/schemas/RangeSpec'
        bitterness:
          $ref: '#/components/schemas/RangeSpec'

    RangeSpec:
      type: object
      properties:
        min:
          type: number
        max:
          type: number
        target:
          type: number
        unit:
          type: string

    CreateRecipeRequest:
      type: object
      required: [name, productType, concept]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200
        productType:
          $ref: '#/components/schemas/ProductType'
        concept:
          $ref: '#/components/schemas/ProductConcept'
        ingredients:
          type: array
          items:
            $ref: '#/components/schemas/RecipeIngredient'

    UpdateRecipeRequest:
      type: object
      properties:
        name:
          type: string
        concept:
          $ref: '#/components/schemas/ProductConcept'

    UpdateIngredientsRequest:
      type: object
      required: [ingredients]
      properties:
        ingredients:
          type: array
          items:
            $ref: '#/components/schemas/RecipeIngredient'

    VersionHistory:
      type: object
      properties:
        recipeId:
          type: string
          format: uuid
        versions:
          type: array
          items:
            type: object
            properties:
              version:
                $ref: '#/components/schemas/RecipeVersion'
              createdAt:
                type: string
                format: date-time
              changeDescription:
                type: string

    # ============================================
    # Quality Standard Schemas
    # ============================================
    QualityStandard:
      type: object
      properties:
        standardId:
          type: string
          format: uuid
        recipeId:
          type: string
          format: uuid
        physicalSpec:
          $ref: '#/components/schemas/QualitySpecification'
        sensorySpec:
          type: object
        effectiveFrom:
          type: string
          format: date
        effectiveTo:
          type: string
          format: date

    DefineQualityStandardRequest:
      type: object
      required: [physicalSpec, effectiveFrom]
      properties:
        physicalSpec:
          $ref: '#/components/schemas/QualitySpecification'
        sensorySpec:
          type: object
        effectiveFrom:
          type: string
          format: date

    UpdateQualityStandardRequest:
      type: object
      properties:
        physicalSpec:
          $ref: '#/components/schemas/QualitySpecification'
        sensorySpec:
          type: object

    QualityAssessmentRequest:
      type: object
      required: [recipeId, sampleData]
      properties:
        recipeId:
          type: string
          format: uuid
        sampleData:
          type: object
          properties:
            alcoholContent:
              type: number
            originalGravity:
              type: number
            color:
              type: number
            bitterness:
              type: number
            ph:
              type: number

    QualityAssessmentResult:
      type: object
      properties:
        recipeId:
          type: string
          format: uuid
        passed:
          type: boolean
        results:
          type: array
          items:
            type: object
            properties:
              parameter:
                type: string
              measured:
                type: number
              target:
                type: number
              inRange:
                type: boolean

    # ============================================
    # Sensory Evaluation Schemas
    # ============================================
    SensoryEvaluation:
      type: object
      properties:
        evaluationId:
          type: string
          format: uuid
        evaluationType:
          $ref: '#/components/schemas/EvaluationType'
        recipeId:
          type: string
          format: uuid
        evaluationDate:
          type: string
          format: date
        status:
          $ref: '#/components/schemas/EvaluationStatus'
        panelistCount:
          type: integer

    SensoryEvaluationList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/SensoryEvaluation'
        totalCount:
          type: integer

    SensoryEvaluationDetail:
      allOf:
        - $ref: '#/components/schemas/SensoryEvaluation'
        - type: object
          properties:
            panelists:
              type: array
              items:
                $ref: '#/components/schemas/Panelist'
            results:
              $ref: '#/components/schemas/EvaluationResults'

    Panelist:
      type: object
      properties:
        panelistId:
          type: string
          format: uuid
        name:
          type: string
        qualification:
          type: string

    EvaluationResults:
      type: object
      properties:
        averageScores:
          type: object
          additionalProperties:
            type: number
        overallScore:
          type: number
        panelConsensus:
          type: string
          enum: [high, medium, low]
        recommendation:
          type: string

    ScheduleEvaluationRequest:
      type: object
      required: [recipeId, evaluationType, evaluationDate]
      properties:
        recipeId:
          type: string
          format: uuid
        evaluationType:
          $ref: '#/components/schemas/EvaluationType'
        evaluationDate:
          type: string
          format: date
        panelistIds:
          type: array
          items:
            type: string
            format: uuid

    AddPanelistRequest:
      type: object
      required: [panelistId]
      properties:
        panelistId:
          type: string
          format: uuid

    RecordScoreRequest:
      type: object
      required: [panelistId, scores]
      properties:
        panelistId:
          type: string
          format: uuid
        scores:
          type: object
          additionalProperties:
            type: number
        comments:
          type: string

    EvaluationReport:
      type: object
      properties:
        evaluationId:
          type: string
          format: uuid
        summary:
          type: string
        detailedScores:
          type: object
        statisticalAnalysis:
          type: object
        recommendations:
          type: array
          items:
            type: string

    # ============================================
    # Search Schemas
    # ============================================
    RecipeSearchResult:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/RecipeSearchHit'
        totalCount:
          type: integer
        facets:
          type: object

    RecipeSearchHit:
      allOf:
        - $ref: '#/components/schemas/Recipe'
        - type: object
          properties:
            score:
              type: number
            highlights:
              type: object

    RecipeSuggestions:
      type: object
      properties:
        suggestions:
          type: array
          items:
            type: object
            properties:
              text:
                type: string
              recipeId:
                type: string
                format: uuid

    SimilarRecipes:
      type: object
      properties:
        baseRecipeId:
          type: string
          format: uuid
        similarRecipes:
          type: array
          items:
            type: object
            properties:
              recipe:
                $ref: '#/components/schemas/Recipe'
              similarity:
                type: number

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

### 受信イベント（← VS1 研究開発）

| イベント | トピック | 処理 |
|---------|---------|------|
| YeastStrainOptimized | vs1.fermentation.events | 利用可能酵母リスト更新 |
| YeastStrainValidated | vs1.fermentation.events | 製造用酵母として登録 |

### 発行イベント（→ VS3 ブランド）

| イベント | トピック | 購読者 |
|---------|---------|--------|
| RecipeApproved | vs2.recipe.events | BC3 BrandPortfolio |
| ProductApproved | vs2.recipe.events | BC3 BrandPortfolio |

---

**作成日**: 2025-11-28
**VS**: VS2 製品開発
**BC**: BC2 Product Recipe
**次成果物**: database-design.md
