from ewalletv1.models.account_model import AccountModel
from ewalletv1.viewers import common_message

class AccountViewer:
    @staticmethod
    def account_view(account):
        if type(account) is AccountModel:
            response = {
                "accountType": account.account_type,
                "accountId": account.account_id,
                "balance": account.balance
            }
            return response, 200
        else:
            return common_message.UNSUCCESSFUL_MESSAGE, 400
