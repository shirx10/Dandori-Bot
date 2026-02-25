import chromadb
import os
import pandas as pd
from google.cloud import firestore

DB_PATH = "./chroma_db"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./secrets/credentials.json"
db = firestore.Client()
 
def get_all_courses():
    docs = db.collection("courses").stream()
    return pd.DataFrame([doc.to_dict() for doc in docs])

df = get_all_courses()

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name="dandori_courses",
    metadata={"hnsw:space": "cosine"}  # use cosine similarity
)

def build_document_text(row):
    return (
        f"Course Title: {row['Course_Title']}\n"
        f"Description: {row['Description']}\n"
        f"Skills Covered: {row['Skills']}\n"
        f"Instructor: {row['Instructor']}\n"
        f"Location: {row['Location']}"
    )

def build_metadata(row):
    return {
        "course_title": row["Course_Title"],
        "instructor": row["Instructor"],
        "location": row["Location"],
        "course_type": row["Course_Type"],
        "cost": float(row["Cost"].replace('£', '')),
        "class_id": row["Class_ID"],
    }

documents, metadatas, ids = [], [], []

for idx, row in df.iterrows():
    documents.append(build_document_text(row))
    metadatas.append(build_metadata(row))
    ids.append(f"{row['Class_ID']}_{row['Course_Title'].replace(' ', '_')}")

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Collection '{collection.name}' now contains {collection.count()} documents.")