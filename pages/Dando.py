import streamlit as st
from llm import llm_client_setup, generate_response

st.title("Dando the Helpful Panda 🐼")

# Initialize session state if not already done
if "df_dandori" not in st.session_state:
    st.error("Course data not loaded. Please go to the main page first.")
    st.stop()

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
        response = generate_response(client, user_query, st.session_state.collection)
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
