from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app = Flask(__name__)
app.secret_key = b'\xedM\xd0\x02\xe4\x90\xd7\xff\xbcK\xbb\x0f\xac\x11\x12\x8a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# 1. Initialize SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)

# 2. Bind the app to the db
db.init_app(app)

# 3. CRITICAL: Push the app context. 
# This solves the "App is not registered with this SQLAlchemy instance" error 
# by ensuring the app is active whenever the database is accessed.
app.app_context().push()

# 4. Initialize other extensions
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)