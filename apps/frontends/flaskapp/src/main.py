from flask import Flask
from flask import Response
from flask import request
import json

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def get_hello_world():
    return "<p>Hello, Brave New World!</p>"


@app.route("/", methods = ['POST'])
def post_hello_world():
    events = request.form
    f = open("events.log", "a")
    f.write(json.dumps(events))
    f.close()
    return Response(events, status=201, mimetype='application/json')
