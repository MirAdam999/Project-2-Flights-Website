from . import db

# 09.01.24
# Mir Shukhman
#Definig&Creating UserRoles table in db
class UserRoles(db.Model):
    __tablename__ = 'UserRoles'
    
    RoleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoleName = db.Column(db.String(30), nullable=False, unique=True)