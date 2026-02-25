__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
import re

# def client_setup():
#     client = chromadb.Client()
#     return client

def client_setup():
    return chromadb.PersistentClient(path="./chroma_db")

def collection_setup(client):
    return client.get_or_create_collection(name="dandori_courses")
    
    # collection = client.get_or_create_collection(name=collection_name)
    # return collection

def build_document_text(row):
    return (
        f"Course Title: {row['Course_Title']}\n"
        f"Description: {row['Description']}\n"
        f"Skills Covered: {row['Skills']}\n"
        f"Instructor: {row['Instructor']}\n"
        f"Location: {row['Location']}"
    )

# def build_metadata(row):
#     return {
#         "course_title": row["Course_Title"],
#         "instructor": row["Instructor"],
#         "location": row["Location"],
#         "course_type": row["Course_Type"],
#         "cost": float(row["Cost"].replace('£', '')),
#         "class_id": row["Class_ID"],
#     }

def build_metadata(row):
    try:
        cost_val = float(str(row["Cost"]).replace('£', '').strip())
    except:
        cost_val = 0.0

    return {
        "course_title": row["Course_Title"],
        "instructor": row["Instructor"],
        "location": row["Location"],
        "course_type": row["Course_Type"],
        "cost": cost_val, 
        "class_id": row["Class_ID"],
    }

def query_collection(collection, query, n_results=5, filters=None):
    """Performs semantic search with multi-metadata filtering (AND logic)."""
    where_clauses = []

    if filters:
        if filters.get("max_cost") is not None:
            where_clauses.append({"cost": {"$lte": float(filters["max_cost"])}})
        
        if filters.get("location"):
            loc = filters["location"].strip().capitalize()
            where_clauses.append({"location": {"$eq": loc}})
        
        if filters.get("course_type"):
            where_clauses.append({"course_type": {"$eq": filters["course_type"]}})

    where_filter = None
    if len(where_clauses) > 1:
        where_filter = {"$and": where_clauses}
    elif len(where_clauses) == 1:
        where_filter = where_clauses[0]

    # Perform the query
    return collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter
    )

# def embed_data(df, collection):

#     documents, metadatas, ids = [], [], []

#     for idx, row in df.iterrows():
#         documents.append(build_document_text(row))
#         metadatas.append(build_metadata(row))
#         ids.append(f"{row['Class_ID']}_{row['Course_Title'].replace(' ', '_')}")

#     collection.add(
#         documents=documents,
#         metadatas=metadatas,
#         ids=ids
#     )

def embed_data(df, collection):
    if collection.count() == 0:
        documents, metadatas, ids = [], [], []

        for idx, row in df.iterrows():
            documents.append(build_document_text(row))
            metadatas.append(build_metadata(row))
            
            unique_id = f"{row['Class_ID']}_idx_{idx}" 
            ids.append(unique_id)

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

# def query_collection(collection, query, n_results=5):
#     pattern = r"£\s*(\d+(?:\.\d{1,2})?)"
#     match = re.search(pattern, query)

#     if match:
#         cost_filter = float(match.group(1))
#         query = re.sub(pattern, '', query).strip()
#         results = collection.query(
#             query_texts=[query],
#             n_results=n_results,
#             where={"Cost": {"$lte": cost_filter}}
#         )
#     else:
#         results = collection.query(
#             query_texts=[query],
#             n_results=n_results
#         )
#     return results
