from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
import os
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='frontend')
CORS(app)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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
    gloss_name = db.Column(db.String(), nullable=False)
    gloss_full = db.Column(db.String(), nullable=False)



class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    gloss_id = db.Column(db.Integer, db.ForeignKey('glosses.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    frames = db.Column(db.Integer, nullable=False)
    keypoints = db.Column(db.Text)
    scores = db.Column(db.Text)

class Feedback(db.Model):
    __tablename__ = "Feedback"
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)



