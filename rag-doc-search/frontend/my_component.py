import streamlit as st
from streamlit.components.v1 import html
from io import BytesIO
import base64

def pythonFunctionName(fileData):
  # ファイルデータをPDFに変換
  pdf_bytes = fileData.read() # バイナリデータとして読み込み
  pdf_buffer = BytesIO(pdf_bytes)

  # PDFをStreamlitに表示
  base64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
  pdf_display = st.markdown(f"""
  <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px">
  </iframe>
  """, unsafe_allow_html=True)

html("my_component.js")