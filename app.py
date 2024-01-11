from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pyodbc
import json

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
from logger import Logger

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
    
    admins_repo= Repository(Administrators)
    airlines_repo= Repository(AirlineCompanies)
    countries_repo= Repository(Countries)
    customers_repo= Repository(Customers)
    flights_repo= Repository(Flights)
    tickets_repo= Repository(Tickets)
    user_roles_repo= Repository(UserRoles)
    users_repo= Repository(Users)
    
    repo_logger= Logger
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=app.config['DEBUG'])