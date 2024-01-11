from flask_sqlalchemy import SQLAlchemy
import datetime

from modules import db

class Repository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, entity_id):
        try:
            if self.model.query.get(entity_id):
                return self.model.query.get(entity_id)
            else:
                return None
        
        except Exception as e:
            raise e

    def get_all(self):
        return self.model.query.all()

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()

    def update(self, entity):
        db.session.commit()

    def add_all(self, entities):
        try:
            db.session.add_all(entities)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e

    def remove(self, entity):
        db.session.delete(entity)
        db.session.commit()


