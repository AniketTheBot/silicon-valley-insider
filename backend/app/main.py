from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
from app.core.database import neo4j_conn
from app.services.scraper import fetch_latest_news
from app.services.extractor import extract_graph_from_text
from app.services.graph_store import save_graph_to_neo4j
from app.services.qa_service import answer_question
from app.core.scheduler import start_scheduler

# Lifespan handles startup and shutdown events


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Starting up Silicon Valley Insider Backend...")
    neo4j_conn.connect()
    yield
    # Shutdown logic
    print("🛑 Shutting down...")
    neo4j_conn.close()

app = FastAPI(title="Silicon Valley Insider Graph", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "online", "message": "Graph Database System Ready"}


@app.get("/test-db")
def test_db_connection():
    """
    Runs a real query against the Neo4j database to prove it works.
    """
    query = "RETURN 'Hello from Neo4j' AS message"

    try:
        session = neo4j_conn.get_session()
        # Run the query and get the single result
        result = session.run(query).single()
        session.close()
        return {"neo4j_response": result["message"]}
    except Exception as e:
        return {"error": str(e)}


@app.get("/scrape-and-extract")
def manual_extraction():
    articles = fetch_latest_news()
    if not articles:
        return {"error": "No articles found"}

    # Let's process the first article
    article = articles[0]
    full_text = f"{article['title']}. {article['summary']}"

    print(f"🧠 Processing: {article['title']}")
    graph_data = extract_graph_from_text(full_text)

    if graph_data:
        # --- THIS IS THE NEW PART ---
        print("💾 Saving to Neo4j...")
        save_graph_to_neo4j(graph_data)
        # ----------------------------

        return {
            "message": "Graph built successfully!",
            "article_title": article['title'],
            "data": graph_data
        }
    else:
        return {"error": "AI extraction failed"}


class QueryRequest(BaseModel):
    question: str
    history: Optional[List[dict]] = []


@app.post("/chat")
def chat_with_graph(request: QueryRequest):
    """
    The GraphRAG Endpoint.
    User asks a question -> System looks up Graph -> Returns Answer.
    """
    result = answer_question(request.question, request.history)
    return result


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting up Silicon Valley Insider Backend...")
    neo4j_conn.connect()

    # Start the background scheduler
    start_scheduler()  # <--- Add this line

    yield
    # Shutdown
    print("🛑 Shutting down...")
    neo4j_conn.close()




@app.get("/graph")
def get_full_graph():
    """
    Fetches the entire Knowledge Graph for the Frontend Visualizer.
    """
    session = neo4j_conn.get_session()
    
    # 1. Fetch all relationships
    # We use LIMIT 1000 to prevent browser crashes if the graph gets too huge
    query = """
    MATCH (s)-[r]->(t)
    RETURN s, r, t
    LIMIT 500
    """
    results = session.run(query)
    
    nodes_dict = {}
    links = []
    
    for record in results:
        source = record["s"]
        target = record["t"]
        rel = record["r"]
        
        # 2. Process Nodes (Use a Dict to prevent Duplicates)
        # Neo4j Node Objects can be accessed like dicts for properties
        s_id = source.get("id", "Unknown")
        t_id = target.get("id", "Unknown")
        
        # Get the Label (e.g., "Company", "Person") for coloring
        s_label = list(source.labels)[0] if source.labels else "Entity"
        t_label = list(target.labels)[0] if target.labels else "Entity"

        nodes_dict[s_id] = {"id": s_id, "group": s_label}
        nodes_dict[t_id] = {"id": t_id, "group": t_label}
        
        # 3. Process Edges
        links.append({
            "source": s_id,
            "target": t_id,
            "relationship": rel.type,
            "sentiment": rel.get("sentiment", "Neutral")
        })
        
    session.close()
    
    # Convert nodes dict back to list
    return {
        "nodes": list(nodes_dict.values()),
        "links": links
    }

if __name__ == "__main__":
    # This allows you to run the file directly with `python app/main.py`
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
