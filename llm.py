import os
import json
from openai import OpenAI
import streamlit as st

# from RAG import query_collection


def llm_client_setup():
    api_key = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment or secrets")
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    return client

def get_query_intent(client, query):
    """Extracts multiple metadata filters from the user query."""
    intent_prompt = f"""
    Analyze this user query: "{query}"
    Extract the following into a JSON object:
    1. search_query: The core subject (e.g., "weaving").
    2. max_cost: Numeric budget if mentioned, else null.
    3. location: City name if mentioned, else null.
    4. course_type: "In-person" or "Online" if mentioned, else null.
    
    Return ONLY valid JSON:
    {{"search_query": "string", "max_cost": number or null, "location": "string or null", "course_type": "string or null"}}
    """
    response = client.chat.completions.create(
        model="mistralai/ministral-3b-2512",
        messages=[{"role": "user", "content": intent_prompt}]
    )
    try:
        content = response.choices[0].message.content.strip().replace('```json', '').replace('```', '')
        return json.loads(content)
    except:
        return {"search_query": query, "max_cost": None, "location": None, "course_type": None}

def generate_response(client, query, collection):
    intent = get_query_intent(client, query)

    search_term = intent.get("search_query")
    if not search_term:
        search_term = query
    # --------------------------------------

    from RAG import query_collection
    retrieved_info = query_collection(
        collection,
        query=search_term,
        n_results=5
    )

    if not retrieved_info['documents'] or not retrieved_info['documents'][0]:
        if query.lower() in ["yes", "no", "yeah", "nope"]:
            return "Ooh, I see! 🐼 Was there a specific course or location you wanted to talk about? I'm ready to help!"
        return "Sorry, I couldn't find any courses matching those specific requirements."

    context = "\n---\n".join(retrieved_info['documents'][0])
    
    prompt = f"Based on the following course information:\n{context}\n\nAnswer the following question:\n{query}"
    
    response = client.chat.completions.create(
        model="mistralai/ministral-3b-2512",
        messages=[
            {"role": "system", "content": """You are Dando, a helpful panda recommending courses.
             Only recommend courses provided in the context. Speak in a friendly, whimsical manner.
             If the user says 'Yes' or 'No' without context, be helpful and ask what they are looking for.
             If the query is irrelevant, say 'Sorry, I cannot answer that question.'"""},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content