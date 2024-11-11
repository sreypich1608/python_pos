from app import app, render_template, request, redirect
import requests
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.route('/crud')
def crud():
    result = connection.execute(text("Select * from user"))
    connection.commit()
    return render_template('crud.html', user_result=result)


@app.post('/create')
def create():
    name = request.form.get('name')
    gender = request.form.get('gender')
    address = request.form.get('address')
    result = connection.execute(text(f"insert into user values (null ,'{name}' ,'{gender}' ,'{address}' )"))
    connection.commit()
    return redirect('/crud')


@app.get('/confirm_edit')
def confirm_edit():
    user_id = request.args.get('id')
    result = connection.execute(text(f"SELECT * FROM user WHERE id ={user_id}"))
    connection.commit()
    data = []
    for user in result:
        print(user)
        data.append({'id':user[0], 'name':user[1], 'gender':user[2], 'address':user[3]})
    return render_template('confirm_edit.html', data=data)


@app.get('/confirm_delete')
def confirm_delete():
    user_id = request.args.get('id')
    result = connection.execute(text(f"SELECT * FROM user WHERE id ={user_id}"))
    connection.commit()
    data = []
    for user in result:
        print(user)
        data.append({'id':user[0], 'name':user[1], 'gender':user[2], 'address':user[3]})
    return render_template('confirm_delete.html', data=data)


@app.post('/edit')
def edit():
    user_id = request.form.get('id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    address = request.form.get('address')
    result = connection.execute(text(f"UPDATE user SET name='{name}', gender='{gender}', address='{address}' WHERE id={user_id}"))
    connection.commit()
    return redirect('/crud')

@app.get('/delete_user')
def delete_user():
    user_id = request.args.get('id')
    result = connection.execute(text("DELETE FROM user WHERE id =" + user_id))
    connection.commit()
    return redirect('/delete')


@app.route('/delete')
def delete():
    result = connection.execute(text("SELECT * FROM USER"))
    connection.commit()
    return render_template('crud.html', user_result=result)
