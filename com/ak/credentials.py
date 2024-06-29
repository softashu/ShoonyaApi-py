import os

import getmac
import pyotp


class Credentials:
    user = os.environ['shoonya_user']
    pwd = os.environ['shoonya_api_pwd']
    # mac address of machine
    imei = getmac.get_mac_address()
    # vc vendor code in shoonya = userId_U
    vc = user + '_U'
    # Shoonya auth key for TOTP generation
    factor2 = pyotp.TOTP(os.environ['shoonya_factor2_key'])
    # shoonya Api key for api access
    shoonya_app_key = os.environ['shoonya_api_key']

    # Constructor
    def __init__(self):
        # Access the class variable
        pass
