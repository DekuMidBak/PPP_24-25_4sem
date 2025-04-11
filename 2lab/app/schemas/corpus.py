from pydantic import BaseModel


class CorpusCreate(BaseModel):
    corpus_name: str
    text: str


class CorpusOut(BaseModel):
    id: int
    corpus_name: str
    text: str

    class Config:
        orm_mode = True
