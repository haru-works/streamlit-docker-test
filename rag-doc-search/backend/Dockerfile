# pythonのTags名を指定。
FROM python:3.10
# 処理を実行するフォルダ名を指定。
WORKDIR /backend
# 実行環境にインストールする内容を記載したtxtファイルを実行フォルダにコピーする
COPY requirements.txt .
# requirements.txtで記載したミドルウェアのインストールの実行
RUN apt-get update && \
    apt-get -y upgrade && \
    pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
