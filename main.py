from flask import Flask, request, jsonify
from nltk.corpus import wordnet as wn
from wordnet_functionality import WordNetFunctionality
import logging
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pythonjsonlogger import jsonlogger

# Prometheus Metriken
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
WORDNET_DURATION = Histogram('wordnet_operation_duration_seconds', 'Time taken for WordNet operations', ['operation'])

# Logging Setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler for Promtail
try:
    log_dir = '/app/logs'
    print(f"Creating log directory at: {log_dir}")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'application.log')
    print(f"Creating log file at: {log_file}")
    
    file_handler = logging.FileHandler(log_file)
    file_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    logger.info("Logging setup completed successfully")
except Exception as e:
    print(f"Error setting up file logging: {str(e)}")
    logger.error(f"Error setting up file logging: {str(e)}")

app = Flask(__name__)
wnf = WordNetFunctionality()

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
        logger.info("Looking for baseword", extra={"word": word, "pos": pos})
        
        operation_start_time = time.time()
        base_form = wnf.get_baseform(word, pos)
        WORDNET_DURATION.labels(operation='baseform').observe(time.time() - operation_start_time)
        
        logger.info("Baseword found", extra={"result": base_form})
        REQUEST_COUNT.labels(method='POST', endpoint='/baseform', status='200').inc()
        return jsonify({"word": base_form})
    except Exception as e:
        logger.error("Error in baseform request", extra={"error": str(e)})
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
        logger.info("Checking hypernym tree", extra={"word": word, "pos": pos, "words_to_check": words_to_check})
        
        operation_start_time = time.time()
        result = wnf.check_hypernym_tree(word, pos, words_to_check)
        WORDNET_DURATION.labels(operation='hypernym_tree').observe(time.time() - operation_start_time)
        
        logger.info("Hypernym tree check result", extra={"result": result})
        REQUEST_COUNT.labels(method='POST', endpoint='/check_hypernym_tree', status='200').inc()
        return jsonify({"status": "success" if result else "fail"})
    except Exception as e:
        logger.error("Error in hypernym tree check", extra={"error": str(e)})
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
        logger.info("Deriving verb", extra={"noun": noun})
        
        operation_start_time = time.time()
        verb = wnf.deriveVerb(noun)
        WORDNET_DURATION.labels(operation='derive_verb').observe(time.time() - operation_start_time)
        
        logger.info("Verb derived", extra={"result": verb})
        REQUEST_COUNT.labels(method='POST', endpoint='/derive_verb', status='200').inc()
        return jsonify({"word": verb})
    except Exception as e:
        logger.error("Error in verb derivation", extra={"error": str(e)})
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
        logger.error("Error in healthcheck", extra={"error": str(e)})
        REQUEST_COUNT.labels(method='GET', endpoint='/healthcheck', status='500').inc()
        return jsonify({"error": str(e)}), 500
    finally:
        REQUEST_LATENCY.labels(method='GET', endpoint='/healthcheck').observe(time.time() - start_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
