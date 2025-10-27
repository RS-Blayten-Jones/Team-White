from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/approved_jokes', methods=['GET'])
def get_approved_jokes():
    # Get token from Authorization header
    token = request.headers.get('Bearer')
    person = authenticationServer(token)

    jokeOperator=jokeOperations(person)
    filters={}
    jokeOperator.queryRecords(filters)
    