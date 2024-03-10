import google.generativeai as gemini
import google.ai.generativelanguage as glm
import streamlit as st
import MeCab

#Mecab init
mt = MeCab.Tagger("-Owakati")

# API key set
gemini.configure(api_key=st.secrets["API_KEY"])

# Title setting
st.set_page_config(
    page_title="SeiSei AI",
    page_icon="😎"
)

st.title("😎 SeiSei AI")

# Session init
if "chat_session" not in st.session_state :
    model = gemini.GenerativeModel("gemini-pro")
    st.session_state["chat_session"] = model.start_chat(history=[
        glm.Content(role="user", parts=[glm.Part(text="あなたは優秀なAIアシスタントです。3行以内で簡潔に回答してください。")]),
        glm.Content(role="model", parts=[glm.Part(text="わかりました。")])
    ])
    st.session_state["chat_history"] = []

# Show chat log all
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function after user input and send
if prompt := st.chat_input("ここに入力してください"):

    # Show user input
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user input in chat log
    st.session_state["chat_history"].append({"role": "user", "content": prompt})

    # Send message for Gemini Pro
    response = st.session_state["chat_session"].send_message(prompt)

    # Show response
    with st.chat_message("assistant"):
        st.markdown(response.text)


    # Add responce in chat log
    st.session_state["chat_history"].append({"role": "assistant", "content": response.text})


