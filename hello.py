from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON
app = Flask(__name__)
application = app
import rdflib
from flask import redirect, url_for, render_template, request, flash
from forms import SearchForm, LetterForm, TravelForm
app.secret_key = 'development key'


graph = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/LD/sparql")

@app.route('/',methods = ['GET','POST'])
def home():
	personform = SearchForm()
	letterform = LetterForm()
	travelform = SearchForm()#used for searching for travels of a specific person
	travel2form = TravelForm()
	if request.method == 'POST':
		form_name = request.form['form-name']
		if form_name == 'form2':
			if letterform.validate_on_submit():# and not personform.validate():
				# if letters is filled out and person isn't
				names = regexnames(letterform.name.data)
				if not names== None:
					if len(names) == 1: #then just go to that!
						st = names[0][0].split('/')[-1:][0]
						#print "!!!!", st
						return redirect(url_for('letterget',text=st))
						#for x in names: # changes url
						#x[0] = 'http://127.0.0.1:5000/letter/' + x[0].split('/')[-1:][0] 
				#return render_template('searchresults.html',names=names,searchtype='letter') 
				return redirect(url_for('temporary2',text=letterform.name.data,names=None))   
                        #return redirect(url_for('temporary',text=form.name.data,names=None))
			else:
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form, tab = 'letters', active = ["tab-pane fade in", "tab-pane fade in", "tab-pane fade in active", "tab-pane fade in"])
			

		elif form_name == 'form1':
			if personform.validate():# and not letterform.validate():
				#if person filled out
				return redirect(url_for('temporary',text=personform.name.data,names=None))
			else:
				#return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form)
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form, tab = 'people', active = ["tab-pane fade in", "tab-pane fade in", "tab-pane fade in", "tab-pane fade in active"])

		#for travel forms:
		elif form_name == 'form4':
			if travel2form.validate():
				text = travel2form.date.data
				if len(str(text)) == 4:
					return redirect(url_for('travelyear', text = text))
				else:
					return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form, tab = 'travels', active = ["tab-pane fade in", "tab-pane fade in active", "tab-pane fade in", "tab-pane fade in"])
			else:
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form, tab = 'travels', active = ["tab-pane fade in", "tab-pane fade in active", "tab-pane fade in", "tab-pane fade in"])

		elif form_name == 'form3':
			if travelform.validate():
				names = regexnames(letterform.name.data)
				if not names== None:
					if len(names) == 1: #then just go to that!
						st = names[0][0].split('/')[-1:][0]
						#print "!!!!", st
						return redirect(url_for('travelget',text=st))
				return redirect(url_for('temporary3',text=travelform.name.data,names=None)) 
			else:
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form, tab = 'travels', active = ["tab-pane fade in", "tab-pane fade in active", "tab-pane fade in", "tab-pane fade in"])


		else:
			#if not personform.validate() or not letterform.validate() or not travelform.validate() or not travel2form.validate():
				flash('All fields are required.')
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form, tab = 'home', active = ["tab-pane fade in active", "tab-pane fade in", "tab-pane fade in", "tab-pane fade in"])
	elif request.method == 'GET':
			return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form, tab = 'home', active = ["tab-pane fade in active", "tab-pane fade in", "tab-pane fade in", "tab-pane fade in"])

@app.route('/person/')
def person():
	return render_template('person.html')

@app.route('/person/<name>')
def hello(name=None, birth=None, death=None, par1=None, par2=None, p2url=None, p1url=None, sb=None,child=None, letwrote=None, letreceived=None, travels=None):
	id_name = "p:" + name  #adds prefix for query
	row = id2name(id_name) # gets name and birth-death
	name, birth, death = row 
	parrow = parents(id_name) #gets parents names and links
   	par1, p1url, par2, p2url = parrow
	sb = sib(id_name)
	letwrote = letterwritten(id_name)
	letreceived = letterreceived(id_name)
	child = children(id_name)
#	travels = travelsbyid(id_name)
	return render_template('hello.html',
				 name=name,
				 birth=birth,
				 death=death,
				 par1=par1,
				 p1url=p1url,
				 par2=par2,
				 p2url=p2url,
				 sb=sb,
				 child=child,
				 letwrote=letwrote,
				 letreceived=letreceived,
				 travels=travels )
	
