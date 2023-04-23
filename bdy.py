from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # Receba a URL do vídeo do formulário
    url = request.form['url']

    # Crie um objeto YouTube para a URL do vídeo
    yt = YouTube(url)

    # Obtenha a transmissão de vídeo com o formato mp4 e a maior resolução disponível
    stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()

    # Defina o diretório pai onde os vídeos serão salvos
    dir_path = r"/tmp"

    # Baixe a transmissão de vídeo selecionada para o diretório pai
    stream.download(dir_path)

    # Renomeie o arquivo de acordo com o título do vídeo
    title = yt.title.replace('/', '')
    os.rename(os.path.join(dir_path, stream.default_filename), os.path.join(dir_path, f'{title}.mp4'))

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False)
