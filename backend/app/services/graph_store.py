from app.core.database import neo4j_conn
from app.models.schemas import GraphData


def save_graph_to_neo4j(graph_data: GraphData):
    """
    Takes the extracted Nodes/Edges and writes them to Neo4j.
    """
    session = neo4j_conn.get_session()

    try:
        # 1. Save Nodes
        for node in graph_data.nodes:
            # Query: MERGE (n:Label {id: "Name"})
            # We use backticks ` ` around the type to handle spaces/special chars safely
            query = f"""
            MERGE (n:`{node.type}` {{id: $id}})
            RETURN n
            """
            session.run(query, id=node.id)

        # 2. Save Edges
        for edge in graph_data.edges:
            # Query: Find Source, Find Target, Create Link
            # Note: We match by ID only, so we don't need to know the Type here
            query = f"""
            MATCH (s {{id: $source_id}})
            MATCH (t {{id: $target_id}})
            MERGE (s)-[r:`{edge.relationship}`]->(t)
            SET r.sentiment = $sentiment
            """
            session.run(query,
                        source_id=edge.source,
                        target_id=edge.target,
                        sentiment=edge.sentiment)

        print(
            f"✅ Saved {len(graph_data.nodes)} nodes and {len(graph_data.edges)} edges to Neo4j.")

    except Exception as e:
        print(f"❌ Database Save Error: {e}")
    finally:
        session.close()


def check_article_exists(url: str):
    session = neo4j_conn.get_session()
    # Check if a Source Node with this URL exists
    query = "MATCH (a:Article {url: $url}) RETURN count(a) as count"
    result = session.run(query, url=url).single()
    session.close()
    return result["count"] > 0
