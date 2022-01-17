from hashlib import sha1


class Bot():
    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id
        self.token = self.create_token(client_id, name)
        self.permissions = 0
        self.users = []

    def create_token(self, client_id, name):
        token_name = str(name) + str(client_id)
        encoded = token_name.encode()
        token = sha1(encoded)
        token = token.hexdigest()
        return token

    def set_permission(self, permissions):
        self.permissions = permissions

    def permission_1(self, username):
        message = "Welcome " + str(username)
        return message

    def permission_2(self, message):
        if "stupid" in message:
            return
        return

    def permission_3(self):
        #check warnings to see if less than 3
        return

    def permission_4(self):
        #compute response time of a message
        return

    def permission_5(self):
        #print user is inactive after 5 mins
        return