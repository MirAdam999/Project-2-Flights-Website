
# 21.01.24
# Mir Shukhman
# Defining class LoginToken that will have methods getter and setter
#       and save the logged-in user's data for facade classes to use 

class LoginToken:
    def __init__(self, ID=None, name=None, role=None):
        """
        21.01.24
        Mir Shukhman
        Holds Login Token as tupple of ID, name, role
        Preset to None
        """
        self._token = (ID, name, role)

    @property
    def login_token(self):
        """
        21.01.24
        Mir Shukhman
        Login Token getter
        """
        return self._token

    @login_token.setter
    def login_token(self, values):
        """
        21.01.24
        Mir Shukhman
        Login Token setter
        """
        self._token = values
