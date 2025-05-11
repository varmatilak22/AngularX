import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Fix import for Pipeline
import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from Pipeline.llm_utils_local import query_llm_local

# Initialize
st.title("🤖 AngularX Chatbot")

model = SentenceTransformer('all-MiniLM-L6-v2')

# Set ChromaDB path (adjust as needed)
CHROMADB_PATH = os.path.join(ROOT_DIR, 'data_preprocessing', 'chroma_db')
client = chromadb.PersistentClient(path=CHROMADB_PATH)

collection = client.get_collection("angular_docs")

# Input query
user_query = st.text_input("Ask About Angular...")

if user_query:
    with st.spinner("Thinking..."):
        user_embeddings = model.encode([user_query])[0]
        results = collection.query(query_embeddings=[user_embeddings], n_results=3)
        all_context = []
        for doc_list in results['documents']:
            all_context.extend(doc_list)
        context = "\n\n".join(all_context)
        prompt = f"""You are a friendly and expert Angular assistant, specializing in Angular 19. Your goal is to help users with any Angular 19 questions they have, providing clear, concise, and easy-to-understand answers.

Make sure to always respond in a helpful, approachable, and supportive tone, as if you're guiding someone through their learning journey. Assume we are using Angular 19 unless stated otherwise, and always refer to the official Angular 19 documentation for your answers.

Feel free to offer additional tips, explain concepts in simpler terms, and give examples to make things clearer. Your responses should be friendly, engaging, and encouraging, helping users feel confident in their learning process.

Now, let’s dive in! How can I help you with Angular 19 today?

Context:
{context}

Question: {user_query}
Answer:"""
        response = query_llm_local(prompt)
        st.success(response)
