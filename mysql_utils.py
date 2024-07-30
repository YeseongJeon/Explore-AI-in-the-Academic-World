import mysql.connector
from mysql.connector import Error


class MySQLClient:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connection to academicworld db successful")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def execute_query(self, query):
        cursor = None
        try:
            if self.connection is not None and self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                print("Query executed successfully")
            else:
                print("Connection is not established")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor is not None:
                cursor.close()

    def fetch_results(self, query):
        cursor = None
        results = None
        try:
            if self.connection is not None and self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
            else:
                print("Connection is not established")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return results

    def fetch_widget1_results(self):
        query = '''
            SELECT name, COUNT(p.id)
            FROM publication_keyword pk
            JOIN keyword k ON pk.keyword_id = k.id
            JOIN publication p ON pk.publication_id = p.id
            WHERE name IN (
                "Artificial intelligence",
                "Computer vision",
                "Natural language processing",
                "Machine learning",
                "Information retrieval"
            )
            GROUP BY k.name
            ORDER BY k.name ASC
            LIMIT 10;
        '''
        return self.fetch_results(query)

    def fetch_widget2_universities(self):
        query = '''
            SELECT DISTINCT u.name, u.id
            FROM university u
            JOIN faculty f ON u.id = f.university_id
            ORDER BY CASE WHEN u.id = 12 THEN 1 ELSE 0 END DESC;
        '''
        return self.fetch_results(query)

    def fetch_widget2_results(self, keyword, university):
        query = f'''
            SELECT f.name, SUM(pk.score * p.num_citations) AS KRC
            FROM faculty f
            JOIN faculty_publication fp ON f.id = fp.faculty_id
            JOIN publication p ON fp.publication_id = p.id
            JOIN publication_keyword pk ON p.id = pk.publication_id
            JOIN keyword k ON pk.keyword_id = k.id
            JOIN university u ON f.university_id = u.id
            WHERE k.name = "{keyword}" AND u.name = "{university}"
            GROUP BY f.name
            ORDER BY KRC DESC
            LIMIT 5;
        '''
        return self.fetch_results(query)
