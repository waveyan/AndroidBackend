import json
from hashlib import md5


def message(**kwargs):
    msg={
        'msg':kwargs.get('msg',''),
        'status':kwargs.get('status','fail')
    }
    access_token=kwargs.get('access_token','')
    if access_token:
        msg['access_token']=access_token
    return json.dumps(msg)

def make_security(data):
    return md5(data).hexdigest()