
from modules.administrators import Administrators
from modules.airline_companies import AirlineCompanies
from modules.countries import Countries
from modules.customers import Customers
from modules.flights import Flights
from modules.tickets import Tickets
from modules.user_roles import UserRoles
from modules.users import Users
from repository import Repository

# 18.01.24
# Mir Shukhman
# Defining class FacadaBase wich will be parent class for all other Facade classes
#       all of FacadeBase funcs can be acsessed by the rest of the Facades

class FacadeBase:
    def __init__(self):
        # Instances of Repository class with all the db.models as parameters 
        #       to utilise Repo's funcs in the Facade classes' funcs
        self.admins_repo= Repository(Administrators)
        self.airlines_repo= Repository(AirlineCompanies)
        self.countries_repo= Repository(Countries)
        self.customers_repo= Repository(Customers)
        self.flights_repo= Repository(Flights)
        self.tickets_repo= Repository(Tickets)
        self.user_roles_repo= Repository(UserRoles)
        self.users_repo= Repository(Users)
      
    # In use
    def _create_new_user(self,_user):
       """
       17.01.24
       Mir Shukhman
       The func calls for add func from users_repo (Repository class)
       Input: new user data as in-
                Users(Username='x', Password='y', Email='z', UserRole=1)
        Output: True if added; False if not ("add" func err); Err str if err
       ***Internal usage only! Does not update admins/airlines/customers tables***
       """
       try:
           if self.users_repo.add(_user) == True:
               return True
           
           else:
               return False
           
       except Exception as e:
           return str(e)
    
    
    def get_user_by_ID(self, userID:int):
        """
       20.01.24
       Mir Shukhman
       The func calls for get_by_id func from users_repo (Repository class)
       Input: user ID (int)
       Output: get_by_id func output (db.model obj/none/str err); Err str if err
       """
        try:
            user=self.users_repo.get_by_id(userID)
            return user
        
        except Exception as e:
           return str(e)
       
       
    def get_admin_by_adminID(self, adminID:int):
        """
       20.01.24
       Mir Shukhman
       The func calls for get_by_id func from admins_repo (Repository class)
       Input: admin ID (int)
       Output: get_by_id func output (db.model obj/none/str err); Err str if err
       """
        try:
            admin=self.admins_repo.get_by_id(adminID)
            return admin
        
        except Exception as e:
           return str(e)
       
       
    def get_customer_by_ID(self, custID:int):
        """
       20.01.24
       Mir Shukhman
       The func calls for get_by_id func from customers_repo (Repository class)
       Input: customer ID (int)
       Output: get_by_id func output (db.model obj/none/str err); Err str if err
       """
        try:
            cust=self.customers_repo.get_by_id(custID)
            return cust
        
        except Exception as e:
           return str(e)
    
    
    def get_country_by_ID(self, countryID:int):
        """
       17.01.24
       Mir Shukhman
       The func calls for get_by_id func from countries_repo (Repository class)
       Input: country ID (int)
       Output: get_by_id func output (db.model obj/none/str err); Err str if err
       """
        try:
            country=self.countries_repo.get_by_id(countryID)
            return country
        
        except Exception as e:
           return str(e)
       
       
    def get_all_countries(self):
        """
       17.01.24
       Mir Shukhman
       The func calls for get_all func from countries_repo (Repository class)
       Input: None
       Output: get_all func output (list of db.model obj/none/str err); Err str if err
       """
        try:
            all_countries=self.countries_repo.get_all()
            return all_countries
        
        except Exception as e:
           return str(e)
       
    
    def	get_airline_by_airline_ID(self, airlineID:int):
        """
       19.01.24
       Mir Shukhman
       The func calls for get_by_id func from airlines_repo (Repository class)
       Input: airlineID (int)
       Output: get_by_id func output (db.model obj/none/str err); Err str if err
       """
        try:
            airline=self.airlines_repo.get_by_id(airlineID)
            return airline
        
        except Exception as e:
           return str(e)
    
    
    def	get_all_airlines(self):
        """
       19.01.24
       Mir Shukhman
       The func calls for get_all func from airlines_repo (Repository class)
       Input: None
       Output: get_all func output (list of db.model obj/none/str err); Err str if err
       """
        try:
            airlines=self.airlines_repo.get_all()
            return airlines
        
        except Exception as e:
           return str(e)
    
    
    def	get_flights_by_ID(self, flightID:int):
        """
        19.01.24
        Mir Shukhman
        The func calls for get_by_id func from flights_repo (Repository class)
        Input: flightID (int)
        Output: get_by_id func output (db.model obj/none/str err); Err str if err
        """
        try:
            flight=self.flights_repo.get_by_id(flightID)
            return flight
        
        except Exception as e:
           return str(e)
    
    
    def	get_all_flights(self):
        """
       19.01.24
       Mir Shukhman
       The func calls for get_all func from flights_repo (Repository class)
       Input: None
       Output: get_all func output (list of db.model obj/none/str err); Err str if err
       """
        try:
            flights=self.flights_repo.get_all()
            return flights
        
        except Exception as e:
           return str(e)
    
    
    def get_flights_by_parameters(self, *, origin_countryID:int, destination_countryID:int, date:str):
        """
       19.01.24
       Mir Shukhman
       The func calls for get_stored_procedure from flights_repo (Repository class)
            to acess 'get_flights_by_parameters' stored procedure in the db
       Input: origin_countryID (int),
                destination_countryID (int),
                date (str)- YYYY-MM-DD,
                [all input by parameter name]
       Output: get_stored_procedure func output (list of tupples/none/str err); Err str if err
       """
        try:
            flights=self.flights_repo.get_stored_procedure('get_flights_by_parameters',
                                                        {'origin_country_id': origin_countryID,
                                                        'destination_country_id': destination_countryID,
                                                        'date': date,})
            return flights

        except Exception as e:
           return str(e)
       
       
    def get_arrival_flights_12hours(self,countryID:int):
        """
       01.02.24
       Mir Shukhman
       The func calls for get_stored_procedure from flights_repo (Repository class)
            to acess 'get_arrival_flights_12hours' stored procedure in the db
       Input: countryID (int)
       Output: get_stored_procedure func output (list of tupples/none/str err); Err str if err
       """
        try:
            flights=self.flights_repo.get_stored_procedure('get_arrival_flights_12hours',
                                                        {'countryID': countryID,})
            return flights

        except Exception as e:
            return str(e)
            
            
    def get_departure_flights_12hours(self,countryID:int):
        """
       01.02.24
       Mir Shukhman
       The func calls for get_stored_procedure from flights_repo (Repository class)
            to acess 'get_departure_flights_12hours' stored procedure in the db
       Input: countryID (int)
       Output: get_stored_procedure func output (list of tupples/none/str err); Err str if err
       """            
        try:
            flights=self.flights_repo.get_stored_procedure('get_departure_flights_12hours',
                                                        {'countryID': countryID,})
            return flights

        except Exception as e:
            return str(e)


    def check_if_customer_exists(self, *, username:str, email:str, phone_num:str, credit_card_num:str):
        """
       01.02.24
       Mir Shukhman
       The func calls for get_stored_procedure from customers_repo (Repository class)
            to acess 'check_if_customer_exists' stored procedure in the db
       Input: username (str),
            email (str),
            phone_num (str),
            credit_card_num (str),
            [all input by parameter name]       
        Output: get_stored_procedure func output (list of tupples/none/str err); Err str if err
       """
        try:
            existing_customer= self.customers_repo.get_stored_procedure('check_if_customer_exists',
                                                                        {'username' : username,
                                                                         'email' : email,
                                                                         'phone_num' : phone_num,
                                                                         'credit_card' : credit_card_num})
            if existing_customer:
                return existing_customer
            
            else:
                return None
            
        except Exception as e:
            return str(e)
        
        
    def check_if_airline_or_admin_exists(self, *, username:str, email:str):
        """
       01.02.24
       Mir Shukhman
       The func calls for get_stored_procedure from users_repo (Repository class)
            to acess 'check_if_airline_or_admin_exists' stored procedure in the db
       Input: username (str),
            email (str)
            [all input by parameter name]       
        Output: get_stored_procedure func output (list of tupples/none/str err); Err str if err
       """        
        try:
            existing_user= self.users_repo.get_stored_procedure('check_if_airline_or_admin_exists',
                                                                        {'username' : username,
                                                                         'email' : email,})
            if existing_user:
                return existing_user
            
            else:
                return None
            
        except Exception as e:
            return str(e)
    
    
    # Currently not in use
       
    def get_airline_by_user_ID(self, userID:int):
        """
       17.01.24
       Mir Shukhman
       The func calls for get_stored_procedure from airlines_repo (Repository class)
            to acess 'get_airline_by_userID' stored procedure in the db
       Input: userID (int)
       Output: get_stored_procedure func output (db.model obj/none/str err); Err str if err
       """
        try:
            airline=self.airlines_repo.get_stored_procedure('get_airline_by_userID',{'userID': userID})
            return airline

        except Exception as e:
           return str(e)
      
       
    def get_airlines_by_country_ID(self, countryID:int):
        """
       18.01.24
       Mir Shukhman
       The func calls for get_stored_procedure from airlines_repo (Repository class)
            to acess 'get_airlines_by_country' stored procedure in the db
       Input: countryID (int)
       Output: get_stored_procedure func output (list of db.model obj/none/str err); Err str if err
       """
        try:
            airlines=self.airlines_repo.get_stored_procedure('get_airlines_by_country',{'countryID': countryID})
            return airlines

        except Exception as e:
           return str(e)
       
       
    # For display
    
    def split_date_time(self,date_time_obj):
        """
       06.02.24
       Mir Shukhman
       The func formats datetime obj that comes from the database into 
        desirable strings of date and time for display.
       Input: date_time_obj (2024-01-29 03:17:00.000)     
        Output: tupple of str date ('%Y-%m-%d') and str time ('%H:%M')
       """       
        date_part = date_time_obj.date()
        time_part = date_time_obj.time()

        date = date_part.strftime('%Y-%m-%d')
        time = time_part.strftime('%H:%M')

        return date, time
    
    