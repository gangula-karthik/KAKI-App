from ticket import Ticket
from db_setup import database_init
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import json

database_init()

# print(json.dumps(db.reference("Users").get(), indent=4))
kakiDB = db.reference("user")

kakiDB.set({
    "email": "johnwick@gmail.com",
    "name": "John Wick"
})

class User: 
    def __init__(self, role_id, email): 
        self.role_id = role_id
        self.email = email
        self.ticket = None

    def create_ticket(self, subject, description):
        self.ticket = Ticket(1, 1, 1, subject)
        self.ticket.addDescription(description)
        self.ticket.addTopic("technical support")
        kakiDB.child("email").set({
            "ticket": json.load(self.ticket.__str__())
        })

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
    user = User(1, "kars@gmail.com")
    user.create_ticket("app is broken", "this app sux")
    print(user.view_ticket())