# 🕸️ Silicon Valley Insider (GraphRAG)

A live Knowledge-Graph Agent mapping the tech ecosystem.  
Backend: FastAPI + Neo4j. AI: Llama 3 (Groq). Frontend: React + React Force Graph 3D.

![Status](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi) ![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB) ![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?logo=neo4j&logoColor=white)

## Concept

Traditional RAG can suffer from "context collapse." This project extracts entities and relationships from news to build a temporal, connected knowledge graph, enabling a chat agent to traverse and answer contextual questions.

Key flow:
- Ingest news (live or simulated)
- Extract entities/relations via Llama 3 (Groq)
- Store graph in Neo4j
- Expose FastAPI endpoints for chat, queries, and visualization
- Frontend visualizer shows interactive 3D graph and camera focus

## Features

- Entity & relation extraction (text → structured graph)
- Neo4j storage (AuraDB supported)
- GraphRAG chat endpoint (graph-augmented answers)
- 3D frontend visualizer with camera focus
- Simulation script to populate the graph for testing

## Tech Stack

- Backend: Python 3.11+, FastAPI, pydantic
- Database: Neo4j (AuraDB)
- AI: Llama 3 via Groq API
- Frontend: React, Vite, React Force Graph 3D
- Dev: uvicorn, node/npm

## Prerequisites

- Neo4j Aura account (URI, username, password)
- Groq API key (for Llama 3)
- Python 3.11+, Node.js, npm

## Backend — Setup (Windows)

1. Open terminal in the `backend` folder:
   ```powershell
   cd "C:\CODE\ResumeProjects\silicon-valley-insider\backend"
   ```

2. Create & activate venv:
   PowerShell:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   CMD:
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Create `.env` in `backend`:
   ```ini
   NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your-neo4j-password
   GROQ_API_KEY=gsk_your_groq_api_key
   ```

5. Run backend (recommended):
   ```powershell
   # from backend folder
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Or:
   ```powershell
   python -m app.main
   ```

## Frontend — Setup

1. Open a new terminal and go to `frontend`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Open: http://localhost:5173

## Populate the Graph (First Run)

The frontend will appear empty until the graph has data. Use the simulator to seed data:

```bash
# from backend folder
python simulate_feed.py
```

This sends simulated headlines through the extractor and writes nodes/edges to Neo4j.

## API Endpoints (examples)

- GET / → status
- GET /test-db → simple Neo4j test query
- GET /scrape-and-extract → run one extraction and save to DB
- POST /chat → GraphRAG chat (body: { "question": "...", "history": [...] })

## Project Structure

```
root/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  │  ├─ database.py
│  │  │  └─ config.py
│  │  ├─ services/
│  │  │  ├─ extractor.py
│  │  │  ├─ graph_store.py
│  │  │  └─ qa_service.py
│  │  └─ models/
│  ├─ simulate_feed.py
│  └─ requirements.txt
└─ frontend/
   ├─ src/
   └─ package.json
```

## Troubleshooting

- ModuleNotFoundError: run with `python -m app.main` or start uvicorn from the `backend` folder.
- Pydantic extra env errors: confirm `.env` keys match fields in `app/core/config.py` or set config to ignore extras.
- Neo4j connection issues: verify URI, username, and password; ensure Aura instance is accessible.

## Notes

- Keep secrets out of VCS. Use environment variables or a secret manager.
- For development, CORS is permissive; tighten for production.
- Adjust `/graph` LIMIT in `main.py` if frontend performance suffers.

---

Built for experimentation and demos — contributions welcome.