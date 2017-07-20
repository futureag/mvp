#!/usr/bin/python

from logData import logData
# Import modules for CGI handling 
import cgi, cgitb
cgitb.enable(display=0, logdir="/home/pi/MVP/web/cgi-bin")

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Test Form Data Submission</title>")
print("</head>")
print("<body>")
print("<H1>MVP Data Submission</H1><hr />")
print("<H2>You have submitted the following data</H2>")

#Check for missing data
if "subject" not in form or "attribute" not in form or "status" not in form:
    print("<H1>Error</H1>")
    print("<p>Missing Field Data</p>")
else:
# Get data from fields
    subject = form.getvalue('subject')
    attribute  = form.getvalue('attribute')
    value = "NONE"
    c_value = ''
    if "value" in form:
        value  = form.getvalue('value')
        c_value = value

    attribute  = form.getvalue('status')
    status  = form.getvalue('status')

    c_comment = ''
    comment = "NONE"
    if "comment" in form:
        comment  = form.getvalue('comment')
        c_comment = comment

#Store in CouchDB
    logData(subject, status, attribute, c_value, c_comment) 
        
        
    print("<p>Subject: %s</p>" % (subject))
    print("<p>Attribute: %s</p>" % (attribute))
    print("<p>Value: %s</p>" % (value))    
    print("<p>Status: %s</p>" % (status))
    print("<p>Comment: %s</p>" % (comment)) 

    print("<br/><br/><p><a target='_blank' href='../MVP_Form.html'>Return to Input Form</a></p>")                 
    print("<br/><br/><p><a target='_blank' href='../index.html'>Return to Charts</a></p>")                 





          
print("</body>")
print("</html>")
