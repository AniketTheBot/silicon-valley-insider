from pydantic import BaseModel
from typing import List, Literal

# Defines a Node (e.g., "Microsoft", "Sam Altman")
class Node(BaseModel):
    id: str
    type: str  # e.g., "Company", "Person", "Product"

# Defines a Relationship (e.g., "Microsoft" -> "INVESTED_IN" -> "OpenAI")
class Edge(BaseModel):
    source: str
    target: str
    relationship: str  # e.g., "INVESTED_IN", "SUED", "LAUNCHED"
    sentiment: Literal["Positive", "Negative", "Neutral"] # The Sentiment Logic

# The final output we expect from the LLM
class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]