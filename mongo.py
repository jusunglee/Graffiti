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


def push(db1, user, key, val):
    fb = firebase()
    auth = fb.auth()
    user = auth.sign_in_with_email_and_password("test@test.com", "ganggang")
    db = fb.database()
    # usercount = db.child("howdy").get(user['idToken']).val()
    data = {
        'dawins': 'dessert'
    }
    db.child("howdy").push(data, user['idToken'])
    # db.child("howdy").child("1").set(data)
    return "Hello"