from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter('login_requests_total', 'Total number of login requests', ['status_code'])
REQUEST_LATENCY = Histogram('login_request_latency_seconds', 'Latency of login requests in seconds')

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/login', methods=['POST'])
def login():
    start_time = time.time()
    # Simulate login logic
    if request.json.get('username') == 'user' and request.json.get('password') == 'pass':
        status_code = 200
        response = jsonify(message='Login successful'), status_code
    else:
        status_code = 400
        response = jsonify(message='Invalid credentials'), status_code

    # Update Prometheus metrics
    REQUEST_COUNT.labels(status_code=status_code).inc()
    REQUEST_LATENCY.observe(time.time() - start_time)

    return response

if __name__ == '__main__':
    from prometheus_client import start_http_server
    start_http_server(8000)
    app.run(port=5000)
