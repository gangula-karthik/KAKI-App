from celery import Celery
from langchain import PromptTemplate, LLMChain
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask_socketio import SocketIO, send
import pyrebase
import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from celery import Celery

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

config = {
    "apiKey": load_dotenv("PYREBASE_API_TOKEN"),
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
}

cred = credentials.Certificate('Account_management/credentials.json')


firebase = pyrebase.initialize_app(config)
pyredb = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()


# See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
repo_id = "tiiuae/falcon-7b-instruct"
falcon_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.6, "max_new_tokens": 2000}, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)

template = """Question: {question}

Using this information about helpdesk tickets: {formatted_template}

Answer: Let's think step by step."""
prompt_template = PromptTemplate(template=template, input_variables=["question", "formatted_template"])



llm_chain = LLMChain(prompt=prompt_template, llm=falcon_llm)

def generate_faqs():
    print("Generating FAQs....")
    faqs = []
    all_tickets_data = ""

    tickets = pyredb.child('tickets').get().val()

    for ticket in tickets:
        subject = pyredb.child(f'tickets/{ticket}/subject').get().val()
        description = pyredb.child(f'tickets/{ticket}/descriptions').get().val()
        comments = pyredb.child(f'comments/').get().val()
        comments_text = '\n'.join(comments) if comments else ''
        all_tickets_data += f"\nTicket ID: {ticket}\nSubject: {subject}\nDescription: {description}\nComments: {comments_text}\n"

    prompts = [
        "What are the most common issues reported?",
        "Which tickets are still open?",
        "Who are the most active users?",
        "What are the next steps for resolving open tickets?"
    ]

    for prompt in prompts:
        formatted_prompt = {
            "question": prompt,
            "formatted_template": all_tickets_data
        }
        response = llm_chain.run(formatted_prompt)
        faqs.append({
            "question": prompt,
            "answer": response
        })

    print(faqs)
    return faqs




if __name__ == "__main__": 
    faqs = generate_faqs()
    print(faqs)