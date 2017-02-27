from flask import Flask
app = Flask(__name__)
import rdflib
from flask import redirect, url_for, render_template, request, flash
from forms import SearchForm, LetterForm, TravelForm
app.secret_key = 'development key'


@app.route('/',methods = ['GET','POST'])
def home():
	personform = SearchForm()
	letterform = LetterForm()
	travelform = SearchForm()#used for searching for travels of a specific person
	travel2form = TravelForm()
	if request.method == 'POST':
		form_name = request.form['form-name']
		if form_name == 'form2':
			if letterform.validate():# and not personform.validate():
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
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form)

		elif form_name == 'form1':
			if personform.validate():# and not letterform.validate():
				#if person filled out
				return redirect(url_for('temporary',text=personform.name.data,names=None))
			else:
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form)

		#for travel forms:
		elif form_name == 'form4':
			if travel2form.validate():
				return redirect(url_for('travelyear', text = travel2form.date.data))
			else:
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form)

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
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form)


		else:
			#if not personform.validate() or not letterform.validate() or not travelform.validate() or not travel2form.validate():
				flash('All fields are required.')
				return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form)
	elif request.method == 'GET':
			return render_template('home.html', personform = personform, letterform = letterform, travelform = travelform, travel2form = travel2form)

@app.route('/person/')
def person():
	return render_template('person.html')

@app.route('/person/<name>')
def hello(name=None, birth=None, death=None, par1=None, par2=None, p2url=None, p1url=None, sb=None,child=None, letwrote=None, letreceived=None, travels=None):
	id_name = "p:" + name  #adds prefix for query
	row = id2name(id_name) # gets name and birth-death
	name, death, birth = row 
	parrow = parents(id_name) #gets parents names and links
    	par1, p1url, par2, p2url = parrow
	sb = sib(id_name)
	print "yahhooo"
#	print sb
	letwrote = letterwritten(id_name)
	letreceived = letterreceived(id_name)
	child = children(id_name)
	travels = travelsbyid(id_name)
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
	return render_template('travelresult.html',name=name)

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







graph = rdflib.Graph()
graph.parse('CEpeople.ttl', format= 'turtle')
graph.parse('CEchild.ttl', format= 'turtle')
graph.parse('CEletters.ttl', format= 'turtle')
graph.parse('CEtravls.ttl', format= 'turtle')

#@app.route('/')
#def hello_world():
 #   return 'Hello, World!'


def infoletter(text):
	query="""
	PREFIX p: <http://127.0.0.1:5000/person/> 
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
        result = graph.query(query)
        print query
	for row in result:
        #        if row == None: then this is maybe not an item... maybe useful 
                Title, RefUrl, Date, Subj, C_url, Creator, Recipient, R_url, Destination, Origin=  row
        	return row





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
	print queryparents	
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
        resultsib = graph.query(querysib)
	print querysib
        if len(resultsib) == 0: #everything is blank
                return None
      #  return len(resultsib)
        ans = []
        for row in resultsib:
        #        if row != None: #this might be unnecessary 
                ans.append(row)
        return ans	
	#for row in resultsib:
         #       if row != None: #this might be unnecessary 
	#		print "test", row
         #               return row




def children(username):
	querychild = """
prefix p: <http://127.0.0.1:5000/person/> 
prefix fhkb: <http://www.example.com/genealogy.owl#> 

 SELECT ?urlperson ?c 
WHERE { 
        REPLACEME  fhkb:hasChild ?urlperson .
        ?urlperson p:labelname ?c .
} 
"""

	querychild = querychild.replace("REPLACEME",username)
        resultchild = graph.query(querychild)
        if len(resultchild) == 0: #everything is blank
                return None
#       	return resultsib #unkown len
	ans = []
	for row in resultchild:
        #        if row != None: #this might be unnecessary 
		ans.append(row)
	return ans



def letterwritten(username):
	querywrote = """
prefix p: <http://127.0.0.1:5000/person/> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?url ?title ?urlrecip ?recipient ?subj
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
        resultwrote = graph.query(querywrote)

        if len(resultwrote) == 0: #everything is blank
                return None
#               return resultsib #unkown len
        ans = []
        for row in resultwrote:
        #        if row != None: #this might be unnecessary 
                ans.append(row)
        return ans

def letterreceived(username):
	queryreceived = """
prefix p: <http://127.0.0.1:5000/person/> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?url ?title ?urlrecip ?recipient ?subj
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
        resultreceived = graph.query(queryreceived)

        if len(resultreceived) == 0: #everything is blank
                return None
#               return resultsib #unkown len
        ans = []
        for row in resultreceived:
        #        if row != None: #this might be unnecessary 
                ans.append(row)
        return ans



def travelsbyid(username):
	querytravel = """
prefix p: <http://127.0.0.1:5000/person/> 
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
        resulttravel = graph.query(querytravel)

        if len(resulttravel) == 0: #everything is blank
                return None
#               return resultsib #unkown len
        ans = []
        for row in resulttravel:
        #        if row != None: #this might be unnecessary 
                ans.append(row)
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
        print "this", names[0]
	for z in names:
		print z
        #names = text
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
			return redirect(url_for('letterget',name=st))	
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
	PREFIX p: <http://127.0.0.1:5000/person/>
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
		resultnames = graph.query(querynames)
		print resultnames
        	if len(resultnames) == 0: #everything is blank
                	return None
        	ans = []
        	for row in resultnames:
        #        if row != None: #this might be unnecessary
               		ans.append(row)
        	return ans



        else: # searchtype == "person":
                querynames= """
PREFIX p: <http://127.0.0.1:5000/person/>
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
        	resultnames = graph.query(querynames)
        	if len(resultnames) == 0: #everything is blank
                	return None
        	ans = []
        	for row in resultnames:
        #        if row != None: #this might be unnecessary
                	ans.append(row)
        	return ans








"""
then call
$ export FLASK_APP=hello.py
$ python -m flask run

"""
