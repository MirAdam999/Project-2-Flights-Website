from . import db

# 09.01.24
# Mir Shukhman
#Definig&Creating Customers table in db
class Customers(db.Model):
    __tablename__ = 'Customers'
    
    CustomerID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False) 
    Address = db.Column(db.String(200)) 
    PhoneNum = db.Column(db.String(50), nullable=False, unique=True)
    CreditCardNum = db.Column(db.String(200), unique=True)
    UserID =  db.Column(db.BigInteger, db.ForeignKey('Users.UserID'), nullable=False, unique=True)


