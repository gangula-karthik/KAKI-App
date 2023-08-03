from customer_support.ticket import db


class Comment():
    def __init__(self): 
        self.comment = None
        self.comment_id = None
        self.comment_date = None
        self.comment_by = None
        self.ticket_id = None

    def add_comment(self, ticket_id, comment, comment_date, comment_by):
        """
        can be used to add and updated a comment to a ticket
        """
        self.ticket_id = ticket_id
        self.comment = comment
        self.comment_date = comment_date
        self.comment_by = comment_by
        db.child("comments").push(self.__dict__)
        return 200

    def delete_comment(self, ticket_id, comment_id):
        """
        can be used to delete a comment to a ticket
        """
        pass
    
    def get_comment(self):
        return self.comment
    
    def get_comment_id(ticket_id, self):
        return self.comment_id
    


if __name__ == "__main__": 
    c = Comment()
    c.add_comment('-NaKM7Bmys6kBmFdC0l0', 'this is a comment', '123', '2020-01-01', '123')
    print(c.get_comment())