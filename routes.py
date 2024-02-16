
from flask import Flask, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

from business_logic.facade_base import FacadeBase
from business_logic.anonymous_facade import AnonymousFacade


class Routes(Blueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self.facade_base=FacadeBase()
        self.anon_facade=AnonymousFacade()
        self._facade= None
        self.token= None
        self.user_ID=None
        self.users_name= None
        self.user_role=  None
        # Anonymous/Base Routes
        self.route('/', methods=['GET','POST'])(self.index)
        self.route('/login', methods=['POST'])(self.login)
        self.route('/signup', methods=['POST'])(self.signup) 
        self.route('/logout')(self.logout)
        self.route('/change_password_form', methods=['POST'])(self.change_password_form)
        self.route('/change_password', methods=['POST','PUT'])(self.change_password)
        self.route('/redirect_to_signup')(self.redirect_to_signup)
        self.route('/redirect_to_login')(self.redirect_to_login)
        self.route('/redirect_to_searchforflightbyid')(self.redirect_to_searchforflightbyid)
        self.route('/searchforflight', methods=['POST'])(self.search_by_parameters)
        self.route('/closest_flights')(self.closest_flights)
        self.route('/search_for_closest_flights_by_country', methods=['POST'])(self.search_for_closest_flights_by_country)
        self.route('/searchforflightbyid', methods=['POST'])(self.search_for_flight_by_id)
        # Admin Routes
        self.route('/admin_info', methods=['POST','PUT'])(self.admin_info)
        self.route('/update_admin', methods=['POST','PUT'])(self.update_admin)
        self.route('/all_flights', methods=['POST'])(self.all_flights)
            # Cust managment
        self.route('/manage_customers', methods=['POST'])(self.manage_customers)
        self.route('/search_for_customer_by_id', methods=['POST'])(self.search_for_customer_by_id)
        self.route('/add_customer_form', methods=['POST'])(self.add_customer_form)
        self.route('/add_customer', methods=['POST'])(self.add_customer)
        self.route('/disactivate_customer', methods=['POST','PUT'])(self.disactivate_customer)
        self.route('/reactivate_customer', methods=['POST','PUT'])(self.reactivate_customer)
            # Airline managment
        self.route('/manage_airlines', methods=['POST'])(self.manage_airlines)
        self.route('/search_for_airline_by_id', methods=['POST'])(self.search_for_airline_by_id)
        self.route('/add_airline_form', methods=['POST'])(self.add_airline_form)
        self.route('/add_airline', methods=['POST'])(self.add_airline)
        self.route('/disactivate_airline', methods=['POST','PUT'])(self.disactivate_airline)
        self.route('/reactivate_airline', methods=['POST','PUT'])(self.reactivate_airline)
            # Admin managment
        self.route('/manage_admins', methods=['POST'])(self.manage_admins)
        self.route('/search_for_admin_by_id', methods=['POST'])(self.search_for_admin_by_id)
        self.route('/add_admin_form', methods=['POST'])(self.add_admin_form)
        self.route('/add_admin', methods=['POST'])(self.add_admin)
        self.route('/disactivate_admin', methods=['POST','PUT'])(self.disactivate_admin)
        self.route('/reactivate_admin', methods=['POST','PUT'])(self.reactivate_admin)
        # Airline Routes
        self.route('/airline_info', methods=['POST','PUT'])(self.airline_info)
        self.route('/update_airline', methods=['POST','PUT'])(self.update_airline)
        self.route('/add_flight', methods=['POST'])(self.add_flight)
        self.route('/add_flight_form', methods=['POST'])(self.add_flight_form)
        self.route('/manage_flights', methods=['POST'])(self.manage_flights)
        self.route('/update_flight', methods=['POST','PUT'])(self.update_flight)
        self.route('/update_flight_form', methods=['POST'])(self.update_flight_form)
        # Customer Routes
        self.route('/customer_info', methods=['POST','PUT'])(self.customer_info)
        self.route('/update_customer', methods=['POST','PUT'])(self.update_customer)
        self.route('/my_tickets', methods=['POST','PUT'])(self.my_tickets)
        self.route('/cancel_ticket', methods=['POST','PUT'])(self.cancel_ticket)
        self.route('/buy_ticket', methods=['POST','PUT'])(self.buy_ticket)

  
    @property
    def facade(self):
        return self._facade
     
    @facade.setter
    def facade(self, new_facade):
        self._facade = new_facade
        
    def countries_to_display(self):
        """
       06.02.24
       Mir Shukhman
       The func calls get_all_countries func and formats the data for
        display into desirable strings of Alph3Codes and CountryNames, 
        and tupples with countryID
        Input: None     
        Output: list of tupples: countryID (int), country name+code (str)
       """           
        list_of_countries= self.facade_base.get_all_countries()
        countries_to_display=[]
        for country in list_of_countries:
            country_name= f'{country.CountryName}, {country.Alpha3Code}'
            countries_to_display.append((country.CountryID,country_name))
            
        return countries_to_display
    
       
    def login(self):
        form_username=request.form['username']
        form_password=request.form['password']
        facade, err=self.anon_facade.login(username=form_username,_password=form_password)
        if facade:
            self._facade=facade
            self.token=self.facade.token
            self.user_ID= int(self.token[0])
            self.users_name= str(self.token[1]) 
            self.user_role= str(self.token[2])
            return self.index()
        
        else:
            return render_template ("login.html", error=err)
        
           
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
                flight_num=flight[0]
                
                flights_to_display.append((airline_logo,airline_name,
                                        org_country_dispaly,
                                        depart_date,depart_time,
                                        dest_country_dispaly,
                                            land_date, land_time,flight_status,flight_num))
                
        countries_to_display= self.countries_to_display() 
             
        return render_template('flights_by_parameters.html', flights=flights_to_display, role=self.user_role, 
                               name= self.users_name,countries=countries_to_display)


    def redirect_to_signup(self):
        countries_to_display= self.countries_to_display()     
        return render_template('signup.html', countries=countries_to_display)


    def redirect_to_login(self):
        return render_template('login.html')
    
    
    def redirect_to_searchforflightbyid(self):
        countries_to_display= self.countries_to_display()  
        return render_template('all_flights.html', countries=countries_to_display,
                               flights=None, role=self.user_role, name= self.users_name)
    
    
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

    
    def change_password_form(self):
        if self.user_role:
            return render_template("change_password.html", role=self.user_role, name= self.users_name)
    
    
    def change_password(self):
        if self.user_role:
            error = None
            
            old_pass=request.form['old_password']
            new_pass=request.form['new_password']
            pass_repeat=request.form['password_reinput']
            
            if new_pass == pass_repeat:
                user_data= self.facade.get_user_by_ID(self.user_ID)
                user_pass=user_data.Password
                
                if user_pass==old_pass:
                    if self.user_role=="Customer":
                        update_pass= self.facade.update_customer(new_user_data={'Password':new_pass},
                                                                 new_cust_data=None)
                    elif self.user_role=="AirlineCompany":
                        update_pass= self.facade.update_airline(new_user_data={'Password':new_pass},
                                                                 new_airline_data=None)
                    elif self.user_role=="Administrator":
                        update_pass= self.facade.update_admin(new_user_data={'Password':new_pass},
                                                                 new_admin_data=None)
                        
                    if update_pass:
                        return render_template('change_password.html', update_sucsess=True,
                                            role=self.user_role, name= self.users_name) 
                    
                    else:
                        return render_template('change_password.html', update_sucsess=False,
                                            role=self.user_role, name= self.users_name)
                else:
                    error= "Incorrect Old Password."
                    return render_template('change_password.html', error_message=error,
                                       role=self.user_role, name= self.users_name)
            else:
                error= "Passwords Don't match. Try again."
                return render_template('change_password.html', error_message=error,
                                       role=self.user_role, name= self.users_name)
    
    
    def search_for_flight_by_id(self):
        flight_id=int(request.form['flight_id'])
        flight= self.facade_base.get_flights_by_ID(flight_id)
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
            
            flight_num=flight.FlightID
            remaning_tickets = flight.RemainingTickets
            flight_status= flight.FlightStatus
            
            flight_to_display=[(airline_logo,airline_name,
                                    org_country_dispaly,
                                    depart_date,depart_time,
                                    dest_country_dispaly,
                                    land_date, land_time,
                                    remaning_tickets,flight_status,flight_num)]
            
            return render_template ("all_flights.html", flights=flight_to_display, role=self.user_role, name= self.users_name)
        
        else:
            return render_template ("all_flights.html", flights=None, role=self.user_role, name= self.users_name)
    
    
    def closest_flights(self):
        countries_to_display= self.countries_to_display()
        return render_template ("closest_flights.html", searched= False,
                                countries=countries_to_display, 
                                arrivals=None, departures=None, role=self.user_role, 
                                name= self.users_name)

    
    def search_for_closest_flights_by_country(self):
        country=request.form['country']
        countries_to_display= self.countries_to_display()
        arrivals= self.facade_base.get_arrival_flights_12hours(country)
        arrivals_to_display=[]
        if arrivals:
            for flight in arrivals:
                airline= self.facade_base.get_airline_by_airline_ID(flight.AirlineID)   
                airline_logo=airline.CompanyLogo
                airline_name=airline.Name
                
                org_country_details= self.facade_base.get_country_by_ID(flight.OriginCountryID)
                org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                depart_date, depart_time= self.facade_base.split_date_time(flight.DepartureTime)
                
                dest_country_details= self.facade_base.get_country_by_ID(flight.DestinationCountryID)
                dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                land_date, land_time= self.facade_base.split_date_time(flight.LandingTime)
                
                flight_num=flight.FlightID
                remaning_tickets = flight.RemainingTickets
                flight_status= flight.FlightStatus
                
                arrivals_to_display.append((airline_logo,airline_name,
                                        org_country_dispaly,
                                        depart_date,depart_time,
                                        dest_country_dispaly,
                                        land_date, land_time,
                                        remaning_tickets,flight_status,flight_num))
        
        departures= self.facade_base.get_departure_flights_12hours(country)
        departures_to_display=[]
        if departures:
            for flight in departures:
                airline= self.facade_base.get_airline_by_airline_ID(flight.AirlineID)   
                airline_logo=airline.CompanyLogo
                airline_name=airline.Name
                
                org_country_details= self.facade_base.get_country_by_ID(flight.OriginCountryID)
                org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                depart_date, depart_time= self.facade_base.split_date_time(flight.DepartureTime)
                
                dest_country_details= self.facade_base.get_country_by_ID(flight.DestinationCountryID)
                dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                land_date, land_time= self.facade_base.split_date_time(flight.LandingTime)
                
                flight_num=flight.FlightID
                remaning_tickets = flight.RemainingTickets
                flight_status= flight.FlightStatus
                
                departures_to_display.append((airline_logo,airline_name,
                                        org_country_dispaly,
                                        depart_date,depart_time,
                                        dest_country_dispaly,
                                        land_date, land_time,
                                        remaning_tickets,flight_status,flight_num))
                
        return render_template ("closest_flights.html", searched= True, 
                    arrivals=arrivals_to_display, departures=departures_to_display,
                    countries=countries_to_display, role=self.user_role, 
                    name= self.users_name)
    
    
    # Admin Functionality
    
    def admin_info(self):
        if self.user_role == "Administrator":
            admin=self.facade.get_admin_data()
            adminID= admin.AdminID
            fnmae=admin.FirstName
            lname=admin.LastName
            userID=admin.UserID 
            user=self.facade_base.get_user_by_ID(userID)
            username=user.Username
            email=user.Email

            admin_to_display=(adminID,fnmae,lname,username,email)
            
            return render_template ("update_admin.html", admin=admin_to_display,
                                    role=self.user_role, name= self.users_name)
        
        
    def update_admin(self):
        if self.user_role == "Administrator":
            error = None
            
            form_username=request.form['username']
            form_pass=request.form['password']
            form_email=request.form['email']
            fname=request.form['fname']
            lname=request.form['lname']
            
            user_data= self.facade.get_user_by_ID(self.user_ID)
            user_pass=user_data.Password
            if user_pass==form_pass:
                new_user_data={'Username':form_username,'Email':form_email}
                new_admin_data={'FirstName':fname,'LastName':lname}
                updated_admin= self.facade.update_admin(new_user_data,new_admin_data)
            
                if updated_admin:
                    return render_template('update_admin.html', update_sucsess=True,
                                           role=self.user_role, name= self.users_name) 
                    
                else:
                    return render_template('update_admin.html', update_sucsess=False,
                                           role=self.user_role, name= self.users_name)
                
            else:
                error= "Incorrect Password."
                return render_template('update_admin.html',
                                       error_message=error, role=self.user_role, name= self.users_name)
                
    
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
                    
                    flight_num=flight.FlightID
                    remaning_tickets = flight.RemainingTickets
                    flight_status= flight.FlightStatus
                    
                    flights_to_display.append((airline_logo,airline_name,
                                            org_country_dispaly,
                                            depart_date,depart_time,
                                            dest_country_dispaly,
                                            land_date, land_time,
                                            remaning_tickets,flight_status,flight_num))
                
                return render_template ("all_flights.html", flights=flights_to_display, role=self.user_role, 
                                        name= self.users_name)
            
            else:
                return render_template ("all_flights.html", flights=None, role=self.user_role, name= self.users_name)
              
    
    def manage_customers(self,new_status_change=None):
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
                    active=user.IsActive
                    
                    status = "Active" if active == True else "Inactive"
                    customers_to_display.append((custID,fnmae,lname,address,
                                                 phone,userID,username,email, status,))
                    
                return render_template ("manage_custs.html", status_change=new_status_change,
                                        customers=customers_to_display,
                                        role=self.user_role, name= self.users_name)
            
            else:
                return render_template ("manage_custs.html", status_change=new_status_change,
                                        customers=None, role=self.user_role, name= self.users_name)
    
    
    def disactivate_customer(self):
        if self.user_role == "Administrator":
            cust_id=request.form.get('cust_id')
            disactivate=self.facade.deactivate_customer(cust_id)
            if disactivate==True:
                return self.manage_customers(new_status_change=("Disactivated",cust_id))
            
            else:
                return self.manage_customers()
    
    
    def reactivate_customer(self):
        if self.user_role == "Administrator":
            cust_id=request.form.get('cust_id')
            activate=self.facade.activate_customer(cust_id)
            if activate==True:
                return self.manage_customers(new_status_change=("Reactivated",cust_id))
            
            else:
                return self.manage_customers()
    
    
    def search_for_customer_by_id(self):
        customer_id=request.form['customer_id']
        if customer_id:
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
                    active=user.IsActive
                    
                    status = "Active" if active == True else "Inactive"
                    customers_to_display=[(custID,fnmae,lname,address,
                                            phone,userID,username,email,status)]
                    
                    return render_template ("manage_custs.html", customers=customers_to_display, 
                                            role=self.user_role, name= self.users_name)
        
                else:
                    return render_template ("manage_custs.html", customers=None, 
                                        role=self.user_role, name= self.users_name)
            
            
    def add_customer_form(self):
        if self.user_role == "Administrator":
            countries_to_display= self.countries_to_display()
            return render_template ("add_customer_by_manager.html",
                                    countries=countries_to_display,
                                    role=self.user_role, name= self.users_name)
    
    
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
                    return render_template('add_customer_by_manager.html', countries=countries_to_display, error_message=error,
                                           role=self.user_role, name= self.users_name)
                    
                else:
                    new_customer= self.facade.add_customer_by_admin(username=form_username,_password=form_pass,
                                email=form_email,
                                first_name=fname,last_name=lname,
                                address=full_address,phone_num=full_phone,
                                _credit_num=full_credit)

                    if new_customer:
                        countries_to_display= self.countries_to_display() 
                        return render_template('add_customer_by_manager.html', countries=countries_to_display, 
                                               adding_sucsess=True, new_cust_data=new_customer,
                                               role=self.user_role, name= self.users_name) 
                    
                    else:
                        countries_to_display= self.countries_to_display() 
                        return render_template('add_customer_by_manager.html', countries=countries_to_display, 
                                               adding_sucsess=False,role=self.user_role, name= self.users_name)
                
            else:
                error= "Passwords Don't match. Try again."
                countries_to_display= self.countries_to_display() 
                return render_template('add_customer_by_manager.html', countries=countries_to_display, error_message=error,
                                       role=self.user_role, name= self.users_name)
    
   
    def manage_airlines(self,new_status_change=None):
        if self.user_role == "Administrator":
            all_airlines = self.facade.get_all_airlines()
            airlines_to_display=[]
            if all_airlines:
                for airline in all_airlines:
                    airlineID= airline.AirlineID
                    name=airline.Name
                    countryID=airline.Country_ID
                    logo=airline.CompanyLogo
                    userID=airline.UserID 
                    user=self.facade_base.get_user_by_ID(userID)
                    username=user.Username
                    email=user.Email
                    active=user.IsActive
                    country=self.facade_base.get_country_by_ID(countryID)
                    country_name=f'{country.CountryName}, {country.Alpha3Code}'
                    
                    status = "Active" if active == True else "Inactive"
                    airlines_to_display.append((airlineID,name,countryID,logo
                                                ,userID,username,email, status,country_name))
                    
                return render_template ("manage_airlines.html", status_change=new_status_change,
                                        airlines=airlines_to_display,
                                        role=self.user_role, name= self.users_name)
            
            else:
                return render_template ("manage_airlines.html", status_change=new_status_change,
                                        airlines=None, role=self.user_role, name= self.users_name)
    
    
    def disactivate_airline(self):
        if self.user_role == "Administrator":
            airline_id=request.form.get('airline_id')
            disactivate=self.facade.deactivate_airline(airline_id)
            if disactivate==True:
                return self.manage_airlines(new_status_change=("Disactivated",airline_id))
            
            else:
                return self.manage_airlines()
    
    
    def reactivate_airline(self):
        if self.user_role == "Administrator":
            airline_id=request.form.get('airline_id')
            activate=self.facade.activate_airline(airline_id)
            if activate==True:
                return self.manage_airlines(new_status_change=("Reactivated",airline_id))
            
            else:
                return self.manage_airlines()
    
    
    def search_for_airline_by_id(self):
        airline_id=request.form['airline_id']
        if airline_id:
            if self.user_role == "Administrator":
                airline = self.facade.get_airline_by_airline_ID(airline_id)
                if airline:
                    airlineID= airline.AirlineID
                    name=airline.Name
                    countryID=airline.Country_ID
                    logo=airline.CompanyLogo
                    userID=airline.UserID 
                    user=self.facade_base.get_user_by_ID(userID)
                    username=user.Username
                    email=user.Email
                    active=user.IsActive
                    country=self.facade_base.get_country_by_ID(countryID)
                    country_name=f'{country.CountryName}, {country.Alpha3Code}'
                        
                    status = "Active" if active == True else "Inactive"
                    airlines_to_display=[(airlineID,name,countryID,logo
                                                ,userID,username,email, status,country_name)]
                    
                    return render_template ("manage_airlines.html", airlines=airlines_to_display, 
                                            role=self.user_role, name= self.users_name)
            
                else:
                    return render_template ("manage_airlines.html", airlines=None, 
                                        role=self.user_role, name= self.users_name)
            
            
    def add_airline_form(self):
        if self.user_role == "Administrator":
            countries_to_display= self.countries_to_display()
            return render_template ("add_airline.html",
                                    countries=countries_to_display,
                                    role=self.user_role, name= self.users_name)
    
    
    def add_airline(self):
        if self.user_role == "Administrator":
            error = None
            
            form_username=request.form['username']
            form_pass=request.form['password']
            pass_repeat=request.form['password_reinput']
            form_email=request.form['email']
            name=request.form['name']
            country=request.form['country']
            logo=request.form['logo']
            
            if form_pass == pass_repeat:
                
                check_if_airline_exists = self.facade_base.check_if_airline_or_admin_exists(
                                                                username=form_username, email= form_email)

                if check_if_airline_exists:
                    error = "Airline by given Username/ Email already exists."
                    countries_to_display= self.countries_to_display() 
                    return render_template('add_airline.html', countries=countries_to_display, error_message=error,
                                           role=self.user_role, name= self.users_name)
                    
                else:
                    new_airline= self.facade.add_airline(username=form_username,_password=form_pass,
                                                        email=form_email,name=name,countryID=country,
                                                        company_logo=logo)

                    if new_airline:
                        countries_to_display= self.countries_to_display() 
                        return render_template('add_airline.html', countries=countries_to_display, 
                                               adding_sucsess=True, new_airline_data=new_airline,
                                               role=self.user_role, name= self.users_name) 
                    
                    else:
                        countries_to_display= self.countries_to_display()
                        return render_template('add_airline.html', countries=countries_to_display, 
                                               adding_sucsess=False,role=self.user_role, name= self.users_name)
                
            else:
                error= "Passwords Don't match. Try again."
                countries_to_display= self.countries_to_display()
                return render_template('add_airline.html', countries=countries_to_display, error_message=error,
                                       role=self.user_role, name= self.users_name)
    
   
    def manage_admins(self,new_status_change=None):
        if self.user_role == "Administrator":
            all_admins = self.facade.get_all_administrators()
            admins_to_display=[]
            if all_admins:
                for admin in all_admins:
                    adminID= admin.AdminID
                    fname=admin.FirstName
                    lname=admin.LastName
                    userID=admin.UserID 
                    user=self.facade_base.get_user_by_ID(userID)
                    username=user.Username
                    email=user.Email
                    active=user.IsActive
                    
                    status = "Active" if active == True else "Inactive"
                    admins_to_display.append((adminID,fname,lname
                                                ,userID,username,email, status))
                    
                return render_template ("manage_admins.html", status_change=new_status_change,
                                        admins=admins_to_display,
                                        role=self.user_role, name= self.users_name,
                                        own_id=self.user_ID)
            
            else:
                return render_template ("manage_admins.html", status_change=new_status_change,
                                        admins=None, role=self.user_role, name= self.users_name)
    
    
    def disactivate_admin(self):
        if self.user_role == "Administrator":
            admin_id=request.form.get('admin_id')
            disactivate=self.facade.deactivate_administrator(admin_id)
            if disactivate==True:
                return self.manage_admins(new_status_change=("Disactivated",admin_id))
            
            else:
                return self.manage_admins()
    
    
    def reactivate_admin(self):
        if self.user_role == "Administrator":
            admin_id=request.form.get('admin_id')
            activate=self.facade.activate_administrator(admin_id)
            if activate==True:
                return self.manage_admins(new_status_change=("Reactivated",admin_id))
            
            else:
                return self.manage_admins()
    
    
    def search_for_admin_by_id(self):
        admin_id=request.form['admin_id']
        if admin_id:
            if self.user_role == "Administrator":
                admin = self.facade.get_admin_by_adminID(admin_id)
                if admin:
                    adminID= admin.AdminID
                    fname=admin.FirstName
                    lname=admin.LastName
                    userID=admin.UserID 
                    user=self.facade_base.get_user_by_ID(userID)
                    username=user.Username
                    email=user.Email
                    active=user.IsActive
                        
                    status = "Active" if active == True else "Inactive"
                    admins_to_display=[(adminID,fname,lname
                                        ,userID,username,email, status)]
                    
                    return render_template ("manage_admins.html", admins=admins_to_display, 
                                            own_id=self.user_ID,
                                            role=self.user_role, name= self.users_name)
            
                else:
                    return render_template ("manage_admins.html",admins=None, 
                                        role=self.user_role, name= self.users_name)
            
            
    def add_admin_form(self):
        if self.user_role == "Administrator":
            countries_to_display= self.countries_to_display()
            return render_template ("add_admin.html",
                                    countries=countries_to_display,
                                    role=self.user_role, name= self.users_name)
    
    
    def add_admin(self):
        if self.user_role == "Administrator":
            error = None
            
            form_username=request.form['username']
            form_pass=request.form['password']
            pass_repeat=request.form['password_reinput']
            form_email=request.form['email']
            fname=request.form['fname']
            lname=request.form['lname']

            
            if form_pass == pass_repeat:
                
                check_if_admin_exists = self.facade_base.check_if_airline_or_admin_exists(
                                                                username=form_username, email= form_email)

                if check_if_admin_exists:
                    error = "Admin by given Username/ Email already exists."
                    countries_to_display= self.countries_to_display() 
                    return render_template('add_admin.html', countries=countries_to_display, error_message=error,
                                           role=self.user_role, name= self.users_name)
                    
                else:
                    new_admin= self.facade.add_administrator(username=form_username,_password=form_pass,
                                                        email=form_email,first_name=fname,last_name=lname)

                    if new_admin:
                        countries_to_display= self.countries_to_display()
                        return render_template('add_admin.html', countries=countries_to_display, 
                                               adding_sucsess=True, new_admin_data=new_admin,
                                               role=self.user_role, name= self.users_name) 
                    
                    else:
                        countries_to_display= self.countries_to_display()
                        return render_template('add_admin.html', countries=countries_to_display, 
                                               adding_sucsess=False,role=self.user_role, name= self.users_name)
                
            else:
                error= "Passwords Don't match. Try again."
                countries_to_display= self.countries_to_display()
                return render_template('add_admin.html', countries=countries_to_display, error_message=error,
                                       role=self.user_role, name= self.users_name)
    
    
    # Airline Functionality
    
    def airline_info(self):
        if self.user_role == "AirlineCompany":
            airline=self.facade.get_airline_data()
            airlineID= airline.AirlineID
            name=airline.Name
            countryID=airline.Country_ID
            logo=airline.CompanyLogo
            userID=airline.UserID 
            user=self.facade_base.get_user_by_ID(userID)
            username=user.Username
            email=user.Email

            airline_to_display=(airlineID,name,countryID,
                                 logo,username,email)
            
            countries_to_display=self.countries_to_display()
            
            return render_template ("update_airline.html", airline=airline_to_display,
                                    countries=countries_to_display,
                                    role=self.user_role, name= self.users_name)
        
        
    def update_airline(self):
        if self.user_role == "AirlineCompany":
            error = None
            
            form_username=request.form['username']
            form_pass=request.form['password']
            form_email=request.form['email']
            name=request.form['name']
            country=request.form['country']
            logo=request.form['logo']
            
            user_data= self.facade.get_user_by_ID(self.user_ID)
            user_pass=user_data.Password
            if user_pass==form_pass:
                new_user_data={'Username':form_username,'Email':form_email}
                new_cust_data={'Name':name,'Country_ID':country,'CompanyLogo':logo}
                updated_airline= self.facade.update_airline(new_user_data,new_cust_data)
            
                if updated_airline:
                    countries_to_display= self.countries_to_display()
                    return render_template('update_airline.html', countries=countries_to_display, update_sucsess=True,
                                           role=self.user_role, name= self.users_name) 
                    
                else:
                    countries_to_display= self.countries_to_display()
                    return render_template('update_airline.html', countries=countries_to_display, update_sucsess=False,
                                           role=self.user_role, name= self.users_name)
                
            else:
                error= "Incorrect Password."
                countries_to_display= self.countries_to_display()
                return render_template('update_airline.html', countries=countries_to_display,
                                       error_message=error, role=self.user_role, name= self.users_name)
                
                
    def add_flight_form(self):
        if self.user_role == "AirlineCompany":
            countries_to_display=self.countries_to_display()
            
            return render_template('add_flight.html', countries=countries_to_display,
                                       role=self.user_role, name= self.users_name)
            
            
    def add_flight(self):
        if self.user_role == "AirlineCompany":
            error = None
            
            org=int(request.form['origin'])
            dest=int(request.form['destination'])
            form_departure=request.form['departure']
            strip_departure=datetime.strptime(form_departure, "%Y-%m-%dT%H:%M")
            departure=strip_departure.strftime("%Y-%m-%d %H:%M:%S.000")
            form_arrival=request.form['arrival']
            strip_arrival=datetime.strptime(form_arrival, "%Y-%m-%dT%H:%M")
            arrival=strip_arrival.strftime("%Y-%m-%d %H:%M:%S.000")
            tickets=int(request.form['tickets'])
            
            if departure < arrival:

                if org == dest:
                    error = "Origin and Destination countries cannot be the same. Try again."
                    countries_to_display= self.countries_to_display() 
                    return render_template('add_flight.html', countries=countries_to_display, error_message=error,
                                           role=self.user_role, name= self.users_name)
                    
                else:
                    new_flight= self.facade.add_flight(org_countryID=org, dest_countryID=dest,
                    depart_time=departure, land_time=arrival, tickets=tickets)
                    
                    if new_flight:
                        countries_to_display= self.countries_to_display()
                        return render_template('add_flight.html', countries=countries_to_display, 
                                               adding_sucsess=True, new_flight_data=new_flight,
                                               role=self.user_role, name= self.users_name) 
                    
                    else:
                        countries_to_display= self.countries_to_display()
                        return render_template('add_flight.html', countries=countries_to_display, 
                                               adding_sucsess=False,role=self.user_role, name= self.users_name)
                
            else:
                error= "Landing date-time is earlier than Departure date-time. Try again."
                countries_to_display= self.countries_to_display()
                return render_template('add_flight.html', countries=countries_to_display, error_message=error,
                                       role=self.user_role, name= self.users_name)
    
    
    def manage_flights(self):
        if self.user_role == "AirlineCompany":
            my_flights = self.facade.get_my_flights()
            flights_to_display=[]
            if my_flights:
                for flight in my_flights:
                    airline= self.facade_base.get_airline_by_airline_ID(flight.AirlineID)   
                    airline_logo=airline.CompanyLogo
                    airline_name=airline.Name
                    
                    org_country_details= self.facade_base.get_country_by_ID(flight.OriginCountryID)
                    org_country_dispaly= f'{org_country_details.CountryName}, {org_country_details.Alpha3Code}'
                    depart_date, depart_time= self.facade_base.split_date_time(flight.DepartureTime)
                    
                    dest_country_details= self.facade_base.get_country_by_ID(flight.DestinationCountryID)
                    dest_country_dispaly= f'{dest_country_details.CountryName}, {dest_country_details.Alpha3Code}'
                    land_date, land_time= self.facade_base.split_date_time(flight.LandingTime)
                    
                    flight_num=flight.FlightID
                    remaning_tickets = flight.RemainingTickets
                    flight_status= flight.FlightStatus
                    
                    flights_to_display.append((airline_logo,airline_name,
                                            org_country_dispaly,
                                            depart_date,depart_time,
                                            dest_country_dispaly,
                                            land_date, land_time,
                                            remaning_tickets,flight_status,flight_num))
                
                return render_template ("all_flights.html", flights=flights_to_display, role=self.user_role, 
                                        name= self.users_name)
            
            else:
                return render_template ("all_flights.html", flights=None, role=self.user_role, name= self.users_name)
            
            
    def update_flight_form(self):
        if self.user_role == "AirlineCompany":
            flight_id=int(request.form.get('flight_num'))
            flight=self.facade_base.get_flights_by_ID(flight_id)
            flightID= flight.FlightID
            org=flight.OriginCountryID
            org_name=self.facade_base.get_country_by_ID(org)
            org_to_display=f'{org_name.CountryName}, {org_name.Alpha3Code}'
            dest=flight.DestinationCountryID
            dest_name=self.facade_base.get_country_by_ID(dest)
            dest_to_display=f'{dest_name.CountryName}, {dest_name.Alpha3Code}'
            departure=flight.DepartureTime 
            arrival=flight.LandingTime
            tickets=flight.RemainingTickets
            status=flight.FlightStatus

            flight_to_display=(flightID,org_to_display,dest_to_display
                               ,departure,arrival,tickets,status)
            
            return render_template ("update_flight.html", flight=flight_to_display,
                                    role=self.user_role, name= self.users_name)
    
    
    def update_flight(self):
        if self.user_role == "AirlineCompany":
            error = None
            
            flightID=int(request.form['flightid'])
            print(flightID)
            form_departure=request.form['departure']
            strip_departure=datetime.strptime(form_departure, "%Y-%m-%dT%H:%M")
            departure=strip_departure.strftime("%Y-%m-%d %H:%M:%S.000")
            form_arrival=request.form['arrival']
            strip_arrival=datetime.strptime(form_arrival, "%Y-%m-%dT%H:%M")
            arrival=strip_arrival.strftime("%Y-%m-%d %H:%M:%S.000")
            tickets=request.form['tickets']
            status = request.form['status']
            
            if departure < arrival:
                updated_flight= self.facade.update_flight(flightID,{'DepartureTime':departure,
                                                                    'LandingTime':arrival,
                                                                    'RemainingTickets':tickets,
                                                                    'FlightStatus':status})
            
                if updated_flight:
                    return render_template ("update_flight.html",
                                    role=self.user_role, name= self.users_name,
                                    update_sucsess=True)
                    
                else:
                    return render_template ("update_flight.html",
                                    role=self.user_role, name= self.users_name
                                    ,update_sucsess=False)

            else:
                error= "Landing date-time is earlier than Departure date-time. Try again."
                return render_template ("update_flight.html",
                                    role=self.user_role, name= self.users_name,
                                    error_message=error)

        else:
            return render_template ("update_flight.html",
                            role=self.user_role, name= self.users_name
                            ,update_sucsess=False)
    
    
    # Customer Functionality
    
    def customer_info(self):
        if self.user_role == "Customer":
            customer=self.facade.get_customer_data()
            custID= customer.CustomerID
            fnmae=customer.FirstName
            lname=customer.LastName
            address=customer.Address 
            phone=customer.PhoneNum
            credit=customer.CreditCardNum
            userID=customer.UserID 
            user=self.facade_base.get_user_by_ID(userID)
            username=user.Username
            email=user.Email

            customer_to_display=(custID,fnmae,lname,address,
                                        phone,credit,username,email)
            
            return render_template ("update_customer.html", cust=customer_to_display,
                                    role=self.user_role, name= self.users_name)
        
        
    def update_customer(self):
        if self.user_role == "Customer":
            error = None
            
            form_username=request.form['username']
            form_pass=request.form['password']
            form_email=request.form['email']
            fname=request.form['fname']
            lname=request.form['lname']
            form_address=request.form['address']
            form_phone=request.form['phone']
            form_credit=request.form['credit_card']
            
            user_data= self.facade.get_user_by_ID(self.user_ID)
            user_pass=user_data.Password
            if user_pass==form_pass:
                new_user_data={'Username':form_username,'Email':form_email}
                new_cust_data={'FirstName':fname,'LastName':lname,'Address':form_address,
                               'PhoneNum':form_phone,'CreditCardNum':form_credit}
                updated_customer= self.facade.update_customer(new_user_data,new_cust_data)
            
                if updated_customer:
                    return render_template('update_customer.html', update_sucsess=True,
                                           role=self.user_role, name= self.users_name) 
                    
                else:
                    return render_template('update_customer.html', update_sucsess=False,
                                           role=self.user_role, name= self.users_name)
                
            else:
                error= "Incorrect Password."
                return render_template('update_customer.html',
                                       error_message=error, role=self.user_role, name= self.users_name)
                
                
    def my_tickets(self,canceled_ticket=None):
        if self.user_role == "Customer":
            my_tickets=self.facade.get_my_tickets()
            tickets_to_display=[]
            if my_tickets:
                for ticket in my_tickets:
                    ticket_id=ticket[0]
                    flight=ticket[1]
                    org_country=ticket[2]
                    dest_country=ticket[3]
                    airline= self.facade_base.get_airline_by_airline_ID(flight.AirlineID)   
                    airline_logo=airline.CompanyLogo
                    airline_name=airline.Name
                    depart_date, depart_time= self.facade_base.split_date_time(flight.DepartureTime)
                    land_date, land_time= self.facade_base.split_date_time(flight.LandingTime)
                    
                    flight_num=flight.FlightID
                    flight_status= flight.FlightStatus
                    
                    tickets_to_display.append((ticket_id,
                            airline_logo,airline_name,
                            org_country,
                            depart_date,depart_time,
                            dest_country,
                            land_date, land_time,
                            flight_status,flight_num))

            return render_template ("my_tickets.html", tickets=tickets_to_display,
                                    role=self.user_role, name= self.users_name,
                                    canceled_ticket=canceled_ticket)
    
    
    def cancel_ticket(self):
        if self.user_role == "Customer":
            ticket_id=request.form.get('ticket_id')
            print(ticket_id)
            cancel=self.facade.remove_ticket(ticket_id)
            print(cancel)
            
            if cancel:
                return self.my_tickets(canceled_ticket=ticket_id)
            
            else:
                return self.my_tickets()
    
    
    def buy_ticket(self):
        if self.user_role == "Customer":
            flight_id=int(request.form.get('flight_num'))
            buy, err=self.facade.add_ticket(flight_id)
            
            if buy:
                return render_template ("ticket_purchase.html", new_ticket=buy,
                        role=self.user_role, name= self.users_name)
            elif err:
                return render_template ("ticket_purchase.html", new_ticket=None,
                        role=self.user_role, name= self.users_name, error=err)
               
            else:
                return self.index()