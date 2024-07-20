# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# # Import configuration
# from config import Config

# # Initialize Flask app
# app = Flask(__name__)
# app.config.from_object(Config)

# # Initialize database
# db = SQLAlchemy(app)

# # Initialize login manager
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# # Import routes
# from routes import *

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pyotp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
