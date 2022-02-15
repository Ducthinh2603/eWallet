import sqlite3
from ewalletv1.controllers import helper


class AccountModel:
    def __init__(self, account_id, account_type, balance = 0):
        self.account_type = account_type
        self.account_id = account_id
        self.balance = balance

    @classmethod
    def add_account(cls, account_type):
        add_account_qr = '''
            INSERT INTO Account VALUES (?,?,0)
        '''
        with sqlite3.connect(helper.DBPATH) as conn:
            c = conn.cursor()
            try:
                account_id = helper.uuid_generator()
                c.execute(add_account_qr, (account_id, account_type))
            except Exception as e:
                return helper.UNSUCCESSFUL_MESSAGE
            else:
                return cls(account_id, account_type)











