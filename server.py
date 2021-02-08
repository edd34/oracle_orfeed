from flask import Flask
from example_async import run

app = Flask(__name__)

@app.route('/arb')
def arb():
    return {"res": run()}, 200


if __name__=='__main__':
    app.run(debug=True)
