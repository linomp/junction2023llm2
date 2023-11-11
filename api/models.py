from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
    confidence: float
    sources: list[str]


class Query(BaseModel):
    value: str


class InformationSource(BaseModel):
    url: str | None
    title: str
    raw_content: str | None
