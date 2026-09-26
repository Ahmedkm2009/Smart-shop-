# Smart-shop-

AI-powered shopping app backend.

Built with **FastAPI**, designed for local businesses / e-commerce with AI features (product recommendations, smart search, demand insights) routed through FreeLLMAPI or any OpenAI-compatible gateway.

## Features (MVP)
- Product catalog (CRUD)
- Sales / order recording
- AI recommendation endpoint (uses FreeLLMAPI / OpenAI-compatible)
- Health checks
- Docker-ready
- GitHub Actions CI

## Quick Start

### 1. Clone & setup
```bash
git clone https://github.com/Ahmedkm2009/Smart-shop-.git
cd Smart-shop-
cp .env.example .env
```

### 2. Run with Docker (recommended)
```bash
docker compose up --build
```
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 3. Local development
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## FreeLLMAPI Integration
This project expects an OpenAI-compatible endpoint (FreeLLMAPI recommended).

1. Install FreeLLMAPI (self-hosted):
   ```bash
   curl -fsSL https://tashfeenahmed.github.io/freellmapi/install.sh | bash
   ```
2. Open http://localhost:3001 → add free provider keys → copy your `freellmapi-...` key.
3. Put the key + base URL into `.env`:
   ```
   OPENAI_API_KEY=freellmapi-your-key-here
   OPENAI_BASE_URL=http://host.docker.internal:3001/v1   # or your public FreeLLMAPI URL
   ```

The AI endpoints will automatically use it.

## Project Structure
```
app/
  main.py              # FastAPI entrypoint
  config.py            # Settings
  routers/
    products.py
    ai.py              # AI recommendations / chat
  services/
    llm.py             # OpenAI-compatible client (FreeLLMAPI)
.gitignore
requirements.txt
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
```

## GitHub Actions
On every push / PR:
- Lint (ruff)
- Type check (mypy – basic)
- Run tests

## Next Steps
- Add PostgreSQL + SQLAlchemy
- Auth (JWT)
- WhatsApp alerts / inventory forecasting
- Frontend (React / Next.js)

---
Made for the SmartShop family of projects.
