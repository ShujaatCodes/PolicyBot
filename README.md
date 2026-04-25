# PolicyBot — RAG Employee Policy Chatbot

An AI-powered chatbot that lets employees ask questions about company policies. Upload PDF policy documents and get instant, accurate answers grounded in those documents — with streaming responses and built-in protection against prompt injection and SQL injection attacks.

**Live Demo:**
- Frontend: https://policybot-frontend.vercel.app
- Backend: https://policybot-production-b8ea.up.railway.app

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy (async) |
| Database | PostgreSQL + pgvector + pg_trgm |
| Embeddings | FastEmbed (`BAAI/bge-small-en-v1.5`) |
| LLM | Groq (`llama-3.3-70b-versatile`) |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` (local, CPU) |
| Auth | JWT (python-jose + bcrypt) |
| Hosting | Railway (backend) + Vercel (frontend) |

---

## How It Works

```
PDF Upload
  → Extract text (pypdf)
  → Semantic chunking (LangChain SemanticChunker)
  → Embed chunks (FastEmbed)
  → Store vectors + full-text index (pgvector + pg_trgm)

User Question
  → Guardrails check (SQL injection, prompt injection, script injection)
  → Hybrid search: vector similarity + full-text (BM25) merged via RRF
  → Cross-encoder reranking (top-3 most relevant chunks)
  → Stream answer token-by-token via SSE (Groq LLM)
```

---

## Features

- **Multi-document support** — upload and manage multiple PDF policy documents independently
- **Hybrid search** — combines pgvector semantic search with pg_trgm full-text search via Reciprocal Rank Fusion
- **Cross-encoder reranking** — local `ms-marco-MiniLM-L-6-v2` model reranks candidates before answering
- **SSE streaming** — answers stream token-by-token for instant feedback
- **Guardrails** — blocks SQL injection, prompt injection, and script injection before they reach the LLM
- **Admin panel** — upload/delete documents, manage users
- **Chat interface** — natural language questions with markdown-formatted answers
- **JWT authentication** — role-based access (admin / employee)
- **Hidden admin registration** — `/register/admin` route exists but no UI link points to it

---

## Project Structure

```
rag-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point + lifespan
│   │   ├── config.py            # Environment config
│   │   ├── database.py          # Async DB engine + migrations
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── agent/               # LangGraph agent
│   │   │   ├── guardrails.py    # Injection/attack detection
│   │   │   └── graph.py         # guard → retrieve → generate pipeline
│   │   ├── auth/                # Register, login, JWT
│   │   ├── chat/                # SSE streaming endpoint
│   │   ├── documents/           # PDF upload + semantic chunking
│   │   ├── rag/                 # Hybrid search, reranker, LLM chain
│   │   └── users/               # User management (admin)
│   ├── tests/                   # 76 tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── pages/               # LoginPage, RegisterPage, ChatPage, AdminPage
    │   ├── components/          # ChatMessage, DocumentUpload, Layout
    │   ├── context/             # AuthContext
    │   └── api/                 # auth, chat, documents clients
    ├── vercel.json
    └── .env.production
```

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL with `pgvector` and `pg_trgm` extensions
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Fill in your values

uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

**Backend `.env`:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/policybot
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_secret_key
FRONTEND_URL=http://localhost:5173
```

**Frontend `.env.local`:**
```env
VITE_API_URL=http://localhost:8000
```

---

## Deployment

### Backend → Railway

1. Create a new Railway project and add a PostgreSQL service
2. Enable the `pgvector` extension on the database
3. Deploy from this repo — Railway detects the `Dockerfile` in `backend/`
4. Add environment variables in the Railway dashboard
5. Set the exposed port to `8080` under Settings → Networking
6. Generate a public domain

### Frontend → Vercel

1. Import the repo in the Vercel dashboard
2. Set the root directory to `frontend`
3. Add `VITE_API_URL=<your-railway-url>` as an environment variable

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new employee | Public |
| POST | `/auth/login` | Login, returns JWT | Public |
| GET | `/auth/me` | Get current user | User |
| GET | `/documents/status` | List uploaded documents | Admin |
| POST | `/documents/upload` | Upload PDF | Admin |
| DELETE | `/documents/{id}` | Delete document + chunks | Admin |
| POST | `/chat/` | Ask a question (non-streaming) | User |
| POST | `/chat/stream` | Ask a question (SSE streaming) | User |
| GET | `/users/` | List all users | Admin |
