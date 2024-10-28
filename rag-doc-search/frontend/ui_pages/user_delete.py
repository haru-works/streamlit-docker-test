import streamlit as st

class UD:
    """A simple example class"""
    def __init__(self):
        None

    def disp_ud(self):
        st.header('ユーザー削除')
        st.write('kengen:' + st.session_state.kengen )