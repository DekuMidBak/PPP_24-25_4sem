def ngram_similarity(word1: str, word2: str, n=2) -> float:
    def get_ngrams(word):
        return {word[i:i+n] for i in range(len(word)-n+1)}
    ngrams1 = get_ngrams(word1)
    ngrams2 = get_ngrams(word2)
    if not ngrams1 or not ngrams2:
        return 0.0
    return len(ngrams1 & ngrams2) / len(ngrams1 | ngrams2)
