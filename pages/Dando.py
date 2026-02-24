import streamlit as st
from llm import llm_client_setup, generate_response
from RAG import client_setup, collection_setup, embed_data

st.title("Dando the Helpful Panda 🐼")

@st.cache_resource
def setup_collection():
    client = client_setup()
    collection = collection_setup(client)
    embed_data(st.session_state.df_dandori, collection)
    return collection

collection = setup_collection()

@st.cache_resource
def setup():
    client = llm_client_setup()
    return client

client = setup()

user_query = st.chat_input("Ask about our courses:")

if "messages" not in st.session_state:
    st.session_state.messages = []


if user_query:
    with st.spinner("Generating response..."):
        st.session_state.messages.append({
            "role": "user", "content": user_query
            })
        response = generate_response(client, user_query, collection)
        st.session_state.messages.append({
            "role": "assistant", "content": response
            })

for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant",avatar="./Po_Profile_cropped.jpg").markdown(message["content"])

if st.session_state.messages:
    if st.button("New Chat"):
        st.session_state.messages = []
