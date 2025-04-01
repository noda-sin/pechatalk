# PechaTalk

PechaTalkは音声認識と人工知能を組み合わせた対話型アシスタントです。マイクから音声を取得し、音声認識でテキストに変換し、OpenAI APIを使用して応答を生成し、テキストまたは音声で出力します。

## 特徴

- **音声認識**: Faster Whisperモデルを使用して高精度な音声認識を実現
- **自然言語処理**: OpenAI APIを使用して自然な対話を実現
- **音声出力**: VOICEVOXを使用した音声合成（オプション）またはテキスト出力
- **カスタマイズ可能**: 認識エンジンや出力方法を簡単に切り替え可能

## 必要条件

- Python 3.8以上
- OpenAI API キー
- 必要なPythonパッケージ（requirements.txtに記載）

## インストール

1. リポジトリをクローンまたはダウンロードします

```bash
git clone https://github.com/yourusername/pechatalk.git
cd pechatalk
```

2. 仮想環境を作成し、アクティベートします

```bash
python -m venv .venv
source .venv/bin/activate  # Linuxの場合
# または
.venv\Scripts\activate  # Windowsの場合
```

3. 必要なパッケージをインストールします

```bash
pip install -r requirements.txt
```

4. `.env`ファイルを作成し、OpenAI APIキーを設定します

```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## 環境設定

### 環境変数

このアプリケーションは `.env` ファイルを使用して環境変数を管理します。以下の手順で設定してください：

1. プロジェクトのルートディレクトリに `.env` ファイルを作成します（既に作成されている場合はこのステップをスキップしてください）
2. `.env` ファイルに以下の環境変数を設定します：

```
OPENAI_API_KEY=your_api_key_here
```

3. `your_api_key_here` を実際のOpenAI APIキーに置き換えてください

注意：`.env` ファイルは `.gitignore` に追加されているため、Git リポジトリにコミットされません。これは API キーなどの機密情報を保護するためです。

## 使用方法

基本的な使い方：

```bash
python cli.py
```

オプションを指定して実行：

```bash
python cli.py --apikey "your_api_key_here" --recognizer "faster_wisper" --mouth "printer"
```

### コマンドラインオプション

- `--apikey`: OpenAI APIキー（指定しない場合は環境変数から読み込み）
- `--recognizer`: 音声認識エンジン（デフォルト: "faster_wisper"）
- `--mouth`: 出力方法（デフォルト: "printer"）
  - "printer": テキスト出力
  - "voicevox": VOICEVOX音声合成（要VOICEVOXサーバー）

## コンポーネント

PechaTalkは以下の主要コンポーネントで構成されています：

### Ear (ear.py)

マイクからの音声入力を担当します。音声を取得し、認識エンジンに送信します。

### Recognizer (recognizer.py)

音声認識を担当します。現在はFaster Whisperモデルをサポートしています。

### Brain (brain.py)

OpenAI APIを使用して、認識されたテキストに対する応答を生成します。

### Mouth (mouth.py)

応答の出力を担当します。テキスト出力またはVOICEVOXを使用した音声合成をサポートしています。

### Pechat (pechat.py)

上記のコンポーネントを統合し、全体のフローを管理します。

### CLI (cli.py)

コマンドラインインターフェースを提供します。

## VOICEVOXの設定

音声出力にVOICEVOXを使用する場合は、以下の手順で設定してください：

1. [VOICEVOX公式サイト](https://voicevox.hiroshiba.jp/)からVOICEVOXをダウンロードしてインストール
2. VOICEVOXを起動し、APIサーバーを有効にする
3. PechaTalkを起動する際に `--mouth "voicevox"` オプションを指定

```bash
python cli.py --mouth "voicevox"
```

## トラブルシューティング

### 音声認識の問題

- マイクが正しく接続されていることを確認してください
- 静かな環境で使用してください
- 必要に応じて `ear.py` の `energy_threshold` や `hallucinate_threshold` を調整してください

### OpenAI APIの問題

- APIキーが正しく設定されていることを確認してください
- インターネット接続を確認してください
- APIの利用制限に達していないか確認してください

### VOICEVOXの問題

- VOICEVOXが起動していることを確認してください
- APIサーバーが有効になっていることを確認してください（デフォルトポート: 50021）
