
from flask import Flask, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from routes.anonymous_routes import AnonymousBlueprint

class AdministratorBlueprint(AnonymousBlueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self.route('/all_flights', methods=['POST'])(self.all_flights)
        self.route('/searchforflightbyid', methods=['POST'])(self.search_for_flight_by_id)
        self.route('/closest_flights', methods=['POST'])(self.closest_flights)
        self.route('/search_for_closest_flights_by_country', methods=['POST'])(self.search_for_closest_flights_by_country)
        self.route('/manage_customers', methods=['POST'])(self.manage_customers)
        self.route('/search_for_customer_by_id', methods=['POST'])(self.search_for_customer_by_id)
        self.route('/add_customer_form', methods=['POST'])(self.add_customer_form)
        self.route('/add_customer', methods=['POST'])(self.add_customer)
        self.route('/customer_managment', methods=['POST','PUT'])(self.customer_managment)
        

    def all_flights(self):
        if self.user_role == "Administrator":
            all_flights = self.facade.get_all_flights()
            flights_to_display=[]
            if all_flights:
                for flight in all_flights:
                    airline= self.facade_base.get_airline_by_airline_ID(flight.AirlineID)   
                    airline_logo=airline.CompanyLogo
                    airline_name=airline.Name
                    
                    org_country_details= self.facade_base.get_country_by_ID(flight.OriginCountryID)
                    org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                    depart_date, depart_time= self.facade_base.split_date_time(flight.DepartureTime)
                    
                    dest_country_details= self.facade_base.get_country_by_ID(flight.DestinationCountryID)
                    dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                    land_date, land_time= self.facade_base.split_date_time(flight.LandingTime)
                    
                    remaning_tickets = flight.RemainingTickets
                    flight_status= flight.FlightStatus
                    
                    flights_to_display.append((airline_logo,airline_name,
                                            org_country_dispaly,
                                            depart_date,depart_time,
                                            dest_country_dispaly,
                                            land_date, land_time,
                                            remaning_tickets,flight_status))
                
                return render_template ("all_flights.html", flights=flights_to_display, role=self.user_role, name= self.users_name)
            
            else:
                return render_template ("all_flights.html", flights=None, role=self.user_role, name= self.users_name)
           
        
    def search_for_flight_by_id(self):
        flight_id=int(request.form['flight_id'])
        if self.user_role == "Administrator":
            flight= self.facade.get_flights_by_ID(flight_id)
            if flight:
                airline= self.facade_base.get_airline_by_airline_ID(flight.AirlineID)   
                airline_logo=airline.CompanyLogo
                airline_name=airline.Name
                
                org_country_details= self.facade_base.get_country_by_ID(flight.OriginCountryID)
                org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                depart_date, depart_time= self.facade_base.split_date_time(flight.DepartureTime)
                
                dest_country_details= self.facade_base.get_country_by_ID(flight.DestinationCountryID)
                dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                land_date, land_time= self.facade_base.split_date_time(flight.LandingTime)
                
                remaning_tickets = flight.RemainingTickets
                flight_status= flight.FlightStatus
                
                flight_to_display=[(airline_logo,airline_name,
                                        org_country_dispaly,
                                        depart_date,depart_time,
                                        dest_country_dispaly,
                                        land_date, land_time,
                                        remaning_tickets,flight_status)]
                
                return render_template ("all_flights.html", flights=flight_to_display, role=self.user_role, name= self.users_name)
            
            else:
                return render_template ("all_flights.html", flights=None, role=self.user_role, name= self.users_name)
            
            
    def closest_flights(self):
        if self.user_role == "Administrator":
            return render_template ("closest_flights.html", searched= False, 
                                    arrivals=None, departures=None, role=self.user_role, 
                                    name= self.users_name)
    
    
    def search_for_closest_flights_by_country(self):
        country=request.form['country']
        if self.user_role == "Administrator":
            arrivals= self.facade.get_arrival_flights_12hours(country)
            arrivals_to_display=[]
            if arrivals:
                for flight in arrivals:
                    airline= self.facade_base.get_airline_by_airline_ID(flight[1])   
                    airline_logo=airline.CompanyLogo
                    airline_name=airline.Name
                    
                    org_country_details= self.facade_base.get_country_by_ID(flight[2])
                    org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                    depart_date, depart_time= self.facade_base.split_date_time(flight[4])
                    
                    dest_country_details= self.facade_base.get_country_by_ID(country)
                    dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                    land_date, land_time= self.facade_base.split_date_time(flight[5])
                    
                    flight_status= flight[7]
                    
                    arrivals_to_display.append((airline_logo,airline_name,
                                            org_country_dispaly,
                                            depart_date,depart_time,
                                            dest_country_dispaly,
                                                land_date, land_time,flight_status))
            
            departures= self.facade.get_departure_flights_12hours(country)
            departures_to_display=[]
            if departures:
                for flight in departures:
                    airline= self.facade_base.get_airline_by_airline_ID(flight[1])   
                    airline_logo=airline.CompanyLogo
                    airline_name=airline.Name
                    
                    org_country_details= self.facade_base.get_country_by_ID(country)
                    org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                    depart_date, depart_time= self.facade_base.split_date_time(flight[3])
                    
                    dest_country_details= self.facade_base.get_country_by_ID(country)
                    dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                    land_date, land_time= self.facade_base.split_date_time(flight[5])
                    
                    flight_status= flight[7]
                    
                    departures_to_display.append((airline_logo,airline_name,
                                            org_country_dispaly,
                                            depart_date,depart_time,
                                            dest_country_dispaly,
                                                land_date, land_time,flight_status))
                    
            return render_template ("closest_flights.html", searched= True, 
                        arrivals=arrivals_to_display, departures=departures_to_display, role=self.user_role, 
                        name= self.users_name)
    
    
    def manage_customers(self):
        if self.user_role == "Administrator":
            all_customers = self.facade.get_all_customers()
            customers_to_display=[]
            if all_customers:
                for customer in all_customers:
                    custID= customer.CustomerID
                    fnmae=customer.FirstName
                    lname=customer.LastName
                    address=customer.Address 
                    phone=customer.PhoneNum
                    userID=customer.UserID 
                    user=self.facade_base.get_user_by_ID(userID)
                    username=user.Username
                    email=user.Email
                    
                    customers_to_display.append((custID,fnmae,lname,address,
                                                 phone,userID,username,email))
                    
                return render_template ("manage_custs.html", customers=customers_to_display, role=self.user_role, name= self.users_name)
            
            else:
                return render_template ("manage_custs.html", customers=None, role=self.user_role, name= self.users_name)
    
    
    def search_for_customer_by_id(self):
        customer_id=int(request.form['customer_id'])
        if self.user_role == "Administrator":
            customer = self.facade.get_customer_by_ID(customer_id)
            if customer:
                custID= customer.CustomerID
                fnmae=customer.FirstName
                lname=customer.LastName
                address=customer.Address 
                phone=customer.PhoneNum
                userID=customer.UserID 
                user=self.facade_base.get_user_by_ID(userID)
                username=user.Username
                email=user.Email
                
                customers_to_display=[(custID,fnmae,lname,address,
                                        phone,userID,username,email)]
                
                return render_template ("manage_custs.html", customers=customers_to_display, role=self.user_role, name= self.users_name)
        
            else:
                return render_template ("manage_custs.html", customers=None, role=self.user_role, name= self.users_name)
            
            
    def add_customer_form(self):
        if self.user_role == "Administrator":
            return render_template ("add_customer_by_manager.html", role=self.user_role, name= self.users_name)
    
    
    def add_customer(self):
        if self.user_role == "Administrator":
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
                    return render_template('add_customer_by_manager.html', countries=countries_to_display, error_message=error)
                    
                else:
                    new_customer= self.facade.add_customer_by_admin(username=form_username,_password=form_pass,
                                email=form_email,
                                first_name=fname,last_name=lname,
                                address=full_address,phone_num=full_phone,
                                _credit_num=full_credit)

                    if new_customer:
                        return render_template('add_customer_by_manager.html', countries=countries_to_display, adding_sucsess=True) 
                    
                    else:
                        return render_template('add_customer_by_manager.html', countries=countries_to_display, adding_sucsess=False)
                
            else:
                error= "Passwords Don't match. Try again."
                countries_to_display= self.countries_to_display() 
                return render_template('add_customer_by_manager.html', countries=countries_to_display, error_message=error)
    
    
    def customer_managment(self):
        if self.user_role == "Administrator":
            
            return render_template ("customer_managment.html", role=self.user_role, name= self.users_name)