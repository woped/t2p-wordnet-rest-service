from flask import Flask, request, jsonify
from nltk.corpus import wordnet as wn
from wordnet_functionality import WordNetFunctionality
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
wnf = WordNetFunctionality()

@app.route('/baseform', methods=['POST'])
def get_baseform():
    data = request.get_json()
    word = data.get('word')
    pos = data.get('pos')
    logging.info(f"Looking for baseword of {word} ({pos})")
    base_form = wnf.get_baseform(word, pos)
    logging.info(f"Returning: {base_form}")
    return jsonify({"word": base_form})

@app.route('/check_hypernym_tree', methods=['POST'])
def check_hypernym_tree():
    data = request.get_json()
    word = data.get('word')
    pos = data.get('pos')
    words_to_check = data.get('words_to_check')
    logging.info(f"Checking hypernym tree for {word} ({pos}) against {words_to_check}")
    result = wnf.check_hypernym_tree(word, pos, words_to_check)
    logging.info(f"Returning: {result}")
    return jsonify({"status": "success" if result else "fail"})

@app.route('/derive_verb', methods=['POST'])
def derive_verb():
    data = request.get_json()
    noun = data.get('word')
    logging.info(f"Deriving verb from {noun}")
    verb = wnf.deriveVerb(noun)
    logging.info(f"Returning: {verb}")
    return jsonify({"word": verb})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"Success": "Todo bien"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
