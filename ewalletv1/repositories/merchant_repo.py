import sqlite3
from ewalletv1.repositories import program_variable

class MerchantRepo:
    @staticmethod
    def get_api_key(account_id):
        qr = '''
            SELECT api_key FROM Merchant WHERE account_id = (?)
        '''
        with sqlite3.connect(program_variable.DBPATH) as conn:
            c = conn.cursor()
            c.execute(qr, (account_id,))
            rs = c.fetchone()
            if rs:
                return rs[0]
            return None