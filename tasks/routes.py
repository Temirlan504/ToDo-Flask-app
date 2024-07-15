from flask import render_template
from tasks import app

@app.route('/')
def home():
    return "Hello, World!"
