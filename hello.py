from flask import Flask
app = Flask(__name__)
import rdflib
from flask import redirect, url_for, render_template, request, flash
from forms import SearchForm, LetterForm
app.secret_key = 'development key'


@app.route('/',methods = ['GET','POST'])
def home():
	form = SearchForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('home.html', form = form)
		else:
			return redirect(url_for('temporary',text=form.name.data,names=None))
	elif request.method == 'GET':
		return render_template('home.html', form = form)

# the below function currently does nothing but hopefully the seach form will be on the home page and 
#therefore it will be important
def search():
        form = SearchForm()
        if request.method == 'POST':
                if form.validate() == False:
                        flash('All fields are required.')
                        return render_template('search.html', form = form)
                else:
#                       return temporary(form.name.data,None)
                        #Go to a results page 
                        return redirect(url_for('temporary',text=form.name.data,names=None))
        elif request.method == 'GET':
                return render_template('search.html', form = form)







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
	
#<<<<<<< HEAD
#=======
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
			names = regexnames(form.name.data)
			if len(names) == 1: #then just go to that!
                		st = names[0][0].split('/')[-1:][0]
                		#print "!!!!", st
                		return redirect(url_for('letterget',text=st))
#			for x in names: # changes url
#				x[0] = 'http://127.0.0.1:5000/letter/' + x[0].split('/')[-1:][0] 
        		return render_template('searchtest.html',names=names,searchtype='letter')			
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


#	return render_template('letterswritten.html')
	

#>>>>>>> 88e9e1afd934e2ca9900ffab78ab326a5fa9ad34
graph = rdflib.Graph()
graph.parse('CEpeople.ttl', format= 'turtle')
graph.parse('CEchild.ttl', format= 'turtle')
graph.parse('CEletters.ttl', format= 'turtle')
graph.parse('CEtravls.ttl', format= 'turtle')

#@app.route('/')
#def hello_world():
 #   return 'Hello, World!'


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


@app.route('/search/<text>')
def temporary(text=None,names=None):
        names = regexnames(text)
        print "this", names[0]
        #names = text
        if len(names) == 1: #then just go to that!
                st = names[0][0].split('/')[-1:][0]
                #print "!!!!", st
                return redirect(url_for('hello',name=st))
        return render_template('searchtest.html',names=names)


def regexnames(text):
        querynames= """
PREFIX p: <http://127.0.0.1:5000/person/> 
PREFIX fhkb: <http://www.example.com/genealogy.owl#> 

SELECT ?url ?name 
WHERE {
  ?id p:labelname ?name .
  FILTER (REGEX(?name, "REPLACEME", "i")) .
  ?url p:labelname ?name .

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
