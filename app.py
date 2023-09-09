from flask import Flask, jsonify

app = Flask(__name__)

# Define a sample route that returns a JSON response
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

if __name__ == '__main__':
    app.run(debug=True)
