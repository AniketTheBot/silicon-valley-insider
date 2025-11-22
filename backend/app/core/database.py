from neo4j import GraphDatabase
from app.core.config import settings

class Neo4jConnection:
    def __init__(self):
        self.driver = None

    def connect(self):
        if not self.driver:
            try:
                print(f"🔌 Connecting to Neo4j at {settings.NEO4J_URI}...")
                self.driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
                )
                # Verify connectivity immediately
                self.driver.verify_connectivity()
                print("✅ Connected to Neo4j successfully!")
            except Exception as e:
                print(f"❌ Failed to connect to Neo4j: {e}")
                # We raise the error so the app knows it failed to start
                raise e

    def close(self):
        if self.driver:
            self.driver.close()
            print("🔒 Neo4j connection closed.")

    def get_session(self):
        """Returns a new session for database transactions."""
        if not self.driver:
            self.connect()
        return self.driver.session()

# Create a single instance to be imported elsewhere
neo4j_conn = Neo4jConnection()