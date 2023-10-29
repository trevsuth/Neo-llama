from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import (
    HumanMessage, 
    SystemMessage
)
from langchain.prompts import (
    ChatPromptTemplate, 
    HumanMessagePromptTemplate
)

def get_text_file(path_to_text_file):
    with open(path_to_text_file, 'r') as file:
        content = file.read()
    return content

# Make system prompt, template, llama model
system_prompt = get_text_file('./few_shot_examples.txt')

code_agent = Ollama(model='codellama:instruct',
             temperature=0.01,
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),)

prompt = system_prompt + '\n' + 'What movies was Keanu Reeves in?'

query = code_agent(prompt)
