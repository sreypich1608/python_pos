from app import app, render_template, request, redirect
import requests
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


# @app.route('/crud')
# def crud():
#     result = connection.execute(text("Select * from user"))
#     connection.commit()
#     return render_template('crud.html', user_result=result)


@app.route('/getUser')
def getUser():
    result = connection.execute(text("Select * from user"))
    record = result.fetchall()
    data = []
    for item in record:
        data.append(
            {
                'id': item[0],
                'name': item[1],
                'gender': item[2],
                'address': item[3],
            }
        )
    connection.commit()
    return data


@app.post('/createUser')
def createUser():
    data = request.get_json()
    # print(data)
    name = data.get('name')
    gender = data.get('gender')
    address = data.get('address')
    result = connection.execute(text(f"insert into user values (null ,'{name}' ,'{gender}' ,'{address}' )"))
    connection.commit()
    return 'sucess'


@app.post('/updateUser')
def updateUser():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    gender = data.get('gender')
    address = data.get('address')
    result = connection.execute(text(f"UPDATE user SET name='{name}', gender='{gender}', address='{address}' WHERE id={user_id}"))
    connection.commit()
    return f'{user_id}'

@app.post('/deleteUser')
def deleteUser():
    data = request.get_json()
    user_id = data.get('user_id')
    result = connection.execute(text(f"DELETE FROM `user` WHERE id = {user_id}"))
    connection.commit()
    return f'{user_id}'

