from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'




"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
