from email.headerregistry import Address
from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import psycopg2
from bson.objectid import ObjectId
from simple_salesforce import Salesforce, SalesforceLogin, SFType

app = Flask(__name__)
# client = MongoClient('localhost', 27017)
# # client = MongoClient('mongodb+srv://rohit:O46GepZHujtrKKxw@cluster0.vymfp.mongodb.net/test')
# db = client.flask_db
# students = db.student


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password='Password')
    return conn



# username = 'rohit.dhayarkar@orektic.com'
# password = 'Tprs@9172'
# security_Token = 'W6oL5WBUWzvsO6VjW9taFDkt'
# domain = 'login'

# sf = Salesforce(username=username, password=password, security_token=security_Token, domain=domain)

@app.route('/', methods=('GET', 'POST'))
def index():
    
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO studentsInfo(firstname, lastname, address)'
                    'VALUES (%s, %s, %s)',
                    (firstname, lastname, address))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM studentsInfo;') 
    all_studs = cur.fetchall() 
    cur.close()
    conn.close()
         
    
    # conn = get_db_connection()
    # cur = conn.cursor()
    
   
    # cur.close()
    # conn.close()    
    
    return render_template('index.html',all_studs = all_studs)


# @app.route('/', methods=('GET', 'POST'))
# def index():
#     if request.method=='POST':
#         firstname = request.form['firstname']
#         lastname = request.form['lastname']
#         address = request.form['address']
#         students.insert_one({'firstname': firstname, 'lastname': lastname, 'Address': address})
#         return redirect(url_for('index'))

#     QueryRecords ="""SELECT Id, Name FROM Account"""
#     AccountRecords = sf.query(QueryRecords)
#     return render_template('index.html', all_stud=AccountRecords)

@app.route('/<id>/delete/')
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor() 
    cur.execute("DELETE FROM studentsInfo WHERE id= %s",(id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/<id>/update/', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    cur = conn.cursor() 
    cur.execute("SELECT * from studentsInfo WHERE id= %s",(id,))
    selected_stud= cur.fetchone()
    print(selected_stud)
    conn.commit()
    cur.close()
    conn.close()
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE studentsInfo SET firstname = %s,lastname = %s, address = %s WHERE id = %s',
                    (firstname, lastname, address, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))      
     
    return render_template('update.html', selected_stud=selected_stud)


if __name__ == "__main__":
    app.run(debug=True)