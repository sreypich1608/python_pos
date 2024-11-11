from app import app, render_template, request
import requests
from short_cut import contact_tel_bot

@app.post('/submit_contact')
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    contact_tel_bot.conform_tel_bot(name, email, phone, address)
    # print(res.status_code)
    return f'work'
