import os

import streamlit as st
from openai import OpenAI

st.title("Trendio")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Say something"):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=url)
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    stream = client.chat.completions.create(
        model="qwen-turbo", messages=st.session_state.messages, stream=True
    )
    response = st.chat_message("assistant").write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
