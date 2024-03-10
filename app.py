import google.generativeai as gemini
import google.ai.generativelanguage as glm
import streamlit as st
import MeCab
import re

#Mecab init
mt = MeCab.Tagger()

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
        glm.Content(role="user", parts=[glm.Part(text="あなたは優秀なAIアシスタントです。3行以内で句読点多めかつ簡潔に回答してください。")]),
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

    node = mt.parseToNode(response.text)
    seisei = ""
    while node:
        word = node.feature.split(",")

        # get next node
        node = node.next

        print(word)
        if word[1] in "数詞":
            word_length = 1
        else:
            word_length = len(word[6])

        if word[0] in "BOS/EOS":
            continue
        if word[0] in "補助記号":
            seisei = seisei + "!　"
            continue
        if word_length % 2 > 0:
            seisei = seisei + "セ"
        for _ in range(int(word_length / 2)):
            seisei = seisei + "セイ"


    # Show response
    with st.chat_message("assistant"):
        st.markdown(seisei)

    # Add responce in chat log
    st.session_state["chat_history"].append({"role": "assistant", "content": seisei})


