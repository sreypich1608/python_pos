from app import app, render_template, request
import requests


@app.get('/dashboard')
@app.get('/admin')
def dashboard():
    module = 'dachboard'
    return render_template('admin/dachboard.html',module=module)
