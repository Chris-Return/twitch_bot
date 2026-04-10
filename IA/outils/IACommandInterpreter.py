

class IACommandInterpreter:
    def __init__(self):
        self.required_role_level = 0
        self.activationCommand = "Undefined"

    def execute(self, username, message, sock):
        raise NotImplementedError