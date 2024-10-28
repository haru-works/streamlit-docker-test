import streamlit as st

class DE:
    """A simple example class"""
    def __init__(self):
        None

    def disp_de(self):
        st.header('ドキュメント登録')
        st.write('kengen:' + st.session_state.kengen )