
from flask import Flask

app = Flask(__name__)


def hello_world():
    return "Hello World, I am bob. SUP!!!! "


@app.route('/')
def hello():
    message = hello_world()
    path = app.root_path
    return path