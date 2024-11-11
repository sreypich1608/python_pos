from app import app, render_template


@app.route('/about')
def hello_about():
    return render_template('about.html')
