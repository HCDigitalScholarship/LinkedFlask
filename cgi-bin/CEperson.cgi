#!/usr/bin/env python
import rdflib
import cgi

form = cgi.FieldStorage()
name = form.getvalue('name')

top = """
<html lang="en"><head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags --> <meta name="description" content=""> <meta name="author" content=""> <link rel="icon" href="http://165.82.13.38/images/favicon.ico"> <title>Linked Data</title> <!-- Bootstrap core CSS --> <link href="http://165.82.13.38/css/bootstrap/css/bootstrap.min.css" rel="stylesheet"> <link href="http://165.82.13.38/css/style.css" rel="stylesheet"> <!-- IE10 viewport hack for Surface/desktop Windows 8 bug --> <link href="http://165.82.13.38/css/bootstrap/css/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"> <!-- Custom styles for this template --> <link href="http://165.82.13.38/css/bootstrap/css/sticky-footer.css" rel="stylesheet"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script> <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script> </head> <body> <!-- Begin page content --> <div class="container"> <div class="page-header"> <h1><a href='http://165.82.13.38/LinkedData.html'>Linked Data</a></h1> </div>
"""

bottom = """
</div> <footer class="footer"> <div class="container"> <p class="text-muted">Haverford College</p> </div> </footer> </body></html>
"""


paneltop = """
<div class="panel-group"> <div class="panel panel-default"> <div class="panel-heading"> <h4 class="panel-title"> <a data-toggle="collapse" href="#collapse1">
"""
#name of panel goes inbetween
panelmid = """
</a><span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span> </h4> </div> <div id="collapse1" class="panel-collapse collapse"> <ul class="list-group">
"""

panelbottom = """
</ul></div> </div> </div>
"""


# ASSUMES PERFECT SPELLING ( NO REGEXP )
graph = rdflib.Graph()
graph.parse('CEletters.ttl',format='turtle')
graph.parse('CEpeople.ttl', format= 'turtle')
graph.parse('CEchild.ttl', format= 'turtle')
graph.parse('CEtravls.ttl', format ='turtle')


querynames = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d: <localhost:3030/ds/date#>

SELECT ?url ?name 
WHERE {
  ?id p:labelname ?name .
  FILTER (REGEX(?name, "REPLACEME", "i"))
  BIND(REPLACE(?name, " ", "+", "i") AS ?url)

}
ORDER BY ?name
OFFSET 1
"""
#BIND(REPLACE(?o, "gotit", "haveit", "i") AS ?o2)

queryone = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d: <localhost:3030/ds/date#>

SELECT ?name 
WHERE {
  ?id p:labelname ?name .
  FILTER (REGEX(?name, "REPLACEME", "i"))

}
ORDER BY ?name
LIMIT 1
"""


