from ewalletv1.models.merchant_model import MerchantModel
from ewalletv1.viewers import common_message

class MerchantViewer:
    @staticmethod
    def merchant_view(merchant):
        if type(merchant) is MerchantModel:
            response = {
                "merchantName": merchant.merchant_name,
                "accountId": merchant.account_id,
                "merchantId": merchant.merchant_id,
                "apiKey": merchant.api_key,
                "merchantUrl": merchant.merchant_url
            }
            return response, 200
        return common_message.UNSUCCESSFUL_MESSAGE, 400