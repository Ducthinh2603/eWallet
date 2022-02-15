import sqlite3
from ewalletv1.controllers import helper
from flask_restful import Resource, request
from ewalletv1.models.transaction_model import TransactionModel
from ewalletv1.repositories.account_repo import AccountRepo
from ewalletv1.repositories.transaction_repo import TransactionRepo
from ewalletv1.viewers.transaction_viewer import TransactionViewer
from ewalletv1.viewers import common_message
from threading import Thread


class CreateTransactionController(Resource):
    @helper.jwt_required("merchant")
    def post(self):
        rq = request.get_json()
        if helper.check_signature(**rq):
            try:
                transaction = TransactionModel.create_transaction(rq["merchantId"], rq["amount"], rq["extraData"])
            except Exception as e:
                return common_message.MISSING_FIELD, 400
            else:
                return TransactionViewer.transaction_view(transaction)
        return common_message.INFO_DAMAGED


class ConfirmTransactionController(Resource):
    @helper.jwt_required("personal")
    def post(self):
        try:
            _id = request.get_json()['accountId']
            transaction_id = request.get_json()['transactionId']
        except Exception as e:
            return common_message.MISSING_FIELD, 400
        else:
            transaction = TransactionModel.get_transaction(transaction_id)
            if transaction.outcome_account:
                return common_message.UNAUTHORIZED_MESSAGE, 400
            else:
                rs = AccountRepo.get_account(_id)
                if rs:
                    account_id = rs[0]
                    if TransactionRepo.confirm_transaction(transaction_id, account_id):
                        t = Thread(target=TransactionRepo.confirm_expire, args=(transaction_id,))
                        t.start()
                        return common_message.SUCCESSFUL_MESSAGE, 200
                return common_message.UNSUCCESSFUL_MESSAGE, 400

class VerifyTransactionController(Resource):
    @helper.jwt_required("personal")
    def post(self):
        try:
            _id = request.get_json()['accountId']
            transaction_id = request.get_json()['transactionId']
        except Exception as e:
            return common_message.MISSING_FIELD, 400
        else:
            transaction = TransactionModel.get_transaction(transaction_id)
            if transaction:
                rs = AccountRepo.get_account(_id)
                if rs:
                    account_id = rs[0]
                    if TransactionRepo.verify_transaction(transaction_id, account_id):
                        return {
                            "message": "Transaction completed"
                        }, 200
            return common_message.UNSUCCESSFUL_MESSAGE, 400

class CancelTransactionController(Resource):
    @helper.jwt_required('personal')
    def post(self):
        try:
            _id = request.get_json()['accountId']
            transaction_id = request.get_json()['transactionId']
        except Exception as e:
            return common_message.MISSING_FIELD, 400
        else:
            transaction = TransactionModel.get_transaction(transaction_id)
            if transaction and TransactionRepo.cancel_transaction(transaction_id):
                return common_message.SUCCESSFUL_MESSAGE, 200
        return common_message.UNSUCCESSFUL_MESSAGE














