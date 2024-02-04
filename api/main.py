import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_models.models import Query, InformationSource, Answer
from utils import get_mocked_answer, get_answer, init_embeddings

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
    InformationSource(url="data/reforms.txt", title="yle.fi - EU carbon market reform impacts Finnish steel industry"),
    InformationSource(url="data/mining.txt",
                      title="ScienceDirect - Europe's mining innovation trends"),
    InformationSource(url="data/sdgs.txt",
                      title="ScienceDirect - The innovative contribution of multinational enterprises to the Sustainable Development Goals"),
    InformationSource(url="data/digitalization.txt",
                      title="ScienceDirect- Digitalisation trends in the mining industry"),
    InformationSource(url="data/sustainability.txt",
                      title="Springer - Impact of minerals policy on sustainable development of mining sector – a comparative assessment of selected EU countries"),
]

chroma = init_embeddings(sources)


@app.post("/query")
async def query(query: Query):
    print(f"Q: {query.question}.")
    if os.environ.get("ENV", None) == "fe_dev":
        return get_mocked_answer(query)

    core_model_answer = get_answer(sources, query, chroma)

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
