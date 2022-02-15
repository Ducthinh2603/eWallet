import sqlite3
from ewalletv1.models.account_model import AccountModel
from ewalletv1.controllers import helper

class MerchantModel:
    def __init__(self, merchant_id, merchant_name,
                 merchant_url, account_id, api_key):
        self.merchant_name = merchant_name
        self.merchant_id = merchant_id
        self.merchant_url = merchant_url
        self.account_id = account_id
        self.api_key = api_key

    @classmethod
    def add_merchant(cls, merchant_name, merchant_url):
        new_account = AccountModel.add_account("merchant")
        account_id = new_account.account_id
        merchant_id = helper.uuid_generator()
        api_key = helper.uuid_generator()
        add_merchant_qr = '''
            INSERT INTO Merchant VALUES (?,?,?,?,?)
            '''
        with sqlite3.connect(helper.DBPATH) as conn:
            c = conn.cursor()
            try:
                c.execute(add_merchant_qr, (merchant_id, merchant_name,
                                            merchant_url, account_id, api_key))
            except Exception:
                return helper.UNSUCCESSFUL_MESSAGE
            else:
                return cls(merchant_id, merchant_name,
                        merchant_url, account_id, api_key)



