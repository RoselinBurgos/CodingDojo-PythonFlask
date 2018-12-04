from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
app = Flask(__name__)

bcrypt = Bcrypt(app)
app.secret_key = 'TheSecretKey'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


mysql = connectToMySQL('login_and_reg')
print("all the users", mysql.query_db("SELECT * FROM users;"))

@app.route('/')
def index():
    if 'sessionatlogin' not in session:
        session['sessionatlogin'] = True
    mysql = connectToMySQL("login_and_reg")
    all_users = mysql.query_db("SELECT * FROM users")
    print("Fetched all users", all_users)
    return render_template('index.html', all_users=all_users)

@app.route('/result', methods=['POST'])
def result():

    passFlag = False
    if len(request.form['first_name']) ==0:
        flash('Invalid first name','wrong')
        passFlag = True

    if not request.form['first_name'].isalpha():
        flash('First name has non-alpha character','wrong')
        passFlag = True

    if len(request.form['last_name']) < 1:
        flash('Invalid last name','wrong')
        passFlag = True

    if not request.form['last_name'].isalpha():
        flash('Last name has a non-alpha character','wrong')
        passFlag = True

    if len(request.form['email']) < 1:
        flash('Invalid email','wrong')
        passFlag = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email format','wrong')
        passFlag = True

    if len(request.form['password']) < 8:
        flash('Password must contain at least 8 characters', 'wrong')
        passFlag = True

    if request.form['password'] != request.form['c_password']:
        flash('Password does not match','wrong')
        passFlag = True

    if passFlag == True:
        return redirect('/')
    else:
        passcrypt = bcrypt.generate_password_hash(request.form['password'])
  

        mysql = connectToMySQL("login_and_reg")
        query = "INSERT INTO users (email,first_name, last_name, password,created_at,updated_at) VALUES (%(email)s,%(first_name)s, %(last_name)s, %(password)s,NOW(),NOW());"
        data = {
                'email': request.form['email'],
                'first_name': request.form['first_name'],
                'last_name':  request.form['last_name'],
                'password': passcrypt
                }
        user_id= mysql.query_db(query, data)
        session['id'] = user_id
        

        flash('Registartion Complete! You may now Login.', 'okgreen')
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    
    mysql = connectToMySQL("login_and_reg")
    query = "SELECT * From users WHERE email = %(email)s"
    data = {
            'email': request.form['email']
            }
    users = mysql.query_db(query,data)

    if len(users) == 0:
        flash("INVALID CREDENTIALS",'wrong')
        return redirect('/')
    user = users[0]
    if bcrypt.check_password_hash(user['password'], request.form['password']):
        session['id'] = user['id']
        session['first_name'] = user['first_name'] 
        return redirect('/main')
    else: 
        flash("INVALID CREDENTIALS",'wrong')
    return redirect('/')


@app.route('/main')
def main():
    if not 'id' in session:
        print("-------SCRAM-------")
        return redirect ('/')
    else:
        print("Logged in")
        return render_template('index2.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)