from flask import Flask

from modules import db
from modules.administrators import Administrators
from modules.airline_companies import AirlineCompanies
from modules.countries import Countries
from modules.customers import Customers
from modules.flights import Flights
from modules.tickets import Tickets
from modules.user_roles import UserRoles
from modules.users import Users

from routes import Routes

app = Flask(__name__)
app.config.from_pyfile('.config')
db.init_app(app)

# Instanse of Blueprint classes
routes_blueprint = Routes('routes', __name__)
    
# Register Blueprints
app.register_blueprint(routes_blueprint)


if __name__ == "__main__":
    
    with app.app_context():       
        db.create_all()
        
    app.run(debug=app.config['DEBUG'], use_reloader=False, host='0.0.0.0',port=8080)