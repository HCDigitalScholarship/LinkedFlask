from flask import Flask
app = Flask(__name__)

@app.route('/')
def ello_world():
    return 'Hello, World!'




"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run
source: http://flask.pocoo.org/docs/0.11/quickstart/
"""
