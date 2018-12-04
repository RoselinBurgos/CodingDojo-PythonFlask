from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)

mysql = connectToMySQL('lead_gen_business')
print("List of top 4 clients", mysql.query_db("SELECT * FROM clients WHERE client_id < 5;"))


@app.route('/')
def index():
    mysql = connectToMySQL("lead_gen_business")

    all_clients = mysql.query_db("SELECT CONCAT(clients.first_name,' ',clients.last_name) AS NAME, COUNT(leads.leads_id) AS leads FROM clients JOIN sites ON clients.client_id = sites.client_id JOIN leads on sites.site_id = leads.site_id where clients.client_id < 5 group by clients.first_name order by clients.client_id;")


    
    print("Fetched top 4 Clients", all_clients)
    return render_template('index.html', all_clients=all_clients)



if __name__=="__main__":   
    app.run(debug=True) 

