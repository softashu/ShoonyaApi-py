import logging

from com.ak.shoonya import loginLogoutHandler

# enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

# start of our program
api = loginLogoutHandler.api
print("Logging out.............")
print(api.logout())