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