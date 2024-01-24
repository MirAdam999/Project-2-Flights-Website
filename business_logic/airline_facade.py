
from business_logic.facade_base import FacadeBase

from modules.flights import Flights

# 24.01.24
# Mir Shukhman
# Defining class AirlineFacade wich inherits from FacadeBase,
#   recives the login token through the init from login func in AnonymousFacade,
#   and will hold update_airline, add_flight, update_flight, remove_flight, cancel_flight, get_my_flights funcs.


class AirlineFacade(FacadeBase):
    def __init__(self, token):
        super().__init__()
        # Inherts FacadeBase init, login token from AnonymousFacade
        # Devides the login token into ID, name and role
        # Calls _get_airline_ID to get airlineID using userId from the token
        self.token= token
        self.token_userID= self.token[0]
        self.token_airline_name= self.token[1]
        self.token_role= self.token[2]
        self.airlineID = self._get_airline_ID()
        
    def _get_airline_ID(self):
        """
        24.01.24
        Mir Shukhman
        Func to retrive airline's ID using userID from the login token,
        Calls for get_stored_procedure from airlines_repo (Repository class)
        to acess 'get_airline_by_userID' stored procedure in the db.
        Input: None
        Output: airlineID (int); None if not found; Err str if err
        ***Internal use only! Does not check facade or name with token***
        """
        try:
            airline=self.airlines_repo.get_stored_procedure('get_airline_by_userID',{'userID': self.token_userID})
            if airline:
                airlineID = airline[0][0]
                return airlineID
            
            else:
                return None
        
        except Exception as e:
            return str(e)
       
        
    def update_airline(self,new_data):
        """     
        24.01.24
        Mir Shukhman
        Update airline func, ensures facade matches token role,
        calls get_by_id func from airlines_repo to get airline's name from db,
        ensures airline's name from db matches token airline name,
        calls update func from airline_repo (Repository class).
        Input: new_data - as dict, example {'Country_ID': 33}
        Output: airlines_repo.update func output (updated airline's data/none/str err);
                False if facade dosen't match token role/no airline in db by given airlineId
                /airline's name from db dosen't token airline name;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='AirlineCompany':
                db_airline= self.airlines_repo.get_by_id(self.airlineID)
                # airline with token_ID found
                if db_airline:
                    name = str(db_airline.Name) # getting airline's name from db
                    
                    # ensuring airline's name from db matches token airline name
                    if name == self.token_airline_name:
                        updated_airline=self.airlines_repo.update(self.airlineID,new_data)
                        return updated_airline # returns updated airline's data/none/str err
                    
                    else:   # airline's name from db dosen't match token airline name
                        return False
                    
                else:   # no airline in db by given airlineId
                    return False
                
            else:   # facade dosen't match token role
                return False   
              
        except Exception as e:
            return str(e)
    
    
    def add_flight(self, *, org_countryID:int, dest_countryID:int,
                    depart_time:str, land_time:str, tickets:int):
        """ 
        24.01.24
        Mir Shukhman
        Add flight func, ensures facade matches token role,
        checks: landing time is after departure time, num of tickets not negative, 
                origin country is not destination country, 
                such flight not alredy exists- calls for get_stored_procedure from flights_repo 
                (Repository class) to acess 'check_if_flight_exists' stored procedure in the db,
        creates new flight by calling add func fron flights_repo (Repository Class),
        gets new flight ID by calling for 'check_if_flight_exists' stored procedure once again.
        Input:  org_countryID (int), dest_countryID (int),
                depart_time (str)- YYYY-MM-DD HH:MM,
                land_time (str) - YYYY-MM-DD HH:MM, 
                tickets (int)
                [all input by parameter name]
        Output: New flight ID;
                flight_repo.add func output - str err , if adding not sucsessful;
                False if facade dosen't match token role/landing time is after departure time/
                negative num of tickets/destcountryId = origincountryID/such flight alredy exists;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='AirlineCompany':
                # check landing time is after departure time
                if land_time > depart_time:
                    # check num of tickets not negative
                    if tickets >= 0:
                        # check origin country is not destination country
                        if org_countryID != dest_countryID:
                            # check if such flight alredy exists
                            if self.flights_repo.get_stored_procedure(
                                                            'check_if_flight_exists',
                                                            {'origin_country_id':org_countryID,
                                                             'destination_country_id':dest_countryID,
                                                            'datetime':depart_time}):
                                return False # such flight alredy exists
                            
                            else:
                                add_flight = self.flights_repo.add(Flights( AirlineID=self.airlineID,
                                                                            OriginCountryID=org_countryID,
                                                                            DestinationCountryID=dest_countryID,
                                                                            DepartureTime=depart_time,
                                                                            LandingTime=land_time,
                                                                            RemainingTickets=tickets))
                                if add_flight == True:  # adding flight sucsess
                                    new_flight = self.flights_repo.get_stored_procedure(
                                                                'check_if_flight_exists',
                                                                {'origin_country_id':org_countryID,
                                                                'destination_country_id':dest_countryID,
                                                                'datetime':depart_time})
                                    new_flightID = new_flight[0][0] # getting new flight's ID
                                    return new_flightID
                        
                                else:
                                    return add_flight # returns str err
                            
                        else:   # destcountryId = origincountryID
                            return False
                        
                    else:   # negative num of tickets
                        return False
                    
                else:    # landing time is after departure time
                    return False   
                
            else:   # facade dosen't match token role
                return False
            
        except Exception as e:
            return str(e)
        
        
    def update_flight(self,flightID,new_data):
        """     
        24.01.24
        Mir Shukhman
        Update flight func, ensures facade matches token role,
        calls get_by_id func from flight_repo to get airline's id from db for the flight,
        ensures airline's id from db matches token airline id,
        calls update func from flights_repo (Repository class).
        Input:  flightID (int)
                new_data - as dict, example {'Country_ID': 33}
        Output: flights_repo.update func output (updated flight's data/none/str err);
                False if facade dosen't match token role/no flight in db by given flightId
                /airline's id from db dosen't token airline id;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='AirlineCompany':
                flight_info = self.flights_repo.get_by_id(flightID)
                # flight found by id
                if flight_info:
                    db_airlineID = flight_info.AirlineID # getting airline's id from db
                    # ensuring airlineID db matches token
                    if db_airlineID== self.airlineID:
                        updated_flight = self.flights_repo.update(flightID,new_data)
                        
                        return updated_flight # returns updated flight data/none/str err
                    
                    else:   # airline's id from db for the flight dosen't  match token airline id
                        return False
                    
                else:   # no flight in db by given flightId
                    return False
                
            else:   # facade dosen't match token role
                return False  
                            
        except Exception as e:
            return str(e)
    
    
    def remove_flight(self,flightID):
        """     
        24.01.24
        Mir Shukhman
        Remove flight func, ensures facade matches token role,
        calls get_by_id func from flight_repo to get airline's id from db for the flight,
        ensures airline's id from db matches token airline id,
        looks for purchased tickets by calling for get_stored_procedure from tickets_repo 
        (Repository class) to acess 'get_tickets_by_flightID' stored procedure in the db,
        if purchased tickets- removes them by calling remove func from tickets_repo,
        calls remove func from flights_repo (Repository class).
        Input:  flightID (int)
        Output: flights_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no flight in db by given flightId
                /airline's id from db dosen't token airline id;
                Err str if err
        *** Warning: also removes customer's purchased tickets!!!*** 
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='AirlineCompany':
                flight_info = self.flights_repo.get_by_id(flightID)
                # flight found by id
                if flight_info:
                    db_airlineID = flight_info.AirlineID # getting airline's id from db
                    # ensuring airlineID db matches token 
                    if db_airlineID== self.airlineID :
                        # look for purchased tickets
                        purchased_tickets = self.tickets_repo.get_stored_procedure('get_tickets_by_flightID',
                                                                                  {'flightID':flightID})
                        # if there are purchased tickets, remove them
                        if purchased_tickets:
                            for ticket in purchased_tickets:
                                ticketID = ticket.TicketID
                                self.tickets_repo.remove(ticketID)
                        
                        remove = self.flights_repo.remove(flightID)
                        
                        return remove # returns True/None/ str err
                    
                    else:   # airline's id from db for the flight dosen't  match token airline id
                        return False
                    
                else:   # no flight in db by given flightId
                    return False
                
            else:   # facade dosen't match token role
                return False  
                            
        except Exception as e:
            return str(e)


    def	get_my_flights(self):
        """
        24.01.24
        Mir Shukhman
        Get all airline's flights func, ensures facade matches token role,
        calls for get_stored_procedure from flights_repo (Repository class) to acess
        'get_flights_by_airline_ID' stored procedure in the db,
        Input: None
        Output: List of tupples with flight info;
                False if facade dosen't match token role;
                None if no flights found for airlineID;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='AirlineCompany':        
                # getting flights using stored procedure
                my_flights= self.flights_repo.get_stored_procedure('get_flights_by_airline_ID',
                                                                   {'airlineID':self.airlineID})
                if my_flights:  # flights found
                    return my_flights
                
                else:   # no flights found for airlineID
                    return None 
                
            else:   # facade dosen't match token role
                return False
            
        except Exception as e:
            return str(e)
