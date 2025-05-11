import chromadb
from chromadb.config import Settings
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt

#Step: 1 Connect to Chromadb
client=chromadb.PersistentClient(path='./chroma_db')

# Step:2 Load Collection
collection=client.get_collection('angular_docs')

#Step 3: Retrive data (you can increase limit as needed)
results=collection.get(include=['embeddings','documents','metadatas'],limit=50)

embeddings=np.array(results['embeddings'])
titles=[meta.get("title",f"id_{i}") for i,meta in enumerate(results['metadatas'])]

#step4: Dimensionaliy reduction using t-sne
tsne=TSNE(n_components=2,random_state=42,perplexity=15)
reduced_embeddings=tsne.fit_transform(embeddings)

#Step-5: Visualisation
plt.figure(figsize=(12,8))
plt.scatter(reduced_embeddings[:,0],reduced_embeddings[:,1],color='skyblue')

for i,label in enumerate(titles):
    plt.annotate(label,(reduced_embeddings[i,0],reduced_embeddings[i,1]),fontsize=8)

plt.title("t-SNE Visualisation of Angular Docs Embeddings")
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.grid(True)
plt.tight_layout()
plt.show()