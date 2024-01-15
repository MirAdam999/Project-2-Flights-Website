from flask_sqlalchemy import SQLAlchemy
import datetime

from modules import db
from logger import Logger

logger = Logger()

# 11.01.24
# Mir Shukhman
# Defining class Repository wich will hold all CRUD and several others funcs for db.Models
# Every use of one of Repo's funcs will be logged in 'log.json' in format:
#    id(Auto-generated), dattime(Auto-generated), class_name, func_name, func_input, func_output

class Repository:
    def __init__(self, model):
        self.model = model
        self.class_name = str(model)

    # CRUD funcs for all db.Models
    
    def get_by_id(self, entity_id):
        """
        11.01.24
        Mir Shukhman
        Getting entity by entity's ID
        Input entity ID output entity (tuuple); logging of action
        Exmp. input user ID output user
        """
        try:
            result = self.model.query.get(entity_id)
            if result:
                logger.log(self.class_name,'get_by_id', entity_id, result)
                return result
            else:
                logger.log(self.class_name,'get_by_id', entity_id, 'None found')
                return None
        
        except Exception as e:
            logger.log(self.class_name,'get_by_id', entity_id, str(e))
            raise e


    def get_all(self):
        """
        11.01.24
        Mir Shukhman
        Getting all entities of certain table in db(class db.model)
        Input class name output all class objects(list of tupples); logging of action
        Exmp. input users (table name) output all users
        """
        try:
            result = self.model.query.all()
            if result:
                logger.log(self.class_name,'get_all', 'None', str(result))
                return result
            else:
                logger.log(self.class_name,'get_all', 'None', 'None Found')
                return None
            
        except Exception as e:
            logger.log(self.class_name,'get_all', 'None', str(e))
            raise e


    def add(self, entity):
        """
        11.01.24
        Mir Shukhman
        Adding new entity to certain table in db (class db.model)
        Input emtity to add, output True if action sucsess; logging of action
        Exmp. input new user, output True
        """
        try:
            db.session.add(entity)
            db.session.commit()
            logger.log(self.class_name,'add', entity, 'Added')
            return True # Return sucsess of action
            
        except Exception as e:
            db.session.rollback()
            logger.log(self.class_name,'add', entity, str(e))
            return str(e)


    def update(self, entity_id, new_info):
        """
        11.01.24
        Mir Shukhman
        Updating an existing entity to certain table in db (class db.model)
        Input emtity ID and new info, output updated entity(tupple); logging of action
        Exmp. input user ID+updated user info, return updated user
        """
        try:
            entity = self.get_by_id(entity_id)
            
            if entity:
                for key, value in new_info.items():
                    setattr(entity, key, value)  
                db.session.commit()
                logger.log(self.class_name,'update', (entity_id, new_info), 'Updated')
                return entity  # Return the updated entity
                
            else:
                logger.log(self.class_name,'update', (entity_id, new_info), 'None Found')
                return None
        
        except Exception as e:
            db.session.rollback()
            logger.log(self.class_name,'update', (entity_id, new_info), str(e))
            raise e 
        

    def add_all(self, entities):
        """
        11.01.24
        Mir Shukhman
        Adding severall new entites to certain table in db (class db.model)
        Input emtities to add, output True if action sucsess; logging of action
        Exmp. input new users, output True
        """
        try:
            for entity in entities:
                db.session.add(entity)
                
            db.session.commit()
            logger.log(self.class_name,'add_all', entities, 'Added All')
            return True # Return sucsess of action
            
        except Exception as e:
            db.session.rollback()
            logger.log(self.class_name,'add_all', entities, str(e))
            raise e
        

    def remove(self, entity_id):
        """
        11.01.24
        Mir Shukhman
        Removing an existing entity to certain table in db (class db.model)
        Input emtity ID, output True if action sucsess; logging of action
        Exmp. input user ID, return True
        """
        try:
            entity = self.get_by_id(entity_id)
            
            if entity:
                db.session.delete(entity) 
                db.session.commit()
                logger.log(self.class_name,'remove', entity_id, 'Removed')
                return True  # Return sucsess of action
                
            else:
                logger.log(self.class_name,'remove', entity_id, 'None Found')
                return None
        
        except Exception as e:
            db.session.rollback()
            logger.log(self.class_name,'remove', entity_id, str(e))
            raise e 

    # Funcs calling for pre-created Stored Procedurs in SQL db
    
    def get_flights_by_parameters(self, _date, _origin_country_id=int, _destination_country_id=int):
        """
        11.01.24
        Mir Shukhman
        Calls for get_flights_by_parameters Stored Procedure in the db
        Getting flights by parameters: date, origin country id, destination country id
        Input (all private parameters) date, origin country id(int), destination country id(int)
        Output flights list
        ; logging of action
        """
        try:
            result = db.session.execute(
            "EXEC get_flights_by_parameters :origin_country_id, :destination_country_id, :date",
            {"origin_country_id": _origin_country_id, 
             "destination_country_id": _destination_country_id, 
             "date": _date}
            )
            flights = result.fetchall()
            
            if flights:
                logger.log('get_flights_by_parameters', (_date, _origin_country_id,
                                                     _destination_country_id), flights)
                return flights
            
            else:
                logger.log('get_flights_by_parameters', (_date, _origin_country_id,
                                                     _destination_country_id), 'None Found')
                return None
        
        except Exception as e:
            logger.log('get_flights_by_parameters', (_date, _origin_country_id,
                                                     _destination_country_id), str(e))
            raise e
    
    def get_flights_by_airline_ID(_airline_id):
        pass
    def get_arrival_flights_12hours(_country_id):
        pass
    def get_departure_flights_12hours(_country_id):
        pass
    def get_tickets_by_customer(_customer_id):
        pass
    def get_user_by_username(_username):
        pass
    def get_airline_by_username(_username):
        pass
    def get_customer_by_username(_username):
        pass

    # Other funcs for db.Models

    def getFlightsByOriginCountryId(self, country_id):
        pass
    
    
    def getFlightsByDestinationCountryId(self, country_id):
        pass
    
    
    def getFlightsByDepartureDate(self, date):
        pass 
    
    
    def getFlightsByLandingDate(self, date):
        pass
    
    
    def getFlightsByCustomer(self, customer):
        pass
    
    
    def getAirlinesByCountry(self, country_id):
        pass
