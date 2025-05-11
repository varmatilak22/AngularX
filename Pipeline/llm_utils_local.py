from transformers import AutoModelForCausalLM,AutoTokenizer,GenerationConfig
import torch
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN=os.getenv('HF_TOKEN')

# 1. Load model and Tokenizer
model_name='mistralai/Mistral-7B-Instruct-v0.3'
tokenizer=AutoTokenizer.from_pretrained(model_name,
                                        use_auth_token=API_TOKEN)
model=AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map='auto',
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    use_auth_token=API_TOKEN
)
model.eval()

# 2. Define your local Inference function
def query_llm_local(prompt:str,
                    max_new_tokens:int=1025,
                    temperature:float=0.7,
                    retries:int=3,
                    delay:float=5):
    """
    Runs Text Generation locally on Mistral-7B-Instruct
    Retires on OOM or other inference Errors
    """
    #Prepare generation configuration
    gen_config=GenerationConfig(
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=True,
        return_dict_in_generate=True
    )
    
    for attempt in range(1,retries+1):
        try:
            #Tokenize Input
            inputs=tokenizer(prompt,return_tensors='pt').to(model.device)
            
            #Generate 
            outputs=model.generate(**inputs,generation_config=gen_config)
            
            #Decode only the new generated tokens
            generated=tokenizer.decode(outputs.sequences[0][inputs.input_ids.shape[-1]:],
                                       skip_special_tokens=True)
            
            return generated.strip()
        except RuntimeError as e:
            print(f"[Attempt {attempt}] Inference Error:{e}")
            torch.cuda.empty_cache()
        
        except Exception as e:
            print(f"[Attempt {attempt}] Unexpected Error: {e}")
        
        time.sleep(delay)
    
    return " The Model is currently unavailable.Please try again later"
            