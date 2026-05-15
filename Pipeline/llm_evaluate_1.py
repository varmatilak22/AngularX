import os
import requests
import asyncio
import functools
from pydantic import PrivateAttr
from typing import List, Optional,ClassVar
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness # type: ignore
from ragas.dataset_schema import SingleTurnSample # type: ignore
import random
import time

load_dotenv()

class MistralChatModel(BaseChatModel):
    """LangChain BaseChatModel wrapper for Mistral API."""
    # Tell Pydantic not to treat these as fields:
    model_name: ClassVar[str]
    _api_key:    str               = PrivateAttr()
    _model:      str               = PrivateAttr()

    def __init__(self, model_name: str, api_key: Optional[str] = None):
        super().__init__()  # initialise BaseChatModel internals
        self._model   = model_name
        self._api_key = api_key or os.environ.get("MISTRAL_API_KEY") or ""
        if not self._api_key:
            raise ValueError("MISTRAL_API_KEY must be set.")

    @property
    def _llm_type(self) -> str:
        return "mistral_chat"

    @property
    def _identifying_params(self):
        return {"model": self._model}

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager=None
    ) -> ChatResult:
        payload = {
            "model": self._model,
            "messages": [
                {
                    "role": (
                        "system"    if isinstance(m, SystemMessage)
                        else "assistant" if isinstance(m, AIMessage)
                        else "user"
                    ),
                    "content": m.content
                }
                for m in messages
            ],
        }
        resp = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"]

        ai_msg = AIMessage(
            content=text,
            additional_kwargs={},
            response_metadata={},
            usage_metadata={"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        )
        gen = ChatGeneration(message=ai_msg)
        return ChatResult(generations=[gen])

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager=None
    ) -> ChatResult:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            functools.partial(self._generate, messages, stop, run_manager)
        )
        
# Instantiate the Mistral chat model (ensure MISTRAL_API_KEY is set in the environment)
mistral_model = MistralChatModel(model_name="mistral-large-latest")

# Load the FAISS vector store (assumes index files in "faiss_index" directory)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
root_dir         = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
faiss_index_path = os.path.join(root_dir, "data_preprocessing", "faiss_index")

vector_store = FAISS.load_local(
    faiss_index_path,
    embeddings,
    allow_dangerous_deserialization=True

)
from langchain.prompts import PromptTemplate

# prompt to generate new Angular questions from context
question_gen_prompt = PromptTemplate.from_template(
    "Generate a beginner-level Angular question about:\n\n{context}"
)

# placeholder reference (you can swap in real answers as needed)
DEFAULT_REFERENCE = "Please refer to the official Angular docs for the canonical answer."

samples = []
for i in range(100):
    # 1) pick a random doc chunk as seed
    seed = random.choice(vector_store.similarity_search("Angular overview", k=10)).page_content

    # 2) ask the model to craft a question
    q = mistral_model.invoke([
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content=question_gen_prompt.format(context=seed))
    ]).content.split("\n")[0].strip()
    if not q:
        continue

    # 3) retrieve top-2 contexts for that question
    docs = vector_store.similarity_search(q, k=2)
    contexts = [d.page_content for d in docs]

    # 4) get the model’s answer
    answer = mistral_model.invoke([
        SystemMessage(content="""You are a friendly and expert Angular assistant, specializing in Angular 19. Your goal is to help users with any Angular 19 questions they have, providing clear, concise, and easy-to-understand answers.

Make sure to always respond in a helpful, approachable, and supportive tone, as if you're guiding someone through their learning journey. Assume we are using Angular 19 unless stated otherwise, and always refer to the official Angular 19 documentation for your answers.

Feel free to offer additional tips, explain concepts in simpler terms, and give examples to make things clearer. Your responses should be friendly, engaging, and encouraging, helping users feel confident in their learning process."""),
        HumanMessage(content=f"{contexts[0]}\n\nQuestion: {q}")
    ]).content

    # 5) wrap into a SingleTurnSample
    samples.append(SingleTurnSample(
        user_input   = q,
        retrieved_contexts = contexts,
        response     = answer,
        reference    = DEFAULT_REFERENCE
    ))

    # small pause to avoid rate limits
    time.sleep(0.2)

# 6) evaluate all samples in batch
results = {}
for metric in [LLMContextRecall(), Faithfulness(), FactualCorrectness()]:
    # attach wrappers
    metric.llm        = LangchainLLMWrapper(mistral_model)
    metric.embeddings = embeddings

    # run async scoring over entire list
    scores = [asyncio.run(metric.single_turn_ascore(s)) for s in samples]
    results[metric.name] = sum(scores) / len(scores)

print("📊 RAGAS Evaluation (1,00 samples):")
for name, score in results.items():
    print(f" • {name}: {score:.3f}")
# Wrap the model with LangchainLLMWrapper for RAGAS integration (if needed)
evaluator_llm = LangchainLLMWrapper(mistral_model)
# The evaluator_llm can now be used with ragas.evaluate or other RAGAS functions.
