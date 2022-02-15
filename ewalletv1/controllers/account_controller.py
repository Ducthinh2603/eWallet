import uuid
from flask_restful import Resource, request
from ewalletv1.models.account_model import AccountModel
from ewalletv1.repositories.account_repo import AccountRepo
from ewalletv1.controllers import helper
from ewalletv1.viewers.account_viewer import AccountViewer
from ewalletv1.viewers import common_message
import jwt


class AccountController(Resource):
    def post(self):
        rq = request.get_json()
        try:
            new_account = AccountModel.add_account(rq['accountType'])
        except Exception:
            return common_message.MISSING_FIELD, 400
        else:
            return AccountViewer.account_view(new_account)


class AccountTokenController(Resource):
    def get(self, account_id):
       return AccountRepo.get_token(account_id)


class AccountTopupController(Resource):
    @helper.jwt_required("personal")
    def post(self, account_id):
        rq = request.get_json()
        try:
            amount = rq['amount']
        except Exception:
            return helper.UNSUCCESSFUL_MESSAGE, 401
        else:
            response = AccountRepo.topup_account(account_id, amount)
            return response
