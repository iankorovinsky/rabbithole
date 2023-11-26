from flask import Flask, jsonify
import cohere
from serp import SerpGenerator
from flask import Flask, request
from flask_cors import CORS
from google.cloud import storage
import time

app = Flask(__name__)
#CORS(app, resources={r"/download_mp3": {"origins": "*"}, r"/get_question": {"origins": "*"}, r"/feedback": {"origins": "*"}})

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

# Create a transcriber object.

@app.route('/', methods=['GET', 'POST'])
def welcome():
    print("Hello Cohere!")
    return "Hello Cohere!"


@app.route('/initialize', methods=['GET', 'POST'])
def initialize():
    #Step 1: Scrape Links
    serp = SerpGenerator()
    print("Initialized SERP Generator, launching search")
    results = serp.generate(request.args["query"])
    print("Scraping links")
    links = serp.get_links(results)
    print(links)
    #Step 2: Embed Everything

    #should just return success
    return links



    


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=105)