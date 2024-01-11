from . import db

# 09.01.24
# Mir Shukhman
# Definig&Creating Administrators table in db
class Administrators(db.Model):
    __tablename__ = 'Administrators'
    
    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False) 
    UserID =  db.Column(db.BigInteger, db.ForeignKey('Users.UserID'), nullable=False, unique=True)

    