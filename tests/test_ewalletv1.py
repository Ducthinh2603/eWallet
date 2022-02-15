import sqlite3

from ewalletv1.controllers import helper

transaction_id = "a9bca8d3-d44f-46d6-9c48-941fd2abd8b4"
qr = '''
    UPDATE Playbook SET outcome_account = NULL, status = 'INITIALIZED' WHERE transaction_id = (?)
    '''
# qr = '''
#       SELECT status FROM Playbook WHERE transaction_id = (?)
#       '''
with sqlite3.connect(helper.DBPATH) as conn:
  c = conn.cursor()
  c.execute(qr,(transaction_id,))
  rs = c.fetchone()
  print(rs)

# item = {
#   "merchantId": "b8c46ef5-e96a-431b-aff8-11a3529746aa",
#   "amount": 100,
#   "extraData": "Cart1",
#   "signature": "aef9d37e71e8bc28e5a9f24a4de2d2e4"
# }
# print(helper.signature_generator(**item))


