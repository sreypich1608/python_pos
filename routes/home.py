from app import app, render_template, request
import requests


@app.route('/')
@app.route('/home')
def hello_world():
    product_list = []
    res = requests.get('https://fakestoreapi.com/products')
    res_json = res.json()
    print(res_json)

    return render_template('home.html', product_list=res_json)


@app.get('/shop_now')
def shopNow():
    id = request.args.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{id}")
    json = res.json()
    return render_template('shop_now.html', product=json)


@app.get('/check_out')
def checkout():
    id = request.args.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{id}")
    json = res.json()
    return render_template('checkout.html', product=json)
