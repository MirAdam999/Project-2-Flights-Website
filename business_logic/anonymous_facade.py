
from facade_base import FacadeBase

# 19.01.24
# Mir Shukhman
# Defining class AnonymousBase wich inherits from FacadeBase
#                   and will hold login & add_customer funcs

class AnonymousFacade(FacadeBase):
    def __init__(self):
        super().__init__()
        self.login_token, self.facade= self.login()
        
    
    def login(self,*,username:str,_password:str):
        try:
            self.users_repo.get_stored_procedure
            if user:
                #call login_token func
                return login_token, facade
            else:
                return None
        except Exception as e:
            return str(e)
   
    
    def add_customer(self,*,username:str,_password:str,
                     email:str,
                     first_name:str,last_name:str,
                     address:str,phone_num:str,
                     _credit_num:str):
        pass