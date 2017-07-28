from __future__ import unicode_literals
from SPARQLWrapper import SPARQLWrapper, JSON
graph = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/LD3/sparql")
graph2 = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/LD3/update")
#graph.addDefaultGraph("http://quakerexplorer.haverford.edu:8080/fuseki-server/test3/data/test")
def changeid(id1=None, name=None):
		
        querychange = """
                prefix p: <http://quakerexplorer.haverford.edu/person/>
                prefix fhkb:  <http://www.example.com/genealogy.owl#> 
        	prefix d: <http://quakerexplorer.haverford.edu:8080/fuseki-server/LD3/data/>

	        DELETE{GRAPH d:test {REPLACE ?labelname ?name . }}
                INSERT{ GRAPH d:test {ME ?labelname ?name . }}
                WHERE{ GRAPH d:test {REPLACE ?labelname ?name . }}
        """
        querychange = querychange.replace("REPLACE", id1)
	querychange = querychange.replace("ME", name)
	#querychange = querychange.replace("HELLO", n)
	graph2.setQuery(querychange)
        graph2.method = 'POST'
        graph2.query()

def changeid2(id1=None, name=None):

        querychange = """
                prefix p: <http://quakerexplorer.haverford.edu/person/>
                prefix fhkb:  <http://www.example.com/genealogy.owl#> 
                prefix d: <http://quakerexplorer.haverford.edu:8080/fuseki-server/LD3/data/>
        	WITH d:test
		DELETE{ ?p ?labelname REPLACE . }
		INSERT{ ?p ?labelname ME . }
		WHERE{ ?p ?labelname REPLACE . }
	"""
        querychange = querychange.replace("REPLACE", id1)
        querychange = querychange.replace("ME", name)
        graph2.setQuery(querychange)
        graph2.method = 'POST'
        graph2.query()	
'''
def check():
	queryquery= """
	PREFIX p: <http://quakerexplorer.haverford.edu/person/>
	PREFIX fhkb: <http://www.example.com/genealogy.owl#>
	PREFIX o: <http://quakerexplorer.haverford.edu/organizations/>
	prefix d: <http://quakerexplorer.haverford.edu:8080/fuseki-server/LD3/data/>

	SELECT ?id
	WHERE {
		GRAPH ?g {?id p:labelname ?name}.
	}
	"""
	graph.setQuery(queryquery)
	graph.setReturnFormat(JSON)
	resultnames = graph.query().convert()
	if len(resultnames["results"]["bindings"]) == 0:
		return None
	lit = []
	for row in resultnames["results"]["bindings"]:
		#name = row["name"]["value"]
		id1 = row["id"]["value"]
		lit.append([id1])
	return lit
'''
querynames= """
PREFIX p: <http://quakerexplorer.haverford.edu/person/>
PREFIX fhkb: <http://www.example.com/genealogy.owl#>
PREFIX o: <http://quakerexplorer.haverford.edu/organizations/>
PREFIX : <.>

SELECT ?id ?name ?gr
WHERE {
{?id p:labelname ?name} UNION{ GRAPH ?gr {?id p:labelname ?name}}.
}
"""

#querynames = querynames.replace("REPLACEME",text)
graph.setQuery(querynames)
graph.setReturnFormat(JSON)
resultnames = graph.query().convert()#querynames)
if len(resultnames["results"]["bindings"]) == 0: #everything is blank
	print( None)
ans = []
an = []
for row in resultnames["results"]["bindings"]:
        #        if row != None: #this might be unnecessary
#	url = row["url"]["value"]
	name = row["name"]["value"]
	id1 = row["id"]["value"]
	if 'gr' in row:
		graph = row["gr"]["value"]
#	birth = row["birth"]["value"]
#	death = row["death"]["value"]
		ans.append([id1,id1,name,graph])
		an.append([id1,name,graph])
	else:
		ans.append([id1,name])
#print(ans)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

