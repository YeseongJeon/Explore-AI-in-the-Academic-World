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

    def find(self, collection_name, query={}, projection={}, limit=None):
        if self.database is not None:
            collection = self.database[collection_name]
            if projection:
                cursor = collection.find(query, projection)
            else:
                cursor = collection.find(query)

            if limit:
                cursor = cursor.limit(limit)
            documents = list(cursor)
            return pd.DataFrame(documents)
        else:
            print("MongoDB collection not selected")
            return pd.DataFrame()

    def aggregate(self, collection_name, pipeline):
        if self.database is not None:
            collection = self.database[collection_name]
            results = collection.aggregate(pipeline)
            return pd.DataFrame(list(results))
        else:
            print("MongoDB collection not selected")
            return pd.DataFrame()

    def fetch_top_unversity_by_keyword(self, keyword = 'artificial intelligence', topn = 10):
        keyword = keyword.lower()
        average_score = self.aggregate("publications", [
            { '$match': { 'keywords.name': keyword } },
            { '$unwind': '$keywords' },
            { '$match': { 'keywords.name': keyword } },
            { '$group': { '_id': None, 'averageScore': { '$avg': '$keywords.score' } } }
        ])['averageScore'][0]
        # Find publications with the keyword and score greater than the average score
        relevant_publications = self.find("publications", {
            'keywords': {
                '$elemMatch': {
                    'name': keyword,
                    'score': { '$gt': average_score }
                }
            }
        }, { '_id': 0, 'id': 1 })
        relevant_publication_ids = [id for id in relevant_publications['id']]
        # Find faculty members affiliated with universities with the most publications
        ranking = self.aggregate("faculty", [
            { '$unwind': '$publications' },
            { '$match': { 'publications': { '$in': relevant_publication_ids } } },
            {
                '$group': {
                    '_id': {
                        'university_name': '$affiliation.name',
                        'university_id': '$affiliation.id'
                    },
                    'KeyPublicationCount': { '$sum': 1 }
                }
            },
            { 
                '$project': {
                    '_id': 0,
                    'UniversityName': '$_id.university_name',
                    'UniversityId': '$_id.university_id',
                    'KeyPublicationCount': 1
                } 
            },
            { '$sort': { 'KeyPublicationCount': -1 } }
        ])
        # Rearrange the columns and return the top universities
        ranking['UniversityName(UniversityId)'] = ranking.apply(lambda row: f"{row['UniversityName']} (Id:{row['UniversityId']})", axis=1)
        ranking = ranking[['UniversityName(UniversityId)', 'KeyPublicationCount']]
        return ranking.head(topn)
    
# Test MongoDB Client
if __name__ == "__main__":
    # Create a MongoDB client
    db = MongoDBClient(host="127.0.0.1", port=27017, database_name="academicworld")
    db.connect()

    df = db.fetch_top_unversity_by_keyword("artificial intelligence", 10)
    print(df)

    # Disconnect db
    db.disconnect()