from langchain import PromptTemplate, LLMChain
from firebase_admin import credentials
from firebase_admin import db
from flask_socketio import SocketIO, send
import pyrebase
import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
import logging
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate


def generate_answers(prompt):
    load_dotenv(find_dotenv())
    HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

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

    memory = ConversationBufferMemory(memory_key="chat_history")

# See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
    repo_id = "tiiuae/falcon-7b-instruct"
    falcon_llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.6, "max_new_tokens": 2000}, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
    )

    output_parser = CommaSeparatedListOutputParser()

    template = """
                Question: {question}
                Context: Take a deep breath and think of the answer step by step. Provide a concise and accurate response using your extensive knowledge as a customer support representative of KAKI. If additional relevant context is available, such as helpdesk ticket information, consider it for a better answer. Format the final answer with proper spaces and line breaks. Each bullet point or numbered item in the list should be a separate item.
                {formatted_template}
                {format_instructions}
                Answer:
            """

    format_instructions = output_parser.get_format_instructions()

    prompt_template = PromptTemplate(template=template, input_variables=[
        "question", "formatted_template"],
        partial_variables={"format_instructions": format_instructions}
    )

    all_tickets_data = ""

    tickets = pyredb.child('tickets').get().val()

    for ticket in tickets:
        subject = pyredb.child(f'tickets/{ticket}/subject').get().val()
        description = pyredb.child(
            f'tickets/{ticket}/descriptions').get().val()
        comments = pyredb.child(f'comments/').get().val()
        comments_text = '\n'.join(comments) if comments else ''
        all_tickets_data += f"\nTicket ID: {ticket}\nSubject: {subject}\nDescription: {description}\nComments: {comments_text}\n"

    _input = prompt_template.format(
        question=prompt, formatted_template=all_tickets_data)
    print(_input)
    output = falcon_llm(_input)

    return output_parser.parse(output)


# llm_chain = LLMChain(prompt=prompt_template, llm=falcon_llm)


# def generate_answers(prompt):
#     print("1. Started to think...")
#     all_tickets_data = ""

#     tickets = pyredb.child('tickets').get().val()

#     for ticket in tickets:
#         subject = pyredb.child(f'tickets/{ticket}/subject').get().val()
#         description = pyredb.child(
#             f'tickets/{ticket}/descriptions').get().val()
#         comments = pyredb.child(f'comments/').get().val()
#         comments_text = '\n'.join(comments) if comments else ''
#         all_tickets_data += f"\nTicket ID: {ticket}\nSubject: {subject}\nDescription: {description}\nComments: {comments_text}\n"

#     formatted_prompt = {
#         "question": prompt,
#         "formatted_template": all_tickets_data
#     }

#     memory_vars = memory.load_memory_variables({})
#     chat_history = memory_vars.get("chat_history", "")

#     print("2. Memory has been initialized...")

#     formatted_prompt = {
#         "question": prompt,
#         "formatted_template": all_tickets_data + "\n\nPrevious Interactions:\n" + chat_history
#     }

#     response = llm_chain.run(formatted_prompt)


#     memory.chat_memory.add_user_message(prompt)
#     if 'Answer' in response:
#         memory.chat_memory.add_ai_message(response['Answer'])

#     print(f"3. Questions have been answered.")

#     return response


# if __name__ == "__main__":
#     faqs = generate_answers("how to solve the email sync issue?")
#     print(faqs)
