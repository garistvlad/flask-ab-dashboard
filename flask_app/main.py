from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

# Login
login = LoginManager(app)
login.login_view = 'auth.login'
# login.login_message = ""
login.login_message_category = "info"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Database Init:
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, App, ABExperiment, ABOption

# Blueprints structure example: https://realpython.com/flask-blueprint/
from ab import ab
from auth import auth
from admin import admin

# Register blueprints
app.register_blueprint(ab.bp)
app.register_blueprint(auth.bp, url_prefix="/auth")
app.register_blueprint(admin.bp, url_prefix="/admin")

# Register shell context:
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'App': App,
        'ABExperiment': ABExperiment,
        'ABOption': ABOption,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
