from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pyodbc

from modules import db
from modules.administrators import Administrators
from modules.airline_companies import AirlineCompanies
from modules.countries import Countries
from modules.customers import Customers
from modules.flights import Flights
from modules.tickets import Tickets
from modules.user_roles import UserRoles
from modules.users import Users
from repository import Repository

class FacadeBase:
    def __init__(self):
        self.admins_repo= Repository(Administrators)
        self.airlines_repo= Repository(AirlineCompanies)
        self.countries_repo= Repository(Countries)
        self.customers_repo= Repository(Customers)
        self.flights_repo= Repository(Flights)
        self.tickets_repo= Repository(Tickets)
        self.user_roles_repo= Repository(UserRoles)
        self.users_repo= Repository(Users)
      
    def _create_new_user(self,_user):
       """
       17.01.24
       Mir Shukhman
       Input new user data
       Calls for add func from users_repo (Repository class)
       Internal usage only! Does not update admins/airlines/customers tables
       """
       try:
           if self.users_repo.add(_user) == True:
               return True
           
           else:
               return False, self.users_repo.add(_user)
           
       except Exception as e:
           return str(e)
    
    
    def get_country_by_ID(self, countryID=int):
        """
       17.01.24
       Mir Shukhman
       Input country ID
       Calls for get_by_id func from countries_repo (Repository class)
       Output country data
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
       Input None
       Calls for get_allfunc from countries_repo (Repository class)
       Output all countries data
       """
        try:
            all_countries=self.countries_repo.get_all()
            return all_countries
        
        except Exception as e:
           return str(e)
       
    def get_airline_by_user_ID(self, userID):
        """
       17.01.24
       Mir Shukhman
       Input userID
       Calls for get_sp from airlines_repo (Repository class,
            to acess 'get_airline_by_userID' stored procedure in the db
       Output airline data
       """
        try:
            airline=self.airlines_repo.get_stored_procedure('get_airline_by_userID',{'userID': userID})
            return airline

        except Exception as e:
           return str(e)