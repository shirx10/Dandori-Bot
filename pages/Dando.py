import uuid

import streamlit as st

from llm import llm_client_setup, generate_response
from RAG import client_setup, collection_setup, embed_data
from app import get_all_courses
from firestore import save_chat_message, get_chat_history

st.set_page_config(page_title="Dando the Panda", page_icon="🐼")
st.title("Dando the Helpful Panda 🐼")

# --- 1. INITIALIZE GLOBAL STATES ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# --- 2. SIDEBAR LOGIC ---
with st.sidebar:
    st.header("Chat Settings")
    
    # We use a key so we can track if the widget itself changed
    session_name = st.text_input(
        "Enter your name or session ID:", 
        value="", 
        placeholder="Enter your name...", 
        key="user_name_input"
    )
    
    # If the user typed something new, update the session and trigger a reload
    if session_name and st.session_state.get("current_user") != session_name:
        st.session_state.current_user = session_name
        st.session_state.session_id = session_name
        if "history_loaded" in st.session_state:
            del st.session_state.history_loaded

    st.info(f"Current Session: {st.session_state.session_id}")

    # --- THE FIXED BUTTON ---
    if st.button("New Chat / Clear History"):
        # 1. Clear the UI messages
        st.session_state.messages = []
        # 2. Block the database reload for this cycle
        st.session_state.history_loaded = True 
        # 3. Rotate the ID so new messages go to a fresh record
        st.session_state.session_id = str(uuid.uuid4())
        # 4. Force rerun to clear the screen
        st.rerun()

# --- 3. DATABASE HISTORY LOADING ---
# This block only runs once per session name change
if "history_loaded" not in st.session_state:
    if session_name:
        db_history = get_chat_history(st.session_state.session_id)
        st.session_state.messages = []
        for chat in db_history:
            st.session_state.messages.append({"role": "user", "content": chat["user"]})
            st.session_state.messages.append({"role": "assistant", "content": chat["bot"]})
    st.session_state.history_loaded = True

# --- 4. TOOL SETUP ---
@st.cache_resource
def setup_tools():
    v_client = client_setup()
    v_collection = collection_setup(v_client)
    df_internal = get_all_courses()
    embed_data(df_internal, v_collection)
    l_client = llm_client_setup()
    return v_collection, l_client

collection, client = setup_tools()

# --- 5. CHAT DISPLAY ---
# Use the custom avatar for Dando
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="./Po_Profile_cropped.jpg" if message["role"] == "assistant" else None,
    ):
        st.markdown(message["content"])

# --- 6. CHAT INPUT & RESPONSE ---
user_query = st.chat_input("Ask about our courses:")

if user_query:
      # Add user message to state and UI
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").markdown(user_query)

   # Generate response
    with st.chat_message("assistant", avatar="./Po_Profile_cropped.jpg"):
        with st.spinner("Dando is checking the scrolls..."):
            response = generate_response(client, user_query, collection)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

     # Save to Firestore
    save_chat_message(st.session_state.session_id, user_query, response)

# if st.sidebar.button("New Chat"):
#     st.session_state.messages = []
#     st.session_state.session_id = str(uuid.uuid4())
#     if "history_loaded" in st.session_state:
#         del st.session_state.history_loaded
#     st.rerun()
