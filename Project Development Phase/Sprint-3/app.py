from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape


import jinja2
import ibm_db
conn = ibm_db.connect("DATABASE= bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fmd31832;PWD=tISolCD4D6S358tX;","","")




app = Flask(__name__)


mysql = ibm_db(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def mainpage():

 
    name = request.form['name']
    password = request.form['password']
   
    sql = "SELECT * FROM use WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('adminpage.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO user VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, password)
     
      ibm_db.execute(prep_stmt)
    
   

