from flask import Flask
import secrets

from modules import db
from modules.administrators import Administrators
from modules.airline_companies import AirlineCompanies
from modules.countries import Countries
from modules.customers import Customers
from modules.flights import Flights
from modules.tickets import Tickets
from modules.user_roles import UserRoles
from modules.users import Users

from routes.anonymous_routes import AnonymousBlueprint
from routes.administrator_routes import AdministratorBlueprint
#from routes.airline_routes import AirlineBlueprint
#from routes.customer_routes import CustomerBlueprint

app = Flask(__name__)
app.config.from_pyfile('.config')
db.init_app(app)
app.secret_key = secrets.token_hex(16)

# Instantiate Blueprint classes
anon_blueprint = AnonymousBlueprint('anon_blueprint', __name__)
admin_blueprint = AdministratorBlueprint('admin_blueprint', __name__)
#airline_blueprint = AirlineBlueprint('airline_blueprint', __name__)
#customer_blueprint = CustomerBlueprint('customer_blueprint', __name__)
    
# Register Blueprints with your app
app.register_blueprint(anon_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
#app.register_blueprint(airline_blueprint, url_prefix='/airline')
#app.register_blueprint(customer_blueprint, url_prefix='/customer')


if __name__ == "__main__":
    
    admins=Administrators()
    airlines=AirlineCompanies()
    countries=Countries()
    customers=Customers()
    flights=Flights()
    tickets=Tickets()
    user_roles=UserRoles()
    users=Users()
      
    with app.app_context():
        db.create_all()
        
        # Testing (and Crying)
        

        
    app.run(debug=app.config['DEBUG'], use_reloader=False)