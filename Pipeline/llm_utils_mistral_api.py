import requests
import time 
import streamlit as st

API_KEY=st.secrets["MISTRAL_API_KEY"]
API_URL='https://api.mistral.ai/v1/chat/completions'

HEADERS={
    "Authorization":f"Bearer {API_KEY}",
    "Content-Type":"application/json"
}

def query_mistral(prompt,max_tokens=10000,retries=3,delay=5):
    payload={
        "model":"mistral-large-latest",
        "messages":[
            {"role":"user",
             "content":prompt}
        ],
        "temperature":0.7,
        "max_tokens":max_tokens,
        
    }
    
    for attempt in range(retries):
        try:
            response=requests.post(API_URL,headers=HEADERS,json=payload)
            response.raise_for_status()
            
            return response.json()['choices'][0]['message']['content'].strip()
        
        except requests.exceptions.HTTPError as e:
            print(f"[Attempt {attempt+1}] HTTP Error :{e}")
        except requests.exceptions.Timeout:
            print(f"[Attempt {attempt+1}] Timeout Error")
        time.sleep(delay)
    
    return "The Server is currently Unavailable.Please Try again"