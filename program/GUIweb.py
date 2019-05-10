from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    msg = input("Hey, what's your name? ")
    msg = ("Hello {}".format(msg))
    return msg


if __name__ == '__main__':
    app.run(debug=True)