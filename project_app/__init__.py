from flask import Flask, render_template
from markupsafe import escape

# from project_app.routes import 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('service.html')

