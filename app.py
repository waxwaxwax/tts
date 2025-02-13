import os
import uuid
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory, abort
from dotenv import load_dotenv

# .env ファイルから環境変数をロード
load_dotenv()

app = Flask(__name__)

# 一時ファイルの保存先ディレクトリを設定（存在しない場合は作成）
TEMP_AUDIO_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "temp_audio")
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
app.config['TEMP_AUDIO_DIR'] = TEMP_AUDIO_DIR

# Azure OpenAI の設定（.env から取得）
azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_DEPLOYMENT_NAME")
api_version = os.environ.get("AZURE_API_VERSION")
api_key = os.environ.get("AZURE_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    data = request.get_json()
    text = data.get('text')
    voice = data.get('voice')

    # 必須パラメータのチェック
    if not text or not voice:
        return jsonify({"success": False, "message": "必要なパラメータが不足しています。"}), 400

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    request_data = {
        "model": "tts-1-hd",
        "input": text,
        "voice": voice
    }

    url = f"{azure_openai_endpoint}/openai/deployments/{deployment_name}/audio/speech?api-version={api_version}"
    response = requests.post(url, headers=headers, json=request_data)

    if response.status_code == 200:
        # 一意なファイルID（ファイル名）を生成して一時ディレクトリに保存
        file_id = f"{uuid.uuid4().hex}.mp3"
        temp_file_path = os.path.join(app.config['TEMP_AUDIO_DIR'], file_id)
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(response.content)

        app.logger.info(f"Generated audio file at: {temp_file_path}")
        # クライアントにはファイルIDのみ返す
        return jsonify({"success": True, "file_id": file_id})
    else:
        app.logger.error(f"Failed to generate audio: {response.text}")
        return jsonify({"success": False, "message": response.text}), response.status_code

@app.route('/download/<file_id>')
def download_file(file_id):
    # クエリパラメータからユーザーが指定したダウンロード用ファイル名（拡張子なし）を取得
    audio_name = request.args.get('audio_name', default=None, type=str)
    directory = app.config['TEMP_AUDIO_DIR']
    file_path = os.path.join(directory, file_id)

    if os.path.exists(file_path):
        # ユーザーが指定した名前に拡張子を付与（指定がなければファイルIDをそのまま使用）
        download_name = f"{audio_name}.mp3" if audio_name else file_id
        return send_from_directory(directory, file_id, as_attachment=True, download_name=download_name)
    else:
        app.logger.error(f"File not found: {file_path}")
        abort(404)

# 再生用エンドポイント（as_attachment=False で送信）
@app.route('/play/<file_id>')
def play_audio(file_id):
    directory = app.config['TEMP_AUDIO_DIR']
    file_path = os.path.join(directory, file_id)
    if os.path.exists(file_path):
        return send_from_directory(directory, file_id, as_attachment=False)
    else:
        app.logger.error(f"File not found: {file_path}")
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
