import streamlit as st
from components.file_and_file_downloader import component_file_and_file_downloader
import re

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"

def handle_event(value):
    st.header('Streamlit')
    st.write('Received from component: ', value)

def run_component(key,props):
    value = component_file_and_file_downloader(key=key  ,**props)
    return value

def remove_file_link_from_msg(msg):
    p = '\\[(.*?)\\]\\((.*?)\\s*(?:"(.*?)")?\\)'
    rr = re.findall(p, msg)
    remove_str = ""
    removed_msg = str(msg)
    for r in rr:
        a,b,c = r
        remove_str = "[" + a + "]" + "(" + b + ")"
        print(remove_str)
        removed_msg = removed_msg.replace(remove_str,"")
    return removed_msg


def gen_file_link(base_key,msg):
    p = '\\[(.*?)\\]\\((.*?)\\s*(?:"(.*?)")?\\)'
    rr = re.findall(p, msg)
    link_index = 0
    for r in rr:
        a,b,c = r
        props = {
                'test': b,
        }
        run_component(base_key + "_" +str(link_index),props)
        link_index = link_index + 1


class AI2:
    """A simple example class"""
    def __init__(self):
        None
        #if "count2" not in st.session_state:
        #    st.session_state.count2 = 0

    def disp_a2(self):
        st.header('ドキュメント比較・要約')
        st.write('kengen:' + st.session_state.kengen )

        user_msg = st.chat_input("ここにメッセージを入力")
        if user_msg:
            # 以前のチャットログを表示
            msg_index = 0
            for chat in st.session_state.chat_log:
                with st.chat_message(chat["name"]):
                    if (chat["name"] == ASSISTANT_NAME):
                        # ファイルリンク削除
                        disp_assistant_chat_msg = remove_file_link_from_msg(chat["msg"])
                        st.write(disp_assistant_chat_msg)
                        # ファイルリンク再生成
                        base_key = "b_" + str(msg_index) 
                        gen_file_link(base_key,chat["msg"])
                    else:
                        st.write(chat["msg"])

                msg_index = msg_index + 1


            # 最新のユーザーメッセージを表示
            with st.chat_message(USER_NAME):
                st.write(user_msg)

             # アシスタントのメッセージを表示
            with st.chat_message(ASSISTANT_NAME):
                assistant_msg = ""
                assistant_response_area = st.empty()
                assistant_msg = "Hi! " + user_msg + " [参考1](http://www.test.com/ssss.pdf)" + " [参考2](http://www.test.com/dddd.pdf) \n"

                # ファイルリンク部分削除
                disp_assistant_msg = remove_file_link_from_msg(assistant_msg)
                # 回答を逐次表示
                assistant_response_area.write(disp_assistant_msg)

                # ファイルリンク部分再生成
                msg_index = 0
                base_key = "a_" + str(msg_index)  
                gen_file_link(base_key,assistant_msg)


            # セッションにチャットログを追加
            st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
            st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})