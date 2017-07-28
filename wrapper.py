
from SPARQLWrapper import SPARQLWrapper, XML, JSON, CONSTRUCT

'''
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])
'''
graph1 = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/LD6/sparql")
graph2 = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/LD6/update")
'''
querynames = """
	prefix p: <http://quakerexplorer.haverford.edu/person/> 
        SELECT ?name ?birth ?death
        WHERE {
                p:i3 p:labelname ?name ;
                     p:birth ?birth ;
                     p:death ?death .
}
"""
#        queryparents = queryparents.replace("REPLACEME",username)
graph.setQuery(querynames)
graph.setReturnFormat(JSON)
resultnames = graph.query().convert()#queryparents)
         # this will assume that everyone has 2 or none parents
print querynames
        #print "len(resultparents)", len(resultparents)
        #NOTE: conditional below might not do what we want anymore 
#if len(resultnames["results"]["bindings"]) == 0: #everything is blank
#	print(None)
	#return [None,None,None,None]
for row in resultnames["results"]["bindings"]:
        name=row["name"]["value"]
        birth =row["birth"]["value"]
        death =row["death"]["value"]
        row = [name, birth, death]        
	print(len(row))
	print(row[0][0])
	print(row[0][1])
'''

'''
querysib = """
PREFIX p: <http://quakerexplorer.haverford.edu/person/> 
PREFIX fhkb: <http://www.example.com/genealogy.owl#> 

SELECT  ?c ?that 
WHERE
{ 
p:i3 p:labelname ?name ;
     p:parent_1 ?p1 ;
     p:parent_2 ?p2 . 
     ?p1 fhkb:hasChild ?that .
     ?that p:labelname ?c .
     ?p2 fhkb:hasChild ?this .
     ?this p:labelname ?c .
     FILTER (?name != ?c)
}
"""
        #print "testing"
#        querysib = querysib.replace("REPLACEME",username)
graph.setQuery(querysib)
graph.setReturnFormat(JSON)
resultsib = graph.query().convert()#querysib)
print(querysib)
if len(resultsib["results"]["bindings"]) == 0: #everything is blank
      print( None)
      #  return len(resultsib)
ans = []
for row in resultsib["results"]["bindings"]:
                name = row["c"]["value"]
                url = row["that"]["value"]
        #        if row != None: #this might be unnecessary 
                ans.append([name,url])
    	    	print(ans)
		print(len(ans))
        #for row in resultsib:
         #       if row != None: #this might be unnecessary 
        #               print "test", row
         #               return row
for sibling in range(len(ans)):
	print(ans[sibling][0] , ans[sibling][1])
'''

def changeid(id1=None, name=None):
		
	querychange = """
		prefix p: <http://quakerexplorer.haverford.edu/person/>
                prefix fhkb:  <http://www.example.com/genealogy.owl#> 
		DELETE{REPLACE ?labelname ?name .
                        ?p ?parent REPLACE . }
		INSERT{REPLACEME ?labelname ?name .
                        ?p ?parent REPLACEME . }
		WHERE{REPLACE ?labelname ?name .
                        ?p ?parent REPLACE . }
	"""
	querychange = querychange.replace("REPLACEME", name)
        querychange = querychange.replace("REPLACE", id1)
        graph2.setQuery(querychange)
        graph2.method = 'POST'
        graph2.query()
	
	'''
        querychange = """
                prefix p: <http://quakerexplorer.haverford.edu/person/>
                prefix fhkb:  <http://www.example.com/genealogy.owl#> 
                CONSTRUCT{REPLACEME ?labelname ?name .
                        ?p ?parent REPLACEME .
                 }
                WHERE{REPLACE ?labelname ?name .
                        ?p ?parent REPLACE .
                        
                }
                LIMIT 5

        """

	querychange = querychange.replace("REPLACEME", name)
        querychange = querychange.replace("REPLACE", id1)
        graph1.setQuery(querychange)
        graph1.setReturnFormat(XML)
        results = graph1.query().convert()
        print(querychange)
        for row in results:
		#["results"]["bindings"]:
                return row
	'''

query = """
        prefix p: <http://quakerexplorer.haverford.edu/person/> 
        SELECT ?p ?name ?birth
        WHERE {
                ?p p:labelname ?name .
		?p p:birth ?birth .

        }       

"""