@app.route('/travels/')
def travel():
	return render_template('travels.html')
	
@app.route('/letters/',methods = ['GET', 'POST'])
def letters():
	form = LetterForm()
        if request.method == 'POST':
                if form.validate() == False:
                        flash('All fields are required.')
                        return render_template('lettersearch.html', form = form)
                else:
			names = regexnames(form.name.data,searchtype="letters")
			if not names == None:
				if len(names) == 1: #then just go to that!
					st = names[0][0].split('/')[-1:][0]
					#print "!!!!", st
					return redirect(url_for('letterget',text=st))
        	return render_template('searchresults.html',names=names,searchtype='letter')
			#return redirect(url_for('temporary',text=form.name.data,names=None))
        elif request.method == 'GET':
                return render_template('lettersearch.html', form = form)


@app.route('/letters/person/<text>')
def letterget(text=None,wrote=None,received=None):
	id_name = "p:" + text  #adds prefix for query
	#temporarly showing both wrote and recieved only
	name = id2name(id_name)[0]
	wrote = 1
	received = 1
	if wrote == 1:
		letwrote = letterwritten(id_name)
        else:
		letwrote =None
	if received == 1:
		letreceived = letterreceived(id_name)
	else:
		letreceived =None
	#TO BE FINISHED....
	#NEEDS TO PUT THIS IN A TEMPLATE
	return render_template('letterresult.html',name=name,letwrote=letwrote,letreceived=letreceived)

@app.route('/travels/person/<text>')
def travelget(text=None):
	id_name = "p:" + text  #adds prefix for query
	#temporarly showing both wrote and recieved only
	name = id2name(id_name)[0]
	travels = travelsbyid(id_name)
	print travels
	return render_template('travelresult.html',name=name,travels=travels)

@app.route('/letters/<text>')
#Doesn't work yet-- created 11/11/16 to be a page for an individual letter
def singleletter(text = None, letter = None):
	id_letter = "letter:" + text
	#if not infoletter(id_letter) == None:
	letter = infoletter(id_letter)
	#return render_template('singleletter.html', letter=letter)
	return render_template('singleletter.html',text=text ,letter=letter)


@app.route('/travels/year/<text>')
#Does not work yet: created 11/11/16, want it to display all travels from one year
def travelyear(text = None):
	date = text
	travels = []#just a filler for now
	return render_template('travelyear.html', travels = travels, date = date)




#graph = SPARQLWrapper("http://quakerexplorer.haverford.edu:8080/fuseki-server/LD/sparql")


#graph = rdflib.Graph()
#graph.parse('CEpeople.ttl', format= 'turtle')
#graph.parse('CEchild.ttl', format= 'turtle')
#graph.parse('CEletters.ttl', format= 'turtle')
#graph.parse('CEtravls.ttl', format= 'turtle')

#@app.route('/#people',methods = ['GET','POST'])
#This doesn't work since it doesn't recognize the '#' and puts in a '%23' for some reason

	


def infoletter(text):
	query="""
	PREFIX p: <http://quakerexplorer.haverford.edu/person/> 
	PREFIX letter:<localhost:3030/ds/letter#>

	SELECT ?Title ?RefUrl ?Date ?Subj ?C_url ?Creator ?Recipient ?R_url ?Destination ?Origin
	WHERE {
     		REPLACEME letter:Title ?Title ;
     		letter:Reference_URL ?RefUrl ;             
     		letter:Date ?Date ;
     		letter:Subject ?Subj ;
    		letter:Creator_ID ?C_url ;
   		letter:Destination ?Destination ;
   		letter:Place_Of_Origin ?Origin ;
    		letter:Recipient_ID ?R_url .
    		?C_url p:labelname ?Creator .
     		?R_url p:labelname ?Recipient .
}

	"""
	query = query.replace("REPLACEME",text)
	graph.setQuery(query)  
	graph.setReturnFormat(JSON)
	result = graph.query().convert()#query)
        #print query
	for row in result["results"]["bindings"]:
        #        if row == None: then this is maybe not an item... maybe useful 
