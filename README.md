# Text-to-Speech Converter

Azure OpenAI の TTS モデルを使用したテキスト読み上げウェブアプリケーションです。

## 機能

- テキストを音声に変換
- 6種類の異なる声から選択可能（Alloy, Echo, Fable, Onyx, Nova, Shimmer）
- 変換した音声をブラウザで再生
- 音声ファイルをMP3形式でダウンロード
- カスタムファイル名での保存に対応

## 技術スタック

- **バックエンド**: Flask (Python)
- **フロントエンド**: HTML, CSS, JavaScript
- **API**: Azure OpenAI API (TTS-1-HD モデル)

## インストール方法

1. リポジトリをクローン:
   ```
   git clone <リポジトリURL>
   cd tts
   ```

2. 依存関係をインストール:
   ```
   pip install -r requirements.txt
   ```

3. 環境変数の設定:
   プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の内容を設定:
   ```
   AZURE_OPENAI_ENDPOINT=<Azure OpenAI エンドポイントURL>
   AZURE_DEPLOYMENT_NAME=<デプロイメント名>
   AZURE_API_VERSION=<API バージョン>
   AZURE_API_KEY=<API キー>
   ```

## 使用方法

1. アプリケーションを起動:
   ```
   python app.py
   ```

2. ブラウザで以下のURLにアクセス:
   ```
   http://localhost:5001
   ```

3. テキスト入力欄に読み上げたいテキストを入力し、声を選択して変換ボタンをクリック

4. 変換後、ブラウザで音声を再生したり、MP3ファイルとしてダウンロードしたりできます

## 依存パッケージ

- Flask==2.3.2
- python-dotenv==0.21.0
- requests==2.28.1
- gunicorn==20.1.0
- flask-cors==3.0.10

## デプロイ

このアプリケーションは Heroku などのPaaSサービスへのデプロイに対応しています。
`Procfile` と `runtime.txt` がデプロイのために含まれています。

## 注意事項

- 一時的に生成された音声ファイルは `temp_audio` ディレクトリに保存されます
- Azure OpenAI APIには適切なアクセス権限が必要です
