import os
import pandas as pd
import streamlit as st
from google.cloud import firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
db = firestore.Client()

st.title("🏫 School of Dandori")
st.subheader("Course Catalog")

@st.cache_data 
def get_all_courses():
    docs = db.collection("courses").stream()
    return pd.DataFrame([doc.to_dict() for doc in docs])

df = get_all_courses()

search_query = st.text_input("Search for a course or professor:")

if search_query:
    filtered_df = df[df['Course_Title'].str.contains(search_query, case=False) | 
                     df['Instructor'].str.contains(search_query, case=False)]
    st.dataframe(filtered_df)
else:
    st.dataframe(df)