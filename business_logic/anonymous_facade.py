
from business_logic.facade_base import FacadeBase
from business_logic.administrator_facade import AdministratorFacade
from business_logic.airline_facade import AirlineFacade
from business_logic.customer_facade import CustomerFacade
from business_logic.login_token import LoginToken

from modules.users import Users
from modules.customers import Customers

# 19.01.24
# Mir Shukhman
# Defining class AnonymouFacade wich inherits from FacadeBase
#                   and will hold login & add_customer funcs

class AnonymousFacade(FacadeBase):
    def __init__(self):
        # Inherts FacadeBase init, 
        # LoginToken class instanse to acsess getter setter funcs from the class
        super().__init__()
        self.lt_instance=LoginToken()
        
        
    def login(self,*,username:str,_password:str):
        """
        22.01.24
        Mir Shukhman
        Login func, makes sure user exists (calls for get_stored_procedure from users_repo (Repository class)
        to acess 'get_user_by_username' stored procedure in the db) and gets user data,
        password correct (matches db password),
        according to user role stored in db:
            gets user's name (calls for get_stored_procedure from admina/airlines/customers 
            repo (Repository class) to acess 'get_admin_by_username'/'get_airline_by_username'/
            'get_customer_by_username'stored procedure in the db)
        generates login token for the user with user ID, name and role (calls for login_token setter
        from LoginToken class),
        gets the generated login token (calls for login_token getter from LoginToken class),
        returns relevant class facade (as decided by user role from db).
        Input: username (str), password (str, private) [all input by parameter name]
        Output: class AdministratorFacade/AirlineFacade/CustomerFacade with login token in init;
                None if username not found, password incorrect or user role not 1,2,3;
                Err str if err
        """
        try:
            # look for user by username(SP)
            user=self.users_repo.get_stored_procedure(
                    'get_user_by_username',{'username':username})
            if user:
                db_pass= user[0][2] 
                db_role= user[0][4]
                user_ID = user[0][0]
                is_active = user[0][5]
                # check password correct
                if db_pass == _password and is_active==True:
                    if db_role == 1:
                        role='Administrator'    # getting admin's name from Admins in db (SP)
                        admin= self.admins_repo.get_stored_procedure( 
                                    'get_admin_by_username',{'username':username})
                        name= f"{admin[0][1]} {admin[0][2]}" 
                        self.lt_instance.login_token= (user_ID,name,role) # using setter
                        current_login_token=self.lt_instance.login_token  # getting token obj from getter
                        facade=AdministratorFacade(current_login_token) 
                        return facade       # returning correct facade with the token in init
                                            
                    elif db_role == 2:
                        role='AirlineCompany'   # getting company's name from AirlineCompanies in db (SP)
                        airline= self.airlines_repo.get_stored_procedure(
                                    'get_airline_by_username',{'username':username})
                        name= f"{airline[0][1]}"
                        self.lt_instance.login_token= (user_ID,name,role) # using setter
                        current_login_token=self.lt_instance.login_token # getting token obj from getter
                        facade=AirlineFacade(current_login_token)
                        return facade       # returning correct facade with the token in init
                        
                    elif db_role == 3:
                        role='Customer'     # getting cust's name from Customres in db (SP)
                        customer= self.customers_repo.get_stored_procedure(
                                    'get_customer_by_username',{'username':username})
                        name=  f"{customer[0][1]} {customer[0][2]}"
                        self.lt_instance.login_token= (user_ID,name,role) # using setter
                        current_login_token=self.lt_instance.login_token # getting token obj from getter
                        facade=CustomerFacade(current_login_token)
                        return facade       # returning correct facade with the token in init
                        
                    else:   # user role not 1,2,3
                        return None
                
                else:   # password incorrect/inactive user
                    return None
                
            else:   #username not found
                return None
        
        except Exception as e:
            return str(e)
   
    
    def add_customer(self,*,username:str,_password:str,
                     email:str,
                     first_name:str,last_name:str,
                     address:str,phone_num:str,
                     _credit_num:str):
        """
        22.01.24
        Mir Shukhman
        Add customer func, ensures password length, calls for _create_new_user 
        func from FacdeBase class,
        calls for get_stored_procedure from users_repo (Repository class)to acess 
        'get_user_by_username' stored procedure in the db to get the created user ID,
        calls for add func from customers_repo to add the new customer to Customers db.
        Input: username (str), password (str, private), email (str),first_name (str),
               last_name(str), address (str), phone_num (str), credit_num (str, private)
               [all input by parameter name]
        Output: True if sucsess; False if customer or user creation err; Err str if err
        """
        try:
            # ensuring password length
            if len(_password) >= 6:
                # create new user using the func from facade base class
                new_user=self._create_new_user(Users(Username=username, 
                                            Password=_password, 
                                            Email=email, 
                                            UserRole=3))
                if new_user:
                    # get newly created user ID from db- find by username
                    created_user=self.users_repo.get_stored_procedure(
                        'get_user_by_username',{'username':username})
                    new_user_ID= created_user[0][0]
                    # create new customer 
                    new_cust=self.customers_repo.add(Customers(FirstName=first_name, 
                                                    LastName=last_name, 
                                                    Address=address,
                                                    PhoneNum=phone_num, 
                                                    CreditCardNum=_credit_num, 
                                                    UserID=new_user_ID))
                    if new_cust:    # creation user+customer sucsess
                        return True 
                    
                    else:   # customer creation err
                        return False 
                
                else:   # user creation err
                    return False 
            
            else:   #password too short
                return False
            
        except Exception as e:
            return str(e)