from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.corpus import CorpusCreate, CorpusOut
from app.schemas.search import SearchRequest
from app.cruds import corpus as corpus_crud
from app.services.algorithms import levenshtein, ngram
from app.core.deps import get_db

router = APIRouter()


@router.post("/upload_corpus", response_model=CorpusOut)
def upload_corpus(corpus: CorpusCreate, db: Session = Depends(get_db)):
    return corpus_crud.create_corpus(db, corpus)


@router.get("/corpuses", response_model=list[CorpusOut])
def get_all_corpuses(db: Session = Depends(get_db)):
    return corpus_crud.get_all_corpuses(db)


@router.post("/search_algorithm")
def search_word(request: SearchRequest, db: Session = Depends(get_db)):
    corpus = corpus_crud.get_corpus_by_id(db, request.corpus_id)
    if not corpus:
        raise HTTPException(status_code=404, detail="Corpus not found")
    words = corpus.text.split()
    results = []
    if request.algorithm == "levenshtein":
        results = [{"word": w,
                    "distance": levenshtein.levenshtein_distance(
                        request.word, w
                        )} for w in words]
        results = sorted(results, key=lambda x: x["distance"])
    elif request.algorithm == "ngram":
        results = [{"word": w,
                    "similarity": ngram.ngram_similarity(
                        request.word, w
                        )} for w in words]
        results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    else:
        raise HTTPException(status_code=400, detail="Unknown algorithm")
    return results[:5]
