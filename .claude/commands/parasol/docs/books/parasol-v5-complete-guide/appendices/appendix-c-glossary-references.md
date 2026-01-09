# 付録C　用語集と参考文献

## C.1 用語集（Glossary）

### あ行

**アーキテクチャ（Architecture）**
システムの基本的な構造と構成要素、それらの関係性、および設計原則を定義したもの。V5では論理アーキテクチャ（Phase 4）から物理実装（Phase 7）まで段階的に詳細化する。

**価値（Value）**
測定可能で、ステークホルダーに具体的な便益をもたらす成果。V5の中核概念であり、すべての活動は価値の実現に向けられる。単なる機能や要件ではなく、ビジネス成果として定義される。

**価値軸（Value-axis）**
6軸システムの一つ。ビジネス価値を中心に据えてシステムを設計・評価する視点。顧客価値、収益価値、社会価値などを体系的に扱う。

**価値ストリーム（Value Stream）**
顧客に価値を届けるために必要な一連の活動の流れ。V5では価値ストリームを可視化し、最適化することで無駄を排除し、価値実現を加速する。

**価値トレーサビリティ（Value Traceability）**
定義された価値から実装・運用まで一貫して追跡可能にする仕組み。V5の品質保証の要であり、すべての実装が価値に貢献していることを保証する。

**価値レベル（VL: Value Level）**
Parasol V5における価値の階層構造。VL1（最上位価値）→VL2（中位価値）→VL3（詳細価値）の3層で構成される。企業のVision/Missionとは異なり、「何を顧客に届けるか（WHAT）」を定義し、顧客理解の深化により進化（深化）する。

**価値マイルストーン（VMS: Value Milestone）**
価値実現の段階的な到達点。VMS1（顧客が最初の価値を体験できる状態）からVMS5（価値が持続的に拡大する状態）まで5段階で定義され、OKRと連携して定量的に測定される。

### か行

**ケイパビリティ（Capability）**
組織が価値を実現するために必要な能力。技術的な機能だけでなく、プロセス、人材、知識などを含む包括的な概念。V5ではPhase 3で体系的に分解・設計する。

**ケイパビリティレベル（CL: Capability Level）**
Parasol V5における能力分解の3段階構造。

- **CL1（活動領域識別）**: バリューストリームにおける活動の傾向を把握する段階。**傾向的分類**であり参考情報のみ。CL2に継承されない。
- **CL2（ケイパビリティ設計）**: 組織が持つべき能力を正式に設計する段階。**TVDC 4分類（Core/VCI/Supporting/Generic）** として投資判断の根拠となる。V5.5では差別化度（Phase 3で評価）と価値必然性（Phase 2 VL3から継承）の2軸で分類する。
- **CL3（詳細能力定義 + BO対応）**: 詳細能力（Sub-capability）と対応するBO（業務オペレーション）を定義する段階。分類は行わず**網羅性**を重視。Phase 4-5でのBounded Context境界確定への入力となる。

**ケイパビリティ軸（Capability-axis）**
6軸システムの一つ。組織が持つべき能力を中心にシステムを構築する視点。技術能力、業務能力、イノベーション能力などを統合的に扱う。

**構造的必然性（Structural Necessity）**
システムの構造が、ビジネスの要求や制約から必然的に導かれるという考え方。恣意的な設計ではなく、論理的に導かれる最適構造を追求する。

**コンテキスト（Context）**
プロジェクトを取り巻く環境や状況。V5ではPhase 1で詳細に定義し、すべての意思決定の基盤とする。ビジネスコンテキスト、技術コンテキスト、組織コンテキストなどを含む。

### さ行

**サブドメイン（Subdomain）**
大きな問題領域（ドメイン）を、管理可能な単位に分割したもの。V5.5ではTVDC 4分類（Core/VCI/Supporting/Generic）で分類される。従来の3分類にVCI（価値必然インフラ）を追加し、「差別化しないが価値提供に不可欠」なケイパビリティを明確に識別できる。

**システム思考（Systems Thinking）**
個別の要素ではなく、全体の相互作用や創発的性質に着目する思考法。V5では複雑なビジネスシステムを理解し、最適化するための基本的なアプローチ。

**ステークホルダー（Stakeholder）**
プロジェクトに利害関係を持つ個人または組織。顧客、ユーザー、経営者、開発チーム、パートナーなど。V5では各ステークホルダーの価値を明確化し、バランスを取る。

