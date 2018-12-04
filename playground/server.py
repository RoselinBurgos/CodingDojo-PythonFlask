# Level 1 Playground
# When a user visits http://localhost:5000/play, have it render three beautiful looking blue boxes.

# Level 2 Playground
# When a user visits localhost:5000/play/(x), have it display the beautiful looking blue boxes x times.  
# For example, localhost:5000/play/7 should display these blue boxes 7 times. 

# Level 3 Playground
# When a user visits localhost:5000/play/(x)/(color), have it display beautiful looking boxes x times,
# but this time where the boxes appear in (color).  
# For example, localhost:5000/play/5/green would display 5 beautiful green boxes. 


from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index1.html")


@app.route('/play/<x>')
def play2(x):
    times = int(x)
    return render_template("index2.html", times = times)    

@app.route('/play/<x>/<color>')
def play3(x,color):
    times = int(x)
    color = color
    return render_template("index3.html", times = times, color = color) 


if __name__ =="__main__":
    app.run(debug=True)   