#?Title ?RefUrl ?Date ?Subj ?C_url ?Creator ?Recipient ?R_url ?Destination ?Origin
                Title= row["Title"]["value"]
		RefUrl= row["RefUrl"]["value"]
		Date = row["Date"]["value"]
		Subj = row["Subj"]["value"]
		C_url= row["C_url"]["value"] 
		Creator= row["Creator"]["value"] 
		Recipient= row["Recipient"]["value"]
		R_url= row["R_url"]["value"] 
		Destination= row["Destination"]["value"] 
		Origin = row["Origin"]["value"]
		row = [Title, RefUrl, Date, Subj, C_url, Creator, Recipient, R_url, Destination, Origin]
        	return row





def id2name(username):
    # show the user profile for that user
	querynames = """
	prefix p: <http://quakerexplorer.haverford.edu/person/> 
	SELECT ?name ?birth ?death
	WHERE {
  		REPLACEME p:labelname ?name ;
		p:birth ?birth ;
   		p:death ?death .
	}	
"""
	querynames = querynames.replace("REPLACEME",username)
	graph.setQuery(querynames)
	graph.setReturnFormat(JSON)
	resultnames = graph.query().convert()#querynames)
#	print querynames
	for row in resultnames["results"]["bindings"]:
		name=row["name"]["value"]
                birth =row["birth"]["value"]
                death =row["death"]["value"]
                row = [name, birth, death]
		#print name, birth, death
		return row



def parents(username): #should handle the issue of Nonetype result
	queryparents = """
	PREFIX p: <http://quakerexplorer.haverford.edu/person/>           
	SELECT ?par1 ?p1 ?par2 ?p2
	WHERE {
  		REPLACEME p:parent_1 ?p1 ;
   		p:parent_2 ?p2 .
   		?p1 p:labelname ?par1 .
   		?p2 p:labelname ?par2 .
	}
"""
	queryparents = queryparents.replace("REPLACEME",username)
	graph.setQuery(queryparents)
	graph.setReturnFormat(JSON)
	resultparents = graph.query().convert()#queryparents)
	 # this will assume that everyone has 2 or none parents
	print queryparents	
	#print "len(resultparents)", len(resultparents)
	#NOTE: conditional below might not do what we want anymore 
	if len(resultparents["results"]["bindings"]) == 0: #everything is blank
		return [None,None,None,None]
	for row in resultparents["results"]["bindings"]:
	#	if row != None: #this might be unnecessary 
			#?par1 ?p1 ?par2 ?p2
		par1 = row["par1"]["value"]
		p1 = row["p1"]["value"]
		par2 = row["par2"]["value"]
		p2 = row["p2"]["value"]
		row = [ par1, p1,par2,p2]
		return row
		


def spouse(username): # THIS IS THE MOST DIFFICULT ONE SO I WILL DO IT LAST :^) 
	queryspouse = """
	prefix p: <http://quakerexplorer.haverford.edu/person/> 

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
	graph.setQuery(queryparents)
	graph.setReturnFormat(JSON)
        resultparents = graph.query().convert()#queryparents)
         # this will assume that everyone has 2 or none parents

        #print "len(resultparents)", len(resultparents)
        if len(resultparents["results"]["bindings"]) == 0: #everything is blank
                return [None,None,None,None]
        for row in resultparents["results"]["bindings"]:
                if row != None: #this might be unnecessary 

                        return row





def sib(username): #this will create an array of [[sib_1,url1],[sib_2,url_2],...] and be traversed in the template with a for-loop 
	querysib = """
PREFIX p: <http://quakerexplorer.haverford.edu/person/> 
PREFIX fhkb: <http://www.example.com/genealogy.owl#> 

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
	print "testing"
	querysib = querysib.replace("REPLACEME",username)
	graph.setQuery(querysib)
	graph.setReturnFormat(JSON)
        resultsib = graph.query().convert()#querysib)
	print querysib
        if len(resultsib["results"]["bindings"]) == 0: #everything is blank
                return None
      #  return len(resultsib)
        ans = []
        for row in resultsib["results"]["bindings"]:
		name = row["c"]["value"] 
		url = row["that"]["value"]
        #        if row != None: #this might be unnecessary 
                ans.append([name,url])
        return ans	
	#for row in resultsib:
         #       if row != None: #this might be unnecessary 
	#		print "test", row
         #               return row