### た行

**多層価値ストリーム軸（Multi-tier Value Stream-axis）**
6軸システムの一つ。組織の階層構造（本社-支社-現場など）に応じて価値ストリームを多層的に管理する視点。ローカル最適とグローバル最適のバランスを取る。

**トレードオフ（Trade-off）**
ある目標を達成するために、別の目標をある程度犠牲にすること。V5では明示的にトレードオフを管理し、意思決定の根拠を明確にする。

**TVDC（Three-Dimensional Value-Driven Classification）**
V5.5で導入された3次元価値駆動分類フレームワーク。差別化度と価値必然性の2軸で、ケイパビリティを4つに分類する：Core（差別化★★★/価値必然性★★★）、VCI（差別化★/価値必然性★★★）、Supporting（差別化★★/価値必然性★★）、Generic（差別化★/価値必然性★）。従来の3分類では曖昧だった「差別化しないが価値提供に不可欠」なケイパビリティをVCIとして明確に識別できる。

### な行

**ノンファンクショナル要求（Non-functional Requirements）**
システムの品質特性に関する要求。性能、信頼性、セキュリティ、使用性など。V5では価値実現に必要な品質特性として体系的に管理する。

### は行

**パラソルドメイン言語（Parasol Domain Language）**
Phase 4-5で定義されたBounded Context内で使用される共通言語。DDDのユビキタス言語に相当し、技術者とビジネスエキスパートが同じ用語で会話できるようにする。各Bounded Contextは独自のパラソルドメイン言語を持ち、コンテキスト間では明示的な翻訳が必要となる。

**バウンデッドコンテキスト（Bounded Context）**
特定のモデルが有効な境界。DDDの中核概念であり、V5では自律的なシステム単位として扱う。各コンテキストは独自のユビキタス言語（パラソルドメイン言語）を持つ。Parasol V5ではPhase 4-5でCL3を基に境界確定される。

**ビジネスユニット軸（Business-unit-axis）**
6軸システムの一つ。組織の事業部門や機能部門の視点からシステムを設計する軸。部門間の協調と自律性のバランスを最適化する。

**プラットフォーム軸（Platform-axis）**
6軸システムの一つ。共通基盤やエコシステムの視点からシステムを構築する軸。再利用性、拡張性、相互運用性を重視する。

**フェーズ（Phase）**
V5の開発プロセスにおける段階。Phase 0（現状理解）からPhase 7（統合価値実現）まで8つのフェーズで構成される。各フェーズは明確な成果物を持つ。

**フュージョン軸（Fusion-axis）**
6軸システムの一つ。異なる領域やシステムの融合による新しい価値創造に焦点を当てる軸。イノベーションや新規事業創造に適している。

### ま行

**マイクロサービス（Microservices）**
小さく、独立してデプロイ可能なサービスの集合としてアプリケーションを構築するアーキテクチャスタイル。V5では必要に応じて採用される実装パターンの一つ。

**マイルストーン（Milestone）**
プロジェクトの重要な通過点。V5ではVMS1からVMS5まで5つの主要価値マイルストーン（Value Milestone）を設定し、段階的に価値を実現する。

### や行

**ユビキタス言語（Ubiquitous Language）**
特定のバウンデッドコンテキスト内で、技術者とドメインエキスパートが共通して使用する言語。誤解を防ぎ、正確なコミュニケーションを実現する。

### ら行

**リファクタリング（Refactoring）**
外部から見た振る舞いを変えずに、内部構造を改善すること。V5では継続的なリファクタリングにより、システムの健全性を維持する。

**レガシーシステム（Legacy System）**
既存の古いシステム。V5では段階的な移行戦略により、ビジネスを止めることなくモダナイゼーションを実現する。

### わ行

**ワークショップ（Workshop）**
関係者が集まって共同作業を行う場。V5では価値発見ワークショップ、アーキテクチャワークショップなど、各フェーズで重要な役割を果たす。

## C.2 略語集

**AI** - Artificial Intelligence（人工知能）

**API** - Application Programming Interface（アプリケーションプログラミングインターフェース）

**B2B** - Business to Business（企業間取引）

**B2C** - Business to Consumer（企業対消費者取引）

**BC** - Bounded Context（バウンデッドコンテキスト）

