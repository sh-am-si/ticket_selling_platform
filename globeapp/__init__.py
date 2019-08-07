from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_session import Session

import os
import stripe

STRIPE_PUBLISHABLE_KEY = 'pk_test_y6wTFqviF3yo5nv3MJ7rYhok005vztxrGl'
STRIPE_SECRET_KEY = 'sk_test_elZWAXFuw6wpRwUVaTDo8jbk00OQVMU7AG'

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.dirname(__file__))\
    +'/database/main.db'

stripe.api_key = STRIPE_SECRET_KEY

db = SQLAlchemy(app)

from globeapp import routes
from globeapp import models