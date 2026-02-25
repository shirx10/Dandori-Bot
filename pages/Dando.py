import uuid

import streamlit as st

from llm import llm_client_setup, generate_response
from RAG import client_setup, collection_setup, embed_data
from app import get_all_courses
from firestore import save_chat_message, get_chat_history

st.title("Dando the Helpful Panda 🐼")

with st.sidebar:
    session_name = st.text_input("Enter your name or session ID:", value="Arthur_Test")

    if st.session_state.get("session_id") != session_name:
        st.session_state.session_id = session_name
        if "history_loaded" in st.session_state:
            del st.session_state.history_loaded

# OLD CODE - COMMENTED OUT FOR COMPARISON
# import chromadb
# DB_PATH = "./chroma_db"
#
# @st.cache_resource
# def load_collection():
#     client = chromadb.PersistentClient(path=DB_PATH)
#     collection = client.get_collection(name="dandori_courses")
#     return collection
#
# st.session_state.collection = load_collection()

# if "df_dandori" not in st.session_state:
#     with st.spinner("Connecting to School of Dandori database..."):
#         st.session_state.df_dandori = get_all_courses()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state or "history_loaded" not in st.session_state:
    db_history = get_chat_history(st.session_state.session_id)
    st.session_state.messages = []
    for chat in db_history:
        st.session_state.messages.append({"role": "user", "content": chat["user"]})
        st.session_state.messages.append({"role": "assistant", "content": chat["bot"]})
    st.session_state.history_loaded = True


@st.cache_resource
def setup_tools():
    v_client = client_setup()
    v_collection = collection_setup(v_client)

    df_internal = get_all_courses()
    embed_data(df_internal, v_collection)

    l_client = llm_client_setup()
    return v_collection, l_client


collection, client = setup_tools()

# OLD CODE - COMMENTED OUT FOR COMPARISON
# @st.cache_resource
# def setup():
#     client = llm_client_setup()
#     return client
#
# client = setup()

for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="./Po_Profile_cropped.jpg" if message["role"] == "assistant" else None,
    ):
        st.markdown(message["content"])

user_query = st.chat_input("Ask about our courses:")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").markdown(user_query)

    with st.spinner("Dando is checking the scrolls..."):
        response = generate_response(client, user_query, collection)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="./Po_Profile_cropped.jpg"):
            st.markdown(response)

        save_chat_message(st.session_state.session_id, user_query, response)

if st.sidebar.button("New Chat"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    if "history_loaded" in st.session_state:
        del st.session_state.history_loaded
    st.rerun()