**CD** - Continuous Delivery（継続的デリバリー）

**CI** - Continuous Integration（継続的インテグレーション）

**CL** - Capability Level（ケイパビリティレベル）- CL1/CL2/CL3の3段階構造

**CRM** - Customer Relationship Management（顧客関係管理）

**DDD** - Domain-Driven Design（ドメイン駆動設計）

**DevOps** - Development and Operations（開発と運用の統合）

**DP** - Design Parameters（設計パラメータ）- Axiomatic Designの基本概念。FRを「どう実現するか」を定義。Parasol V5ではBC/サービスに相当。

**DX** - Digital Transformation（デジタルトランスフォーメーション）

**TVDC** - Three-Dimensional Value-Driven Classification（3次元価値駆動分類）- V5.5で導入。差別化度×価値必然性の2軸で4分類（Core/VCI/Supporting/Generic）

**ERP** - Enterprise Resource Planning（企業資源計画）

**ESG** - Environment, Social, Governance（環境・社会・ガバナンス）

**FR** - Functional Requirements（機能要件）- Axiomatic Designの基本概念。システムが「何を実現するか」を定義。Parasol V5ではCL3（業務オペレーション）に相当。

**IaC** - Infrastructure as Code（インフラストラクチャのコード化）

**IoT** - Internet of Things（モノのインターネット）

**KPI** - Key Performance Indicator（重要業績評価指標）

**ML** - Machine Learning（機械学習）

**MVP** - Minimum Viable Product（実用最小限の製品）

**NFR** - Non-Functional Requirements（非機能要求）

**OKR** - Objectives and Key Results（目標と主要な結果）

**ROI** - Return on Investment（投資収益率）

**SaaS** - Software as a Service（サービスとしてのソフトウェア）

**SLA** - Service Level Agreement（サービスレベル合意）

**SOA** - Service-Oriented Architecture（サービス指向アーキテクチャ）

**UI/UX** - User Interface / User Experience（ユーザーインターフェース/ユーザー体験）

**VCI** - Value-Critical Infrastructure（価値必然インフラ）- V5.5で導入。差別化度は低いが価値提供に不可欠なケイパビリティ（例：決済処理、認証基盤）

**V5** - Parasol Version 5（パラソル第5版）

**VL** - Value Level（価値レベル）- VL1/VL2/VL3の3層構造

**VMS** - Value Milestone（価値マイルストーン）- VMS1〜VMS5の5段階

**VUCA** - Volatility, Uncertainty, Complexity, Ambiguity（変動性、不確実性、複雑性、曖昧性）

## C.3 参考文献

### 基礎文献

