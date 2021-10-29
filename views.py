from app import app
from flask import  render_template, g ,jsonify,request
@app.route('/')

def index():
    print(request.environ['REMOTE_ADDR'])
    return render_template('base.html')

@app.route('/one')
def one():
    return render_template('one.html')