for a in range(len(ans)):
	if is_number(ans[a][0][-1]):
		my_count = sum(1 for sublist in ans[:a] if sublist[0].startswith(ans[a][0][:-1])) + 1
        	ans[a][0] = ans[a][0][:-1] + str(my_count)
	else:
		my_count = sum(1 for sublist in ans[:a] if sublist[0].startswith(ans[a][0])) + 1
        	ans[a][0] = ans[a][0] + str(my_count)
#	print(ans[a])

ls = []
for m in ans:
        for k in m:
                if k.startswith('http://quakerexplorer.haverford.edu:8080/fuseki-server/LD3/data/'):
			ls.append(m)
#			print(m)
#			print(m[0])
#			print(m[1])


#ls = []
for n in ls:
		#if q.startswith('http://quakerexplorer.haverford.edu:8080/fuseki-server/test5/data/'):
	if any(e[1] == n[0] for e in ls) == True:
		sub = n[0][:-1]
		bro = [s for s in ls if sub in s[0]]
	#	print(bro)
		for i in bro:
		#	if i[0].startswith('http://quakerexplorer.haverford.edu/person/jhain'):
		#		print(bro)
			#yo = [k for k in bro if k[0] == i[0] and k[1] != i[0]]
			yo = []
			yo2 = []
			out = []
			if any(k[0] == i[1] for k in bro) == True and any(k[1] == i[0] for k in bro) == False:
				yo.append(bro)
			#print(yo)
			for elm in yo:
				if elm not in yo2 and elm != []:
					yo2.append(elm)
			yo = yo2
			print(yo2)
			yo1 = filter(None, yo)
			yo = [x for x in yo if x != []]
			print(yo1)
			yo = sorted(yo)
			#print(yo)
			out = [yo[i] for i in range(len(yo)) if i == 0 or k[i] != k[i-1] ]	
		#	for o in reversed(out):
		#		print(o)
'''			if any(k[0] == i[1] for k in bro) == False and i[0] != i[1]:
			#	for i in reversed(bro):
					print(changeid("p:"+i[1].split('/')[-1],"p:"+i[0].split('/')[-1]))
                	                print(changeid2("p:"+i[1].split('/')[-1],"p:"+i[0].split('/')[-1] ))
		#for i in reversed(bro):
			#if any(k == i for k in bro) == True:
		#		print(changeid("p:"+i[1].split('/')[-1],"p:"+i[0].split('/')[-1]))
		#		print(changeid2("p:"+i[1].split('/')[-1],"p:"+i[0].split('/')[-1] ))
			#elif any(k[0] == i[0] for k in bro) == False:
         #                       print(changeid("p:"+i[1].split('/')[-1],"p:"+i[0].split('/')[-1]))
          #                      print(changeid2("p:"+i[1].split('/')[-1],"p:"+i[0].split('/')[-1] ))
	elif any(e[1] == n[0] for e in ls) == False:
				
			print(n)
			print(changeid("p:"+n[1].split('/')[-1],"p:"+n[0].split('/')[-1]))
			print(changeid2("p:"+n[1].split('/')[-1],"p:"+n[0].split('/')[-1] ))
			#else:			
			#print(n)
			#print("p:"+n[1].split('/')[-1])
			#print("p:"+n[0].split('/')[-1])
			#	print(changeid("p:"+n[1].split('/')[-1],"p:"+n[0].split('/')[-1] ))
#for r in range(len(an)):
# and for at in range(len(ans)):
#for r in list(results["results"]["bindings"] + range(len(ans))):
                #row1 = 
        #if summ <= len(ans)-1:
         #       print(ans[summ])
 	               
'''                
"""
ls = []
for a in ans:
#	for an in ans:		
	if sum(x.count(a[0]) for x in ans) > 1:
		#print(len(a[1]))
		ls.append(a)
	#	print(ls)

l = []
summ = 0
for q in ls:
	if any(e[0] == q[0] for e in an):
		l.append(q)
for y in l:
	print(y)
#m = []
#m = l + an
for t in range(len(an)):
	my_count = sum(1 for sublist in an[:t] if sublist[0].startswith(an[t][0][:-1])) + 1
	for i in range(len(l)):
		you_count = sum(1 for sub in l if sub[0].startswith(an[t][0][:-1])) + 1


"""
