from . import db

# 09.01.24
# Mir Shukhman
#Definig&Creating AirlineCompanies table in db
class AirlineCompanies(db.Model):
    __tablename__ = 'AirlineCompanies'
    
    AirlineID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False, unique=True)
    Country_ID = db.Column(db.Integer, db.ForeignKey('Countries.CountryID'), nullable=False)
    UserID = db.Column(db.BigInteger, db.ForeignKey('Users.UserID'), nullable=False, unique=True)
    CompanyLogo= db.Column(db.String(300))

    