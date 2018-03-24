from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from App import application

#here we are routing/mapplicationing using decorator '@' -- use it to map URL to return value
#the response to the URL is what the function returns
# @ signifies a decorator
@application.route('/', methods=['GET', 'POST'])

def index():
	"""
	Render Mainpage - also passes map html when called by maingpage.html
	:return: Rendered mainpage
	"""
	if request.method == 'POST':
		race = str(request.form.get('race'))
		return render_template('mainpage.html',map = race+ '.html')
	else:
		return render_template('mainpage.html', map= 'blank.html')


if __name__ == "__main__":
    application.run(host='0.0.0.0',debug=True)
