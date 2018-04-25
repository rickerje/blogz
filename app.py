from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'Aq0ZrF8r/3fX R~XHH6jmN]L7X/,J?RU'

db = SQLAlchemy(app)

