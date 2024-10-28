import streamlit as st

class UE:
    """A simple example class"""
    def __init__(self):
        None

    def disp_ue(self):
        st.header('ユーザー登録')
        st.write('kengen:' + st.session_state.kengen )