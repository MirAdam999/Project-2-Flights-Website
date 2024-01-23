
# 21.01.24
# Mir Shukhman
# Defining class LoginToken that will have methods getter and setter
#       and save the logged-in user's data for facade classes to use 

class LoginToken:
    def __init__(self, ID=None, name=None, role=None):
        self._token = (ID, name, role)

    @property
    def login_token(self):
        """
        21.01.24
        Mir Shukhman
        """
        return self._token

    @login_token.setter
    def login_token(self, values):
        """
        21.01.24
        Mir Shukhman
        """
        self._token = values
