from . import db

# 09.01.24
# Mir Shukhman
#Definig&Creating Users table in db
class Users(db.Model):
    __tablename__ = 'Users'
    
    UserID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    Password = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False, unique=True)
    UserRole =  db.Column(db.Integer, db.ForeignKey('UserRoles.RoleID'), nullable=False)
    IsActive = db.Column(db.Boolean, default=True)
    