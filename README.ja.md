# Album Cover Director

$album-cover-director は、アルバム、EP、シングルのジャケットを構想から3000px納品までディレクションするCodex Skill / Pluginです。曲の意味を3つの異なる画面構造へ変換し、GPT Image 2で候補を生成・比較し、文字を独立したデザイン品質として検査します。

トラックメイカー、音楽家、プロデューサー、インディーレーベル、デザイナーが共通で使えることを目的にしています。特定アーティストの設定、外部MCP、APIキーは必須ではありません。

## 特徴

- 音楽評価から切り離し、ジャケット自体の評価と文字支配度を作品ごとに審査する研究パイプライン
- スタイル名ではなく「何が正方形を組織するか」を表す12パターン
- 色違いではなく構造が異なる3方向
- 文字生成が崩れたときに後組版へ切り替える独立ゲート
- 56px、128px、256px、原寸、グレースケール、ぼかしの比較
- 1回1変数、最大2サイクルの修正
- 3000 x 3000 PNG/JPGと256pxサムネイルの再現可能な書き出し

## インストール

Codexに次のように依頼できます。

~~~text
次のGitHubリポジトリから album-cover-director スキルをインストールして:
https://github.com/usedhonda/album-cover-director/tree/main/skills/album-cover-director
~~~

手動の場合:

~~~bash
git clone https://github.com/usedhonda/album-cover-director.git
mkdir -p ~/.agents/skills
ln -s "$PWD/album-cover-director/skills/album-cover-director" ~/.agents/skills/album-cover-director
~~~

インストール後にCodexを再起動してください。リポジトリ直下は .codex-plugin/plugin.json を備えたPlugin bundleでもあり、CodexのPlugin marketplaceへ内容を組み替えず掲載できます。

## 使い方

~~~text
$album-cover-director
作品名: Glass Weather
アーティスト: Example Artist
実行量: standard
歌詞: ...
避けたい表現: ネオン都市、中央の顔
~~~

自然文でも起動します。

~~~text
この新曲のジャケットを歌詞から6枚作って。
色違いではなく構造の違う3方向にして、3000pxで納品して。
~~~

必須入力:

- 正確な作品名
- アーティスト名
- 歌詞、曲の説明、音源のいずれか

実行量は quick=3枚、standard=6枚、deep=12枚。文字モードは auto、image-native、post-typeset、custom-wordmark です。

## 文字設計

custom-wordmark ではフォント名だけを指定しません。骨格、幅、太さ、カウンター、端部、リズム、加工原理を定義します。正確な綴り、字間、行間、ベースラインを満たさないAI生成文字は採用せず、文字なし原版と正確な後組版へ切り替えます。

後組版は `cover-ops.py typeset` で、ライセンス確認済みのフォント、正確なタイトル文字列、位置、整列、字間を明示して行えます。コマンドは入力文字列・フォント・配置・出力SHA-256を記録します。

完成条件は、128pxで読めることに加え、画像を隠してもタイトル造形として成立することです。

## 成果物

~~~text
album-cover/<release-slug>/
├── creative-brief.yaml
├── directions.md
├── prompts/
├── run-ledger.jsonl
├── selected-master.png
├── delivery/cover-3000.png
├── delivery/cover-3000.jpg
├── delivery/thumbnail-256.png
└── cover-report.md
~~~

画像生成環境またはPillowがない場合、完成したbrief、方向案、prompt、正確な書き出し仕様までは返しますが、「納品完了」とは表示しません。

## 研究と著作権

[research/corpus.yaml](research/corpus.yaml) は置換予定の旧ドラフトであり、制作時の正本ではありません。`v0.1.0` 前に、ジャケット固有の評価根拠と実物視覚審査を持つ文字支配型コーパスへ置き換えます。現在の研究到達点は [checkpoint-80.md](research/checkpoint-80.md) に記録しており、出典を分離して検証するまでは最終採用品ではありません。第三者のジャケット画像は収録しません。

新コーパスの採用条件は、ジャケット固有の評価根拠、文字支配度T4/T5、実物視覚確認、作品固有の転用原理です。名盤順位、売上、音楽的知名度はジャケット評価の根拠にしません。

## 検証

~~~bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
~~~

CIではSkill frontmatter、Plugin manifest、旧ドラフト／最終コーパスの明示状態、研究チェックポイントと分布、リンク形式、第三者画像の不在、秘密情報・ローカル絶対パスの不在を検査します。

## ライセンス

コード、指示、スキーマ、独自観察は[MIT License](LICENSE)です。第三者のアルバム画像は含まず、再ライセンスもしません。
