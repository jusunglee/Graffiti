#!/usr/local/bin/python3

from flask import Flask, abort, make_response, jsonify
import mongo

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/<firstname>')
def index(firstname):
    mongo.push()
    return "Pushed."

if __name__ == '__main__':
    app.run(debug=False)