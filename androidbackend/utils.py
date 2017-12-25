from hashlib import md5


def message(**kwargs):
    msg = {
        'msg': kwargs.get('msg', ''),
        'status': kwargs.get('status', 'fail'),
        'id': kwargs.get('instance_Id', '')
    }
    access_token = kwargs.get('access_token', '')
    if access_token:
        msg['access_token'] = access_token
    return msg


def make_security(data):
    return md5(data).hexdigest()


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
