from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import pandas as pd
#from flask_sqlalchemy import SQLAlchemy
import time
from App import application

#application = Flask(__name__)

#here we are routing/mapplicationing using decorator '@' -- use it to map URL to return value
#the response to the URL is what the function returns
# @ signifies a decorator
@application.route('/', methods=['GET', 'POST'])

def index():
	if request.method == 'POST':
		race = str(request.form.get('race'))
		return render_template('mainpage.html',map = race+ '.html')
	else:
		return render_template('mainpage.html', map= 'blank.html')


@application.route('/about')
def about():
    return 'This is the about page'

@application.route('/test')
def test():
    return '<h2>Testing</h2>' #you can write html in here!

#now username is a variable if inside "<>"
@application.route('/profile/<username>')
def profile(username):
   return '<h2>Hey there %s<h2>' % username

#for integers you need to specify type int
@application.route('/post/<int:post_id>')
def post(post_id):
   return '<h2>Post ID is %s<h2>' % post_id

#Using HTML Templates
@application.route("/profile2/<name>")
def profile2(name):
    return render_template("profile.html",name=name)

if __name__ == "__main__":
    application.run(host='0.0.0.0',debug=True)
