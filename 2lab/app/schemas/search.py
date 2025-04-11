from pydantic import BaseModel


class SearchRequest(BaseModel):
    word: str
    algorithm: str  # "levenshtein" or "ngram"
    corpus_id: int
