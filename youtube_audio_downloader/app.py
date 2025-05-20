from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            output_path = 'downloads'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            file_path = audio_stream.download(output_path=output_path)
            base, ext = os.path.splitext(file_path)
            mp3_file = base + '.mp3'
            os.rename(file_path, mp3_file)
            return send_file(mp3_file, as_attachment=True)
        except Exception as e:
            return f"Erro: {e}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
