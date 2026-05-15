import os
import json
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document


#Setup paths
data_dir = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),"data_cleaning"),"clean_scraped_docs")  # <-- change to your actual folder

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
faiss_index_path=os.path.join(root_dir,"data_preprocessing",'faiss_index')

# Initalise SentenceTransformers Embeddings
embedding_model=SentenceTransformerEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#Load documents
docs=[]
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        try:
            with open(os.path.join(data_dir,filename),'r',encoding='utf-8') as f:
                data=json.load(f)
                
                content=f"{data['title']}\n{data['description']}\n{data['content']}"
                
                docs.append(Document(page_content=content,metadata={"source":filename}))
                print(f"✅ Loaded: {filename}")
        except Exception as e:
             print(f"❌ Error loading {filename}: {e}")

#Build FAISS index from documents
db=FAISS.from_documents(docs,embedding_model)

#Save FAISS index
db.save_local(faiss_index_path)
print("🚀 All files embedded and stored using LangChain FAISS!")