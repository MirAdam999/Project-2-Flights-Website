import csv
#Add countries from csv
"""
def get_countries_from_csv(file):
    with open (file, newline='') as csvfile:
        reader= csv.reader(csvfile, delimiter=',')
        line_counter=0
        list_of_countries_and_codes=[]
        for row in reader:
            if line_counter==0:
                line_counter+=1
            else:
                country=row[0]
                alpha_three=row[2]
                tup=(country.strip(),alpha_three.strip(' "" '))
                list_of_countries_and_codes.append(tup)
                
        return list_of_countries_and_codes
"""

# ---> app.py
"""
        list_of_tupples=get_countries_from_csv('countries_codes_and_coordinates.csv')
        countries_to_insert=[]
        for tup in list_of_tupples:
            country=tup[0]
            alpha_three=tup[1]
            to_insert= Countries(CountryName=country, Alpha3Code=alpha_three, CountryFlag=None)
            countries_to_insert.append(to_insert)
            
        countries_repo.add_all(countries_to_insert)
            
"""
# Function to generate random flights
"""  
import random
from datetime import timedelta, datetime
    def generate_random_flights(num_flights):
            flights = []
            for _ in range(num_flights):
                flight = Flights(
                    AirlineID=random.randint(1, 3),
                    OriginCountryID=random.randint(3, 245),
                    DestinationCountryID=random.randint(3, 245),
                    DepartureTime=datetime.now() + timedelta(days=random.randint(1, 30)),
                    LandingTime=datetime.now() + timedelta(days=random.randint(31, 60)),
                    RemainingTickets=random.randint(50, 200)
                )
                flights.append(flight)
                
            return flights
        
        random_flights = generate_random_flights(20)
        flights_repo.add_all(random_flights)
    
"""
# Function to generate random tickets
"""
import random
        def generate_random_tickets(num_tickets, max_customer_id, max_flight_id):
            tickets = []
            for _ in range(num_tickets):
                ticket = Tickets(
                    FlightID=random.randint(1, max_flight_id),
                    CustomerID=random.randint(1, max_customer_id),
                )
                tickets.append(ticket)
            return tickets

        # Generate 5 random tickets
        random_tickets = generate_random_tickets(5, 5, 20)
        tickets_repo.add_all(random_tickets)

"""


