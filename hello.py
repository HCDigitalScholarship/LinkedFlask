from flask import Flask
app = Flask(__name__)
import rdflib
from flask import render_template

@app.route('/person/')
@app.route('/person/<name>')
def hello(name=None, birth=None, death=None, par1=None, par2=None):

	#name, birth, death, par1url, par1, par2url, par2  = id2name(name)    
	row = id2name(name)    
	#name, birth, death, par1, par2 = id2name(name)    
	#print "name", name
	name, birth, death = row
	print name, birth, death
	return render_template('hello.html', name=name, birth=birth, death=death )




graph = rdflib.Graph()
graph.parse('CEpeople.ttl', format= 'turtle')

#querynames = """
#prefix p: <localhost:3030/ds/person#> 
#SELECT ?name 
#WHERE {
#  REPLACEME p:labelname ?name .
#}
#"""


@app.route('/')
def hello_world():
    return 'Hello, World!'


def id2name(username):
    # show the user profile for that user
	querynames = """
	prefix p: <localhost:3030/ds/person#> 
	SELECT ?name ?birth ?death
	WHERE {
  		REPLACEME p:labelname ?name ;
		p:birth ?birth ;
   		p:death ?death .
	}	
"""

	querynames = querynames.replace("REPLACEME",username)
	resultnames = graph.query(querynames)
#	print 'User %s' % username
	print querynames
	for row in resultnames:
		print "row", row
		name, birth, death=  row
		print name, birth, death
		return row
		#return name, birth, death, par1, par2

#	return '??? %s' % username















"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
