# ADR-005: JWT認証の選択

## ステータス

**承認済み** (2025-11-27)

## コンテキスト

マイクロサービス環境での認証・認可方式を決定する必要がある。

**要件:**
- ステートレスな認証（サービス間でセッション共有不要）
- サービス間通信での認証
- 外部クライアント（Web/Mobile）からの認証
- ユーザー情報・権限情報の伝搬
- 標準的なプロトコルの採用

**候補:**
1. JWT (JSON Web Token) + OAuth 2.0
2. セッションベース認証
3. API Key認証
4. mTLS（相互TLS）のみ

## 決定

**JWT (JSON Web Token) + OAuth 2.0 を認証方式として採用する。**

構成:
- IdP (Identity Provider): Keycloak（または Azure AD）
- 認証フロー: OAuth 2.0 Authorization Code Flow（外部クライアント）
- サービス間: JWT + mTLS

```yaml
外部クライアント認証:
  フロー: Authorization Code Flow + PKCE
  トークン:
    Access Token: JWT (有効期限: 1時間)
    Refresh Token: Opaque (有効期限: 7日)

サービス間認証:
  方式: Service Account JWT + mTLS
  トークン発行: IdPから事前取得またはClient Credentials Flow
```

## 結果

### 良い影響

1. **ステートレス**: サーバー側でセッション管理不要。スケーラビリティ向上。
2. **自己完結型**: トークン内にユーザー情報・権限を含む。IdPへの問い合わせ不要。
3. **標準規格**: OAuth 2.0, OpenID Connect, JWTは広く採用された標準。
4. **クロスドメイン**: 異なるドメイン・サービス間で認証情報を共有可能。
5. **監査可能**: トークンにユーザー情報が含まれ、監査ログに記録可能。

### 悪い影響/トレードオフ

1. **トークンサイズ**: JWTはセッションIDより大きい（通常1-2KB）。
   - 影響: ヘッダーサイズ増加。R&D用途では許容範囲。
2. **即時無効化の困難**: 発行済みトークンを即座に無効化できない。
   - 対策: 短い有効期限（1時間）、リフレッシュトークンローテーション
3. **秘密鍵管理**: 署名用秘密鍵の安全な管理が必要。
   - 対策: IdPに管理を委任、定期的なキーローテーション

### リスク

1. **トークン漏洩**: トークンが漏洩すると有効期限まで不正利用可能。
   - 対策: HTTPS必須、短い有効期限、センシティブ操作時の再認証
2. **IdP障害**: IdPがダウンすると新規認証不可。
   - 対策: IdPの高可用性構成、トークンのキャッシュ

## トークン構造

```json
// Access Token Payload
{
  "iss": "https://auth.asahi-rnd.example.com",
  "sub": "user-uuid-here",
  "aud": ["beer-development-service", "fermentation-research-service"],
  "exp": 1732752000,
  "iat": 1732748400,
  "scope": "read write",
  "roles": ["researcher", "developer"],
  "department": "beer-development",
  "name": "山田 太郎",
  "email": "yamada@asahi.example.com"
}
```

## 認可 (Authorization)

```yaml
方式: RBAC (Role-Based Access Control)

ロール定義:
  researcher:
    - 研究データの読み書き
    - 実験記録の作成
  developer:
    - 製品開発データの読み書き
    - 試作依頼の作成
  evaluator:
    - 官能評価の実施
    - 評価結果の記録
  viewer:
    - 読み取りのみ
  admin:
    - 全権限
    - ユーザー管理

スコープ (API単位):
  read: GET操作
  write: POST/PUT/DELETE操作
  admin: 管理操作
```

## 代替案

### 代替案1: セッションベース認証

**評価:**
- メリット: 即時無効化可能、実装がシンプル
- デメリット: ステートフル（セッションストア必要）、スケーラビリティに課題
- 判断: マイクロサービス環境には不向き

### 代替案2: API Key認証

**評価:**
- メリット: シンプル、サービス間通信に適する
- デメリット: ユーザー認証には不向き、権限管理が困難
- 判断: 外部システム連携の補助手段としては検討可能

### 代替案3: mTLSのみ

**評価:**
- メリット: 強力なサービス間認証、暗号化も兼ねる
- デメリット: ユーザー情報の伝搬が困難、証明書管理が複雑
- 判断: サービス間通信の補強として併用

## 関連

- ADR-003: API Gatewayパターンの採用
- integration-patterns.md (セキュリティセクション)

---

**作成者:** Claude (Parasol V5)
**作成日:** 2025-11-27