graph1.setQuery(query)
graph1.setReturnFormat(JSON)
results = graph1.query().convert()
print(query)
ans = []
for row in results["results"]["bindings"]:
        p = row["p"]["value"]
	#print(p)
        name = row["name"]["value"]
        birth = row["birth"]["value"]
	ans.append([p, name, birth])
#print(ans)
for an in range(len(ans)):
	ans[an][1] = ans[an][1].lower()	
#        for a in range(len(ans)):
 #               if ("p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-1][0:3]) == ("p:" + ans[a][1].split(" ")[0][0] + ans[a][1].split(" ")[-1][0:3]) :
	if ans[an][1][0] == '[':
		if ans[an][1][2] == " ":
			ans[an][0] = "p:" + ans[an][1].split(" ")[1][0] + ans[an][1].split(" ")[-1][0:4]
		elif ans[an][1] == "['tyson'; ' eleanor cope'; ' '; ' ']":
                	ans[an][0] = "p:" + ans[an][1].split(" ")[0][2:6]
        	elif ans[an][1] == "['unknown']":
                	ans[an][0] = "p:" + ans[an][1][2:6]
		elif ans[an][1] == "['washington (d.c.)']":
			ans[an][0] = "p:" + ans[an][1][2:6]
		elif len(ans[an][1].split(" ")[-1][:-2]) < 4:
			ans[an][0] = "p:" + ans[an][1].split(" ")[0][2] + ans[an][1].split(" ")[-1][0:-2]
		else:
			ans[an][0] = "p:" + ans[an][1].split(" ")[0][2] + ans[an][1].split(" ")[-1][0:4]	
	elif ans[an][1] == "e.n. l'duvier":
		ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-1][2:5]
	elif ans[an][1].split(" ")[-1] == 'Jr.' or ans[an][1].split(" ")[-1] == 'jr.':
		ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-2][0:4]
	elif ans[an][1] == 'david colden  murrayd. 1885':
		ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-2][0:4]
	elif ans[an][1] == "j. miller (james miller) m'kim":
		ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-1][2:]
	elif len(ans[an][1].split(" ")[-1]) < 4:
		ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-1][0:]
	else:
		ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-1][0:4]  
#	print(ans[an])
	#ans[an][0].lower()

for a in range(len(ans)):
	my_count = sum(1 for sublist in ans[:a] if sublist[0].startswith(ans[a][0])) + 1
	ans[a][0] = ans[a][0] + str(my_count)
	#print(ans[a])
	#if any(ans[a][0] in sublist for sublist in ans):
         #      count = count + 1
	       #print(count)
#	ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[-1][0:3] + str(count)
	#print(ans[an][0])
#print(ans)
summ = 0
for r in results["results"]["bindings"]:
# and for at in range(len(ans)):
#for r in list(results["results"]["bindings"] + range(len(ans))):
		#row1 = 
	if summ <= len(ans)-1:
		print(ans[summ])
		print(changeid("p:"+r["p"]["value"].split('/')[-1], ans[summ][0]))
		summ = summ + 1
'''
        if len(ans[an][1].split(" ")) == 3:
                print(ans[an][1].split(" "))
                ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[2][0:3] + str(count)
                #change(ans[an][0])
        elif len(ans[an][1].split(" ")) == 2:
                ans[an][0] = "p:" + ans[an][1].split(" ")[0][0] + ans[an][1].split(" ")[1][0:3] + str(count)
                print(ans[an][0])

#print(ans)     

def changeid(id1=None, name=None):
        querychange = """
                prefix p: <http://quakerexplorer.haverford.edu/person/>
                prefix fhkb:  <http://www.example.com/genealogy.owl#> 
                CONSTRUCT{REPLACEME ?labelname ?name .
                        ?p ?parent REPLACEME .
                 }
                WHERE{REPLACE ?labelname ?name .
                        ?p ?parent REPLACE
                        
                }
                LIMIT 5

        """
        querychange = querychange.replace("REPLACEME", name)
        querychange = querychange.replace("REPLACE", id1)
        graph.setQuery(querychange)
        graph.setReturnFormat(JSON)
        results = graph.query().convert()
        print(querychange)
        for row in results["results"]["bindings"]:
                return row


'''
