from flask import Flask, render_template, request
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

from business_logic.facade_base import FacadeBase

from repository import Repository

app = Flask(__name__)
app.config.from_pyfile('.config')
db.init_app(app)

if __name__ == "__main__":
    
    admins=Administrators()
    airlines=AirlineCompanies()
    countries=Countries()
    customers=Customers()
    flights=Flights()
    tickets=Tickets()
    user_roles=UserRoles()
    users=Users()
    
    facade_base=FacadeBase()
    
    with app.app_context():
        db.create_all()
        """
        admins_repo= Repository(Administrators)
        airlines_repo= Repository(AirlineCompanies)
        countries_repo= Repository(Countries)
        customers_repo= Repository(Customers)
        flights_repo= Repository(Flights)
        tickets_repo= Repository(Tickets)
        user_roles_repo= Repository(UserRoles)
        users_repo= Repository(Users)
        """
        
        # Testing (and Crying)
        """
        parameters = {
            "origin_country_id": 38,
            "destination_country_id": 106,
            "date": '2024-01-27'
        }
        print(flights_repo.get_stored_procedure('get_flights_by_parameters',parameters))
        """
        
        print(facade_base.get_country_by_ID(3))
        
    app.run(debug=app.config['DEBUG'], use_reloader=False)