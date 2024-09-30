import os

import streamlit as st
from openai import OpenAI

st.title("Trendio")

if "convs" not in st.session_state:
    st.session_state["convs"] = {}
if "cur_conv" not in st.session_state:
    st.session_state["cur_conv"] = ""
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])

if prompt := st.chat_input("Say something"):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=url)

    if not st.session_state.messages:
        st.session_state.cur_conv = prompt
        st.session_state.convs[prompt] = []

    st.chat_message("user", avatar=":material/face:").write(prompt)
    st.session_state.messages.append(
        {"role": "user", "avatar": ":material/face:", "content": prompt}
    )
    stream = client.chat.completions.create(
        model="qwen-turbo", messages=st.session_state.messages, stream=True
    )
    response = st.chat_message("assistant", avatar=":material/smart_toy:").write_stream(
        stream
    )
    st.session_state.messages.append(
        {"role": "assistant", "avatar": ":material/smart_toy:", "content": response}
    )


def new_conv():
    if st.session_state.messages:
        st.session_state.convs[st.session_state.cur_conv] = st.session_state.messages
    st.session_state["messages"] = []


def load_conv():
    if st.session_state.messages:
        st.session_state.convs[st.session_state.cur_conv] = st.session_state.messages
    st.session_state["messages"] = st.session_state.convs[st.session_state.selection]
    st.session_state["cur_conv"] = st.session_state.selection


with st.sidebar:
    st.header("Conversations")
    st.button(
        "New Conversation", on_click=new_conv, type="primary", use_container_width=True
    )
    st.sidebar.selectbox(
        "conversation",
        st.session_state.convs.keys(),
        label_visibility="collapsed",
        index=(
            list(st.session_state.convs).index(st.session_state.cur_conv)
            if len(st.session_state.convs) > 0
            else 0
        ),
        key="selection",
        on_change=load_conv,
    )
