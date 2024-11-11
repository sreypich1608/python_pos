from app import app, render_template, request
import requests
from sqlalchemy import create_engine, text
from routes.admin import category
from routes.admin import tag
from routes.admin import brand
from routes.admin import unit

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.get('/admin/product')
def product():
    module = 'product'
    return render_template('admin/product.html', module=module)


@app.get('/admin/get-product')
def getproduct():
    category_list = category.getCategory_list()
    brand_list = brand.getBrand_list()
    tag_list = tag.getTag_list()
    unit_list = unit.getUnit_list()
    product_list = getProduct_list()
    return {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list': brand_list,
        'tag_list': tag_list,
        'unit_list': unit_list,
    }


@app.post('/admin/create-product')
def create_product():
    format_data = request.get_json()
    name = format_data['name']
    cost = format_data['cost']
    price = format_data['price']
    qty = format_data['qty']
    category_id = format_data['category']
    unit_id = format_data['unit']
    brand_id = format_data['brand']
    tag_ids = format_data['tag']  # Expecting tag_ids to be a list of tag IDs

    # Insert product and retrieve the new product ID
    result = connection.execute(text("""
    INSERT INTO product (name, cost, price, qty, category_id, unit_id, brand_id) 
    VALUES (:name, :cost, :price, :qty, :category_id, :unit_id, :brand_id)
    """), {'name': name, 'cost': cost, 'price': price, 'qty': qty, 'category_id': category_id, 'unit_id': unit_id,
           'brand_id': brand_id})
    product_id = result.lastrowid

    # Insert tags into the product_tag table
    for tag_id in tag_ids:
        connection.execute(text("INSERT INTO product_tag (product_id, tag_id) VALUES (:product_id, :tag_id)"),
                           {'product_id': product_id, 'tag_id': tag_id})

    connection.commit()
    return {"status": "success"}


@app.post('/admin/delete-product')
def deleteproduct():
    format_data = request.get_json()
    product_id = format_data['product_id']
    result = connection.execute(text(f"delete from product where id = '{product_id}'"))
    connection.commit()
    return f"{product_id}"


@app.post('/admin/update-product')
def update_product():
    format_data = request.get_json()
    product_id = format_data['id']
    name = format_data['name']
    cost = format_data['cost']
    price = format_data['price']
    qty = format_data['qty']
    category_id = format_data['category']
    unit_id = format_data['unit']
    brand_id = format_data['brand']
    tag_ids = format_data['tag']  # Expecting a list of tag IDs

    # Update product details
    connection.execute(text("""
    UPDATE product 
    SET name = :name, cost = :cost, price = :price, qty = :qty, category_id = :category_id, 
        unit_id = :unit_id, brand_id = :brand_id 
    WHERE id = :product_id
    """), {'name': name, 'cost': cost, 'price': price, 'qty': qty, 'category_id': category_id, 'unit_id': unit_id,
           'brand_id': brand_id, 'product_id': product_id})

    # Clear existing tags
    connection.execute(text("DELETE FROM product_tag WHERE product_id = :product_id"), {'product_id': product_id})

    # Insert new tags
    for tag_id in tag_ids:
        connection.execute(text("INSERT INTO product_tag (product_id, tag_id) VALUES (:product_id, :tag_id)"),
                           {'product_id': product_id, 'tag_id': tag_id})

    connection.commit()
    return {"status": "updated", "id": product_id}


def getProduct_list():
    result = connection.execute(text("""
            SELECT 
                p.id AS product_id,
                p.name AS product_name,
                p.cost,
                p.price,
                p.qty,
                c.name AS category_name,
                u.name AS unit_name,
                b.name AS brand_name,
                GROUP_CONCAT(CONCAT(t.id, ':', t.name) SEPARATOR ', ') AS tag_data
            FROM 
                product p
            LEFT JOIN 
                category c ON p.category_id = c.id
            LEFT JOIN 
                unit u ON p.unit_id = u.id
            LEFT JOIN 
                brand b ON p.brand_id = b.id
            LEFT JOIN 
                product_tag pt ON p.id = pt.product_id
            LEFT JOIN 
                tag t ON pt.tag_id = t.id
            GROUP BY 
                p.id
            ORDER BY 
                p.id ASC;

        """))
    record = result.fetchall()
    data = []
    for item in record:
        tag = []
        if item[8]:  # item[7] contains `tag_data` as "id:name, id:name, ..."
            for tag_pair in item[8].split(', '):
                tag_id, tag_name = tag_pair.split(':')
                tag.append({'id': int(tag_id), 'name': tag_name})
        data.append({
            'id': item[0],
            'name': item[1],
            'cost': item[2],
            'price': item[3],
            'qty': item[4],
            'category': item[5],
            'unit': item[6],
            'brand': item[7],
            'tag': tag,
            'image': f"https://picsum.photos/id/{item[0]}/150"
        })
    return data


def getProductByCategoryId(category_id):
    result = connection.execute(
        text("""
            SELECT 
                p.id AS product_id,
                p.name AS product_name,
                p.cost,
                p.price,
                p.qty,
                c.name AS category_name,
                u.name AS unit_name,
                b.name AS brand_name,
                GROUP_CONCAT(CONCAT(t.id, ':', t.name) SEPARATOR ', ') AS tag_data
            FROM 
                product p
            LEFT JOIN 
                category c ON p.category_id = c.id
            LEFT JOIN 
                unit u ON p.unit_id = u.id
            LEFT JOIN 
                brand b ON p.brand_id = b.id
            LEFT JOIN 
                product_tag pt ON p.id = pt.product_id
            LEFT JOIN 
                tag t ON pt.tag_id = t.id
            WHERE c.id = :category_id
            GROUP BY 
                p.id
            ORDER BY 
                p.id ASC
        """), {"category_id": category_id}
    )

    record = result.fetchall()
    data = []
    for item in record:
        tag = []
        if item[8]:  # item[7] contains `tag_data` as "id:name, id:name, ..."
            for tag_pair in item[8].split(', '):
                tag_id, tag_name = tag_pair.split(':')
                tag.append({'id': int(tag_id), 'name': tag_name})
        data.append({
            'id': item[0],
            'name': item[1],
            'cost': item[2],
            'price': item[3],
            'qty': item[4],
            'category': item[5],
            'unit': item[6],
            'brand': item[7],
            'tag': tag,
            'image': f"https://picsum.photos/id/{item[0]}/150"
        })
    return data



