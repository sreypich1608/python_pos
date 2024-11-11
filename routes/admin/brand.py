from app import app, render_template, request
import requests
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.get('/admin/brand')
def brand():
    module = 'brand'
    return render_template('admin/brand.html', module=module)


@app.get('/admin/get-brand')
def getbrand():
    return getBrand_list()


@app.post('/admin/create-brand')
def create_brand():
    format_data = request.get_json()
    name = format_data['name']
    description = format_data['description']
    result = connection.execute(text(f"insert into brand values (null ,'{name}','{description}')"))
    connection.commit()
    return [name, description]


@app.post('/admin/delete-brand')
def deletebrand():
    format_data = request.get_json()
    brand_id = format_data['brand_id']
    result = connection.execute(text(f"delete from brand where id = '{brand_id}'"))
    connection.commit()
    return f"{brand_id}"


@app.post('/admin/update-brand')
def update_brand():
    format_data = request.get_json()
    brand_id = format_data['id']
    name = format_data['name']
    description = format_data['description']
    result = connection.execute(text(f"""
    UPDATE `brand` SET `name` = '{name}', 
    description = '{description}'
    WHERE id = '{brand_id}'
    """))
    connection.commit()
    return [brand_id,name, description]


def getBrand_list():
    result = connection.execute(text("Select * from brand"))
    record = result.fetchall()
    data = []
    for item in record:
        data.append(
            {
                'id': item[0],
                'name': item[1],
                'description': item[2],
            }
        )
    connection.commit()
    return data