from pymongo import MongoClient
import pandas as pd

class MongoDBClient:
    def __init__(self, host='localhost', port=27017, database_name=None):
        self.host = host
        self.port = port
        self.database_name = database_name
        self.client = None
        self.database = None

    def connect(self):
        try:
            self.client = MongoClient(self.host, self.port)
            if self.database_name:
                self.database = self.client[self.database_name]
                print("Connection to MongoDB successful")
        except Exception as e:
            print(f"Error: {e}")
            self.client = None

    def disconnect(self):
        if self.client:
            self.client.close()
            print("MongoDB connection is closed")

    def fetch_documents_to_dataframe(self, collection_name, query={}, limit=None):
        if self.database is not None:
            collection = self.database[collection_name]
            cursor = collection.find(query)
            if limit:
                cursor = cursor.limit(limit)
            documents = list(cursor)
            return pd.DataFrame(documents)
        else:
            print("Database not selected")
            return pd.DataFrame()

    def aggregate(self, collection_name, pipeline):
        if self.database is not None:
            collection = self.database[collection_name]
            results = collection.aggregate(pipeline)
            return list(results)
        else:
            print("Database not selected")
            return []

# Test MongoDB Client
if __name__ == "__main__":
    # Create a MongoDB client
    db = MongoDBClient(host="127.0.0.1", port=27017, database_name="academicworld")
    db.connect()
    
    # Sample query
    df = db.fetch_documents_to_dataframe("publications", limit=1)
    print(df)
    
    # Disconnect db
    db.disconnect()