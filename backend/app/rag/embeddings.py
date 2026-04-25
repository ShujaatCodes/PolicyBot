from functools import lru_cache

from langchain_community.embeddings import FastEmbedEmbeddings


@lru_cache(maxsize=1)
def get_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
