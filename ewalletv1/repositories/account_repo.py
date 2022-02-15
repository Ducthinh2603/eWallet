import sqlite3
from ewalletv1.repositories import program_variable
import jwt

class AccountRepo:
    @staticmethod
    def get_account(account_id):
        get_account_qr = '''
                SELECT * FROM Account WHERE account_id = (?)
            '''
        with sqlite3.connect(program_variable.DBPATH) as conn:
            c = conn.cursor()
            c.execute(get_account_qr, (account_id,))
            rs = c.fetchone()
            if rs:
                account_id = rs[0]
                account_type = rs[1]
                return account_id, account_type
            return None

    @staticmethod
    def get_token(account_id):
        _id, type = AccountRepo.get_account(account_id)
        if _id:
            if type == "merchant":
                get_key_qr = '''
                    SELECT api_key FROM Merchant WHERE account_id = (?)
                '''
                with sqlite3.connect(program_variable.DBPATH) as conn:
                    c = conn.cursor()
                    c.execute(get_key_qr, (_id,))
                    api_key = c.fetchone()[0]
                token = jwt.encode({"accountId": _id}, api_key, algorithm="HS256")
            elif type == "personal":
                token = jwt.encode({"accountId": _id}, "secret", algorithm="HS256")
            return {
                       'token': token
                   }, 200
        return {
                   'message': "account doesn't exist."
               }, 400

    @staticmethod
    def topup_account(account_id, amount):
        topup_qr = '''
            UPDATE Account SET balance = balance + (?) WHERE account_id = (?)
        '''
        with sqlite3.connect(program_variable.DBPATH) as conn:
            c = conn.cursor()
            try:
                c.execute(topup_qr, (amount, account_id))
            except Exception:
                return helper.UNSUCCESSFUL_MESSAGE, 400
            else:
                get_account_qr = '''
                        SELECT * FROM Account WHERE account_id = (?)
                    '''
                c.execute(get_account_qr, (account_id,))
                account = c.fetchone()
                response = {
                    'message': 'Succesful.',
                    'detail': {
                        'accountId': account[0],
                        'balance': account[2]
                    }
                }
                return response, 200