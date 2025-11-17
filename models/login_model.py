USERS = [
    {
        'id': 1,
        'username': 'ibrahim',
        'password': 'nopassword',
        'email': 'ibrahim@google.com'
    },
    {
        'id': 2,
        'username': 'tyler',
        'password': 'nopassword1',
        'email': 'tyler@google.com'
    },
    {
        'id': 3,
        'username': 'marin',
        'password': 'nopassword2',
        'email': 'marin@google.com'
    }
]


def validate_login(username, password):
    for user in USERS:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def get_user_by_username(username):
    for user in USERS:
        if user['username'] == username:
            return user
    return None     

