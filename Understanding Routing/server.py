# Create a server file that generates 5 different http responses for the following 5 url requests:

# localhost:5000 - have it say "Hello World!" - Hint: If you have only one route that your server is listening for, it must be your root route ("/")
# localhost:5000/dojo - have it say "Dojo!"
# localhost:5000/say/flask - have it say "Hi Flask".  Have function say() handle this routing request.
# localhost:5000/say/michael - have it say "Hi Michael" (have the same function say() handle this routing request)
# localhost:5000/say/john - have it say "Hi John!" (have the same function say() handle this routing request)
# localhost:5000/repeat/35/hello - have it say "hello" 35 times! - You will need to convert a string "35" to an integer 35.  To do this use int().  For example int("35") returns 35.  If the user request localhost:5000/repeat/80/hello, it should say "hello" 80 times.
# localhost:5000/repeat/99/dogs - have it say "dogs" 99 times! (have this be handled by the same route function as #6)



from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>hello world<h1>"

@app.route("/dojo")
def coding():
    return "<h1>Dojo</h1>"

@app.route('/say/<bark>')
def say(bark):
    return "Hi " + bark
# This does numbers 3-5

@app.route("/repeat/<count>/<last>")
def printer(count,last):
    new = ""
    for i in range(int(count)):
        new += last      
    return new  


if __name__ =="__main__":
    app.run(debug=True)   