# flask and extensions imports
from flask import Flask, url_for, request
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.restless import APIManager

# user defined module imports
from app.shared.connection import db
from app.shared.models import User, Category, Post

# blueprint imports
from app.frontend.views import frontend
from app.auth.views import auth
from app.admin.views import UserAdminView, PostAdminView, CategoryAdminView, MyAdminIndexView


# create app object
app = Flask(__name__)
app.config.from_object('app.shared.configuration.DevelopmentConfig')

# setup db
db.init_app(app)

# create database tables within app context
with app.app_context():
	db.create_all()

# setup migration
migrate = Migrate(app, db)

# setup manage script
script = Manager(app)
script.add_command('db', MigrateCommand)

# setup login
login = LoginManager()
login.init_app(app)
login.login_view = 'auth.login'

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

# setup admin panel
admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminIndexView())

admin.add_view(UserAdminView(User, db.session))
admin.add_view(CategoryAdminView(Category, db.session))
admin.add_view(PostAdminView(Post, db.session))

# setup debug toolbar
toolbar = DebugToolbarExtension(app)

# setup api
api = APIManager(app, flask_sqlalchemy_db=db)

# create api blueprint within app context
with app.app_context():
	api.create_api(Category, methods=['GET', 'POST', 'DELETE'])
	api.create_api(Post, methods=['GET', 'POST', 'DELETE'])

# register all blueprints
app.register_blueprint(frontend)
app.register_blueprint(auth)

@app.before_request
def option_autoreply():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        
        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
            
        h = resp.headers
        
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Methods']
        h['Access-Control-Max-Age'] = "10"
        
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers
            
        return resp
        

@app.after_request
def set_allow_origin(resp):
    h = resp.headers
    
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        
    return resp