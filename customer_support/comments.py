from ticket import Ticket

class Comment(Ticket):
    def __init__(self): 
        super().__init__()
        self.comment = None
        self.comment_id = None
        self.comment_date = None
        self.comment_by = None

    def add_comment(self, comment, comment_id, comment_date, comment_by):
        """
        can be used to add and updated a comment to a ticket
        """
        self.comment = comment
        self.comment_id = comment_id
        self.comment_date = comment_date
        self.comment_by = comment_by

    def delete_comment(self, comment_id):
        """
        can be used to delete a comment to a ticket
        """
        pass
    
    def get_comment(self):
        return self.comment
    
    def get_comment_id(self):
        return self.comment_id
    
    def get_comment_date(self):
        return self.comment_date
    
    def get_comment_by(self):
        return self.comment_by
    
    def __str__(self):
        return f"Comment: {self.comment}\nComment ID: {self.comment_id}\nComment Date: {self.comment_date}\nComment By: {self.comment_by}\n"