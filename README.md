# PolicyBot — RAG Employee Policy Chatbot

An AI-powered chatbot that lets employees ask questions about company policies. Upload PDF policy documents and get instant, accurate answers grounded in those documents.

**Live Demo:**
- Frontend: https://policybot-frontend.vercel.app
- Backend: https://policybot-production-b8ea.up.railway.app

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy (async) |
| Database | PostgreSQL + pgvector |
| Embeddings | FastEmbed (`BAAI/bge-small-en-v1.5`) |
| LLM | Groq (`llama-3.3-70b-versatile`) |
| Auth | JWT (python-jose + bcrypt) |
| Hosting | Railway (backend) + Vercel (frontend) |

---

## How It Works

```
PDF Upload
  → Extract text (pypdf)
  → Split into chunks (LangChain RecursiveCharacterTextSplitter)
  → Embed chunks (FastEmbed)
  → Store vectors (pgvector)

User Question
  → Embed question (FastEmbed)
  → Find top-4 similar chunks (pgvector similarity search)
  → Send chunks + question to Groq LLM
  → Return grounded answer
```

---

## Features

- **Admin panel** — upload and manage PDF policy documents, manage users
- **Chat interface** — ask questions in natural language, get answers with source grounding
- **JWT authentication** — role-based access (admin / user)
- **Persistent chat history** — all conversations saved to PostgreSQL

---

## Project Structure

```
rag-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── config.py         # Environment config
│   │   ├── database.py       # Async DB engine + session
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── auth/             # Register, login, JWT
│   │   ├── chat/             # Chat endpoint + RAG pipeline
│   │   ├── documents/        # PDF upload + processing
│   │   ├── rag/              # Embeddings, vectorstore, LLM chain
│   │   └── users/            # User management (admin)
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── pages/            # LoginPage, ChatPage, AdminPage
    │   ├── components/       # ChatMessage, DocumentUpload, UserTable
    │   ├── context/          # AuthContext
    │   └── api/              # API service classes
    ├── vercel.json
    └── .env.production
```

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL with pgvector extension
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
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

1. Create a new Railway project
2. Add a PostgreSQL service and enable the pgvector extension
3. Deploy from this repo, set root directory to `backend`
4. Add environment variables in Railway dashboard
5. Generate a public domain under Settings → Networking

### Frontend → Vercel

1. Run `vercel --prod` from the `frontend` directory
2. Or import the repo in the Vercel dashboard with root directory set to `frontend`

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | Public |
| POST | `/auth/login` | Login, returns JWT | Public |
| GET | `/documents/` | List all documents | Admin |
| POST | `/documents/upload` | Upload PDF | Admin |
| DELETE | `/documents/{id}` | Delete document | Admin |
| POST | `/chat/` | Send a message | User |
| GET | `/chat/history` | Get chat history | User |
| GET | `/users/` | List all users | Admin |
| GET | `/health` | Health check | Public |
