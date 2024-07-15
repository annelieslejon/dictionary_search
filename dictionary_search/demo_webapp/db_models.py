from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
import os
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig
from datetime import datetime
app = Flask(__name__, static_url_path='', static_folder='frontend')
CORS(app)


env = os.getenv('FLASK_ENV', 'development') 
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)



# Configure the SQLAlchemy part of the app instance
#app.config['SQLALCHEMY_DATABASE_URI'] =  app.config.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create an SQLAlchemy object named `db` and bind it to your app
db = SQLAlchemy(app)
# Define models
class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(), nullable=False)

class Gloss(db.Model):
    __tablename__ = 'glosses'
    id = db.Column(db.Integer, primary_key=True)
    #gloss_name = db.Column(db.String(), nullable=False)
    gloss_full = db.Column(db.String(), nullable=False)



class Video(db.Model):
    __tablename__ = 'keypoints'
    id = db.Column(db.Integer, primary_key=True)
    gloss_name= db.Column(db.Integer, db.ForeignKey('glosses.gloss_full'), nullable=False)
    gloss_id = db.Column(db.Integer, db.ForeignKey('glosses.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    signknowledge = db.Column(db.Integer)
    results = db.Column(db.Text)
    scores = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    frames = db.Column(db.Integer)
    filename = db.Column(db.Text)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    feedback_gloss_name = db.Column(db.Text)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    answers = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)




