from quizz.models import User


def response_with_success(data, message='Success'):
    response = {
        'data': data,
        'message': message
    }
    return response
    

def response_with_errors(errors, message='Error'):
    response = {
        'errors': errors,
        'message': message
    }
    return response


def auth(token):
    try:
        user = User.objects.get(token=token)
        return user
    except:
        return None

def create_token(max_length = 100):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(max_length))

def hashPassword(password):
    import hashlib
    return hashlib.md5(password.encode('utf-8')).hexdigest()