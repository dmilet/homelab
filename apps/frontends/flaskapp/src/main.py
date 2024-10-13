from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def get_hello_world():
    return "<p>Hello, Brave New World!</p>"


@app.route("/", methods = ['POST'])
def post_hello_world():
    events = request.form
    print (f"{events}")
    return Response(events, status=201, mimetype='application/json')
