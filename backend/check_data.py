# backend/check_data.py
from app.core.database import neo4j_conn

def print_graph_data():
    print("🕵️ Checking Database Content...")
    neo4j_conn.connect()
    session = neo4j_conn.get_session()
    
    # 1. Count Nodes
    count_query = "MATCH (n) RETURN count(n) as count"
    result = session.run(count_query).single()
    print(f"📊 Total Nodes: {result['count']}")
    
    # 2. List the first 5 Nodes
    list_query = "MATCH (n) RETURN n.id, labels(n) LIMIT 5"
    results = session.run(list_query)
    
    print("\n📝 First 5 Nodes found:")
    for record in results:
        print(f" - [{record['labels(n)'][0]}] {record['n.id']}")
        
    session.close()
    neo4j_conn.close()

if __name__ == "__main__":
    print_graph_data()