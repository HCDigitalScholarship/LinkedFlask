from flask import Flask
app = Flask(__name__)
import rdflib
from flask import render_template

@app.route('/person/')
@app.route('/person/<name>')
def hello(name=None):

	name = id2name(name)    
	print name
	return render_template('hello.html', name=name)




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


def id2name(username):
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
		print 'result %s' % row
		return '%s' % row

#	return '??? %s' % username















"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
