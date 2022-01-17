class ChatRoom():
    """
    Implementation for a Chat Room
    """
    messages = {}

    def __init__(self, id, admin):
        self.id = id
        self.users = []
        self.admin = admin

    @staticmethod
    def add_message(message, recipient_id):
        """
        Adds a message to the dictionary messages
        for a specific recipient.
        """
        if recipient_id in ChatRoom.messages:
            ChatRoom.messages[recipient_id].append(message)
        else:
            ChatRoom.messages[recipient_id] = []
            ChatRoom.messages[recipient_id].append(message)
