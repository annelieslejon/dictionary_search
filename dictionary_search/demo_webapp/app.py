import argparse
import json
import os
import uuid
from typing import List, Dict, Tuple
import logging
import numpy as np
from dictionary_search_model import Model
from flask import Flask, request, Response, redirect, url_for
from flask.json import jsonify
from werkzeug.utils import redirect
import search_engine
from db_models import *
from flask_restx import Api, Resource
#parser = argparse.ArgumentParser()
#parser.add_argument('model_path', type=str,
#                    help='The path to the model (that generates the embeddings) checkpoint.')
#parser.add_argument('data_store', type=str, help='Where to save recordings.')
#parser.add_argument('db_path', type=str, help='The path to the database directory.')
#parser.add_argument('-m', '--max_entries', type=int, help='Maximum database entries to consider.', default=100)
#args = parser.parse_args()
number_of_scores_tostore = 10
number_of_items_toreturn = 6
guid = None
import random
import datetime

def generate_db_entries(database_path, db_file):
    f = open(db_file)
    data = f.readlines()
    data = [os.path.join(database_path,d.strip())+'.npy' for d in data]
    app.logger.info('nof data' + str(len(data)))
    f.close()
    return data

if not app.debug:
    # Set up logging to a file if the application is not in debug mode
    handler = logging.FileHandler('/home/VGT/dictionary_search/demo_webapp/flask_app.log')  # Adjust the path as needed
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

# Accessing config
model_path = app.config['MODEL_PATH']
data_store = app.config['DATA_STORE']
db_path = app.config['DB_PATH']
db_file = app.config['DB_FILE']
max_entries = app.config['MAX_ENTRIES']
model: Model = Model(model_path)


query_set = generate_db_entries(db_path, db_file)
query_set_original = query_set.copy()
app.logger.info('nof signs' +str(len(query_set)))

database: search_engine.SearchEngine = search_engine.SearchEngine(db_path, max_entries, query_set=query_set_original )
query_set = [q.split('/')[-1].split('.npy')[0] for q in query_set]
app.logger.info('nof querys signs: ' + str(len(query_set)))
@app.route('/')
def index():
    return redirect(url_for('static', filename="slr/index.html"), code=302)
def create_session(guid = None):
    session  = Session(guid=guid) 
    db.session.add(session)
    db.session.commit()
    return session


def create_video_entry(gloss_name, session_id):
    app.logger.info('session_id' + str(session_id))
    app.logger.info(gloss_name)
    gloss_id = Gloss.query.filter_by(gloss_full=gloss_name).first().id
    created_at = datetime.datetime.now()
    new_video = Video(
        gloss_id = gloss_id,
        gloss_name=gloss_name,
        session_id=session_id,
        created_at = created_at
    )
    db.session.add(new_video)
    db.session.commit()
    app.logger.info('video entry created session' + str(session_id) +'guid' +  str(guid))


def create_feedback_entry(gloss_name, session_id):
    app.logger.info('session_id' + str(session_id))
    app.logger.info('gloss_name'+str(gloss_name))
    created_at = datetime.datetime.now()

    new_feedback = Feedback(feedback_gloss_name =gloss_name, session_id=session_id , created_at=created_at)
    db.session.add(new_feedback)
    db.session.commit()


@app.route('/get_start_video', methods=['GET'])
def get_start_video():
    session =create_session(guid = request.headers.get('sessionId') ) 
    app.logger.info('session_id' + str(session.guid) )
    app.logger.info('session_request_id' + str(request.headers.get('sessionId' ) ))

    count = len(query_set)
    app.logger.info('query set' + str(len(query_set)))
    random_offset = random.randint(0,len(query_set))
    app.logger.info('random_offset' + str(random_offset))
    random_gloss = query_set[random_offset]


    app.logger.info('start gloss' + str(random_gloss))
    create_video_entry(random_gloss, session.id)
    response: Dict[str, List[str]] = {

        "start_gloss": random_gloss,
        "sessionId" : session.guid
        # Only return 9 glosses to the UI, which can only display 5 anyway.
    }

    response: Response = jsonify(response)
    
    return response





