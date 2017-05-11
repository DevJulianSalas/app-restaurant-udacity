from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world test 1"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)