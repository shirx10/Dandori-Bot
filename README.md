# 🐼 Dando the Helpful Panda: School of Dandori Bot

Welcome to the **School of Dandori**! This project is an end-to-end RAG (Retrieval-Augmented Generation) chatbot designed to help users navigate a catalog of 211+ courses through natural conversation. 

Dando isn't just a search bar; he is an intelligent assistant that understands intent, budget, and location, providing a whimsical and efficient user experience.

## 🚀 Key Features

* **Intelligent Intent Parsing:** Uses an LLM to "read between the lines." If a user asks for "classes under 150 pounds," the bot extracts the currency and numeric value to filter the database automatically.
* **Conversational Memory:** Powered by **Google Firestore**, Dando remembers who you are via a Session ID/UUID, allowing you to pick up your conversation exactly where you left off.
* **Semantic Search:** Utilizing **ChromaDB**, the bot doesn't just look for keywords—it understands the context of your query to find the most relevant course "scrolls."
* **Enterprise-Grade Security:** Implements **Google Cloud IAM** and Service Accounts to eliminate hardcoded passwords, ensuring a "Zero-Trust" security model.

## 🛠️ The £0 Tech Stack

This project was built to solve a technical challenge with a **£0 budget**, utilizing industry-leading free-tier technologies:

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based Web Framework)
* **Orchestration:** [Python](https://www.python.org/)
* **Database (Memory):** [Google Firestore](https://cloud.google.com/firestore)
* **Vector Store (Knowledge):** [ChromaDB](https://www.trychroma.com/)
* **LLM Gateway:** [OpenRouter](https://openrouter.ai/) (Accessing Mistral-7B/Ministral)
* **Cloud Security:** [Google Cloud IAM](https://cloud.google.com/iam)



## 🏗️ Data Engineering Pipeline

One of the core challenges was processing 211 inconsistent PDFs. Our pipeline solved this through:
1.  **Normalization:** Converting inconsistent casing (e.g., "pottery" vs "Pottery") into a clean Title Case format for UI filters.
2.  **Composite Keys:** Solving "Class_ID" collisions by merging IDs with Course Titles to ensure no data was overwritten during the cloud upload.
3.  **Fallback Extraction:** Using keyword-based logic when standard Regex patterns failed to capture Course Titles due to unique PDF layouts.



## 📋 How to Run Locally

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/dandori-bot.git](https://github.com/YOUR_USERNAME/dandori-bot.git)
cd dandori-bot

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Setup Secrets
Create a .streamlit/secrets.toml file or a .env file with your credentials:
OPENROUTER_API_KEY = "your_key_here"
# Add your Google Cloud Service Account JSON credentials here if required

### 4. Run the App
streamlit run pages/Dando.py
