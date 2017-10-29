#!/usr/local/bin/python3

from flask import Flask, abort, make_response, jsonify, request
import mongo

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/addcomment', methods = ['POST'])
def addComment():
    if request.method == 'POST':
        url = request.form['url']
        comment = request.form['comment']
        location = request.form['location']
        print(url, comment, location)
        return add_new_comment_to_db(url, comment, location)
    else:
        return "Bad request."

@app.route('/gettopcomments', methods = ['GET'])
def getTopComments():
    if request.method == 'GET':
        url = request.args.get('url')
        k = request.args.get('k')
        top_comments = mongo.get_top_k_comments(url, k)
        print(top_comments)
        return "a"

if __name__ == '__main__':
    app.run(debug=False)