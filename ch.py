from SPARQLWrapper import SPARQLWrapper, JSON
graph = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/test5/sparql")
queryparents = """
        prefix p: <http://quakerexplorer.haverford.edu/person/>           
        prefix o: <http://quakerexplorer.haverford.edu/organizations/>
        SELECT ?par1 ?p1
        WHERE {
                p:mkirk3 p:parent_1 ?p1 .
                ?p1 p:labelname ?par1 .
        }
	"""
queryparents1 = """
        prefix p: <http://quakerexplorer.haverford.edu/person/>           
        prefix o: <http://quakerexplorer.haverford.edu/organizations/>
        SELECT ?par2 ?p2
        WHERE{
                p:mkirk3 p:parent_2 ?p2.
                ?p2 p:labelname ?par2
                
        }
        """
#queryparents = queryparents.replace("REPLACEME",username)
#queryparents1 = queryparents1.replace("REPLACEME", username)
graph.setQuery(queryparents)
graph.setQuery(queryparents1)
graph.setReturnFormat(JSON)
resultparents = graph.query().convert()#queryparents)
         # this will assume that everyone has 2 or none parents
print queryparents
        #print "len(resultparents)", len(resultparents)
        #NOTE: conditional below might not do what we want anymore 
if len(resultparents["results"]["bindings"]) == 0: #everything is blank
	print [None,None,None,None]
for row in resultparents["results"]["bindings"]:
        #       if row != None: #this might be unnecessary 
                        #?par1 ?p1 ?par2 ?p2
	par1 = row["par1"]["value"]
        p1 = row["p1"]["value"]
        par2 = row["par2"]["value"]
        p2 = row["p2"]["value"]
        row = [ par1, p1,par2,p2]
        print row
