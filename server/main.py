from flask import Flask, jsonify
import cohere
from serp import SerpGenerator
from flask import Flask, request
from flask_cors import CORS
from google.cloud import storage
import time
import generate_questions as questions

import cohere_sample as bot

app = Flask(__name__)
# CORS(app, resources={r"/download_mp3": {"origins": "*"}, r"/get_question": {"origins": "*"}, r"/feedback": {"origins": "*"}})

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

# Create a transcriber object.

documents = None


@app.route('/', methods=['GET', 'POST'])
def welcome():
    print("Hello Cohere!")
    return jsonify({"response": "Hello Cohere!"})


@app.route('/initialize', methods=['GET', 'POST'])
def initialize():
    # Step 1: Scrape Links
    serp = SerpGenerator()
    print("Initialized SERP Generator, launching search")
    results = serp.generate(request.args["query"])
    print("Scraping links")
    links = serp.get_links(results)
    print(links)
    # Step 2: Embed Everything

    # should just return success
    return jsonify({"response": "success"})


@app.route('/get_questions', methods=['GET', 'POST'])
def get_questions():
    initial_question = request.args["question"]
    print("Getting questions")
    response = questions.get_questions(initial_question)
    return jsonify({"response": response})


@app.route('/init_documents', methods=['POST'])
def init_documents():
    req = request.json
    sources = req["sources"]
    documents = bot.initDocuments(sources)

    return jsonify(success=True)


@app.route('/get_response', methods=['POST'])
def get_response():

    if documents is None:
        print("Documents not initialized")
        return jsonify(success=False)

    req = request.json
    message = req["message"]
    response = bot.getResponse(message, documents)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=105)
