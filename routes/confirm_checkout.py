from app import app, render_template, request
import requests
from short_cut import checkout_bot

@app.post('/conform_checkout')
def conform_checkout():
    product_id = request.form.get('product_id')
    res = requests.get(f"https://fakestoreapi.com/products/{product_id}")
    product = res.json()
    cust_name = request.form.get('name')
    cust_phone = request.form.get('phone')
    cust_email = request.form.get('email')
    cust_address = request.form.get('address')
    cust_message = request.form.get('messageToSeller')
    checkout_bot.conform_tel_bot(cust_name, cust_email, cust_phone, cust_address, cust_message, product)
    return 'work'