def get_gloss_id(gloss_name):
    g = Gloss.query.filter_by(gloss_full=gloss_name).first()
    app.logger.info(gloss_name)
    app.logger.info(g)
    return  g

def get_gloss_session(session_id): 
   g = Video.query.filter_by(session_id=session_id).first().gloss_id
   app.logger.info(g)
   return g

def is_session_id_available(guid):
    return db.session.query(Session).filter_by(guid=str(guid)).first()

def update_feedback_entry(session_id, answers):
    app.logger.info('session_id: %s, update feedback answers: %s', session_id, answers)
    app.logger.info('type of answers: %s', type(answers))

    feedback = Feedback.query.filter_by(session_id=session_id).first()
    app.logger.info('feedback session id' + str(feedback.session_id))
    try:
        feedback.answers = answers
        db.session.commit()
        app.logger.info('Feedback updated successfully for session_id: %s', session_id)
    except Exception as e:  # Catch the exception properly
        db.session.rollback()  # Rollback the session in case of an error
        app.logger.error('Failed to update feedback entry: %s', e)

    feedback = Feedback.query.filter_by(session_id=session_id).first()
    app.logger.info('answers in feedback: %s', feedback.answers)


def update_feedback_entry_0(session_id, answers):
    app.logger.info('session_id' + str(session_id) + 'update feedback answers' + str(answers) )
    app.logger.info('type answers' + str( type(answers) ))
    feedback = Feedback.query.filter_by(session_id=session_id).first()
    if feedback is None:
        app.logger.error('No feedback found for session_id: %s', session_id)
    try:
        feedback.answers = answers
        db.session.commit()
        app.logger.info('Feedback updated successfully for session_id: %s', session_id)
    except: 
        app.logger.info('failed to update entry feedback: %s', e) 
    feedback = Feedback.query.filter_by(session_id=session_id).first()
    app.logger.info('answers feedback' + str(feedback.answers))




def update_video_entry(session_id,signknowledge,  number_frames, fn, search_glosses, scores):
    video = Video.query.filter_by(session_id = session_id).first()
    gloss_name = video.gloss_name
    video.frames = number_frames
    video.filename = str(session_id) + '_'+ gloss_name + '_'+ str(video.created_at) + '.npy'

    video.signknowledge= int(signknowledge)
    app.logger.info('scores' + str(scores))
    video.scores = ' '.join([str(round(s,2)) for s in scores])
    search_ids = [db.session.query(Gloss.id).filter(Gloss.gloss_full==g ).first()[0] for g in search_glosses]
    # Create a dictionary from the results


    video.results = ','.join([str(s) for s in search_ids])
    db.session.commit()
    return video


def get_feedback_id(ids):
    return 0


def get_random_feedback_ids(gloss_name, search_results, random= False):
    gloss_names_pred = [s[0] for s in search_results]
    wrong_glosses = [g for g in gloss_names_pred if g!= gloss_name]
    app.logger.info('wrong_glosses'+ str(wrong_glosses))
    if(random ==True):
        random_gloss = np.random.choice(wrong_glosses)
    else:
        random_gloss = wrong_glosses[0]
    app.logger.info('random gloss' + random_gloss)
    return random_gloss


def create_response(gloss_name, search_results, random=False):
    ids_selection  = []
    for j, s in enumerate(search_results):
        if( s[0] != gloss_name):
            ids_selection.append(j)
    if(random):
        random_id = np.random.choice(ids_selection)
    else:
        random_id = ids_selection[0]
    app.logger.info('random_id' +str(random_id))
    app.logger.info('selected feedback' + str(search_results[random_id]))
    response_results = [{"gloss":r[0], "score": r[2], "feedback_gloss": False} for r in search_results]
    response_results[random_id]['feedback_gloss'] = True


    return response_results, response_results[random_id]['gloss']




