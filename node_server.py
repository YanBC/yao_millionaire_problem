from flask import Flask

app = Flask(__name__)

@app.route('/public_key', methods=['POST'])
def get_peer