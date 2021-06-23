from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_index():
    return 'Hello! You search servers IP and his port.'

