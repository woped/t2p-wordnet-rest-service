from flask import Flask, request, jsonify
from nltk.corpus import wordnet

app = Flask(__name__)

@app.route('/synonyms', methods=['GET'])
def get_synonyms():
    word = request.args.get('word')
    synonyms = []

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    synonyms = list(set(synonyms))
    return jsonify(synonyms)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
