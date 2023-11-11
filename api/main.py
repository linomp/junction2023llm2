import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_models.models import Query, InformationSource, Answer
from utils import get_mocked_answer, get_answer

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
    InformationSource(url="data/file1.txt", title="File about Steve's location"),
]


@app.post("/query")
async def query(query: Query):
    print(f"Q: {query.question}.")
    if os.environ.get("ENV", None) == "fe_dev":
        return get_mocked_answer(query)

    core_model_answer = get_answer(sources, query)

    print(f"Q: {core_model_answer.question}")
    print(f"A: {core_model_answer.answer}")
    print(f"Sources: {core_model_answer.sources}")

    return Answer.from_core_model_answer(core_model_answer)


@app.post("/sources")
async def add_source(source: InformationSource):
    sources.append(source)
    return source


@app.get("/sources")
async def get_sources() -> list[InformationSource]:
    return sources


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
