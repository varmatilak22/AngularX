import os
import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# 1. Load model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# 2. Setup ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("angular_docs")

# 3. Directory containing all JSON files
data_dir = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),"data_cleaning"),"clean_scraped_docs")  # <-- change to your actual folder

# 4. Loop through all files
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(data_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                content = f"{data['title']}\n{data['description']}\n{data['content']}"
                embedding = model.encode([content])[0]

                doc_id = os.path.splitext(filename)[0]  # Remove .json from filename

                collection.add(
                    documents=[content],
                    embeddings=[embedding.tolist()],
                    metadatas=[{
                        "title": data.get("title", ""),
                        "description": data.get("description", ""),
                        "url": data.get("sourceURL", "")
                    }],
                    ids=[doc_id]
                )
                print(f"✅ Added: {filename}")
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

# 5. Save DB
print("🚀 All files embedded and stored in ChromaDB!")