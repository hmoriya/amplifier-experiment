# BC1: Fermentation Platform - API仕様

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS1 研究開発 |
| BC | Fermentation Platform |
| 技術スタック | Python / FastAPI |
| API形式 | REST + GraphQL (検索用) |
| 認証 | OAuth 2.0 / JWT |

---

## OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: Fermentation Platform API
  version: 1.0.0
  description: |
    アサヒグループ発酵プラットフォームAPI
    酵母ライブラリ管理、発酵プロセス管理、研究実験管理

servers:
  - url: https://api.asahi-rd.internal/fermentation/v1
    description: Production (内部)
  - url: https://api-staging.asahi-rd.internal/fermentation/v1
    description: Staging

tags:
  - name: YeastStrains
    description: 酵母株管理
  - name: FermentationProcesses
    description: 発酵プロセス管理
  - name: Experiments
    description: 研究実験管理
  - name: Recommendations
    description: 酵母推薦・最適化

paths:
  # ============================================
  # Yeast Strains
  # ============================================
  /yeast-strains:
    get:
      summary: 酵母株一覧取得
      operationId: listYeastStrains
      tags: [YeastStrains]
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [research, validated, production, archived]
        - name: flocculation
          in: query
          schema:
            type: string
            enum: [low, medium, high]
        - name: keyword
          in: query
          schema:
            type: string
          description: 名称・コードで検索
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
            maximum: 100
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YeastStrainList'

    post:
      summary: 酵母株登録
      operationId: registerYeastStrain
      tags: [YeastStrains]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RegisterYeastStrainRequest'
      responses:
        '201':
          description: 登録成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YeastStrain'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: 重複エラー（strainCode）

  /yeast-strains/{strainId}:
    get:
      summary: 酵母株詳細取得
      operationId: getYeastStrain
      tags: [YeastStrains]
      parameters:
        - $ref: '#/components/parameters/strainId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YeastStrainDetail'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: 酵母株更新
      operationId: updateYeastStrain
      tags: [YeastStrains]
      parameters:
        - $ref: '#/components/parameters/strainId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateYeastStrainRequest'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YeastStrain'
        '404':
          $ref: '#/components/responses/NotFound'

  /yeast-strains/{strainId}/flavor-profile:
    put:
      summary: 風味プロファイル更新
      operationId: updateFlavorProfile
      tags: [YeastStrains]
      parameters:
        - $ref: '#/components/parameters/strainId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FlavorProfile'
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YeastStrain'

  /yeast-strains/{strainId}/optimize:
    post:
      summary: 酵母株最適化情報登録
      operationId: optimizeYeastStrain
      tags: [YeastStrains]
      parameters:
        - $ref: '#/components/parameters/strainId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OptimizationRequest'
      responses:
        '200':
          description: 最適化情報登録成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YeastStrain'

  /yeast-strains/{strainId}/events:
    get:
      summary: 酵母株イベント履歴取得
      operationId: getYeastStrainEvents
      tags: [YeastStrains]
      parameters:
        - $ref: '#/components/parameters/strainId'
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EventHistory'

  /yeast-strains/compare:
    post:
      summary: 酵母株比較
      operationId: compareYeastStrains
      tags: [YeastStrains]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [strainIds]
              properties:
                strainIds:
                  type: array
                  items:
                    type: string
                    format: uuid
                  minItems: 2
                  maxItems: 5
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StrainComparison'

  # ============================================
  # Fermentation Processes
  # ============================================
  /fermentation-processes:
    get:
      summary: 発酵プロセス一覧取得
      operationId: listFermentationProcesses
      tags: [FermentationProcesses]
      parameters:
        - name: strainId
          in: query
          schema:
            type: string
            format: uuid
        - name: status
          in: query
          schema:
            type: string
            enum: [planned, in_progress, completed, aborted]
        - name: scaleType
          in: query
          schema:
            type: string
            enum: [laboratory, pilot, production]
        - name: startFrom
          in: query
          schema:
            type: string
            format: date
        - name: startTo
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
                $ref: '#/components/schemas/FermentationProcessList'

    post:
      summary: 発酵プロセス開始
      operationId: startFermentationProcess
      tags: [FermentationProcesses]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StartFermentationRequest'
      responses:
        '201':
          description: 開始成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FermentationProcess'

  /fermentation-processes/{processId}:
    get:
      summary: 発酵プロセス詳細取得
      operationId: getFermentationProcess
      tags: [FermentationProcesses]
      parameters:
        - $ref: '#/components/parameters/processId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FermentationProcessDetail'
        '404':
          $ref: '#/components/responses/NotFound'

  /fermentation-processes/{processId}/measurements:
    get:
      summary: 測定データ一覧取得
      operationId: getMeasurements
      tags: [FermentationProcesses]
      parameters:
        - $ref: '#/components/parameters/processId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MeasurementList'

    post:
      summary: 測定データ記録
      operationId: recordMeasurement
      tags: [FermentationProcesses]
      parameters:
        - $ref: '#/components/parameters/processId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RecordMeasurementRequest'
      responses:
        '201':
          description: 記録成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProcessMeasurement'

  /fermentation-processes/{processId}/conditions:
    put:
      summary: 発酵条件調整
      operationId: adjustConditions
      tags: [FermentationProcesses]
      parameters:
        - $ref: '#/components/parameters/processId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdjustConditionsRequest'
      responses:
        '200':
          description: 調整成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FermentationProcess'

  /fermentation-processes/{processId}/complete:
    post:
      summary: 発酵プロセス完了
      operationId: completeFermentationProcess
      tags: [FermentationProcesses]
      parameters:
        - $ref: '#/components/parameters/processId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CompleteProcessRequest'
      responses:
        '200':
          description: 完了成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FermentationProcess'

  /fermentation-processes/{processId}/timeseries:
    get:
      summary: 時系列データ取得
      operationId: getTimeSeries
      tags: [FermentationProcesses]
      parameters:
        - $ref: '#/components/parameters/processId'
        - name: metric
          in: query
          schema:
            type: string
            enum: [temperature, ph, gravity, cell_count]
        - name: interval
          in: query
          schema:
            type: string
            enum: [raw, 1h, 6h, 1d]
            default: raw
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TimeSeriesData'

  # ============================================
  # Experiments
  # ============================================
  /experiments:
    get:
      summary: 研究実験一覧取得
      operationId: listExperiments
      tags: [Experiments]
      parameters:
        - name: strainId
          in: query
          schema:
            type: string
            format: uuid
        - name: status
          in: query
          schema:
            type: string
            enum: [planned, in_progress, completed]
        - name: researcherId
          in: query
          schema:
            type: string
            format: uuid
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
                $ref: '#/components/schemas/ExperimentList'

    post:
      summary: 研究実験計画
      operationId: planExperiment
      tags: [Experiments]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlanExperimentRequest'
      responses:
        '201':
          description: 計画成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Experiment'

  /experiments/{experimentId}:
    get:
      summary: 研究実験詳細取得
      operationId: getExperiment
      tags: [Experiments]
      parameters:
        - $ref: '#/components/parameters/experimentId'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExperimentDetail'

  /experiments/{experimentId}/findings:
    post:
      summary: 発見事項追加
      operationId: addFinding
      tags: [Experiments]
      parameters:
        - $ref: '#/components/parameters/experimentId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AddFindingRequest'
      responses:
        '201':
          description: 追加成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResearchFinding'

  # ============================================
  # Recommendations
  # ============================================
  /recommendations/yeast:
    post:
      summary: 酵母株推薦
      operationId: recommendYeast
      tags: [Recommendations]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/YeastRecommendationRequest'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YeastRecommendationResponse'

  /recommendations/optimize-conditions:
    post:
      summary: 発酵条件最適化
      operationId: optimizeConditions
      tags: [Recommendations]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OptimizeConditionsRequest'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OptimizeConditionsResponse'

  /recommendations/predict-outcome:
    post:
      summary: 発酵結果予測
      operationId: predictOutcome
      tags: [Recommendations]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PredictOutcomeRequest'
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PredictOutcomeResponse'

