from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.chat.router import router as chat_router
from app.config import settings
from app.database import create_tables, run_migrations
from app.documents.router import router as documents_router
from app.rag.embeddings import get_embeddings
from app.rag.reranker import load_reranker
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await run_migrations()
    get_embeddings()       # pre-warm FastEmbed model
    load_reranker()        # pre-warm cross-encoder (~85MB download on first run)
    yield


app = FastAPI(title="Employee Policy Chatbot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(users_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
