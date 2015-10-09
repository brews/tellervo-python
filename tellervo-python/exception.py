class XmlError(Exception):
    pass # Something about XML failing to validate?

class RequestError(Exception):
    def __init__(self, message, message_code):
        self.message = message
        self.message_code = message_code

    def __str__(self):
        return repr(self.message)