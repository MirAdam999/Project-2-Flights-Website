from sqlalchemy import CheckConstraint
from . import db

# 09.01.24
# Mir Shukhman
#Definig&Creating Flights table in db
class Flights(db.Model):
    __tablename__ = 'Flights'
    
    FlightID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    AirlineID = db.Column(db.BigInteger, db.ForeignKey('AirlineCompanies.AirlineID'), nullable=False)
    OriginCountryID = db.Column(db.Integer, db.ForeignKey('Countries.CountryID'), nullable=False)
    DestinationCountryID = db.Column(db.Integer, db.ForeignKey('Countries.CountryID'), nullable=False)
    DepartureTime = db.Column(db.DateTime)
    LandingTime = db.Column(db.DateTime)
    RemainingTickets = db.Column(db.Integer)
    FlightStatus = db.Column(db.String(20))
    
    __table_args__ = (CheckConstraint('RemainingTickets >= 0', name='check_remaining_tickets'),)