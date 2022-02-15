import sqlite3
import uuid
import jwt
import logging
import os
import functools
import json
import hashlib
from ewalletv1.repositories.account_repo import AccountRepo
from ewalletv1.repositories.merchant_repo import MerchantRepo
from flask_restful import request

DBPATH = "/Users/thdg/PycharmProjects/eWalletv1/ewallet.db"
UNSUCCESSFUL_MESSAGE = {'message': 'Unsuccessful'}
REJECTED_MESSAGE = {
    'message': 'Rejected',
    'detail': 'Your token is incorrect'
    }
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def uuid_generator():
    return str(uuid.uuid4())

def signature_generator(**kwargs):
    del kwargs['signature']
    to_encode = json.dumps(kwargs)
    rs = hashlib.md5(to_encode.encode())
    return rs.hexdigest()

def check_signature(**kwargs):
    rs = signature_generator(**kwargs)
    if rs == kwargs['signature']:
        return True
    return False


def token_decode(token, api_key=None):
    if api_key:
        return jwt.decode(token, api_key, algorithms = ["HS256"])
    return jwt.decode(token, options={"verify_signature": False})


def jwt_required(type):
    def decorate_func(func):
        @functools.wraps(func)
        def decorated_func(*args, **kwargs):
            try:
                rq = request.get_json()
                token = request.headers.getlist(key="Authorization")[0].split()[1]
            except Exception:
                return REJECTED_MESSAGE, 400
            else:
                account_id = token_decode(token).get("accountId", None)
                if type == "merchant":
                    api_key = MerchantRepo.get_api_key(account_id)
                    account_id = token_decode(token, api_key).get("accountId", None)
                if account_id == rq['accountId']:
                    return func(*args, **kwargs)
                return REJECTED_MESSAGE, 400
        return decorated_func
    return decorate_func


def logging_helper():
    def setup_logger():
        time = datetime.datetime.now()

        file_name = os.path.join(DIR_PATH, f"{str(time.date())}.log")

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)

        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(c_handler)
        return logger

