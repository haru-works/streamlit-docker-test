import streamlit as st

class AI2:
    """A simple example class"""
    def __init__(self):
        None

    def disp_a2(self):
        st.header('ドキュメント比較・要約')
        st.write('kengen:' + st.session_state.kengen )