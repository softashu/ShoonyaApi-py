import logging

from api_helper import ShoonyaApiPy
from com.ak.credentials import Credentials

# enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

# start of our program
api = ShoonyaApiPy()

# credentials
shoonyaCredentials = Credentials()
uid = shoonyaCredentials.user
pwd = shoonyaCredentials.pwd
imei = shoonyaCredentials.imei
factor2 = shoonyaCredentials.factor2.now()
vc = shoonyaCredentials.vc
app_key = shoonyaCredentials.shoonya_app_key
# make the api call
try:
    # login to broker
    ret = api.login(userid=uid, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    print("Login success...")
    print(ret)
except Exception as e:
    logging.error('Login via API has issues : ')
    logging.error(e)