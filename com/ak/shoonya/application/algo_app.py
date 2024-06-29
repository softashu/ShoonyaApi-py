from flask import Flask, request

##############################################
#                   SERVER                   #
##############################################
app = Flask(__name__)


@app.route("/")
def hello_world():
    return 'Hello World 12'


@app.route("/ltp")
def getLtp():
    return "In the Ltp rest call"


def startServer():
    print("Inside startServer()")
    app.run()


if __name__ == "__main__":
    startServer()
