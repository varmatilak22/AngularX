import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN=os.getenv("HF_TOKEN")
API_URL='https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3'
HEADERS={"Authorization":f"Bearer {API_TOKEN}"}

def query_llm(prompt,max_tokens=1025,retries=3,delay=5):
    payload={
        "inputs":prompt,
        "parameters":{
            "max_new_tokens":max_tokens,
            "temperature":0.7,
            "return_full_text":False
        }
    }
    
    for attempt  in range(retries):
        try:
            response=requests.post(API_URL,headers=HEADERS,json=payload)
            response.raise_for_status()
            return response.json()[0]['generated_text'].strip()
        except requests.exceptions.HTTPError as e:
            print(f"[Attempt {attempt+1}] Http Error:{e}")
        except requests.exceptions.Timeout:
            print(f"[Attempt {attempt+1}] Timeout Error")
        time.sleep(delay)
    
    return " The Server is Currently Unavailable.Please try again later."