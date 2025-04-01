# PechaTalk

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

```bash
python cli.py
```

オプションで API キーを直接指定することもできます：

```bash
python cli.py --apikey "your_api_key_here"
```

その他のオプション：

```bash
python cli.py --recognizer "faster_wisper" --mouth "printer"
```
