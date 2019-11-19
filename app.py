from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/clean')
def clean():
  to_return = {
    "result": True
  }
  print("Hit clean")
  return jsonify(to_return)
