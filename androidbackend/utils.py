import json
from hashlib import md5
import os


def message(**kwargs):
    msg = {
        'msg': kwargs.get('msg', ''),
        'status': kwargs.get('status', 'fail')
    }
    access_token = kwargs.get('access_token', '')
    if access_token:
        msg['access_token'] = access_token
    return msg


def make_security(data):
    return md5(data).hexdigest()


def upload_to(instance, filename):
    return os.path.join(str(instance.id), filename)
