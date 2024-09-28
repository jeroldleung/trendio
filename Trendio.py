import os

import streamlit as st
from openai import OpenAI

st.title("Trendio")

conversations = {}

if "conversations" not in st.session_state:
    st.session_state["conversations"] = []

if "current_conv" not in st.session_state:
    st.session_state["current_conv"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if prompt := st.chat_input("Say something"):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=url)

    if not st.session_state.messages:
        st.session_state.current_conv = prompt
        st.session_state.conversations.append(prompt)

    st.chat_message("user", avatar=":material/face:").write(prompt)
    st.session_state.messages.append(
        {
            "role": "user",
            "avatar": ":material/face:",
            "content": prompt,
        },
    )

    stream = client.chat.completions.create(
        model="qwen-turbo", messages=st.session_state.messages, stream=True
    )

    response = st.chat_message(
        "assistant", avatar=":material/smart_toy:"
    ).write_stream(stream)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "avatar": ":material/smart_toy:",
            "content": response,
        }
    )


def save_conversation():
    if st.session_state.messages:
        conversations[st.session_state.current_conv] = st.session_state.messages
        st.session_state["messages"] = []


def select_conversation():
    save_conversation()
    st.session_state.messages = conversations[st.session_state.current_conv]


st.sidebar.button(
    "New Conversation",
    on_click=save_conversation,
    type="primary",
    use_container_width=True,
)

st.sidebar.header("Chat History")

st.session_state.current_conv = st.sidebar.selectbox(
    "conversation",
    st.session_state.conversations,
    label_visibility="collapsed",
    index=len(st.session_state.conversations) - 1,
    on_change=select_conversation,
)
