from email.headerregistry import Address
from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.flask_db
students = db.student



@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        students.insert_one({'firstname': firstname, 'lastname': lastname, 'Address': address})
        return redirect(url_for('index'))

    all_stud = students.find()
    return render_template('index.html', all_stud=all_stud)

@app.route('/<id>/delete/')
def delete(id):
    students.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))   

@app.route('/<id>/update/', methods=('GET', 'POST'))
def update(id):
    selected_stud = students.find_one({"_id": ObjectId(id)})       
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        students.update_one({"_id": ObjectId(id)},
            {"$set":{"firstname":firstname,"lastname":lastname,"Address":address},
        # {"$set":{"firstname":"bdjff","lastname":"jjfhjfh","Address":"jfdjf"},
            })
        return redirect(url_for('index'))       
     
    return render_template('update.html', selected_stud=selected_stud )


if __name__ == "__main__":
    app.run(debug=True)