1. **Evans, Eric** (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
   - DDDの原典。V5の理論的基盤の一つ。

2. **Vernon, Vaughn** (2013). *Implementing Domain-Driven Design*. Addison-Wesley.
   - DDDの実践的な実装方法を解説。

3. **Newman, Sam** (2021). *Building Microservices, 2nd Edition*. O'Reilly Media.
   - マイクロサービスアーキテクチャの包括的ガイド。

4. **Fowler, Martin** (2018). *Refactoring: Improving the Design of Existing Code, 2nd Edition*. Addison-Wesley.
   - リファクタリングの基本書。

5. **Bass, Len et al.** (2021). *Software Architecture in Practice, 4th Edition*. Addison-Wesley.
   - ソフトウェアアーキテクチャの体系的解説。

### システム思考・価値創造

6. **Meadows, Donella H.** (2008). *Thinking in Systems: A Primer*. Chelsea Green Publishing.
   - システム思考の入門書。V5の全体最適化アプローチの基礎。

7. **Reinertsen, Donald G.** (2009). *The Principles of Product Development Flow*. Celeritas Publishing.
   - 価値の流れを最適化する原則。

8. **Poppendieck, Mary & Tom** (2006). *Implementing Lean Software Development*. Addison-Wesley.
   - リーン思考のソフトウェア開発への適用。

9. **Kim, Gene et al.** (2016). *The DevOps Handbook*. IT Revolution Press.
   - DevOpsの実践方法とその価値。

### アーキテクチャパターン

10. **Richardson, Chris** (2018). *Microservices Patterns*. Manning Publications.
    - マイクロサービスの設計パターン集。

11. **Hohpe, Gregor & Bobby Woolf** (2003). *Enterprise Integration Patterns*. Addison-Wesley.
    - エンタープライズ統合のパターンカタログ。

12. **Ford, Neal et al.** (2017). *Building Evolutionary Architectures*. O'Reilly Media.
    - 進化的アーキテクチャの構築方法。

13. **Kleppmann, Martin** (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
    - データ中心のアプリケーション設計。

### 組織・チーム

14. **Skelton, Matthew & Manuel Pais** (2019). *Team Topologies*. IT Revolution Press.
    - 効果的なチーム構造の設計。

15. **Forsgren, Nicole et al.** (2018). *Accelerate*. IT Revolution Press.
    - 高パフォーマンス組織の科学的研究。

16. **DeMarco, Tom & Timothy Lister** (2013). *Peopleware, 3rd Edition*. Addison-Wesley.
    - 生産的なソフトウェアチームの構築。

### AI・未来技術

17. **Russell, Stuart & Peter Norvig** (2020). *Artificial Intelligence: A Modern Approach, 4th Edition*. Pearson.
    - AIの包括的教科書。

18. **Brynjolfsson, Erik & Andrew McAfee** (2014). *The Second Machine Age*. W. W. Norton & Company.
    - デジタル技術による社会変革。

19. **O'Reilly, Tim** (2017). *WTF?: What's the Future and Why It's Up to Us*. Harper Business.
    - 技術の未来と人間の役割。

### 日本語文献

20. **増田 亨** (2022). 『現場で役立つシステム設計の原則』. 技術評論社.
    - 実践的な設計原則の解説。

21. **成瀬 允宣** (2022). 『ドメイン駆動設計入門』. 翔泳社.
    - DDDの日本語入門書。

22. **松岡 聡 他** (2019). 『マイクロサービスアーキテクチャ』. オライリージャパン.
    - マイクロサービスの日本語解説。

## C.4 オンラインリソース

### 公式サイト・ドキュメント

- **Parasol V5 公式サイト**: https://parasol-v5.io
  - 最新情報、ドキュメント、ダウンロード

- **Parasol Community Forum**: https://community.parasol-v5.io
  - ユーザーコミュニティ、Q&A、事例共有

- **Parasol Academy**: https://academy.parasol-v5.io
  - オンライン学習コース、認定プログラム

### 関連サイト

- **Martin Fowler's Blog**: https://martinfowler.com
  - アーキテクチャ、リファクタリング、アジャイル

- **Domain-Driven Design Community**: https://dddcommunity.org
  - DDD関連の情報とリソース

- **InfoQ**: https://www.infoq.com
  - ソフトウェア開発の最新トレンド

- **ThoughtWorks Technology Radar**: https://www.thoughtworks.com/radar
  - 技術トレンドの評価

### 学術リソース

- **IEEE Xplore Digital Library**: https://ieeexplore.ieee.org
  - コンピュータサイエンスの学術論文

- **ACM Digital Library**: https://dl.acm.org
  - コンピューティング分野の研究論文

- **arXiv**: https://arxiv.org
  - プレプリントサーバー（CS分野）

## C.5 推奨学習パス

### 初級者向け

1. 本書の通読
2. Parasol Academy「V5 Fundamentals」コース
3. 小規模パイロットプロジェクトの実施
4. コミュニティフォーラムへの参加

### 中級者向け

1. DDD関連書籍の学習
2. アーキテクチャパターンの研究
3. 実プロジェクトでのV5適用
4. 事例発表・知識共有

### 上級者向け

1. カスタムパターンの開発
2. 他社へのメンタリング
3. V5の拡張・貢献
4. 論文・書籍の執筆

## C.6 認定制度

### Parasol V5 認定資格

**V5 Practitioner**
- 基礎知識の理解
- 小規模プロジェクトの実施能力
- オンライン試験

**V5 Professional**
- 実践的な適用能力
- 中規模プロジェクトのリード
- 実技試験＋面接

**V5 Master**
- 高度な応用能力
- 大規模・複雑プロジェクトの統括
- 論文審査＋実績評価

**V5 Instructor**
- 教育・指導能力
- カリキュラム開発
- 指導実績＋peer review

---

この用語集と参考文献は、V5の学習と実践を支援するためのものです。継続的に更新されますので、最新版は公式サイトでご確認ください。

さらなる学習のために、コミュニティへの参加をお勧めします。実践者同士の交流が、最も価値ある学びをもたらすでしょう。