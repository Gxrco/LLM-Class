from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
from typing import Set

st.header("Python 🐍 - Documentation Helper Bot")
st.write("Welcome to the Python 🐍 - Documentation Helper Bot! This bot is designed to help you find answers to your Python questions. This project was made by Gerson Ramírez (Gerco)")
prompt = st.text_input("Prompt", placeholder="Enter your prompt here")

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    source_list = list(source_urls)
    source_list.sort()
    sources_string = "sources: \n"
    for i, source in enumerate(source_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

        sources = set(doc.metadata["source"] for doc in generated_response["source"])

        formatted_response = (
            f"{generated_response['result']}\n\n{create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

if st.session_state["chat_answers_history"]:
    for user_query, generated_response in zip(st.session_state["user_prompt_history"],
                                              st.session_state["chat_answers_history"]):
        message(user_query, is_user=True)
        message(generated_response)
