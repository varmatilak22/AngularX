<h1 align="center">AngularX Chatbot - AI-Powered Assistant for Learning Angular 19</h1>

<p align="center">
  <img src="https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/assets/icons/favicon.ico" alt="angularx-logo" width="120px" height="120px"/>
  <br>
  <em>AngularX uses Retrieval-Augmented Generation to deliver real-time, accurate answers from the latest Angular documentation.</em>
  <br>
</p>

<p align="center">
  <a href="https://github.com/varmatilak22/AngularX"><strong>GitHub Repository</strong></a>
  ·
  <a href="https://angularx-chatbot.streamlit.app">Live Demo</a>
  ·
  <a href="CONTRIBUTING.md">Contributing Guidelines</a>
  <br><br>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=for-the-badge"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=for-the-badge"/></a>
  <a href="https://img.shields.io/badge/Langchain-black?style=for-the-badge"><img alt="Langchain" src="https://img.shields.io/badge/Langchain-black?style=for-the-badge"/></a>
  <a href="https://img.shields.io/badge/Mistral-7B-blueviolet?style=for-the-badge"><img alt="Mistral-7B" src="https://img.shields.io/badge/Mistral-7B-blueviolet?style=for-the-badge"/></a>
  <a href="https://img.shields.io/badge/HuggingFace-FFB200?logo=huggingface&logoColor=black&style=for-the-badge"><img alt="HuggingFace" src="https://img.shields.io/badge/HuggingFace-FFB200?logo=huggingface&logoColor=black&style=for-the-badge"/></a>
  <a href="https://img.shields.io/badge/Firecrawl-FF4500?style=for-the-badge"><img alt="Firecrawl" src="https://img.shields.io/badge/Firecrawl-FF4500?style=for-the-badge"/></a>
  <a href="https://img.shields.io/badge/FAISS-003366?style=for-the-badge"><img alt="FAISS" src="https://img.shields.io/badge/FAISS-003366?style=for-the-badge"/></a>
  <a href="https://img.shields.io/badge/ChromaDB-00FF99?style=for-the-badge"><img alt="ChromaDB" src="https://img.shields.io/badge/ChromaDB-00FF99?style=for-the-badge"/></a>
  <a href="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge"/></a>
</p>

<hr>

## 📖 Overview

AngularX Chatbot is an AI-driven assistant that helps you **learn Angular 19** through an interactive chat interface. It leverages **RAG (Retrieval-Augmented Generation)** with **Langchain**, **Firecrawl**, and the **Mistral-7B Instruct** LLM to fetch and synthesize answers from the official Angular docs in real time.

---

## 🚀 Quickstart

### Prerequisites

- Python 3.10+  
- `git`  
- (Optional) Hugging Face API token for HF inference  

### Install & Run

```bash
git clone https://github.com/your-org/angularx-chatbot.git
cd angularx-chatbot
pip install -r requirements.txt
```
For Chromadb :
```bash
# Start the Streamlit app
streamlit run FrontEnd/chroma_main.py
```

For Faiss : 
```bash
# Start the Streamlit app
streamlit run FrontEnd/cfaiss_main.py
```
Visit [http://localhost:8501](http://localhost:8501) to interact with AngularX  and Deployed using Faiss script.

---

## 🛠️ Tech Stack

| Category             | Technologies                                               |
|----------------------|------------------------------------------------------------|
| **Languages**        | Python, HTML                                               |
| **Frontend & UI**    | Streamlit                                                  |
| **RAG & Orchestration** | Langchain, Firecrawl                                     |
| **LLM**              | Mistral-7B Instruct (via HF Inference or Mistral API)      |
| **Vector DB**        | FAISS, ChromaDB                                            |
| **Embeddings**       | Hugging Face SentenceTransformers                          |
| **Deployment**       | Streamlit Cloud                                            |

---

## 🧠 System Pipeline Overview

### 📥 Documentation Ingestion  
> **Tech Used:** Firecrawl, Langchain, Python  
- Crawls official Angular 19 docs and assets in real time  
- Cleans HTML pages, extracts code snippets & metadata  

### 🔍 Embedding & Vector Store  
> **Tech Used:** Sentence Transformers, FAISS, ChromaDB  
- Converts docs into vector embeddings for semantic search  
- Stores/retrieves embeddings from FAISS or ChromaDB  

### 🤖 Retrieval-Augmented Generation (RAG)  
> **Tech Used:** Langchain, Python, Vector DB  
- Performs similarity search on vector store  
- Concatenates top-k docs into prompt context for LLM  

### 💬 Inference & Chatbot Logic  
> **Variants Supported:**  
- **HF Inference Endpoint:** Mistral-7B via Hugging Face API  
- **Mistral AI API:** Direct calls to Mistral-hosted endpoint  
- **Local Container (future):** Self-hosted Mistral model  
- Applies prompt templates, post-processing for clarity  

### 🎨 User Interface  
> **Tech Used:** Streamlit  
- Interactive chat UI with message history  
- Syntax-highlighted Angular code snippets & links  
- Custom theming, code copy buttons, error feedback  

### 🚀 Deployment  
> **Tech Used:** Streamlit Cloud  
- One-click deploy on Streamlit Cloud
  
---

## 🚀 Technologies Explained

### 🔥 Firecrawl — *Doc Crawling*  
- Continuously syncs Angular docs & assets  
- Converts pages into JSON for downstream RAG  

### 🧩 Langchain — *Orchestration*  
- Manages ingestion pipelines, vector stores, agents  
- Simplifies prompt chaining and memory  

### 📦 FAISS / ChromaDB — *Vector Storage*  
- FAISS for in-memory speed, ChromaDB for persistence  
- Enables low-latency semantic searches  

### 🤖 Mistral-7B & HF API — *LLM Inference*  
- Uses highly capable instruct-tuned model  
- Options for hosted or self-managed endpoints  

### 🖥️ Streamlit — *Frontend*  
- Rapidly build and deploy interactive UIs  
- Easy customization of components and layouts  

---

## 🔮 Future Enhancements

- 🤖 **Langchain Agents:** Tool integration for live code execution  
- 📊 **Analytics Dashboard:** Sessions, token usage, drop-off rates  
- ⚡ **Local Inference Server:** vLLM or Text-Generation-WebUI  
- 🌐 **Multi-Framework Support:** React & Vue doc loaders  
- 📚 **Plugin Ecosystem:** Third-party plugins for Angular tooling  

---

## 👨‍💻 Author

**Tilak Varma**  
_AI Product Developer_

📧 [varmatilak22@example.com]  
🔗 [LinkedIn](https://www.linkedin.com/in/varmatilak) • [GitHub](https://github.com/varmatilak22)

---
