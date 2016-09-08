from flask import Flask
app = Flask(__name__)
import rdflib


graph = rdflib.Graph()
graph.parse('CEpeople.ttl', format= 'turtle')


querynames = """
prefix p: <localhost:3030/ds/person#> 

SELECT ?name 
WHERE {
  REPLACEME p:labelname ?name .
}
"""









@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
	querynames = """
prefix p: <localhost:3030/ds/person#> 

SELECT ?name 
WHERE {
  REPLACEME p:labelname ?name .
}
"""   
	querynames = querynames.replace("REPLACEME",username)
	resultnames = graph.query(querynames)
#	print 'User %s' % username
	print querynames
	for row in resultnames:
		print 'huh %s' % resultnames
	return '??? %s' % resultnames
#	return '??? %s' % username





"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
