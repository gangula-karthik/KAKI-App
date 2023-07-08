from ticket import Ticket
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/daaa/Downloads/KAKI-App/customer_support/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference('Users')


class User: 
    def __init__(self, role_id, email): 
        self.role_id = role_id
        self.email = email
        self.ticket = None

    def create_ticket(self, subject, description):
        self.ticket = Ticket(1, 1, 1, subject)
        self.ticket.addDescription(description)
        self.ticket.addTopic("technical support")

    def update_ticket(self):
        pass

    def delete_ticket(self):
        self.ticket.deleteTicket()

    def view_ticket(self):
        return self.ticket

    def read_ticket(self):
        pass


class Staff:
    pass

if __name__ == "__main__":
    user = User(1, "karthik@gmail.com")
    user.create_ticket("I am not able to login", "I am not able to login to my account, please help me")
    print(user.view_ticket())
    user.delete_ticket()
    print(user.view_ticket())