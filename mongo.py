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
    """push takes a datbase reference a key and val as strings and pushes them
     to the given database. No return value"""
    db1.child(key).set(val, user['idToken'])
    usercount = db1.child("UserCount").get(user['idToken']).val()
