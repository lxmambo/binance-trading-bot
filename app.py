#this file contains the web application
from flask import Flask

#our app is a flask object
app = Flask[__name__]

#define some routes and a function to call
#when that route is accessed from the browser
@app.route('/')
def hello_world():
    return 'hello world!'

#export FLASK_APP = app.py
#flask run

#set FLASK_APP = app.py
#set FLASK_ENV=development
#flask run

if __name__ == "__main__":
    app.run()