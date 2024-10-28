import streamlit as st

class DD:
    """A simple example class"""
    def __init__(self):
        None

    def disp_dd(self):
        st.header('ドキュメント削除')
        st.write('kengen:' + st.session_state.kengen )