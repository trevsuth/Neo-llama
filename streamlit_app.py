import streamlit as st
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain.llms.ollama import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class Neo4jService:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def run_cypher_query(self, query):
        with self._driver.session() as session:
            return session.run(query).value()

def get_text_file(path_to_text_file):
    with open(path_to_text_file, 'r') as file:
        content = file.read()
    return content

# Load the .env file
load_dotenv()

# Get environment vars
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
AURA_INSTANCEID = os.getenv('AURA_INSTANCEID')
AURA_INSTANCENAME = os.getenv('AURA_INSTANCENAME')

service = Neo4jService(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

# Make system prompt, template, llama model
system_prompt = get_text_file('./few_shot_examples.txt')

code_agent = Ollama(model='codellama:instruct',
             temperature=0.01,
             verbose=False,
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),)

# Streamlit UI
st.title("Neo4j Query Generator and Executor")

user_input = st.text_area("Enter your prompt:", "Who acted in A League of Their Own?")

if st.button("Generate and Run Query"):
    prompt = system_prompt + '\n' + user_input
    st.write('Generated query:')
    query = code_agent(prompt)
    st.write(query)

    st.write('\nResults:')
    response = service.run_cypher_query(query)
    for r in response:
        st.write(r)

    service.close()