queryString = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?birth ?death ?par1url ?par1 ?par2url ?par2
WHERE {
?x p:labelname "REPLACEME" ;
   p:birth ?birth ;
   p:death ?death ;
   p:parent_1 ?p1 ;
   p:parent_2 ?p2 .
   ?p1 p:labelname ?par1 .
   ?p2 p:labelname ?par2 .
BIND(REPLACE(?par1, " ", "+", "i") AS ?par1url)
BIND(REPLACE(?par2, " ", "+", "i") AS ?par2url)
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
	?m p:labelname "REPLACEME" ;
	fhkb:hasChild ?this .
        ?this p:labelname ?c .
BIND(REPLACE(?c, " ", "+", "i") AS ?urlperson)
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
?X p:labelname "REPLACEME" ;
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






queryspouse = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT ?partners
WHERE
{
?m p:labelname "REPLACEME" .
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


querywrote = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>


SELECT   ?url ?title ?urlrecip ?recipient ?subj
WHERE {
?x p:labelname "REPLACEME" .

?m letter:Creator_ID ?x ;
      letter:Title ?title ;
      letter:Reference_URL ?url ;
      letter:Subject ?subj ;
      letter:Recipient_ID ?rt .
     ?rt p:labelname ?recipient .
BIND(REPLACE(?recipient, " ", "+", "i") AS ?urlrecip)
}
"""

queryrecieved = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>


SELECT  ?url ?title ?urlperson ?person ?subj
WHERE {
?x p:labelname "REPLACEME" .

?m letter:Recipient_ID ?x ;
      letter:Title ?title ;
      letter:Reference_URL ?url ;
      letter:Subject ?subj ;
      letter:Creator_ID ?rt .
     ?rt p:labelname ?person .
BIND(REPLACE(?person, " ", "+", "i") AS ?urlperson)
}
"""



querytravel = """
        prefix p: <localhost:3030/ds/person#> 
        prefix t: <localhost:3030/ds/trip#> 
        prefix d:<localhost:3030/ds/date#>
        prefix letter:<localhost:3030/ds/letter#>

        SELECT ?loc ?month ?year 
        WHERE
        { ?m p:labelname "REPLACEME" ;
                p:trip  ?thetrip .
        ?thetrip t:location ?loc ;
                d:date_m ?month ;
                d:date_y ?year .
        }
        """


queryone = queryone.replace("REPLACEME",name)
oneresult = graph.query(queryone)      

for row in oneresult: #finds the closest match name and assigns it
        thename = row[0]

#below use the closest found name and preforms a series of searches
queryString = queryString.replace("REPLACEME",thename)
querychild = querychild.replace("REPLACEME",thename)
querysib = querysib.replace("REPLACEME",thename)
#queryspouse = queryspouse.replace("REPLACEME",name)
querywrote = querywrote.replace("REPLACEME",thename)
queryrecieved = queryrecieved.replace("REPLACEME",thename)
querytravel = querytravel.replace("REPLACEME",thename)
#print queryString

#stores the searches
result = graph.query(queryString)
resultchild = graph.query(querychild)
resultsib = graph.query(querysib)
resultwrote = graph.query(querywrote)
resultrecieved = graph.query(queryrecieved)
resulttravel = graph.query(querytravel)
#resultspouse = graph.query(queryspouse)

print top #header and top content of the site

#print "<p>" + queryString + " </p>"
#print "<p>" + querychild + " </p>"
#print "<p>" + querysib + " </p>"
#print "<p>" + queryspouse + " </p>"



querynames = querynames.replace("REPLACEME",name)
namesresult = graph.query(querynames) #finds the similar names to offer as other links in side bar


#print "<h1> TEST : "+ str(name) + " </h1>" 
x = len(namesresult)
print("<div class='sidebar' style='float:left;'><b><p>" + str(x) + " Similar results for " + str(name)+"</p></b>")
for row in namesresult:
        print("<a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> <p>  %s</p> </a> " % row)
print"</div>"
#print("<h1> test" + str(namesresult[0]) + "</h1>")



print("<div class='container info'>")

print ("<p class='lead'><b> Info: "+ str(thename) +"</b></p>")
for row in result:
    print("<p>  %s - %s </p><p><b>Parents:</b><a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s</a>, <a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s </a></p>  " % row)


print("<p><b>Siblings:</b> ")    
if len(resultsib) == 0:
	print("None </p>")
else:
	for row in resultsib:
    	#print("<p><b>Siblings:</b> %s</p> " % row)
    		print("<a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s </a> ," %row)
	print("</p>")

#for row in resultspouse:
#    print("<p>Spouse: %s</p> " % row)
print"<p><b>Spouse:</b> Not Coded yet </p>"


print("<p><b>Children:</b> ")
if len(resultchild) == 0:
        print("None </p>")
else:
	for row in resultchild:
    	#print("<p><b>Children:</b> %s</p> " % row) 
    		print("<a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s </a> ," %row)
	print("</p>")

#print(paneltop + "TEST" + panelmid + "<li class='list-group-item'>One</li> <li class='list-group-item'>Two</li> <li class='list-group-item'>Three</li>" + panelbottom)


print(paneltop + "Letters Written" + panelmid )
if len(resultwrote) == 0:
        print("<li class='list-group-item'><p>None </p> </li>")
else:
	for row in resultwrote:
		print("<li class='list-group-item'> <p style='margin:0 0 0px;'> <a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s  </a> to <a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s </a> </p><p style='font-size:smaller;margin:0 0 0px;'>Subject: %s </p> </li> " % row)
print panelbottom 


paneltop2 = paneltop.replace("collapse1","collapse2")
panelmid2 = panelmid.replace("collapse1","collapse2")
print(paneltop2 + "Letters Recieved" + panelmid2 )
if len(resultrecieved) == 0:
        print("<li class='list-group-item'><p>None </p> </li>")
else:
	for row in resultrecieved:
        	print("<li class='list-group-item'> <p style='margin:0 0 0px;'> <a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s  </a> by <a href=http://165.82.13.38/cgi-bin/CEperson.cgi?name=%s> %s </a> </p> <p style='font-size:smaller;margin:0 0 0px;'>Subject: %s </p></li> " % row)
print panelbottom


paneltop3 = paneltop.replace("collapse1","collapse3")
panelmid3 = panelmid.replace("collapse1","collapse3")
print(paneltop3 + "Travels" + panelmid3 )
if len(resulttravel) == 0:
        print("<li class='list-group-item'><p>None </p> </li>")
else:
	for row in resulttravel:
        	print("<li class='list-group-item'> <p> %s on %s, %s </p> </li> " % row)
print "</div>"
print panelbottom



print bottom
