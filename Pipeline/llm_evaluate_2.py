import os
import random
import time
import requests
import asyncio
import functools
import re
from typing import List, Optional, ClassVar
from pydantic import PrivateAttr
from dotenv import load_dotenv
from requests.exceptions import HTTPError, ReadTimeout, ConnectionError

# LangChain-core imports
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.language_models.chat_models import BaseChatModel

# Embeddings & FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# RAGAS imports
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness
from ragas.dataset_schema import SingleTurnSample
load_dotenv()

# ——— Utility function to sanitize JSON strings ———
def sanitize_json_string(json_str):
    json_str = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', json_str)
    json_str = re.sub(r'\\(?=[^"\\/bfnrtu])', r'\\\\', json_str)
    return json_str

# ——— Mistral Chat Model ———
class MistralChatModel(BaseChatModel):
    model_name: ClassVar[str]
    _api_key:    str = PrivateAttr()
    _model:      str = PrivateAttr()

    def __init__(self, model_name: str, api_key: Optional[str] = None):
        super().__init__()
        self._model   = model_name
        self._api_key = api_key or os.environ.get("MISTRAL_API_KEY", "")
        if not self._api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is required")

    @property
    def _llm_type(self) -> str:
        return "mistral_chat"

    @property
    def _identifying_params(self):
        return {"model": self._model}

    def _generate(self, messages: List[BaseMessage], **kwargs) -> ChatResult:
        # synchronous version (you can keep or remove)
        payload = {
            "model": self._model,
            "messages": [
                {
                    "role": (
                        "system" if isinstance(m, SystemMessage)
                        else "assistant" if isinstance(m, AIMessage)
                        else "user"
                    ),
                    "content": m.content
                }
                for m in messages
            ]
        }
        max_retries = 5
        base_delay = 1.0
        max_delay = 30.0

        for attempt in range(max_retries):
            try:
                resp = requests.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=60
                )
                if resp.status_code == 429:
                    raise HTTPError("Rate limit hit", response=resp)
                resp.raise_for_status()

                raw_text = resp.json()["choices"][0]["message"]["content"]
                clean_text = sanitize_json_string(raw_text)

                ai_msg = AIMessage(
                    content=clean_text,
                    additional_kwargs={},
                    response_metadata={},
                    usage_metadata={"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
                )
                gen = ChatGeneration(message=ai_msg)
                return ChatResult(generations=[gen])

            except HTTPError as e:
                if resp.status_code == 429 and attempt < max_retries - 1:
                    delay = min(max_delay, base_delay * (2 ** attempt))
                    delay += delay * 0.1 * (2 * (random.random() - 0.5))
                    print(f"[Retry {attempt+1}/{max_retries}]: 429 Rate Limit hit, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
                else:
                    print(f"HTTP error: {e}, Status code: {resp.status_code}")
                    raise
            except (ReadTimeout, ConnectionError) as e:
                if attempt < max_retries - 1:
                    delay = 5
                    print(f"[Retry {attempt+1}/{max_retries}]: Network timeout/error, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
                else:
                    print(f"Network error: {e}")
                    raise
            except Exception as e:
                print(f"Unexpected error: {e}")
                raise

        raise Exception("Failed to get response from Mistral API after retries.")

    async def _agenerate(self, messages: List[BaseMessage], **kwargs) -> ChatResult:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(self._generate, messages))

# ——— Instantiate models, embeddings, FAISS, metrics ———
mistral = MistralChatModel("mistral-large-latest")
wrapped_llm = LangchainLLMWrapper(mistral)

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
faiss_idx = os.path.join(root, "data_preprocessing", "faiss_index")

vector_store = FAISS.load_local(faiss_idx, emb, allow_dangerous_deserialization=True)

metrics = [LLMContextRecall(), Faithfulness(), FactualCorrectness()]
for m in metrics:
    m.llm = wrapped_llm
    m.embeddings = emb

# ——— Async evaluation helper ———
async def evaluate_batch(samples):
    results = {}
    for m in metrics:
        total = 0.0
        for s in samples:
            score = await m.single_turn_ascore(s)
            total += score
        results[m.name] = total / len(samples) if samples else 0.0
    return results

# ——— Async main function ———
async def async_main():
    N = 20
    DEFAULT_REF = "See Angular 19 docs for the canonical answer."
    question_prompt = SystemMessage(content="Generate a beginner-level Angular question about the following context:")
    answer_with_prompt = SystemMessage(content="Answer using ONLY the given context:")
    answer_no_ctx_prompt = SystemMessage(content="Answer the question without any context:")

    samples_with = []
    samples_without = []

    for i in range(N):
        context = random.choice(vector_store.similarity_search("Angular overview", k=10)).page_content

        # Generate question (await API call)
        q = (await mistral._agenerate([
            question_prompt,
            HumanMessage(content=context)
        ])).generations[0].message.content.strip().split("\n")[0]
        if not q:
            continue

        # Retrieve top-2 contexts
        docs = vector_store.similarity_search(q, k=2)
        ctxs = [d.page_content for d in docs]

        # Answer with context
        aw = (await mistral._agenerate([
            answer_with_prompt,
            HumanMessage(content=f"{ctxs[0]}\n\nQuestion: {q}")
        ])).generations[0].message.content

        # Answer without context
        an = (await mistral._agenerate([
            answer_no_ctx_prompt,
            HumanMessage(content=q)
        ])).generations[0].message.content

        # Append samples
        samples_with.append(SingleTurnSample(
            user_input=q,
            retrieved_contexts=ctxs,
            response=aw,
            reference=DEFAULT_REF
        ))
        samples_without.append(SingleTurnSample(
            user_input=q,
            retrieved_contexts=[],
            response=an,
            reference=DEFAULT_REF
        ))

        print(f"Completed sample {i+1}")
        await asyncio.sleep(1)  # pause between requests

    # Evaluate
    res_no_ctx = await evaluate_batch(samples_without)
    res_with_ctx = await evaluate_batch(samples_with)

    # Print comparison
    print("Metric            No Context    With Context    Δ")
    print("-------------------------------------------------")
    for name in res_no_ctx:
        no = res_no_ctx[name]
        wi = res_with_ctx[name]
        print(f"{name:16s}  {no:>8.3f}      {wi:>8.3f}    {wi-no:>+8.3f}")

# ——— Run async main ———
if __name__ == "__main__":
    asyncio.run(async_main())
