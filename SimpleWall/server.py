from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
from time import strftime, localtime
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'TheSecretKey'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


mysql = connectToMySQL('wall')
print("all the users", mysql.query_db("SELECT * FROM users;"))

@app.route('/')
def index():

    mysql = connectToMySQL("wall")
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
  

        mysql = connectToMySQL("wall")
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
    
    mysql = connectToMySQL("wall")
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


# @app.route('/main')
# def main():
#     if not 'id' in session:
#         print("-------INVALID-------")
#         return redirect ('/')
#     else:
#         print("Logged in")
#         return render_template('index2.html')

@app.route('/main')
def home_index():

    if not 'id' in session:
        print("-------INVALID-------")
        return redirect ('/')

    time = strftime('%Y-%m-%d %H:%M:%S', localtime())
    mysql = connectToMySQL('wall')
    query = "select * from messages JOIN users on messages.sender_id = users.id WHERE recipient_id = %(user_id)s"
    data = {
        'user_id':session['id']
    }
    messages = mysql.query_db(query,data)
    mysql2 = connectToMySQL('wall')
    send_query = "SELECT * FROM users WHERE NOT id = %(user_id)s;"
    send_data ={
            'user_id':session['id']
        }
    send_check = mysql2.query_db(send_query,send_data)
    return render_template('index2.html',messages=messages,send_check = send_check )

@app.route('/delete_message/<message_id>')
def del_msg(message_id):
    mysql = connectToMySQL('wall')
    query = 'select * from messages where id = %(message_id)s;'
    data = {
        'message_id':message_id
    }
    check = mysql.query_db(query,data)
    if check[0]['recipient_id'] != session['id']:
        return redirect('/danger')
    elif check[0]['recipient_id'] == session['id']:
        mysql = connectToMySQL('wall')
        query = "DELETE FROM messages where id = %(message)s"
        data = {
            'message':message_id
        }
        mysql.query_db(query,data)
        return redirect('/main')

@app.route('/send_message', methods = ['POST'])
def send_msg():
    mysql = connectToMySQL('wall')
    query = "SELECT * FROM users WHERE id = %(id)s "
    data = {
        "id":request.form['button']
    }
    users = mysql.query_db(query,data) 

    mysql = connectToMySQL('wall')
    query = "INSERT INTO messages (sender_id, recipient_id, message, created_at, updated_at) VALUES (%(sender_id)s, %(recipient_id)s, %(message)s, NOW(), NOW());"
    data = {
            "sender_id":session['id'],
            "recipient_id":request.form['button'],
            "message":request.form['message']
        }
    mysql.query_db(query,data)
    # session['sent_msg_cnt'] += 1
    return redirect('/main')








@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)