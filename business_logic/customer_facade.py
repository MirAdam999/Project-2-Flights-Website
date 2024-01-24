
from business_logic.facade_base import FacadeBase

from modules.tickets import Tickets

# 23.01.24
# Mir Shukhman
# Defining class CustomerFacade wich inherits from FacadeBase,
#   recives the login token through the init from login func in AnonymousFacade,
#   and will hold update_customer, add_ticket, remove_ticket, get_my_tickets funcs.


class CustomerFacade(FacadeBase):
    def __init__(self, token):
        super().__init__()
        # Inherts FacadeBase init, login token from AnonymousFacade
        # Devides the login token into ID, name and role
        # Calls _get_customer_ID to get customerID using userId from the token
        self.token= token
        self.token_userID= self.token[0]
        self.token_cust_name= self.token[1]
        self.token_role= self.token[2]
        self.customerID = self._get_customer_ID()
        
    def _get_customer_ID(self):
        """
        24.01.24
        Mir Shukhman
        Func to retrive customer's ID using userID from the login token,
        Calls for get_stored_procedure from customers_repo (Repository class)
        to acess 'get_customer_by_userID' stored procedure in the db.
        Input: None
        Output: customerID (int); None if not found; Err str if err
        ***Internal use only! Does not check facade or name with token***
        """
        try:
            customer=self.customers_repo.get_stored_procedure('get_customer_by_userID',{'userID': self.token_userID})
            if customer:
                customerID = customer[0][0]
                return customerID
            
            else:
                return None
        
        except Exception as e:
            return str(e)
    
        
    def update_customer(self,new_data):
        """ 
        23.01.24
        Mir Shukhman
        Update customer func, ensures facade matches token role,
        calls get_by_id func from customers_repo to get cust's name from db,
        ensures cust's name from db matches token cust name,
        calls update func from customers_repo (Repository class).
        Input: new_data - as dict, example {'PhoneNum': '+15551234560','Address': '555 Main St'}
        Output: customers_repo.update func output (updated cust's data/none/str err);
                False if facade dosen't match token role/no cust in db by given custId
                /cust's full name from db dosen't token cust name;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Customer':
                db_customer= self.customers_repo.get_by_id(self.customerID)
                # customer with token_ID found
                if db_customer:
                    first_name = str(db_customer.FirstName)
                    last_name = str(db_customer.LastName)
                    full_name= f"{first_name} {last_name}"  # getting cust's full name from db
                    
                    # ensuring cust's full name from db matches token cust name
                    if full_name == self.token_cust_name:
                        updated_customer=self.customers_repo.update(self.customerID,new_data)
                        return updated_customer # returns updated cust's data/none/str err
                    
                    else:   # cust's full name from db dosen't token cust name
                        return False
                    
                else:   # no cust in db by given custId
                    return False
                
            else:   # facade dosen't match token role
                return False
            
        except Exception as e:
            return str(e)
    
    
    def add_ticket(self,flightID):
        """ 
        23.01.24
        Mir Shukhman
        Add (buy) ticket func, ensures facade matches token role,
        checks customer dosen't already own a ticket to the flight(calls for get_stored_procedure from
        tickets_repo (Repository class) to acess 'check_if_customer_owns_ticket_for_flight' stored
        procedure in the db),
        checks flight with flightID exists & that there are remaning tickets for the flight by
        calling get_by_id from flights_repo,
        creates new ticket by calling add func from tickets_repo,
        calls sp to update flights table remaning tickets -1 (calls for get_stored_procedure from
        flights_repo (Repository class) to acess 'buy_ticket' stored procedure in the db),
        gets new ticket ID by calling for 'check_if_customer_owns_ticket_for_flight' 
        stored procedure once again.
        Input: flightID (int)
        Output: New ticket ID;
                tickets_repo.add func output - str err , if adding not sucsessful;
                False if facade dosen't match token role/cust already owns ticket;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Customer':
                # cheking customer dosent already own a ticket to the flight
                if self.tickets_repo.get_stored_procedure('check_if_customer_owns_ticket_for_flight',
                                                          {'flightID':flightID,
                                                           'customerID':self.customerID}):
                    return False # cust already owns ticket
                
                else: # look for flight with flightID
                    flight_data= self.flights_repo.get_by_id(flightID)
                    remaning_tickets = flight_data.RemainingTickets
                    # check there are remaning tickets for the flight
                    if remaning_tickets > 0:
                        add_ticket = self.tickets_repo.add(Tickets(FlightID=flightID, CustomerID=self.customerID))
                        if add_ticket == True:  # adding ticket sucsess
                            # calling sp to update flights table remaning tickets -1
                            self.flights_repo.get_stored_procedure('buy_ticket',{'flightID':flightID})
                            new_ticket = self.tickets_repo.get_stored_procedure(
                                                                'check_if_customer_owns_ticket_for_flight',
                                                                {'flightID':flightID,
                                                                'customerID':self.customerID})
                            new_ticketID = new_ticket[0][0] # getting new ticket's ID
                            return new_ticketID
                        
                        else:
                            return add_ticket # returns str err
                        
                    else:   # no tickets left for flight/no flight with flightID
                        return False
                    
            else: # facade dosen't match token role
                return False
            
        except Exception as e:
            return str(e)

    
    def remove_ticket(self,ticketID):
        """ 
        23.01.24
        Mir Shukhman
        Remove ticket func, ensures facade matches token role,
        calls get_by_id func from tickets_repo to get cust ID & flightID thats in the ticket from db,
        ensures cust ID thats in the ticket from db matches token custID,
        calls sp to update flights table remaning tickets +1 (calls for get_stored_procedure from
        flights_repo (Repository class) to acess 'remove_ticket' stored procedure in the db)
        calls remove func from tickets_repo (Repository class).
        Input: ticketID (int)
        Output: tickets_repo.remove func output (True/None/str err);
                False if facade dosen't match token role/no ticket in db by given ticketID
                /cust ID thats in the ticket from db dosen't token custID;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Customer':
                #looking for ticket with given ID
                ticket = self.tickets_repo.get_by_id(ticketID)
                if ticket:
                    ticket_custID = int(ticket.CustomerID) # getting cust ID thats in the ticket from db
                    flightID = int(ticket.FlightID)
                    
                    # ensuring cust ID thats in the ticket from db matches token custID
                    if ticket_custID == self.customerID:
                        # calling sp to update flights table remaning tickets +1
                        self.flights_repo.get_stored_procedure('return_ticket',{'flightID':flightID})
                        remove = self.tickets_repo.remove(ticketID)
                        return remove # returns True/None/ str err
                    
                    else:   # cust ID thats in the ticket from db dosen't token custID
                        return False
                    
                else:   # no ticket in db by given ticketID
                    return False
                
            else:   # facade dosen't match token role
                return False
            
        except Exception as e:
            return str(e)
    
    
    def get_my_tickets(self):
        """
        23.01.24
        Mir Shukhman
        Get all customer's tickets func, ensures facade matches token role,
        calls for get_stored_procedure from tickets_repo (Repository class) to acess
        'get_tickets_by_customer' stored procedure in the db,
        for each ticket found retrives ticket id and flight id,
        gets the flight info by calling get_by_id func from tickets_repo,
        creates a list of dicts where each dict is a ticket: {ticket_id:flight_info}.
        Input: None
        Output: List of dicts where each ticket is a dict: {ticket_id:flight_info}
                ticket_id is int, flight_info is db.model object;
                False if facade dosen't match token role;
                None if no tickets found for customerID;
                Err str if err
        """
        try:
            # ensuring facade matches token role
            if self.token_role=='Customer':
                # getting tickets using stored procedure
                my_tickets = self.tickets_repo.get_stored_procedure('get_tickets_by_customer',
                                                                    {'customerID':self.customerID})
                if my_tickets:  # tickets found
                    my_tickets_info=[]
                    for ticket in my_tickets:
                        ticket_id = int(ticket[0])
                        flight_id = ticket[1]
                        # getting flight info for each ticket
                        flight_info= self.flights_repo.get_by_id(flight_id)
                        # creating a dict for each ticket and adding to list of tickets
                        my_tickets_info.append({ticket_id:flight_info})
                    
                    return my_tickets_info # returning the list of tickets
                    
                else:   # no tickets found for customerID
                    return None 
                
            else:   # facade dosen't match token role
                return False
            
        except Exception as e:
            return str(e)