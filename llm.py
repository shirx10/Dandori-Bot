from openai import OpenAI
import streamlit as st
from RAG import query_collection

def llm_client_setup():
    client = OpenAI(api_key=st.secrets["OPENROUTER_API_KEY"],
                    base_url="https://openrouter.ai/api/v1")
    return client


def generate_response(client, query, collection):
    retrieved_info = query_collection(collection, query)
    context = retrieved_info['documents'][0]
    
    prompt = f"Based on the following course information:\n{context}\n\nAnswer the following question:\n{query}"
    
    response = client.chat.completions.create(
        model="mistralai/ministral-3b-2512",
        messages=[
            {"role": "system", "content": """ You are a chatbot recommending courses to users. 
             It is important that you only recommend courses that are in the provided context. 
             If a course is not in the context, do not recommend it.
             If the user's query cannot be answered with the provided course information or it is not relevant, respond with 'Sorry, I cannot answer that question.'
             You should speak to the user in a friendly and whimsical manner, providing clear and concise information about the courses, do not be verbose.
             """},
            {"role": "user", "content": prompt}
            ]
    )
    
    return response.choices[0].message.content