
from flask import Flask, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from business_logic.facade_base import FacadeBase
from business_logic.anonymous_facade import AnonymousFacade


class AnonymousBlueprint(Blueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self.facade_base=FacadeBase()
        self.anon_facade=AnonymousFacade()
        self._facade= None
        self.token= None
        self.users_name= None
        self.user_role=  None
        self.route('/', methods=['GET','POST'])(self.index)
        self.route('/searchforflight', methods=['POST'])(self.search_by_parameters)
        self.route('/redirect_to_signup')(self.redirect_to_signup)
        self.route('/redirect_to_login')(self.redirect_to_login)
        self.route('/login', methods=['POST'])(self.login)
        self.route('/signup', methods=['POST'])(self.signup)
        self.route('/logout', methods=['POST'])(self.logout)

  
    @property
    def facade(self):
        return self._facade
     
    @facade.setter
    def facade(self, new_facade):
        self._facade = new_facade
        
    def login(self):
        form_username=request.form['username']
        form_password=request.form['password']
        facade=self.anon_facade.login(username=form_username,_password=form_password)
        if facade:
            self._facade=facade
            self.token=self.facade.token
            self.users_name= str(self.token[1]) 
            self.user_role= str(self.token[2]) 
            return self.index()
        
        else:
            return self.login()
        
           
    def index(self):
        countries_to_display= self.countries_to_display()         
        return render_template('index.html', countries=countries_to_display,role=self.user_role, name= self.users_name)


    def search_by_parameters(self):
        org_country=request.form['origin']
        dest_country=request.form['destination']
        chosen_date=request.form['date']
        
        db_flights=self.facade_base.get_flights_by_parameters(origin_countryID=org_country,
                                            destination_countryID=dest_country,
                                            date=chosen_date)
        
        flights_to_display=[]
        if db_flights:
            for flight in db_flights:
                airline= self.facade_base.get_airline_by_airline_ID(flight[1])   
                airline_logo=airline.CompanyLogo
                airline_name=airline.Name
                
                org_country_details= self.facade_base.get_country_by_ID(org_country)
                org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                depart_date, depart_time= self.facade_base.split_date_time(flight[4])
                
                dest_country_details= self.facade_base.get_country_by_ID(dest_country)
                dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                land_date, land_time= self.facade_base.split_date_time(flight[5])
                
                flight_status= flight[7]
                
                flights_to_display.append((airline_logo,airline_name,
                                        org_country_dispaly,
                                        depart_date,depart_time,
                                        dest_country_dispaly,
                                            land_date, land_time,flight_status))
                
        return render_template('flights_by_parameters.html', flights=flights_to_display, role=self.user_role, name= self.users_name)


    def redirect_to_signup(self):
        countries_to_display= self.countries_to_display()     
        return render_template('signup.html', countries=countries_to_display)


    def redirect_to_login(self):
        return render_template('login.html')
    
       
    def signup(self):
        error = None
        
        form_username=request.form['username']
        form_pass=request.form['password']
        pass_repeat=request.form['password_reinput']
        form_email=request.form['email']
        fname=request.form['fname']
        lname=request.form['lname']
        country=request.form['country']
        form_address=request.form['address']
        country_code=request.form['phone_country_code']
        form_phone=request.form['phone']
        form_credit=request.form['credit_card']
        form_credit_exp=request.form['credit_card_exp_date']
        form_credit_cvv=request.form['credit_card_cvv']
        
        if form_pass == pass_repeat:
            
            full_address= str(f'{country} {form_address}')
            full_phone = str(f'+{country_code}{form_phone}')
            full_credit = str(f'{form_credit}, {form_credit_exp}, {form_credit_cvv}')
            
            check_if_customer_exists = self.facade_base.check_if_customer_exists(username=form_username, email= form_email,
                                                                            phone_num= full_phone,
                                                                            credit_card_num= full_credit)

            if check_if_customer_exists:
                error = "Customer by given Username/ Email/ Phone Number/ Credit Card Number, already exists."
                countries_to_display= self.countries_to_display() 
                return render_template('signup.html', countries=countries_to_display, error_message=error)
                
            else:
                new_customer= self.anon_facade.add_customer(username=form_username,_password=form_pass,
                            email=form_email,
                            first_name=fname,last_name=lname,
                            address=full_address,phone_num=full_phone,
                            _credit_num=full_credit)

                if new_customer:
                    return render_template('signup_result.html', fullname= str(f'{fname} {lname}')) 
                
                else:
                    return render_template('signup_result.html', fullname= None)
            
        else:
            error= "Passwords Don't match. Try again."
            countries_to_display= self.countries_to_display() 
            return render_template('signup.html', countries=countries_to_display, error_message=error)
        
         
    def logout(self):
        self._facade= None
        self.token= None
        self.users_name= None
        self.user_role= None 
        return self.index()
    
    
    def closest_arrivals(self):
        pass
    
    
    def closest_departures(self):
        pass
    
    
    def closes_flights(self):
        pass
    
    
    def serach_by_flight_ID(self):
        pass
    
    
    def countries_to_display(self):
        list_of_countries= self.facade_base.get_all_countries()
        countries_to_display=[]
        for country in list_of_countries:
            country_name= f'{country.CountryName}, {country.Alpha3Code}'
            countries_to_display.append((country.CountryID,country_name))
            
        return countries_to_display
            