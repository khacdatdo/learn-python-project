def response_with_success(data):
    response = {
        'data': data,
        'message': 'Thành công'
    }
    return response
    

def response_with_errors(errors):
    response = {
        'errors': errors,
        'message': 'Sao mày ngu thế?'
    }
    return response