def children(username):
	querychild = """
prefix p: <http://quakerexplorer.haverford.edu/person/> 
prefix fhkb: <http://www.example.com/genealogy.owl#> 

 SELECT ?urlperson ?c 
WHERE { 
        REPLACEME  fhkb:hasChild ?urlperson .
        ?urlperson p:labelname ?c .
} 
"""

	querychild = querychild.replace("REPLACEME",username)
	graph.setQuery(querychild)
	graph.setReturnFormat(JSON)
        resultchild = graph.query().convert()#querychild)
        if len(resultchild["results"]["bindings"]) == 0: #everything is blank
                return None
#       	return resultsib #unkown len
	ans = []
#	for row in resultchild:
        #        if row != None: #this might be unnecessary 
#		ans.append(row)
#	return ans
	for item in resultchild["results"]["bindings"]:
        	name = item["c"]["value"]
        	url = item["urlperson"]["value"]
        	ans.append([url,name])
	return ans

def letterwritten(username):
	querywrote = """
prefix p: <http://quakerexplorer.haverford.edu/person/> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?url ?title ?rt ?recipient ?subj
WHERE {
?m letter:Creator_ID REPLACEME ;
      letter:Title ?title ;
      letter:Subject ?subj ;
      letter:Reference_URL ?url ;
      letter:Recipient_ID ?rt .
     ?rt p:labelname ?recipient .
}
"""
	querywrote = querywrote.replace("REPLACEME",username)
        graph.setQuery(querywrote)
	graph.setReturnFormat(JSON)
	resultwrote = graph.query().convert()#querywrote)

        if len(resultwrote["results"]["bindings"]) == 0: #everything is blank
                return None
#               return resultsib #unkown len
        ans = []
        for row in resultwrote["results"]["bindings"]:
		url = row["url"]["value"]
		title = row["title"]["value"]
		urlrecip = row["rt"]["value"]
		recipient = row["recipient"]["value"]
		subj = row["subj"]["value"]
        #        if row != None: #this might be unnecessary 
                ans.append([url, title, urlrecip, recipient, subj])
        return ans

def letterreceived(username):
	queryreceived = """
prefix p: <http://quakerexplorer.haverford.edu/person/> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?url ?title ?rt ?recipient ?subj
WHERE {
?m letter:Recipient_ID REPLACEME ;
      letter:Title ?title ;
      letter:Subject ?subj ;
      letter:Reference_URL ?url ;
      letter:Creator_ID ?rt .
     ?rt p:labelname ?recipient .
}
"""

        queryreceived = queryreceived.replace("REPLACEME",username)
	graph.setQuery(queryreceived)
        graph.setReturnFormat(JSON)
	resultreceived = graph.query().convert()#queryreceived)

        if len(resultreceived["results"]["bindings"]) == 0: #everything is blank
                return None
#               return resultsib #unkown len
        ans = []
        for row in resultreceived["results"]["bindings"]:
        #        if row != None: #this might be unnecessary 
		url = row["url"]["value"]
	 	title = row["title"]["value"]
		urlrecip = row["rt"]["value"]
		recipient= row["recipient"]["value"]
		subj = row["subj"]["value"]
                ans.append([url, title, urlrecip, recipient, subj])
        return ans



def travelsbyid(username):
	querytravel = """
prefix p: <http://quakerexplorer.haverford.edu/person/> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>

SELECT ?loc ?month ?year 
WHERE
{ ?m p:Name "REPLACEME" ;
	p:trip  ?thetrip .
?thetrip t:location ?loc ;
	d:date_m ?month ;
	d:date_y ?year .
}


"""
        querytravel = querytravel.replace("REPLACEME",username)
	graph.setQuery(querytravel)
        graph.setReturnFormat(JSON)
	resulttravel = graph.query().convert()#querytravel)
	print querytravel
        if len(resulttravel["results"]["bindings"]) == 0: #everything is blank
                return None
#               return resultsib #unkown len
        ans = []
        for row in resulttravel["results"]["bindings"]:
        #        if row != None: #this might be unnecessary 
		loc= row["loc"]["value"]
		month = row["month"]["value"]
		year = row["year"]["value"] 
                ans.append([loc,month,year])
        return ans


#@app.route('/search/')
#@app.route('/search/<text>')
#def temporary(text=None,names=None):
#	names = regexnames(text)
#	print "this", names[0]
	#names = text
