# pythonのTags名を指定。
FROM python:3.11
# 処理を実行するフォルダ名を指定。
WORKDIR /frontend
# 実行環境にインストールする内容を記載したtxtファイルを実行フォルダにコピーする
COPY requirements.txt .
# requirements.txtで記載したミドルウェアのインストールの実行
RUN apt-get update && \
    apt-get -y upgrade && \
    pip install -r requirements.txt

EXPOSE 8501

COPY . .

CMD ["streamlit", "run","app.py","--server.port","8501"]