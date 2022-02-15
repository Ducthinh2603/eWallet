from flask_restful import Resource, request
from models.merchant_model import MerchantModel
from ewalletv1.models.account_model import AccountModel
from ewalletv1.controllers import helper
from ewalletv1.viewers.merchant_viewer import MerchantViewer
from ewalletv1.viewers import common_message

class MerchantController(Resource):
    def post(self):
        rq = request.get_json()
        try:
            merchant = MerchantModel.add_merchant(rq['merchantName'],
                                                  rq['merchantUrl'])
        except Exception as e:
            return common_message.UNSUCCESSFUL_MESSAGE, 400
        else:
            return MerchantViewer.merchant_view(merchant)





