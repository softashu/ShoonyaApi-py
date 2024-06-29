from NorenApi import NorenApi
from com.ak.credentials import Credentials


def Shoonya_login():
    # credentials
    shoonyaCredentials = Credentials()
    api = NorenApi()
    app_key = shoonyaCredentials.shoonya_app_key
    # make the api call
    ret = api.login(userid=shoonyaCredentials.user,
                    password=shoonyaCredentials.pwd,
                    twoFA=shoonyaCredentials.factor2.now(),
                    vendor_code=shoonyaCredentials.vc,
                    api_secret=app_key,
                    imei=shoonyaCredentials.imei)
    print(ret)
    print(ret['susertoken'])
    print(api)


Shoonya_login()