components:
  parameters:
    strainId:
      name: strainId
      in: path
      required: true
      schema:
        type: string
        format: uuid
      description: 酵母株ID

    processId:
      name: processId
      in: path
      required: true
      schema:
        type: string
        format: uuid
      description: 発酵プロセスID

    experimentId:
      name: experimentId
      in: path
      required: true
      schema:
        type: string
        format: uuid
      description: 実験ID

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
    # Yeast Strain Schemas
    # ============================================
    YeastStrain:
      type: object
      properties:
        strainId:
          type: string
          format: uuid
        strainCode:
          type: string
          pattern: '^ASH-\d{4}-\d{4}$'
        name:
          type: string
        origin:
          $ref: '#/components/schemas/StrainOrigin'
        characteristics:
          $ref: '#/components/schemas/YeastCharacteristics'
        flavorProfile:
          $ref: '#/components/schemas/FlavorProfile'
        fermentationProfile:
          $ref: '#/components/schemas/FermentationProfile'
        status:
          type: string
          enum: [research, validated, production, archived]
        registeredAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    YeastStrainList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/YeastStrain'
        totalCount:
          type: integer
        page:
          type: integer
        pageSize:
          type: integer

    YeastStrainDetail:
      allOf:
        - $ref: '#/components/schemas/YeastStrain'
        - type: object
          properties:
            processHistory:
              type: array
              items:
                $ref: '#/components/schemas/ProcessSummary'
            experimentHistory:
              type: array
              items:
                $ref: '#/components/schemas/ExperimentSummary'

    StrainOrigin:
      type: object
      properties:
        source:
          type: string
          enum: [natural, bred, modified, acquired]
        location:
          type: string
        collectedAt:
          type: string
          format: date
        parentStrainIds:
          type: array
          items:
            type: string
            format: uuid

    YeastCharacteristics:
      type: object
      properties:
        alcoholTolerance:
          type: number
          minimum: 0
          maximum: 100
        temperatureRange:
          type: object
          properties:
            min:
              type: number
            max:
              type: number
        flocculationLevel:
          type: string
          enum: [low, medium, high]
        attenuationRange:
          type: object
          properties:
            min:
              type: number
            max:
              type: number
        oxygenRequirement:
          type: string
          enum: [low, medium, high]

    FlavorProfile:
      type: object
      properties:
        esterLevel:
          $ref: '#/components/schemas/FlavorLevel'
        phenolLevel:
          $ref: '#/components/schemas/FlavorLevel'
        sulfurLevel:
          $ref: '#/components/schemas/FlavorLevel'
        fruitiness:
          $ref: '#/components/schemas/FlavorLevel'
        spiciness:
          $ref: '#/components/schemas/FlavorLevel'
        cleanness:
          $ref: '#/components/schemas/FlavorLevel'
        notes:
          type: array
          items:
            type: string

    FlavorLevel:
      type: string
      enum: [none, very_low, low, medium, high, very_high]

    FermentationProfile:
      type: object
      properties:
        optimalTemperature:
          type: number
        fermentationSpeed:
          type: string
          enum: [slow, medium, fast]
        typicalDuration:
          type: object
          properties:
            minDays:
              type: integer
            maxDays:
              type: integer
        co2Production:
          type: string
          enum: [low, medium, high]

    RegisterYeastStrainRequest:
      type: object
      required: [name, origin, characteristics]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        origin:
          $ref: '#/components/schemas/StrainOrigin'
        characteristics:
          $ref: '#/components/schemas/YeastCharacteristics'
        flavorProfile:
          $ref: '#/components/schemas/FlavorProfile'
        fermentationProfile:
          $ref: '#/components/schemas/FermentationProfile'

    UpdateYeastStrainRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        characteristics:
          $ref: '#/components/schemas/YeastCharacteristics'
        status:
          type: string
          enum: [research, validated, production, archived]

    OptimizationRequest:
      type: object
      required: [optimizationType, improvements]
      properties:
        optimizationType:
          type: string
        improvements:
          type: object
          additionalProperties:
            type: object
            properties:
              before:
                type: string
              after:
                type: string
              description:
                type: string

    StrainComparison:
      type: object
      properties:
        strains:
          type: array
          items:
            $ref: '#/components/schemas/YeastStrain'
        comparisonMatrix:
          type: object
          additionalProperties:
            type: object
        recommendations:
          type: array
          items:
            type: string

    # ============================================
    # Fermentation Process Schemas
    # ============================================
    FermentationProcess:
      type: object
      properties:
        processId:
          type: string
          format: uuid
        processCode:
          type: string
        strainId:
          type: string
          format: uuid
        strainName:
          type: string
        conditions:
          $ref: '#/components/schemas/FermentationConditions'
        scaleType:
          type: string
          enum: [laboratory, pilot, production]
        status:
          type: string
          enum: [planned, in_progress, completed, aborted]
        startedAt:
          type: string
          format: date-time
        completedAt:
          type: string
          format: date-time

    FermentationProcessList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/FermentationProcess'
        totalCount:
          type: integer
        page:
          type: integer
        pageSize:
          type: integer

    FermentationProcessDetail:
      allOf:
        - $ref: '#/components/schemas/FermentationProcess'
        - type: object
          properties:
            timeline:
              type: array
              items:
                $ref: '#/components/schemas/FermentationStage'
            latestMeasurement:
              $ref: '#/components/schemas/ProcessMeasurement'
            measurementCount:
              type: integer

    FermentationConditions:
      type: object
      properties:
        temperature:
          type: number
        pressure:
          type: number
        dissolvedOxygen:
          type: number
        pitchRate:
          type: number
        wortGravity:
          type: number

    FermentationStage:
      type: object
      properties:
        stageId:
          type: string
          format: uuid
        name:
          type: string
        targetConditions:
          $ref: '#/components/schemas/FermentationConditions'
        duration:
          type: integer
          description: Duration in hours
        status:
          type: string
          enum: [pending, active, completed]

    ProcessMeasurement:
      type: object
      properties:
        measurementId:
          type: string
          format: uuid
        measuredAt:
          type: string
          format: date-time
        temperature:
          type: number
        ph:
          type: number
        gravity:
          type: number
        cellCount:
          type: number
        notes:
          type: string

    MeasurementList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/ProcessMeasurement'
        totalCount:
          type: integer

    StartFermentationRequest:
      type: object
      required: [strainId, conditions, scaleType]
      properties:
        strainId:
          type: string
          format: uuid
        conditions:
          $ref: '#/components/schemas/FermentationConditions'
        scaleType:
          type: string
          enum: [laboratory, pilot, production]
        timeline:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              targetConditions:
                $ref: '#/components/schemas/FermentationConditions'
              durationHours:
                type: integer

    RecordMeasurementRequest:
      type: object
      required: [temperature, ph, gravity]
      properties:
        temperature:
          type: number
        ph:
          type: number
        gravity:
          type: number
        cellCount:
          type: number
        notes:
          type: string

    AdjustConditionsRequest:
      type: object
      required: [conditions, reason]
      properties:
        conditions:
          $ref: '#/components/schemas/FermentationConditions'
        reason:
          type: string

    CompleteProcessRequest:
      type: object
      required: [finalMeasurement]
      properties:
        finalMeasurement:
          $ref: '#/components/schemas/RecordMeasurementRequest'
        notes:
          type: string

    TimeSeriesData:
      type: object
      properties:
        processId:
          type: string
          format: uuid
        metric:
          type: string
        dataPoints:
          type: array
          items:
            type: object
            properties:
              timestamp:
                type: string
                format: date-time
              value:
                type: number

    # ============================================
    # Experiment Schemas
    # ============================================
    Experiment:
      type: object
      properties:
        experimentId:
          type: string
          format: uuid
        experimentCode:
          type: string
        title:
          type: string
        hypothesis:
          type: string
        methodology:
          $ref: '#/components/schemas/ExperimentMethodology'
        strainIds:
          type: array
          items:
            type: string
            format: uuid
        status:
          type: string
          enum: [planned, in_progress, completed]
        conductedBy:
          type: string
          format: uuid
        startedAt:
          type: string
          format: date-time
        completedAt:
          type: string
          format: date-time

    ExperimentList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Experiment'
        totalCount:
          type: integer
        page:
          type: integer
        pageSize:
          type: integer

    ExperimentDetail:
      allOf:
        - $ref: '#/components/schemas/Experiment'
        - type: object
          properties:
            variables:
              type: array
              items:
                $ref: '#/components/schemas/ExperimentVariable'
            results:
              $ref: '#/components/schemas/ExperimentResults'
            findings:
              type: array
              items:
                $ref: '#/components/schemas/ResearchFinding'

    ExperimentMethodology:
      type: object
      properties:
        type:
          type: string
          enum: [comparative, factorial, optimization, exploratory]
        description:
          type: string
        equipment:
          type: array
          items:
            type: string

    ExperimentVariable:
      type: object
      properties:
        name:
          type: string
        type:
          type: string
          enum: [independent, dependent, controlled]
        unit:
          type: string
        range:
          type: object
          properties:
            min:
              type: number
            max:
              type: number

    ExperimentResults:
      type: object
      properties:
        summary:
          type: string
        conclusion:
          type: string

    ResearchFinding:
      type: object
      properties:
        findingId:
          type: string
          format: uuid
        type:
          type: string
          enum: [expected, unexpected, serendipitous]
        description:
          type: string
        significance:
          type: string
          enum: [low, medium, high, breakthrough]
        applicationPotential:
          type: array
          items:
            type: string
        discoveredAt:
          type: string
          format: date-time

    PlanExperimentRequest:
      type: object
      required: [title, hypothesis, methodology, strainIds]
      properties:
        title:
          type: string
        hypothesis:
          type: string
        methodology:
          $ref: '#/components/schemas/ExperimentMethodology'
        strainIds:
          type: array
          items:
            type: string
            format: uuid
        variables:
          type: array
          items:
            $ref: '#/components/schemas/ExperimentVariable'

    AddFindingRequest:
      type: object
      required: [type, description, significance]
      properties:
        type:
          type: string
          enum: [expected, unexpected, serendipitous]
        description:
          type: string
        significance:
          type: string
          enum: [low, medium, high, breakthrough]
        applicationPotential:
          type: array
          items:
            type: string

    # ============================================
    # Recommendation Schemas
    # ============================================
    YeastRecommendationRequest:
      type: object
      required: [targetFlavorProfile]
      properties:
        targetFlavorProfile:
          $ref: '#/components/schemas/FlavorProfile'
        constraints:
          type: object
          properties:
            temperatureRange:
              type: object
              properties:
                min:
                  type: number
                max:
                  type: number
            scaleType:
              type: string
              enum: [laboratory, pilot, production]
            excludeStrainIds:
              type: array
              items:
                type: string
                format: uuid

    YeastRecommendationResponse:
      type: object
      properties:
        recommendations:
          type: array
          items:
            type: object
            properties:
              strain:
                $ref: '#/components/schemas/YeastStrain'
              matchScore:
                type: number
                minimum: 0
                maximum: 1
              matchDetails:
                type: object
                additionalProperties:
                  type: number

    OptimizeConditionsRequest:
      type: object
      required: [strainId, targetAttributes, scaleType]
      properties:
        strainId:
          type: string
          format: uuid
        targetAttributes:
          type: object
          properties:
            flavorProfile:
              $ref: '#/components/schemas/FlavorProfile'
            fermentationSpeed:
              type: string
              enum: [slow, medium, fast]
            targetAttenuation:
              type: number
        scaleType:
          type: string
          enum: [laboratory, pilot, production]

    OptimizeConditionsResponse:
      type: object
      properties:
        optimalConditions:
          $ref: '#/components/schemas/FermentationConditions'
        expectedProfile:
          $ref: '#/components/schemas/FlavorProfile'
        confidence:
          type: number
          minimum: 0
          maximum: 1
        notes:
          type: array
          items:
            type: string

    PredictOutcomeRequest:
      type: object
      required: [strainId, conditions]
      properties:
        strainId:
          type: string
          format: uuid
        conditions:
          $ref: '#/components/schemas/FermentationConditions'
        scaleType:
          type: string
          enum: [laboratory, pilot, production]

    PredictOutcomeResponse:
      type: object
      properties:
        predictedProfile:
          $ref: '#/components/schemas/FlavorProfile'
        predictedDuration:
          type: object
          properties:
            minDays:
              type: integer
            maxDays:
              type: integer
        riskFactors:
          type: array
          items:
            type: object
            properties:
              factor:
                type: string
              severity:
                type: string
                enum: [low, medium, high]
              mitigation:
                type: string
        confidence:
          type: number
          minimum: 0
          maximum: 1

    # ============================================
    # Common Schemas
    # ============================================
    ProcessSummary:
      type: object
      properties:
        processId:
          type: string
          format: uuid
        processCode:
          type: string
        status:
          type: string
        startedAt:
          type: string
          format: date-time

    ExperimentSummary:
      type: object
      properties:
        experimentId:
          type: string
          format: uuid
        experimentCode:
          type: string
        title:
          type: string
        status:
          type: string

    EventHistory:
      type: object
      properties:
        events:
          type: array
          items:
            type: object
            properties:
              eventId:
                type: string
                format: uuid
              eventType:
                type: string
              occurredAt:
                type: string
                format: date-time
              data:
                type: object

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
            properties:
              field:
                type: string
              message:
                type: string

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## イベント連携（VS間）

### 発行イベント（→ VS2 製品開発）

| イベント | トピック | 購読者 |
|---------|---------|--------|
| YeastStrainOptimized | vs1.fermentation.events | BC2 ProductRecipe |
| YeastStrainValidated | vs1.fermentation.events | BC2 ProductRecipe |
| BreakthroughDiscovered | vs1.fermentation.events | BC5 ProductInnovation |

### イベントスキーマ（Kafka）

```json
{
  "eventId": "uuid",
  "eventType": "YeastStrainOptimized",
  "source": "vs1.fermentation",
  "timestamp": "2024-11-28T10:00:00Z",
  "data": {
    "strainId": "uuid",
    "optimizationType": "string",
    "improvements": {}
  }
}
```

---

**作成日**: 2025-11-28
**VS**: VS1 研究開発
**BC**: BC1 Fermentation Platform
**次成果物**: database-design.md
