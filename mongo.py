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


def auth():
    fb = firebase()
    auth = fb.auth()
    user = auth.sign_in_with_email_and_password("test@test.com", "ganggang")
    db = fb.database()
    return db, user


def hash_url(url):
    encoded_url = url.replace('.', '||DOT||')
    encoded_url = encoded_url.replace('%', '||PERCENT||')
    encoded_url = encoded_url.split('?')[0]
    print(encoded_url)
    return encoded_url


def add_new_comment_to_db(url, comment, serialized_location):
    encoded_url = hash_url(url)
    db, user = auth()
    does_exist = db.child("websites/" + encoded_url).get().val()
    if does_exist is None:
        db.child("websites").child(encoded_url).set('')
    data = {
        'comment': comment,
        'stars': 1,
        'location': serialized_location
    }
    comment_hash = db.child("websites").child(encoded_url).push(data)
    return comment_hash


def push_comment_like_to_db(url, comment_hash):
    encoded_url = hash_url(url)
    db, user = auth()
    num_stars = db.child("websites/" + encoded_url + "/" + comment_hash + "/" + "stars").get().val() + 1
    print(num_stars)
    db.child("websites/" + encoded_url + "/" + comment_hash).update({'stars': num_stars})
    return


def top10Comments(url):
    db = auth()
    encoded_url = hash_url(url)
    comments = db[url]
    print(comments)
    # comments.sort() # thumbs up are the first element in the tuple
    # return comments[:10]

ch = add_new_comment_to_db('https%3A%2F%2Fwww.nytimes.com%2F2017%2F08%2F12%2Fus%2Fpolitics%2Felizabeth-warren-democrats-liberals.html%3F_r%3D1','im gonna knock it. it\'s a little gay', '5')['name']
push_comment_like_to_db('https%3A%2F%2Fwww.nytimes.com%2F2017%2F08%2F12%2Fus%2Fpolitics%2Felizabeth-warren-democrats-liberals.html%3F_r%3D1', ch)