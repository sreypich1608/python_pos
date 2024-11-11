from app import app, render_template


@app.errorhandler(404)
def error(e):
    return render_template('error/404.html')


@app.errorhandler(500)
def error(e):
    return  render_template('error/500.html')
