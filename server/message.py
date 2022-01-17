class Message:

    messages = {}   # takes a recipient id as a key and message as value

    @staticmethod
    def add_message(message, recipient_id):
        """
        Adds a message to the dictionary messages
        for a specific recipient.
        """
        if recipient_id in Message.messages:
            Message.messages[recipient_id].append(message)
        else:
            Message.messages[recipient_id] = []
            Message.messages[recipient_id].append(message)

    @staticmethod
    def delete_messages(recipient_id):
        """
        Deletes all messages from the dictionary
        messages for a specific recipient id.
        """
        if recipient_id in Message.messages:
            Message.messages[recipient_id].clear()

    @staticmethod
    def num_of_messages(recipient_id):
        """
        Returns the number of messages for a
        recipient id.
        """
        if recipient_id in Message.messages:
            return len(Message.messages[recipient_id])
        else:
            return 0

    @staticmethod
    def get_messages(recipient_id):
        """
        Returns an array containing all the
        messages.
        """
        if recipient_id in Message.messages:
            return Message.messages[recipient_id]

