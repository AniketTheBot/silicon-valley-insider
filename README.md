# 🕸️ The Silicon Valley Insider (GraphRAG)

A Live Knowledge Graph Agent that maps the Tech Ecosystem.  
Powered by FastAPI, Neo4j, Llama 3 (Groq), and React Force Graph 3D.  
![alt text](https://img.shields.io/badge/Status-Live-brightgreen)

![alt text](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)

![alt text](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)

![alt text](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)

![alt text](https://img.shields.io/badge/Neo4j-008CC1?logo=neo4j&logoColor=white)

![alt text](https://img.shields.io/badge/AI-Llama_3-blueviolet)

## 💡 The Concept

Standard RAG (Retrieval Augmented Generation) has a flaw: Context Collapse. If you search for "Sam Altman", a Vector Database finds documents with his name but misses the temporal connections (e.g., He was Fired, then Rehired, then Joined Microsoft).  
The Silicon Valley Insider solves this by building a Knowledge Graph.

- Instead of chunking text, we use an AI Agent to extract Entities (Nodes) and Relationships (Edges).
- Input: Live RSS Feeds / Simulated News Data.
- Processing: Llama 3 extracts structured JSON (e.g., Microsoft -> INVESTED_IN -> OpenAI).
- Storage: Neo4j Graph Database.
- Output: An Agentic Chatbot that "walks" the graph to answer complex questions + a 3D Visualization that reacts to the conversation.

## 🏗️ Architecture

### Ingestion Pipeline (ETL):
- Scrapes TechCrunch/The Verge (or uses simulate_feed.py for testing).
- Llama 3 (Groq) analyzes text and extracts Entities & Sentiment.
- Deduplication Logic ensures "Sam Altman" and "Samuel Altman" merge into one node.

### Database (The Brain):
- Neo4j AuraDB stores the connected web of data.

### Backend (The API):
- FastAPI serves the Graph data and handles Chat endpoints.
- LangChain orchestrates the "Contextualization" (rewriting user queries based on history).

### Frontend (The Visuals):
- React + Vite for the UI.
- React Force Graph 3D for the interactive visualization.
- Camera Auto-Focus: The camera physically flies to the node mentioned in the chat.

## 🛠️ Tech Stack

- Backend: Python 3.11+, FastAPI, LangChain, Groq SDK.
- Database: Neo4j (AuraDB Free Tier).
- AI Engine: Llama 3.3 70B (via Groq API).
- Frontend: React, Tailwind CSS, Framer Motion, Three.js (React Force Graph).

## 🚀 Setup Guide

### Prerequisites
- Neo4j Aura Account: Get a Free Instance here. Save your password and URI.
- Groq API Key: Get a Free Key here.
- Python 3.11+ and Node.js installed.

### 1. Clone & Configure Backend

```bash
cd backend
```

# Create Virtual Environment
```bash
python -m venv venv
```

# Activate (Windows Git Bash)
```bash
source venv/Scripts/activate
```

# Activate (Mac/Linux)
```bash
source venv/bin/activate
```

# Install Dependencies
```bash
pip install -r requirements.txt
```

Create a .env file in the backend folder:

```ini
NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-neo4j-password
GROQ_API_KEY=gsk_your_groq_api_key
```

Start the Server:

```bash
python -m app.main
```

You should see: "✅ Connected to Neo4j successfully!"

### 2. Configure Frontend

Open a new terminal.

```bash
cd frontend
```

# Install Dependencies
```bash
npm install
```

# Start UI
```bash
npm run dev
```

Open http://localhost:5173 in your browser.

## 🧪 First Run: Populating the Graph

When you first launch the app, the screen will be black because the database is empty. You need to run the Simulation Script to inject data.

We have built a sophisticated simulation script that mimics a live news feed over several months (OpenAI firing drama, Nvidia chip releases, Apple Intelligence, etc.).

1. Keep the Backend and Frontend running.
2. Open a 3rd Terminal in the backend folder.
3. Run the Simulation:

```bash
python simulate_feed.py
```

What happens next:
- The script sends raw headlines to Llama 3.
- Llama 3 extracts nodes/edges and detects sentiment (e.g., "Elon Sued OpenAI" -> Negative Edge).
- The data is pushed to Neo4j.
- Watch your Frontend: You will see the graph grow in real-time without refreshing.

## 🎮 How to Use

### 1. The Visualizer
- Rotate/Zoom: Click and drag to explore the Silicon Valley ecosystem.
- Nodes: Represent Companies, People, or Products.
- Edges: Represent relationships (Hired, Fired, Sued, Invested).
- Colors: Different colors for different Entity types (Person vs Company).

### 2. The Agentic Chat (GraphRAG)
Ask complex questions in the chat box. The Agent remembers context.

Try this conversation flow:

- "What happened between Sam Altman and OpenAI?"  
  Result: The bot explains he was fired and rehired. The Camera flies to the OpenAI node.

- "Who is hostile towards them?"  
  Result: The bot understands "them" = OpenAI. It finds Elon Musk (Sued). The Camera flies to Elon Musk.

- "How is Microsoft involved?"  
  Result: It explains the investment partnership.

## 📂 Project Structure

```text
root/
├── backend/
│   ├── app/
│   │   ├── main.py            # API Entry & Scheduler
│   │   ├── core/              # DB Connection & Config
│   │   ├── services/
│   │   │   ├── extractor.py   # Llama 3 Logic (Text -> JSON)
│   │   │   ├── qa_service.py  # RAG Logic (Context -> Answer)
│   │   │   └── graph_store.py # Neo4j Cypher Queries
│   │   └── models/            # Pydantic Schemas
│   ├── simulate_feed.py       # TEST SCRIPT (Run this first!)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GraphView.jsx   # 3D Visualizer + Camera Logic
│   │   │   ├── ChatOverlay.jsx # Chat UI + History Logic
│   │   │   └── CursorGlow.jsx  # Custom UI Effects
│   │   ├── App.jsx             # Layout & Layering
│   └── tailwind.config.js

```
## 🛡️ Troubleshooting
Graph is Empty?
Did you run python simulate_feed.py?
Check your .env credentials.
Camera doesn't fly?
Ensure the node exists in the graph. The chat logs 🎯 Chatbot identified target: [Name] in the console.
"Connection Error"?
Ensure Backend is running on Port 8000.