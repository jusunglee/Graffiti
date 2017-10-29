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
    return encoded_url


def add_new_comment_to_db(url, comment, serialized_location, timestamp):
    encoded_url = hash_url(url)
    db, user = auth()
    does_exist = db.child("websites/" + encoded_url).get().val()
    if does_exist is None:
        db.child("websites").child(encoded_url).set('')
    data = {
        'comment': comment,
        'stars': 0,
        'location': serialized_location,
        'timestamp': timestamp
    }
    comment_hash = db.child("websites").child(encoded_url).push(data)['name']
    return comment_hash


def push_comment_like_to_db(url, comment_hash):
    encoded_url = hash_url(url)
    db, user = auth()
    num_stars = db.child("websites/" + encoded_url + "/" + comment_hash + "/" + "stars").get().val() + 1
    db.child("websites/" + encoded_url + "/" + comment_hash).update({'stars': num_stars})
    return str(num_stars)


def get_top_k_comments(url, k=10):
    encoded_url = hash_url(url)
    db, user = auth()
    does_exist = db.child("websites/" + encoded_url).get().val()
    if does_exist is None:
        return ''
    comments_list = dict(db.child("websites/" + encoded_url).get().val())
    sorted_list = sorted(comments_list, key=lambda k_: comments_list[k_]['timestamp'], reverse=True)[:k]
    sorted_list_dict = [[k_, comments_list[k_]] for k_ in sorted_list]
    # sorted_list = sorted(comments_list, key=lambda k_: comments_list[k_]['timestamp'], reverse=True)[:k]
    # for item in sorted_list:
    #     sorted_list_dict.append([item, comments_list[item]])
    return sorted_list_dict
    

if __name__ == "__main__":
    pass
    # test_url = 'https%3A%2F%2Fwww.nytimes.com%2F2017%2F08%2F12%2Fus%2Fpolitics%2Felizabeth-warren-democrats-liberals.html%3F_r%3D1'
    # # ch = add_new_comment_to_db(test_url,'im gonna knock it. it\'s a little gay', '5')['name']
    # push_comment_like_to_db(test_url, ch)
    # get_top_k_comments(test_url)
