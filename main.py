from flask import Flask, request, jsonify
from nltk.corpus import wordnet as wn
from wordnet_functionality import WordNetFunctionality
import logging
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Prometheus Metriken
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
WORDNET_DURATION = Histogram('wordnet_operation_duration_seconds', 'Time taken for WordNet operations', ['operation'])

# Logging Setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

logger.info("Logging setup completed successfully")

app = Flask(__name__)
wnf = WordNetFunctionality()

@app.before_request
def suppress_metrics_logging():
    """Suppress logging for /metrics endpoint to avoid log spam."""
    if request.path == '/metrics':
        app.logger.disabled = True

@app.after_request
def restore_logging(response):
    """Restore logging after request is processed."""
    app.logger.disabled = False
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/baseform', methods=['POST'])
def get_baseform():
    start_time = time.time()
    try:
        data = request.get_json()
        word = data.get('word')
        pos = data.get('pos')
        logger.info("Looking for baseword: %s (POS: %s)", word, pos)
        
        operation_start_time = time.time()
        base_form = wnf.get_baseform(word, pos)
        WORDNET_DURATION.labels(operation='baseform').observe(time.time() - operation_start_time)
        
        logger.info("Baseword found: %s", base_form)
        REQUEST_COUNT.labels(method='POST', endpoint='/baseform', status='200').inc()
        return jsonify({"word": base_form})
    except Exception as e:
        logger.error("Error in baseform request: %s", str(e))
        REQUEST_COUNT.labels(method='POST', endpoint='/baseform', status='500').inc()
        return jsonify({"error": str(e)}), 500
    finally:
        REQUEST_LATENCY.labels(method='POST', endpoint='/baseform').observe(time.time() - start_time)

@app.route('/check_hypernym_tree', methods=['POST'])
def check_hypernym_tree():
    start_time = time.time()
    try:
        data = request.get_json()
        word = data.get('word')
        pos = data.get('pos')
        words_to_check = data.get('words_to_check')
        logger.info("Checking hypernym tree for word: %s (POS: %s), words to check: %s", word, pos, words_to_check)
        
        operation_start_time = time.time()
        result = wnf.check_hypernym_tree(word, pos, words_to_check)
        WORDNET_DURATION.labels(operation='hypernym_tree').observe(time.time() - operation_start_time)
        
        logger.info("Hypernym tree check result: %s", result)
        REQUEST_COUNT.labels(method='POST', endpoint='/check_hypernym_tree', status='200').inc()
        return jsonify({"status": "success" if result else "fail"})
    except Exception as e:
        logger.error("Error in hypernym tree check: %s", str(e))
        REQUEST_COUNT.labels(method='POST', endpoint='/check_hypernym_tree', status='500').inc()
        return jsonify({"error": str(e)}), 500
    finally:
        REQUEST_LATENCY.labels(method='POST', endpoint='/check_hypernym_tree').observe(time.time() - start_time)

@app.route('/derive_verb', methods=['POST'])
def derive_verb():
    start_time = time.time()
    try:
        data = request.get_json()
        noun = data.get('word')
        logger.info("Deriving verb for noun: %s", noun)
        
        operation_start_time = time.time()
        verb = wnf.deriveVerb(noun)
        WORDNET_DURATION.labels(operation='derive_verb').observe(time.time() - operation_start_time)
        
        logger.info("Verb derived: %s", verb)
        REQUEST_COUNT.labels(method='POST', endpoint='/derive_verb', status='200').inc()
        return jsonify({"word": verb})
    except Exception as e:
        logger.error("Error in verb derivation: %s", str(e))
        REQUEST_COUNT.labels(method='POST', endpoint='/derive_verb', status='500').inc()
        return jsonify({"error": str(e)}), 500
    finally:
        REQUEST_LATENCY.labels(method='POST', endpoint='/derive_verb').observe(time.time() - start_time)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    start_time = time.time()
    try:
        REQUEST_COUNT.labels(method='GET', endpoint='/healthcheck', status='200').inc()
        return jsonify({"Success": "Todo bien"})
    except Exception as e:
        logger.error("Error in healthcheck: %s", str(e))
        REQUEST_COUNT.labels(method='GET', endpoint='/healthcheck', status='500').inc()
        return jsonify({"error": str(e)}), 500
    finally:
        REQUEST_LATENCY.labels(method='GET', endpoint='/healthcheck').observe(time.time() - start_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
