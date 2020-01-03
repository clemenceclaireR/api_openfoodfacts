

class Request:
    def __init__(self, cursor, database):
        self.user_cursor = cursor
        self.user_database = database

        # connexion avec la base de données
        self.running = False

    def show_categories(self):
        self.running = True
        while self.running:

            pass




