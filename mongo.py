"""database contains the interface to interact directly with the firebase backend"""
import pyrebase


def firebase():
    """fireBase returns a firebase instance to be used when posting/reading from the database"""
    keys = "api_auth.txt"
    with open(keys) as file_:
        content = file_.readlines()

    config = dict()

    for line in content:
        tokens = line.split('=')
        tokens = [token.strip() for token in tokens]
        config[tokens[0]] = tokens[1]
    return pyrebase.initialize_app(config)


def push(encoded_url, comment):
    # usercount = db.child("howdy").get(user['idToken']).val()
    data = {
        'comments': [
            {
                'comment': comment,
                'stars': 1
            }
        ]
    }
    encoded_url = encoded_url.replace('{{DOT}}', '.')
    db = auth()
    db.child("websites/").child(encoded_url).set(data)
    return "Hello"


def auth():
    fb = firebase()
    auth = fb.auth()
    user = auth.sign_in_with_email_and_password("test@test.com", "ganggang")
    db = fb.database()
    return db


def top10Comments(url):
    db = auth()
    comments = db[url]
    print(comments)
    # comments.sort() # thumbs up are the first element in the tuple
    # return comments[:10]

push('https%3A%2F%2Fwww.nytimes.com%2F2017%2F08%2F12%2Fus%2Fpolitics%2Felizabeth-warren-democrats-liberals{{DOT}}html%3F_r%3D1','im gonna knock it. it\'s a little gay')