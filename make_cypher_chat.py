from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

def make_ollama_model(model_name):
    model = ChatOllama(model=model_name,
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))
    return model

def get_text_file(path_to_text_file):
    with open(path_to_text_file, 'r') as file:
        content = file.read()
    return content

def make_template(sysmsg):
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(sysmsg)),
            HumanMessagePromptTemplate.from_template('{text}'),
        ]
    )
    return template

def llm(prompt, model, template, verbose=False):
    output = model(template.format_messages(text=prompt)).content
    if verbose == True:
        print(output)
    return output

# Make system prompt, template, llama model
system_prompt = get_text_file('./few_shot_examples.txt')
template = make_template(system_prompt)
code_agent = make_ollama_model('mistral:instruct')

code_agent(template.format_messages(text='What movies was Keanu Reeves in?'))
