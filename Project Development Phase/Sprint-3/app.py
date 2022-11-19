import re
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

      @app.route('/')
      def hello():
      return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        pd = request.form['password']
        sql = "SELECT * FROM people WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    mg=''
    if request.method == "POST":
        username=request.form['name']
        email=request.form['email']
        pw=request.form['password'] 
        address=request.form['address']
        phone=request.form['phone']
        sql='SELECT * FROM people WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            mg='Account already exits!!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mg='Please enter the avalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            ms='name must contain only character and number'
        else:
            insert_sql='INSERT INTO people VALUES (?,?,?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,username)
            ibm_db.bind_param(pstmt,2,address)
            ibm_db.bind_param(pstmt,3,phone)
            ibm_db.bind_param(pstmt,4,email)
            ibm_db.bind_param(pstmt,5,pw)
            ibm_db.execute(pstmt)
            mg='You have successfully registered click signin!!'
            return render_template("login.html")      

    else:
        msg="fill out the form first!"
        return render_template('signup.html',meg=mg)

@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return render_template("home.html")

@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    mg=''
    if request.method == "POST":
        prodname=request.form['prodname']
        quantity=request.form['quantity']
        warehouse_location=request.form['warehouse_location'] 
        sql='SELECT * FROM product WHERE prodname =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,prodname)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            mg='Product already exits!!'
        else:
            insert_sql='INSERT INTO product VALUES (?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,prodname)
            ibm_db.bind_param(pstmt,2,quantity)
            ibm_db.bind_param(pstmt,3,warehouse_location)
            ibm_db.execute(pstmt)
            mg='You have successfully added the products!!'
            return render_template("dashboard.html")      

    else:
        msg="fill out the form first!"
        return render_template('add_stock.html',meg=mg)

@app.route('/delete_stock',methods=['GET','POST'])
def delete_stock():
    if(request.method=="POST"):
        prodname=request.form['prodname']
        sql2="DELETE FROM product WHERE prodname=?"
        stmt2 = ibm_db.prepare(conn, sql2)    
        ibm_db.bind_param(stmt2,1,prodname)
        ibm_db.execute(stmt2)

        flash("Product Deleted", "success")

        return render_template("dashboard.html")

@app.route('/update_stock',methods=['GET','POST'])
def update_stock():
    mg=''
    if request.method == "POST":
        prodname=request.form['prodname']
        quantity=request.form['quantity']
        quantity=int(quantity)
        print(quantity)
        print(type(quantity))
        warehouse_location=request.form['warehouse_location'] 
        sql='SELECT * FROM product WHERE prodname =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,prodname)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            insert_sql='UPDATE product SET  quantity=?,warehouse_location=? WHERE prodname=? '
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,quantity)
            ibm_db.bind_param(pstmt,2,warehouse_location)
            ibm_db.bind_param(pstmt,3,prodname)
            ibm_db.execute(pstmt)
            mg='You have successfully updated the products!!'
            limit=5
            print(type(limit))
            if(quantity<=limit):
                  alert("Please update the quantity of the product {}, Atleast {} number of pieces must be added!".format(prodname,10))
            return render_template("dashboard.html",meg=mg)   
            
        else:
             mg='Product not found!!'
               

    else:
         msg="fill out the form first!"
         return render_template('update_stock.html',meg=msg)

@app.route('/view_stock')
def view_stock():
   
    sql = "SELECT * FROM product"
    stmt = ibm_db.prepare(conn, sql)
    result=ibm_db.execute(stmt)
    print(result)

    products=[]
    row = ibm_db.fetch_assoc(stmt)
    print(row)
    while(row):
        products.append(row)
        row = ibm_db.fetch_assoc(stmt)
        print(row)
    products=tuple(products)
    print(products)

    if result>0:
        return render_template('view.html', products = products)
    else:
        msg='No products found'
        return render_template('view.html', msg=msg)

    

@app.route('/delete')
def delete():
    return render_template('delete_stock.html')

@app.route('/update')
def update():
    return render_template('update_stock.html')
    

if __name__ == "__main__":
    app.run(debug=True)
    
   

