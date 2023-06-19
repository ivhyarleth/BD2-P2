from flask import Flask, request, Response
from flask_cors import CORS
from inverted_index import InvertedIndex
import json

app = Flask(__name__)
index = InvertedIndex()
CORS(app)

@app.route('/query/<int:id>', methods=["POST"])
def query(id):
    req = request.get_json()
    query_results = index.compare_query(req['query'])
    tweets = []
    for result in query_results[:id]:
        with open(result['docId'], encoding='utf-8') as f:
            file = json.load(f)
            tweets_ids = [r["tweets"] for r in result["results"]]
            for tweet_ids in tweets_ids:
                for tweet in tweet_ids:
                    for j in file:
                        if tweet['tweet_id'] == j['id']:
                            j['id'] = str(j['id'])
                            j['user_id'] = str(j['user_id'])
                            tweets.append(j)
    return Response(json.dumps(tweets), status=202, mimetype="application/json")

if __name__ == '__main__':
    index.initiate_inverted_index()
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host='127.0.0.1')
