from app import app, render_template, request
import requests
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.get('/admin/user')
def user():
    module = 'user'
    return render_template('admin/user.html', module=module)


@app.get('/admin/get-user')
def getuser():
    result = connection.execute(text("Select * from user"))
    record = result.fetchall()
    data = []
    for item in record:
        data.append(
            {
                'id': item[0],
                'name': item[1],
                'gender': item[2],
                'password': item[3],
                'email': item[4],
                'phone': item[5],
                'address': item[6],
            }
        )
    connection.commit()
    return data


@app.post('/admin/create-user')
def create_user():
    format_data = request.get_json()
    name = format_data['name']
    gender = format_data['gender']
    password = format_data['password']
    email = format_data['email']
    phone = format_data['phone']
    address = format_data['address']
    result = connection.execute(text(f"insert into user "
    f"values (null ,'{name}','{gender}','{password}','{email}','{phone}','{address}')"))
    connection.commit()
    return [name, gender, password, email, phone, address]


@app.post('/admin/delete-user')
def deleteuser():
    format_data = request.get_json()
    user_id = format_data['user_id']
    result = connection.execute(text(f"delete from user where id = '{user_id}'"))
    connection.commit()
    return f"{user_id}"


@app.post('/admin/update-user')
def update_user():
    format_data = request.get_json()
    user_id = format_data['id']
    name = format_data['name']
    gender = format_data['gender']
    password = format_data['password']
    email = format_data['email']
    phone = format_data['phone']
    address = format_data['address']
    result = connection.execute(text(f"""
    UPDATE `user` SET `name` = '{name}', 
    gender = '{gender}', 
    `password` = '{password}', 
    email = '{email}', 
    phone = '{phone}', 
    address = '{address}' 
    WHERE id = '{user_id}';
    """))
    connection.commit()
    return [user_id,name, gender, password, email, phone, address]
