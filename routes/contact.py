from app import app, render_template, request
import requests

@app.route('/contact')
def hello_contact():
    return render_template('contact.html')
