import sqlite3
from ewalletv1.repositories import program_variable
import time


class TransactionRepo:
    # @staticmethod
    # def check_transaction(transaction_id):
    #     qr = '''
    #         SELECT transaction_id FROM Playbook WHERE transaction_id = (?)
    #         '''
    #     with sqlite3.connect(program_variable.DBPATH) as conn:
    #         c= conn.cursor()
    #         c.execute(qr,(transaction_id,))
    #         rs = c.fetchone()
    #         if rs:
    #             return True
    #         return False

    @staticmethod
    def check_status_transaction(transaction_id):
        status_check = '''
            SELECT status FROM Playbook WHERE transaction_id = (?)
        '''
        with sqlite3.connect(program_variable.DBPATH) as conn:
            c = conn.cursor()
            c.execute(status_check, (transaction_id,))
            rs = c.fetchone()
            if rs:
                return rs[0]
            return 0

    @staticmethod
    def confirm_transaction(transaction_id, account_id):
        status = TransactionRepo.check_status_transaction(transaction_id)
        if status and status != program_variable.COMPLETED and \
                status != program_variable.CANCELED and status != program_variable.FAILED:
            qr = '''
                UPDATE Playbook SET outcome_account = (?), status = (?) WHERE transaction_id = (?)
                '''
            with sqlite3.connect(program_variable.DBPATH) as conn:
                c = conn.cursor()
                try:
                    c.execute(qr,(account_id, program_variable.CONFIRMED, transaction_id))
                except Exception as e:
                    return False
                else:
                    return True
        return False

    @staticmethod
    def confirm_expire(transaction_id):
        time.sleep(60 * 30)
        status = TransactionRepo.check_status_transaction(transaction_id)
        if status and status != program_variable.COMPLETED and \
                status != program_variable.CANCELED and status != program_variable.FAILED:
            qr = '''
                UPDATE Playbook SET status = (?) WHERE transaction_id = (?)
            '''
            c = conn.cursor()
            c.execute(qr, (program_variable.EXPIRED, transaction_id))

    @staticmethod
    def verify_transaction(transaction_id, account_id):
        status = TransactionRepo.check_status_transaction(transaction_id)
        if status and status != program_variable.COMPLETED and \
                status != program_variable.CANCELED and status != program_variable.FAILED:
            balance_qr = '''
                SELECT balance FROM Account WHERE account_id = (?)
            '''
            amount_qr = '''
                SELECT amount FROM Playbook WHERE transaction_id = (?)
            '''
            with sqlite3.connect(program_variable.DBPATH) as conn:
                c = conn.cursor()
                c.execute(balance_qr, (account_id,))
                balance = c.fetchone()[0]
                c.execute(amount_qr, (transaction_id,))
                amount = c.fetchone()[0]
                update_transaction_qr = '''
                    UPDATE Playbook SET status = (?) WHERE transaction_id = (?)
                '''
                if balance >= amount:
                    update_account_qr = '''
                        UPDATE Account SET balance = (?) WHERE account_id = (?)
                    '''
                    c.execute(update_account_qr, (balance - amount, account_id))
                    c.execute(update_transaction_qr, (program_variable.COMPLETED, transaction_id))
                    return True
                else:
                    c.execute(update_transaction_qr, (program_variable.FAILED, transaction_id))
        return False

    @staticmethod
    def cancel_transaction(transaction_id):
        status = TransactionRepo.check_status_transaction(transaction_id)
        if status and status != program_variable.COMPLETED and \
                status != program_variable.CANCELED and status != program_variable.FAILED:
            qr = '''
                UPDATE Playbook SET status = (?) WHERE transaction_id = (?)
            '''
            with sqlite3.connect(program_variable.DBPATH) as conn:
                c = conn.cursor()
                try:
                    c.execute(qr, (program_variable.CANCELED, transaction_id))
                except Exception as e:
                    return False
                else:
                    return True
        return False






