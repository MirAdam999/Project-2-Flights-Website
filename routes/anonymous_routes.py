
from flask import Flask, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from business_logic.facade_base import FacadeBase
from business_logic.anonymous_facade import AnonymousFacade

facade_base=FacadeBase()
anon_facade=AnonymousFacade()

class AnonymousBlueprint(Blueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self._facade= None
        self.token=None
        self.route('/', methods=['GET','POST'])(self.index)
        self.route('/searchforflight', methods=['POST'])(self.search_by_parameters)
        self.route('/redirect_to_signup')(self.redirect_to_signup)
        self.route('/redirect_to_login')(self.redirect_to_login)
        self.route('/login', methods=['POST'])(self.login)
        self.route('/signup', methods=['POST'])(self.signup)
  
    @property
    def facade(self):
        return self._facade
     
    @facade.setter
    def facade(self, new_facade):
        self._facade = new_facade
        
    def login(self):
        form_username=request.form['username']
        form_password=request.form['password']
        facade=anon_facade.login(username=form_username,_password=form_password)
        if facade:
            self.facade=facade
            self.token=self.facade.token
            return self.index(login=self.token)
        
        else:
            return self.login()
        
            
    def index(self, login=None):
        list_of_countries= facade_base.get_all_countries()
        countries_to_display=[]
        for country in list_of_countries:
            country_name= f'{country.CountryName}, {country.Alpha3Code}'
            countries_to_display.append((country.CountryID,country_name))
                
        return render_template('index.html', logged_in=login, countries=countries_to_display)


    def search_by_parameters(self):
        org_country=request.form['origin']
        dest_country=request.form['destination']
        chosen_date=request.form['date']
        
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


    def redirect_to_signup(self):
        return render_template('signup.html')


    def redirect_to_login(self):
        return render_template('login.html')
    
       
    def signup(self):
        pass