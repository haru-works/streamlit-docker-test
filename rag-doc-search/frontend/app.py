import streamlit as st

import ui_pages.ai_1 as a1
import ui_pages.ai_2 as a2
import ui_pages.docs_delete as dd
import ui_pages.docs_entry as de
import ui_pages.user_delete as ud
import ui_pages.user_entry as ue
import ui_pages.user_update as uu

#h = Hoge()  # この行でインスタンス化
#h.print_hoge()

ai1 = a1.AI1() 
ai2 = a2.AI2() 

idd = dd.DD() 
ide = de.DE() 
iud = ud.UD() 
iue = ue.UE() 
iuu = uu.UU() 

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
ai1_p = st.Page(ai1.disp_a1, title="ドキュメント検索・要約", icon="🔍", default=True)
ai2_P = st.Page(ai2.disp_a2, title="ドキュメント比較・要約", icon="📚")

# ユーザー設定
user_entry = st.Page(iue.disp_ue, title="ユーザー登録", icon="🪪")
user_delete = st.Page(iud.disp_ud, title="ユーザー削除", icon="🗑️")
user_update = st.Page(iuu.disp_uu, title="ユーザー更新", icon="🔄")

# ドキュメント設定
docs_entry = st.Page(ide.disp_de, title="ドキュメント登録", icon="📄")
docs_delete = st.Page(idd.disp_dd, title="ドキュメント削除", icon="🗑️")

if st.session_state.logged_in:

    if st.session_state.kengen == "管理者":   
        pg = st.navigation(
            {
                "ログイン/ログアウト": [logout_page],
                "AI画面": [ai1_p, ai2_P],
                "ドキュメント設定": [docs_entry, docs_delete],
                "ユーザー設定": [user_entry, user_delete,user_update],
            }
        )
    elif st.session_state.kengen == "一般":   
        pg = st.navigation(
            {
                "ログイン/ログアウト": [logout_page],
                "AI画面": [ai1_p, ai2_P],
            }
        )
    else:
        pg = st.navigation([login_page])

else:
    pg = st.navigation([login_page])

pg.run()