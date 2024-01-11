from . import db

# 09.01.24
# Mir Shukhman
#Definig&Creating Countries table in db
class Countries(db.Model):
    __tablename__ = 'Countries'
    
    CountryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CountryName = db.Column(db.String(50), nullable=False, unique=True)
    Alpha3Code = db.Column(db.String(3), nullable=False, unique=True)
    CountryFlag = db.Column(db.String(300))