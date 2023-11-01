'''
langserve
'''
from typing import List, Tuple

from fastapi import FastAPI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline # pylint: disable = no-name-in-module
from langchain.vectorstores import Chroma # pylint: disable = no-name-in-module
from langserve import add_routes
from pydantic import BaseModel, Field # pylint: disable = no-name-in-module
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

import uvicorn

# User input
class ChatHistory(BaseModel):
    """Chat history with the bot."""

    chat_history: List[Tuple[str, str]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "question"}},
    )
    question: str

if __name__ == "__main__":
    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs = {'device': 'cuda'}
        )

    vectorstore = Chroma(persist_directory='data/chroma', embedding_function=embedding_function)

    retriever = vectorstore.as_retriever()

    MODEL_ID="TheBloke/Llama-2-7b-Chat-GPTQ"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

    pipeline = pipeline(
        "text-generation",
        model=model, 
        tokenizer=tokenizer, 
        max_length=2048,
        temperature=0.1,
        do_sample=True,
        device=0,  # -1 for CPU
    )

    tokenizer.pad_token_id = model.config.eos_token_id

    llm = HuggingFacePipeline(
        pipeline=pipeline,
    )

    chain = ConversationalRetrievalChain.from_llm(llm, retriever).with_types(
        input_type=ChatHistory
    )

    app = FastAPI(
        title="LangChain Server",
        version="1.0",
        description="Spin up a simple api server using Langchain's Runnable interfaces",
    )

    # Adds routes to the app for using the chain under:
    # /invoke
    # /batch
    # /stream
    add_routes(app, chain)

    uvicorn.run(app, host="localhost", port=8000)
