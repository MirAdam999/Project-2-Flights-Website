from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

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
from business_logic.anonymous_facade import AnonymousFacade


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
    anon_facade=AnonymousFacade()
    
   
    with app.app_context():
        db.create_all()
        
        # Testing (and Crying)
        admin_facade=anon_facade.login(username='Admin1',_password='VerySecurePassword123')
        print(admin_facade.remove_administrator(2))
        print(admin_facade.remove_airline(2))
        print(admin_facade.remove_customer(7))
        
        
    app.run(debug=app.config['DEBUG'], use_reloader=False)