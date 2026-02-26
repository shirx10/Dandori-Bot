import datetime
import os

import pandas as pd
import streamlit as st
from google.cloud import firestore, secretmanager

def get_firestore_client():
    """Get Firestore client with credentials from Secret Manager or local file."""
    try:
        # Try to get from Secret Manager (Cloud Run)
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.environ.get("GCP_PROJECT_ID")
        if project_id:
            name = f"projects/{project_id}/secrets/google-credentials/versions/latest"
            response = client.access_secret_version(request={"name": name})
            creds_json = response.payload.data.decode("UTF-8")
            with open("/tmp/credentials.json", "w", encoding="utf-8") as f:
                f.write(creds_json)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/credentials.json"
    except Exception:
        # Fallback to local credentials
        if os.path.exists("./secrets/credentials.json"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./secrets/credentials.json"
        elif os.path.exists("credentials.json"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

    return firestore.Client()


db = get_firestore_client()

def save_chat_message(session_id, user_query, bot_response):
    chat_ref = db.collection("chat_sessions").document(session_id)

    chat_ref.set({
        "messages": firestore.ArrayUnion([{
            "user": user_query,
            "bot": bot_response,
            "timestamp": datetime.datetime.now().isoformat()
        }])
    }, merge = True)

def get_chat_history(session_id):
    doc = db.collection("chat_sessions").document(session_id).get()
    if doc.exists:
        return doc.to_dict().get("messages", [])
    return []

@st.cache_data 
def get_all_courses():
    docs = db.collection("courses").stream()
    return pd.DataFrame([doc.to_dict() for doc in docs])