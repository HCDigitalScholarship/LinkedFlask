import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
graph = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/test1/sparql")
graph1 = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/test1/update")
#graph.parse('people-half.ttl', format= 'turtle')
def changeid(id1=None, name=None):
	
        querychange = """
                prefix p: <http://quakerexplorer.haverford.edu/person/>
                prefix fhkb:  <http://www.example.com/genealogy.owl#> 
		prefix o: <http://quakerexplorer.haverford.edu/organizations/>
                DELETE{REPLACE p:affiliations ?name . }
                INSERT{REPLACE p:affiliations REPLACEME . }
                WHERE{REPLACE p:affiliations ?name . }
        """
        querychange = querychange.replace("REPLACEME", name)
        querychange = querychange.replace("REPLACE", id1)
        graph1.setQuery(querychange)
        graph1.method = 'POST'
        graph1.query()
	
queryupdate="""
	PREFIX p: <http://quakerexplorer.haverford.edu/person/>
	SELECT  ?p ?org
	WHERE{
		?p p:affiliations ?org
	}


"""
graph.setQuery(queryupdate)
graph.setReturnFormat(JSON)
results = graph.query().convert()
print(queryupdate)
ans = []

for row in results["results"]["bindings"]:
        p = row["p"]["value"]
        #print(p)
        #name = row["name"]["value"]
        org = row["org"]["value"]
        ans.append([p,org])
#print(ans)
li = []
li = ans
#print(li)
for a in ans:
	#if a[1].find("_") != -1:
	#if a[0] == u'http://quakerexplorer.haverford.edu/person/rholl1':
	k = a[1].rfind("/")
	a[1] = a[1][k+1:]
	ans1 = a[1].split("_")
	if len(ans1) == 1:
		a[1] = "o:" + ans1[0]
	else:
		a[1] = "o:" + ans1[0] + " , "
		for an in range(1,len(ans1)):
			if ans1[an] == ans1[len(ans1)-1]:
				a[1] += "o:" + ans1[an]
			else:
				a[1] += "o:" + ans1[an] + " , "
	print(a)
summ = 0
for aa in range(len(li)):
	if summ <= len(ans) - 1:
		#print(li[aa][1].find("_"))
		#if li[aa][1].find("_") != -1:
#		print("done")
		print(ans[summ])
		print(changeid("p:"+ans[summ][0].split('/')[-1], ans[summ][1]))
                summ = summ + 1
		
	
"""
for row in ans:
	if row[0] == rdflib.term.URIRef(u'http://quakerexplorer.haverford.edu/person/tstew1'):
		k = row[1].rfind("/")
		row1 = row[1][k+1:]
		ans1 = row1.split("_")
		
		for a in range(len(ans)):
		    if ans[a] == ans[len(ans) - 1]:
		        row[1] += "o:" + ans[a]
		    else:
		        row[1] += "o:" + ans[a] + " , "
		print(row)
"""
