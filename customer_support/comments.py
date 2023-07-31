from ticket import Ticket, db



class Comment(Ticket):
    def __init__(self): 
        super().__init__()
        self.comment = None
        self.comment_id = None
        self.comment_date = None
        self.comment_by = None
        db.child(f'/tickets/{self.ticket_id}/comments').set(self.comments)

    def add_comment(self, ticket_id, comment, comment_id, comment_date, comment_by):
        """
        can be used to add and updated a comment to a ticket
        """
        self.ticket_id = ticket_id
        self.comment = comment
        self.comment_id = comment_id
        self.comment_date = comment_date
        self.comment_by = comment_by

    def delete_comment(self, ticket_id, comment_id):
        """
        can be used to delete a comment to a ticket
        """
        pass
    
    def get_comment(self):
        return self.comment
    
    def get_comment_id(ticket_id, self):
        return self.comment_id