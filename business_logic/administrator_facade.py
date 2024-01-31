
from business_logic.facade_base import FacadeBase

from modules.users import Users
from modules.customers import Customers
from modules.airline_companies import AirlineCompanies
from modules.administrators import Administrators

# 24.01.24
# Mir Shukhman
# Defining class AdministratorFacade wich inherits from FacadeBase,
#   recives the login token through the init from login func in AnonymousFacade,
#   and will hold get all, add, activate and de-activate (admins, airlines, customers) funcs.


class AdministratorFacade(FacadeBase):
    def __init__(self, token):
        super().__init__()
        # Inherts FacadeBase init, login token from AnonymousFacade
        # Devides the login token into ID, name and role
        self.token= token
        self.token_userID= self.token[0]
        self.token_admin_name= self.token[1]
        self.token_role= self.token[2]
    

    def _remove_user(self,_userID):
       """
       24.01.24
       Mir Shukhman
       The func calls for remove func from users_repo (Repository class)
       Input: _userID (int, private)
        Output: True if removed; False if not ("remove" func err); Err str if err
       ***Internal usage only! Does not update admins/airlines/customers tables***
       """
       try:
           if self.users_repo.remove(_userID) == True:
               return True
           
           else:
               return False
           
       except Exception as e:
           return str(e)
       
             
    def get_all_customers(self):
        """
        24.01.24
        Mir Shukhman
        Get all customers func, calls for get all func from customers repo
        Input: None
        Output: List of db Model objects; False if facade dosen't match token role;
                None if none found; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                # calling get all
                all_customers = self.customers_repo.get_all()
                if all_customers:
                    return all_customers
                
                else:   # no customers found
                    return None
                
            else:   # facade dosen't match token role
                return False
                                       
        except Exception as e:
            str(e)       
                
    
    def get_all_airlines(self):
        """
        24.01.24
        Mir Shukhman
        Get all airlines func, calls for get all func from airlinesrepo
        Input: None
        Output: List of db Model objects; False if facade dosen't match token role;
                None if none found; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                # calling get all
                all_airlines = self.airlines_repo.get_all()
                if all_airlines:
                    return all_airlines
                
                else:   # no airlines found
                    return None
                
            else:   # facade dosen't match token role
                return False
                           
        except Exception as e:
            str(e)  
            
            
    def get_all_administrators(self):
        """
        24.01.24
        Mir Shukhman
        Get all administrators func, calls for get all func from administrators repo
        Input: None
        Output: List of db Model objects; False if facade dosen't match token role;
                None if none found; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                # calling get all
                all_administrators = self.admins_repo.get_all()
                if all_administrators:
                    return all_administrators
                
                else:   # no administrators found
                    return None
                
            else:   # facade dosen't match token role
                return False
                            
        except Exception as e:
            str(e)    
            
                    
    def add_airline(self,*,username:str,_password:str,
                     email:str,
                     name:str,countryID:int,
                     company_logo:str):
        """
        24.01.24
        Mir Shukhman
        Add airline func, ensures password length, calls for _create_new_user func 
        from FacdeBase class,
        calls for get_stored_procedure from users_repo (Repository class) to acess 
        'get_user_by_username' stored procedure in the db to get the created user ID,
        calls for add func from airlines_repo to add the new airline to Airlines db.
        Input: username (str), password (str, private), email (str),name (str),
               countryID (int), company_logo (str)
               [all input by parameter name]
        Output: True if sucsess; False if airline or user creation err/
                facade dosen't match token role; Err str if err
        """
        try:
            # ensuring password length
            if len(_password) >= 6:
                # ensuring facade matches token role
                if self.token_role=='Administrator':
                    # create new user using the func from facade base class
                    new_airline=self._create_new_user(Users(Username=username, 
                                                Password=_password, 
                                                Email=email, 
                                                UserRole=2))
                    if new_airline:
                        # get newly created user ID from db- find by username
                        created_user=self.users_repo.get_stored_procedure(
                            'get_user_by_username',{'username':username})
                        new_user_ID= created_user[0][0]
                        # create new airline 
                        new_airline=self.airlines_repo.add(AirlineCompanies(Name=name, Country_ID=countryID,
                                                                            UserID=new_user_ID,
                                                                            CompanyLogo=company_logo))
                        if new_airline:    # creation user+airline sucsess
                            return True 
                        
                        else:   # airline creation err
                            return False 
                    
                    else:   # airline creation err
                        return False 
                    
                else:   # facade dosen't match token role
                    return False
                        
            else:   # password too short
                return False
                        
        except Exception as e:
            return str(e)   
    
     
    def add_customer_by_admin(self,*,username:str,_password:str,
                     email:str,
                     first_name:str,last_name:str,
                     address:str,phone_num:str,
                     _credit_num:str):
        """
        22.01.24
        Mir Shukhman
        Add customer func, ensures password length, calls for _create_new_user func 
        from FacdeBase class,
        calls for get_stored_procedure from users_repo (Repository class)to acess 
        'get_user_by_username' stored procedure in the db to get the created user ID,
        calls for add func from customers_repo to add the new customer to Customers db.
        Input: username (str), password (str, private), email (str),first_name (str),
               last_name(str), address (str), phone_num (str), credit_num (str, private)
               [all input by parameter name]
        Output: True if sucsess; False if customer or user creation err/
                facade dosen't match token role; Err str if err
        """
        try:
            # ensuring password length
            if len(_password) >= 6:
                # ensuring facade matches token role
                if self.token_role=='Administrator':
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
                    
                else:   # facade dosen't match token role
                    return False
                        
            else:   # password too short
                return False
                
        except Exception as e:
            return str(e)
    
    
    def add_administrator(self,*,username:str,_password:str,
                            email:str,first_name:str,last_name:str):
        """
        24.01.24
        Mir Shukhman
        Add admin func, ensures password length, calls for _create_new_user func 
        from FacdeBase class,
        calls for get_stored_procedure from users_repo (Repository class)to acess 
        'get_user_by_username' stored procedure in the db to get the created user ID,
        calls for add func from admins_repo to add the new admin to Admins db.
        Input: username (str), password (str, private), email (str),first_name (str),
               last_name(str)
               [all input by parameter name]
        Output: True if sucsess; False if admin or user creation err/
                facade dosen't match token role; Err str if err
        """
        try:
            # ensuring password length
            if len(_password) >= 6:
                # ensuring facade matches token role
                if self.token_role=='Administrator':
                    # create new user using the func from facade base class
                    new_user=self._create_new_user(Users(Username=username, 
                                                Password=_password, 
                                                Email=email, 
                                                UserRole=1))
                    if new_user:
                        # get newly created user ID from db- find by username
                        created_user=self.users_repo.get_stored_procedure(
                            'get_user_by_username',{'username':username})
                        new_user_ID= created_user[0][0]
                        # create new admin 
                        new_admin=self.admins_repo.add(Administrators(FirstName=first_name, 
                                                        LastName=last_name, UserID=new_user_ID))
                        if new_admin:    # creation user+admin sucsess
                            return True 
                        
                        else:   # admin creation err
                            return False 
                    
                    else:   # user creation err
                        return False
                    
                else:   # facade dosen't match token role
                    return False
                        
            else:   # password too short
                return False
                
        except Exception as e:
            return str(e)
    
    
    def deactivate_airline(self,airlineID):
        """ 
        24.01.24
        Mir Shukhman
        Remove airline func, ensures facade matches token role,
        calls remove func from airlines_repo.
        Input: airlinetID (int)
        Output: airline_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no airline by ID found/
                user or airline removal err; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                airline = self.airlines_repo.get_by_id(airlineID)
                #finding airline
                if airline:
                    userID = airline.UserID     # getting userID to deactivate user
                    remove = self.airlines_repo.update(userID,{'IsActive':False})   # deactivating
                    
                    if remove:
                        return True
            else:   
                return False
            
        except Exception as e:
            return str(e)
        
        
    def deactivate_customer(self, customerID):
        """ 
        24.01.24
        Mir Shukhman
        Remove customer func, ensures facade matches token role,
        calls remove func from customers_repo.
        Input: customerID (int)
        Output: customers_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no customer by ID found/
                user or customer removal err; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                customer = self.customers_repo.get_by_id(customerID)
                #finding customer
                if customer:
                    userID = customer.UserID     # getting userID to deactivate user
                    remove = self.customers_repo.update(userID,{'IsActive':False})   # deactivating
                    
                    if remove:
                        return True
            else:   
                return False
            
        except Exception as e:
            return str(e)    
        
        
    def deactivate_administrator(self, adminID):
        """ 
        24.01.24
        Mir Shukhman
        Remove admin func, ensures facade matches token role,
        calls remove func from admins_repo.
        Input: adminID (int)
        Output: admins_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no admin by ID found/
                user or admin removal err; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                admin = self.admins_repo.get_by_id(adminID)
                #finding admin
                if admin:
                    userID = admin.UserID    # getting userID to deactivate  user
                    remove = self.admins_repo.update(userID,{'IsActive':False})   # deactivating
                    
                    if remove:
                        return True
            else:  
                return False
            
        except Exception as e:
            return str(e)
        
        
    def activate_airline(self,airlineID):
        """ 
        24.01.24
        Mir Shukhman
        Remove airline func, ensures facade matches token role,
        calls remove func from airlines_repo.
        Input: airlinetID (int)
        Output: airline_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no airline by ID found/
                user or airline removal err; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                airline = self.airlines_repo.get_by_id(airlineID)
                #finding airline
                if airline:
                    userID = airline.UserID     # getting userID to activate user
                    activate = self.airlines_repo.update(userID,{'IsActive':True})   # activating
                    
                    if activate:
                        return True
            else:   
                return False
            
        except Exception as e:
            return str(e)
        
        
    def activate_customer(self, customerID):
        """ 
        24.01.24
        Mir Shukhman
        Remove customer func, ensures facade matches token role,
        calls remove func from customers_repo.
        Input: customerID (int)
        Output: customers_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no customer by ID found/
                user or customer removal err; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                customer = self.customers_repo.get_by_id(customerID)
                #finding customer
                if customer:
                    userID = customer.UserID     # getting userID to activate user
                    activate = self.customers_repo.update(userID,{'IsActive':True})   # activating
                    
                    if activate:
                        return True
            else:   
                return False
            
        except Exception as e:
            return str(e)    
        
        
    def activate_administrator(self, adminID):
        """ 
        24.01.24
        Mir Shukhman
        Remove admin func, ensures facade matches token role,
        calls remove func from admins_repo.
        Input: adminID (int)
        Output: admins_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no admin by ID found/
                user or admin removal err; Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Administrator':
                admin = self.admins_repo.get_by_id(adminID)
                #finding admin
                if admin:
                    userID = admin.UserID    # getting userID to activate  user
                    activate = self.admins_repo.update(userID,{'IsActive':True})   # activating
                    
                    if activate:
                        return True
            else:  
                return False
            
        except Exception as e:
            return str(e)