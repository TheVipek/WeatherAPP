from flask import Flask
from flask.templating import render_template
import logging
app = Flask(__name__)
logging.basicConfig(filename="events.log",level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


from views import *
if __name__ == "__main__":
    app.run(debug=True)