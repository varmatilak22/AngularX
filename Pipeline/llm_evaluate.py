import os
import random
import time
import requests
import asyncio
import nest_asyncio
from typing import ClassVar

from pydantic import PrivateAttr
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import ChatResult, ChatGeneration, AIMessage
from langchain.chat_models.base import BaseChatModel

from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics.base import SingleTurnSample

# Allow nested event loops
nest_asyncio.apply()

# Load environment vars
load_dotenv()
API_URL = "https://api.mistral.ai/v1/chat/completions"
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set MISTRAL_API_KEY in your environment")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def query_mistral_raw(
    prompt: str,
    max_tokens: int = 2000,
    retries: int = 5,
    backoff: float = 2.0
) -> str:
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }
    for i in range(retries):
        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=(5, 30))
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
        if resp.status_code == 429:
            wait = backoff * (2 ** i)
            print(f"[429] Rate limited, waiting {wait:.1f}s…")
            time.sleep(wait)
            continue
        if resp.status_code == 401:
            raise RuntimeError("Unauthorized – check your MISTRAL_API_KEY")
        resp.raise_for_status()
    raise RuntimeError("Max retries exceeded for Mistral API.")

class MistralChatModel(BaseChatModel):
    """LangChain-compatible wrapper for Mistral with mutable temp & tokens."""
    model_name: ClassVar[str] = "mistral-large-latest"
    _temperature: float = PrivateAttr(0.7)
    _max_tokens: int   = PrivateAttr(2000)

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, t: float):
        self._temperature = t

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, m: int):
        self._max_tokens = m

    @property
    def _llm_type(self) -> str:
        return "mistral"

    def _generate(self, messages, stop=None, run_manager=None) -> ChatResult:
        prompt = "\n".join(m.content for m in messages)
        text = query_mistral_raw(prompt, max_tokens=self._max_tokens)
        # Provide both `text` and an `AIMessage`
        gen = ChatGeneration(
            text=text,
            generation_info={},
            message=AIMessage(content=text)
        )
        return ChatResult(generations=[[gen]], llm_output={})

    async def _agenerate(self, messages, stop=None, run_manager=None) -> ChatResult:
        return self._generate(messages, stop=stop, run_manager=run_manager)

# Wrap LLM & embeddings
wrapped_llm = LangchainLLMWrapper(langchain_llm=MistralChatModel())
hf_embed    = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
wrapped_emb = LangchainEmbeddingsWrapper(embeddings=hf_embed)

# Load FAISS index
root_dir         = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
faiss_index_path = os.path.join(root_dir, "data_preprocessing", "faiss_index")
db = FAISS.load_local(faiss_index_path, hf_embed, allow_dangerous_deserialization=True)

# Prepare prompt
question_prompt = PromptTemplate.from_template("Generate 3 beginner questions about:\n\n{content}")

# Generate synthetic QA pairs
questions, contexts = [], []
while len(questions) < 5:
    doc   = random.choice(db.similarity_search("Angular overview", k=200)).page_content
    raw_qs = query_mistral_raw(question_prompt.format(content=doc))
    for q in raw_qs.split("\n"):
        q = q.strip()
        if q and len(questions) < 5:
            questions.append(q)
            contexts.append([doc])
    time.sleep(0.5)

# Generate answers
answers = []
for q, ctx in zip(questions, contexts):
    prompt = (
        f"Context:\n{ctx[0]}\n\n"
        f"Question:\n{q}\n\n"
        "Answer in simple terms:"
    )
    answers.append(query_mistral_raw(prompt))
    time.sleep(0.5)

# Mock ground truths
ground_truths = ["Refer to Angular docs for the precise answer."] * len(questions)

# Attach LLM & embeddings to metrics
metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
for m in metrics:
    m.llm        = wrapped_llm
    m.embeddings = wrapped_emb

# Evaluate each sample via SingleTurnSample
nest_asyncio.apply()
loop    = asyncio.get_event_loop()
results = {}
for m in metrics:
    scores = []
    for q, ctx, ans, gt in zip(questions, contexts, answers, ground_truths):
        sample = SingleTurnSample(
            user_input   = q,
            contexts     = ctx,
            response     = ans,
            ground_truth = gt
        )
        score = loop.run_until_complete(m.single_turn_ascore(sample))
        scores.append(score)
    results[m.name] = sum(scores) / len(scores)

# Print results
print("📊 RAGAS Evaluation:")
for name, score in results.items():
    print(f"{name}: {score:.3f}")
