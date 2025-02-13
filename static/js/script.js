document.getElementById('ttsForm').addEventListener('submit', function (event) {
    event.preventDefault();
  
    // 入力値の取得
    const text = document.getElementById('text').value;
    const voice = document.getElementById('voice').value;
  
    // プログレスバーの初期化・表示
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressBar.textContent = '0%';
  
    // 変換リクエストを送信
    fetch('/convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text,
        voice: voice
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        progressBar.style.width = '100%';
        progressBar.textContent = '100%';
  
        const fileId = data.file_id; // サーバ側で生成された一意のファイルID
        const resultElement = document.getElementById('result');
        resultElement.innerHTML = `
          <p>読み上げが完了しました。</p>
          <!-- 再生用audioタグ（非表示またはcontrolsを付けず、再生ボタンで制御） -->
          <audio id="audioPlayer" src="/play/${encodeURIComponent(fileId)}"></audio>
          <!-- 再生ボタン -->
          <button id="playButton">再生</button>
          <br><br>
          <p>この音声をmp3ファイルとしてダウンロードできます。</p>
          <label for="downloadFileName">ファイル名:</label>
          <input type="text" id="downloadFileName" placeholder="ファイル名を入力 (拡張子不要)" />
          <button id="downloadButton">ダウンロード</button>
        `;
  
        // 再生ボタンのイベントリスナー
        document.getElementById('playButton').addEventListener('click', function () {
          const audio = document.getElementById('audioPlayer');
          audio.play();
        });
  
        // ダウンロードボタンのイベントリスナー
        document.getElementById('downloadButton').addEventListener('click', function () {
          const fileName = document.getElementById('downloadFileName').value.trim();
          if (!fileName) {
            alert("ファイル名を入力してください。");
            return;
          }
          // ダウンロード用エンドポイントへリダイレクト
          window.location.href = `/download/${encodeURIComponent(fileId)}?audio_name=${encodeURIComponent(fileName)}`;
        });
      } else {
        document.getElementById('result').textContent = `Error: ${data.message}`;
      }
    })
    .catch(error => {
      document.getElementById('result').textContent = `Error: ${error.message}`;
    });
  });
  
  // 文字数カウントの更新
  document.getElementById('text').addEventListener('input', function () {
    const charCount = this.value.length;
    document.getElementById('charCount').textContent = `Characters: ${charCount}`;
  });
  