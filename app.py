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

facade_base=FacadeBase()
anon_facade=AnonymousFacade()


@app.route('/')
def index():
    list_of_countries= facade_base.get_all_countries()
    countries_to_display=[]
    for country in list_of_countries:
        country_name= f'{country.CountryName}, {country.Alpha3Code}'
        countries_to_display.append((country.CountryID,country_name))
              
    return render_template('index.html', logged_in=False, countries=countries_to_display)


@app.route('/searchforflight', methods = ['POST'])
def search_by_parameters():
    org_country=request.form['origin']
    dest_country=request.form['destination']
    chosen_date=request.form['date']
    
    # go to 
    
    db_flights=facade_base.get_flights_by_parameters(origin_countryID=org_country,
                                          destination_countryID=dest_country,
                                          date=chosen_date)
    
    flights_to_display=[]
    if db_flights:
        for flight in db_flights:
            airline= facade_base.get_airline_by_airline_ID(flight[1])   
            print(flight[1])
            airline_logo=airline.CompanyLogo
            airline_name=airline.Name
            
            org_country_details= facade_base.get_country_by_ID(org_country)
            org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
            depart_date, depart_time= facade_base.split_date_time(flight[4])
            
            dest_country_details= facade_base.get_country_by_ID(dest_country)
            dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
            land_date, land_time= facade_base.split_date_time(flight[5])
            
            flights_to_display.append((airline_logo,airline_name,
                                    org_country_dispaly,
                                    depart_date,depart_time,
                                    dest_country_dispaly,
                                        land_date, land_time))
            
    return render_template('flights_by_parameters.html', flights=flights_to_display)


@app.route('/redirect_to_signup')
def redirect_to_signup():
    return render_template('signup.html')

@app.route('/redirect_to_login')
def redirect_to_login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    pass

@app.route('/logout', methods = ['POST'])
def logout():
    pass


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