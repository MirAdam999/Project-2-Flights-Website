from . import db

# 09.01.24
# Mir Shukhman
#Definig&Creating Tickets table in db
class Tickets(db.Model):
    __tablename__ = 'Tickets'
    
    TicketID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    FlightID = db.Column(db.BigInteger, db.ForeignKey('Flights.FlightID'), nullable=False)
    CustomerID = db.Column(db.BigInteger, db.ForeignKey('Customers.CustomerID'), nullable=False)

    __table_args__ = (db.UniqueConstraint('FlightID', 'CustomerID'),)
