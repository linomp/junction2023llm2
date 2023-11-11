import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

from api_models.models import Query, Answer, InformationSource
import random
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

sources = [
    InformationSource(url="https://www.google.com", title="Google"),
    InformationSource(url="https://www.wikipedia.org", title="State of The Union")
]


@app.post("/query")
async def query(query: Query):
    print(f"Q: {query.question}")
    loader = TextLoader("../data/state_of_the_union_full.txt", encoding="utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # TODO: serialize the embeddings and/or docsearch to disk, consider pickle
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    prompt_template = """Answer in one sentence.

    {context}

    Question: {question}
    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(),
                                     chain_type_kwargs=chain_type_kwargs)

    res = qa.run(query.question)
    print(res)

    return Answer(answer=res, confidence=random.random(), sources=sources)


@app.post("/sources")
async def addSource(source: InformationSource):
    sources.append(source)
    return source


@app.get("/sources")
async def getSources() -> list[InformationSource]:
    return sources


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
