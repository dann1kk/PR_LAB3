from flask import Flask, request, jsonify, url_for, abort, make_response
from threading import Thread
import requests
import threading
from contextlib import suppress
import requests

app = Flask(__name__)

# Memory data structure acting as data storage 
lessons = [
    {
        'id' : 1,
        'topic' : 'Cripthography and Security',
        'description' : 'Studying ciphers, starting from the classical ones and ending with hash functions and modern criptography.',
        'accredited' : 'true'
    },
    {
        'id' : 2,
        'topic' : 'Operating Systems: Internal Mechanisms and Design Principles',
        'description' : 'Stuff about internal mechanism of a computer and different principles.',
        'accredited' : 'true'
    },
    {
        'id' : 3,
        'topic' : 'Network Programming',
        'description' : 'Learning how to use computer code to write programs or processes that can communicate with other programs or processes across a network.',
        'accredited' : 'true'
    },
    {
        'id' : 4,
        'topic' : 'Design Techniques and Mechanisms',
        'description' : 'Studying patterns and different mechanisms of making code clearer and better.',
        'accredited' : 'true'
    },
    {
        'id' : 5,
        'topic' : 'Secure application development',
        'description' : 'Developing an application, following all the securization steps.',
        'accredited' : 'true'
    }
]

# A helper function that generates a public version of a lesson to send to the client
def make_public_lesson(lesson):
    new_lesson = {}
    for field in lesson:
        if field == 'id':
            new_lesson['uri'] = url_for('get_lesson', id = lesson['id'], _external = True)
        else:
            new_lesson[field] = lesson[field]
    return new_lesson   

# HTTP GET request to get all lessons
@app.route('/lessons', methods = ['GET'])
# @auth.login_required
def get_lessons():
    print(jsonify({'Lessons' : list(map(make_public_lesson, lessons))}))
    return jsonify({'Lessons' : list(map(make_public_lesson, lessons))})

# HTTP GET request to get a single lesson
@app.route('/lessons/<int:id>', methods = ['GET'])
# @auth.login_required
def get_lesson(id):
    lesson = list(filter(lambda l: l['id'] == id, lessons))
    if len(lesson) == 0:
        abort(404)
    print(jsonify({'Lesson' : make_public_lesson(lesson[0])}))
    return jsonify({'Lesson' : make_public_lesson(lesson[0])})
    

# HTTP POST request to create a new lesson
@app.route('/lessons', methods = ['POST'])
def create_lesson():
    if not request.json or not 'topic' in request.json:
        abort(400)
    lesson = {
        'id' : request.json['id'],
        'topic' : request.json['topic'],
        'description' : request.json.get('description',  ""),
        'accredited' : 'false'  
    }
    lessons.append(lesson)
    print(({'Lesson' : make_public_lesson(lesson)}))
    return jsonify({'Lesson' : make_public_lesson(lesson)}), 201

# HTTP PUT request to update a lesson
@app.route('/lessons/<int:id>', methods = ['PUT'])
def update_lesson(id):
    lesson = list(filter(lambda l: l['id'] == id, lessons))
    if len(lesson) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'topic' in request.json and type(request.json['topic']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'accredited' in request.json and type (request.json['accredited']) is not bool:
        abort(400)
    lesson[0]['topic'] = request.json.get('topic', lesson[0]['topic'])
    lesson[0]['description'] = request.json.get('description', lesson[0]['description'])
    lesson[0]['accredited'] = request.json.get('accredited', lesson[0]['accredited'])
    print(jsonify({'lesson' : make_public_lesson(lesson[0])}))
    return jsonify({'lesson' : make_public_lesson(lesson[0])})

# HTTP DELETE request to delete a lesson
@app.route('/lessons/<int:id>', methods = ['DELETE'])
def delete_lesson(id):
    lesson = list(filter(lambda l: l['id'] == id, lessons))
    if len(lesson) == 0:
        abort(404)
    lessons.remove(lesson[0])
    print(jsonify({'result' : True}))
    return jsonify({'result' : True})

# an error handler for a bad request 
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error' : 'Bad Request'}), 400)

# an error handler for a resource not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

def post_request():
    with suppress(Exception):
        # Create a new lesson with id: 11
        payload = dict({'id': 11, 'topic': "Special Mathematics", 'description': "Hard stuff"})
        requests.post('http://localhost:8080/lessons', json = payload, timeout = 0.0000000001)

def get_request():
    with suppress(Exception):
        # Get request for previously created lesson with id: 11
            requests.get('http://localhost:8080/lessons/11', timeout = 0.0000000001)
        
        # Get request for all lesssons
            requests.get('http://localhost:8080/lessons', timeout = 0.0000000001)

def put_request():
    with suppress(Exception):
        # Modify previously created lesson
        payload = dict({'topic': "Ethics", 'description': "Boring stuff", 'accredited': False})
        requests.put('http://localhost:8080/lessons/11', json = payload, timeout = 0.0000000001)

def delete_request():
    with suppress(Exception):
        # Delete created lesson with id: 11
        requests.delete('http://localhost:8080/lessons/11')


def main():
    main_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8080, debug = False, use_reloader = False), daemon= True)
    main_thread.start()
     
    Thread1 = threading.Timer(1.0, post_request)
    Thread1.start()   
    Thread2 = threading.Timer(3.0, get_request)
    Thread2.start()
    Thread3 = threading.Timer(6.0, put_request)
    Thread3.start()
    Thread4 = threading.Timer(9.0, delete_request)
    Thread4.start()

main()