@app.route("/feedback/questions", methods =["post"] )
def feedback():
    app.logger.info('get feedback')
    data = request.get_json()
    try:

        sessionId = request.headers.get('sessionId')
        session_id = Session.query.filter_by(guid=sessionId).first().id
        app.logger.info('sessionId' + str(session_id)+ ',' + str(sessionId))
        app.logger.info('blabla')
        answers = data.get('answers')
        app.logger.info(str(answers))
        gloss = data.get('gloss')
        app.logger.info('feedback_method ' + str(gloss))
        app.logger.info(str(request.headers))
        app.logger.info(str(data))
        update_feedback_entry(session_id=session_id, answers=str(answers) )
        #feedback_name = request.headers.get('feedback_gloss', "HERFST-B-4897")
        #app.logger.info(feedback_name)
        #session_id = request.headers.get('sessionId')
        #app.logger.info(str(session_id))
        #answers = data.get('answers')
        #app.logger.info(str(answers))
        #feedback_id = get_gloss_id(feedback_name)
        #app.logger.info('feedback_id' + str(feedback_id)
        #session_id = request.headers.get('session_id','blabla')
        #app.logger.info('session_id' + str(session_id))
        #feedback_str = request.data
        #app.logger.info('feedback str ' + str(feedback_str))
        #feedback_entry = Feedback(video_id=feedback_id+1,session_id=session_id, feedback=feedback_str)
        #db.session.add(feedback_entry)
        #db.sesion.commit()
        return  jsonify({"status": "success", "message": "Feedback added to temporary storage"})
    except:
        return jsonify({"status": "error", "message": "Feedback adding failed"})



@app.route("/search_test", methods=['post'])
def search_test() -> Response:
    app.logger.info(str(request ))
    #app.logger.info(str(type(request.data['landMarks'])))
    data = request.get_json()
    keypoints = data['landmarks']
    keypoints = np.array(keypoints)
    signknowledge =  data['signKnowledge']
    app.logger.info('keypoints' + str(keypoints))
    app.logger.info('knowledge' + str(signknowledge))
    #if(request.data == []):
    #keypoints = np.zeros((38,543,3))

    #features = keypoints.reshape((-1, 543, 3))
    app.logger.info(features.shape)
    return jsonify({"status" : "success" , "message" : "search"}),200


@app.route("/search_final", methods=['post'])
def search_final() -> Response:
    # app.logger.info(str(request.keys())
    # app.logger.info(str(type(request.data['landMarks'])))
    # keypoints = np.fromstring(request.data, dtype=float, sep=',')
    # if(request.data == []):
    data = request.get_json()
    sessionId = request.headers.get('sessionId')
    kpts = np.array(data['landMarks'])
    app.logger.info('searching')
    features = kpts.reshape((-1, 543, 3))
    nr_frames = features.shape[0]
    app.logger.info('features shape' + str(features.shape))
    app.logger.info('global guid' + str(guid))
    session = Session.query.filter_by(guid=sessionId).first()
    if (session is None):
        app.logger.info('session is None')
        session = create_session(guid=request.headers.get('sessionId'))
    embedding: np.ndarray = model.get_embedding(features)

    search_results: List[Tuple[str, int, float, float]] = database.get_results(embedding, embedding)
    app.logger.info(search_results)
    scores = [t[2] for t in search_results]
    unique_filename = session.guid
    app.logger.info('fn' + str(unique_filename))

    app.logger.info('session_id' + str(session.guid))
    app.logger.info('knowledge' + str(data['signKnowledge']))
    int_knowledge = 0 if data['signKnowledge'] == 'no' else 1
    app.logger.info('nr frames' + str(nr_frames))
    search_glosses = [s[0] for s in search_results][:number_of_items_toreturn]
    video_entry = update_video_entry(session_id=session.id, signknowledge=int_knowledge, number_frames=nr_frames, \
                                     fn=unique_filename, search_glosses=search_glosses,
                                     scores=scores[:number_of_items_toreturn])
    app.logger.info('true gloss' + str(video_entry.gloss_name))

    np.save(os.path.join(data_store, 'kpts_' + str(video_entry.filename)), features)
    np.save(os.path.join(data_store, 'scores_' + str(video_entry.filename)), scores)
    app.logger.info('filename' + str(video_entry.filename))

    response, feedback_gloss_name = create_response(gloss_name = video_entry.gloss_name, search_results=search_results[:number_of_items_toreturn])

    create_feedback_entry(gloss_name=feedback_gloss_name,session_id=session.id)
    # Return search results.



    response: Response = jsonify(response)

    return response


