import os
import random

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from starlette.middleware.cors import CORSMiddleware

from api_models.models import Query, Answer, InformationSource

URL_MOCK_FILE_PATH = 'data/file1.txt'

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
    InformationSource(raw_content="aaaaa", title="Title just an A"),
    InformationSource(raw_content="bbbbb", title="Title just an B"),
    InformationSource(url="hasdhashdash", title="Now a Z"),
]


def mock_url_source_raw_content(url=None) -> str:
    try:
        return read_file(url)
    except:
        return read_file(URL_MOCK_FILE_PATH)


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def get_mapped_sources(sources: list[InformationSource]) -> list[InformationSource]:
    mapped_sources = []
    for source in sources:
        mocked_source = InformationSource(raw_content=mock_url_source_raw_content(source.url), url=source.url,
                                          title=source.title)
        mapped_sources.append(mocked_source)
    return mapped_sources


def get_text_chunks_langchain(text: str) -> list[Document]:
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs


@app.post("/query")
async def query(query: Query):
    print(f"Q: {query.question}.")
    if os.environ.get("ENV", None) == "fe_dev":
        return Answer(answer="42",
                      confidence=0.42,
                      sources=[
                          InformationSource(url="https://www.google.com", title="Google",
                                            raw_content="Last year COVID-19 kept us apart. This year we are finally together again."),
                          InformationSource(url="https://www.wikipedia.org", title="Wikipedia",
                                            raw_content="With a duty to one another to the American people to the Constitution.  And with an unwavering resolve that freedom will always triumph over tyranny."),
                          InformationSource(url=None, title="custom text",
                                            raw_content="America is moving. Moving forward. And we can't stop now.")
                      ])

    documents = []
    mapped_sources = get_mapped_sources(sources)
    print(f"Using sources: {mapped_sources}")
    for source in mapped_sources:
        documents.extend(get_text_chunks_langchain(source.raw_content))

    llm = OpenAI(temperature=0, model_name='text-davinci-003')
    # TODO: serialize the embeddings and/or docsearch to disk, consider pickle
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(documents, embeddings)

    prompt_template = """Answer in one sentence.

    {context}

    Question: {question}
    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(),
                                     chain_type_kwargs=chain_type_kwargs)

    result = qa({"query": query.question})
    result_str = result['result']
    print(f"Result: {result_str}")

    return Answer(answer=result_str, confidence=random.random(), sources=mapped_sources)


@app.post("/sources")
async def addSource(source: InformationSource):
    sources.append(source)
    return source


@app.get("/sources")
async def getSources() -> list[InformationSource]:
    return sources


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
