import chromadb
import re

def client_setup():
    client = chromadb.Client()
    return client

# def collection_setup(client):
#     collection_name = "dandori_courses"
    
#     if collection_name in client.list_collections():
#         collection = client.get_collection(collection_name)
#     else:
#         collection = client.create_collection(name=collection_name)

#     return collection

def collection_setup(client):
    return client.get_or_create_collection(name="dandori_courses")
    
    collection = client.get_or_create_collection(name=collection_name)
    return collection

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


def embed_data(df, collection):

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

def query_collection(collection, query, n_results=5):
    pattern = r"£\s*(\d+(?:\.\d{1,2})?)"
    match = re.search(pattern, query)

    if match:
        cost_filter = float(match.group(1))
        query = re.sub(pattern, '', query).strip()
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"Cost": {"$lte": cost_filter}}
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
    return results
