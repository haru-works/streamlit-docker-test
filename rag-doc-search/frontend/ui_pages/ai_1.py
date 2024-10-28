import streamlit as st

class AI1:
    """A simple example class"""
    def __init__(self):
        None

    def disp_a1(self):
        st.header('ドキュメント検索・要約')
        st.write('kengen:' + st.session_state.kengen )