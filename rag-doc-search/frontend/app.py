import streamlit as st

if "kengen" not in st.session_state:
    st.session_state.kengen = "一般"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.header('login')
    st.write('loginページ')

    kengen = st.text_input("入力してください")

    if st.button("Log in"):
        st.session_state.kengen = kengen
        st.session_state.logged_in = True
        st.rerun()

def logout():
    st.header('logout')
    st.write('logoutページ')

    if st.button("Log out"):
        st.session_state.kengen = ""
        st.session_state.logged_in = False
        st.rerun()

# ログイン/ログアウト
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# AI画面
ai_1 = st.Page("ui_pages/ai_1.py", title="ドキュメント検索・要約", icon="🔍", default=True)
ai_2 = st.Page("ui_pages/ai_2.py", title="ドキュメント比較・要約", icon="📚")

# ユーザー設定
user_entry = st.Page("ui_pages/user_entry.py", title="ユーザー登録", icon="🪪")
user_delete = st.Page("ui_pages/user_delete.py", title="ユーザー削除", icon="🗑️")
user_update = st.Page("ui_pages/user_update.py", title="ユーザー更新", icon="🔄")

# ドキュメント設定
docs_entry = st.Page("ui_pages/docs_entry.py", title="ドキュメント登録", icon="📄")
docs_delete = st.Page("ui_pages/docs_delete.py", title="ドキュメント削除", icon="🗑️")

if st.session_state.logged_in:

    if st.session_state.kengen == "管理者":   
        pg = st.navigation(
            {
                "ログイン/ログアウト": [logout_page],
                "AI画面": [ai_1, ai_2],
                "ドキュメント設定": [docs_entry, docs_delete],
                "ユーザー設定": [user_entry, user_delete,user_update],
            }
        )
    elif st.session_state.kengen == "一般":   
        pg = st.navigation(
            {
                "ログイン/ログアウト": [logout_page],
                "AI画面": [ai_1, ai_2],
            }
        )
    else:
        pg = st.navigation([login_page])

else:
    pg = st.navigation([login_page])

pg.run()