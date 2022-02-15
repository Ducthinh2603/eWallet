import sqlite3
from ewalletv1.models.account_model import AccountModel
from ewalletv1.controllers import helper
from ewalletv1.repositories import program_variable


class TransactionModel:
    def __init__(self, transaction_id, merchant_id,
                 income_account, outcome_account,
                 amount, extra_data, status):
        self.transaction_id = transaction_id
        self.merchant_id = merchant_id
        self.income_account = income_account
        self.outcome_account = outcome_account
        self.amount = amount
        self.extra_data = extra_data
        self.status = status

    @classmethod
    def create_transaction(cls, merchant_id, amount, extra_data):
        check_merchant = '''
            SELECT account_id FROM Merchant WHERE merchant_id = (?)
        '''
        with sqlite3.connect(helper.DBPATH) as conn:
            c = conn.cursor()
            c.execute(check_merchant,(merchant_id,))
            rs = c.fetchone()
            if rs:
                income_account = rs[0]
                outcome_account = None
                transaction_id = helper.uuid_generator()
                status = program_variable.INITIALIZED
                create_qr = '''
                    INSERT INTO Playbook VALUES (?, ?, ?, NULL, ?, ?, ?)
                '''
                c.execute(create_qr,(transaction_id, merchant_id,
                                        income_account, amount, status))
                return cls(transaction_id, merchant_id,
                            income_account, outcome_account,
                            amount, extra_data, status)
            return helper.UNSUCCESSFUL_MESSAGE

    @classmethod
    def get_transaction(cls, transaction_id):
        qr = '''
            SELECT * FROM Playbook WHERE transaction_id = (?)
            '''
        with sqlite3.connect(helper.DBPATH) as conn:
            c = conn.cursor()
            c.execute(qr,(transaction_id,))
            rs = c.fetchone()
            if rs:
                return cls(*rs)
            return None




