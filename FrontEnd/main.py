import os
import sys
import streamlit as st
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Fix import for Pipeline
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from Pipeline.llm_utils_mistral_api import query_mistral

# Set environment and page config
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
st.set_page_config(page_title="AngularX Chatbot", page_icon="🤖")

st.title("🤖 AngularX Chatbot")

# Initialize embedding model and DB
model = SentenceTransformer('all-MiniLM-L6-v2')
CHROMADB_PATH = os.path.join(ROOT_DIR, 'data_preprocessing', 'chroma_db')
client = chromadb.PersistentClient(path=CHROMADB_PATH)
collection = client.get_collection("angular_docs")

# Session state for chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat UI with input box
with st.chat_message("assistant"):
    st.markdown("Hello! 👋 I'm your Angular 19 assistant. Ask me anything about Angular!")

user_input = st.chat_input("Ask about Angular...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)

    with st.spinner("Thinking..."):
        # Embed query and search ChromaDB
        user_embedding = model.encode([user_input])[0]
        results = collection.query(query_embeddings=[user_embedding], n_results=3)
        all_context = []
        for doc_list in results['documents']:
            all_context.extend(doc_list)
        context = "\n\n".join(all_context)

        # Build the prompt
        prompt = f"""You are a friendly and expert Angular assistant, specializing in Angular 19. Your goal is to help users with any Angular 19 questions they have, providing clear, concise, and easy-to-understand answers.

Make sure to always respond in a helpful, approachable, and supportive tone, as if you're guiding someone through their learning journey. Assume we are using Angular 19 unless stated otherwise, and always refer to the official Angular 19 documentation for your answers.

Feel free to offer additional tips, explain concepts in simpler terms, and give examples to make things clearer. Your responses should be friendly, engaging, and encouraging, helping users feel confident in their learning process.

Context:
{context}

Question: {user_input}
Answer:"""

        # Get LLM response
        bot_response = query_mistral(prompt)

        # Save and display bot response
        st.session_state.chat_history.append((user_input, bot_response))
        st.chat_message("assistant").markdown(bot_response)

# Show previous conversation history
for user_msg, bot_msg in st.session_state.chat_history:
    st.chat_message("user").markdown(user_msg)
    st.chat_message("assistant").markdown(bot_msg)
