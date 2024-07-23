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
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Test the connection
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"Error when connecting to Neo4j: {e}")
            self.driver = None

    def disconnect(self):
        if self.driver:
            self.driver.close()
            print("Neo4j connection is closed")


# Test Neo4j Client
if __name__ == "__main__":
    # Create a Neo4j client
    db = Neo4jClient(uri="bolt://localhost:7687", user="neo4j", password="ilovecs411")
    db.connect()

    # Sample query
    records, summary, keys = db.driver.execute_query(
        "MATCH (f:FACULTY) RETURN count(f)",
        database_="academicworld",
    )
    print(records)

    # Summary information
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after,
    ))
    
    # Disconnect db
    db.disconnect()
