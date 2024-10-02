import secrets
import string

def ran_code(size):
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(size))
    return res
