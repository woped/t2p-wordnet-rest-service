from flask import Flask, request, jsonify
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import logging

logging.basicConfig(
    level=logging.INFO
)
app = Flask(__name__)
lemmatizer = WordNetLemmatizer()

@app.route('/synonyms', methods=['GET'])
def get_synonyms():
    word = request.args.get('word')
    synonyms = []

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    synonyms = list(set(synonyms))
    return jsonify(synonyms)

@app.route('/baseform', methods=['POST'])
def get_baseform():
    data = request.get_json()
    word = data.get('word')
    pos = data.get('pos')
    logging.info(f"Looking for baseword of {word} ({pos})")
    base_form = lemmatizer.lemmatize(word, pos)
    logging.info(f"Returning: {base_form}")
    return jsonify({"word": base_form})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
