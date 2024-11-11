from app import app, render_template, request
import requests
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.get('/admin/tag')
def tag():
    module = 'tag'
    return render_template('admin/tag.html', module=module)


@app.get('/admin/get-tag')
def gettag():
    return getTag_list()


@app.post('/admin/create-tag')
def create_tag():
    format_data = request.get_json()
    name = format_data['name']
    description = format_data['description']
    inser_query = text(f"insert into tag values (null ,'{name}','{description}')")
    result = connection.execute(inser_query)
    connection.commit()
    return [name, description]


@app.post('/admin/delete-tag')
def deletetag():
    format_data = request.get_json()
    tag_id = format_data['tag_id']
    # Use parameterized queries to prevent SQL injection
    delete_query = text("""
        DELETE FROM tag WHERE id = :tag_id;
        """)
    # Execute the query with parameters
    result = connection.execute(delete_query, {'tag_id': tag_id})
    connection.commit()
    return f"{tag_id}"


@app.post('/admin/update-tag')
def update_tag():
    format_data = request.get_json()
    tag_id = format_data['id']
    name = format_data['name']
    description = format_data['description']
    result = connection.execute(text(f"""
    UPDATE `tag` SET `name` = '{name}', 
    description = '{description}'
    WHERE id = '{tag_id}'
    """))
    connection.commit()
    return [tag_id,name, description]


def getTag_list():
    select_query = text("Select * from tag ORDER BY id ASC;")
    result = connection.execute(select_query)
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