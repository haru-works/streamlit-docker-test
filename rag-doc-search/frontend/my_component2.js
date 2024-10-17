import streamlit as st
from streamlit.components.v1 import html

def pythonFunctionName(fileData):
  # ファイルデータを処理する (ここでは処理を省略)
  st.write("ファイルがアップロードされました！")

html("my_component.js", args={"url": "https://example.com/api/file", "fileName": "downloaded_file.pdf"}) 
# Python側から引数を渡す