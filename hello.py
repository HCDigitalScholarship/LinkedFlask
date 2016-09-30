from flask import Flask
app = Flask(__name__)
import rdflib
from flask import render_template

@app.route('/person/')
@app.route('/person/<name>')
def hello(name=None, birth=None, death=None, par1=None, par2=None, p2url=None, p1url=None, sib=None):
	id_name = "p:" + name  #adds prefix for query
	row = id2name(id_name) # gets name and birth-death
	name, birth, death = row 
	parrow = parents(id_name) #gets parents names and links
    	par1, p1url, par2, p2url = parrow
#	sib = sib(id_name)
#	print sib
	return render_template('hello.html',
				 name=name,
				 birth=birth,
				 death=death,
				 par1=par1,
				 p1url=p1url,
				 par2=par2,
				 p2url=p2url,
				 sib=sib )
	




graph = rdflib.Graph()
graph.parse('CEpeople.ttl', format= 'turtle')
graph.parse('CEchild.ttl', format= 'turtle')

@app.route('/')
def hello_world():
    return 'Hello, World!'


def id2name(username):
    # show the user profile for that user
	querynames = """
	prefix p: <http://127.0.0.1:5000/person/> 
	SELECT ?name ?birth ?death
	WHERE {
  		REPLACEME p:labelname ?name ;
		p:birth ?birth ;
   		p:death ?death .
	}	
"""

	querynames = querynames.replace("REPLACEME",username)
	resultnames = graph.query(querynames)
	print querynames
	for row in resultnames:
		#print "row", row
		name, birth, death=  row
		#print name, birth, death
		return row



def parents(username): #should handle the issue of Nonetype result
	queryparents = """
	PREFIX p: <http://127.0.0.1:5000/person/>           
	SELECT ?par1 ?p1 ?par2 ?p2
	WHERE {
  		REPLACEME p:parent_1 ?p1 ;
   		p:parent_2 ?p2 .
   		?p1 p:labelname ?par1 .
   		?p2 p:labelname ?par2 .
	}
"""
	queryparents = queryparents.replace("REPLACEME",username)
	resultparents = graph.query(queryparents)
	 # this will assume that everyone has 2 or none parents
	
	#print "len(resultparents)", len(resultparents)
	if len(resultparents) == 0: #everything is blank
		return [None,None,None,None]
	for row in resultparents:
		if row != None: #this might be unnecessary 
			return row
		


def spouse(username): # THIS IS THE MOST DIFFICULT ONE SO I WILL DO IT LAST :^) 


	queryspouse = """
	prefix p: <http://127.0.0.1:5000/person/> 

	SELECT ?partners
	WHERE
	{
	REPLACEME p:labelname ?name .
	?x p:parent_1 ?m;
   	p:parent_1 ?person_id;
   	?person_id p:labelame ?person ;
   	p:parent_2 ?partner_id;
  	?partner_id p:labelname ?partners . 
	?y p:parent_2 ?m;
    	p:parent_2 ?person_id;
    	?person_id p:labelname ?person ;
    	p:parent_1 ?partner_id;
    	?partner_id p:labelname ?partners . 
	}
	"""
	
	queryparents = queryparents.replace("REPLACEME",username)
        resultparents = graph.query(queryparents)
         # this will assume that everyone has 2 or none parents

        #print "len(resultparents)", len(resultparents)
        if len(resultparents) == 0: #everything is blank
                return [None,None,None,None]
        for row in resultparents:
                if row != None: #this might be unnecessary 
                        return row





def sib(username): #this will create an array of [[sib_1,url1],[sib_2,url_2],...] and be traversed in the template with a for-loop 

	querysib = """
PREFIX p: <http://127.0.0.1:5000/person/> 
PREFIX fhkb: <http://www.example.com/genealogy.owl/> 

SELECT  ?c ?that 
WHERE
{ 
REPLACEME p:labelname ?name ;
     p:parent_1 ?p1 ;
     p:parent_2 ?p2 . 
     ?p1 fhkb:hasChild ?that .
     ?that p:labelname ?c .
     ?p2 fhkb:hasChild ?this .
     ?this p:labelname ?c .
     FILTER (?name != ?c)
}
"""

	querysib = querysib.replace("REPLACEME",username)
        resultsib = graph.query(querysib)
        if len(resultsib) == 0: #everything is blank
                return None
        for row in resultsib:
                if row != None: #this might be unnecessary 
                        return row




def children(username):

	querychild = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>
prefix fhkb: <http://www.example.com/genealogy.owl#> 

SELECT ?urlperson ?c 
WHERE { 
	REPLACEME p:labelname ?name ;
	fhkb:hasChild ?this .
        ?this p:labelname ?c .
BIND(REPLACE(?c, " ", "+", "i") AS ?urlperson)
 } 
"""



	querysib = querysib.replace("REPLACEME",username)
        resultsib = graph.query(querysib)
        if len(resultsib) == 0: #everything is blank
                return None
        for row in resultsib:
                if row != None: #this might be unnecessary 
                        return row











"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
