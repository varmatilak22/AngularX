import os 
import json
from sklearn.feature_extraction.text import TfidfVectorizer


def generate_keywords(text, top_n=10):
    if not text.strip():
        return []
    
    # Basic TF-IDF approach
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    keywords = [word for word, score in sorted_scores[:top_n]]
    return keywords

# Step-1 Current Dir path
current_path=os.getcwd()
print(current_path)

#Step-2 Parent dir path
parent_path=os.path.dirname(current_path)
print(parent_path)

#Step-3 Inside Scrap docs
target_folder=os.path.join(parent_path,'data_extraction')
print(target_folder)

#step-4 -target is raw scarp docs dir

source_dir=os.path.join(target_folder,'raw_scraped_docs')
print(source_dir)


destination_dir=os.path.join(current_path,'clean_scraped_docs')
print(destination_dir)

os.makedirs(destination_dir,exist_ok=True)

# Looping each file name in source dir 
count=1
for filename in os.listdir(source_dir):
    count+=1
    if filename.endswith(".json"):
        # Each file path from source dir
        source_file_path=os.path.join(source_dir,filename)

        #Reading each file 
        with open(source_file_path,'r',encoding='utf-8') as f:
            data=json.load(f)
        

        content=data.get("data",{}).get("markdown","").replace("\\n","\n")
        title=data.get("metadata",{}).get("title")
        description=data.get("metadata", {}).get("description", "")
        keywords=data.get("metadata",{}).get("keywords")

        if not keywords or keywords==None:
            keywords = generate_keywords(content)
        
        #Cleanning the json
        cleaned_data={
            "content":content,
            "title":title,
            "description":description,
            "keywords":keywords,
            "sourceURL":data.get("sourceURL")

        }

        #Desitionaton file path
        destination_file_path=os.path.join(destination_dir,filename)

        #Saving cleaned files in desination folder with exact name in source dir 
        with open(destination_file_path,'w',encoding='utf-8') as f:
            json.dump(cleaned_data,f,indent=2)
        
        print(f"✅ Cleaned and saved: {filename}")
print("\n All files cleaned and saved successfully!")
print(count)
        
