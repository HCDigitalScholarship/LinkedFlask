from flask import Flask
app = Flask(__name__)
import rdflib
from flask import render_template

@app.route('/person/')
@app.route('/person/<name>')
def hello(name=None, birth=None, death=None, par1=None, par2=None):
	id_name = "p:" + name
	row = id2name(id_name)    
	#name, birth, death, par1, par2 = id2name(name)    
	name, birth, death = row
	print name, birth, death
	return render_template('hello.html', name=name, birth=birth, death=death )


graph = rdflib.Graph()
graph.parse('CEpeople.ttl', format= 'turtle')

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
	print querynames
	for row in resultnames:
		print "row", row
		name, birth, death=  row
		print name, birth, death
		return row



#def parents(username): should handle the issue of Nonetype result


queryspouse = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

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


querysib = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>
prefix fhkb: <http://www.example.com/genealogy.owl#> 

SELECT ?urlperson ?c
WHERE
{ 
REPLACEME p:labelname ?name ;
     p:parent_1 ?p1 ;
     p:parent_2 ?p2 . 
     ?p1 fhkb:hasChild ?that .
     ?that p:Name ?c .
     FILTER ( ?c != "REPLACEME" )
     ?p2 fhkb:hasChild ?this .
     ?this p:labelname ?c .
     FILTER ( ?c != "REPLACEME" )
BIND(REPLACE(?c, " ", "+", "i") AS ?urlperson)
}
"""




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














"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
