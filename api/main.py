import uvicorn
from fastapi import FastAPI

from api.models import Query, Answer, InformationSource

app = FastAPI()

sources = []


@app.post("/query")
async def query(query: Query):
    print(query.value)
    return Answer(answer="42", confidence=0.42, sources=["The answer is always 42"])


@app.post("/sources")
async def addSource(source: InformationSource):
    sources.append(source)
    return source


@app.get("/sources")
async def getSources() -> list[InformationSource]:
    return sources


if __name__ == "main":
    uvicorn.run(app, host="0.0.0.0", port=8000)
