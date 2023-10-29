import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

class Neo4jService:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def run_cypher_query(self, query):
        with self._driver.session() as session:
            return session.run(query).value()


#Load the .env file
load_dotenv()

#Get environment vars
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
AURA_INSTANCEID = os.getenv('AURA_INSTANCEID')
AURA_INSTANCENAME = os.getenv('AURA_INSTANCENAME')

service = Neo4jService(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

dat = service.run_cypher_query('MATCH (p1:Person{name:"Ron Howard"})-[r:DIRECTED]->(m:Movie)<-[r2:ACTED_IN]-(p2:Person) RETURN p2.name')
print(dat)
service.close()