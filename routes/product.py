from app import app, render_template
import requests

@app.route('/product')
def productList():
    return render_template('product_item_card_1.html')
