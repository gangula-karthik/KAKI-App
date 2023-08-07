from langchain import PromptTemplate, LLMChain
from flask_socketio import SocketIO, send
import pyrebase
import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.memory import ConversationBufferMemory
import logging


try:
    load_dotenv(find_dotenv())
    HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
except KeyError:
    print("Error: HUGGINGFACEHUB_API_TOKEN not found in environment variables.")
except Exception as e:
    print(f"An unknown error occurred ({e})...")

memory = ConversationBufferMemory(memory_key="chat_history")

logging.info("Starting FAQ generation...")

config = {
    "apiKey": load_dotenv("PYREBASE_API_TOKEN"),
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
}


firebase = pyrebase.initialize_app(config)
pyredb = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()

logging.info("Firebase initialized.")


# See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
repo_id = "tiiuae/falcon-7b-instruct"
falcon_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.6, "max_new_tokens": 2000}, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)

template = """Question: {question}

Context: As a seasoned professional with extensive experience, provide a concise response to the query. If the user offers a greeting, reciprocate warmly. If the answer isn't immediately known, utilize the provided helpdesk ticket information: {formatted_template} and past conversation: {chat_history}.

Guideline: Responses should be succinct, aiming for no more than three sentences.

Answer:

"""


prompt_template = PromptTemplate(template=template, input_variables=["question", "formatted_template", "chat_history"])

llm_chain = LLMChain(prompt=prompt_template, llm=falcon_llm, memory=memory)

def generate_answers(prompt):
    print("Thinking...")
    all_tickets_data = ""

    tickets = pyredb.child('tickets').get().val()

    for ticket in tickets:
        subject = pyredb.child(f'tickets/{ticket}/subject').get().val()
        description = pyredb.child(f'tickets/{ticket}/descriptions').get().val()
        comments = pyredb.child(f'comments/').get().val()
        comments_text = '\n'.join(comments) if comments else ''
        all_tickets_data += f"\nTicket ID: {ticket}\nSubject: {subject}\nDescription: {description}\nComments: {comments_text}\n"

    memory_vars = memory.load_memory_variables({})
    chat_history = memory_vars.get("chat_history", "")

    formatted_prompt = {
        "question": prompt,
        "formatted_template": all_tickets_data,
        "chat_history": chat_history
    }

    response = llm_chain.run(formatted_prompt)

    memory.chat_memory.add_user_message(prompt)
    memory.chat_memory.add_ai_message(response.get('Answer', ''))

    print(f"questions have been answered.")

    return response




if __name__ == "__main__": 
    faqs = generate_answers("how to solve the email sync issue?")
    print(faqs)