#	if len(names) == 1: #then just go to that!
#		st = names[0][0].split('/')[-1:][0]
		#print "!!!!", st
#		return redirect(url_for('hello',name=st))
#	return render_template('searchtest.html',names=names)


#############################################################################							
#############################################################################							
#############################################################################							
#############################################################################							

@app.route('/search', methods = ['GET', 'POST'])
#@app.route('/contact/<text>')
def search():
	form = SearchForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('search.html', form = form)
		else:
#			return render_template('success.html')
		
#			return temporary(form.name.data,None)
			#this should also change the url...
			return redirect(url_for('temporary',text=form.name.data,names=None))
	elif request.method == 'GET':
		return render_template('search.html', form = form)



@app.route('/person/search/<text>')
def temporary(text=None,names=None):
	names = regexnames(text,searchtype="person")
	if not names == None:
		if len(names) == 1: #then just go to that!
			st = names[0][0].split('/')[-1:][0]
                #print "!!!!", st
			return redirect(url_for('hello',name=st))
	return render_template('searchresults.html',names=names, searchtype = 'person')
        
@app.route('/letters/person/search/<text>')
def temporary2(text=None,names=None):
	names = regexnames(text)
	if not names == None:
		if len(names) == 1: #then just go to that!
			st = names[0][0].split('/')[-1:][0]
			#print "!!!!", st
			return redirect(url_for('letterget',text=st))	
	return render_template('searchresults.html',names=names, searchtype='letter')
        
@app.route('/travels/person/search/<text>')
def temporary3(text=None,names=None):
	names = regexnames(text)
	if not names == None:
		if len(names) == 1: #then just go to that!
			st = names[0][0].split('/')[-1:][0]
			return redirect(url_for('travelget',name=st))
	return render_template('searchresults.html',names=names, searchtype='travel')


def regexnames(text=None,searchtype=None):
	#searchtype ="testing"
	if searchtype == "letters":
		querynames="""
	PREFIX p: <http://quakerexplorer.haverford.edu/person/>
	PREFIX fhkb: <http://www.example.com/genealogy.owl#>

	SELECT ?url2 ?name ?birth ?death
	WHERE {
  	?id p:labelname ?name .
  	FILTER (REGEX(?name, "REPLACEME", "i")) .
  	?url p:labelname ?name ;
  	BIND( REPLACE(STR(?url), "person", "letter/person") AS ?url2) .
  	?url  p:birth ?birth ;
   	p:death ?death .

	}	
	"""
		querynames = querynames.replace("REPLACEME",text)
        	print querynames
		graph.setQuery(querynames)
		graph.setReturnFormat(JSON)
		resultnames = graph.query().convert()#querynames)
		print resultnames
        	if len(resultnames["results"]["bindings"]) == 0: #everything is blank
                	return None
        	ans = []
        	for row in resultnames["results"]["bindings"]:
        #        if row != None: #this might be unnecessary
			url2= row["url2"]["value"]
			name = row["name"]["value"]
		 	birth = row["birth"]["value"]
			death = row["death"]["value"]
               		ans.append([url2, name, birth, death])
        	return ans



        else: # searchtype == "person":
                querynames= """
PREFIX p: <http://quakerexplorer.haverford.edu/person/>
PREFIX fhkb: <http://www.example.com/genealogy.owl#>

SELECT ?url ?name ?birth ?death
WHERE {
  ?id p:labelname ?name .
  FILTER (REGEX(?name, "REPLACEME", "i")) .
  ?url p:labelname ?name ;
        p:birth ?birth ;
        p:death ?death .
}
"""

        	querynames = querynames.replace("REPLACEME",text)
        	graph.setQuery(querynames)
		graph.setReturnFormat(JSON)
		resultnames = graph.query().convert()#querynames)
        	if len(resultnames["results"]["bindings"]) == 0: #everything is blank
                	return None
        	ans = []
        	for row in resultnames["results"]["bindings"]:
        #        if row != None: #this might be unnecessary
                	url = row["url"]["value"]
			name = row["name"]["value"]
			birth = row["birth"]["value"]
			death = row["death"]["value"]
			ans.append([url, name, birth, death])
        	return ans


if __name__ == "__main__":
    app.run(host='0.0.0.0')





"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
