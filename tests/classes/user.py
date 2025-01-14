class User:
    def __init__(self, username, password, userid):
        self.username = username
        self.password = password
        self.userid = userid

    def __repr__(self):
        return f"User(username={self.username}, userid={self.userid})"