@app.route("/search", methods=['post'])
def search() -> Response:
    #app.logger.info(str(request.keys())
    #app.logger.info(str(type(request.data['landMarks'])))
    #keypoints = np.fromstring(request.data, dtype=float, sep=',')
    #if(request.data == []):
    data = request.get_json()
    sessionId = request.headers.get('sessionId')
    kpts = np.array(data['landMarks'])
    app.logger.info('searching' ) 
    features = kpts.reshape((-1, 543, 3))
    nr_frames = features.shape[0]
    app.logger.info('features shape' + str(features.shape))
    app.logger.info('global guid' + str(guid))
    session = Session.query.filter_by(guid=sessionId).first()
    if(session is None) : 
        app.logger.info('session is None' ) 
        session = create_session( guid = request.headers.get('sessionId'))
    embedding: np.ndarray = model.get_embedding(features)
    
    search_results: List[Tuple[str, int, float, float]] = database.get_results(embedding,embedding)
    app.logger.info(search_results) 
    scores = [t[2] for t in search_results]
    unique_filename = session.guid
    app.logger.info('fn' + str(unique_filename))

    app.logger.info('session_id' + str(session.guid))
    app.logger.info('knowledge' + str(data['signKnowledge']))
    int_knowledge = 0 if data['signKnowledge'] == 'no' else 1
    app.logger.info('nr frames' + str(nr_frames))
    search_glosses = [s[0] for s in search_results][:number_of_items_toreturn]
    video_entry = update_video_entry(session_id=session.id, signknowledge=int_knowledge,number_frames=nr_frames,\
                    fn=unique_filename,   search_glosses=search_glosses, scores  = scores[:number_of_items_toreturn])
    app.logger.info('true gloss'+ str(video_entry.gloss_name))

    np.save(os.path.join(data_store, 'kpts_' + str(video_entry.filename)), features)
    np.save(os.path.join(data_store, 'scores_' + str(video_entry.filename)), scores)
    app.logger.info('filename' + str(video_entry.filename))

    feedback_id = get_feedback_id([result[1]] for result in search_results[:number_of_items_toreturn]) +1
    #feedback_gloss =  Gloss.query.filter_by(id=feedback_id).first().gloss_full
    random_feedback_gloss = get_random_feedback_ids(video_entry.gloss_name, search_results[:number_of_items_toreturn])
    app.logger.info('random feedback' + str(random_feedback_gloss))
    #create_feedback_entry(gloss_name=random_feedback_gloss,session_id=sessionId)
    # Return search results.
    response: Dict[str, List[str]] = {
        "results": [result[0] for result in search_results[:number_of_items_toreturn]],
        "scores": [result[2] for result in search_results[:number_of_items_toreturn]],
        "feedback_gloss": random_feedback_gloss,
        "sessionId" : session.guid
        # Only return 9 glosses to the UI, which can only display 5 anyway.
    }

    response: Response = jsonify(response)

    return response


if __name__ == '__main__':    
    app.run(debug=False)


