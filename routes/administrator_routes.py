
from flask import Flask, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from routes.anonymous_routes import AnonymousBlueprint

from business_logic.facade_base import FacadeBase
from business_logic.administrator_facade import AdministratorFacade


facade_base=FacadeBase()

class AdministratorBlueprint(AnonymousBlueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self.route('/admin_dashboard', methods=['POST'])(self.admin_dashboard)
     

        
    def admin_dashboard(self):
        return render_template('admin_dashboard.html', name=self.name_of_admin)