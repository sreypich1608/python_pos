from app import app, render_template, request
import requests
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.get('/admin/category')
def category():
    module = 'category'
    return render_template('admin/category.html', module=module)


@app.get('/admin/get-category')
def getcategory():
    return getCategory_list()


@app.post('/admin/create-category')
def create_category():
    format_data = request.get_json()
    name = format_data['name']
    description = format_data['description']
    result = connection.execute(text(f"insert into category values (null ,'{name}','{description}')"))
    connection.commit()
    return [name, description]


@app.post('/admin/delete-category')
def deletecategory():
    format_data = request.get_json()
    category_id = format_data['category_id']
    result = connection.execute(text(f"delete from category where id = '{category_id}'"))
    connection.commit()
    return f"{category_id}"


@app.post('/admin/update-category')
def update_category():
    format_data = request.get_json()
    category_id = format_data['id']
    name = format_data['name']
    description = format_data['description']
    result = connection.execute(text(f"""
    UPDATE `category` SET `name` = '{name}', 
    description = '{description}'
    WHERE id = '{category_id}'
    """))
    connection.commit()
    return [category_id,name, description]


def getCategory_list():
    result = connection.execute(text("Select * from category;"))
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