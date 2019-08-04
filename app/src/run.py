from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    from datetime import datetime
    return "hello, " + datetime.now().strftime('%Y/%m/%d %H:%M:%S')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
