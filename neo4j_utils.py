from neo4j import GraphDatabase
import pandas as pd


class Neo4jClient:
    def __init__(self, uri, user, password, database=None):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None

    def connect(self):
        try:
            self.driver = GraphDatabase.driver(
                self.uri, auth=(self.user, self.password))
            # Test the connection
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"Error when connecting to Neo4j: {e}")
            self.driver = None

    def disconnect(self):
        if self.driver:
            self.driver.close()
            print("Neo4j connection is closed")

    def fetch_most_cited_publications(self, keyword, limit=10):
        query = f"""
        MATCH (p:PUBLICATION)-[:LABEL_BY]->(k:KEYWORD {{name: "{keyword}"}})
        RETURN p.id AS id, p.title AS title, p.numCitations AS citations
        ORDER BY p.numCitations DESC
        LIMIT {limit}
        """
        with self.driver.session(database="academicworld") as session:
            result = session.run(query)
            records = result.data()
            return pd.DataFrame(records)
