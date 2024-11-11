from app import app, render_template, request
import requests
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.get('/admin/unit')
def unit():
    module = 'unit'
    return render_template('admin/unit.html', module=module)


@app.get('/admin/get-unit')
def getunit():
    return getUnit_list()


@app.post('/admin/create-unit')
def create_unit():
    format_data = request.get_json()
    name = format_data['name']
    description = format_data['description']
    result = connection.execute(text(f"insert into unit values (null ,'{name}','{description}')"))
    connection.commit()
    return [name, description]


@app.post('/admin/delete-unit')
def deleteunit():
    format_data = request.get_json()
    unit_id = format_data['unit_id']
    result = connection.execute(text(f"delete from unit where id = '{unit_id}'"))
    connection.commit()
    return f"{unit_id}"


@app.post('/admin/update-unit')
def update_unit():
    format_data = request.get_json()
    unit_id = format_data['id']
    name = format_data['name']
    description = format_data['description']
    result = connection.execute(text(f"""
    UPDATE `unit` SET `name` = '{name}', 
    description = '{description}'
    WHERE id = '{unit_id}'
    """))
    connection.commit()
    return [unit_id,name, description]


def getUnit_list():
    result = connection.execute(text("Select * from unit"))
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