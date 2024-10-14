import streamlit as st
from datetime import datetime
import hashlib
import requests
import json
from components.file_and_directory_uploader import component_file_and_directory_uploader

if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'access_token' not in st.session_state:
    st.session_state.access_token = ""

if 'token_type' not in st.session_state:
    st.session_state.token_type = ""

if 'username' not in st.session_state:
    st.session_state.username = ""

def run_component(props):
    value = component_file_and_directory_uploader(key='file_and_directory_uploader_1', **props)
    return value


def handle_event(value):
    st.header('Streamlit')
    st.write('Received from component: ', value)


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False






def main():
    st.title("ログイン機能テスト")
    menu = ["ログイン","メイン","サインアップ"]
    choice = st.sidebar.selectbox("メニュー",menu)


    if choice == "ログイン":
        st.subheader("ログイン画面")
        username = st.text_input("ユーザー名を入力してください")
        password = st.text_input("パスワードを入力してください",type='password')
        if st.button("ログイン"):

            url = 'http://rag-doc-search-backend-1:8000/api/v1/login/access-token'
            #url = 'http://localhost:8000/api/v1/login/access-token'
            #url = 'http://localhost:8000/api/v1/login/access-token'


            form_data = {
                "grant_type":"password",
                "username": username,
                "password": password,
                "scope":"",
                "client_id":"string",
                "client_secret":"string"
            }

            response = requests.post(
                url,
                headers={"Accept": "application/json",
                         "Content-Type":"application/x-www-form-urlencoded"},
                data=form_data,
            )

            token = json.loads(response.text)

            if( response.status_code == 200 and token["access_token"] !=""):

                st.success("{}さんでログインしました".format(username))
                st.session_state.access_token = token["access_token"]
                st.session_state.token_type = token["token_type"]
                st.session_state.username = username

            else:
                st.warning("ユーザー名かパスワードが間違っています")
                st.session_state.access_token = ""
                st.session_state.token_type = ""
                st.session_state.username = ""

          
    elif choice == "メイン":

        if( st.session_state.username != "" and st.session_state.access_token !=""):
             
            st.subheader("メイン画面")
            st.success("{}さんでログイン中".format(st.session_state.username))
            st.session_state.counter = st.session_state.counter + 1

            collectionname = st.text_input("コレクション名を入力してください")

            props = {
                'counter': st.session_state.counter,
                'datetime': str(datetime.now().strftime("%H:%M:%S, %d %b %Y")),
                'username': str(st.session_state.username),
                'collectionname': str(collectionname),
                'access_token': str(st.session_state.access_token),
            }

            handle_event(run_component(props))

        else:
            st.warning("ログインしてください")
     

    elif choice == "サインアップ":
        st.subheader("新しいアカウントを作成します")
        username = st.text_input("ユーザー名を入力してください")
        password = st.text_input("パスワードを入力してください",type='password')
        repassword = st.text_input("再度パスワードを入力してください",type='password')
        if st.button("サインアップ"):
            st.success("アカウントの作成に成功しました")
            st.info("ログイン画面からログインしてください")


if __name__ == '__main__':
    main()
