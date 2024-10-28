import streamlit as st
class UU:
    """A simple example class"""
    def __init__(self):
        None

    def disp_uu(self):
        st.header('ユーザー更新')
        st.write('kengen:' + st.session_state.kengen )