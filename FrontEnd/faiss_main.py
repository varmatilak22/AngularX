import os
import sys
import uuid
import streamlit as st
import numpy as np
import time
import base64
import uuid
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings

os.environ["TRANSFORMERS_NO_TF"] = "1"

# Fix import for Pipeline
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from Pipeline.llm_utils_mistral_api import query_mistral

# --- Main Chat Interface ---
gif_path = os.path.join(ROOT_DIR, "assets", "angular_icon_gradient.gif")
logo_path=os.path.join(ROOT_DIR, "assets", "angular_icon_gradient-removebg-preview.png")
user_path=os.path.join(ROOT_DIR,"assets","user-removebg-preview.png")
assist_path=os.path.join(ROOT_DIR,"assets","assitant-removebg-preview.png")

with open(gif_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
with open(user_path, "rb") as f:
    b65 = base64.b64encode(f.read()).decode()
with open(assist_path, "rb") as f:
    b66 = base64.b64encode(f.read()).decode()

AVATAR_DATA_URL = f"data:image/gif;base64,{b64}"
USER_DATA_URL = f"data:image/gif;base64,{b65}"
ASSIST_DATA_URL = f"data:image/gif;base64,{b66}"

# Page config
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
st.set_page_config(page_title="AngularX Chatbot", page_icon=f"{logo_path}",layout="wide",initial_sidebar_state='expanded')

# Embedding model & FAISS index initialization
FAISS_INDEX_PATH = os.path.join(ROOT_DIR, 'data_preprocessing', 'faiss_index.index')

model =SentenceTransformerEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vectorstore=FAISS.load_local(FAISS_INDEX_PATH.replace(".index",""),model,allow_dangerous_deserialization=True)

retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":3})

# Initialize or load FAISS index
if os.path.exists(FAISS_INDEX_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
    print("FAISS index loaded.")
else:
    print("FAISS index not found. Please ensure the index is pre-created.")

# --- Session State Initialization ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}           # {chat_id: [(user_msg, bot_msg), ...]}
if "current_chat_id" not in st.session_state:
    # start with one empty chat
    new_id = str(uuid.uuid4())
    st.session_state.all_chats[new_id] = []
    st.session_state.current_chat_id = new_id

# --- Sidebar: Manage Chats ---
with st.sidebar:
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat_id = new_id
        st.rerun()
    # List saved chats
    for cid, history in st.session_state.all_chats.copy().items():
        title = history[-1][0] if history else "Untitled Chat"
        if len(title) > 30:
            title = title[:27] + "..."

        with st.expander(title):
            # Show prompts inside the expander
            for i, (prompt, _) in enumerate(history):
                st.markdown(f"**Prompt {i+1}:** {prompt}")

            # Side-by-side buttons
            col1, col2 = st.columns([0.5, 0.5])
            with col1:
                if st.button("🔁", key=f"select_{cid}"):
                    st.session_state.current_chat_id = cid
                    st.rerun()
            with col2:
                if st.button("❌", key=f"delete_{cid}"):
                    st.session_state.all_chats.pop(cid, None)
                    if st.session_state.current_chat_id == cid:
                        fallback = next(iter(st.session_state.all_chats), None)
                        if fallback:
                            st.session_state.current_chat_id = fallback
                        else:
                            new_id = str(uuid.uuid4())
                            st.session_state.all_chats[new_id] = []
                            st.session_state.current_chat_id = new_id
                    st.rerun()

st.markdown("""
<style>
section[data-testid="stSidebar"] > div {
    max-height: 90vh;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

header_html = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
*{{
   font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}
.angular-gradient-text {{
    font-size: 2.5rem;
    font-weight: 600;
    background: linear-gradient(90deg, #ff006a, #c800ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}}
</style>

<div style="display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #e0e0e0; justify-content: center; flex-direction: column;">
    <div style="display: flex;">
    <img src="{AVATAR_DATA_URL}" width="80" style="border-radius:8px; postion:relative;top:-8px;" />
    <h1 class="angular-gradient-text">AngularX</h1>
    </div>
    <p style="margin: 0; font-size: 0.9rem; color: #888; text-align:center;">Latest Angular 19 docs—indexed, retrieved, and ready for you.</p>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

current_id = st.session_state.current_chat_id
history = st.session_state.all_chats[current_id]

# Show welcome on brand new chat
if not history:
    with st.chat_message("assistant", avatar=ASSIST_DATA_URL):
        st.markdown(
    "<div style='font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;'>"
    "Hello! 👋 I'm your Angular 19 assistant. How can I help you today?"
    "</div>",
    unsafe_allow_html=True
)

# Render past messages
for user_msg, bot_msg in history:
    st.chat_message("user", avatar=USER_DATA_URL).markdown(
    f'<div style="font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif;">{user_msg}</div>',
    unsafe_allow_html=True
    ) 
    st.chat_message("assistant", avatar=ASSIST_DATA_URL).markdown(
    f'<div style="font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif;">{bot_msg}</div>',
    unsafe_allow_html=True
    )

# New user input
if prompt := st.chat_input("Ask about Angular..."):
    # Display user message
    st.chat_message("user", avatar=USER_DATA_URL).markdown(f'<div style="font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif;">{prompt}</div>',
     unsafe_allow_html=True)
    with st.spinner("Thinking..."):
        # Embed + retrieve context
        docs=retriever.get_relevant_documents(prompt)
        
        context = "\n\n".join([doc.page_content for doc in docs])

        full_prompt = f"""You are a friendly and expert Angular assistant, specializing in Angular 19. Your goal is to help users with any Angular 19 questions they have, providing clear, concise, and easy-to-understand answers.

Make sure to always respond in a helpful, approachable, and supportive tone, as if you're guiding someone through their learning journey. Assume we are using Angular 19 unless stated otherwise, and always refer to the official Angular 19 documentation for your answers.

Feel free to offer additional tips, explain concepts in simpler terms, and give examples to make things clearer. Your responses should be friendly, engaging, and encouraging, helping users feel confident in their learning process.

Context:
{context}

Question: {prompt}
Answer:"""
        response = query_mistral(full_prompt)
        chat = st.chat_message("assistant", avatar=ASSIST_DATA_URL)
        placeholder = chat.empty()
        displayed = ""
        # Split by lines to keep it sane for big blobs
        for char in response:
            displayed += char
            placeholder.markdown(
    f'<div style="font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif;">{displayed}</div>',
    unsafe_allow_html=True
)
            time.sleep(0.02) 

        # Save to history
        st.session_state.all_chats[current_id].append((prompt, response)) 
