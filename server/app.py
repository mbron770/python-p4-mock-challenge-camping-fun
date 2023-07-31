#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''


@app.route('/campers', methods = ['GET', 'POST'])
def campers():
    if(request.method == 'GET'):
        all = Camper.query.all()
        campers = []
        for camper in all: 
            campers.append(camper.to_dict(rules = ('-signups',)))
        return campers, 200
    else: 
        data = request.json 
        camper = Camper()
        try: 
            for attr in data: 
                setattr(camper, attr, data[attr])
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(rules = ('-signups',)), 201
        except ValueError as ie: 
            return {'error': ie.args}, 422
        

@app.route('/campers/<int:id>', methods = ['GET', 'PATCH'])
def camper_by_id(id):
    camper = Camper.query.filter(Camper.id).first()
    if not camper:
        return {'error' : 'Camper not found'}, 404
    if(request.method == 'GET'):
        return camper.to_dict(rules = ('-signups',)), 200
    else: 
        data = request.json 
        try: 
            for attr in data: 
                setattr(camper, attr, data[attr])
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(rules = ('-signups',)), 201
        except ValueError as ie:
            return {'error': ie.args}, 422
        
@app.route('/activities')
def activities():
    all = Activity.query.all()
    activities = []
    for activity in all: 
        activities.append(activity.to_dict(rules = ('-signups',)))
    return activities, 200

@app.route('/activities/<int:id>', methods = ['DELETE'])
def activity_by_id(id):
    activity = Activity.query.filter(Camper.id).first()
    if not activity:
        return {'error' : 'Activity not found'}, 404
    try: 
        db.session.delete(activity)
        db.session.commit()
        return {}, 201 
    except ValueError as ie: 
        return {'error': ie.args}, 422 
    
    
###ask about this 
    
@app.route('/signups', methods = ['POST'])
def signups():
    
        data = request.json 
        signup = Signup(
        )
        try: 
            for attr in data: 
                setattr(signup, attr, data[attr])
            db.session.add(signup)
            db.session.commit()
            return signup.to_dict(rules = ('-activity.signups', '-camper.signups')), 201
        except ValueError as ie: 
            return {'error': ie.args}, 422

# @app.post('/signups')
# def post_signups():
#      try:
#             signup = Signup(
#                 time=request.json["time"],
#                 camper_id=request.json["camper_id"],
#                 activity_id=request.json["activity_id"]
#             )

#             db.session.add(signup)
#             db.session.commit()

#             return make_response(signup.to_dict(), 201)

#      except ValueError:
#         return make_response({"errors": ["validation errors"]}, 400)
    
    
    

        
            
if __name__ == '__main__':
    app.run(port=5555, debug=True)
