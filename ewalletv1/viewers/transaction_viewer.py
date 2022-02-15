from ewalletv1.models.transaction_model import TransactionModel
from ewalletv1.viewers import common_message
from ewalletv1.controllers import helper

class TransactionViewer:
    @staticmethod
    def transaction_view(transaction):
        if type(transaction) is TransactionModel:
            response = {
                "transactionId": transaction.transaction_id,
                "merchantId": transaction.merchant_id,
                "incomeAccount": transaction.income_account,
                "outcomeAccount": transaction.outcome_account if transaction.outcome_account else "NULL",
                "amount": transaction.amount,
                "extraData": transaction.extra_data,
                "status": transaction.status
            }
            signature = helper.signature_generator()
            response['signature'] = signature
            return response, 200
        return common_message.UNSUCCESSFUL_MESSAGE, 400