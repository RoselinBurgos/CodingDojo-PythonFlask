from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)

mysql = connectToMySQL('friendsdb')
print("all the users", mysql.query_db("SELECT * FROM friends;"))


@app.route('/')
def index():
    mysql = connectToMySQL("friendsdb")
    all_friends = mysql.query_db("SELECT * FROM friends")
    print("Fetched all friends", all_friends)
    return render_template('index.html', all_friends=all_friends)

@app.route('/results', methods=['POST'])
def create():
    firstname = request.form['firstname']
    lastname= request.form['lastname']
    occupation = request.form['occupation']

    mysql = connectToMySQL("friendsdb")
    query = "INSERT INTO friends (first_name, last_name, occupation,created_at,updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s,NOW(),NOW());"
    data = {
             'first_name': request.form['firstname'],
             'last_name':  request.form['lastname'],
             'occupation': request.form['occupation']
            }
    mysql.query_db(query, data)
    return redirect('/')

if __name__=="__main__":   
    app.run(debug=True) 

